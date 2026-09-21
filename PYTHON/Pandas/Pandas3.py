#Selecting Rows using .loc
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
print(df.loc[0])
print("--------")
print(df.loc[1])
print("--------")
print(df.loc[2,"Name"]) # access the particular value of the row and column