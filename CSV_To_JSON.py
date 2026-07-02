"""CSV to JSON.

This module reads asset information, categorizes them into High Poly and Low Poly,
based on their vertices. Finally it saves all assets to their category-based JSON files.
"""

import csv
import json

# Global variables for categorization and statistics
categories = {'HighPoly': [], 'LowPoly': []}

all_verc = 0
highpol = 0
lowpol = 0

def save_json(data, filename):
    """Saves a dictionary as a formatted JSON file.
    
    Args:
        data: The dictionary containing the data to be saved.
        filename: The target filename (without extension).
    """
    path = (fr'C:\Users\moriz\Desktop\RTS\python_start\{filename}.json')
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# Read raw asset data from the CSV file
try:
    with open(r'C:\Users\moriz\Desktop\RTS\python_start\assets.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
except:
    print("ERRROR: CSV not found!")
    exit()

# Process and filter individual assets
for obj in data:
    status = 'imported'
    count = int(obj['Vertices'])

    # Create a cleaned data object for the asset
    obj_data = {
        'Object Name': obj['Object Name'],
        'Vertices': count,
        'Type': obj['Type'],
        'Status': status
        } 
    
    # Categorize based on a threshold of 500 vertices
    cat_name = 'HighPoly' if count > 500 else 'LowPoly'
    categories[cat_name].append(obj_data)

    # Update statistical counters
    all_verc += count
    if cat_name == 'HighPoly':
        highpol += 1
    else:
        lowpol += 1

# Export categorized data into separate JSON files
for cat_name, asset_list_of_cat in categories.items():
    current_scene_data = {
    'Metadata': {"author": "Moriz", "version": 3.0},
    'Scene Name': 'Korg Electribe 2 Sampler', 'Assets': asset_list_of_cat
    }
    save_json(current_scene_data, cat_name)