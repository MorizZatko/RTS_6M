class Asset:
    def __init__(self, name, asset_type, version, size):
        self.name = name
        self.asset_type = asset_type
        self.version = version
        self.size = size

    def describe(self):
        return f"{self.name} {self.asset_type} V{self.version} - {self.size}MB"
    

class AssetLibary:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset_obj):
        self.assets.append(asset_obj)

    def get_total_size(self):
        total = 0
        for a in self.assets:
            total += a.size
        return total
    
    def list_all_assets(self):
        for a in self.assets:
            print(a.describe())
    

Mesh_1 = Asset("Asset_1", "Mesh", 1.6, 150)
Texture_1 = Asset("Asset_2", "Texture", 3.4, 164)

my_lib = AssetLibary()

my_lib.add_asset(Mesh_1)
my_lib.add_asset(Texture_1)

my_lib.list_all_assets()       
print(f"Insgesamte Größe:", my_lib.get_total_size())