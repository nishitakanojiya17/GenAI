# head & tail 

import os
import pandas as pd

data = {
    "Name": ["Rahul", "Aman", "Priya","Arpita","Rohit","Sakshi","ARpit","Nishita"],
    "Age": [20, 21, 19, 22, 20, 21, 23, 20],
    "Marks": [85, 90, 78, 88, 92, 80, 75, 89]
}

df = pd.DataFrame(data)
print(df)
print("--------")
print(df.head()) # returns the first 5 rows of the dataframe
print("--------")
print(df.tail()) # returns the last 5 rows of the dataframe
