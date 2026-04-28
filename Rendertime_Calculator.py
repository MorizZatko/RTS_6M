"""Redering Time/Price Calculator.

This module calculates the needed rendering time and price by values provided via standard user input.
Output needed time in in seconds, minutes and hours aswell as the total price for the rendering.
"""

# User input
project = input("Projektname:")
number_of_frames = int(input("Anzahl der Frames:"))
time_per_frame = float(input("Zeit pro Frame in Sekunden:").replace(",", "."))
price_per_minute = float(input("Renderpreis pro Minute:").replace(",", "."))

# LOGIC BLOCK
# 1. Calculates needed time
time = number_of_frames * time_per_frame

# 2. Calculates time in minutes
time_minute = time / 60

# 3. Calculates time in hours
time_hour = time_minute / 60

# 4. Calculates render price
render_price = price_per_minute * time_minute

# Output all results
print(f"---Die Renderzeit für das Projekt {project}, beträgt vorraussichtlich {time:.2f} Sekunden---")
print(f"In Minuten: {time_minute:.2f}")
print(f"In Stunden: {time_hour:.2f}")
print(f"Die Kosten liegen bei ca. {render_price:.2f}€")

# Request user to end programm
input("\nDrücke Enter, um das Programm zu beenden...")