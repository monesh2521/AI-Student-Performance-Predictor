
import streamlit as st
import pandas as pd
import time

from model import (
    predict_score,
    get_risk,
    get_recommendations
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NEXUS | AI Student Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(0, 255, 170, 0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(0, 120, 255, 0.10),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(140, 0, 255, 0.08),
                transparent 30%
            ),
            #020405;

        color: #f5f7fa;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }


    /* =========================
       MOVING GRID
       ========================= */

    .grid-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;

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

        background-size: 45px 45px;

        animation: gridmove 12s linear infinite;
    }

    @keyframes gridmove {
        from {
            transform: translateY(0);
        }

        to {
            transform: translateY(45px);
        }
    }


    /* =========================
       HERO
       ========================= */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 42px;

        border-radius: 26px;

        background:
            linear-gradient(
                135deg,
                rgba(7, 15, 16, 0.98),
                rgba(4, 8, 10, 0.96)
            );

        border: 1px solid rgba(0,255,170,0.22);

        box-shadow:
            0 0 50px rgba(0,255,170,0.06),
            inset 0 0 40px rgba(0,255,170,0.025);

        z-index: 1;
    }


    .hero-orb {
        position: absolute;

        width: 260px;
        height: 260px;

        right: -80px;
        top: -100px;

        border-radius: 50%;

        border: 1px solid rgba(0,255,170,0.25);

        box-shadow:
            0 0 30px rgba(0,255,170,0.15);

        animation: orb 4s ease-in-out infinite;
    }

    @keyframes orb {

        0%, 100% {
            transform: scale(0.9);
            opacity: 0.4;
        }

        50% {
            transform: scale(1.15);
            opacity: 0.9;
        }
    }


    .hero-small {
        color: #00ffaa;

        font-size: 11px;

        letter-spacing: 4px;

        font-weight: 700;

        margin-bottom: 12px;
    }


    .hero-title {
        font-size: 48px;

        font-weight: 900;

        letter-spacing: 3px;

        color: white;

        text-shadow:
            0 0 20px rgba(0,255,170,0.35);
    }


    .hero-title span {
        color: #00ffaa;
    }


    .hero-description {
        margin-top: 12px;

        color: #7d8991;

        font-size: 16px;
    }


    /* =========================
       STATUS
       ========================= */

    .status {
        display: inline-flex;

        align-items: center;

        gap: 9px;

        margin-top: 22px;

        padding: 8px 14px;

        border-radius: 50px;

        background: rgba(0,255,170,0.04);

        border: 1px solid rgba(0,255,170,0.2);

        color: #00ffaa;

        font-size: 10px;

        letter-spacing: 2px;
    }


    .status-dot {
        width: 8px;
        height: 8px;

        background: #00ffaa;

        border-radius: 50%;

        box-shadow: 0 0 12px #00ffaa;

        animation: blink 1s infinite;
    }


    @keyframes blink {

        0%, 100% {
            opacity: 1;
        }

        50% {
            opacity: 0.2;
        }
    }


    /* =========================
       SECTION
       ========================= */

    .section-title {

        margin-top: 30px;

        margin-bottom: 16px;

        color: #00ffaa;

        font-size: 16px;

        font-weight: 800;

        letter-spacing: 2px;
    }


    /* =========================
       GLASS CARD
       ========================= */

    .glass {

        background:
            linear-gradient(
                145deg,
                rgba(13,19,21,0.96),
                rgba(5,8,9,0.96)
            );

        border: 1px solid rgba(255,255,255,0.06);

        border-radius: 20px;

        padding: 24px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.35);

        transition: 0.3s;
    }


    .glass:hover {

        transform: translateY(-3px);

        border-color:
            rgba(0,255,170,0.25);

        box-shadow:
            0 0 25px rgba(0,255,170,0.07);
    }


    /* =========================
       AI CORE
       ========================= */

    .core-container {

        display: flex;

        justify-content: center;

        align-items: center;

        padding: 15px;
    }


    .core {

        width: 180px;
        height: 180px;

        border-radius: 50%;

        display: flex;

        justify-content: center;

        align-items: center;

        position: relative;

        background:
            radial-gradient(
                circle,
                #09201b 0%,
                #04100d 40%,
                #020605 70%
            );

        border: 2px solid #00ffaa;

        box-shadow:
            0 0 20px rgba(0,255,170,0.35),
            inset 0 0 30px rgba(0,255,170,0.15);

        animation: corepulse 2.5s infinite;
    }


    .core:before {

        content: "";

        position: absolute;

        width: 215px;
        height: 215px;

        border-radius: 50%;

        border: 1px dashed rgba(0,255,170,0.4);

        animation: rotate 8s linear infinite;
    }


    .core:after {

        content: "";

        position: absolute;

        width: 250px;
        height: 250px;

        border-radius: 50%;

        border: 1px solid rgba(0,150,255,0.12);

        animation: reverseRotate 12s linear infinite;
    }


    @keyframes corepulse {

        0%, 100% {
            transform: scale(0.95);
            box-shadow:
                0 0 20px rgba(0,255,170,0.3);
        }

        50% {
            transform: scale(1.05);
            box-shadow:
                0 0 45px rgba(0,255,170,0.55);
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


    @keyframes reverseRotate {

        from {
            transform: rotate(360deg);
        }

        to {
            transform: rotate(0deg);
        }
    }


    .core-text {

        color: #00ffaa;

        text-align: center;

        font-size: 13px;

        font-weight: 800;

        letter-spacing: 3px;
    }


    /* =========================
       SCORE
       ========================= */

    .score {

        text-align: center;

        color: #00ffaa;

        font-size: 44px;

        font-weight: 900;

        margin-top: 12px;

        text-shadow:
            0 0 20px rgba(0,255,170,0.5);
    }


    .score-label {

        text-align: center;

        color: #657078;

        font-size: 10px;

        letter-spacing: 2px;
    }


    /* =========================
       METRIC
       ========================= */

    .metric-card {

        text-align: center;

        padding: 22px;

        border-radius: 17px;

        background: #070b0d;

        border: 1px solid #182326;

        transition: 0.3s;
    }


    .metric-card:hover {

        border-color: #00ffaa;

        box-shadow:
            0 0 25px rgba(0,255,170,0.1);
    }


    .metric-label {

        color: #66727a;

        font-size: 9px;

        letter-spacing: 2px;

        font-weight: 700;
    }


    .metric-value {

        color: white;

        font-size: 25px;

        font-weight: 800;

        margin-top: 8px;
    }


    /* =========================
       TERMINAL
       ========================= */

    .terminal {

        background: #010303;

        border: 1px solid #172326;

        border-radius: 14px;

        padding: 18px;

        color: #00ffaa;

        font-family: monospace;

        font-size: 13px;

        line-height: 1.8;

        box-shadow:
            inset 0 0 25px rgba(0,255,170,0.03);
    }


    .terminal-title {

        color: #68757d;

        margin-bottom: 8px;
    }


    /* =========================
       RECOMMENDATIONS
       ========================= */

    .recommendation {

        background: #080d0f;

        border-left: 3px solid #00ffaa;

        border-radius: 10px;

        padding: 15px;

        margin-bottom: 9px;

        color: #c7d0d5;

        transition: 0.25s;
    }


    .recommendation:hover {

        transform: translateX(5px);

        background: #0c1517;
    }


    /* =========================
       BUTTON
       ========================= */

    .stButton > button {

        width: 100%;

        height: 56px;

        border-radius: 13px;

        border: 1px solid #00ffaa;

        background:
            linear-gradient(
                90deg,
                #00ffaa,
                #00c98b
            );

        color: #00150e;

        font-size: 14px;

        font-weight: 900;

        letter-spacing: 1px;

        transition: 0.25s;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 0 30px rgba(0,255,170,0.45);
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {

        text-align: center;

        margin-top: 50px;

        padding: 30px;

        color: #354047;

        font-size: 10px;

        letter-spacing: 3px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MOVING GRID
# ============================================================

st.markdown(
    '<div class="grid-background"></div>',
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-orb"></div>

        <div class="hero-small">
            NEXUS // EDUCATION INTELLIGENCE
        </div>

        <div class="hero-title">
            EDU<span>PREDICT</span>
        </div>

        <div class="hero-description">
            Predict academic performance before it becomes a problem.
        </div>

        <div class="status">
            <div class="status-dot"></div>
            AI ENGINE ONLINE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">◈ STUDENT PROFILE</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    attendance = st.slider(
        "📡 Attendance",
        0,
        100,
        80
    )

    internal_marks = st.slider(
        "🧠 Internal Marks",
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
        "⚡ Study Hours / Day",
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


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.button(
    "⚡ START AI ANALYSIS"
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    student = student_name.strip()

    if student == "":
        student = "STUDENT-001"


    # --------------------------------------------------------
    # ANIMATION
    # --------------------------------------------------------

    status_box = st.empty()


    animation_steps = [

        "INITIALIZING NEURAL ENGINE",

        "READING ACADEMIC SIGNALS",

        "NORMALIZING STUDENT DATA",

        "RUNNING RANDOM FOREST",

        "CALCULATING PERFORMANCE",

        "DETECTING RISK PATTERNS",

        "GENERATING AI STRATEGY"

    ]


    for step in animation_steps:

        status_box.markdown(
            f"""
            <div class="terminal">

                <div class="terminal-title">
                    NEXUS AI // SYSTEM LOG
                </div>

                <span style="color:#00ffaa;">
                    ●
                </span>

                {step}
                <span style="animation:blink 1s infinite;">
                    █
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(0.35)


    status_box.empty()


    # --------------------------------------------------------
    # RANDOM FOREST PREDICTION
    # --------------------------------------------------------

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
        f"✓ ANALYSIS COMPLETE — {student}"
    )


    # ========================================================
    # AI CORE
    # ========================================================

    st.markdown(
        '<div class="section-title">◈ AI CORE OUTPUT</div>',
        unsafe_allow_html=True
    )


    core_left, core_middle, core_right = st.columns(
        [1, 2, 1]
    )


    with core_middle:

        st.markdown(
            f"""
            <div class="glass">

                <div class="core-container">

                    <div class="core">

                        <div class="core-text">
                            NEXUS
                            <br>
                            <span style="
                                font-size:9px;
                                color:#68757d;
                            ">
                                ACTIVE
                            </span>
                        </div>

                    </div>

                </div>

                <div class="score">
                    {score}%
                </div>

                <div class="score-label">
                    PREDICTED PERFORMANCE
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # METRICS
    # ========================================================

    st.markdown(
        '<div class="section-title">◈ INTELLIGENCE RESULTS</div>',
        unsafe_allow_html=True
    )


    if score >= 85:
        performance = "EXCELLENT"
        performance_icon = "🏆"

    elif score >= 75:
        performance = "GOOD"
        performance_icon = "⭐"

    elif score >= 60:
        performance = "AVERAGE"
        performance_icon = "📘"

    else:
        performance = "CRITICAL"
        performance_icon = "⚠️"


    if risk == "LOW":
        risk_icon = "🟢"

    elif risk == "MEDIUM":
        risk_icon = "🟡"

    else:
        risk_icon = "🔴"


    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    AI SCORE
                </div>

                <div class="metric-value">
                    {score}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    RISK LEVEL
                </div>

                <div class="metric-value">
                    {risk_icon} {risk}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    PERFORMANCE
                </div>

                <div class="metric-value">
                    {performance_icon} {performance}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # PERFORMANCE GRAPH
    # ========================================================

    st.markdown(
        '<div class="section-title">◈ ACADEMIC SIGNALS</div>',
        unsafe_allow_html=True
    )


    chart_data = pd.DataFrame(
        {
            "Score": [
                attendance,
                internal_marks,
                assignment_marks,
                previous_score,
                score
            ]
        },
        index=[
            "Attendance",
            "Internal",
            "Assignments",
            "Previous",
            "AI Prediction"
        ]
    )


    st.bar_chart(chart_data)


    # ========================================================
    # RISK DETECTION
    # ========================================================

    st.markdown(
        '<div class="section-title">◈ EARLY WARNING ENGINE</div>',
        unsafe_allow_html=True
    )


    risks = []


    if attendance < 75:

        risks.append(
            "Attendance is below the recommended level."
        )


    if internal_marks < 60:

        risks.append(
            "Internal marks require improvement."
        )


    if assignment_marks < 60:

        risks.append(
            "Assignment performance is below target."
        )


    if study_hours < 2:

        risks.append(
            "Daily study time is low."
        )


    if previous_score < 60:

        risks.append(
            "Previous semester score indicates risk."
        )


    if len(risks) == 0:

        st.success(
            "✓ NO MAJOR RISK SIGNALS DETECTED"
        )

    else:

        for item in risks:

            st.warning(
                "⚠ " + item
            )


    # ========================================================
    # AI RECOMMENDATIONS
    # ========================================================

    st.markdown(
        '<div class="section-title">◈ PERSONALIZED AI STRATEGY</div>',
        unsafe_allow_html=True
    )


    for recommendation in recommendations:

        st.markdown(
            f"""
            <div class="recommendation">

                <span style="
                    color:#00ffaa;
                    font-weight:800;
                ">
                    AI →
                </span>

                {recommendation}

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # WHAT IF SIMULATOR
    # ========================================================

    st.markdown(
        '<div class="section-title">◈ FUTURE SIMULATOR</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="glass">

            <b>WHAT-IF ENGINE</b>

            <br><br>

            Increase attendance and simulate
            a possible future performance.

        </div>
        """,
        unsafe_allow_html=True
    )


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


    improvement = round(
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
            "POTENTIAL",
            f"{improvement:+.1f}%"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        NEXUS AI

        <br><br>

        PREDICT • DETECT • IMPROVE

        <br><br>

        AI STUDENT PERFORMANCE INTELLIGENCE SYSTEM

    </div>
    """,
    unsafe_allow_html=True
)
