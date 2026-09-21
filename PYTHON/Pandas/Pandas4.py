#.iloc is used for position-based selection.

import os
import pandas as pd

data = {
    "Name": ["Rahul", "Aman", "Priya"],
    "Age": [20, 21, 19],
    "Marks": [85, 90, 78]
}

df = pd.DataFrame(data)
print(df)
print("--------")
print(df.iloc[0]) # access the first row
print("--------")
print(df.iloc[0,1]) #first row and second column 