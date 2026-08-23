import streamlit as st
import pandas as pd

from model import (
    predict_score,
    get_risk,
    get_recommendations
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="EduPredict AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #f8fafc 0%,
        #eef2ff 50%,
        #f8fafc 100%
    );
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Hero */
.hero {
    padding: 35px 35px 30px 35px;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        #111827,
        #312e81,
        #4f46e5
    );
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 15px 40px rgba(79,70,229,0.25);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 17px;
    color: #dbeafe;
}

.badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 50px;
    background: rgba(255,255,255,0.15);
    margin-bottom: 15px;
    font-size: 13px;
}

/* Section title */
.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #111827;
    margin-top: 20px;
}

/* Metric cards */
.metric-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 25px rgba(15,23,42,0.06);
    text-align: center;
}

.metric-label {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
}

.metric-value {
    font-size: 31px;
    font-weight: 800;
    color: #111827;
    margin-top: 5px;
}

/* Risk cards */
.low-risk {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
}

.medium-risk {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #b45309;
}

.high-risk {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #b91c1c;
}

.risk-card {
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    font-weight: 800;
    font-size: 24px;
}

/* Recommendation */
.recommendation {
    background: white;
    border-left: 5px solid #4f46e5;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 5px 15px rgba(15,23,42,0.05);
}

/* Info box */
.info-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 52px;
    font-size: 16px;
    font-weight: 700;
    background: linear-gradient(
        90deg,
        #4f46e5,
        #7c3aed
    );
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79,70,229,0.3);
}

/* Input styling */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🎓 EduPredict AI")

    st.caption("Smart Academic Early-Warning System")

    st.divider()

    st.markdown("### 🧠 How it works")

    st.write("""
    **1. Input Data**  
    Enter academic information.

    **2. AI Analysis**  
    Random Forest analyzes the data.

    **3. Risk Detection**  
    Identify academic risk.

    **4. Personalized Advice**  
    Get improvement recommendations.
    """)

    st.divider()

    st.markdown("### 📊 AI Factors")

    st.write("📅 Attendance")
    st.write("📝 Internal Marks")
    st.write("📚 Assignments")
    st.write("⏱️ Study Hours")
    st.write("📈 Previous Score")

    st.divider()

    st.caption("Hackathon Prototype • 2026")


# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero">

<div class="badge">🤖 AI-POWERED EDUCATION</div>

<div class="hero-title">
EduPredict AI
</div>

<div class="hero-subtitle">
Predict student performance • Detect academic risk •
Generate personalized improvement strategies
</div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# INPUT
# =====================================================

st.markdown(
    '<div class="section-title">👤 Student Profile</div>',
    unsafe_allow_html=True
)

st.write("Enter the student's current academic information.")

col1, col2 = st.columns(2)

with col1:

    student_name = st.text_input(
        "Student Name",
        placeholder="e.g. Armaan"
    )

    attendance = st.slider(
        "📅 Attendance",
        0,
        100,
        80,
        help="Overall attendance percentage"
    )

    internal_marks = st.slider(
        "📝 Internal Marks",
        0,
        100,
        70
    )

with col2:

    assignment_marks = st.slider(
        "📚 Assignment Marks",
        0,
        100,
        75
    )

    study_hours = st.number_input(
        "⏱️ Study Hours / Day",
        min_value=0.0,
        max_value=15.0,
        value=3.0,
        step=0.5
    )

    previous_score = st.slider(
        "📈 Previous Semester Score",
        0,
        100,
        70
    )


st.write("")

predict = st.button(
    "🚀 ANALYZE STUDENT PERFORMANCE"
)


# =====================================================
# PREDICTION
# =====================================================

if predict:

    if not student_name:
        student_name = "Student"

    with st.spinner("🤖 AI is analyzing academic patterns..."):

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
        f"Analysis completed for **{student_name}**"
    )


    # =================================================
    # TOP METRICS
    # =================================================

    st.markdown(
        '<div class="section-title">📊 AI Prediction</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-label">
        PREDICTED FINAL SCORE
        </div>

        <div class="metric-value">
        {score}%
        </div>

        </div>
        """, unsafe_allow_html=True)


    with c2:

        if risk == "LOW":

            risk_class = "low-risk"
            risk_icon = "🟢"

        elif risk == "MEDIUM":

            risk_class = "medium-risk"
            risk_icon = "🟡"

        else:

            risk_class = "high-risk"
            risk_icon = "🔴"


        st.markdown(f"""
        <div class="risk-card {risk_class}">

        {risk_icon}<br>

        <span style="font-size:14px;">
        ACADEMIC RISK
        </span>

        <br>

        {risk}

        </div>
        """, unsafe_allow_html=True)


    with c3:

        if score >= 85:

            performance = "Excellent"
            icon = "🏆"

        elif score >= 75:

            performance = "Good"
            icon = "⭐"

        elif score >= 60:

            performance = "Average"
            icon = "📘"

        else:

            performance = "Needs Improvement"
            icon = "⚠️"


        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-label">
        PERFORMANCE
        </div>

        <div class="metric-value">
        {icon} {performance}
        </div>

        </div>
        """, unsafe_allow_html=True)


    # =================================================
    # SCORE PROGRESS
    # =================================================

    st.markdown(
        '<div class="section-title">🎯 Performance Score</div>',
        unsafe_allow_html=True
    )

    st.progress(
        min(max(int(score), 0), 100)
    )

    st.caption(
        f"AI predicted performance: **{score}% / 100%**"
    )


    # =================================================
    # RISK ANALYSIS
    # =================================================

    st.markdown(
        '<div class="section-title">🔍 Risk Analysis</div>',
        unsafe_allow_html=True
    )

    risk_factors = []


    if attendance < 75:

        risk_factors.append(
            f"📅 Attendance is below 75% ({attendance}%)."
        )

    elif attendance < 85:

        risk_factors.append(
            f"📅 Attendance could be improved ({attendance}%)."
        )


    if internal_marks < 60:

        risk_factors.append(
            f"📝 Internal marks are low ({internal_marks})."
        )


    if assignment_marks < 60:

        risk_factors.append(
            f"📚 Assignment performance needs attention ({assignment_marks})."
        )


    if study_hours < 2:

        risk_factors.append(
            f"⏱️ Study time is low ({study_hours} hrs/day)."
        )


    if previous_score < 60:

        risk_factors.append(
            f"📈 Previous score indicates an improvement area ({previous_score}%)."
        )


    if not risk_factors:

        st.success(
            "✨ No major risk factors detected!"
        )

    else:

        for factor in risk_factors:

            st.warning(factor)


    # =================================================
    # PERSONALIZED RECOMMENDATIONS
    # =================================================

    st.markdown(
        '<div class="section-title">🤖 AI Recommendations</div>',
        unsafe_allow_html=True
    )

    for recommendation in recommendations:

        st.markdown(
            f"""
            <div class="recommendation">
            💡 {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )


    # =================================================
    # ACADEMIC CHART
    # =================================================

    st.markdown(
        '<div class="section-title">📈 Academic Analytics</div>',
        unsafe_allow_html=True
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
        "Internal",
        "Assignments",
        "Previous Score",
        "AI Prediction"

    ])

    st.bar_chart(chart_data)


    # =================================================
    # WHAT-IF ANALYSIS
    # =================================================

    st.markdown(
        '<div class="section-title">🚀 What-If Simulator</div>',
        unsafe_allow_html=True
    )

    st.write(
        "See how improving attendance could affect the AI prediction."
    )

    improved_attendance = st.slider(
        "Simulated Attendance",
        min_value=attendance,
        max_value=100,
        value=min(attendance + 10, 100)
    )


    simulated_score = predict_score(

        improved_attendance,

        internal_marks,

        assignment_marks,

        study_hours,

        previous_score

    )


    difference = round(
        simulated_score - score,
        1
    )


    w1, w2, w3 = st.columns(3)


    with w1:

        st.metric(
            "Current Score",
            f"{score}%"
        )


    with w2:

        st.metric(
            "Simulated Score",
            f"{simulated_score}%"
        )


    with w3:

        st.metric(
            "Potential Change",
            f"{difference:+.1f}%"
        )


    # =================================================
    # ACTION PLAN
    # =================================================

    st.markdown(
        '<div class="section-title">🎯 Suggested Action Plan</div>',
        unsafe_allow_html=True
    )

    if risk == "HIGH":

        st.error("""
        **Priority:** Immediate academic intervention

        • Increase study consistency  
        • Improve attendance  
        • Meet faculty/mentor  
        • Focus on weak subjects
        """)

    elif risk == "MEDIUM":

        st.warning("""
        **Priority:** Prevent performance decline

        • Maintain regular revision  
        • Improve assignments  
        • Increase study hours  
        • Track weekly progress
        """)

    else:

        st.success("""
        **Priority:** Maintain and optimize

        • Continue current routine  
        • Challenge yourself with advanced topics  
        • Maintain attendance  
        • Keep consistent revision
        """)


# =====================================================
# EMPTY STATE
# =====================================================

else:

    st.info(
        "👆 Enter student information above and click "
        "**ANALYZE STUDENT PERFORMANCE** to start."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    "<center>🎓 <b>EduPredict AI</b> • "
    "AI Student Performance Early-Warning System • Hackathon 2026</center>",
    unsafe_allow_html=True
)
