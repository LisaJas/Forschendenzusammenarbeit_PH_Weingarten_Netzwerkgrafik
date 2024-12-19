UMSETZUNG   

Zu Beginn wurden die XML-Quelldateien der Forschungsdatenbank der PH Weingarten heruntergeladen. Anschließend wurden die daraus relevanten XML-Dateien herausgefiltert, die für die Erstellung der Netzwerkgrafik benötigt wurden. Diese wurden zur einfacheren Verarbeitung in einem ersten Schritt mittels eines mit Hilfe von KI generierten Python-Skripts angepasst, um alle Zeichenentitäten durch tatsächliche Umlaute zu ersetzen (..corrected.xml). Nun wurde mit Hilfe von KI ein weiteres Python-Skript generiert, welches zur Analyse der Zusammenarbeit von Forschenden an Publikationen dient. Mit diesem Skript wurden wesentliche Inhalte zu den Forschenden und ihrer Forschungszusammenarbeit in eine CSV-Datei übertragen (xml_to_csv). Ein weiteres Python-Skript, erneut mit Hilfe von KI erstellt, konnte im nächsten Schritt die CSV-Datei einbinden und diese mit zugehörigen Informationen zu den Publikationen verknüpfen. Ausgabeformat war eine JSON-Datei, welche die Beziehungen zwischen den Entitäten des Netzwerkes repräsentiert (xml_to_json). Die JSON-Datei wurde in einer HTML-Datei eingebunden (Chord-Diagramm_publications.html). Diese enthält einen JavaScript-Code, der für die Erstellung des Chord-Diagramms notwendig ist. Beim Öffnen in einem Browser generiert die HTML-Datei letztlich das Chord-Diagramm. (Hierfür zum Beispiel die html Datei mittels Visual Studio Code)

Dieser Prozess wurde, jedoch ohne Erstellung einer zusätzlichen CSV-Datei, ein weiteres Mal für die Visualisierung der Projekt-Zusammenarbeit von Forschenden durchgeführt. 