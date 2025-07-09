import pandas as pd
import json

df = pd.read_csv("data/cleaned_placement_details.csv", skiprows=4)  
df.columns = df.iloc[0] 
df = df[1:].reset_index(drop=True)  
df.columns = df.columns.str.strip()  

print("Updated Column Names:", df.columns.tolist())

company_column = "Name of the Organization"
ctc_column = "(LPA)" 

placement_data = {
    "total_placed": {},
    "companies": []
}

for col in df.columns[2:-2]:  
    placement_data["total_placed"][col] = df.iloc[-2][col]  

for index, row in df[:-2].iterrows():
    company_info = {
        "name": row[company_column],  
        "branch_wise": {col: row[col] for col in df.columns[2:-2]},
        "total_selected": row["Selected"],
        "ctc_lpa": row[ctc_column]
    }
    placement_data["companies"].append(company_info)

with open("data/placement_data.json", "w", encoding="utf-8") as f:
    json.dump(placement_data, f, indent=4)

print(" JSON data saved as placement_data.json")
