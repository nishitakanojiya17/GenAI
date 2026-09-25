import joblib
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score
)

from preprocessing import prepare_data


DATA_PATH = "D:\GenAI\MACHINE LEARNING\AI FRAUD DETECTION\DATA\creditcard.csv"


(
    X_train_scaled,
    X_test_scaled,
    y_train,
    y_test,
    scaler,
    X_train,
    X_test
) = prepare_data(DATA_PATH)


models = {
    "Logistic Regression": (
        joblib.load("../models/logistic_model.pkl"),
        X_test_scaled
    ),

    "Random Forest": (
        joblib.load("../models/random_forest_model.pkl"),
        X_test
    ),

    "XGBoost": (
        joblib.load("../models/xgboost_model.pkl"),
        X_test
    )
}


results = []


for name, (model, X_data) in models.items():

    y_pred = model.predict(X_data)

    y_probability = model.predict_proba(X_data)[:, 1]

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    precision = report["1"]["precision"]
    recall = report["1"]["recall"]
    f1 = report["1"]["f1-score"]

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )

    pr_auc = average_precision_score(
        y_test,
        y_probability
    )

    results.append({
        "Model": name,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc
    })


results_df = pd.DataFrame(results)

print("\nModel Comparison")
print("=" * 70)

print(results_df.to_string(index=False))


results_df.to_csv(
    "../outputs/reports/model_comparison.csv",
    index=False
)