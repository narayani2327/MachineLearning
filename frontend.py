import streamlit as st
import pandas as pd
import pickle
import joblib

# Load the trained model
model = joblib.load("iris_rf_model.pkl")

st.title("Loan Prediction App")

# User input form
st.subheader("Enter Applicant Details")

loan_id = st.text_input("Loan ID:", "LP999999")
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

# Create DataFrame from user input
new_data = pd.DataFrame([{
    'Loan_ID': loan_id,
    'Gender': gender,
    'Married': married,
    'Dependents': dependents,
    'Education': education,
    'Self_Employed': self_employed,
    'ApplicantIncome': applicant_income,
    'CoapplicantIncome': coapplicant_income,
    'LoanAmount': loan_amount,
    'Loan_Amount_Term': loan_term,
    'Credit_History': credit_history,
    'Property_Area': property_area
}])

# Predict on submit
if st.button("Predict Loan Status"):
    # Preprocess new_data if needed (encoding categorical variables etc.)
    # Example: model.predict(new_data_transformed)
    
    # Call the model
    prediction = model.predict(new_data)  # assuming model handles preprocessing
    prediction_proba = model.predict_proba(new_data) if hasattr(model, "predict_proba") else None

    st.subheader("Prediction Result")
    st.write(f"**Loan Status Prediction:** {'Approved' if prediction[0]==1 else 'Not Approved'}")
    
    if prediction_proba is not None:
        st.write(f"**Probability:** {prediction_proba[0]}")
