import streamlit as st
import pandas as pd
import joblib
from backend import save_to_db, fetch_all_data

# Load model
model = joblib.load("iris_rf_model.pkl")  # Replace with your actual model

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

new_data = pd.DataFrame([{
    'Loan_ID': 'LP999999',
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

# --- Predict on submit ---
if st.button("Predict Loan Status"):
    # Call model
    prediction = model.predict(new_data)
    print(prediction)
    prediction_proba = model.predict_proba(new_data) if hasattr(model, "predict_proba") else None

    result = 'Approved' if prediction[0] == 1 else 'Not Approved'
    
    st.subheader("Prediction Result")
    st.write(f"**Loan Status Prediction:** {result}")
    
    if prediction_proba is not None:
        st.write(f"**Probability:** {prediction_proba[0]}")

    new_data = new_data.drop("Loan_ID", axis=1)

    # Save to SQLite
    save_to_db(new_data.iloc[0].to_dict(), result)
    st.success("Data saved to database successfully!")

# --- Display all SQLite data ---
st.subheader("All Submitted Data")
all_data = fetch_all_data()
st.dataframe(all_data)
st.bar_chart(all_data['Prediction'].value_counts())
