import sys
import os

import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from preprocessing import prepare_data


DATA_PATH = "D:\GenAI\MACHINE LEARNING\AI FRAUD DETECTION\DATA\creditcard.csv"
MODEL_DIR = "D:\GenAI\MACHINE LEARNING\AI FRAUD DETECTION\models"


os.makedirs(MODEL_DIR, exist_ok=True)


# --------------------------------------------------
# Load and prepare data
# --------------------------------------------------

(
    X_train_scaled,
    X_test_scaled,
    y_train,
    y_test,
    scaler,
    X_train,
    X_test
) = prepare_data(DATA_PATH)


# --------------------------------------------------
# Logistic Regression
# --------------------------------------------------

logistic_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

logistic_model.fit(
    X_train_scaled,
    y_train
)


joblib.dump(
    logistic_model,
    "../models/logistic_model.pkl"
)


# --------------------------------------------------
# Random Forest
# --------------------------------------------------

rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(
    X_train,
    y_train
)


joblib.dump(
    rf_model,
    "../models/random_forest_model.pkl"
)


# --------------------------------------------------
# XGBoost
# --------------------------------------------------

fraud_count = y_train.sum()
legitimate_count = len(y_train) - fraud_count

scale_pos_weight = legitimate_count / fraud_count


xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

xgb_model.fit(
    X_train,
    y_train
)


joblib.dump(
    xgb_model,
    "../models/xgboost_model.pkl"
)


# --------------------------------------------------
# Save scaler
# --------------------------------------------------

joblib.dump(
    scaler,
    "../models/scaler.pkl"
)


print("All models trained successfully!")