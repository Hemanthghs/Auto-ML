from app import *

data = pd.read_csv("/home/hemanthsai/Downloads/drug_inputs.csv")

data = impute_null(data)
print(data)


data, encodings = encode_data(data)
print(encodings)

cr_data.update_one({"model_id":int(1)},{"$set":{
    "encodings":encodings
    }})

print(type(encodings))
print(type(encodings["BP"]["HIGH"]))

for i in cr_data.find():
    print(i)

