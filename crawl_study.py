import pandas as pd
import numpy as np
import json

print("hello")
data = pd.read_json("C:/Users/dpgbu/Desktop/SAE/university/UROP/IStoreService_GetAppList_v1_1.json", orient="columns")
print(data.head())
data.to_csv("C:/Users/dpgbu/Desktop/SAE/university/UROP/IStoreService_GetAppList_v1_1.csv", index=False)