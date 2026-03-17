projekt = "Synth Sound Corp"
resolution_px = (1920, 1080)
rendering_percentage = 75
print(f"Das Projekt {projekt} ist zu {rendering_percentage}% fertig.")
aufgaben = ["Modeling", "Texturing", "Lighting"]
len(aufgaben)
print(f"Offene To-do´s für {projekt}: {len(aufgaben)}")
aufgaben_text = ", ".join(aufgaben)
print(f"To-do für Projekt {projekt}: {aufgaben_text}")
aufgaben.append("Animation")
print(f"Neues To-do für das Projekt {projekt}: {aufgaben[-1]}")
print(f"Insgesamt Anzahl der Todos für {projekt}: {len(aufgaben)}")
aufgaben_liste = ", ".join(aufgaben)
print(f"Bereiche: {aufgaben_liste}")