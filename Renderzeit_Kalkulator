"""
Module: Redering Time/Price Calculator
Description: Tool that calculates the needed rendering time and price trough given values via user input.
Function:
    1. Asks user for the project name (project), total number of frames (number_of_frames), time per frame in seconds (time_per_frame)
       and the rendering price per minute (price_per_minute)
    2. Calculates the rendering time in minutes and hours aswell as the price for the rendering in euro.
    3. Outputs strings with all results for the project.
    4. Request the user to press enter to close this module.

Args:
    None: All needed values are provided by the user via standard input.
Retuns:
    None: Outputs four strings with all final results via standard output.
"""

project = input("Projektname:")
number_of_frames = int(input("Anzahl der Frames:"))
time_per_frame = float(input("Zeit pro Frame in Sekunden:").replace(",", "."))
price_per_minute = float(input("Renderpreis pro Minute:").replace(",", "."))

# --- Calculate logic ---
time = number_of_frames * time_per_frame
time_minute = time / 60
time_hour = time_minute / 60
render_price = price_per_minute * time_minute

# --- Output ---
print(f"---Die Renderzeit für das Projekt {project}, beträgt vorraussichtlich {time:.2f} Sekunden---")
print(f"In Minuten: {time_minute:.2f}")
print(f"In Stunden: {time_hour:.2f}")
print(f"Die Kosten liegen bei ca. {render_price:.2f}€")

input("\nDrücke Enter, um das Programm zu beenden...")