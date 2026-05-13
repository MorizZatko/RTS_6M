class Asset:
    def __init__(self, name, asset_type, version, size):
        self.name = name
        self.asset_type = asset_type
        self.version = version
        self.size = size

    def describe(self):
        return f"Asset {self.name} ({self.asset_type}) V{self.version:.1f} - {self.size}MB"
    
    def update_version(self):
        self.version += 0.1

class TextureAsset(Asset):
    def __init__(self, name, asset_type, version, size, resolution):
        super().__init__(name, asset_type, version, size)
        self.resolution = resolution
    
    def describe(self):
        return f"TextureAsset {self.name} ({self.asset_type}) V{self.version:.1f} Res:{self.resolution} - {self.size}MB"

class MeshAsset(Asset):
    def __init__(self, name, asset_type, version, size, polycount):
        super().__init__(name, asset_type, version, size)
        self.polycount = polycount

    def describe(self):
        return f"Asset {self.name} ({self.asset_type}) V{self.version:.1f} Poly:{self.polycount} - {self.size}MB"


my_mesh = MeshAsset("Hero_Charakter", "Mesh", 1.6, 150, 6400)
my_texture = TextureAsset("Skin_Texture", "Texture", 1.2, 46, "1080x1920")


my_texture.update_version()
my_texture.update_version()
my_mesh.update_version()

print(my_mesh.describe())
print(my_texture.describe())