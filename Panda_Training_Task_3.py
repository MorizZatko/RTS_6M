import pandas as pd
import numpy as np

data = {
    'Name': ['SkyboxTextures', 'TerrainMeshes', 'CharacterModels', 'VehicleAnimations',
             'LightingPresets', 'WaterMesh', 'VegetationAssets', 'ParticleEffects',
             'EnvironmentProps', 'UIElements'],
    'Category': ['Texture', 'Mesh', 'Texture', 'Animation',
                 'Mesh', 'Mesh', 'Animation', 'Texture',
                 'Props', 'UI'],
    'Size_MB': [200, 1288, 300, 100,
                10, 200, 50, 4680,
                75, 50],
    'Status': ['Ready', 'Work', 'Ready', 'Ready',
               'Ready', 'Ready', 'Ready', 'Ready',
               'Ready', 'Work']
}

df = pd.DataFrame(data)
df_clean = df[(df['Size_MB'] <= 1000)]
clean_sum = df_clean.groupby('Category').agg({'Size_MB': 'sum', 'Name': 'count'})
mesh_sum = clean_sum.loc['Mesh', 'Size_MB']

print(f"Die bereinigten Meshes nehmen insgesamt: ", mesh_sum, "MB Speicherplatz ein.")