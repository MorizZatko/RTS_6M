"""Asset Pipeline Auditor.

This module validates a provided asset list as txt file to check status and weight.
Outputs a new DataFrame and two string lines with the results for status and weight.
"""

import pandas as pd
import numpy as np

def load_raw_assets(file_path):
    """Loading function for txt file with length check.

    Read txt file, check length of asset and converts version, size and extra data to float.
    Exception handling by ValueError.
    
    Args:
        file_path (str): Path to asset text file.

    Returns:
        data (list): fill data with checked assets.
    """
    data = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            #print(f"DEBUG: Verarbeitete Zeile: '{line}'")
            if not line: continue

            elements = line.split(',')

            if len(elements) == 5:
                try:
                    data.append({
                        'Name': elements[0],
                        'Type': elements[1],
                        'Version': float(elements[2]),
                        'Size': float(elements[3]),
                        'Extra': float(elements[4])
                    })

                except ValueError:
                    print(f"Fehler beim umwandeln der Version oder Size in der Zeile: {line}")

            else:
                print(f"Ungültige Anzahl der Elemente in Zeile: {line}")
    return data

class Asset:
    """Basic class for all assets.

    Args:
        name (str): name of asset.
        asset_type (str): type of asset.
        version (float): version number.
        size (float): size of asset in MB.
    """
    def __init__(self, name, asset_type, version, size):
        self.name = name
        self.asset_type = asset_type
        self.version = version
        self.size = size
        self.status = "ok"

    def describe_asset(self):
        """Provides a short description of the asset."""
        print(f"{self.name} ({self.asset_type}) V{self.version} {self.size} | {self.status}")

class MeshAsset(Asset):
    """Specialized class for 3D-Object data.

    Args:
        name (str): name of asset.
        asset_type (str): type of asset.
        version (float): version number.
        size (float): size of asset in MB.
        polycount (float): polygon count of asset.
    """
    def __init__(self, name, asset_type, version, size, polycount):
        super().__init__ (name, asset_type, version, size)
        self.polycount = polycount

class TextureAsset(Asset):
    """Specialized class for texture data.

    Args:
        name (str): name of asset.
        asset_type (str): type of asset.
        version (float): version number.
        size (float): size of asset in MB.
        resolution (float): pixel resolution of asset.
    """
    def __init__(self, name, asset_type, version, size, resolution):
        super().__init__ (name, asset_type, version, size)
        self.resolution = resolution

class AssetLibrary:
    """Global class to manage all validated assets."""
    def __init__(self):
        self.assets = []

    def add_asset(self, asset_obj):
        """Adds asset objects to asset list."""
        self.assets.append(asset_obj)

    def list_all_assets(self):
        """Starts describe_asset methode for every asset."""
        for a in self.assets:
            print(a.describe_asset())

    def run_health_check(self):
        """Scanns all assets for outliers and adjust the status."""
        for a in self.assets:
            if a.version < 2.0:
                a.status = "Outdated"
            if a.size > 500:
                a.status = "Too heavy"

raw_data = load_raw_assets('raw_assets.txt')
df = pd.DataFrame(raw_data)

my_lib = AssetLibrary()

# Basic loop to filter all validated assets by asset type
for index, row in df.iterrows():
    if row['Type'] == 'Mesh':
        mesh_obj = MeshAsset(row['Name'], "Mesh", row['Version'], row['Size'], row['Extra'])
        my_lib.add_asset(mesh_obj)
    elif row['Type'] == 'Texture':
        texture_obj = TextureAsset(row['Name'], "Texture", row['Version'], row['Size'], row['Extra'])
        my_lib.add_asset(texture_obj)
    else:
        obj = Asset(row['Name'], row['Type'], row['Version'], row['Size'])
        my_lib.add_asset(obj)

my_lib.run_health_check()

print("----------------")
for a in my_lib.assets:
    a.describe_asset()

report_data = []

# Basic loop for output
for a in my_lib.assets:
    asset_info = {
        "Name": a.name,
        "Type": a.asset_type,
        "Size_MB": a.size,
        "Status": a.status
    }
    report_data.append(asset_info)

df_report = pd.DataFrame(report_data)

# Total count of crtitical assets.
critical_assets = df_report[df_report['Status'] != 'ok']
total_critical = len(critical_assets)

# Total count of final assets.
final_assets = df_report[df_report['Status'] == 'ok']
total_final = len(final_assets)

print("-------------------")
print(f"Insgesamt kritische Daten: {total_critical}")
print(f"Insgesamt finale Daten: {total_final}")