from app import *

data = pd.read_csv("/home/hemanthsai/Downloads/drug_inputs.csv")

data = impute_null(data)
print(data)

data, encodings = encode_data(data)
print(data)
print(encodings)

