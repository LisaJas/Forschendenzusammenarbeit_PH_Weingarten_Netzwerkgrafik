import csv
import json
from bs4 import BeautifulSoup

# Funktion, um die CSV-Datei zu lesen und die Verbindungen zu extrahieren
def read_csv(csv_file):
    coauthors = []
    researchers_info = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            coauthors.append({
                'author1_id': row['author1_id'],
                'author2_id': row['author2_id'],
                'publication_id': row['publication_id']
            })

            if row['author1_id'] not in researchers_info:
                researchers_info[row['author1_id']] = {
                    'user_id': row['author1_id'],
                    'user_name': row['author1_name'].title(),
                    'vorname': row['author1_vorname'].title(),
                    'nachname': row['author1_nachname'].title(),
                    'funktion': row['author1_funktion'],
                    'institut': row['author1_institut'],
                    'publications': []
                }
    return coauthors, researchers_info

# Funktion, um die Publikationen aus der XML-Datei zu extrahieren
def parse_publications(xml_file):
    publications = {}
    researchers_info = {}
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'xml')

    # Parse the publications
    for pub in soup.find_all('publikation'):
        pub_id = pub['id']
        title = pub.find('titel_beitrag').text if pub.find('titel_beitrag') else ''
        year = pub.find('jahr').text if pub.find('jahr') else ''
        publications[pub_id] = {'title': title, 'year': year}

    # Parse the researcher information with titles
    for user in soup.find_all('user'):
        user_id = user['id']
        vorname = user.find('vorname').text if user.find('vorname') else ''
        nachname = user.find('nachname').text if user.find('nachname') else ''
        institut = user.find('institut').text if user.find('institut') else ''
        
        researchers_info[user_id] = {
            'user_id': user_id,
            'vorname': vorname,
            'nachname': nachname,
            'institut': institut,
            'publications': []
        }
    
    return publications, researchers_info

# Funktion zur Bereinigung der Publikationen
def clean_publication_ids(data):
    researchers = data["researchers"]
    publications = data["publications"]

    # Schritt 1: Duplikate finden (kleinste ID je Titel wählen)
    title_to_min_id = {}
    for pub in publications:
        title = pub["title"].lower().strip()
        pub_id = int(pub["publication_id"])
        if title not in title_to_min_id:
            title_to_min_id[title] = pub_id
        else:
            title_to_min_id[title] = min(title_to_min_id[title], pub_id)

    # Schritt 2: Mapping der alten IDs zu den kleinsten IDs erstellen
    old_to_new_id = {}
    for pub in publications:
        title = pub["title"].lower().strip()
        old_id = int(pub["publication_id"])
        new_id = title_to_min_id[title]
        old_to_new_id[old_id] = new_id

    # Schritt 3: Aktualisiere "publikations_ids" der Forschenden
    for researcher in researchers:
        updated_ids = set()
        for pub_id in map(int, researcher["publikations_ids"].split(",")):
            updated_ids.add(old_to_new_id.get(pub_id, pub_id))
        researcher["publikations_ids"] = ",".join(map(str, sorted(updated_ids)))

    # Schritt 4: Bereinigte Publikationsliste erstellen
    unique_publications = {}
    for pub in publications:
        new_id = title_to_min_id[pub["title"].lower().strip()]
        if new_id not in unique_publications:
            unique_publications[new_id] = pub

    # Ergebnisse zurücksetzen
    data["publications"] = list(unique_publications.values())
    data["researchers"] = researchers

    return data

# Funktion, um die JSON-Daten zu erstellen
def create_json_from_csv_and_publications(csv_file, publikationen_xml):
    coauthors, researchers_info = read_csv(csv_file)
    publications, researchers_info_xml = parse_publications(publikationen_xml)

    # Mischen der beiden Informationsquellen: CSV und XML
    for researcher_id, data in researchers_info_xml.items():
        if researcher_id in researchers_info:
            researchers_info[researcher_id].update(data)

    researchers = {}
    connections = set()

    for row in coauthors:
        author1_id = row['author1_id']
        author2_id = row['author2_id']
        publication_id = row['publication_id']
        
        if author1_id not in researchers:
            researchers[author1_id] = researchers_info[author1_id]

        if publication_id not in researchers[author1_id]['publications']:
            researchers[author1_id]['publications'].append(publication_id)

        if author1_id != author2_id:
            connection = tuple(sorted([author1_id, author2_id]))
            connections.add(connection)

    result = {
        "researchers": [],
        "publications": [],
        "connections": []
    }

    for researcher_id, data in researchers.items():
        # Titel und Name kombinieren
        full_name = f"{data['vorname']} {data['nachname']}"
        data["full_name"] = full_name  # Setze den vollständigen Namen

        data["publikations_ids"] = ",".join(data["publications"])
        del data["publications"]
        result["researchers"].append(data)

    for pub_id, pub_data in publications.items():
        result["publications"].append({
            "publication_id": pub_id,
            "title": pub_data['title'],
            "year": pub_data['year']
        })

    for source, target in connections:
        result["connections"].append({
            "source": source,
            "target": target,
            "value": 1
        })

    # Bereinige die Publikationen
    result = clean_publication_ids(result)
    return result

# Funktion, um das JSON zu speichern
def save_json_to_file(data, filename='output.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"JSON-Daten erfolgreich gespeichert in {filename}")

# Hauptfunktion
def main():
    csv_file = 'coauthor_connections_with_infos.csv'
    publikationen_xml = 'fpubdb_publikationen_corrected.xml'

    data = create_json_from_csv_and_publications(csv_file, publikationen_xml)
    save_json_to_file(data, 'output_publications&researchers.json')

if __name__ == '__main__':
    main()
