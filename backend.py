from fastapi import FastAPI, Request
import joblib
import pandas as pd

from database import save_to_db, fetch_all_data

app = FastAPI(title="Loan Prediction Backend API")

# Load model
model = joblib.load("iris_rf_model.pkl")


# ----- Prediction API -----
@app.post("/predict")
async def predict_loan(request: Request):
    data: dict = await request.json()

    # Convert dict to DataFrame
    df = pd.DataFrame([data])

    # Predict
    prediction = model.predict(df)[0]
    result = "Approved" if prediction == 1 else "Not Approved"

    # Save to SQLite
    save_to_db(data, result)

    return {
        "prediction": result
    }


# ----- Fetch all records API -----
@app.get("/records")
def get_all_records():
    df = fetch_all_data()
    return df.to_dict(orient="records")
