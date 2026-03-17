import time

name = input("Wie ist dein Künstlername? ")
print(f"Initialisiere System für {name}...")
time. sleep(1)

for i in range(1, 4):
    print(f"Lade Creative-Modul {i}...")
    time.sleep(0.5)

print(f"\nStatus: BEREIT. {name}, willkommen in der Zukunft.")