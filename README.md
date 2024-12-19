# Forschendenzusammenarbeit_PH_Weingarten_Netzwerkgrafik

Das Chord-Diagramm gibt es einmal für die Zusammenarbeit an den Publikationen und einmal für die Zusammenarbeit an den Projekten. (siehe seperate Ordner)

Hier das Vorgehen für die Forschungszusammenarbeit an Publikationen:

01. Relevanten XML-Dateien "gesäubert" (fdb_user.xml, fpubdb_autoren.xml und fpubdb_publikationen) und Sonderzeichen durch Umlaute ersetzt (xmltoxml.py)
02. Die relevanten XML-Dateien in eine csv-Datei umgewandelt (coauthor_connections_with_infos) (xml_to_csv.py)
03. Die CSV-Datei sowie die Datei zu den Publikationen in einen Code eingebunden, welcher die Json-Datei erstellt (xml_to_json.py)
04. Die ausgegebene Json-Datei (output_publications&researchers.json) in den HTML-Code eingebunden (Chord-Diagramm_publications.html)
    >> beim Starten der HTML-Datei wird nun das Chord Diagramm aangezeigt
