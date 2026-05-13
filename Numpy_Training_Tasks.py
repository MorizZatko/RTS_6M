import numpy as np

def sanitizer():
    print("Sanitizer:")
    try:
        arr_file = np.loadtxt('coords_test.txt')
        arr_points = arr_file.reshape(-1, 3)
        arr_el = arr_points[:, 0]
        mask = arr_el < 0
        neg_points = arr_points[mask]
        print("Assets mit X-Wert unter 0: ", neg_points, "\n")
    except FileNotFoundError:
        print("Datei nicht gefunden!")
    except ValueError:
        print("Fehlerhafte Daten in Datei!")

def budget_check():
    print("Budget Check MB:")
    try:
        arr_file = np.loadtxt('MBsize_test.txt')
        mask = arr_file <= 50
        s_size = arr_file[mask]
        sum_s = np.sum(s_size)
        mean_s = np.mean(s_size)
        max_s =np.max(s_size)
        print("Alle Assets kleiner als 50MB: ", s_size)
        print("Insgesamte Datenmenge aller Assets unter 50MB: ", sum_s)
        print("Durschnittliche Datenmenge aller Assets unter 50MB: ", mean_s)
        print("Größte Datei unter 50MB: ", max_s)
    except FileNotFoundError:
        print("Datei nicht gefunden!")
    except ValueError:
        print("Datei enthält ungültige Daten!")

sanitizer()
budget_check()
    