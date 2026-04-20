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
            # On cherche les lignes de fuites (souvent dans des colonnes col-md-10)
            # On va cibler les éléments qui contiennent les pastilles de statut et qui sont suivis par un nom
            
            seen = set()
            # On cherche les éléments qui commencent par une pastille
            for tag in soup.find_all(['div', 'span', 'td']):
                text = tag.get_text().strip()
                if text and (text.startswith('🟢') or text.startswith('🟠') or text.startswith('🔴')):
                    name = text.replace('🟢', '').replace('🟠', '').replace('🔴', '').strip()
                    # On filtre pour ne pas prendre de phrases trop longues ou de doublons
                    if name and name not in seen and len(name) < 40:
                        seen.add(name)
                        # On cherche la date dans le même bloc ou le bloc précédent
                        # Souvent la date est dans un col-md-2 juste avant
                        date = datetime.now().strftime("%d %B %Y")
                        prev_tag = tag.find_previous(['div', 'span', 'td'], class_='col-md-2')
                        if prev_tag:
                            date = prev_tag.get_text().strip()
                        
                        leaks.append({
                            "source": name,
                            "date": date,
                            "description": "Nouvelle fuite de données répertoriée."
                        })
                if len(leaks) >= 3: break
            
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
            # On cherche les projets dans la section "Trending"
            # Les noms de projets sont souvent dans des h3 ou des liens forts
            for trending_item in soup.select('div.trending-item, .project-card')[:3]:
                name_tag = trending_item.find(['h3', 'h4', 'a'])
                if name_tag:
                    name = name_tag.get_text().strip().split('🦔')[0].strip() # Nettoyage si icône accolée
                    cat_tag = trending_item.find(['span', 'div'], class_='category')
                    cat = cat_tag.get_text().strip() if cat_tag else "Software"
                    desc_tag = trending_item.find('p')
                    desc = desc_tag.get_text().strip() if desc_tag else "Projet open-source en tendance."
                    
                    if name and len(name) < 40:
                        opensource.append({
                            "name": name,
                            "category": cat,
                            "description": desc[:100] + "..." if len(desc) > 100 else desc
                        })
            
            # Fallback si les sélecteurs CSS ont échoué
            if not opensource:
                for h3 in soup.find_all('h3')[:3]:
                    name = h3.get_text().strip().split('🦔')[0].strip()
                    if name and len(name) < 30:
                        opensource.append({
                            "name": name,
                            "category": "Open Source",
                            "description": "Projet en tendance sur la plateforme."
                        })
            
            print(f"Trouvé {len(opensource)} projets.")
    except Exception as e:
        print(f"Erreur OpenSourceProjects: {e}")

    # Back-up au cas où la scraping échoue (Mis à jour avec les dernières fuites réelles)
    if not leaks:
        leaks = [
            {"source": "Jeu Jouet", "date": "17 Avril 2026", "description": "Fuite confirmée impactant les données clients."},
            {"source": "Brit Hotel", "date": "17 Avril 2026", "description": "Noms, emails, téléphones et réservations exposés."},
            {"source": "Police Nationale", "date": "16 Avril 2026", "description": "170 000 agents concernés via e-Campus."}
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
