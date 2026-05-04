"""Point-Cloud cleaner.

This module takes a text-file as input, proofs if no text is included and no numbers outside the range 100 to -100.
Outputs a clean numpy-array text-file ready for ML-Pipelines. 
"""

import numpy as np

values = []
clean_values = []

# Import
with open('raw_points_bad.txt') as file:
    lines = file.readlines()
    for line in lines:
        try:
            value = float(line.strip())
            values.append(value)
        except ValueError as e:
             print(f"Daten Fehlerhaft, enthalten Text! (str) {e}")
             exit()

# Number range proof
for value in values:
    try:
        if value > 100 or value < -100:
            raise ValueError
        else:
            clean_values.append(value)
    except ValueError as e:
            print(f"Fehler! {e}")
            continue

# Convert to numpy-array
try:
    arr = np.array(clean_values)
    arr_3d = arr.reshape(-1, 3)
except ValueError as e:
     print(f"Falsche Anzahl für 3D Matrix: {e}")

# Create clean array
mask = (arr_3d >= -100) & (arr_3d <= 100)
row_mask = mask.all(axis=1)
final_clean_arr = arr_3d[row_mask]
print(final_clean_arr)

# Finds max and min array
max_point = np.max(final_clean_arr, axis=0)
print(f"Größter Wert: ", max_point)

min_point = np.min(final_clean_arr, axis=0)
print(f"Kleinster Wert: ", min_point)

# Creates final text-file
np.savetxt('cleaned_points.txt', final_clean_arr)