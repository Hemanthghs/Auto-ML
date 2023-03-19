# from app import *

# data = pd.read_csv("/home/hemanthsai/Downloads/drug_inputs.csv")

# data = impute_null(data)
# print(data)


# data, encodings = encode_data(data)
# print(encodings)

# cr_data.update_one({"model_id":int(1)},{"$set":{
#     "encodings":encodings
#     }})

# print(type(encodings))
# print(type(encodings["BP"]["HIGH"]))

# for i in cr_data.find():
#     print(i)

d = {'Sex': {'F': 0, 'M': 1}, 'BP': {'HIGH': 0, 'LOW': 1, 'NORMAL': 2}, 'Cholesterol': {'HIGH': 0, 'NORMAL': 1}}
params = list(d.keys())
values = list(d.values())
params_values = []
for p,v in zip(params, values):
    params_values.append([p,v])

print(params_values)



