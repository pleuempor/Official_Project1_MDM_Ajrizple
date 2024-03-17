from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient, ContainerClient
import os
import joblib
from io import BytesIO

app = Flask(__name__)

def get_latest_model_container_name(blob_service_client, prefix="score-prediction-modell-v"):
    containers = blob_service_client.list_containers(name_starts_with=prefix)
    latest_version = 0
    latest_container_name = None
    for container in containers:
        version_part = container['name'].replace(prefix, "")
        if version_part.isdigit():
            version = int(version_part)
            if version > latest_version:
                latest_version = version
                latest_container_name = container['name']
    return latest_container_name

def load_model_from_blob():
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    latest_container_name = get_latest_model_container_name(blob_service_client)
    
    if latest_container_name is None:
        raise ValueError("Kein Modellcontainer gefunden.")
    
    container_client = blob_service_client.get_container_client(latest_container_name)
    blob_list = container_client.list_blobs()
    latest_model_blob_name = None
    
    for blob in blob_list:
        latest_model_blob_name = blob.name
        break
    
    if latest_model_blob_name is None:
        raise ValueError("Kein Modell im Container gefunden.")
    
    blob_client = container_client.get_blob_client(latest_model_blob_name)
    blob_data = blob_client.download_blob().readall()
    model = joblib.load(BytesIO(blob_data))
    
    return model

# Das Modell wird beim Start der App geladen
model = load_model_from_blob()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        score = float(data['score'])
        reviews_count = int(data['reviews_count'])
        prediction = model.predict([[score, reviews_count]])
        return jsonify({'predicted_price': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
