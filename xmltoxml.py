from bs4 import BeautifulSoup

# Funktion zum Entfernen von HTML-Entitäten und Ersetzen durch korrekte Umlaute
def clean_xml(xml_file: str, output_file: str):
    """Liest eine XML-Datei, entfernt HTML-Entitäten und speichert die bereinigte Datei."""
    with open(xml_file, 'r', encoding='utf-8') as file:
        # Lese den Inhalt der XML-Datei
        content = file.read()
        
        # Verwende BeautifulSoup mit 'html.parser', um HTML-Entitäten zu entschlüsseln
        soup = BeautifulSoup(content, 'html.parser')

        # Konvertiere den entschlüsselten Inhalt zurück in einen XML-String
        # Wir müssen auf `soup` als "string" zurückgreifen, um die originale XML-Struktur zu erhalten
        cleaned_content = str(soup)

    # Schreibe die bereinigte XML in eine neue Datei
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write(cleaned_content)

# Liste der XML-Dateien und Ziel-Dateinamen für bereinigte Versionen
xml_files = [
    ('fdb_user.xml', 'fdb_user_corrected.xml'),
    ('fpubdb_autoren.xml', 'fpubdb_autoren_corrected.xml'),
    ('fpubdb_publikationen.xml', 'fpubdb_publikationen_corrected.xml')
]

# Bereinige alle Dateien und speichere die bereinigte Version
for input_file, output_file in xml_files:
    clean_xml(input_file, output_file)
    print(f"Bereinigte Datei gespeichert: {output_file}")
