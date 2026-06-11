"""Dataset Aggregator.

This module scans a directory of Poly Heaven assets, reads individual local 
'metadata.json' files and adds them into a single master catalog.
Finnaly, it generates and prints statistics with all unique categories and tags.
"""

import os
import json

# Setup master catalog to store all metadata
master_catalog = {}

# Root directory to all Poly Heaven downloads
base_dir = r"C:/Users/moriz/Desktop/RTS/python_start/Media_Doc/Downloads/PolyHeaven"

# Iterate through the base directory to get metadata from each asset folder
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)

    if os.path.isdir(folder_path):
        meta_file = os.path.join(folder_path, "metadata.json")

        if os.path.exists(meta_file):
            print(f"Gefunden: {meta_file}")
            with open(meta_file, "r", encoding="utf-8") as f:
                master_catalog[folder] = json.load(f)

# Export the final master catalog to a single JSON file
dataset_path = os.path.join(base_dir, "dataset_catalog.json")
with open(dataset_path, "w", encoding="utf-8") as f:
    json.dump(master_catalog, f, indent=4)

# Calculate dataset statistics
total_assets = len(master_catalog)
unique_cats = {cat for asset in master_catalog.values() for cat in asset.get("categories", [])}
unique_tags = {tag for asset in master_catalog.values() for tag in asset.get("tags", [])}

# Display the final statistics
print(f"\n=== ML Data Statistik ===")
print(f"Gesamt-Assets im Datensatz: {total_assets}")
print(f"Einzigartige Kategorien ({len(unique_cats)}):\n {'\n '.join(unique_cats)}")
print(f"Einzigartige Tags ({len(unique_tags)}):\n {'\n '.join(unique_tags)}")