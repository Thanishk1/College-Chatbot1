import json
import re
import unicodedata
from typing import List, Dict, Any

# Load JSON Files
def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Fix Unicode Issues & Text Formatting
def clean_text(text: str) -> str:
    """Normalize and clean text."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text).replace("\n", " ").strip()
    text = re.sub(r"\u2013", "-", text)  # Replace en-dash with hyphen
    return text

# Generate Question Variations
def generate_question_variations(base_question: str, variations: List[str]) -> List[str]:
    """Generate multiple question variations for a base question."""
    return [base_question] + variations

# Round CTC values to whole numbers
def round_ctc_values(placement_data: Dict[str, Any]) -> Dict[str, Any]:
    """Round all CTC values in the placement dataset to the nearest whole number."""
    for company in placement_data.get("companies", []):
        ctc_lpa = company.get("ctc_lpa", "0")
        try:
            ctc_lpa_rounded = str(round(float(ctc_lpa)))  # Round to nearest whole number
            company["ctc_lpa"] = ctc_lpa_rounded
        except (ValueError, TypeError):
            company["ctc_lpa"] = "0"  # Default to 0 if CTC is invalid
    return placement_data

# Generate Placement Q&A
def generate_placement_queries(placement_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate Q&A pairs for placement data."""
    placement_queries = []
    companies = placement_data.get("companies", [])
    
    # Sort companies by CTC in descending order
    def get_ctc_value(company):
        ctc = company.get("ctc_lpa", "0")
        try:
            return float(ctc)
        except (ValueError, TypeError):
            return 0.0  # Default to 0 if CTC is invalid

    sorted_companies = sorted(companies, key=get_ctc_value, reverse=True)
    
    # Generate queries for each company
    for company in sorted_companies:
        company_name = clean_text(company.get("name", "Unknown Company"))
        students_placed = clean_text(str(company.get("total_selected", "N/A")))
        ctc_lpa = clean_text(company.get("ctc_lpa", "N/A"))

        if company_name and students_placed and ctc_lpa:
            # Base question and variations for placement count
            base_question = f"How many students were placed in {company_name}?"
            variations = [
                f"What is the placement count for {company_name}?",
                f"How many students got placed in {company_name}?",
                f"Tell me the number of students placed in {company_name}.",
                f"What is the total number of students placed in {company_name}?",
            ]
            questions = generate_question_variations(base_question, variations)

            for question in questions:
                placement_queries.append({
                    "question": question,
                    "answer": f"{students_placed} students were placed in {company_name} with a salary package of {ctc_lpa} LPA."
                })

    # Generate queries for highest package
    if sorted_companies:
        highest_package_company = sorted_companies[0]
        highest_company_name = clean_text(highest_package_company.get("name", "Unknown Company"))
        highest_ctc = clean_text(highest_package_company.get("ctc_lpa", "N/A"))

        base_question = "Which company offered the highest package?"
        variations = [
            "What is the highest CTC offered?",
            "Which company has the highest salary package?",
            "Tell me the company with the highest CTC.",
            "What is the top salary package offered?",
        ]
        questions = generate_question_variations(base_question, variations)

        for question in questions:
            placement_queries.append({
                "question": question,
                "answer": f"{highest_company_name} offered the highest package of {highest_ctc} LPA."
            })

    # Generate queries for companies above whole number CTC thresholds
    ctc_thresholds = sorted(list(set([round(get_ctc_value(c)) for c in sorted_companies])), reverse=True)
    for threshold in ctc_thresholds:
        base_question = f"List companies with CTC above {threshold} LPA."
        variations = [
            f"Which companies have CTC exceeding {threshold} LPA?",
            f"Show companies offering more than {threshold} LPA.",
            f"Who are the companies with packages above {threshold} LPA?"
        ]
        questions = generate_question_variations(base_question, variations)
        
        above_threshold = [
            clean_text(c.get("name", "Unknown Company"))
            for c in sorted_companies 
            if get_ctc_value(c) >= threshold
        ]
        
        for question in questions:
            placement_queries.append({
                "question": question,
                "answer": f"The companies offering above {threshold} LPA are: {', '.join(above_threshold)}."
            })

    return placement_queries

# Generate Academic Schedule Q&A
def generate_academic_queries(academic_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate Q&A pairs for academic schedule."""
    academic_queries = []
    for event in academic_data:
        event_name = clean_text(event.get("Particulars", "Unknown Event"))
        odd_semester = clean_text(event.get("ODD SEMESTER", "N/A"))
        even_semester = clean_text(event.get("EVEN SEMESTER", "N/A"))

        if event_name and odd_semester and even_semester:
            base_question = f"When is {event_name}?"
            variations = [
                f"What is the date for {event_name}?",
                f"Tell me the schedule for {event_name}.",
                f"When does {event_name} happen?",
                f"Can you tell me when {event_name} is scheduled?",
            ]
            questions = generate_question_variations(base_question, variations)

            for question in questions:
                academic_queries.append({
                    "question": question,
                    "answer": f"{event_name} is scheduled in Odd Semester: {odd_semester}, Even Semester: {even_semester}."
                })
    return academic_queries

# Generate Faculty Q&A
def generate_faculty_queries(faculty_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate Q&A pairs for faculty data."""
    faculty_queries = []
    department_faculty_map = {}

    for faculty in faculty_data:
        name = clean_text(faculty.get("name", "Unknown Faculty"))
        department = clean_text(faculty.get("department", "Unknown Department"))

        if name and department:
            # Variations for "Who is [name]?"
            base_question = f"Who is {name}?"
            variations = [
                f"Can you tell me about {name}?",
                f"Tell me about {name}.",
                f"Who is the faculty member {name}?",
                f"Give me information about {name}.",
            ]
            questions = generate_question_variations(base_question, variations)

            for question in questions:
                faculty_queries.append({
                    "question": question,
                    "answer": f"{name} is a faculty member in the {department} department."
                })

            # Variations for "Which department does [name] belong to?"
            base_question = f"Which department does {name} belong to?"
            variations = [
                f"In which department is {name}?",
                f"Which department is {name} part of?",
                f"Tell me the department of {name}.",
                f"Where does {name} work?",
            ]
            questions = generate_question_variations(base_question, variations)

            for question in questions:
                faculty_queries.append({
                    "question": question,
                    "answer": f"{name} belongs to the {department} department."
                })

            department_faculty_map.setdefault(department, []).append(name)

    for dept, faculty_list in department_faculty_map.items():
        base_question = f"List all faculty members in the {dept} department."
        variations = [
            f"Who are the faculty members in the {dept} department?",
            f"Can you list the faculty in the {dept} department?",
            f"Tell me the faculty members in the {dept} department.",
            f"Who works in the {dept} department?",
        ]
        questions = generate_question_variations(base_question, variations)

        for question in questions:
            faculty_queries.append({
                "question": question,
                "answer": f"Faculty in {dept}: {', '.join(faculty_list)}."
            })

    return faculty_queries

# Main Function to Generate Q&A Dataset
def generate_qa_dataset(academic_data: List[Dict[str, Any]],
                        placement_data: Dict[str, Any],
                        faculty_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate the final Q&A dataset."""
    # Round CTC values before generating queries
    placement_data = round_ctc_values(placement_data)
    
    academic_queries = generate_academic_queries(academic_data)
    placement_queries = generate_placement_queries(placement_data)
    faculty_queries = generate_faculty_queries(faculty_data)

    # Combine all Q&A pairs
    final_qa_pairs = academic_queries + placement_queries + faculty_queries
    return final_qa_pairs

# Save Q&A Dataset
def save_qa_dataset(qa_pairs: List[Dict[str, str]], output_file: str) -> None:
    """Save the Q&A dataset to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(qa_pairs, f, indent=4)
    print(f"✅ Q&A dataset saved as {output_file}")

# Load Data Files
academic_data = load_json("data/academic_schedule.json")
placement_data = load_json("data/placement_data.json")
faculty_data = load_json("data/faculty_data.json")

# Generate Q&A Dataset
final_qa_pairs = generate_qa_dataset(academic_data, placement_data, faculty_data)

# Save Q&A Dataset
output_file = "final_qa_pairs1.json"
save_qa_dataset(final_qa_pairs, output_file)