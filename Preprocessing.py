"""Preprocessing.

This module loads a json file, converts it to a Pandas DataFrame,
extracts and preprocesses numerical and categorical features using
Scikit-Learn, applies Kmeans clustering as well as PCA reduction.
Finally, it outputs a sorted chart of the clustered objects.
"""

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load JSON data from file
with open('scene.json', 'r') as f:
    data = json.load(f)

# Convert to Pandas DataFrame
df = pd.DataFrame(data['objects'])

# Extract numerical features as NumPy array
X_num = np.array([[obj['Vertices'], *obj['Location']] for obj in data['objects']])

# Extract categorical features as NumPy array
X_cat = np.array([obj['Type'] for obj in data['objects']])
names = np.array([obj['Object Name'] for obj in data['objects']])

# Standardize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_num)

# Encode categorical features
encoder = OneHotEncoder(sparse_output=False)
category_encoded = encoder.fit_transform(X_cat.reshape(-1, 1))

# Combine numerical and categorical features
X = np.hstack((X_scaled, category_encoded))

# Kmeans clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
clusters = kmeans.fit_predict(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Get original vertices count
vertices = X_num[:, 0]

# Create new DataFrame for the results
results_df = pd.DataFrame({
    "Object Name": names,
    "Cluster": clusters,
    "Vertices": vertices
})

# Sort DataFrame by clusters
sorted_df = results_df.sort_values(by="Cluster")

# Output dataset dimensions
print(f"{sorted_df.to_string()}")