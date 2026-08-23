import streamlit as st
import pandas as pd

from model import (
    predict_score,
    get_risk,
    get_recommendations
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🎓 AI Student Performance Predictor")

st.write(
    "Predict academic performance, identify risk, "
    "and receive personalized recommendations."
)

st.divider()


# ==========================================
# STUDENT INPUT
# ==========================================

st.header("📝 Student Information")

col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Student Name"
    )

    attendance = st.slider(
        "Attendance (%)",
        0,
        100,
        80
    )

    internal_marks = st.slider(
        "Internal Marks",
        0,
        100,
        70
    )

    assignment_marks = st.slider(
        "Assignment Marks",
        0,
        100,
        75
    )


with col2:

    study_hours = st.number_input(
        "Study Hours Per Day",
        0.0,
        15.0,
        3.0,
        0.5
    )

    previous_score = st.slider(
        "Previous Semester Score",
        0,
        100,
        70
    )


# ==========================================
# PREDICT BUTTON
# ==========================================

st.divider()

predict = st.button(
    "🔮 PREDICT PERFORMANCE",
    use_container_width=True
)


# ==========================================
# RESULT
# ==========================================

if predict:

    if name == "":
        name = "Student"

    # Call Person 1's ML model
    score = predict_score(
        attendance,
        internal_marks,
        assignment_marks,
        study_hours,
        previous_score
    )

    risk = get_risk(score)

    recommendations = get_recommendations(
        attendance,
        internal_marks,
        assignment_marks,
        study_hours,
        previous_score
    )


    st.success(
        f"Prediction generated for {name}!"
    )


    # ======================================
    # RESULT CARDS
    # ======================================

    st.header("📊 Prediction Result")

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Predicted Score",
            f"{score}%"
        )


    with col2:

        if risk == "LOW":

            st.metric(
                "Risk Level",
                "🟢 LOW"
            )

        elif risk == "MEDIUM":

            st.metric(
                "Risk Level",
                "🟡 MEDIUM"
            )

        else:

            st.metric(
                "Risk Level",
                "🔴 HIGH"
            )


    with col3:

        if score >= 85:
            performance = "Excellent"

        elif score >= 75:
            performance = "Good"

        elif score >= 60:
            performance = "Average"

        else:
            performance = "Needs Improvement"


        st.metric(
            "Performance",
            performance
        )


    # ======================================
    # PERFORMANCE BAR
    # ======================================

    st.subheader("📈 Performance")

    st.progress(
        int(max(0, min(score, 100)))
    )


    # ======================================
    # RISK ANALYSIS
    # ======================================

    st.subheader("🔍 Risk Analysis")

    risk_factors = []


    if attendance < 75:

        risk_factors.append(
            f"Attendance is low ({attendance}%)."
        )


    if internal_marks < 60:

        risk_factors.append(
            f"Internal marks are low ({internal_marks})."
        )


    if assignment_marks < 60:

        risk_factors.append(
            f"Assignment marks are low ({assignment_marks})."
        )


    if study_hours < 2:

        risk_factors.append(
            f"Study time is low ({study_hours} hours/day)."
        )


    if previous_score < 60:

        risk_factors.append(
            f"Previous score is low ({previous_score}%)."
        )


    if len(risk_factors) == 0:

        st.success(
            "No major academic risk factors detected."
        )

    else:

        for factor in risk_factors:

            st.warning(factor)


    # ======================================
    # RECOMMENDATIONS
    # ======================================

    st.subheader(
        "🤖 Personalized Recommendations"
    )


    for recommendation in recommendations:

        st.write(
            "✅ " + recommendation
        )


    # ======================================
    # CHART
    # ======================================

    st.subheader(
        "📊 Academic Analysis"
    )


    chart_data = pd.DataFrame({

        "Score": [

            attendance,
            internal_marks,
            assignment_marks,
            previous_score,
            score

        ]

    }, index=[

        "Attendance",
        "Internal Marks",
        "Assignment Marks",
        "Previous Score",
        "Predicted Score"

    ])


    st.bar_chart(
        chart_data
    )


    # ======================================
    # WHAT-IF ANALYSIS
    # ======================================

    st.subheader(
        "🚀 What-If Analysis"
    )


    improved_attendance = min(
        100,
        attendance + 10
    )


    improved_score = predict_score(

        improved_attendance,

        internal_marks,

        assignment_marks,

        study_hours,

        previous_score

    )


    improvement = round(
        improved_score - score,
        1
    )


    st.write(
        f"If attendance improves from "
        f"**{attendance}% → {improved_attendance}%**, "
        f"predicted score becomes approximately "
        f"**{improved_score}%**."
    )


    if improvement > 0:

        st.success(
            f"📈 Potential improvement: +{improvement}%"
        )

    else:

        st.info(
            "Try improving other academic factors as well."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Student Performance Predictor | Hackathon Prototype"
)
