"""Numpy Basics.

This module is a training task of week 6.
Simple numpy basics to get in touch with numpy.
"""

import numpy as np

def basic_arrays():
    print("Basic arrays task:")
    arr_1d = np.array([1, 2, 3, 4, 5])
    print("1-Dimensionales Array:", arr_1d)

    arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
    print("2-Dimensionales Array:\n", str(arr_2d), "\n")

def basic_operators():
    print("Basic operators task:")
    arr = np.array([1, 2, 3, 4, 5])

    sum_elements = np.sum(arr)
    print("Summe:", sum_elements)

    mean_elements = np.mean(arr)
    print("Durschnitt:", mean_elements)

    max_element = np.max(arr)
    min_element = np.min(arr)
    print("Kleinstes Element:", min_element)
    print("Größtes Element:", max_element, "\n")

def basic_slicing():
    print("Basic slicing task:")
    arr = np.array([[1, 2, 3], [4, 5, 6,], [7,  8, 9]])

    element = arr[1, 2]
    print("Element:", element)

    row = arr[1, :]
    print("Reihe:", row)

    column = arr[: ,1]
    print("Folge:", column, "\n")

def basic_reshaping():
    print("Basic reshaping task:")
    r_arr = np.random.random(12)

    r_arr_points = r_arr.reshape(-1, 3)

    print(r_arr_points, "\n")

def basic_masking():
    print("Basic masking task:")
    arr = np.array([12, 55, 120, 8, 200, 45, 10, 60, 150, 30])
    mask = arr > 100
    large_assets = arr[mask]
    print(large_assets, "\n")

def basic_integration():
    print("Basic integration task:")
    try:
        coords_file = np.loadtxt('coords_test.txt')
        print(coords_file, "\n")
    except FileNotFoundError: 
        print("Keine gültige Datei gefunden!")
    except ValueError:
        print("Datei enthält ungültige Daten!")


basic_arrays()
basic_operators()
basic_slicing()
basic_reshaping()
basic_masking()
basic_integration()

print(f"Fertig!")