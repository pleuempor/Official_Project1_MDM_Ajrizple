from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error





client = MongoClient('mongodb+srv://mongodb:project1.@mongodb-p1-ajrizple.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')
db = client['MDMProjectOne']
collection = db['HotelSummary']


documents = collection.find({})
df = pd.DataFrame(list(documents))

df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).astype(float)
df['reviews count'] = df['reviews count'].str.replace(',', '').astype(int)
df['score'] = df['score'].astype(float)
df['is_25_may'] = df['date'].apply(lambda x: 1 if x == "2024-05-25" else 0)


X = df[['score', 'reviews count']].values
y = df['price'].values.astype(float)  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

polynomial_degree = 2

model = make_pipeline(PolynomialFeatures(degree=polynomial_degree), LinearRegression())

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = model.score(X_test, y_test)
msle = mean_squared_log_error(y_test, y_pred)
median_ae = median_absolute_error(y_test, y_pred)

print(f'Median Absolute Error: {median_ae}')
print(f'Mean Squared Logarithmic Error: {msle}')

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

for col in df.columns:
    if df[col].dtype == 'object' or isinstance(df[col].dtype, pd.CategoricalDtype):
        df = df.drop(col, axis=1)
        
corr = df.corr()

sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')

plt.title('Korrelationsmatrix')

plt.show()

client.close()

import joblib
joblib.dump(model, 'hotel_price_prediction_model.pkl')
