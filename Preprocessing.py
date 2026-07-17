"""Preprocessing.

This module loads a json file, converts it to a Pandas DataFrame,
expands vector-based location data, preprocesses numerical and categorical features.
It then trains a Logistic Regression model to classify objects based on their vertex count
and predicts the status of a new asset.
"""

import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Load JSON data from file
with open('scene.json', 'r') as f:
    data = json.load(f)

# Convert to Pandas DataFrame
df = pd.DataFrame(data['objects'])

# Expand location items
loc_df = pd.DataFrame(df['Location'].tolist(),
                      columns=['loc_x', 'loc_y', 'loc_z'])

# Fuse dataframe with the expanded location data and drop the original list 
df_expand = df.drop(columns=['Location']).join(loc_df)

# Define preprocessing for numerical and categorical features 
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['loc_x', 'loc_y', 'loc_z', 'Vertices']),
        ('cat', OneHotEncoder(), ['Type'])
    ]
)

# Pipeline logic, combining scaling, encoding, and the logistic regression model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

# Create binary target labels based on vertex threshold
y = np.array([1 if obj['Vertices'] > 500 else 0 for obj in data['objects']])

# Fit the pipeline on the expanded features and generate target labels
pipeline.fit(df_expand, y)

# Define new test asset to verify model predictions
new_asset = pd.DataFrame({
    'Object Name': ['Test_Hero_Asset'],
    'Vertices': [1200],
    'Type': ['Mesh'],
    'loc_x': [0.5],
    'loc_y': [0.2],
    'loc_z': [0.8]
})

# Predict the target label for the test asset using the trained pipeline
prediction = pipeline.predict(new_asset)

# Map the binary prediction to string status labels
result = "PDR" if prediction[0] == 1 else "WIP"

# Output dataset and test asset output
print(f"{df.to_string()}")
print(f"Test Object To Predict:\nObject: {new_asset['Object Name'][0]} | Result: {result}")