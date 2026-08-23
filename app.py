
import streamlit as st
import pandas as pd
import time

from model import (
    predict_score,
    get_risk,
    get_recommendations
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NEXUS AI | Student Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DARK FUTURISTIC CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* ================= BODY ================= */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0,255,170,0.08), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(90,0,255,0.10), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(0,150,255,0.08), transparent 30%),
        #030506;
    color: #e5e7eb;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ================= SCANLINES ================= */

.stApp:before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background: repeating-linear-gradient(
        0deg,
        rgba(255,255,255,0.015) 0px,
        rgba(255,255,255,0.015) 1px,
        transparent 1px,
        transparent 4px
    );
    z-index: 999;
}


/* ================= HERO ================= */

.hero {

    position: relative;

    padding: 45px;

    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            rgba(10,15,20,0.96),
            rgba(5,20,20,0.92)
        );

    border: 1px solid rgba(0,255,170,0.25);

    box-shadow:
        0 0 30px rgba(0,255,170,0.08),
        inset 0 0 40px rgba(0,255,170,0.02);

    overflow: hidden;

    margin-bottom: 25px;
}


.hero:after {

    content: "";

    position: absolute;

    width: 250px;
    height: 250px;

    border-radius: 50%;

    right: -100px;
    top: -100px;

    border: 1px solid rgba(0,255,170,0.25);

    box-shadow:
        0 0 30px rgba(0,255,170,0.2);

    animation: pulse 3s infinite;
}


@keyframes pulse {

    0% {
        transform: scale(0.8);
        opacity: 0.3;
    }

    50% {
        transform: scale(1.1);
        opacity: 0.7;
    }

    100% {
        transform: scale(0.8);
        opacity: 0.3;
    }
}


.system {

    color: #00ffaa;

    font-family: 'Orbitron';

    font-size: 12px;

    letter-spacing: 4px;

    margin-bottom: 15px;
}


.hero-title {

    font-family: 'Orbitron';

    font-size: 44px;

    font-weight: 800;

    letter-spacing: 2px;

    color: white;

    text-shadow:
        0 0 15px rgba(0,255,170,0.5);
}


.hero-title span {

    color: #00ffaa;

}


.hero-subtitle {

    margin-top: 10px;

    color: #8b949e;

    font-size: 16px;
}


/* ================= STATUS ================= */

.status {

    display: inline-flex;

    align-items: center;

    gap: 10px;

    margin-top: 25px;

    padding: 8px 15px;

    border-radius: 50px;

    background: rgba(0,255,170,0.05);

    border: 1px solid rgba(0,255,170,0.2);

    color: #00ffaa;

    font-family: 'Orbitron';

    font-size: 11px;
}


.status-dot {

    width: 8px;
    height: 8px;

    background: #00ffaa;

    border-radius: 50%;

    box-shadow:
        0 0 8px #00ffaa;

    animation: blink 1.2s infinite;
}


@keyframes blink {

    0%, 100% {
        opacity: 1;
    }

    50% {
        opacity: 0.2;
    }
}


/* ================= SECTION ================= */

.section {

    font-family: 'Orbitron';

    font-size: 18px;

    letter-spacing: 2px;

    color: #00ffaa;

    margin-top: 25px;

    margin-bottom: 15px;
}


/* ================= GLASS CARD ================= */

.card {

    background:
        linear-gradient(
            145deg,
            rgba(16,20,24,0.95),
            rgba(5,8,10,0.95)
        );

    border: 1px solid #1c272b;

    border-radius: 18px;

    padding: 22px;

    box-shadow:
        0 10px 40px rgba(0,0,0,0.35);

    transition: all 0.3s ease;
}


.card:hover {

    transform: translateY(-4px);

    border-color: rgba(0,255,170,0.4);

    box-shadow:
        0 0 25px rgba(0,255,170,0.08);
}


/* ================= METRICS ================= */

.metric {

    background: #080b0d;

    border: 1px solid #172125;

    border-radius: 18px;

    padding: 25px;

    text-align: center;

    transition: 0.3s;
}


.metric:hover {

    border-color: #00ffaa;

    box-shadow:
        0 0 20px rgba(0,255,170,0.1);
}


.metric-label {

    color: #68737a;

    font-size: 11px;

    font-family: 'Orbitron';

    letter-spacing: 2px;
}


.metric-value {

    color: white;

    font-family: 'Orbitron';

    font-size: 30px;

    font-weight: 700;

    margin-top: 8px;
}


/* ================= BUTTON ================= */

.stButton > button {

    height: 55px;

    border-radius: 12px;

    border: 1px solid #00ffaa;

    background:
        linear-gradient(
            90deg,
            #00ffaa,
            #00c98b
        );

    color: #00150e;

    font-family: 'Orbitron';

    font-weight: 800;

    letter-spacing: 1px;

    transition: all 0.25s ease;
}


.stButton > button:hover {

    transform: scale(1.01);

    box-shadow:
        0 0 25px rgba(0,255,170,0.45);
}


/* ================= INPUTS ================= */

div[data-baseweb="input"] > div {

    background: #080b0d !important;

    border: 1px solid #1b292d !important;

    border-radius: 10px !important;

}


div[data-baseweb="select"] > div {

    background: #080b0d !important;

    border-radius: 10px !important;

}


/* ================= SCORE RING ================= */

.score-ring {

    width: 190px;

    height: 190px;

    border-radius: 50%;

    margin: 20px auto;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        radial-gradient(
            circle,
            #050809 55%,
            transparent 56%
        );

    border: 5px solid #00ffaa;

    box-shadow:
        0 0 15px rgba(0,255,170,0.4),
        inset 0 0 20px rgba(0,255,170,0.15);

    animation: ringpulse 2.5s infinite;
}


@keyframes ringpulse {

    0%,100% {
        box-shadow:
            0 0 15px rgba(0,255,170,0.25),
            inset 0 0 15px rgba(0,255,170,0.1);
    }

    50% {
        box-shadow:
            0 0 35px rgba(0,255,170,0.55),
            inset 0 0 25px rgba(0,255,170,0.2);
    }
}


.score-number {

    font-family: 'Orbitron';

    font-size: 42px;

    font-weight: 800;

    color: #00ffaa;
}


/* ================= RECOMMENDATIONS ================= */

.recommendation {

    background: #080c0e;

    border-left: 3px solid #00ffaa;

    padding: 16px;

    border-radius: 10px;

    margin-bottom: 10px;

    color: #c9d1d9;

    transition: 0.2s;
}


.recommendation:hover {

    background: #0c1315;

    transform: translateX(5px);
}


/* ================= RISK ================= */

.low {

    color: #00ffaa;

    text-shadow:
        0 0 10px rgba(0,255,170,0.5);
}


.medium {

    color: #ffd166;

    text-shadow:
        0 0 10px rgba(255,209,102,0.4);
}


.high {

    color: #ff4d6d;

    text-shadow:
        0 0 10px rgba(255,77,109,0.5);
}


/* ================= FOOTER ================= */

.footer {

    text-align: center;

    color: #465057;

    font-size: 11px;

    font-family: 'Orbitron';

    letter-spacing: 2px;

    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<div class="system">
NEXUS // STUDENT INTELLIGENCE SYSTEM
</div>

<div class="hero-title">
EDU<span>PREDICT</span> AI
</div>

<div class="hero-subtitle">
AI-powered academic intelligence & early-warning system
</div>

<div class="status">
<div class="status-dot"></div>
AI CORE ONLINE
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    '<div class="section">◈ STUDENT DATA INPUT</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:

    name = st.text_input(
        "Student ID / Name",
        placeholder="Enter student name"
    )

    attendance = st.slider(
        "Attendance %",
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


with c2:

    assignment_marks = st.slider(
        "Assignment Performance",
        0,
        100,
        75
    )

    study_hours = st.number_input(
        "Study Hours / Day",
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


st.write("")

analyze = st.button(
    "⚡ RUN AI PERFORMANCE ANALYSIS"
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    student = name if name else "STUDENT-001"

    with st.spinner("◈ NEXUS AI CORE ANALYZING DATA..."):

        time.sleep(1)

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
        f"AI ANALYSIS COMPLETE // {student.upper()}"
    )


    # =====================================================
    # SCORE
    # =====================================================

    st.markdown(
        '<div class="section">◈ AI PREDICTION</div>',
        unsafe_allow_html=True
    )


    score_col, info_col = st.columns([1, 2])


    with score_col:

        st.markdown(f"""
        <div class="card">

        <div style="
            text-align:center;
            color:#68737a;
            font-family:Orbitron;
            font-size:11px;
            letter-spacing:2px;
        ">
        PREDICTED SCORE
        </div>

        <div class="score-ring">

            <div class="score-number">
                {score}%
            </div>

        </div>

        <div style="
            text-align:center;
            color:#68737a;
            font-size:12px;
        ">
        MODEL CONFIDENCE OUTPUT
        </div>

        </div>
        """, unsafe_allow_html=True)


    with info_col:

        m1, m2 = st.columns(2)

        with m1:

            st.markdown(f"""
            <div class="metric">

            <div class="metric-label">
            RISK LEVEL
            </div>

            <div class="metric-value">

            {"🟢" if risk=="LOW"
             else "🟡" if risk=="MEDIUM"
             else "🔴"}

            {risk}

            </div>

            </div>
            """, unsafe_allow_html=True)


        with m2:

            if score >= 85:
                performance = "EXCELLENT"
            elif score >= 75:
                performance = "GOOD"
            elif score >= 60:
                performance = "AVERAGE"
            else:
                performance = "CRITICAL"


            st.markdown(f"""
            <div class="metric">

            <div class="metric-label">
            PERFORMANCE
            </div>

            <div class="metric-value">
            {performance}
            </div>

            </div>
            """, unsafe_allow_html=True)


        st.write("")

        st.markdown(
            f"""
            <div class="card">

            <b>AI STATUS</b>

            <br><br>

            Model successfully analyzed
            <b>{student}</b>'s academic profile.

            <br><br>

            Prediction:
            <b>{score}%</b>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # ACADEMIC SIGNALS
    # =====================================================

    st.markdown(
        '<div class="section">◈ ACADEMIC SIGNALS</div>',
        unsafe_allow_html=True
    )


    signal_data = pd.DataFrame({

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
        "Previous",
        "AI Prediction"

    ])


    st.bar_chart(
        signal_data
    )


    # =====================================================
    # RISK ENGINE
    # =====================================================

    st.markdown(
        '<div class="section">◈ RISK DETECTION ENGINE</div>',
        unsafe_allow_html=True
    )


    factors = []


    if attendance < 75:
        factors.append(
            "LOW ATTENDANCE DETECTED"
        )

    if internal_marks < 60:
        factors.append(
            "LOW INTERNAL PERFORMANCE"
        )

    if assignment_marks < 60:
        factors.append(
            "ASSIGNMENT PERFORMANCE BELOW TARGET"
        )

    if study_hours < 2:
        factors.append(
            "INSUFFICIENT STUDY HOURS"
        )

    if previous_score < 60:
        factors.append(
            "PREVIOUS PERFORMANCE BELOW TARGET"
        )


    if not factors:

        st.success(
            "✓ NO CRITICAL RISK SIGNALS DETECTED"
        )

    else:

        for factor in factors:

            st.warning(
                "⚠ " + factor
            )


    # =====================================================
    # AI RECOMMENDATIONS
    # =====================================================

    st.markdown(
        '<div class="section">◈ AI ACTION PLAN</div>',
        unsafe_allow_html=True
    )


    for rec in recommendations:

        st.markdown(
            f"""
            <div class="recommendation">

            <span style="
                color:#00ffaa;
                font-family:Orbitron;
            ">
            AI →
            </span>

            {rec}

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # WHAT IF
    # =====================================================

    st.markdown(
        '<div class="section">◈ FUTURE SIMULATOR</div>',
        unsafe_allow_html=True
    )


    st.markdown("""
    <div class="card">

    Simulate an improvement and observe
    how the AI prediction changes.

    </div>
    """, unsafe_allow_html=True)


    simulated_attendance = st.slider(
        "Simulated Attendance",
        int(attendance),
        100,
        min(int(attendance + 10), 100)
    )


    simulated_score = predict_score(

        simulated_attendance,

        internal_marks,

        assignment_marks,

        study_hours,

        previous_score
    )


    difference = round(
        simulated_score - score,
        1
    )


    x1, x2, x3 = st.columns(3)


    with x1:

        st.metric(
            "CURRENT",
            f"{score}%"
        )


    with x2:

        st.metric(
            "SIMULATED",
            f"{simulated_score}%"
        )


    with x3:

        st.metric(
            "CHANGE",
            f"{difference:+.1f}%"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

NEXUS AI // EDU-PREDICT

<br><br>

STUDENT INTELLIGENCE • EARLY WARNING • PERSONALIZED ACTION

</div>
""", unsafe_allow_html=True)
