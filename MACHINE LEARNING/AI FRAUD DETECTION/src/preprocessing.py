import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from feature_eng import create_features


def load_data(path):
    """
    Load fraud detection dataset.
    """

    df = pd.read_csv("D:\GenAI\MACHINE LEARNING\AI FRAUD DETECTION\DATA\creditcard.csv")

    return df


def prepare_data(path):
    """
    Load dataset, create features and split data.
    """

    df = load_data("D:\GenAI\MACHINE LEARNING\AI FRAUD DETECTION\DATA\creditcard.csv")

    # Feature engineering
    df = create_features(df)

    # Separate target
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42
    )

    # Scaling
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        scaler,
        X_train,
        X_test
    )