import numpy as np

try:
    arr = np.loadtxt('valid_coords_test.txt')
    if arr.shape[1] != 3:
        raise ValueError("Ungültige Spalten Zahl!")
    
    print(np.max(arr, axis=0))

except ValueError as e:
    print(f"Daten ungültig {e}")      