
import streamlit as st
import pandas as pd
import time
import math

from model import (
    predict_score,
    get_risk,
    get_recommendations
)

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="AURA AI",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DARK UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 20%, #06251e 0%, transparent 25%),
        radial-gradient(circle at 90% 10%, #101d3d 0%, transparent 25%),
        radial-gradient(circle at 50% 100%, #160b28 0%, transparent 30%),
        #030507;
    color: #f5f7fa;
}

header, footer, #MainMenu {
    visibility: hidden;
}

/* Animated background */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;

    background-image:
        linear-gradient(rgba(0,255,190,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,190,.025) 1px, transparent 1px);

    background-size: 60px 60px;

    animation: movegrid 15s linear infinite;
}

@keyframes movegrid {
    from { transform: translateY(0); }
    to { transform: translateY(60px); }
}

/* Main title */

.main-title {
    font-size: 52px;
    font-weight: 900;
    letter-spacing: 5px;
    color: white;
    text-align: center;
    margin-top: 10px;
}

.main-title span {
    color: #00ffc3;
    text-shadow: 0 0 25px #00ffc3;
}

.subtitle {
    text-align: center;
    color: #718096;
    letter-spacing: 3px;
    margin-bottom: 30px;
}

/* Cards */

.card {
    background: rgba(9,14,18,.85);
    border: 1px solid rgba(0,255,195,.14);
    border-radius: 22px;
    padding: 25px;
    box-shadow: 0 15px 40px rgba(0,0,0,.35);
    margin-bottom: 15px;
    transition: .3s;
}

.card:hover {
    border-color: rgba(0,255,195,.5);
    box-shadow: 0 0 30px rgba(0,255,195,.08);
}

/* Section */

.section {
    color: #00ffc3;
    font-weight: 800;
    letter-spacing: 3px;
    font-size: 14px;
    margin: 25px 0 15px;
}

/* AI Orb */

.orb {
    width: 170px;
    height: 170px;
    margin: auto;
    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(circle,
        #00ffc3 0%,
        #073b31 18%,
        #03110e 45%,
        #020506 70%);

    border: 2px solid #00ffc3;

    box-shadow:
        0 0 25px #00ffc3,
        0 0 80px rgba(0,255,195,.25);

    animation: orb 3s infinite;
}

@keyframes orb {
    0%,100% {
        transform: scale(.94);
        box-shadow:
            0 0 20px #00ffc3;
    }

    50% {
        transform: scale(1.05);
        box-shadow:
            0 0 55px #00ffc3;
    }
}

.orb-text {
    text-align: center;
    color: white;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
}

/* Score */

.big-score {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #00ffc3;
    text-shadow: 0 0 25px #00ffc3;
}

/* Metric */

.metric {
    text-align: center;
    padding: 20px;
    background: #080d11;
    border-radius: 16px;
    border: 1px solid #18242a;
}

.metric-title {
    color: #66737d;
    font-size: 10px;
    letter-spacing: 2px;
}

.metric-value {
    color: white;
    font-size: 26px;
    font-weight: 800;
    margin-top: 7px;
}

/* AI log */

.log {
    background: #020405;
    border: 1px solid #142127;
    border-radius: 15px;
    padding: 18px;
    font-family: monospace;
    color: #00ffc3;
    line-height: 2;
}

/* Recommendations */

.tip {
    padding: 16px;
    background: #080e11;
    border-left: 3px solid #00ffc3;
    border-radius: 10px;
    margin-bottom: 10px;
}

/* Button */

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    background: linear-gradient(90deg,#00ffc3,#00bfff);
    color: #00100c;
    border: none;
    font-weight: 900;
    letter-spacing: 2px;
    transition: .3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 30px rgba(0,255,195,.5);
}

/* Inputs */

div[data-baseweb="input"] > div {
    background: #080d11 !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] > div {
    background: #080d11 !important;
    border-radius: 12px !important;
}

/* Footer */

.footer {
    text-align: center;
    color: #39454d;
    letter-spacing: 4px;
    font-size: 9px;
    padding: 35px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">AURA <span>AI</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">STUDENT PERFORMANCE INTELLIGENCE PLATFORM</div>',
    unsafe_allow_html=True
)


# =========================================================
# TOP STATUS
# =========================================================

a, b, c, d = st.columns(4)

with a:
    st.metric("AI ENGINE", "ONLINE")

with b:
    st.metric("MODEL", "RANDOM FOREST")

with c:
    st.metric("ANALYSIS", "REAL-TIME")

with d:
    st.metric("STATUS", "READY")


# =========================================================
# STUDENT INPUT
# =========================================================

st.markdown(
    '<div class="section">◈ STUDENT DATA MATRIX</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:

    name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    attendance = st.slider(
        "Attendance",
        0,
        100,
        80
    )

    internal = st.slider(
        "Internal Marks",
        0,
        100,
        70
    )

with right:

    assignment = st.slider(
        "Assignment Performance",
        0,
        100,
        75
    )

    study = st.number_input(
        "Study Hours / Day",
        0.0,
        15.0,
        3.0,
        .5
    )

    previous = st.slider(
        "Previous Semester Score",
        0,
        100,
        70
    )


st.write("")

start = st.button(
    "◉ ACTIVATE AURA INTELLIGENCE"
)


# =========================================================
# AI PROCESSING
# =========================================================

if start:

    student = name if name else "Student"

    box = st.empty()

    steps = [
        "BOOTING AURA NEURAL ENGINE",
        "READING STUDENT PROFILE",
        "ANALYZING ATTENDANCE SIGNAL",
        "ANALYZING PERFORMANCE SIGNALS",
        "EXECUTING RANDOM FOREST",
        "CALCULATING RISK VECTOR",
        "GENERATING PERSONALIZED PLAN"
    ]

    for step in steps:

        box.markdown(
            f"""
            <div class="log">
            [ AURA ] &gt;&gt; {step}...
            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(.3)

    box.empty()


    # =====================================================
    # MODEL
    # =====================================================

    score = predict_score(
        attendance,
        internal,
        assignment,
        study,
        previous
    )

    risk = get_risk(score)

    recommendations = get_recommendations(
        attendance,
        internal,
        assignment,
        study,
        previous
    )


    # =====================================================
    # RESULT
    # =====================================================

    st.markdown(
        '<div class="section">◈ NEURAL CORE RESULT</div>',
        unsafe_allow_html=True
    )

    core_left, core, core_right = st.columns([1,2,1])

    with core:

        st.markdown(
            """
            <div class="card">

                <div class="orb">

                    <div class="orb-text">
                        AURA<br>
                        <span style="color:#718096;font-size:9px;">
                        ANALYZING
                        </span>
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="big-score">{score}%</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "PREDICTED FINAL PERFORMANCE"
        )


    # =====================================================
    # RESULT CARDS
    # =====================================================

    st.markdown(
        '<div class="section">◈ PERFORMANCE VECTOR</div>',
        unsafe_allow_html=True
    )

    r1, r2, r3 = st.columns(3)

    if risk == "LOW":
        risk_display = "🟢 LOW"
    elif risk == "MEDIUM":
        risk_display = "🟡 MEDIUM"
    else:
        risk_display = "🔴 HIGH"


    if score >= 85:
        level = "🏆 EXCELLENT"
    elif score >= 75:
        level = "⭐ GOOD"
    elif score >= 60:
        level = "📘 AVERAGE"
    else:
        level = "⚠️ CRITICAL"


    with r1:

        st.markdown(
            f"""
            <div class="metric">

            <div class="metric-title">
            PREDICTED SCORE
            </div>

            <div class="metric-value">
            {score}%
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with r2:

        st.markdown(
            f"""
            <div class="metric">

            <div class="metric-title">
            RISK VECTOR
            </div>

            <div class="metric-value">
            {risk_display}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with r3:

        st.markdown(
            f"""
            <div class="metric">

            <div class="metric-title">
            PERFORMANCE LEVEL
            </div>

            <div class="metric-value">
            {level}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # DATA VISUALIZATION
    # =====================================================

    st.markdown(
        '<div class="section">◈ PERFORMANCE RADAR</div>',
        unsafe_allow_html=True
    )

    data = pd.DataFrame({
        "Performance": [
            attendance,
            internal,
            assignment,
            previous,
            score
        ]
    }, index=[
        "Attendance",
        "Internal",
        "Assignments",
        "Previous",
        "Prediction"
    ])

    st.bar_chart(data)


    # =====================================================
    # RISK DETECTION
    # =====================================================

    st.markdown(
        '<div class="section">◈ EARLY WARNING SYSTEM</div>',
        unsafe_allow_html=True
    )

    problems = []

    if attendance < 75:
        problems.append("Attendance below safe threshold")

    if internal < 60:
        problems.append("Internal marks need improvement")

    if assignment < 60:
        problems.append("Assignment performance is weak")

    if study < 2:
        problems.append("Study time is insufficient")

    if previous < 60:
        problems.append("Previous score indicates risk")


    if problems:

        for problem in problems:

            st.warning(
                "⚠ " + problem
            )

    else:

        st.success(
            "✓ NO CRITICAL ACADEMIC SIGNALS DETECTED"
        )


    # =====================================================
    # AI ADVICE
    # =====================================================

    st.markdown(
        '<div class="section">◈ AURA AI ADVISOR</div>',
        unsafe_allow_html=True
    )

    for recommendation in recommendations:

        st.markdown(
            f"""
            <div class="tip">
            🤖 <b>AI:</b> {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # WHAT IF
    # =====================================================

    st.markdown(
        '<div class="section">◈ FUTURE SCENARIO SIMULATOR</div>',
        unsafe_allow_html=True
    )

    st.write(
        "What happens if the student improves attendance?"
    )

    future_attendance = st.slider(
        "Future Attendance",
        int(attendance),
        100,
        min(90, int(attendance + 10))
    )

    future_score = predict_score(
        future_attendance,
        internal,
        assignment,
        study,
        previous
    )

    improvement = round(
        future_score - score,
        1
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        st.metric(
            "CURRENT",
            f"{score}%"
        )

    with q2:
        st.metric(
            "FUTURE",
            f"{future_score}%"
        )

    with q3:
        st.metric(
            "GAIN",
            f"{improvement:+.1f}%"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AURA AI
        <br><br>
        PREDICT • UNDERSTAND • IMPROVE
        <br><br>
        AI STUDENT PERFORMANCE INTELLIGENCE
    </div>
    """,
    unsafe_allow_html=True
)
