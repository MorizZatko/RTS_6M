"""Version Changer.

This Module changes the version number of linux path by 1.
All paths are hardcoded in a list.
If no directory on the second last element of the path starts with v and continues with integers, it displays a fallback message.
All outputs via standard terminal.
"""
path = [
    "/mnt/server/Projekte/Shot01/Render/v001/image.0001.exr",
    "/mnt/server/Projekte/Notizen.txt",
    "/mnt/server/Projekte/Shot02/Render/v008/image.0001.exr",
    "/mnt/server/Projekte/Shot02/Render/voice01/image.0001.exr"
]   

for single_path in path:
    # Cleanup path at slashes and split the components       
    split = single_path.strip("/").split("/")   
    print(f"DEBUG: Prüfe Pfad: {single_path}")  

    # LOGIC CHECK
    # 1. Path must have 2 elements or more
    # 2. Second last element must start with 'v'
    # 3. Second last element must continues with digits
    if len(split) >= 2 and split[-2].startswith("v") and split[-2][1:].isdigit():   
        print("--> Check bestanden! Versions-Nummer wird erhöht...")

        # 1. Full path until version element
        path_start = ("/").join(split[:-2])

        # 2. Extracts version element
        path_version = split[-2] 

        # 3. Extracts only the digits of the version element und uppers the number by 1
        path_version_new = int(path_version[1:]) + 1 

        # 4. Formats new version element with three digits
        path_new_number = f"v{path_version_new:03d}" 

        # 5. Last element (file-type)
        path_end = split[-1]

        # Output of the new version path
        print(f"/{path_start}/{path_new_number}/{path_end}")   
    else:  
        # Fallback message if path doesnt match
        print("--> Überprüfung fehlgeschlagen! Keine Versions-Nummer an Index -2 erkannt.")
        print(f"Pfad Übersprungen: {single_path} (ungültiger Ordner)")