import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("CSV File Viewer")

# Read CSV
df = pd.read_csv("Loan dataset_classification.csv")

# Display first 10 rows
st.subheader("CSV Data Preview")
st.dataframe(df.head(10))

# Streamlit inputs
st.subheader("User Input Form")

name = st.text_input("Enter your name:")
age = st.slider("Select your age:", 0, 100)
drop = st.selectbox("Select your favorite color:", ["Red", "Green", "Blue"])
check = st.checkbox("I agree to the terms and conditions")
radio = st.radio("Select your gender:", ["Male", "Female", "Other"])
number = st.number_input("Enter your lucky number:", min_value=0, max_value=100)
address = st.text_area("Enter your address:")
# Choose 2 numeric columns to plot
col1 = st.selectbox("Select column for X-axis:", df.columns)
col2 = st.selectbox("Select column for Y-axis:", df.columns)

# Make sure columns are numeric for plotting
if pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2]):
    st.line_chart(df[[col1, col2]])
else:
    st.warning("Please select numeric columns for plotting!")
# Charts
linechart = st.line_chart({"data": [1, 3, 2, 4, 3, 5]})
barchart = st.bar_chart({"data": [5, 3, 4, 2, 1, 0]})

# Pie chart
st.subheader("Pie Chart Example")
fig, ax = plt.subplots()
ax.pie([10, 20, 30], labels=["A", "B", "C"], autopct='%1.1f%%')
st.pyplot(fig)

# Display all inputs on button click
if st.button("Submit"):
    st.subheader("Entered Data")
    st.write(f"**Name:** {name}")
    st.write(f"**Age:** {age}")
    st.write(f"**Favorite Color:** {drop}")
    st.write(f"**Agree to Terms:** {check}")
    st.write(f"**Gender:** {radio}")
    st.write(f"**Lucky Number:** {number}")
    st.write(f"**Address:** {address}")
    
    st.subheader("Charts")
    st.line_chart({"Line Data": df.columns})
    st.bar_chart({"Bar Data": [5, 3, 4, 2, 1, 0]})
    st.pyplot(fig)
    
    st.subheader("CSV Data Preview")
    st.dataframe(df.head(10))
