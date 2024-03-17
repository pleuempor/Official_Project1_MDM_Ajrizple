import pandas as pd
from pymongo import MongoClient
import json

# Schritt 1: CSV in JSON umwandeln
csv_file_path = 'hotels_list.csv'  # Pfad zur CSV-Datei
json_file_path = 'data.json'  # Ziel-JSON-Dateipfad

# CSV-Datei einlesen
df = pd.read_csv(csv_file_path)
df['score'] = df['score'].str.extract('(\d+\.\d+)').astype(float)
# DataFrame in ein JSON-Format umwandeln und in eine Datei schreiben
df.to_json(json_file_path, orient='records', lines=True)

# Schritt 2: JSON in Azure Cosmos DB importieren

# Verbindung zu Cosmos DB herstellen
cosmos_url = "mongodb+srv://mongodb:project1.@mongodb-p1-ajrizple.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(cosmos_url)
db = client['MDMProjectOne']
collection = db['HotelSummary']

# JSON-Daten einlesen
with open(json_file_path, 'r') as file:
    data = [json.loads(line) for line in file]

# Daten in Cosmos DB einfügen
collection.insert_many(data)

print(f"Es wurden {len(data)} Datensätze erfolgreich in Cosmos DB importiert.")

# Verbindung schließen
client.close()
