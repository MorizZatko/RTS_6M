import pandas as pd
import numpy as np

data = {
    "Asset_Name": ["Hero_Mesh", "Skin_Texture", "Env_Rock", "Grass_Texture", "Cubic_Mesh", "Wall_Texture"],
    "Type": ["Mesh", "Texture", "Mesh", "Texture", "Mesh", "Texture"],
    "Size_MB": [150, 46, 120, 30, 64, 48],
    "Version": [1.2, 2.0, 1.1, 1.0, 3.6, 2.4],
    "Status": ["ready", "work", "ready", "ready", "ready", "work"]
}

df = pd.DataFrame(data)
df['Size_GB'] = df['Size_MB'] / 1024
df['Optimized_Priority'] = np.where(df['Size_MB'] > 100, "Yes", "No")
filter = df[(df['Optimized_Priority'] == 'Yes') & (df['Status'] == 'ready')]

print(filter)