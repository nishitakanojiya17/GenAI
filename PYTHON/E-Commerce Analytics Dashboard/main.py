from src.Data_cleaning import load_data, clean_data 

#data set path
file_path = "D:\\Python\\E-Commerce Analytics Dashboard\\datasets\\Amazon Sale Report.csv"

#load dataset
df=load_data("D:\\Python\\E-Commerce Analytics Dashboard\\datasets\\Amazon Sale Report.csv")

#clean data
df=clean_data(df)

#display results
print("\n Final dataset")
print(df.head())

print("\n Dataset Shape") 
print(df.shape)