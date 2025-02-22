import streamlit as st
import numpy as np

# Manually assigned weights for CAD risk factors
weights = np.array([0.03, 0.02, 0.025, 0.02, 0.015, 0.02, -0.02, 0.012, 0.014, 0.016, -0.018, 0.05, 0.04])

st.title("🩺 CAD Risk Estimator - 10-Year Prediction")

# User Inputs
age = st.number_input("Age", min_value=20, max_value=100, value=45)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
sbp = st.number_input("Systolic BP", min_value=90, max_value=200, value=120)
dbp = st.number_input("Diastolic BP", min_value=60, max_value=140, value=80)
total_chol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=300, value=180)
ldl_chol = st.number_input("LDL Cholesterol (mg/dL)", min_value=50, max_value=200, value=100)
hdl_chol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=50)
triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=500, value=150)
heart_rate = st.number_input("Heart Rate (BPM)", min_value=40, max_value=150, value=75)
resting_hr = st.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=100, value=65)
hrv = st.number_input("HRV (Heart Rate Variability)", min_value=10, max_value=100, value=50)
smoking = st.checkbox("Smoking (Check if Yes)")
diabetes = st.checkbox("Diabetes (Check if Yes)")

# Convert checkboxes to numeric values
smoking_val = 1 if smoking else 0
diabetes_val = 1 if diabetes else 0

# Compute CAD Risk Score
inputs = np.array([age, bmi, sbp, dbp, total_chol, ldl_chol, hdl_chol, triglycerides, heart_rate, resting_hr, hrv, smoking_val, diabetes_val])
cad_risk_score = np.dot(weights, inputs)

# Convert risk score into categories
if cad_risk_score < 0.3:
    risk_category = "🟢 Low CAD Risk"
elif 0.3 <= cad_risk_score < 0.7:
    risk_category = "🟡 Moderate CAD Risk"
else:
    risk_category = "🔴 High CAD Risk"

# Display results
st.subheader(f"🔮 Predicted 10-Year CAD Risk: {risk_category}")
st.write(f"📊 Estimated Risk Score: **{cad_risk_score * 100:.2f}%**")
