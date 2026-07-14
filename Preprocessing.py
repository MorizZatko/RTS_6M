"""Preprocessing.

This module loads a json file, converts it to a Pandas DataFrame and extracts numerical as well as 
categorical features to get a feature matrix and a target vector.
It then simulates object render times based on vertex count with added random noise and outliers,
to predict these times using random forest regression.
"""

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

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

# Simulate render times based on vertex count with added noise
np.random.seed(42)
y = (X_num[:, 0] * 0.01) * np.random.uniform(0.8, 1.2, len(X_num))

# Add outliers to challenge the model
outliers = np.random.choice(len(y), 5, replace=False)
y[outliers] *= 10

# Split data into training and testing sets
X_train, X_test, y_train, y_test, names_train, names_test = train_test_split(X, y, names, test_size=0.2, random_state=42)

# Initialize and train the random forest regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Get shape of final feature matrix and target vector
X_shape = X.shape
y_shape = y.shape
y_out = y_test
prd_out = predictions

# Create new DataFrame for the results
results_df = pd.DataFrame({
    "Object Name": names_test,
    "Actual Time": y_test,
    "Predicted Time": predictions
})

# Output dataset dimensions
print(f"X-Shape: {X_shape}\n Y-Shape: {y_shape}")
print(f"Y-Test: {y_out}\n Prediction: {prd_out}")
print(results_df.to_string())