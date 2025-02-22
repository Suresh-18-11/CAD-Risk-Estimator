import streamlit as st
import numpy as np

def calculate_cad_risk(age, bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv, smoking, diabetes):
    """Calculates the estimated CAD risk score based on medical weightage and predicts the 10-year risk."""
    
    # Adjusted weightage for 10-year risk estimation based on medical studies
    weights = np.array([0.08, 0.04, 0.05, 0.04, 0.035, 0.04, -0.03, 0.03, 0.025, 0.028, -0.03, 0.08, 0.07])
    features = np.array([age, bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv, smoking, diabetes])
    
    risk_score = np.dot(features, weights) / 1.5  # Normalized for 10-year estimation
    
    if risk_score < 10:
        return "Low CAD Risk", "🟢", risk_score
    elif 10 <= risk_score < 20:
        return "Moderate CAD Risk", "🟡", risk_score
    else:
        return "High CAD Risk", "🔴", risk_score

# Streamlit UI
st.set_page_config(page_title="CAD Risk Estimator", layout="wide")
st.title("🩺 CAD Risk Estimator - 10-Year Prediction")

# UI Design Layout
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    age = st.number_input("Current Age *", value="",  min_value=30, max_value=70, step=1, format="%d")
    st.caption("Age must be between 30 - 70")
    sex = st.radio("Sex", ["Male", "Female"], index=None)
    race = st.radio("Race", ["White", "African American", "Other"], index=None)
    bmi = st.number_input("BMI *")
    st.caption("BMI must be between 18.5 - 40 (Based on health guidelines)")
    sbp = st.number_input("Systolic Blood Pressure (mmHg) *")
    st.caption("Value must be between 90 - 200")
    dbp = st.number_input("Diastolic Blood Pressure (mmHg) *")
    st.caption("Value must be between 60 - 130")
    
with col2:
    total_cholesterol = st.number_input("Total Cholesterol (mg/dL) *")
    st.caption("Value must be between 130 - 320")
    ldl = st.number_input("LDL Cholesterol (mg/dL) *")
    st.caption("Value must be between 30 - 300")
    hdl = st.number_input("HDL Cholesterol (mg/dL) *")
    st.caption("Value must be between 20 - 100")
    triglycerides = st.number_input("Triglycerides (mg/dL) *")
    st.caption("Value must be between 50 - 400")
    
with col3:
    heart_rate = st.number_input("Heart Rate (BPM) *")
    st.caption("Value must be between 40 - 120")
    resting_hr = st.number_input("Resting Heart Rate (BPM) *")
    st.caption("Value must be between 40 - 100")
    hrv = st.number_input("HRV (Heart Rate Variability) *")
    st.caption("Value must be between 10 - 100")
    smoking = st.radio("Smoking", ["Yes", "No"], index=None)
    diabetes = st.radio("Diabetes", ["Yes", "No"], index=None)

# Convert radio buttons to 1/0 for calculations
smoking = 1 if smoking == "Yes" else 0
diabetes = 1 if diabetes == "Yes" else 0

# Calculate Risk Button
if st.button("Calculate Risk"):
    if not all([age, bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv]) or sex is None or race is None:
        st.warning("Please fill in all fields before calculating risk.")
    else:
                                    risk_label, risk_icon, risk_score = calculate_cad_risk(age, bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv, smoking, diabetes)
    st.markdown(f"### 🎯 Predicted 10-Year CAD Risk: {risk_icon} {risk_label}")
    st.markdown(f"📊 Estimated 10-Year Risk Score: **{risk_score:.2f}%**")
