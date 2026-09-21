import pandas as pd
import numpy as np


# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

def load_data(file_path):
    """Load Amazon sales CSV dataset."""
    df = pd.read_csv("D:\\Python\\E-Commerce Analytics Dashboard\\datasets\\Amazon Sale Report.csv", low_memory=False)
    return df


# --------------------------------------------------
# 2. CLEAN COLUMN NAMES
# --------------------------------------------------

def clean_column_names(df):
    """
    Remove leading/trailing spaces from column names.
    """
    df.columns = df.columns.str.strip()

    return df


# --------------------------------------------------
# 3. REMOVE UNNECESSARY COLUMNS
# --------------------------------------------------

def remove_unnecessary_columns(df):
    """
    Remove empty/unnamed columns if present.
    """

    columns_to_remove = [
        "Unnamed: 22"
    ]

    existing_columns = [
        col for col in columns_to_remove
        if col in df.columns
    ]

    df = df.drop(columns=existing_columns)

    return df


# --------------------------------------------------
# 4. REMOVE DUPLICATES
# --------------------------------------------------

def remove_duplicates(df):
    """
    Remove duplicate rows.
    """

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(f"Duplicate rows removed: {before - after}")

    return df


# --------------------------------------------------
# 5. CONVERT DATE
# --------------------------------------------------

def convert_date(df):
    """
    Convert Date column into datetime format.
    """

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%m-%d-%y",
            errors="coerce"
        )

    return df


# --------------------------------------------------
# 6. NUMERIC COLUMNS
# --------------------------------------------------

def convert_numeric_columns(df):
    """
    Convert important numerical columns to numeric datatype.
    """

    numeric_columns = [
        "Qty",
        "Amount",
        "ship-postal-code"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# --------------------------------------------------
# 7. HANDLE MISSING VALUES
# --------------------------------------------------

def handle_missing_values(df):
    """
    Handle missing values according to column meaning.
    """

    # Amount missing means we cannot calculate sales
    if "Amount" in df.columns:
        df = df.dropna(subset=["Amount"])

    # Quantity missing
    if "Qty" in df.columns:
        df["Qty"] = df["Qty"].fillna(0)

    # Category missing
    if "Category" in df.columns:
        df["Category"] = df["Category"].fillna("Unknown")

    # Size missing
    if "Size" in df.columns:
        df["Size"] = df["Size"].fillna("Unknown")

    # State missing
    if "ship-state" in df.columns:
        df["ship-state"] = df["ship-state"].fillna("Unknown")

    # B2B missing
    if "B2B" in df.columns:
        df["B2B"] = df["B2B"].fillna(False)

    return df


# --------------------------------------------------
# 8. CREATE NEW FEATURES
# --------------------------------------------------

def create_features(df):
    """
    Create useful columns for analysis.
    """

    # Month
    if "Date" in df.columns:

        df["Year"] = df["Date"].dt.year

        df["Month"] = df["Date"].dt.month

        df["Month_Name"] = df["Date"].dt.strftime("%B")

        df["Year_Month"] = (
            df["Date"].dt.to_period("M").astype(str)
        )

    # Revenue per quantity
    if "Amount" in df.columns and "Qty" in df.columns:

        df["Revenue_Per_Item"] = np.where(
            df["Qty"] > 0,
            df["Amount"] / df["Qty"],
            0
        )

    return df


# --------------------------------------------------
# 9. COMPLETE CLEANING PIPELINE
# --------------------------------------------------

def clean_data(df):

    print("Starting data cleaning...")

    print(f"Initial rows: {len(df)}")
    print(f"Initial columns: {len(df.columns)}")

    df = clean_column_names(df)

    df = remove_unnecessary_columns(df)

    df = remove_duplicates(df)

    df = convert_date(df)

    df = convert_numeric_columns(df)

    df = handle_missing_values(df)

    df = create_features(df)

    print("\nCleaning completed.")

    print(f"Final rows: {len(df)}")
    print(f"Final columns: {len(df.columns)}")

    return df


# --------------------------------------------------
# TEST THE FILE DIRECTLY
# --------------------------------------------------

if __name__ == "__main__":

    file_path = "D:\\Python\\E-Commerce Analytics Dashboard\\datasets\\Amazon Sale Report.csv"

    df = load_data(file_path)

    df = clean_data(df)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())