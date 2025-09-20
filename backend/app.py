from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import fitz  # PyMuPDF
import docx
import spacy
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)

# Load spacy and sentence-transformer models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def extract_text_from_pdf(file_stream):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_stream):
    doc = docx.Document(file_stream)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text(file):
    if file.filename.endswith('.pdf'):
        return extract_text_from_pdf(file.stream)
    elif file.filename.endswith('.docx'):
        return extract_text_from_docx(file.stream)
    elif file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        try:
            return file.read().decode('utf-8')
        except UnicodeDecodeError:
            return "Unsupported file type or encoding."

def extract_keywords_from_jd(jd_text):
    doc = nlp(jd_text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    keywords.extend([chunk.text for chunk in doc.noun_chunks])
    return list(set([keyword.lower() for keyword in keywords]))

def get_fit_verdict(score):
    if score >= 70:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"

def calculate_relevance(jd_text, resume_text):
    jd_keywords = extract_keywords_from_jd(jd_text)
    
    resume_text_lower = resume_text.lower()
    
    found_skills = [skill for skill in jd_keywords if skill in resume_text_lower]
    missing_skills = [skill for skill in jd_keywords if skill not in resume_text_lower]
    
    # Semantic similarity score
    embedding1 = model.encode(jd_text, convert_to_tensor=True)
    embedding2 = model.encode(resume_text, convert_to_tensor=True)
    semantic_similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
    
    # Keyword score
    keyword_score = (len(found_skills) / len(jd_keywords)) * 100 if jd_keywords else 0
    
    # Combined score (weighted)
    score = (semantic_similarity * 100 * 0.6) + (keyword_score * 0.4)
    score = min(100, score) # Ensure score is not more than 100

    feedback = f"Your resume has a good alignment with the job description. To improve further, consider adding the following skills: {', '.join(missing_skills[:3])}." if missing_skills else "Your resume is a great fit for this role!"

    return score, found_skills, missing_skills, feedback

@app.route('/')
def index():
    return "Resume Relevance Checker API"

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'jd' not in request.files:
        return jsonify({"error": "No job description file"}), 400
    
    jd_file = request.files['jd']
    
    if jd_file.filename == '':
        return jsonify({"error": "No selected job description file"}), 400

    jd_text = ""
    if jd_file:
        jd_text = extract_text(jd_file)

    if 'resumes' not in request.files:
        return jsonify({"error": "No resume files"}), 400

    resume_files = request.files.getlist('resumes')

    if not resume_files or all(f.filename == '' for f in resume_files):
        return jsonify({"error": "No selected resume files"}), 400

    resumes_data = []
    for resume in resume_files:
        if resume:
            resume_text = extract_text(resume)
            score, found_skills, missing_skills, feedback = calculate_relevance(jd_text, resume_text)
            fit_verdict = get_fit_verdict(score)
            
            resumes_data.append({
                "filename": resume.filename,
                "score": round(score, 2),
                "fit_verdict": fit_verdict,
                "found_skills": found_skills,
                "missing_skills": missing_skills,
                "feedback": feedback
            })

    resumes_data.sort(key=lambda x: x['score'], reverse=True)

    return jsonify({
        "job_description": {
            "filename": jd_file.filename,
        },
        "results": resumes_data
    })

if __name__ == '__main__':
    app.run(debug=True)