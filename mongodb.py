import pandas as pd
from pymongo import MongoClient
import json


csv_file_path = 'hotels_list.csv' 
json_file_path = 'data.json' 


df = pd.read_csv(csv_file_path)
df['score'] = df['score'].str.extract('(\d+\.\d+)').astype(float)

df.to_json(json_file_path, orient='records', lines=True)




cosmos_url = "mongodb+srv://mongodb:project1.@mongodb-p1-ajrizple.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(cosmos_url)
db = client['MDMProjectOne']
collection = db['HotelSummary']


with open(json_file_path, 'r') as file:
    data = [json.loads(line) for line in file]


collection.insert_many(data)

print(f"Es wurden {len(data)} Datensätze erfolgreich in Cosmos DB importiert.")


client.close()
