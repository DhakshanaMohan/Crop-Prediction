import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

# Define the relative path to the CSV file
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crop_data.csv')

# Load the data
data = pd.read_csv(data_path)

# Features and target for crop prediction
X = data[['Soil Type', 'Ideal Season', 'Average Temperature (°C)', 'Average Rainfall (mm)']]
y_crop = data['Crop']

# Encode categorical data
X = pd.get_dummies(X)

# Split data for training
X_train, X_test, y_train_crop, y_test_crop = train_test_split(X, y_crop, test_size=0.2, random_state=42)

# Train crop model
crop_model = DecisionTreeClassifier(random_state=42)
crop_model.fit(X_train, y_train_crop)

# Save crop model
model_dir_crop = os.path.join(os.path.dirname(__file__), "crop_recommendation.pkl")
joblib.dump(crop_model, model_dir_crop)

# Evaluate model
crop_accuracy = crop_model.score(X_test, y_test_crop)
print(f"Crop Model Accuracy: {crop_accuracy * 100:.2f}%")
