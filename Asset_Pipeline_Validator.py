"""Asset Pipeline Validator.

This module scans and validates a DataFrame to output a panda chart with all files equal or over 500MB size and version equal or under 2.0.
"""
import pandas as pd
import numpy as np

# Data to validate
data = {
    'Name': ['Hero_Mesh', 'Skin_Tex', 'Env_Rock', 'Grass_Tex', 'Water_Mesh'],
    'Type': ['Mesh', 'Texture', 'Mesh', 'Texture', 'Mesh'],
    'Size_MB': [600, 40, 120, 30, 800],
    'Version': [1.5, 2.1, 1.1, 2.0, 1.0],
    'Shader': ['PBR_Skin', 'Standard', 'PBR_Rock', 'Standard', 'Water_Shader'],
    'Extra': [5000, 2048, 1200, 1024, 8000]
}
df = pd.DataFrame(data) 

class Material:
    """Represents a surface material for a 3D-Object.
    
    Args:
        shader_name (str): Name of shader.
        base_color (str): Name of surface color.
    """
    def __init__(self, shader_name, base_color):
        self.shader_name = shader_name
        self.base_color = base_color

class Asset:
    """Basic class for all assets.
    
    Args:
        name (str): Name of asset
        asset_type (str): Type of asset ('Mesh'/'Texture')
        version (float): Version number of asset.
        size (int): Size of asset in MB.
    """
    def __init__(self, name, asset_type, version, size):
        self.name = name
        self.asset_type = asset_type
        self.version = version
        self.size = size
        self.status = 'OK'

    def describe(self):
        """Provides a short description of the asset.
        
        Returns:
            str: Formatted string with name, version and size.
        """
        return f"Asset {self.name} V{self.version:.1f} - {self.size}MB"
    
    def update_version(self):
        """Increases version number by 0.1."""
        self.version += 0.1

class MeshAsset(Asset):
    """Specialized class for 3D-Object-Data in assets.
    
    Args:
        name (str): Name of asset
        asset_type (str): Type of asset ('Mesh'/'Texture')
        version (float): Version number of asset.
        size (int): Size of asset in MB.
        polycount (int): Polygon count of asset.
    """
    def __init__(self, name, asset_type, version, size, polycount):
        super().__init__(name, asset_type, version, size)
        self.polycount = polycount

    def describe(self):
        """Provides a short description of the 3D-Asset.
        
        Returns:
            str: Formatted string with name, version and size.
        """
        return f"Asset {self.name} V{self.version:.1f} Poly:{self.polycount} - {self.size}MB"
    
class TextureAsset(Asset):
    """Specialized class for Texture-Data in assets.
    
    Args:
        name (str): Name of asset
        asset_type (str): Type of asset ('Mesh'/'Texture')
        version (float): Version number of asset.
        size (int): Size of asset in MB.
        resolution (int): Resolution of asset.
    """
    def __init__(self, name, asset_type, version, size, resolution):
        super().__init__(name, asset_type, version, size)
        self.resolution = resolution
    
    def describe(self):
        """Provides a short description for the Texture_Data.
        
        Returns:
            str: Formatted string with name, version and size.
        """
        return f"TextureAsset {self.name} ({self.asset_type}) V{self.version:.1f} Res:{self.resolution} - {self.size}MB"

class AssetLibrary:
    """Global class to manage and validates all assets."""
    def __init__(self):
        self.assets = []

    def add_asset(self, asset_obj):
        """Adds Asset-Object to library.

        Args:
            asset_obj: Asset-Object with all specific object data.
        """
        self.assets.append(asset_obj)

    def get_total_size(self):
        """Calculates total weight of all assets in MB.
        
        Returns:
            int: Total size of all stored assets.
        """
        total = 0
        for a in self.assets:
            total += a.size
        return total
    
    def list_all_assets(self):
        """Provides a description of all assets per terminal."""
        for a in self.assets:
            print(a.describe())

    def find_heavy_assets(self, threshold):
        """Scans all assets to filter too heavy ones.
        
        Args:
            threshold (int): Size limit in MB.

        Returns:
            heavy_assets (list): List of all assets heavier than the threshold.
        """
        heavy_assets = []
        for a in self.assets:
            if a.size > threshold:
                heavy_assets.append(a)
        return heavy_assets
    
    def run_health_check(self):
        """Scans all assets to filter outliners."""
        for a in self.assets:
            if a.version <= 2.0:
                a.status = 'Outdated'
                
            if a.size >= 500:
                a.status= 'Too Heavy'
            
# Initialize process   
my_lib = AssetLibrary()

# Convert DataFrame-Rows to Asset_Objects
for index, row in df.iterrows():
    if row['Type'] == 'Mesh':
        Mesh_pd = MeshAsset(row['Name'], row['Type'], row['Version'], row['Size_MB'], row['Extra'])
        my_lib.add_asset(Mesh_pd)
    elif row['Type'] == 'Texture':
        Texture_pd = TextureAsset(row['Name'], row['Type'], row['Version'], row['Size_MB'], row['Extra'])
        my_lib.add_asset(Texture_pd)

# Starts health-check method
my_lib.run_health_check()
report_list = []

# Scans all assets and adds them with three categories to a dictionary
for a in my_lib.assets:
    asset_dic = {
        "Name": a.name,
        "Category": a.asset_type,
        "status": a.status

    }
    report_list.append(asset_dic)

# Converts report_list to panda DataFrame
df_report = pd.DataFrame(report_list)

# Outputs DataFrame results
print(df_report)