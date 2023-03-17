from app import preprocess
import pandas as pd
from sklearn.preprocessing import LabelEncoder


data = pd.read_csv("/home/hemanthsai/Desktop/Auto ML/app/data/data.csv")

print(data)

for col in data.columns:
    if data[col].isnull().any():
        if data[col].dtype == "object":
            data[col] = data[col].fillna(data[col].mode()[0])
        else:
            data[col] = data[col].fillna(data[col].mean())

print(data)




