import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:5000"   # FastAPI base URL

st.title("🏠 House Price & Sale Prediction App")

st.subheader("Enter Property Details")

# ----------- User Inputs -----------
square_footage = st.number_input("Square Footage", min_value=0)
bedrooms = st.number_input("Bedrooms", min_value=0)
bathrooms = st.number_input("Bathrooms", min_value=0)
age = st.number_input("Age of Property (Years)", min_value=0)
garage_spaces = st.number_input("Garage Spaces", min_value=0)
lot_size = st.number_input("Lot Size", min_value=0)
floors = st.number_input("Floors", min_value=0)
neighborhood_rating = st.slider("Neighborhood Rating", 1, 10)
condition = st.slider("Condition", 1, 10)
school_rating = st.slider("School Rating", 1, 10)
has_pool = st.selectbox("Has Pool", [0, 1])
renovated = st.selectbox("Renovated", [0, 1])
location_type_dec = st.selectbox("Location Type", ["Suburban", "Urban", "Downtown","Rural"])
distance_to_center = st.number_input("Distance to City Center (KM)", min_value=0.0)
days_on_market = st.number_input("Days on Market", min_value=0)

# ----------- Payload -----------
payload = {
    "Square_Footage": square_footage,
    "Bedrooms": bedrooms,
    "Bathrooms": bathrooms,
    "Age": age,
    "Garage_Spaces": garage_spaces,
    "Lot_Size": lot_size,
    "Floors": floors,
    "Neighborhood_Rating": neighborhood_rating,
    "Condition": condition,
    "School_Rating": school_rating,
    "Has_Pool": has_pool,
    "Renovated": renovated,
    "Location_Type_Dec": location_type_dec,
    "Distance_To_Center_KM": distance_to_center,
    "Days_On_Market": days_on_market
}

# ----------- Predict Button -----------
if st.button("Predict"):
    try:
        # Price Prediction
        price_response = requests.post(f"{API_URL}/predict-price", json=payload)
        sold_response = requests.post(f"{API_URL}/predict-sold", json=payload)

        if price_response.status_code == 200 and sold_response.status_code == 200:
            price = price_response.json()["predicted_price"]
            sold = sold_response.json()["sold_within_week"]

            st.success(f"💰 Predicted Price: ₹ {price:,.2f}")
            st.info(f"📦 Sold Within a Week: {sold}")

        else:
            st.error("Prediction failed. Check API.")

    except Exception as e:
        st.error(f"API connection error: {e}")

# ----------- Show Stored Records -----------
st.subheader("📊 Prediction History")

col1, col2 = st.columns(2)

with col1:
    if st.button("Show Price Records"):
        res = requests.get(f"{API_URL}/price-records")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            st.dataframe(df)

with col2:
    if st.button("Show Sold Records"):
        res = requests.get(f"{API_URL}/sold-records")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            st.dataframe(df)
