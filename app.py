
import streamlit as st
import pandas as pd
import time
import random

from model import (
    predict_score,
    get_risk,
    get_recommendations
)

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="VOID AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       BLACK SPACE BACKGROUND
       ========================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 30%,
                rgba(0,255,190,0.07),
                transparent 25%
            ),
            radial-gradient(
                circle at 20% 80%,
                rgba(70,0,255,0.08),
                transparent 30%
            ),
            #000000;

        color: #ffffff;
    }

    header,
    footer,
    #MainMenu {
        visibility: hidden;
    }


    /* =========================================
       STAR FIELD
       ========================================= */

    .stars {
        position: fixed;
        inset: 0;

        pointer-events: none;

        background-image:
            radial-gradient(#ffffff 1px, transparent 1px),
            radial-gradient(#00ffc3 1px, transparent 1px),
            radial-gradient(#ffffff 1px, transparent 1px);

        background-size:
            120px 120px,
            190px 190px,
            260px 260px;

        background-position:
            10px 20px,
            40px 80px,
            100px 30px;

        opacity: .25;

        animation: starsMove 25s linear infinite;

        z-index: 0;
    }


    @keyframes starsMove {

        from {
            transform: translateY(0);
        }

        to {
            transform: translateY(120px);
        }

    }


    /* =========================================
       TOP BRAND
       ========================================= */

    .brand {

        text-align: center;

        margin-top: 15px;

        font-size: 12px;

        letter-spacing: 8px;

        color: #00ffc3;

        font-weight: 700;

        text-shadow:
            0 0 15px #00ffc3;
    }


    .title {

        text-align: center;

        font-size: 58px;

        font-weight: 900;

        letter-spacing: 7px;

        margin-top: 12px;

        color: #ffffff;

        text-shadow:
            0 0 25px rgba(0,255,195,.25);
    }


    .title span {

        color: #00ffc3;

        text-shadow:
            0 0 30px #00ffc3;
    }


    .subtitle {

        text-align: center;

        color: #555f66;

        letter-spacing: 4px;

        font-size: 11px;

        margin-bottom: 35px;
    }


    /* =========================================
       GLASS PANELS
       ========================================= */

    .panel {

        background:
            linear-gradient(
                145deg,
                rgba(12,14,16,.92),
                rgba(3,4,5,.96)
            );

        border:

            1px solid
            rgba(255,255,255,.08);

        border-radius: 24px;

        padding: 25px;

        box-shadow:
            0 20px 50px rgba(0,0,0,.6);

        transition: .3s;

    }


    .panel:hover {

        border-color:
            rgba(0,255,195,.35);

        box-shadow:
            0 0 35px
            rgba(0,255,195,.07);

        transform:
            translateY(-3px);
    }


    /* =========================================
       SECTION
       ========================================= */

    .section {

        color: #00ffc3;

        font-size: 12px;

        letter-spacing: 4px;

        font-weight: 800;

        margin-top: 28px;

        margin-bottom: 15px;
    }


    /* =========================================
       AI PLANET
       ========================================= */

    .planet {

        width: 220px;

        height: 220px;

        margin: 10px auto 25px auto;

        border-radius: 50%;

        position: relative;

        display: flex;

        justify-content: center;

        align-items: center;

        background:

            radial-gradient(
                circle at 35% 30%,
                #23ffe0,
                #064c40 15%,
                #011713 35%,
                #000000 70%
            );

        border:
            2px solid
            rgba(0,255,195,.8);

        box-shadow:

            0 0 30px
            rgba(0,255,195,.6),

            0 0 100px
            rgba(0,255,195,.18),

            inset 0 0 40px
            rgba(0,255,195,.4);

        animation:
            planetPulse 4s ease-in-out infinite;
    }


    .planet:before {

        content: "";

        position: absolute;

        width: 290px;

        height: 90px;

        border-radius: 50%;

        border:
            1px solid
            rgba(0,255,195,.7);

        transform:
            rotate(-18deg);

        box-shadow:
            0 0 20px
            rgba(0,255,195,.15);

        animation:
            orbit 6s linear infinite;
    }


    .planet:after {

        content: "";

        position: absolute;

        width: 340px;

        height: 110px;

        border-radius: 50%;

        border:
            1px dashed
            rgba(80,100,255,.35);

        transform:
            rotate(35deg);

        animation:
            reverseOrbit 10s linear infinite;
    }


    @keyframes planetPulse {

        0%,100% {

            transform:
                scale(.94);

        }

        50% {

            transform:
                scale(1.05);

        }

    }


    @keyframes orbit {

        from {

            transform:
                rotate(-18deg)
                rotate(0deg);

        }

        to {

            transform:
                rotate(-18deg)
                rotate(360deg);

        }

    }


    @keyframes reverseOrbit {

        from {

            transform:
                rotate(35deg)
                rotate(360deg);

        }

        to {

            transform:
                rotate(35deg)
                rotate(0deg);

        }

    }


    .planet-text {

        text-align: center;

        font-size: 14px;

        font-weight: 900;

        letter-spacing: 4px;

        color: white;

        text-shadow:
            0 0 15px #00ffc3;
    }


    /* =========================================
       SCORE
       ========================================= */

    .score {

        text-align: center;

        font-size: 60px;

        font-weight: 900;

        color: #00ffc3;

        text-shadow:
            0 0 30px #00ffc3;

        animation:
            scoreGlow 2s infinite;
    }


    @keyframes scoreGlow {

        0%,100% {

            text-shadow:
                0 0 15px #00ffc3;

        }

        50% {

            text-shadow:
                0 0 40px #00ffc3;

        }

    }


    .score-label {

        text-align: center;

        color: #58636a;

        letter-spacing: 4px;

        font-size: 9px;
    }


    /* =========================================
       METRICS
       ========================================= */

    .metric {

        background:
            rgba(8,10,12,.9);

        border:
            1px solid
            rgba(255,255,255,.07);

        border-radius: 18px;

        padding: 20px;

        text-align: center;

        transition: .3s;
    }


    .metric:hover {

        border-color:
            #00ffc3;

        box-shadow:
            0 0 25px
            rgba(0,255,195,.12);

    }


    .metric-title {

        color: #59636b;

        font-size: 9px;

        letter-spacing: 3px;
    }


    .metric-value {

        font-size: 25px;

        font-weight: 900;

        margin-top: 8px;

        color: #ffffff;
    }


    /* =========================================
       SCANNER
       ========================================= */

    .scanner {

        height: 6px;

        width: 100%;

        background: #081012;

        border-radius: 10px;

        overflow: hidden;

        margin-top: 15px;
    }


    .scanner-line {

        height: 100%;

        width: 30%;

        background:
            linear-gradient(
                90deg,
                transparent,
                #00ffc3,
                transparent
            );

        box-shadow:
            0 0 15px #00ffc3;

        animation:
            scan 2s linear infinite;
    }


    @keyframes scan {

        from {

            transform:
                translateX(-150%);

        }

        to {

            transform:
                translateX(450%);

        }

    }


    /* =========================================
       RECOMMENDATIONS
       ========================================= */

    .advice {

        padding: 16px;

        border-radius: 12px;

        margin-bottom: 10px;

        background:
            rgba(8,12,14,.9);

        border-left:
            3px solid
            #00ffc3;

        transition: .25s;
    }


    .advice:hover {

        transform:
            translateX(7px);

        background:
            rgba(0,255,195,.04);
    }


    /* =========================================
       BUTTON
       ========================================= */

    .stButton > button {

        width: 100%;

        height: 58px;

        border-radius: 16px;

        background:
            linear-gradient(
                90deg,
                #00ffc3,
                #00aaff
            );

        border: none;

        color: #00100c;

        font-size: 13px;

        font-weight: 900;

        letter-spacing: 3px;

        transition: .3s;

    }


    .stButton > button:hover {

        transform:
            translateY(-3px)
            scale(1.01);

        box-shadow:
            0 0 35px
            rgba(0,255,195,.5);

    }


    /* =========================================
       FOOTER
       ========================================= */

    .footer {

        text-align: center;

        color: #30383e;

        font-size: 9px;

        letter-spacing: 5px;

        padding: 45px;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STAR FIELD
# =========================================================

st.markdown(
    '<div class="stars"></div>',
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="brand">◈ ARTIFICIAL INTELLIGENCE LAB ◈</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title">VOID <span>AI</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">STUDENT PERFORMANCE PREDICTION SYSTEM</div>',
    unsafe_allow_html=True
)


# =========================================================
# LIVE STATUS
# =========================================================

status1, status2, status3, status4 = st.columns(4)

with status1:
    st.metric("AI CORE", "ONLINE")

with status2:
    st.metric("MODEL", "RF-01")

with status3:
    st.metric("ENGINE", "ACTIVE")

with status4:
    st.metric("MODE", "PREDICT")


# =========================================================
# INPUT
# =========================================================

st.markdown(
    '<div class="section">◈ ENTER STUDENT DATA</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2)


with left:

    student_name = st.text_input(
        "Student ID / Name",
        placeholder="e.g. ARMAAN"
    )

    attendance = st.slider(
        "Attendance %",
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

    assignments = st.slider(
        "Assignment Marks",
        0,
        100,
        75
    )

    study_hours = st.number_input(
        "Daily Study Hours",
        min_value=0.0,
        max_value=15.0,
        value=3.0,
        step=.5
    )

    previous = st.slider(
        "Previous Score",
        0,
        100,
        70
    )


st.write("")


# =========================================================
# START
# =========================================================

start = st.button(
    "✦ LAUNCH PREDICTION ENGINE"
)


if start:

    student = (
        student_name.strip()
        if student_name.strip()
        else "STUDENT-001"
    )


    # =====================================================
    # SCANNING ANIMATION
    # =====================================================

    animation = st.empty()


    messages = [

        "CONNECTING TO VOID AI",

        "LOCKING STUDENT PROFILE",

        "SCANNING ACADEMIC DATA",

        "EXTRACTING PERFORMANCE FEATURES",

        "RUNNING RANDOM FOREST",

        "CALCULATING RISK PROBABILITY",

        "BUILDING FUTURE SCENARIO",

        "AI ANALYSIS COMPLETE"

    ]


    for message in messages:

        animation.markdown(
            f"""
            <div class="panel">

                <div style="
                    color:#00ffc3;
                    font-family:monospace;
                    letter-spacing:2px;
                ">

                ◉ SYSTEM &gt; {message}

                </div>

                <div class="scanner">

                    <div class="scanner-line"></div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(.35)


    animation.empty()


    # =====================================================
    # PREDICTION
    # =====================================================

    score = predict_score(
        attendance,
        internal,
        assignments,
        study_hours,
        previous
    )


    risk = get_risk(score)


    recommendations = get_recommendations(
        attendance,
        internal,
        assignments,
        study_hours,
        previous
    )


    # =====================================================
    # AI CORE
    # =====================================================

    st.markdown(
        '<div class="section">◈ NEURAL PLANET</div>',
        unsafe_allow_html=True
    )


    a, b, c = st.columns([1,2,1])


    with b:

        st.markdown(
            """
            <div class="panel">

                <div class="planet">

                    <div class="planet-text">

                        VOID AI

                        <br>

                        <span style="
                            color:#69757d;
                            font-size:9px;
                            letter-spacing:2px;
                        ">
                            NEURAL CORE
                        </span>

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f'<div class="score">{score}%</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="score-label">PREDICTED PERFORMANCE</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # RESULT
    # =====================================================

    st.markdown(
        '<div class="section">◈ AI DECISION</div>',
        unsafe_allow_html=True
    )


    if risk == "LOW":

        risk_text = "🟢 LOW"

    elif risk == "MEDIUM":

        risk_text = "🟡 MEDIUM"

    else:

        risk_text = "🔴 HIGH"


    if score >= 85:

        performance = "🏆 EXCELLENT"

    elif score >= 75:

        performance = "⭐ GOOD"

    elif score >= 60:

        performance = "📘 AVERAGE"

    else:

        performance = "⚠️ CRITICAL"


    c1, c2, c3 = st.columns(3)


    with c1:

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


    with c2:

        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-title">
                    RISK LEVEL
                </div>

                <div class="metric-value">
                    {risk_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-title">
                    PERFORMANCE
                </div>

                <div class="metric-value">
                    {performance}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # GRAPH
    # =====================================================

    st.markdown(
        '<div class="section">◈ ACADEMIC ENERGY MAP</div>',
        unsafe_allow_html=True
    )


    graph = pd.DataFrame({

        "Performance": [

            attendance,

            internal,

            assignments,

            previous,

            score

        ]

    }, index=[

        "Attendance",

        "Internal",

        "Assignments",

        "Previous",

        "AI Prediction"

    ])


    st.bar_chart(graph)


    # =====================================================
    # RISK ENGINE
    # =====================================================

    st.markdown(
        '<div class="section">◈ THREAT DETECTION</div>',
        unsafe_allow_html=True
    )


    warnings = []


    if attendance < 75:

        warnings.append(
            "Attendance anomaly detected"
        )


    if internal < 60:

        warnings.append(
            "Low internal assessment signal"
        )


    if assignments < 60:

        warnings.append(
            "Assignment performance anomaly"
        )


    if study_hours < 2:

        warnings.append(
            "Insufficient study-time signal"
        )


    if previous < 60:

        warnings.append(
            "Historical performance risk"
        )


    if warnings:

        for warning in warnings:

            st.warning(
                "⚠ " + warning
            )

    else:

        st.success(
            "✓ NO HIGH-RISK SIGNALS DETECTED"
        )


    # =====================================================
    # AI ADVISOR
    # =====================================================

    st.markdown(
        '<div class="section">◈ AI MISSION PLAN</div>',
        unsafe_allow_html=True
    )


    for recommendation in recommendations:

        st.markdown(
            f"""
            <div class="advice">

                <span style="
                    color:#00ffc3;
                    font-weight:900;
                ">
                AI →
                </span>

                {recommendation}

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # FUTURE
    # =====================================================

    st.markdown(
        '<div class="section">◈ FUTURE SIMULATION</div>',
        unsafe_allow_html=True
    )


    future = st.slider(
        "Simulate Improved Attendance",
        int(attendance),
        100,
        min(95, int(attendance + 10))
    )


    future_score = predict_score(
        future,
        internal,
        assignments,
        study_hours,
        previous
    )


    gain = round(
        future_score - score,
        1
    )


    f1, f2, f3 = st.columns(3)


    with f1:

        st.metric(
            "CURRENT",
            f"{score}%"
        )


    with f2:

        st.metric(
            "FUTURE",
            f"{future_score}%"
        )


    with f3:

        st.metric(
            "POTENTIAL GAIN",
            f"{gain:+.1f}%"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        VOID AI

        <br><br>

        PREDICT • DETECT • SIMULATE • IMPROVE

        <br><br>

        STUDENT PERFORMANCE INTELLIGENCE

    </div>
    """,
    unsafe_allow_html=True
)
