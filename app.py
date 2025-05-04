from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

app = Flask(__name__)

# Load and preprocess dataset
df = pd.read_csv("CSV.csv")
df = pd.get_dummies(df, columns=["Soil_color", "District_Name"])

# Features
X = df.drop(["Crop", "Fertilizer", "Link"], axis=1)

# Targets
y_crop = df["Crop"]
y_fert = df["Fertilizer"]

# Split and train crop model
X_train_crop, X_test_crop, y_train_crop, y_test_crop = train_test_split(X, y_crop, test_size=0.2)
crop_model = RandomForestClassifier()
crop_model.fit(X_train_crop, y_train_crop)
joblib.dump(crop_model, "model_crop.pkl")

# Split and train fertilizer model
X_train_fert, X_test_fert, y_train_fert, y_test_fert = train_test_split(X, y_fert, test_size=0.2)
fert_model = RandomForestClassifier()
fert_model.fit(X_train_fert, y_train_fert)
joblib.dump(fert_model, "model_fert.pkl")

# API Endpoint
@app.route("/predict", methods=["POST"])
def predict():
    input_data = request.get_json()
    input_df = pd.DataFrame([input_data])
    
    # One-hot encode to match training
    input_df = pd.get_dummies(input_df)
    for col in X.columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[X.columns]

    # Load models
    crop_model = joblib.load("model_crop.pkl")
    fert_model = joblib.load("model_fert.pkl")

    # Make predictions
    crop_pred = crop_model.predict(input_df)[0]
    fert_pred = fert_model.predict(input_df)[0]

    return jsonify({
        "predicted_crop": crop_pred,
        "predicted_fertilizer": fert_pred
    })

# Run server
if __name__ == "__main__":
    app.run(debug=True)
