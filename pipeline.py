projekt = input("Projektname?")
artist = input("Name?")
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
width_high_res = resolution_px[0] * 2
height_high_res = resolution_px[-1] * 2
print(f"Die neue Auflösung entspricht: {width_high_res}x{height_high_res} px")
new_res = width_high_res * height_high_res
megapx_res = new_res / 1000000
print(f"Die Insgesamte Pixelanzahl beträgt: {new_res} px")
print(f"In Megapixeln: {megapx_res}MP")
print(f"Artist {artist} arbeitet am Projekt {projekt} mit folgenden offenen To-do´s: {aufgaben_liste}")