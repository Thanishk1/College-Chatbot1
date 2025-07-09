from flask import Flask, request, jsonify, render_template
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
with open('final_qa_pairs1.json', 'r') as f:
    qa_pairs = json.load(f)
questions = [pair['question'].lower().strip() for pair in qa_pairs]
answers = [pair['answer'] for pair in qa_pairs]
model = SentenceTransformer('all-MiniLM-L6-v2')
question_embeddings = model.encode(questions, normalize_embeddings=True)
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(question_embeddings)
SIMILARITY_THRESHOLD = 0.7  
TOP_K = 5  

def get_answer(query):
    query_embedding = model.encode([query.lower().strip()], normalize_embeddings=True)
    distances, indices = index.search(query_embedding, k=TOP_K)
    
    best_match_score = distances[0][0]
    best_match_idx = indices[0][0]
    
    if best_match_score >= SIMILARITY_THRESHOLD:
        return {"answer": answers[best_match_idx], "similar_questions": []}
    else:
        similar_questions = [questions[idx] for idx in indices[0]]
        return {"answer": None, "similar_questions": similar_questions}



@app.route('/')
def home():
    return render_template('index.html')  # Serve HTML file
@app.route('/query', methods=['POST'])
def query_bot():
    data = request.json
    user_query = data.get("query", "").strip()
    
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    response = get_answer(user_query)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
