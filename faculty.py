import requests
from bs4 import BeautifulSoup
import json

department_urls = {
    'CSE': 'https://kitsw.rlabs.in/cse.php',
    'ECE': 'https://kitsw.rlabs.in/ece.php',
    'EEE': 'https://kitsw.rlabs.in/eee.php',
    'CE': 'https://kitsw.rlabs.in/civ.php',
    'MH': 'https://kitsw.rlabs.in/mh.php',
    'CSN': 'https://kitsw.rlabs.in/csn.php',
    'CSM':'https://kitsw.rlabs.in/csm.php',
}

def scrape_faculty():
    faculty_data = []
    for dept, url in department_urls.items():
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Failed to access {url}")
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        faculty_list = soup.find_all('td')
        for td in faculty_list:
            a_tag = td.find('a')
            if a_tag and a_tag.text.strip():
                name = a_tag.text.strip()
                if "@kitsw.ac.in" not in name:
                    faculty_data.append({"name": name, "department": dept})
    with open('data/faculty_data.json', 'w', encoding='utf-8') as f:
        json.dump(faculty_data, f, indent=4)
    print("✅ Faculty data saved successfully!")

scrape_faculty()
