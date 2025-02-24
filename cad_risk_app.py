import streamlit as st
import numpy as np
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    SEABORN_AVAILABLE = True
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    MATPLOTLIB_AVAILABLE = False
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
import seaborn as sns

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
    age = st.number_input("Current Age *", value=30, min_value=30, max_value=70, step=1, format="%d")
    sex = st.radio("Sex", ["Male", "Female"], index=None)
    race = st.radio("Race", ["White", "African American", "Other"], index=None)
    bmi = st.number_input("BMI *", value=22.5)
    sbp = st.number_input("Systolic Blood Pressure (mmHg) *", value=110)
    dbp = st.number_input("Diastolic Blood Pressure (mmHg) *", value=75)
    
with col2:
    total_cholesterol = st.number_input("Total Cholesterol (mg/dL) *", value=170)
    ldl = st.number_input("LDL Cholesterol (mg/dL) *", value=90)
    hdl = st.number_input("HDL Cholesterol (mg/dL) *", value=60)
    triglycerides = st.number_input("Triglycerides (mg/dL) *", value=100)
    
with col3:
    heart_rate = st.number_input("Heart Rate (BPM) *", value=65)
    resting_hr = st.number_input("Resting Heart Rate (BPM) *", value=55)
    hrv = st.number_input("HRV (Heart Rate Variability) *", value=75)
    smoking = st.radio("Smoking", ["Yes", "No"], index=1)
    diabetes = st.radio("Diabetes", ["Yes", "No"], index=1)

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
        
        # Visualization: Risk Distribution
        # Comparison Graph (User values vs. Ideal values)
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        metrics = ['BMI', 'SBP', 'DBP', 'Total Chol.', 'LDL', 'HDL', 'Trigly.', 'HR', 'RHR', 'HRV']
        user_values = [bmi, sbp, dbp, total_cholesterol, ldl, hdl, triglycerides, heart_rate, resting_hr, hrv]
        ideal_values = [22, 120, 80, 180, 100, 55, 150, 70, 60, 75]
        
        x = np.arange(len(metrics))
        ax2.bar(x - 0.2, user_values, width=0.4, label='Your Values', color='blue')
        ax2.bar(x + 0.2, ideal_values, width=0.4, label='Ideal Values', color='green', alpha=0.6)
        
        ax2.set_xticks(x)
        ax2.set_xticklabels(metrics, rotation=45)
        ax2.set_ylabel("Measurement Values")
        ax2.set_title("User vs. Ideal Health Standards")
        ax2.legend()
        st.pyplot(fig2)
        fig, ax = plt.subplots()
        categories = ['Low Risk', 'Moderate Risk', 'High Risk']
        values = [10, 20, 30]  # Example benchmark values
        user_value = [risk_score]
        
        ax.bar(categories, values, color=['green', 'yellow', 'red'], alpha=0.5, label="Benchmark")
        ax.bar(['User Score'], user_value, color='blue', label="Your Score")
        ax.set_ylabel("Risk Score")
        ax.set_title("Risk Score Distribution")
        ax.legend()
        st.pyplot(fig)
        
        # Health Suggestions Based on Risk
        if risk_score < 10:
            st.success("✅ Your risk is low! Maintain a healthy lifestyle with regular exercise and a balanced diet.")
        elif 10 <= risk_score < 20:
            st.warning("⚠️ Your risk is moderate. Consider reducing cholesterol intake and exercising more.")
        else:
            st.error("🚨 Your risk is high! Consult a doctor for medical evaluation and lifestyle changes.")
