import joblib
import pandas as pd

from feature_eng import create_features


MODEL_PATH = "D:\GenAI\MACHINE LEARNING\AI FRAUD DETECTION\models\xgboost_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_transaction(transaction):

    """
    Predict whether a transaction is potentially fraudulent.
    """

    df = pd.DataFrame([transaction])

    df = create_features(df)

    probability = model.predict_proba(df)[0][1]

    prediction = int(probability >= 0.5)

    return prediction, probability


if __name__ == "__main__":

    sample_transaction = {
        "Time": 50000,
        "Amount": 100
    }

    prediction, probability = predict_transaction(
        sample_transaction
    )

    print("Prediction:", prediction)
    print("Fraud Probability:", probability)