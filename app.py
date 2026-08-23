
import streamlit as st
import pandas as pd
import time
import random

from model import (
    predict_score,
    get_risk,
    get_recommendations
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

html, body, [class*="css"] {
    color: #e6edf3;
}

/* =========================================================
   MAIN BACKGROUND
   ========================================================= */

.stApp {

    background:

        radial-gradient(
            circle at 10% 10%,
            rgba(0,255,170,0.12),
            transparent 20%
        ),

        radial-gradient(
            circle at 90% 20%,
            rgba(0,140,255,0.12),
            transparent 20%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(120,0,255,0.10),
            transparent 30%
        ),

        #020405;

    min-height: 100vh;
}


/* =========================================================
   ANIMATED GRID
   ========================================================= */

.stApp:after {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    background-image:

        linear-gradient(
            rgba(0,255,170,0.025) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(0,255,170,0.025) 1px,
            transparent 1px
        );

    background-size: 50px 50px;

    animation: gridMove 15s linear infinite;

    z-index: 0;
}


@keyframes gridMove {

    from {
        transform: translateY(0);
    }

    to {
        transform: translateY(50px);
    }

}


/* =========================================================
   SCAN LINE
   ========================================================= */

.stApp:before {

    content: "";

    position: fixed;

    left: 0;

    right: 0;

    height: 2px;

    background: linear-gradient(
        90deg,
        transparent,
        #00ffaa,
        transparent
    );

    opacity: 0.25;

    animation: scan 6s linear infinite;

    pointer-events: none;

    z-index: 999;
}


@keyframes scan {

    0% {
        top: -5%;
    }

    100% {
        top: 105%;
    }

}


/* =========================================================
   REMOVE STREAMLIT UI
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {

    position: relative;

    padding: 50px;

    margin-bottom: 25px;

    border-radius: 30px;

    background:

        linear-gradient(
            135deg,
            rgba(5,10,12,0.98),
            rgba(8,20,20,0.94)
        );

    border: 1px solid rgba(0,255,170,0.25);

    box-shadow:

        0 0 60px rgba(0,255,170,0.07),

        inset 0 0 60px rgba(0,255,170,0.02);

    overflow: hidden;

    z-index: 1;
}


/* animated light */

.hero-light {

    position: absolute;

    width: 350px;

    height: 350px;

    border-radius: 50%;

    right: -150px;

    top: -180px;

    background:

        radial-gradient(
            circle,
            rgba(0,255,170,0.2),
            transparent 65%
        );

    animation: heroPulse 4s infinite;
}


@keyframes heroPulse {

    0%,100% {
        transform: scale(0.9);
    }

    50% {
        transform: scale(1.2);
    }

}


/* =========================================================
   TYPOGRAPHY
   ========================================================= */

.system {

    color: #00ffaa;

    font-family: 'Orbitron';

    letter-spacing: 5px;

    font-size: 11px;

    margin-bottom: 15px;
}


.hero-title {

    font-family: 'Orbitron';

    font-size: 52px;

    font-weight: 900;

    letter-spacing: 4px;

    color: white;

    text-shadow:
        0 0 20px rgba(0,255,170,0.4);
}


.hero-title span {

    color: #00ffaa;

}


.hero-subtitle {

    color: #78838a;

    margin-top: 10px;

    font-size: 16px;
}


/* =========================================================
   ONLINE STATUS
   ========================================================= */

.online {

    display: inline-flex;

    align-items: center;

    gap: 10px;

    margin-top: 25px;

    padding: 8px 15px;

    border-radius: 30px;

    border: 1px solid rgba(0,255,170,0.25);

    background: rgba(0,255,170,0.04);

    color: #00ffaa;

    font-family: 'Orbitron';

    font-size: 10px;

    letter-spacing: 2px;
}


.online-dot {

    width: 8px;

    height: 8px;

    background: #00ffaa;

    border-radius: 50%;

    box-shadow: 0 0 12px #00ffaa;

    animation: blink 1s infinite;
}


@keyframes blink {

    0%,100% {
        opacity: 1;
    }

    50% {
        opacity: 0.2;
    }

}


/* =========================================================
   SECTION
   ========================================================= */

.section {

    font-family: 'Orbitron';

    color: #00ffaa;

    letter-spacing: 3px;

    font-size: 17px;

    margin-top: 30px;

    margin-bottom: 15px;
}


/* =========================================================
   GLASS CARD
   ========================================================= */

.glass {

    background:

        linear-gradient(
            145deg,
            rgba(12,17,19,0.95),
            rgba(4,7,8,0.95)
        );

    border:

        1px solid
        rgba(255,255,255,0.06);

    border-radius: 20px;

    padding: 25px;

    box-shadow:

        0 15px 40px
        rgba(0,0,0,0.35),

        inset 0 0 30px
        rgba(0,255,170,0.015);

    transition: 0.3s;

}


.glass:hover {

    transform: translateY(-4px);

    border-color:
        rgba(0,255,170,0.3);

    box-shadow:

        0 0 30px
        rgba(0,255,170,0.08);
}


/* =========================================================
   AI CORE
   ========================================================= */

.ai-core {

    width: 210px;

    height: 210px;

    margin: 10px auto 25px auto;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    position: relative;

    background:

        radial-gradient(
            circle,
            #071412 25%,
            #020606 55%,
            transparent 70%
        );

    border: 2px solid #00ffaa;

    box-shadow:

        0 0 25px rgba(0,255,170,0.4),

        inset 0 0 30px rgba(0,255,170,0.15);

    animation: corePulse 3s infinite;
}


.ai-core:before {

    content: "";

    position: absolute;

    inset: -18px;

    border-radius: 50%;

    border:

        1px dashed
        rgba(0,255,170,0.5);

    animation:
        rotate 8s linear infinite;
}


.ai-core:after {

    content: "";

    position: absolute;

    inset: -35px;

    border-radius: 50%;

    border:

        1px solid
        rgba(0,255,170,0.1);

    animation:
        rotateReverse 12s linear infinite;
}


@keyframes corePulse {

    0%,100% {

        transform: scale(0.95);

        box-shadow:
            0 0 20px
            rgba(0,255,170,0.25);
    }

    50% {

        transform: scale(1.05);

        box-shadow:
            0 0 50px
            rgba(0,255,170,0.55);
    }

}


@keyframes rotate {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }

}


@keyframes rotateReverse {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }

}


.core-text {

    text-align: center;

    font-family: 'Orbitron';

    color: #00ffaa;

    font-size: 13px;

    letter-spacing: 2px;

}


/* =========================================================
   SCORE
   ========================================================= */

.score {

    font-family: 'Orbitron';

    font-size: 45px;

    font-weight: 900;

    color: #00ffaa;

    text-align: center;

    text-shadow:
        0 0 20px
        rgba(0,255,170,0.6);
}


.score-label {

    text-align: center;

    color: #657078;

    font-family: 'Orbitron';

    font-size: 10px;

    letter-spacing: 3px;
}


/* =========================================================
   METRICS
   ========================================================= */

.metric {

    padding: 22px;

    background: #070b0d;

    border-radius: 17px;

    border: 1px solid #182326;

    text-align: center;

    transition: 0.3s;
}


.metric:hover {

    border-color: #00ffaa;

    box-shadow:
        0 0 25px
        rgba(0,255,170,0.1);
}


.metric-label {

    font-family: 'Orbitron';

    color: #657078;

    font-size: 9px;

    letter-spacing: 2px;
}


.metric-value {

    color: white;

    font-family: 'Orbitron';

    font-size: 25px;

    font-weight: 700;

    margin-top: 8px;
}


/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {

    height: 58px;

    width: 100%;

    border-radius: 14px;

    border: 1px solid #00ffaa;

    background:

        linear-gradient(
            90deg,
            #00ffaa,
            #00c98b
        );

    color: #00130d;

    font-family: 'Orbitron';

    font-weight: 900;

    letter-spacing: 2px;

    transition: 0.3s;
}


.stButton > button:hover {

    transform:
        translateY(-2px)
        scale(1.01);

    box-shadow:

        0 0 30px
        rgba(0,255,170,0.5);
}


/* =========================================================
   INPUT
   ========================================================= */

div[data-baseweb="input"] > div {

    background: #070b0d !important;

    border:
        1px solid #1b292d !important;

    border-radius: 12px !important;
}


/* =========================================================
   RECOMMENDATION
   ========================================================= */

.recommend {

    padding: 16px;

    margin-bottom: 10px;

    border-radius: 12px;

    background: #080d0f;

    border-left:
        3px solid #00ffaa;

    transition: 0.2s;
}


.recommend:hover {

    transform: translateX(6px);

    background: #0c1517;
}


/* =========================================================
   TERMINAL
   ========================================================= */

.terminal {

    background: #010303;

    border: 1px solid #172325;

    border-radius: 14px;

    padding: 20px;

    font-family: monospace;

    color: #00ffaa;

    line-height: 1.8;

    box-shadow:
        inset 0 0 25px
        rgba(0,255,170,0.03);
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align: center;

    padding: 40px;

    color: #374148;

    font-family: 'Orbitron';

    font-size: 9px;

    letter-spacing: 3px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-light"></div>

<div class="system">
NEXUS // NEURAL EDUCATION INTELLIGENCE
</div>

<div class="hero-title">
EDU<span>PREDICT</span>
</div>

<div class="hero-subtitle">
Predict. Detect. Improve.
</div>

<div class="online">
<div class="online-dot"></div>
AI CORE ONLINE
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT
# ============================================================

st.markdown(
    '<div class="section">◈ STUDENT NEURAL PROFILE</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2)


with left:

    student_name = st.text_input(
        "Student Identifier",
        placeholder="Enter student name"
    )

    attendance = st.slider(
        "📡 Attendance",
        0,
        100,
        80
    )

    internal_marks = st.slider(
        "🧠 Internal Performance",
        0,
        100,
        70
    )


with right:

    assignment_marks = st.slider(
        "📚 Assignment Performance",
        0,
        100,
        75
    )

    study_hours = st.number_input(
        "⚡ Study Hours / Day",
        0.0,
        15.0,
        3.0,
        0.5
    )

    previous_score = st.slider(
        "📈 Previous Score",
        0,
        100,
        70
    )


st.write("")


run = st.button(
    "⚡ INITIALIZE AI ANALYSIS"
)


# ============================================================
# ANALYSIS
# ============================================================

if run:

    student = (
        student_name
        if student_name
        else "UNKNOWN STUDENT"
    )


    # ========================================================
    # AI ANIMATION
    # ========================================================

    placeholder = st.empty()


    messages = [

        "◈ CONNECTING TO AI CORE...",

        "◈ ANALYZING ATTENDANCE SIGNAL...",

        "◈ PROCESSING ACADEMIC FEATURES...",

        "◈ RUNNING RANDOM FOREST MODEL...",

        "◈ DETECTING RISK PATTERNS...",

        "◈ GENERATING PERSONALIZED STRATEGY..."

    ]


    for message in messages:

        placeholder.markdown(
            f"""
            <div class="terminal">

            <span style="color:#00ffaa">
            SYSTEM
            </span>

            <br>

            {message}

            <span style="animation:blink 1s infinite">
            █
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(0.45)


    placeholder.empty()


    # ========================================================
    # MODEL
    # ========================================================

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


    # ========================================================
    # AI CORE
    # ========================================================

    st.markdown(
        '<div class="section">◈ AI CORE</div>',
        unsafe_allow_html=True
    )


    core1, core2, core3 = st.columns([1, 2, 1])


    with core2:

        st.markdown(f"""
        <div class="glass">

        <div class="ai-core">

            <div class="core-text">

            NEXUS<br>

            <span style="
                font-size:10px;
                color:#68737a;
            ">
            ACTIVE
            </span>

            </div>

        </div>

        <div class="score">
            {score}%
        </div>

        <div class="score-label">
            PREDICTED PERFORMANCE
        </div>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # METRICS
    # ========================================================

    st.markdown(
        '<div class="section">◈ INTELLIGENCE OUTPUT</div>',
        unsafe_allow_html=True
    )


    a, b, c = st.columns(3)


    if risk == "LOW":

        risk_icon = "🟢"

    elif risk == "MEDIUM":

        risk_icon = "🟡"

    else:

        risk_icon = "🔴"


    if score >= 85:

        performance = "EXCELLENT"

    elif score >= 75:

        performance = "GOOD"

    elif score >= 60:

        performance = "AVERAGE"

    else:

        performance = "CRITICAL"


    with a:

        st.markdown(f"""
        <div class="metric">

        <div class="metric-label">
        PREDICTED SCORE
        </div>

        <div class="metric-value">
        {score}%
        </div>

        </div>
        """, unsafe_allow_html=True)


    with b:

        st.markdown(f"""
        <div class="metric">

        <div class="metric-label">
        RISK STATUS
        </div>

        <div class="metric-value">
        {risk_icon} {risk}
        </div>

        </div>
        """, unsafe_allow_html=True)


    with c:

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


    # ========================================================
    # SIGNAL ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section">◈ SIGNAL ANALYSIS</div>',
        unsafe_allow_html=True
    )


    chart = pd.DataFrame({

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


    st.bar_chart(chart)


    # ========================================================
    # RISK ENGINE
    # ========================================================

    st.markdown(
        '<div class="section">◈ RISK ENGINE</div>',
        unsafe_allow_html=True
    )


    factors = []


    if attendance < 75:

        factors.append(
            "⚠ Attendance below safe threshold"
        )


    if internal_marks < 60:

        factors.append(
            "⚠ Internal marks require improvement"
        )


    if assignment_marks < 60:

        factors.append(
            "⚠ Assignment performance is weak"
        )


    if study_hours < 2:

        factors.append(
            "⚠ Study time is below recommended level"
        )


    if previous_score < 60:

        factors.append(
            "⚠ Previous academic performance is low"
        )


    if not factors:

        st.success(
            "✓ SYSTEM STATUS: NO CRITICAL SIGNALS"
        )

    else:

        for factor in factors:

            st.warning(factor)


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.markdown(
        '<div class="section">◈ AI STRATEGY GENERATOR</div>',
        unsafe_allow_html=True
    )


    for recommendation in recommendations:

        st.markdown(

            f"""
            <div class="recommend">

            <span style="
                color:#00ffaa;
                font-family:Orbitron;
            ">
            AI →
            </span>

            {recommendation}

            </div>
            """,

            unsafe_allow_html=True

        )


    # ========================================================
    # FUTURE SIMULATOR
    # ========================================================

    st.markdown(
        '<div class="section">◈ FUTURE SIMULATION</div>',
        unsafe_allow_html=True
    )


    st.markdown("""
    <div class="glass">

    <b>WHAT-IF ENGINE</b>

    <br><br>

    Modify attendance and see how the
    AI prediction responds.

    </div>
    """, unsafe_allow_html=True)


    simulated_attendance = st.slider(

        "Simulated Attendance",

        int(attendance),

        100,

        min(
            int(attendance + 10),
            100
        )
    )


    simulated_score = predict_score(

        simulated_attendance,

        internal_marks,

        assignment_marks,

        study_hours,

        previous_score
    )


    change = round(
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
            "IMPROVEMENT",
            f"{change:+.1f}%"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

NEXUS AI

<br><br>

EDUCATION INTELLIGENCE SYSTEM

<br><br>

PREDICT • DETECT • IMPROVE

</div>
""", unsafe_allow_html=True)
