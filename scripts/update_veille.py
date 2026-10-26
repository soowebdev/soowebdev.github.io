import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta, timezone

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
            
            # On cherche les blocs "timeline-entry"
            entries = soup.find_all('div', class_='timeline-entry')[:3]
            
            for entry in entries:
                # Extraction de la date
                time_tag = entry.find('time')
                date = time_tag.get_text().strip() if time_tag else datetime.now().strftime("%d %B %Y")
                
                # Extraction du nom (dans le h2, après l'icône et la pastille)
                h2 = entry.find('h2')
                if h2:
                    # On récupère tout le texte et on nettoie les symboles
                    full_name = h2.get_text().strip()
                    # On enlève la pastille (🟢, 🟠, 🔴) et l'espace insécable si présent
                    name = full_name.replace('🟢', '').replace('🟠', '').replace('🔴', '').strip()
                    # On nettoie les éventuels espaces bizarres (&nbsp;)
                    name = name.replace('\xa0', ' ')
                else:
                    name = "Inconnu"
                
                # Extraction de la description (premier paragraphe ou liste d'atouts)
                desc_tag = entry.find('p')
                if desc_tag:
                    desc = desc_tag.get_text().strip()
                    if not desc and entry.find('ul'):
                        # Si le p est vide, on prend les premiers éléments de la liste
                        items = [li.get_text().strip() for li in entry.find('ul').find_all('li')[:2]]
                        desc = "Données : " + ", ".join(items)
                else:
                    desc = "Nouvelle fuite de données répertoriée."

                if name and name != "Inconnu":
                    leaks.append({
                        "source": name,
                        "date": date,
                        "description": desc[:100] + "..." if len(desc) > 100 else desc
                    })
            
            print(f"Trouvé {len(leaks)} fuites.")
    except Exception as e:
        print(f"Erreur BonjourLaFuite: {e}")

    # 2. Dépôts GitHub créés cette semaine qui gagnent le plus d'étoiles
    repos = []
    try:
        print("Recherche des dépôts en hausse sur GitHub...")
        since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%d')
        api_headers = {'Accept': 'application/vnd.github+json'}
        if os.environ.get('GITHUB_TOKEN'):
            api_headers['Authorization'] = f"Bearer {os.environ['GITHUB_TOKEN']}"
        response = requests.get(
            'https://api.github.com/search/repositories',
            params={'q': f'created:>{since}', 'sort': 'stars', 'order': 'desc', 'per_page': 3},
            headers=api_headers, timeout=10)
        response.raise_for_status()
        for repo in response.json().get('items', []):
            desc = repo.get('description') or "Pas de description."
            repos.append({
                "name": repo['full_name'],
                "url": repo['html_url'],
                "description": desc[:100] + "..." if len(desc) > 100 else desc
            })
        print(f"Trouvé {len(repos)} dépôts.")
    except Exception as e:
        print(f"Erreur API GitHub: {e}")

    # Back-up au cas où la scraping échoue (Mis à jour avec les dernières fuites réelles)
    if not leaks:
        leaks = [
            {"source": "Jeu Jouet", "date": "17 Avril 2026", "description": "Fuite confirmée impactant les données clients."},
            {"source": "Brit Hotel", "date": "17 Avril 2026", "description": "Noms, emails, téléphones et réservations exposés."},
            {"source": "Police Nationale", "date": "16 Avril 2026", "description": "170 000 agents concernés via e-Campus."}
        ]

    # 3. Mise à jour du fichier JSON 
    data = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "leaks": leaks, "repos": repos}
    os.makedirs('data', exist_ok=True)
    with open('data/veille.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_veille()
