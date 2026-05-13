import pandas as pd

data = {
    "Asset_Name": ["Hero_Mesh", "Skin_Texture", "Env_Rock", "Grass_Texture", "Cubic_Mesh", "Wall_Texture"],
    "Type": ["Mesh", "Texture", "Mesh", "Texture", "Mesh", "Texture"],
    "Size_MB": [150, 46, 120, 30, 64, 48],
    "Version": [1.2, 2.0, 1.1, 1.0, 3.6, 2.4],
    "Status": ["ready", "work", "ready", "ready", "ready", "work"]
}

df = pd.DataFrame(data)
summary = df.groupby('Type').agg({'Size_MB': 'sum', 'Version': 'mean'})
mesh_size = summary.loc['Mesh', 'Size_MB']
print(summary)
print(f"Die Meshes wiegen insgesamt {mesh_size} MB")