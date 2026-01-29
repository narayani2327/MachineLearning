import streamlit as st
import pandas as pd
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.title("Loan Prediction App")

# --- User Input Form ---
st.subheader("Enter Applicant Details")

gender = st.selectbox("Gender:", ["Male", "Female"])
married = st.selectbox("Married:", ["Yes", "No"])
dependents = st.selectbox("Dependents:", ["0", "1", "2", "3+"])
education = st.selectbox("Education:", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed:", ["Yes", "No"])
applicant_income = st.number_input("Applicant Income:", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income:", min_value=0)
loan_amount = st.number_input("Loan Amount (in thousands):", min_value=0)
loan_term = st.number_input("Loan Amount Term (in months):", min_value=0)
credit_history = st.selectbox("Credit History:", [0, 1])
property_area = st.selectbox("Property Area:", ["Urban", "Semiurban", "Rural"])

# Payload to send to backend
payload = {
    "Gender": gender,
    "Married": married,
    "Dependents": dependents,
    "Education": education,
    "Self_Employed": self_employed,
    "ApplicantIncome": applicant_income,
    "CoapplicantIncome": coapplicant_income,
    "LoanAmount": loan_amount,
    "Loan_Amount_Term": loan_term,
    "Credit_History": credit_history,
    "Property_Area": property_area
}

# --- Predict on submit ---
if st.button("Predict Loan Status"):
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)

        if response.status_code == 200:
            result = response.json()["prediction"]
            st.subheader("Prediction Result")
            st.success(f"Loan Status: {result}")
        else:
            st.error("Prediction failed")

    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

# --- Display all SQLite data ---
st.subheader("All Submitted Data")

try:
    records_response = requests.get(f"{API_URL}/records")
    if records_response.status_code == 200:
        all_data = pd.DataFrame(records_response.json())

        if not all_data.empty:
            st.dataframe(all_data)
            st.bar_chart(all_data["Prediction"].value_counts())
        else:
            st.info("No records found.")
    else:
        st.error("Failed to fetch records")

except Exception as e:
    st.error(f"Error fetching records: {e}")
