# import seaborn as sns
# import pandas as pd
# import matplotlib.pyplot as plt
# import pandas_profiling
# from app import *

# df = pd.read_csv("/home/hemanthsai/Desktop/Auto ML/app/data/cancer_input.csv")

# X = df
# y = pd.read_csv("/home/hemanthsai/Desktop/Auto ML/app/data/cancer_output.csv")

# X = impute_null(X)
# X, encodings = encode_data(X)

# model = LogisticRegression()
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# metrics = dict()

# model.fit(X_train, y_train)

# y_pred = model.predict(X_train)
# y_train = np.reshape(y_train, (y_train.shape[0], ))
# y_pred = np.reshape(y_pred, (y_pred.shape[0], ))
# acc = accuracy_score(y_train, y_pred)
# prec = precision_score(y_train, y_pred, average='weighted')
# rec = recall_score(y_train, y_pred, average='weighted')
# f1 = f1_score(y_train, y_pred, average='weighted')

# print(type(acc.item()), type(prec), type(rec), type(f1))

a = [1,2,3]
print(a[:100])