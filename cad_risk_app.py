import streamlit as st
import numpy as np

def calculate_cad_risk(age, bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv, smoking, diabetes):
    """Calculates the estimated CAD risk score based on manual weightage and predicts 10-year risk."""
    
    weights = np.array([0.03, 0.02, 0.025, 0.02, 0.015, 0.02, -0.02, 0.012, 0.014, 0.016, -0.018, 0.05, 0.04])
    features = np.array([age, bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv, smoking, diabetes])
    
    risk_score = np.dot(features, weights) * 10  # Scale up to percentage
    
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
    age = st.number_input("Current Age", min_value=20, max_value=79, step=1, help="Age must be between 20-79")
    sex = st.radio("Sex", ["Male", "Female"], index=None, help="Select your sex")
    race = st.radio("Race", ["White", "African American", "Other"], index=None, help="Select your race")
    bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, step=0.1, help="Value must be between 15-50")
    sbp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=90, max_value=200, step=1, help="Value must be between 90-200")
    dbp = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=60, max_value=130, step=1, help="Value must be between 60-130")
    
with col2:
    total_cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=130, max_value=320, step=1, help="Value must be between 130-320")
    ldl = st.number_input("LDL Cholesterol (mg/dL)", min_value=30, max_value=300, step=1, help="Value must be between 30-300")
    hdl = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, step=1, help="Value must be between 20-100")
    triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=400, step=1, help="Value must be between 50-400")
    
with col3:
    heart_rate = st.number_input("Heart Rate (BPM)", min_value=40, max_value=120, step=1, help="Value must be between 40-120")
    resting_hr = st.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=100, step=1, help="Value must be between 40-100")
    hrv = st.number_input("HRV (Heart Rate Variability)", min_value=10, max_value=100, step=1, help="Value must be between 10-100")
    smoking = st.radio("Smoking", ["Yes", "No"], index=None, help="Select if you are a smoker")
    diabetes = st.radio("Diabetes", ["Yes", "No"], index=None, help="Select if you have diabetes")

# Convert radio buttons to 1/0 for calculations
smoking = 1 if smoking == "Yes" else 0
diabetes = 1 if diabetes == "Yes" else 0

# Buttons
def reset():
    st.experimental_rerun()

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Calculate Risk"):
        if None in [sex, race]:
            st.warning("Please select Sex and Race.")
        else:
            risk_label, risk_icon, risk_score = calculate_cad_risk(age, bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv, smoking, diabetes)
            st.markdown(f"### 🎯 Predicted 10-Year CAD Risk: {risk_icon} {risk_label}")
            st.markdown(f"📊 Estimated 10-Year Risk Score: **{risk_score:.2f}%**")
    
with col2:
    if st.button("Reset"):
        reset()
