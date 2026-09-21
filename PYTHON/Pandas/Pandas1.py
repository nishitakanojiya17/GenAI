import os
import pandas as pd

data = {
    "Name": ["Rahul", "Aman", "Priya"],
    "Age": [20, 21, 19],
    "Marks": [85, 90, 78]
}

df = pd.DataFrame(data,index=['s1','s2','s3'])

print(df)
print(df.shape)
print(df.size)
print(df.ndim)
print(df.columns)
print(df.index)