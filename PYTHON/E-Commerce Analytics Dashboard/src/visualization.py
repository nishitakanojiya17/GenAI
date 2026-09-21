import matplotlib.pyplot as plt
import seaborn as sns
import os


# ==========================================================
# OUTPUT DIRECTORY
# ==========================================================

# Create output directory if it does not exist
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# 1. ORDER STATUS
# ==========================================================

def plot_order_status(df):

    plt.figure(figsize=(10, 6))

    status_counts = df["Status"].value_counts()

    sns.barplot(
        x=status_counts.index,
        y=status_counts.values
    )

    plt.title("Order Status Distribution")
    plt.xlabel("Order Status")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "order_status.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 2. CATEGORY SALES
# ==========================================================

def plot_category_sales(df):

    category_sales = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=category_sales.values,
        y=category_sales.index
    )

    plt.title("Revenue by Product Category")
    plt.xlabel("Revenue")
    plt.ylabel("Category")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "category_sales.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 3. MONTHLY SALES
# ==========================================================

def plot_monthly_sales(df):

    monthly = (
        df.groupby("Year_Month")["Amount"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=monthly,
        x="Year_Month",
        y="Amount",
        marker="o"
    )

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "monthly_sales.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 4. TOP 10 STATES
# ==========================================================

def plot_top_states(df):

    state_sales = (
        df.groupby("ship-state")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=state_sales.values,
        y=state_sales.index
    )

    plt.title("Top 10 States by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("State")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "top_states.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 5. SIZE DISTRIBUTION
# ==========================================================

def plot_size_distribution(df):

    size_counts = df["Size"].value_counts()

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=size_counts.index,
        y=size_counts.values
    )

    plt.title("Product Size Distribution")
    plt.xlabel("Size")
    plt.ylabel("Number of Orders")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "size_distribution.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 6. FULFILMENT
# ==========================================================

def plot_fulfilment(df):

    fulfilment_counts = df["Fulfilment"].value_counts()

    plt.figure(figsize=(8, 6))

    sns.barplot(
        x=fulfilment_counts.index,
        y=fulfilment_counts.values
    )

    plt.title("Orders by Fulfilment Method")
    plt.xlabel("Fulfilment")
    plt.ylabel("Number of Orders")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "fulfilment.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 7. B2B VS NON-B2B
# ==========================================================

def plot_b2b_sales(df):

    b2b_sales = (
        df.groupby("B2B")["Amount"]
        .sum()
        .reset_index()
    )

    b2b_sales["B2B"] = b2b_sales["B2B"].astype(str)

    plt.figure(figsize=(8, 6))

    sns.barplot(
        data=b2b_sales,
        x="B2B",
        y="Amount"
    )

    plt.title("B2B vs Non-B2B Revenue")
    plt.xlabel("B2B")
    plt.ylabel("Revenue")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "b2b_sales.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 8. QUANTITY VS REVENUE
# ==========================================================

def plot_quantity_vs_revenue(df):

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="Qty",
        y="Amount",
        alpha=0.5
    )

    plt.title("Quantity vs Revenue")
    plt.xlabel("Quantity")
    plt.ylabel("Revenue")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "quantity_vs_revenue.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 9. REVENUE DISTRIBUTION
# ==========================================================

def plot_revenue_distribution(df):

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["Amount"].dropna(),
        bins=50,
        kde=True
    )

    plt.title("Revenue Distribution")
    plt.xlabel("Order Amount")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "revenue_distribution.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# 10. CORRELATION HEATMAP
# ==========================================================

def plot_correlation(df):

    numerical_df = df[
        ["Qty", "Amount", "ship-postal-code"]
    ].copy()

    correlation = numerical_df.corr()

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Numerical Feature Correlation")

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "correlation_heatmap.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()


# ==========================================================
# RUN ALL VISUALIZATIONS
# ==========================================================

if __name__ == "__main__":

    # Import cleaning functions
    from Data_cleaning import load_data, clean_data

    # ======================================================
    # DATASET PATH
    # ======================================================

    file_path = "D:\\Python\\E-Commerce Analytics Dashboard\\datasets\\Amazon Sale Report.csv"

    # ======================================================
    # LOAD DATA
    # ======================================================

    print("\nLoading dataset...")

    df = load_data(file_path)

    # ======================================================
    # CLEAN DATA
    # ======================================================

    print("Cleaning dataset...")

    df = clean_data(df)

    print("\nDataset ready for visualization!")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

    # ======================================================
    # CREATE GRAPHS
    # ======================================================

    print("\nCreating visualizations...\n")

    print("1. Creating Order Status graph...")
    plot_order_status(df)

    print("2. Creating Category Sales graph...")
    plot_category_sales(df)

    print("3. Creating Monthly Sales graph...")
    plot_monthly_sales(df)

    print("4. Creating Top 10 States graph...")
    plot_top_states(df)

    print("5. Creating Size Distribution graph...")
    plot_size_distribution(df)

    print("6. Creating Fulfilment graph...")
    plot_fulfilment(df)

    print("7. Creating B2B Sales graph...")
    plot_b2b_sales(df)

    print("8. Creating Quantity vs Revenue graph...")
    plot_quantity_vs_revenue(df)

    print("9. Creating Revenue Distribution graph...")
    plot_revenue_distribution(df)

    print("10. Creating Correlation Heatmap...")
    plot_correlation(df)

    # ======================================================
    # COMPLETION MESSAGE
    # ======================================================

    print("\n" + "=" * 60)
    print("ALL GRAPHS CREATED SUCCESSFULLY!")
    print("=" * 60)

    print(f"\nGraphs saved directly in:")
    print(os.path.abspath(OUTPUT_DIR))