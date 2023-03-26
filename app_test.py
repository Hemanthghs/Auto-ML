import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling

df = pd.read_csv("/home/hemanthsai/Desktop/Auto ML/app/data/cancer_input.csv")

# se = pd.plotting.scatter_matrix(df)
# plt.show()

# sr = pd.plotting.parallel_coordinates(df)
# plt.show()

report = pandas_profiling.ProfileReport(df)
report.to_file("test.html")
