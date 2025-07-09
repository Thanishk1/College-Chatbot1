import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

with open('final_qa_pairs1.json', 'r') as f:
    qa_pairs = json.load(f)

questions = [pair['question'].lower().strip() for pair in qa_pairs]
answers = [pair['answer'] for pair in qa_pairs]

model = SentenceTransformer('all-MiniLM-L6-v2')
question_embeddings = model.encode(questions, normalize_embeddings=True)

dimension = question_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(question_embeddings)

test_cases = [
    {
        "question": "When is the Mid Semester Examination-1 (MSE-I)?",
        "expected_answer": "Mid Semester Examination-1 (MSE-I) is scheduled in Odd Semester: 09.09.2024 to 18.09.2024, Even Semester: 17.02.2025 to 24.02.2025."
    },
    {
        "question": "How many students got placed in ORACLE?",
        "expected_answer": "3 students were placed in ORACLE with a salary package of 14.00 LPA."
    },
    {
        "question": "What is the schedule for the commencement of classwork?",
        "expected_answer": "COMMENCEMENT OF CLASSWORK is scheduled in Odd Semester: 22.07.2024 (Monday), Even Semester: 20.12.2024 (Friday)."
    },
    {
        "question": "When is the Sankranthi vacation?",
        "expected_answer": "SANKRANTHI VACATION is scheduled in Odd Semester: --, Even Semester: 13.01.2025 to 19.01.2025."
    },
    {
        "question": "Tell me the schedule for the cultural fest Sanskriti.",
        "expected_answer": "CULTURALFEST - SANSKRITI is scheduled in Odd Semester: --, Even Semester: 07.02.2025 & 08.02.2025."
    }
]


correct_predictions = 0

for test in test_cases:
    query_embedding = model.encode([test["question"].lower().strip()], normalize_embeddings=True)
    distances, indices = index.search(query_embedding, k=1)  # Get top match
    retrieved_answer = answers[indices[0][0]]
    
    if retrieved_answer.lower().strip() == test["expected_answer"].lower().strip():
        correct_predictions += 1

accuracy = (correct_predictions / len(test_cases)) * 100
print(f"Model Accuracy: {accuracy:.2f}%")
