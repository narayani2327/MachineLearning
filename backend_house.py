from fastapi import FastAPI, Request
import joblib
import pandas as pd

from database import (
    fetch_all_data,
    save_to_db
)

app = FastAPI(title="House Price & Sale Prediction API")

# ------------------ Load Models ------------------
price_model = joblib.load("iris_rf_model_house_price.pkl")        # Regression
sold_model = joblib.load("iris_rf_model_house_sold.pkl")          # Classification


# ------------------ PRICE PREDICTION ------------------
@app.post("/predict-price")
async def predict_price(request: Request):
    data: dict = await request.json()

    df = pd.DataFrame([data])

    predicted_price = float(price_model.predict(df)[0])
    prediction = sold_model.predict(df)[0]
    sold_within_week = "Yes" if prediction == 1 else "No"

    save_to_db(data, sold_within_week)

    return {
        "predicted_price": predicted_price,
        "sold_within_week": sold_within_week
    }


# ------------------ FETCH RECORDS ------------------
@app.get("/price-records")
def get_price_records():
    df = fetch_all_data()
    return df.to_dict(orient="records")

