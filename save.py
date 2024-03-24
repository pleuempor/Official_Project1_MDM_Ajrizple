from azure.storage.blob import BlobServiceClient
import argparse

def create_blob_service_client(connection_string):
    return BlobServiceClient.from_connection_string(connection_string)

def get_latest_container_version(blob_service_client, prefix):
    containers = blob_service_client.list_containers(name_starts_with=prefix)
    max_version = 0
    for container in containers:
        version_part = container.name.replace(prefix, "").replace("v", "")
        if version_part.isdigit():
            version = int(version_part)
            max_version = max(version, max_version)
    return max_version

def main(connection_string):
    local_file_path = "hotel_price_prediction_model.pkl"  
    blob_service_client = create_blob_service_client(connection_string)
    prefix = "score-prediction-modell-v"
    latest_version = get_latest_container_version(blob_service_client, prefix)
    new_version = latest_version + 1
    new_container_name = f"{prefix}{new_version}"

    
    container_client = blob_service_client.create_container(new_container_name)

    blob_client = container_client.get_blob_client("model")

   
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)

    print(f"Model uploaded to container: {new_container_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a model to Azure Blob Storage with versioning.")
    parser.add_argument("-c", "--connection-string", required=True, help="Azure Blob Storage connection string.")
    args = parser.parse_args()

    main(args.connection_string)
