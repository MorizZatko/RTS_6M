"""Automated Asset Downloader.

This module requests asset files (textures) via the poly heaven API.
It filters all found assets by a hardcoded target category, as well as by 1k resolution and PNG images.
After downloading it generates a folder, named after the asset to store the downloaded files.
Finally, it generates a JSON file containing the specific metadata for every asset.  
"""

import requests
import json
import os


def download_map(files_dict, map_name, folder):
    """Downloads a specific texture map in 1k resolution and PNG format.
    
    Args:
        files_dict: A dictionary containing available files from the API.
        map_name: The name of the texture map (Diffuse, Rough).
        folder: The local diretory path where the file should be saved.
    """
    try:
        # Extract the specific URL
        img_url = files_dict[map_name]["1k"]["png"]["url"]
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


# Create base download directory
os.makedirs("Media_Doc/Downloads", exist_ok=True)

# Define target category and download count
target_category = "asphalt"
download_count = 0

# Fetch the global list of available texture assets
assets_url = "https://api.polyhaven.com/assets"
headers = {"User-Agent": "MyCreativePipelineTool/1.0"}
params = {"t": "textures"}

response = requests.get(assets_url, params=params, headers=headers)
assets = response.json()

# Process asset matching the filter up to the defined limit
for asset_id, info in assets.items():
    if target_category in info.get("categories", []) and download_count < 3:
        print(f"\n[Pipeline] Starte Download für: {asset_id}")

        # Fetch detailed file lists and URLs for the current asset
        files_url = f"https://api.polyhaven.com/files/{asset_id}"
        headers = {"User-Agent": "MyCreativePipelineTool/1.0"}
        files_data = requests.get(files_url, headers=headers).json()

        # Create a dedicated subdirectory for the current asset
        asset_folder = f"Media_Doc/Downloads/PolyHeaven/{asset_id}"
        os.makedirs(asset_folder, exist_ok=True)

        # Download the required maps
        maps_to_get = ["Diffuse", "Rough", "nor_gl"]
        for map_name in maps_to_get:
            download_map(files_data, map_name, asset_folder )
            
        #  Create local metadata file
        metadata(info, asset_folder)
        download_count += 1