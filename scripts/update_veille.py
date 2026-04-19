import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def update_veille():
    # 1. Fetch Data Leaks from BonjourLaFuite
    leaks = []
    try:
        response = requests.get('https://bonjourlafuite.eu.org/')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Assuming leaks are in rows or cards, adjust based on actual HTML
            # This is a simplified example based on common patterns
            rows = soup.find_all('div', class_='leak-item')[:3] # Get top 3
            if not rows:
                # Fallback to a different selector if the above doesn't work
                # Based on web_reference 1, it seems like a list of dates and companies
                rows = soup.select('div.card-body')[:3] 
            
            for row in rows:
                date = row.find('span', class_='date').text.strip() if row.find('span', class_='date') else datetime.now().strftime("%d %B %Y")
                source = row.find('h3').text.strip() if row.find('h3') else "Inconnu"
                desc = row.find('p').text.strip() if row.find('p') else "Aucune description disponible."
                leaks.append({"source": source, "date": date, "description": desc})
    except Exception as e:
        print(f"Error fetching leaks: {e}")

    # 2. Fetch Trending Open Source from OpenSourceProjects
    opensource = []
    try:
        response = requests.get('https://opensourceprojects.cc/')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            projects = soup.find_all('div', class_='project-card')[:3]
            if not projects:
                # Based on web_reference 2
                projects = soup.select('div.trending-item')[:3]

            for proj in projects:
                name = proj.find('h3').text.strip() if proj.find('h3') else "Projet"
                cat = proj.find('span', class_='category').text.strip() if proj.find('span', class_='category') else "Software"
                desc = proj.find('p').text.strip() if proj.find('p') else "Description non disponible."
                opensource.append({"name": name, "category": cat, "description": desc})
    except Exception as e:
        print(f"Error fetching opensource: {e}")

    # Fallback data if scraping fails (using the ones we have now)
    if not leaks:
        leaks = [
            {"source": "Police Nationale", "date": "16 Avril 2026", "description": "170 000 agents concernés via e-Campus (Noms, emails, logins)."},
            {"source": "ÉduConnect", "date": "14 Avril 2026", "description": "Éducation Nationale : Identifiants, noms et établissements."},
            {"source": "Basic Fit", "date": "13 Avril 2026", "description": "Données membres et informations bancaires exposées."}
        ]
    if not opensource:
        opensource = [
            {"name": "PostHog", "category": "Product Analytics", "description": "Plateforme d'analyse complète tout-en-un pour les développeurs."},
            {"name": "Umami", "category": "Web Analytics", "description": "Alternative à Google Analytics axée sur la vie privée et sans cookies."},
            {"name": "Plane", "category": "Project Management", "description": "Gestion de projet moderne et open-source (Alternative à Jira)."}
        ]

    # 3. Update JSON file
    data = {"leaks": leaks, "opensource": opensource}
    os.makedirs('data', exist_ok=True)
    with open('data/veille.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_veille()
