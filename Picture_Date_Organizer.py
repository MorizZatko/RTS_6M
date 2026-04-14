import os
import time
import shutil
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS
from colorama import init, Fore, Style
# Import von Datenbanken

"""
Globale Initialisierung: Erstellung von globalen Variablen und Listen.
Die Listen 'Image_EXT' und 'Video_EXT' werden mit Tuplen (Datei-Endungen) gefüllt.
Dient der Speicherung von Dateityp-Endungen.

Args:
    None.

Returns:
    None.
"""
user_path = ""
all_files = []
plan = []
Image_EXT = [".jpg", ".jpeg", ".png", ".arw", ".raw", ".tiff", ".tif", ".psd", ".psb", ".nef" ]
Video_EXT = [".mp4", ".mov"]


def create_plan():
    """
    Erstellt die Globale 'plan' Liste. Diese wird mit den wichtigen Metadaten 
    für alle in 'all_files' gelisteten Dateien gefüllt.

    Die Funktion durchläuft alle Dateien, erstellt für jede einen vollständigen Pfad
    und versucht das Aufnahme-Datum der Exif zu ermitteln, falls dies fehlschlägt,
    wird ein Fallback-Datum verwendet (basierend auf dem letzten Änderungszeitsttempel des Dateisystems).

    Args:
        None. Verlässt sich auf die gobalen Variablen "all_files" (Liste der Dateinamen) und "user_path" (aktuell gewählter Quellordner)

    Returns:
        Keine direkten Rückgabewerte. Funktion ändert die globalen Variablen "plan" und füllt sie mit Tuplen: (Dateiname, Datum, Dateiendung)
    """
    global plan
    plan = []
    for f in all_files:
        ext = os.path.splitext(f)[1].lower()
        full_path = os.path.join(user_path, f)
        date = get_shooting_date(full_path)
        if not date:
            date = "Unbekanntes_Datum"
        plan.append((f, date, ext))
# Funktion um eine Liste zu erstellen mit allen Dateien die ein Datum in der Exif haben

def get_shooting_date(pic_path):
    """
    Die Funktion extrahiert das Aufnahme-Datum aus den Exif-Metadaten der Bilddatei.
    Fallback: Wenn keine gültigen Exif-Daten gefunden werden, wird der letzte timestamp des Dateisystems genommen (mtime)

    Args:
        'pic_path' (str) ist der vollständige Pfad zur Bild-Datei, deren Datum extrahiert werden soll

    Returns:
        str: Das formatierte Datum im String 'YYYY-MM-DD'
    """
    try:
        with Image.open(pic_path) as img:
            exif_date = img._getexif()
            if exif_date:
                for tag_id, value in exif_date.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "DateTimeOriginal":
                        return value[:10].replace(":", "-")
    except Exception:
        pass
     
    ts = os.path.getmtime(pic_path)
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
# Funktion um das Datum der Datei auszulesen, falls keine Exif vorhanden ist, wird das Windows Datum genommen
    

def select_folder():
    """
    Funktion führt ein Dialog aus in dem der Benutzer seinen Quellordner wählt.
    Nach der Auswahl werden alle Dateien des Ordners gescannt 
    und die globalen Variablen 'all_files' und 'user_path' geladen.

    Args:
        None.

    Returns:
        None. Aktualisiert die globalen Variablen 'all_files' und 'user_path' sowie die GUI_Elemente.
    """
    global all_files
    global user_path 
    user_path = filedialog.askdirectory(title="Ordner zum Scannen wählen")
    if not user_path:
        log_area.insert(tk.END, "Abbruch: Kein Quell-Ordner ausgewählt.\n")
        log_area.delete(tk.END)
        log_area.see(tk.END)
        return

    folder_name = os.path.basename(user_path)

    log_area.delete("1.0", tk.END)
    label_status.config(text=f"Ausgewählter Ordner: {user_path}")
    log_area.insert(tk.END, f"Ordner ausgewählt: {folder_name}\n")
    log_area.insert(tk.END, "Scanne Daten, bitte warten...\n")
    window.update()
    
    all_files = [f for f in os.listdir(user_path) if os.path.isfile(os.path.join(user_path, f))]
    total_files = len(all_files)

    if total_files == 0:
        log_area.insert(tk.END, "Ordner ist leer!\n")
        log_area.delete(tk.END)
        return
    
    for index, f in enumerate(all_files):
        scan_progress = ((index + 1) / total_files) * 100
        progress["value"] = scan_progress

        if index % 10 == 0:
            window.update()

    log_area.insert(tk.END, f"Scan abgeschlossen! {total_files} Dateien gefunden...\n")
    log_area.insert(tk.END, "Bereit zum Sortieren, klicke auf 'Start'.\n")
    log_area.insert(tk.END, "-" * 40)
    log_area.see(tk.END)
# Funktion zum Scannen des angegeben Ordners, prüft ob der Ornder existiert und wie viele Dateien enthalten sind

def show_stats():
    """
    Funktion generiert eine detaillierte Statistik der im Quellordner gefunden Dateien und zählt diese.
    Die Funktion führt zuerst 'create_plan()' aus, um die notwendigen Daten zu sammeln.
    Die Statistik wird nach den Kategorien 'Bilder', 'Videos' und 'andere Dateien' zusammengefasst und wird im GUI ausgegeben. 
    Fallback: Wenn keine Dateien gefunden im Quellordner gefunden werden, wird dies auch über das GUI ausgegeben.

    Args:
        None. Funktion nutzt globale Variablen 'all_files' und 'user_path'.

    Returns:
        None. Aktualisiert globale Liste 'plan' und gibt Ergebnisse über die GUI aus.
    """
    global all_files
    global plan

    total_files = len(all_files)
    folder_name = os.path.basename(user_path)

    log_area.delete("1.0", tk.END)

    log_area.insert(tk.END, f"Ordner ausgewählt: {folder_name}\n")
    log_area.insert(tk.END, "Scanne Daten, bitte warten...\n")
    log_area.insert(tk.END, f"Scan abgeschlossen! {total_files} Dateien gefunden...\n")
    log_area.insert(tk.END, "Bereit zum Sortieren, klicke auf 'Start'.\n")
    log_area.insert(tk.END, "-" * 40 + "\n")

    create_plan()

    if not plan:
            messagebox.showinfo("Info:", "Es wurden keine Bild-Daten gefunden...\n")
            return

    stats = {
         "Bilder": 0,
        "Videos": 0,
        "Andere Dateien": 0
    }
    
    for f, date, ext in plan:
        if ext in Image_EXT:
            stats["Bilder"] += 1
        elif ext in Video_EXT:
            stats["Videos"] += 1
        else:
            stats["Andere Dateien"] += 1
            

    
        log_area.insert(tk.END, f"Gefundene Dateien: {f}\n")
        log_area.see(tk.END)
        window.update()

    log_area.insert(tk.END, "-" * 40 + "\n")
    log_area.see(tk.END)
# Funktion zeigt an wie viele Dateien im Ornder "Bilder", "Videos" oder "andere Dateien" sind

def start_sorting():
    """
    Startet den Hauptsortier- und Bewegungs-/Kopierprozess für Bild- & Video-daten.

    Dieser Prozess führt folgende Schritte aus:
    1. Initialprüfung: Stellt sicher, dass ein Quell-Ordner definiert wurde.
    2. Planung: Ruft 'create_plan()' auf um alle Metadaten zu sammeln.
    3. Vorschau: Zeigt dem Benutzer die Statistik aller Dateitypen
    4. Zielauswahl: Fordert den Nutzer zur Auswahl des Ziel-Root-Ordners auf.
    5. Durchführung: Iteriert durch jede gefundene Datei. Für alle gültigen Dateitypen wird ein Unterordner
       nach dem EXIF-Datum im Zielordner angelegt. Die Datei wird dann entweder kopiert oder verschoben ('move'/'copy')
       und der Fortschritt wird laufend aktualisiert im GUI angezeigt.
    5. Abschluss: Erstellt ein finales Protokoll ('Alle_kopierten_Dateien.txt') mit allen verarbeiteten Dateinamen.

    Args:
        None. Nutz globale Variablen wie 'user_path', 'plan', 'all_files', 'sort_mode'.

    Returns:
        None. Die Ergebnisse werden über die GUI (log_area) und Pop-up-Messageboxen ausgegeben.
    """
    global user_path
    global full_path
    global plan
    global all_files
    
    all_scc_files = []

    if not user_path:
        messagebox.showwarning("Fehler", "Bitte zuerst einen Quell-Ordner auswählen!")
        return
    create_plan()
    if not plan:
        messagebox.showinfo("Info", "Es wurden keine Bild-Daten gefunden...")
        return
    
    stats = {
         "Bilder": 0,
        "Videos": 0,
        "Andere Dateien": 0
    }

    for file_name, date, ext in plan:
    
        if ext in Image_EXT:
            stats["Bilder"] += 1
            should_copy = True
        elif ext in Video_EXT:
            stats["Videos"] += 1
            should_copy = True
        else:
            stats["Andere Dateien"] += 1
            should_copy = False
    
    if messagebox.askyesno("Vorschau:", f"\nEs wurden: {len(plan)} Dateien gefunden.\n"
                           f"Davon:\n"
                           f"Bilder: {stats['Bilder']}\n"
                            f"Videos: {stats['Videos']}\n"
                            f"Andere Dateien: {stats['Andere Dateien']}\n"
                            f"Ziel-Ordner auswählen?"):
        target_base = filedialog.askdirectory(parent=window, title="Bitte Ziel-Ordner wählen")
        if not target_base:
            log_area.insert(tk.END, "Abbgebrochen: Kein Ziel-Ordner ausgewählt.\n")
            log_area.see(tk.END)
            return
    else:
        log_area.insert(tk.END, "\nVorgang vom Nutzer gestoppt.\n")
        log_area.see(tk.END)
        return

    start_time = time.time()
    total_images = len(plan)
    processed_count = 0
    total_files_in_plan = len(plan)

    for file_name, date, ext in plan:
        processed_count += 1
    
        if ext in Image_EXT:
            stats["Bilder"] += 1
            should_copy = True
        elif ext in Video_EXT:
            stats["Videos"] += 1
            should_copy = True
        else:
            stats["Andere Dateien"] += 1
            should_copy = False
            
        if should_copy:
            all_scc_files.append(file_name)
            try:
                target_folder = os.path.join(target_base, date)
                os.makedirs(target_folder, exist_ok=True)
                source_path = os.path.join(user_path, file_name)
                target_path = os.path.join(target_folder, file_name)

                if sort_mode.get() == "move":
                    shutil.move(source_path, target_path)
                    log_area.insert(tk.END, f"Verschoben: {file_name}\n")
                else:
                    shutil.copy(source_path, target_path)
                    log_area.insert(tk.END, f"Kopiert: {file_name}\n")
                
                
                elapsed_time = time.time() - start_time
                files_remaining = total_images - processed_count
                time_per_file = elapsed_time / processed_count
                remaining_seconds = int(time_per_file * files_remaining)
                mins, secs = divmod(remaining_seconds, 60)
                time_str = f"{mins:02d}:{secs:02d}"

                progress["value"] = (processed_count / total_files_in_plan) * 100
                label_status.config(text=f"Noch ca. {time_str} Min. ({processed_count}/{total_images})")

                log_area.see(tk.END)
                window.update()
            except Exception as e:
                log_area.insert(tk.END, f"FEHLER: {file_name} | {e}\n")

    

    try:
        message_path = os.path.join(target_base, "Alle_kopierten_Dateien.txt")
        with open(message_path, "w") as datei:
            datei.write("Zusammenfassung der Sortierung:\n")
            datei.write("-" * 30 + "\n")
            for dateiname in all_scc_files:
                datei.write(dateiname + "\n")

        log_area.insert(tk.END, f"Protokoll erstellt unter:\n{message_path}\n")
    except Exception as e:
        log_area.insert(tk.END, f"Fehler beim erstellen des Protokolls: {e}\n")
            

    messagebox.showinfo("Fertig!",
                        f"Sortierung abgeschlossen!\n\n"
                        f"Bilder: {stats['Bilder']}\n"
                        f"Videos: {stats['Videos']}\n"
                        f"Andere Dateien: {stats['Andere Dateien']}\n"
                        f"{processed_count} Dateien wurden kopiert/verschoben!")
# Funktion die nach dem Ziel-Ordner frägt und dann alle Bild und Video Daten kopiert oder verschiebt, ein log-file erstellt und ausgibt wie viele Daten bewegt wurden    
    


bg_color = "#2e2e2e"
fg_color = "#ffffff"
accent_color = "#ff8c00"
text_bg = "#1e1e1e"
# Farb definiton

window = tk.Tk()
window.title("Foto_Datum_Sortierer_V2")
window.geometry("800x650")
window.configure(bg=bg_color)

label_status = tk.Label(window, text="Zu sortierenden Ordner auswählen:", 
                        bg=bg_color, fg=accent_color, font=("Arial", 10, "bold"), pady=10)
label_status.pack()

log_area = tk.Text(window, height=27, width=80,
                   bg=text_bg, fg=fg_color,
                   insertbackground=fg_color,
                   highlightthickness=2, highlightbackground=accent_color)
log_area.pack(padx=10, pady=10)

btn_frame_top = tk.Frame(window, bg=bg_color)
btn_frame_top.pack(pady=10)

btn_frame_bottom = tk.Frame(window, bg=bg_color)
btn_frame_bottom.pack(pady=5)

sort_mode = tk.StringVar(value="copy")

radio_copy = tk.Radiobutton(btn_frame_bottom, text="Kopieren", variable=sort_mode, value="copy",
                            bg=bg_color, fg=fg_color, selectcolor=text_bg, activebackground=accent_color)
radio_copy.pack(side=tk.LEFT, padx=5)

radio_move = tk.Radiobutton(btn_frame_bottom, text="Verschieben", variable=sort_mode, value="move",
                            bg=bg_color, fg=fg_color, selectcolor=text_bg, activebackground=accent_color)
radio_move.pack(side=tk.LEFT, padx=5)

button_style = {"bg": accent_color, "fg": "black", "font": ("Arial", 9, "bold"), "activebackground": "#e67e00"}

btn_select = tk.Button(btn_frame_bottom, text="Ordner wählen", command=select_folder, **button_style)
btn_select.pack(side=tk.LEFT, padx=5)

btn_check = tk.Checkbutton(btn_frame_bottom, text="Scann anzeigen", command=show_stats, 
                           bg=bg_color, fg=fg_color, selectcolor=text_bg, activebackground=accent_color)
btn_check.pack(side=tk.LEFT, padx=5)

btn_start = tk.Button(btn_frame_bottom, text="Start", command=start_sorting, **button_style)
btn_start.pack(side=tk.LEFT, padx=5)

btn_quit = tk.Button(btn_frame_bottom, text="Beenden", command=window.destroy, 
                     bg="#555555", fg=fg_color, font=("Arial", 9, "bold"))
btn_quit.pack(side=tk.RIGHT, padx=5)

progress = ttk.Progressbar(window, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)
# Gestaltung der Benutzer Oberfläche mit Tkinter

window.mainloop()