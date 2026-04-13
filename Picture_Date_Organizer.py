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
Erstellung von globalen Variablen und Listen.

Die Listen "Image_EXT" und "Video_EXT" werden mit Tuplen (Datei-Endungen) gefüllt.

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
    Erstellt die Globale "plan" Liste, in dem der ausgewählte Ordner gescannt wird 
    und aus allen Dateien eine Liste mit den wichtigen Metadaten sammelt.

    Die Funktion durchläuft alle Dateien, erstellt für jede einen vollständigen Pfad
    und versucht das Aufnahme-Datum der Exif zu ermitteln oder fallback (WindowsDatum) zu bestimmen.

    Args:
        None. Verlässt sich auf die gobalen Variablen "all_files" (Datei-Liste) und "user_path" (aktuell gewählter Ordner)

    Returns:
        Keine direkten Rückgabewerte. Funktion ändert die globalen Variablen "plan" und füllt sie mit Tuplen (Datei-Name, Datum, Datei-Endung)
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
    Die Funktion scannt jede Datei im "Pic-Path" nach einer Exif Datei,
    und extrahiert das Datum. Fallback: Wenn kein Datum in der Exif steht,
    wird der letzte timestamp von Windows genommen.

    Args:
        "pic_path" ist der vollständige Pfad zur Bild-Datei, deren Datum extrahiert werden soll

    Returns:
        None.
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
    Funktion fragt Nutzer nach dem Ordner, prüft ob relevante Dateien enthalten sind und zäht diese, gibt die Information über das GUI aus.
    Fallback: Keine Dateien im Ornder, wird ausgegeben über die GUI.

    Args:
        None. Funktion nutzt globale Variablen "all_files" und "user_path"

    Returns:
        None. Funktion arbeitet eng mit Tkinter zusammen um die Information dem Nutzer zu präsentieren
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
    Funktion erstellt einer Statistik nach den Kategorien (Bilder, Videos, Andere) mit allen gefunden Dateien und zählt diese. 
    Fallback: Keine Dateien gefunden, wird über GUI ausgegeben.

    Args:
        None. Funktion nutzt globale Variablen "all_files" und "plan" so wie die funktion "create_plan".

    Returns:
        Stats: Die Liste stats speichert die Statistik die erstellt wurde. Die Funktion ist eng mit Tkinter verknüpft 
        und gibt alle notwendigen Information im GUI aus

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
    Startet den Hauptsortier- und Bewegungs-/Kopierprozess für Bilddaten.

    Dieser Prozess führt folgende Schritte aus:
    1. Vorab-Prüfung: Stellt sicher, dass ein Quell-Ordner ausgewählt wurde.
    2. Vorschau: Zeigt dem Nutzer eine Übersicht über die zu findenden Dateitypen (Bilder, Videos, Andere).
    3. Zielauswahl: Fordert den Nutzer zur Auswahl des Ziel-Root-Ordners auf.
    4. Durchführung: Durchläuft jede gefundene Datei. Bei gültigen Dateitypen wird das Dateiformat
       nach dem EXIF-Datum in Unterordnern neu erstellt. Die Datei wird dann entweder kopiert oder verschoben
       und der Fortschritt wird laufend im GUI angezeigt.
    5. Abschluss: Erstellt ein finales Protokoll mit allen bearbeiteten Dateinamen.

    Args:
        (Diese Funktion ist eng mit dem GUI-Kontext gekoppelt und nutzt globale
        Variablen wie user_path, plan und sort_mode, um ihren Zustand zu erhalten.)

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