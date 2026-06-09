"""Automated Asset Downloader.

This module requests asset files (textures) via the Poly Heaven API based on settings loaded from a local 'config.json'.
It allows dynamic user input in the terminal for category and resolution, exports a list of all available categories to a JSON file.
Finally, it stores the downloaded maps with their strucutured metadata.
"""

import requests
import json
import os


def download_map(files_dict, map_name, folder, resolution):
    """Downloads a specific texture map in 1k resolution and PNG format.
    
    Args:
        files_dict: A dictionary containing available files from the API.
        map_name: The name of the texture map (Diffuse, Rough).
        folder: The local diretory path where the file should be saved.
        resolution: The target resolution string (1k, 2k, 4k)
    """
    try:
        # Extract the specific URL
        img_url = files_dict[map_name][resolution]["png"]["url"]
        img_data = requests.get(img_url).content
        file_path = os.path.join(folder, f"{map_name.lower()}_1k.png")
        with open(file_path, "wb") as file:
            file.write(img_data)
        print(f"-> {map_name} erfolgreich gesichert!")
    except KeyError as e:
        print(f"-> Map '{map_name}' in 1k nicht verfügbar.")


def metadata(first_asset, asset_folder):
    """Generates a local JSON metadata file for the downloaded asset.
    
    Args:
        first_asset: A dictionary containing core asset info (tags, categories).
        asset_folder: The local directory path where the JSON should be saved.
    """
    # Structure metadata based on API info and expected local paths
    local_metadata = {
        "name": first_asset["name"],
        "categories": first_asset["categories"],
        "tags": first_asset["tags"],
        "local_files": {
            "diffuse": os.path.join(asset_folder, "diffuse_1k.png"),
            "roughness": os.path.join(asset_folder, "rough_1k.png"),
            "normal": os.path.join(asset_folder, "nor_gl_1k.png")
        }
    }
    # Save the structured data to a local metadata.json file
    with open (os.path.join(asset_folder, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(local_metadata, f, indent=4)
        print("Metadaten erfolgreich geschrieben!")

# Setup directory paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Load configurations from the local config file
with open(os.path.join(script_dir, "config.json"), "r", encoding="utf-8") as file:
    config = json.load(file)

print(f"Config geladen! Kategorie: {config['target_category']}")
print(f"Limit: {config['download_limit']} (Datentypen: {type(config['download_limit'])})")

# Allow dynamic input via terminal
user_cat = input(f"Textur Kategorie [Standard: {config['target_category']}]: ").strip()
if user_cat:
    config['target_category'] =  user_cat

user_res = input(f"Auflösung (1k, 2k, 4k) [Standard: {config['resolution']}]: ").strip()
if user_res:
    config['resolution'] = user_res

# Define target category and download count
target_category = config['target_category']
download_count = 0

# Fetch the global list of available texture assets
assets_url = "https://api.polyhaven.com/assets"
headers = {"User-Agent": "MyCreativePipelineTool/1.0"}
params = {"t": "textures"}

response = requests.get(assets_url, params=params, headers=headers)
assets = response.json()

# Extract all unique categories across all available assets
all_cats = set()
for info in assets.values():
    all_cats.update(info.get('categories', []))

# Export list of all found categories
with open(os.path.join(script_dir, "available_categories.json"), "w") as f:
    json.dump(sorted(list(all_cats)), f, indent=4)

# Process asset matching the filter up to the defined limit
for asset_id, info in assets.items():
    if target_category in info.get("categories", []) and download_count < config['download_limit']:
        print(f"\n[Pipeline] Starte Download für: {asset_id}")

        # Fetch detailed file lists and URLs for the current asset
        files_url = f"https://api.polyhaven.com/files/{asset_id}"
        headers = {"User-Agent": "MyCreativePipelineTool/1.0"}
        files_data = requests.get(files_url, headers=headers).json()

        # Create a dedicated subdirectory for the current asset
        absolute_base_dir = os.path.join(parent_dir, config['base_directory'])
        asset_folder = os.path.join(absolute_base_dir, asset_id)
        os.makedirs(asset_folder, exist_ok=True)

        # Download the required maps
        maps_to_get = config['maps_to_load']
        for map_name in maps_to_get:
            download_map(files_data, map_name, asset_folder, config['resolution'] )
            
        #  Create local metadata file
        metadata(info, asset_folder)
        download_count += 1