# tests/test_model_load.py

import joblib
import pandas as pd


def main():
    model = joblib.load("app/ml/artifacts/travel_style_classifier.pkl")
    feature_columns = joblib.load("app/ml/artifacts/feature_columns.pkl")

    print("Model loaded successfully")
    print("Feature columns loaded successfully")
    print("Columns:")
    print(feature_columns)

    sample = {
        "avg_daily_cost_usd": 80,
        "avg_hotel_price_usd": 60,
        "safety_score": 8,
        "temperature": 24,
        "adventure_score": 0.7,
        "budget_score": 0.5,
    }

    df = pd.DataFrame([sample])

    for column in feature_columns:
        if column not in df.columns:
            df[column] = 0

    df = df[feature_columns]

    prediction = model.predict(df)[0]

    print("Prediction:")
    print(prediction)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(df)[0]
        result = dict(zip(model.classes_, probabilities))
        print("Probabilities:")
        print(result)


if __name__ == "__main__":
    main()