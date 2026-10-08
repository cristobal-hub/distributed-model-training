from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LogisticRegression
import sys

app = Flask(__name__)

# Get dataset index from command line argument (default to 1)
dataset_idx = sys.argv[1] if len(sys.argv) > 1 else "1"
# Get port from command line argument (default to 5000)
port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

print(f"Loading data from dataset {dataset_idx}...")

# Load local dataset based on index
data_file = f"data{dataset_idx}.csv" if dataset_idx != "1" else "data.csv"
label_file = f"label{dataset_idx}.csv" if dataset_idx != "1" else "label.csv"

X = pd.read_csv(data_file, header=None)
y = pd.read_csv(label_file, header=None).values.ravel()

print("Training model...")

model = LogisticRegression(max_iter=200)
model.fit(X, y)

print("Model ready!")

# Endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['data']
    prediction = model.predict([data])
    return jsonify({'prediction': int(prediction[0])})

# Status endpoint
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "running"})

app.run(host='0.0.0.0', port=port)