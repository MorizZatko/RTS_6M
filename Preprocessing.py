"""Preprocessing.

This module loads a json file, converts it to a Pandas DataFrame and extracts numerical as well as 
categorical features to get a feature matrix and a target vector.
Finally, it outputs the dataset dimensions as a string via standard terminal.
"""

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Load JSON data from file
with open('scene.json', 'r') as f:
    data = json.load(f)

# Convert to Pandas DataFrame
df = pd.DataFrame(data['objects'])

# Extract numerical features as NumPy array
X_num = np.array([[obj['Vertices'], *obj['Location']] for obj in data['objects']])

# Extract categorical features as NumPy array
X_cat = np.array([obj['Type'] for obj in data['objects']])

# Standardize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_num)

# Encode categorical features
encoder = OneHotEncoder(sparse_output=False)
category_encoded = encoder.fit_transform(X_cat.reshape(-1, 1))

# Combine numerical and categorical features
X = np.hstack((X_scaled, category_encoded))

# Create binary targets based on Vertices threshold
y = np.array([1 if obj['Vertices'] > 500 else 0 for obj in data['objects']])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Get shape of final feature matrix and target vector
X_shape = X.shape
y_shape = y.shape

# Output dataset dimensions
print(f"X-Shape: {X_shape}\n Y-Shape: {y_shape}")