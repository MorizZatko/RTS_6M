"""Preprocessing.

This module loads a json file, converts it to a Pandas DataFrame and extracts numerical as well as 
categorical features to get a feature matrix and a target vector.
It then simulates object render times based on vertex count with added random noise and predicts
these times using linear regression.
"""

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression

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

# Simulate render times
np.random.seed(42)
y = (X_num[:, 0] * 0.01) + np.random.random(len(X_num)) * 0.5

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict render times for the test set
predictions = model.predict(X_test)

# Get shape of final feature matrix and target vector
X_shape = X.shape
y_shape = y.shape

# Shape output
y_out = y_test[:5]
prd_out = predictions[:5]

# Output dataset dimensions
print(f"X-Shape: {X_shape}\n Y-Shape: {y_shape}")
print(f"Y-Test: {y_out}\n Prediction: {prd_out}")