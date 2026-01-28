import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

model = joblib.load("iris_rf_model.pkl")


@app.post("/predict")
def predict(data:dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return {"predicted_output":int(prediction[0])}


# Input:

# {
#     "Married": "No",
#     "Education": "Not Graduate",
#     "Self_Employed": "No",
#     "ApplicantIncome": 6500,
#     "CoapplicantIncome": 1100,
#     "LoanAmount": 2100,
#     "Loan_Amount_Term": 360,
#     "Credit_History": 3,
#     "Property_Area": "Rural"
# }
