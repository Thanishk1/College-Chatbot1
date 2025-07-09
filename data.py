import pdfplumber
import pandas as pd
import json

# ✅ Extract tables from PDF
def extract_tables_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    data.append(row)
    return data

# ✅ Save extracted tables to CSV
def save_to_csv(data, output_csv):
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"✅ Data saved to {output_csv}")

# ✅ Clean CSV Data
def clean_csv(csv_path, output_path):
    df = pd.read_csv(csv_path)
    df.columns = [col.strip() for col in df.columns]  # Remove extra spaces
    df.replace(to_replace=r"\nInternship", value=" Internship", regex=True, inplace=True)
    df.fillna("-", inplace=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ Cleaned data saved as {output_path}")

# ✅ Convert CSV to JSON
def convert_csv_to_json(csv_path, json_path):
    column_names = ["S. No.", "Particulars", "ODD SEMESTER", "EVEN SEMESTER"]
    df = pd.read_csv(csv_path, names=column_names, skiprows=1)
    data = df.to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Converted CSV to JSON: {json_path}")

# ✅ Process Placement Data
def process_placements(pdf_path, csv_path, json_path):
    data = extract_tables_from_pdf(pdf_path)
    save_to_csv(data, csv_path)
    clean_csv(csv_path, "cleaned_placement_details.csv")
    convert_csv_to_json("cleaned_placement_details.csv", json_path)

# ✅ Process Almanac Data
def process_almanac(pdf_path, csv_path, json_path):
    data = extract_tables_from_pdf(pdf_path)
    save_to_csv(data, csv_path)
    convert_csv_to_json(csv_path, json_path)

# ✅ File Paths (Update paths as needed)
process_placements(r"D:\college_chatbot3\2024-25 Placement Details.pdf", "placement_details.csv", "placement_data.json")
process_almanac(r"D:\\college_chatbot3\250A_Almanac of B.Tech. A.Y. 2024-25_20.08.2024_Revised.pdf", "academic_schedule.csv", "academic_schedule.json")
