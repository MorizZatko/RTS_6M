path = [
    "/mnt/server/Projekte/Shot01/Render/v001/image.0001.exr",
    "/mnt/server/Projekte/Notizen.txt",
    "/mnt/server/Projekte/Shot02/Render/v008/image.0001.exr",
    "/mnt/server/Projekte/Shot02/Render/voice01/image.0001.exr"
]       #  # Nested List mit 4 verschieden Pfaden

for single_path in path:        # erstellt iterationsschleife für die Liste path
    split = single_path.strip("/").split("/")   # schneidet jedes Element der Liste bei / und löscht alle /
    print(f"DEBUG: Prüfe Pfad: {single_path}")  # Gibt aus welches Element der Liste geprüft wird

    if len(split) >= 2 and split[-2].startswith("v") and split[-2][1:].isdigit():   # prüft ob das Element min 2 Indexe lang ist, ob der 2 letzte Index mit 'v' beginnt und ob das zweit letzte Element ab dem zweiten Index aus Zahlen besteht
        print("--> Check bestanden! Versions-Nummer wird erhöht...")  # gibt aus das der Check pro Zeile erfolgreich war
        path_start = ("/").join(split[:-2])     # extrahiert alle Elemente bis zum 2 letzten und verbindet diese mit '/'
        path_version = split[-2]        # extrahiert das 2 letzte Element
        path_version_new = int(path_version[1:]) + 1    # ändert den Inhalt der path_version variable von String zu Integer und addiert 1 (Die Variable selbst bleibt ein String)
        path_new_number = f"v{path_version_new:03d}"    # definiert die Variable path_new_number als String mit einer Variable die, v am Anfang für die v der Versions-Nummer, das :03d füllt alle leeren stell mit 0 auf, sagt das es min 3 stellen gibt und das d steht für digit (ganze Zahlen) 
        path_end = split[-1]        # extrahiert das letzte Element
        print(f"/{path_start}/{path_new_number}/{path_end}")    # gibt den neuen Pfad aus
    else:   # wenn der Check der If Zeile nicht erfolgreich war wird folgendes ausgegeben...
        print("--> Überprüfung fehlgeschlagen! Keine Versions-Nummer an Index -2 erkannt.")
        print(f"Pfad Übersprungen: {single_path} (ungültiger Ordner)")


