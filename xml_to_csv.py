import xml.etree.ElementTree as ET
from typing import List, Tuple
from collections import defaultdict
import csv
import re
from bs4 import BeautifulSoup

# Funktion, um die Projekt-Mitarbeiter und Projekte aus der ersten XML-Datei zu extrahieren
def parse_authors(xml_file: str) -> List[Tuple[str, str, str]]:
    """Parse XML file and return list of (author_id, publication_id) tuples"""
    # Read file and replace problematic entities
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all HTML entities with a space - we only care about IDs
    content = re.sub('&[a-zA-Z]+;', ' ', content)
    
    # Parse the modified content
    root = ET.fromstring(content)
    authors = []
    
    for autor in root.findall('autor'):
        author_id = autor.find('id_autor').text
        # Skip authors with id_autor = 0
        if author_id == '0':
            continue
            
        pub_id = autor.find('id_publikation').text if autor.find('id_publikation') is not None else ''
        authors.append((author_id, pub_id))
    
    return authors

# Funktion, um die Verbindungen und Benutzerdaten für author1_id zu erstellen
def create_coauthor_connections(authors: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
    """Create list of co-author connections using author IDs"""
    # Group authors by publication
    pub_authors = defaultdict(list)
    for author_id, pub_id in authors:
        pub_authors[pub_id].append(author_id)
    
    # Create connections
    connections = []
    for pub_id, author_list in pub_authors.items():
        # Skip publications with only one author after filtering
        if len(author_list) < 2:
            continue
            
        # Create all possible pairs for each publication
        for i in range(len(author_list)):
            for j in range(len(author_list)):
                if i != j:  # Avoid self-connections
                    author1_id = author_list[i]
                    author2_id = author_list[j]
                    connections.append((author1_id, author2_id, pub_id))
    
    # Remove duplicates while maintaining order
    seen = set()
    unique_connections = []
    for conn in connections:
        if conn not in seen:
            seen.add(conn)
            unique_connections.append(conn)
    
    return unique_connections

# Funktion, um die Verbindungen in eine CSV-Datei zu speichern
def save_connections_to_csv(connections: List[Tuple[str, str, str]], output_file: str):
    """Save connections to CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'author1_id', 'author2_id', 'publication_id'])  # Header
        for i, (author1_id, author2_id, pub_id) in enumerate(connections, 1):
            writer.writerow([i, author1_id, author2_id, pub_id])

# Funktion, um die Nutzerdaten aus der fdb_user.xml zu extrahieren
def parse_user_info(xml_file):
    user_info = {}
    with open(xml_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'xml')
    users = soup.find_all('user')

    for user in users:
        user_id = user['id']
        user_data = {
            'user_name': user.find('user_name').text,
            'nachname': user.find('nachname').text,
            'vorname': user.find('vorname').text,
            'funktion': user.find('funktion').text,
            'institut': user.find('institut').text,
        }
        user_info[user_id] = user_data

    return user_info

# Funktion, um die Verbindungen und Benutzerdaten für author1_id in eine neue CSV zu schreiben
def write_connections_with_user_info(input_csv, output_csv, user_info):
    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = [
            'index', 'author1_id', 'author1_name', 'author1_nachname', 'author1_vorname', 'author1_funktion', 'author1_institut',
            'author2_id', 'publication_id'  # author2_id bleibt unverändert
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for row in reader:
            author1_id = row['author1_id']
            author2_id = row['author2_id']
            pub_id = row['publication_id']

            # Hole die Benutzerinformationen für author1
            author1_data = user_info.get(author1_id, {})

            # Erstelle die neue Zeile mit den Benutzerdaten für author1 und author2_id unverändert
            writer.writerow({
                'index': row['index'],
                'author1_id': author1_id,
                'author1_name': author1_data.get('user_name', ''),
                'author1_nachname': author1_data.get('nachname', ''),
                'author1_vorname': author1_data.get('vorname', ''),
                'author1_funktion': author1_data.get('funktion', ''),
                'author1_institut': author1_data.get('institut', ''),
                'author2_id': author2_id,  # Keine Änderung für author2_id
                'publication_id': pub_id  # Hinzufügen der publication_id
            })

# Hauptfunktion, die das Skript ausführt
def main():
    input_file = 'fpubdb_autoren_corrected.xml'  # XML-Datei mit Autoren und Publikationen
    output_csv = 'coauthor_connections_with_infos.csv'  # Ausgabedatei mit den erweiterten Informationen für author1_id
    fdb_user_xml = 'fdb_user_corrected.xml'  # XML-Datei mit den Benutzerdaten
    
    try:
        # Parse authors and publications
        authors = parse_authors(input_file)
        
        # Create co-author connections
        connections = create_coauthor_connections(authors)
        
        # Save connections to CSV
        coauthor_connections_csv = 'coauthor_connections.csv'
        save_connections_to_csv(connections, coauthor_connections_csv)
        print(f"Successfully created {coauthor_connections_csv} with {len(connections)} connections")
        
        # Parse user info from fdb_user.xml
        user_info = parse_user_info(fdb_user_xml)
        
        # Write connections with user info to new CSV
        write_connections_with_user_info(coauthor_connections_csv, output_csv, user_info)
        print(f"Successfully created {output_csv} with extended user data for author1_id")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
