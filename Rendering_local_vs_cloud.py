"""Rendering time and price comparison.

This module calculates and compares local and cloud rendering time and costs by values
provided via standard user input.
Outputs a chart via standard output, displaying the costs/time aswell as the differences (euro and hours).
Outputs two strings with the fastest and the cheapest option.
"""

# User input
local_price = float(input("Lokale Stromkosten pro Stunde:").replace(",", "."))
local_time = float(input("Lokale Render Zeit in Stunden:").replace(",", "."))
cloud_price = float(input("Cloud Stromkosten pro Stunde:").replace(",", "."))
cloud_time = float(input("Cloud Render Zeit in Stunden:").replace(",", "."))

# Calculates time/price and difference
local_cost = local_price * local_time
cloud_cost = cloud_price * cloud_time
dif_cost = abs(cloud_cost - local_cost)
dif_time  = abs(local_time - cloud_time) 

# Logic to detect fastest and cheapest option
if local_cost < cloud_cost:
    tip = "Lokal"
else:
    tip = "Cloud"

if local_time < cloud_time:
    tip_time = "Lokal"
else: 
    tip_time = "Cloud"

# Outputs string chart
print("+" + "-"*53 + "+")
print(f"| {"Anbieter":<15} | {"Kosten in €":>15} | {"Zeit in h":>15} |")
print("+" + "-"*53 + "+")
print(f"| {"Lokal":<15} | {local_cost:>15.2f} | {local_time:>15.2f} |")
print("+" + "-"*53 + "+")
print(f"| {"Cloud":<15} | {cloud_cost:>15.2f} | {cloud_time:>15.2f} |")
print("+" + "-"*53 + "+")
print(f"| {"Differenz":<15} | {dif_cost:>15.2f} | {dif_time:>15.2f} |")
print("+" + "-"*53 + "+")

# Outputs string for smart decision
print(f"\nDie Kostengünstigere Variante ist {tip}, um {dif_cost:.2f}€ günstiger.")
print(f"Die Schnellere Variante ist {tip_time}, um {dif_time:.2f}h schneller.")