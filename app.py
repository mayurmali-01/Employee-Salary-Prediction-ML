import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Employee Salary Prediction",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# Load Model & Scaler
# -----------------------------
model = joblib.load("salary_prediction_model.pkl")
scaler = joblib.load("minmax_scaler.pkl")

# Feature names used during training
feature_columns = scaler.feature_names_in_

# -----------------------------
# Title
# -----------------------------
st.title("💰 Employee Salary Prediction System")
st.markdown(
    """
Predict an employee's expected salary using a Machine Learning model trained on
job characteristics and experience.
"""
)

st.divider()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Project Information")

st.sidebar.info(
"""
**Model Used**

✅ XGBoost Regressor

**Features**

- Job Type
- Degree
- Major
- Industry
- Years of Experience
- Distance from Metropolis

Developed using:

- Python
- Scikit-Learn
- XGBoost
- Streamlit
"""
)

# -----------------------------
# Input Form
# -----------------------------
st.subheader("Enter Employee Details")

col1, col2 = st.columns(2)

with col1:

    jobType = st.selectbox(
        "Job Type",
        [
            "CEO",
            "CFO",
            "CTO",
            "VICE_PRESIDENT",
            "MANAGER",
            "JUNIOR",
            "SENIOR",
            "JANITOR"
        ]
    )

    degree = st.selectbox(
        "Degree",
        [
            "HIGH_SCHOOL",
            "BACHELORS",
            "MASTERS",
            "DOCTORAL",
            "NONE"
        ]
    )

    major = st.selectbox(
        "Major",
        [
            "BUSINESS",
            "ENGINEERING",
            "MATH",
            "PHYSICS",
            "CHEMISTRY",
            "COMPSCI",
            "LITERATURE",
            "BIOLOGY",
            "NONE"
        ]
    )

with col2:

    industry = st.selectbox(
        "Industry",
        [
            "FINANCE",
            "OIL",
            "SERVICE",
            "WEB",
            "HEALTH",
            "AUTO",
            "EDUCATION"
        ]
    )

    yearsExperience = st.slider(
        "Years of Experience",
        0,
        30,
        5
    )

    milesFromMetropolis = st.slider(
        "Miles From Metropolis",
        0,
        100,
        20
    )

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Salary", use_container_width=True):

    input_df = pd.DataFrame({
        "jobType":[jobType],
        "degree":[degree],
        "major":[major],
        "industry":[industry],
        "yearsExperience":[yearsExperience],
        "milesFromMetropolis":[milesFromMetropolis]
    })

    # One-Hot Encoding
    input_df = pd.get_dummies(
        input_df,
        columns=["jobType","degree","major","industry"],
        drop_first=True,
        dtype=int
    )

    # Match Training Columns
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    # Scaling
    input_scaled = scaler.transform(input_df)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    st.success(f"### 💵 Predicted Salary : ${prediction:,.2f}")

    st.metric(
        label="Estimated Salary",
        value=f"${prediction:,.2f}"
    )

st.divider()

st.markdown(
"""
### About

This web application predicts employee salary based on:

- Job Type
- Education
- Major
- Industry
- Years of Experience
- Distance from Metropolis

The prediction is generated using a tuned **XGBoost Regression** model.
"""
)