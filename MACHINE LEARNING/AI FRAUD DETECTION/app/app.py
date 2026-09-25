import streamlit as st
import joblib
import pandas as pd

from pathlib import Path


st.set_page_config(
    page_title="AI Fraud Detection",
    page_icon="🔐",
    layout="wide"
)


st.title(" AI-Powered Fraud Detection System")

st.write(
    "Machine Learning based financial transaction fraud detection."
)


# --------------------------------------------------
# Load model
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "xgboost_model.pkl"

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# User Input
# --------------------------------------------------

st.subheader("Transaction Details")

amount = st.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=100.0
)

time = st.number_input(
    "Transaction Time",
    min_value=0.0,
    value=50000.0
)


if st.button("Analyze Transaction"):

    st.info(
        "The complete prediction form will use the trained model's required features."
    )

    st.write("Amount:", amount)
    st.write("Time:", time)