import pandas as pd

data = {
    "Asset_Name": ["Hero_Mesh", "Skin_Texture", "Env_Rock", "Grass_Texture"],
    "Type": ["Mesh", "Texture", "Mesh", "Texture"],
    "Size_MB": [150, 46, 120, 30],
    "Version": [1.2, 2.0, 1.1, 1.0],
    "Status": ["work", "ready", "work", "ready"]
}

df = pd.DataFrame(data)
df_approved = df[df['Status'] == 'ready']
f2 = df.head(2)


print(f2)
print(df['Size_MB'].describe())
print(df_approved)