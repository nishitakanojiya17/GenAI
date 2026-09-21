import pandas as pd
import numpy as np


# ==========================================================
# BASIC SALES ANALYSIS
# ==========================================================

def sales_summary(df):
    """Return basic sales statistics."""

    summary = {
        "Total Revenue": df["Amount"].sum(),
        "Average Order Value": df["Amount"].mean(),
        "Median Order Value": df["Amount"].median(),
        "Maximum Order Value": df["Amount"].max(),
        "Minimum Order Value": df["Amount"].min(),
        "Total Quantity Sold": df["Qty"].sum(),
        "Average Quantity per Order": df["Qty"].mean()
    }

    return summary


# ==========================================================
# CATEGORY ANALYSIS
# ==========================================================

def category_analysis(df):
    """Analyze sales by product category."""

    result = (
        df.groupby("Category")
        .agg(
            Orders=("Order ID", "count"),
            Quantity=("Qty", "sum"),
            Revenue=("Amount", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    return result


# ==========================================================
# MONTHLY SALES ANALYSIS
# ==========================================================

def monthly_sales(df):
    """Calculate monthly revenue."""

    result = (
        df.groupby("Year_Month")
        .agg(
            Orders=("Order ID", "count"),
            Quantity=("Qty", "sum"),
            Revenue=("Amount", "sum")
        )
        .reset_index()
    )

    return result


# ==========================================================
# STATE-WISE SALES
# ==========================================================

def state_sales(df):
    """Analyze revenue by shipping state."""

    result = (
        df.groupby("ship-state")
        .agg(
            Orders=("Order ID", "count"),
            Quantity=("Qty", "sum"),
            Revenue=("Amount", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    return result


# ==========================================================
# TOP SKU ANALYSIS
# ==========================================================

def top_skus(df, n=10):
    """Find top N SKUs based on revenue."""

    result = (
        df.groupby("SKU")
        .agg(
            Orders=("Order ID", "count"),
            Quantity=("Qty", "sum"),
            Revenue=("Amount", "sum")
        )
        .sort_values("Revenue", ascending=False)
        .head(n)
    )

    return result


# ==========================================================
# SIZE ANALYSIS
# ==========================================================

def size_analysis(df):
    """Analyze sales by product size."""

    result = (
        df.groupby("Size")
        .agg(
            Orders=("Order ID", "count"),
            Quantity=("Qty", "sum"),
            Revenue=("Amount", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    return result


# ==========================================================
# FULFILMENT ANALYSIS
# ==========================================================

def fulfilment_analysis(df):
    """Analyze revenue by fulfilment method."""

    result = (
        df.groupby("Fulfilment")
        .agg(
            Orders=("Order ID", "count"),
            Quantity=("Qty", "sum"),
            Revenue=("Amount", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )

    return result


# ==========================================================
# B2B ANALYSIS
# ==========================================================

def b2b_analysis(df):
    """Compare B2B and non-B2B sales."""

    result = (
        df.groupby("B2B")
        .agg(
            Orders=("Order ID", "count"),
            Quantity=("Qty", "sum"),
            Revenue=("Amount", "sum")
        )
    )

    return result


# ==========================================================
# ORDER STATUS ANALYSIS
# ==========================================================

def order_status_analysis(df):
    """Analyze order status."""

    result = (
        df.groupby("Status")
        .agg(
            Orders=("Order ID", "count"),
            Revenue=("Amount", "sum")
        )
        .sort_values("Orders", ascending=False)
    )

    return result


# ==========================================================
# NUMPY STATISTICS
# ==========================================================

def numpy_statistics(df):
    """Calculate sales statistics using NumPy."""

    amount = df["Amount"].dropna().to_numpy()

    statistics = {
        "Mean": np.mean(amount),
        "Median": np.median(amount),
        "Standard Deviation": np.std(amount),
        "Minimum": np.min(amount),
        "Maximum": np.max(amount)
    }

    return statistics


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    from Data_cleaning import load_data, clean_data

    file_path = "D:\\Python\\E-Commerce Analytics Dashboard\\datasets\\Amazon Sale Report.csv"

    df = load_data(file_path)
    df = clean_data(df)

    print("\n========== SALES SUMMARY ==========")

    summary = sales_summary(df)

    for key, value in summary.items():
        print(f"{key}: {value:,.2f}")

    print("\n========== CATEGORY ANALYSIS ==========")
    print(category_analysis(df))

    print("\n========== MONTHLY SALES ==========")
    print(monthly_sales(df))

    print("\n========== TOP 10 SKUs ==========")
    print(top_skus(df))

    print("\n========== STATE-WISE SALES ==========")
    print(state_sales(df).head(10))

    print("\n========== FULFILMENT ANALYSIS ==========")
    print(fulfilment_analysis(df))

    print("\n========== B2B ANALYSIS ==========")
    print(b2b_analysis(df))

    print("\n========== ORDER STATUS ==========")
    print(order_status_analysis(df))

    print("\n========== NUMPY STATISTICS ==========")
    print(numpy_statistics(df))