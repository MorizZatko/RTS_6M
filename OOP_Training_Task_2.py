class Material:
    def __init__(self, shader_name, base_color):
        self.shader_name = shader_name
        self.base_color = base_color

class Asset:
    def __init__(self, name, asset_type, version, size):
        self.name = name
        self.asset_type = asset_type
        self.version = version
        self.size = size
    

class MeshAsset(Asset):
    def __init__(self, name, asset_type, version, size, material):
        
        super().__init__(name, "Mesh", version, size)
        self.material = material

    def describe(self):
        shader = self.material.shader_name
        color = self.material.base_color
        return f"Mesh: {self.name} nutzt Shader: {shader} mit Base_Color: {color}"
       
my_material = Material("Standard_Shader", "RED")
my_mesh = MeshAsset("Stone", "mesh", 3.6, 1250, my_material)

print(my_mesh.describe())