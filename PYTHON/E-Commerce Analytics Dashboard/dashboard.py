import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Amazon Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    color: #666;
    font-size: 17px;
    margin-bottom: 25px;
}

.metric-card {
    padding: 20px;
    border-radius: 10px;
    background-color: #f8f9fa;
    border: 1px solid #e5e5e5;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# DATA LOADING
# ==========================================================

@st.cache_data
def load_dataset():

    file_path = "D:\\Python\\E-Commerce Analytics Dashboard\\datasets\\Amazon Sale Report.csv"

    df = pd.read_csv(
        file_path,
        low_memory=False
    )

    # Clean column names
    df.columns = df.columns.str.strip()

    # Remove unnecessary column
    if "Unnamed: 22" in df.columns:
        df.drop(columns=["Unnamed: 22"], inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%m-%d-%y",
            errors="coerce"
        )

    # Convert numerical columns
    for column in ["Qty", "Amount", "ship-postal-code"]:

        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Missing values
    if "Category" in df.columns:
        df["Category"] = df["Category"].fillna("Unknown")

    if "Size" in df.columns:
        df["Size"] = df["Size"].fillna("Unknown")

    if "ship-state" in df.columns:
        df["ship-state"] = df["ship-state"].fillna("Unknown")

    if "Qty" in df.columns:
        df["Qty"] = df["Qty"].fillna(0)

    if "B2B" in df.columns:
        df["B2B"] = df["B2B"].fillna(False)

    # Remove rows without revenue
    if "Amount" in df.columns:
        df = df.dropna(subset=["Amount"])

    # Create date features
    if "Date" in df.columns:

        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month

        df["Month_Name"] = df["Date"].dt.strftime("%b")

        df["Year_Month"] = (
            df["Date"]
            .dt.to_period("M")
            .astype(str)
        )

    return df


# ==========================================================
# LOAD DATA
# ==========================================================

try:

    df = load_dataset()

except Exception as e:

    st.error(
        f"Unable to load dataset.\n\nError: {e}"
    )

    st.stop()


# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="main-title">📊 Amazon Sales Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive analysis of Amazon sales, orders, products and customers'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Dashboard Filters")


# Category filter
categories = sorted(
    df["Category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)


# Fulfilment filter
fulfilments = sorted(
    df["Fulfilment"]
    .dropna()
    .unique()
    .tolist()
)

selected_fulfilments = st.sidebar.multiselect(
    "Select Fulfilment",
    fulfilments,
    default=fulfilments
)


# B2B filter
b2b_options = df["B2B"].dropna().unique().tolist()

selected_b2b = st.sidebar.multiselect(
    "B2B",
    b2b_options,
    default=b2b_options
)


# State filter
states = sorted(
    df["ship-state"]
    .dropna()
    .unique()
    .tolist()
)

selected_states = st.sidebar.multiselect(
    "Select State",
    states,
    default=[]
)


# Date filter
min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df.copy()


# Category
if selected_categories:

    filtered_df = filtered_df[
        filtered_df["Category"].isin(
            selected_categories
        )
    ]


# Fulfilment
if selected_fulfilments:

    filtered_df = filtered_df[
        filtered_df["Fulfilment"].isin(
            selected_fulfilments
        )
    ]


# B2B
if selected_b2b:

    filtered_df = filtered_df[
        filtered_df["B2B"].isin(
            selected_b2b
        )
    ]


# State
if selected_states:

    filtered_df = filtered_df[
        filtered_df["ship-state"].isin(
            selected_states
        )
    ]


# Date
if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        &
        (filtered_df["Date"] <= end_date)
    ]


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_revenue = filtered_df["Amount"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_quantity = filtered_df["Qty"].sum()

average_order_value = (
    filtered_df["Amount"].mean()
    if len(filtered_df) > 0
    else 0
)


# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )


with col2:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with col3:

    st.metric(
        "Quantity Sold",
        f"{total_quantity:,.0f}"
    )


with col4:

    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.2f}"
    )


# ==========================================================
# CATEGORY + ORDER STATUS
# ==========================================================

st.markdown("---")

col1, col2 = st.columns(2)


# Category revenue
with col1:

    st.subheader(" Revenue by Category")

    category_data = (
        filtered_df
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig_category = px.bar(
        category_data,
        x="Category",
        y="Amount",
        title="Revenue by Product Category",
        labels={
            "Amount": "Revenue",
            "Category": "Category"
        }
    )

    fig_category.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# Order status
with col2:
    st.subheader(" Order Status")

    status_data = (
        filtered_df["Status"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Status",
        "Orders"
    ]

    fig_status = px.bar(
        status_data,
        x="Status",
        y="Orders",
        title="Order Status Distribution"
    )

    fig_status.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# ==========================================================
# MONTHLY REVENUE
# ==========================================================

st.markdown("---")

st.subheader(" Monthly Revenue Trend")


monthly_data = (
    filtered_df
    .groupby("Year_Month")["Amount"]
    .sum()
    .reset_index()
)


fig_monthly = px.line(
    monthly_data,
    x="Year_Month",
    y="Amount",
    markers=True,
    title="Monthly Revenue"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ==========================================================
# STATE + FULFILMENT
# ==========================================================

st.markdown("---")

col1, col2 = st.columns(2)


# Top states
with col1:

    st.subheader("🇮🇳 Top 10 States by Revenue")

    state_data = (
        filtered_df
        .groupby("ship-state")["Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    fig_state = px.bar(
        state_data,
        x="Amount",
        y="ship-state",
        orientation="h",
        title="Top 10 States"
    )

    st.plotly_chart(
        fig_state,
        use_container_width=True
    )


# Fulfilment
with col2:

    st.subheader(" Fulfilment Method")

    fulfilment_data = (
        filtered_df["Fulfilment"]
        .value_counts()
        .reset_index()
    )

    fulfilment_data.columns = [
        "Fulfilment",
        "Orders"
    ]

    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Orders",
        title="Orders by Fulfilment"
    )

    st.plotly_chart(
        fig_fulfilment,
        use_container_width=True
    )


# ==========================================================
# SIZE + B2B
# ==========================================================

st.markdown("---")

col1, col2 = st.columns(2)


# Size
with col1:

    st.subheader(" Product Size Distribution")

    size_data = (
        filtered_df["Size"]
        .value_counts()
        .reset_index()
    )

    size_data.columns = [
        "Size",
        "Orders"
    ]

    fig_size = px.bar(
        size_data,
        x="Size",
        y="Orders",
        title="Orders by Size"
    )

    st.plotly_chart(
        fig_size,
        use_container_width=True
    )


# B2B
with col2:

    st.subheader(" B2B vs Non-B2B")

    b2b_data = (
        filtered_df
        .groupby("B2B")["Amount"]
        .sum()
        .reset_index()
    )

    b2b_data["B2B"] = (
        b2b_data["B2B"]
        .astype(str)
    )

    fig_b2b = px.bar(
        b2b_data,
        x="B2B",
        y="Amount",
        title="Revenue: B2B vs Non-B2B"
    )

    st.plotly_chart(
        fig_b2b,
        use_container_width=True
    )


# ==========================================================
# QUANTITY VS REVENUE
# ==========================================================

st.markdown("---")

st.subheader(" Quantity vs Revenue")

fig_scatter = px.scatter(
    filtered_df,
    x="Qty",
    y="Amount",
    hover_data=[
        "Category",
        "Size",
        "Fulfilment"
    ],
    title="Quantity vs Order Revenue"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ==========================================================
# TOP PRODUCTS
# ==========================================================

st.markdown("---")

st.subheader(" Top 10 SKUs by Revenue")


sku_data = (
    filtered_df
    .groupby("SKU")
    .agg(
        Orders=("Order ID", "count"),
        Quantity=("Qty", "sum"),
        Revenue=("Amount", "sum")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
    .reset_index()
)


fig_sku = px.bar(
    sku_data,
    x="Revenue",
    y="SKU",
    orientation="h",
    title="Top 10 Products"
)

st.plotly_chart(
    fig_sku,
    use_container_width=True
)


# ==========================================================
# DATA TABLE
# ==========================================================

st.markdown("---")

st.subheader("Filtered Dataset")

st.write(
    f"Showing {len(filtered_df):,} records"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# ==========================================================
# DOWNLOAD DATA
# ==========================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇ Download Filtered Data",
    data=csv_data,
    file_name="filtered_amazon_sales.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Amazon Sales Analytics Dashboard | "
    "Built with Python, Pandas, NumPy, Streamlit and Plotly"
)