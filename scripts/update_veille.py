import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def update_veille():
    # Simulation d'un vrai navigateur pour éviter d'être bloqué (CORS/User-Agent)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    # 1. Ajouter les data leak depuis BonjourLaFuite
    leaks = []
    try:
        print("Scraping BonjourLaFuite...")
        response = requests.get('https://bonjourlafuite.eu.org/', headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Recherche des cartes de fuites (basé sur la structure réelle du site)
            items = soup.find_all(['h3', 'div'], class_=['card-body', 'leak-item'])[:3]
            
            # Si le sélecteur spécifique échoue, on cherche par texte
            if not items:
                # Fallback simple sur les h3 qui contiennent souvent les noms d'entreprises
                items = soup.find_all('h3')[:3]

            for item in items:
                source = item.get_text().strip().replace('🟢', '').replace('🟠', '').replace('🔴', '').strip()
                # On essaie de trouver une date proche
                date_tag = item.find_previous('h2') or item.find_previous('span', class_='date')
                date = date_tag.get_text().strip() if date_tag else datetime.now().strftime("%d %B %Y")
                leaks.append({
                    "source": source,
                    "date": date,
                    "description": "Dernière fuite confirmée ou revendiquée sur le site."
                })
            print(f"Trouvé {len(leaks)} fuites.")
    except Exception as e:
        print(f"Erreur BonjourLaFuite: {e}")

    # 2. Ajouter les projets tendants depuis OpenSourceProjects
    opensource = []
    try:
        print("Scraping OpenSourceProjects...")
        response = requests.get('https://opensourceprojects.cc/', headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Recherche des projets (basé sur les tendances)
            projects = soup.select('div.trending-item, div.project-card')[:3]
            
            if not projects:
                # Fallback sur les liens ou titres h3
                projects = soup.find_all('h3')[:3]

            for proj in projects:
                name = proj.get_text().strip()
                cat_tag = proj.find_next('span', class_='category')
                cat = cat_tag.get_text().strip() if cat_tag else "Open Source"
                desc_tag = proj.find_next('p')
                desc = desc_tag.get_text().strip() if desc_tag else "Projet open-source en tendance actuellement."
                opensource.append({
                    "name": name,
                    "category": cat,
                    "description": desc[:100] + "..." if len(desc) > 100 else desc
                })
            print(f"Trouvé {len(opensource)} projets.")
    except Exception as e:
        print(f"Erreur OpenSourceProjects: {e}")

    # Back-up au cas où la scraping échoue
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

    # 3. Mise à jour du fichier JSON 
    data = {"leaks": leaks, "opensource": opensource}
    os.makedirs('data', exist_ok=True)
    with open('data/veille.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_veille()
