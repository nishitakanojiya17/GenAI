import pandas as pd
import numpy as np


def create_features(df):
    """
    Create additional features from transaction data.
    """

    df = df.copy()

    # Convert Time from seconds into hour of day
    df["Hour"] = (df["Time"] // 3600) % 24

    # Log transformation of transaction amount
    df["Amount_Log"] = np.log1p(df["Amount"])

    return df