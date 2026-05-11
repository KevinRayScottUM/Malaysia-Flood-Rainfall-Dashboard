from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# 1) Page config
# =========================================================
st.set_page_config(
    page_title="Malaysia Rainfall & Flood Risk Dashboard",
    layout="wide",
    initial_sidebar_state="auto",
)

APP_DIR = Path(__file__).parent
CSV_PATH = APP_DIR / "malaysia_chirps_2000_2026_city_rainfall_clean_eda.csv"
MAIN_CSV_NAME = "malaysia_chirps_2000_2026_city_rainfall_clean_eda.csv"


# =========================================================
# 2) Custom CSS
# =========================================================
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* Make Plotly charts and Streamlit widgets more comfortable on touch screens. */
    div[data-testid="stSidebar"] button,
    div[data-testid="stSidebar"] label,
    div[data-testid="stSidebar"] input,
    div[data-testid="stSidebar"] textarea,
    div[data-testid="stSidebar"] [role="button"] {
        min-height: 36px;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(0,0,0,0.05);
        border-radius: 14px;
        padding: 10px 12px;
    }

    /* Mobile responsive layout */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.8rem 0.7rem 1.5rem 0.7rem;
        }

        h1 {
            font-size: 1.45rem !important;
            line-height: 1.22 !important;
        }

        h2 {
            font-size: 1.15rem !important;
        }

        h3 {
            font-size: 1.02rem !important;
        }

        p, label, span, div {
            font-size: 0.92rem;
        }

        section[data-testid="stSidebar"] {
            width: 92vw !important;
            min-width: 92vw !important;
        }

        div[data-testid="stSidebarContent"] {
            padding: 1rem 0.8rem;
        }

        div[data-baseweb="select"] {
            font-size: 0.9rem;
        }

        div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
            max-width: 135px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        div[data-testid="stSlider"] {
            padding-top: 0.2rem;
            padding-bottom: 0.6rem;
        }

        div[data-testid="stMetric"] {
            padding: 8px 10px;
            margin-bottom: 0.35rem;
        }

        .js-plotly-plot .plotly .modebar {
            transform: scale(0.82);
            transform-origin: top right;
        }

        iframe {
            max-width: 100% !important;
        }
    }


    /* =====================================================
       iOS 26 / Liquid Glass inspired UI skin
       ===================================================== */
    :root {
        --glass-bg: rgba(255, 255, 255, 0.58);
        --glass-bg-strong: rgba(255, 255, 255, 0.74);
        --glass-border: rgba(255, 255, 255, 0.62);
        --glass-shadow: 0 18px 48px rgba(31, 38, 135, 0.18);
        --glass-inner: inset 0 1px 0 rgba(255,255,255,0.80), inset 0 -1px 0 rgba(255,255,255,0.24);
        --ios-red: #007AFF;
        --ios-blue: #007AFF;
        --ios-purple: #d45af3;
        --ios-yellow: #fff02e;
    }

    html, body, .stApp {
        background:
            radial-gradient(circle at 18% 10%, rgba(67, 169, 255, 0.22), transparent 30%),
            radial-gradient(circle at 88% 2%, rgba(255, 83, 201, 0.16), transparent 28%),
            linear-gradient(135deg, #f7fbff 0%, #eef4fb 46%, #f8fbff 100%) !important;
    }

    .main, [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(20, 22, 32, 0.72) !important;
        backdrop-filter: blur(28px) saturate(170%);
        -webkit-backdrop-filter: blur(28px) saturate(170%);
        border-right: 1px solid rgba(255,255,255,0.12);
    }

    section[data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.94);
    }

    div[data-testid="stSidebarContent"] {
        background:
            radial-gradient(circle at 20% 0%, rgba(80, 180, 255, 0.18), transparent 24%),
            radial-gradient(circle at 95% 28%, rgba(255, 75, 190, 0.13), transparent 26%);
    }

    .metric-card,
    div[data-testid="stMetric"],
    div[data-testid="stAlert"],
    div[data-testid="stDataFrame"],
    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 24px !important;
        box-shadow: var(--glass-shadow), var(--glass-inner) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    }

    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) {
        padding: 14px 14px 6px 14px;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: rgba(255,255,255,0.96) !important;
        text-shadow: 0 1px 10px rgba(0,0,0,0.20);
    }

    div[data-testid="stMetric"] {
        background:
            linear-gradient(135deg, rgba(255,255,255,0.34), rgba(255,255,255,0.12)),
            radial-gradient(circle at 0% 0%, rgba(255,255,255,0.44), transparent 45%) !important;
    }

    .stButton > button,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primary"],
    button[kind="secondary"] {
        border: 1px solid rgba(255,255,255,0.62) !important;
        border-radius: 999px !important;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.78), rgba(255,255,255,0.32)),
            radial-gradient(circle at 20% 15%, rgba(255,255,255,0.92), transparent 35%) !important;
        color: #111827 !important;
        box-shadow: 0 14px 36px rgba(31,38,135,0.18), inset 0 1px 0 rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(22px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(22px) saturate(180%) !important;
        transition: transform 160ms ease, box-shadow 160ms ease, background 160ms ease !important;
        font-weight: 750 !important;
    }

    .stButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover {
        transform: translateY(-1px) scale(1.015);
        box-shadow: 0 18px 44px rgba(31,38,135,0.24), inset 0 1px 0 rgba(255,255,255,0.95) !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    div[data-testid="stSlider"] [role="slider"] {
        border-radius: 18px !important;
        background: rgba(255,255,255,0.10) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.18) !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background: rgba(0, 122, 255, 0.92) !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(0,122,255,0.24) !important;
    }

    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {
        border-radius: 999px;
    }

    .js-plotly-plot .updatemenu-item-rect,
    .js-plotly-plot .slider-container .slider-bg {
        fill: rgba(255,255,255,0.62) !important;
        stroke: rgba(255,255,255,0.78) !important;
        filter: drop-shadow(0 10px 22px rgba(31,38,135,0.18));
    }

    .glass-caption {
        padding: 14px 18px;
        border-radius: 22px;
        background: rgba(255,255,255,0.58);
        border: 1px solid rgba(255,255,255,0.65);
        box-shadow: 0 16px 42px rgba(31,38,135,0.16), inset 0 1px 0 rgba(255,255,255,0.75);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        margin: 8px 0 16px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 2.1) High-contrast liquid-glass override
#     The previous white glass skin made map titles, legends and
#     Plotly controls unreadable on deployed Streamlit. This layer
#     keeps the glass feeling but forces readable contrast.
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --tt-bg-0: #070913;
        --tt-bg-1: #101827;
        --tt-panel: rgba(18, 24, 38, 0.76);
        --tt-panel-soft: rgba(24, 32, 48, 0.62);
        --tt-panel-strong: rgba(15, 23, 42, 0.88);
        --tt-border: rgba(255, 255, 255, 0.20);
        --tt-text: #f8fafc;
        --tt-muted: rgba(226, 232, 240, 0.78);
        --tt-accent: #007AFF;
        --tt-blue: #007AFF;
        --tt-purple: #d946ef;
        --tt-yellow: #fde047;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 18% 8%, rgba(0, 122, 255, 0.22), transparent 34%),
            radial-gradient(circle at 88% 12%, rgba(217, 70, 239, 0.18), transparent 30%),
            linear-gradient(135deg, var(--tt-bg-0) 0%, var(--tt-bg-1) 55%, #07111f 100%) !important;
        color: var(--tt-text) !important;
    }

    .main, .block-container, h1, h2, h3, h4, p, label, span, div {
        color: var(--tt-text);
    }

    .block-container {
        max-width: 1500px;
    }

    [data-testid="stHeader"] {
        background: rgba(7, 9, 19, 0.72) !important;
        backdrop-filter: blur(22px) saturate(160%);
        -webkit-backdrop-filter: blur(22px) saturate(160%);
    }

    section[data-testid="stSidebar"] {
        background: rgba(17, 24, 39, 0.86) !important;
        border-right: 1px solid rgba(255,255,255,0.18) !important;
        box-shadow: 16px 0 42px rgba(0,0,0,0.28);
    }

    section[data-testid="stSidebar"] * {
        color: var(--tt-text) !important;
        text-shadow: none !important;
    }

    div[data-testid="stSidebarContent"] {
        background:
            radial-gradient(circle at 0% 0%, rgba(0, 122, 255, 0.18), transparent 34%),
            radial-gradient(circle at 100% 32%, rgba(217, 70, 239, 0.14), transparent 32%) !important;
    }

    .metric-card,
    div[data-testid="stMetric"],
    div[data-testid="stAlert"],
    div[data-testid="stDataFrame"],
    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) {
        background:
            linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.055)),
            var(--tt-panel) !important;
        border: 1px solid var(--tt-border) !important;
        border-radius: 26px !important;
        box-shadow: 0 22px 58px rgba(0,0,0,0.30), inset 0 1px 0 rgba(255,255,255,0.22) !important;
        backdrop-filter: blur(22px) saturate(165%) !important;
        -webkit-backdrop-filter: blur(22px) saturate(165%) !important;
    }

    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) {
        padding: 16px 16px 8px 16px;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: var(--tt-text) !important;
        text-shadow: none !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 850 !important;
    }

    .stButton > button,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primary"],
    button[kind="secondary"] {
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.32) !important;
        border-radius: 999px !important;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.22), rgba(255,255,255,0.08)),
            radial-gradient(circle at 20% 15%, rgba(255,255,255,0.28), transparent 36%) !important;
        box-shadow: 0 14px 34px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.34) !important;
        backdrop-filter: blur(18px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
        font-weight: 800 !important;
    }

    .stButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-1px) scale(1.018);
        border-color: rgba(255,255,255,0.55) !important;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.30), rgba(255,255,255,0.12)),
            radial-gradient(circle at 22% 15%, rgba(255,255,255,0.38), transparent 38%) !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        background: rgba(9, 12, 22, 0.48) !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        border-radius: 18px !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background: rgba(0, 122, 255, 0.95) !important;
        color: #ffffff !important;
        border-radius: 11px !important;
    }

    [data-testid="stRadio"] label, [data-testid="stCheckbox"] label {
        color: var(--tt-text) !important;
    }

    .glass-caption {
        color: var(--tt-text) !important;
        background: rgba(15, 23, 42, 0.72) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        box-shadow: 0 18px 44px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.22) !important;
    }

    /* Plotly text/controls need explicit dark-panel contrast on Streamlit Cloud. */
    .js-plotly-plot .plotly text {
        fill: #f8fafc !important;
    }
    .js-plotly-plot .modebar {
        background: rgba(15, 23, 42, 0.76) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }
    .js-plotly-plot .modebar-btn svg path {
        fill: #f8fafc !important;
    }

    /* Plotly animation buttons: default should look calm, not permanently hovered/selected. */
    .js-plotly-plot .updatemenu-item-rect {
        fill: rgba(15, 23, 42, 0.42) !important;
        stroke: rgba(255, 255, 255, 0.26) !important;
        filter: none !important;
    }
    .js-plotly-plot .updatemenu-item-text {
        fill: #f8fafc !important;
        font-weight: 650 !important;
    }
    .js-plotly-plot .slider-bg {
        fill: rgba(15, 23, 42, 0.25) !important;
        stroke: rgba(255,255,255,0.28) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)




# =========================================================
# 2.2) Anti-flicker rendering patch
#     The liquid-glass skin is beautiful, but backdrop-filter +
#     Plotly Mapbox hover/modebar repaint can make Chromium/Safari
#     flash on every mouse movement. This override keeps the overall
#     design while removing GPU-expensive effects only around charts.
# =========================================================
st.markdown(
    """
    <style>
    /* Do not blur the Plotly container itself. Mapbox already uses a GPU canvas;
       putting backdrop-filter over/around that canvas causes full-layer repaint
       when the mouse moves, when the modebar appears, or when hover labels update. */
    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) {
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        background: rgba(18, 24, 38, 0.82) !important;
        box-shadow: 0 18px 44px rgba(0,0,0,0.26), inset 0 1px 0 rgba(255,255,255,0.14) !important;
        transform: translateZ(0);
        contain: paint;
    }

    /* Plotly's modebar normally appears/disappears on hover. That DOM change is
       one common reason the whole map looks like it is flashing. We already have
       Start/Pause/Reset controls inside the figure, so the floating modebar is disabled. */
    .js-plotly-plot .modebar,
    .js-plotly-plot .modebar-container {
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Avoid expensive hover transforms on Streamlit buttons while the map is nearby. */
    .stButton > button,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primary"],
    button[kind="secondary"] {
        transition: none !important;
        transform: none !important;
    }
    .stButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover {
        transform: none !important;
    }

    /* Streamlit can briefly show a running overlay/status during reruns. Keep it
       visually quiet instead of a strong flash. */
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"] {
        opacity: 0.18 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# =========================================================
# 2.3) Final iOS #007AFF liquid-glass polish
#      This layer intentionally comes last so it overrides the
#      earlier red accent and gives the marked areas a consistent
#      blue liquid-glass look.
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ios-blue: #007AFF;
        --ios-blue-rgb: 0, 122, 255;
        --ios-blue-soft: rgba(0, 122, 255, 0.18);
        --ios-blue-mid: rgba(0, 122, 255, 0.42);
        --ios-blue-strong: rgba(0, 122, 255, 0.92);
        --liquid-surface: rgba(16, 24, 39, 0.58);
        --liquid-surface-2: rgba(25, 34, 52, 0.66);
        --liquid-border: rgba(255, 255, 255, 0.24);
        --liquid-border-blue: rgba(0, 122, 255, 0.52);
        --liquid-highlight: rgba(255, 255, 255, 0.34);
        --liquid-shadow: 0 22px 58px rgba(0, 0, 0, 0.34), 0 0 34px rgba(0, 122, 255, 0.13);
    }

    /* Global background: keep the dark premium tone but make the main accent pure iOS blue. */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 12% 8%, rgba(var(--ios-blue-rgb), 0.26), transparent 32%),
            radial-gradient(circle at 88% 4%, rgba(var(--ios-blue-rgb), 0.13), transparent 28%),
            radial-gradient(circle at 78% 74%, rgba(255,255,255,0.055), transparent 34%),
            linear-gradient(135deg, #050914 0%, #071426 45%, #08101d 100%) !important;
    }

    /* Red-circled status/info area. */
    div[data-testid="stAlert"] {
        position: relative !important;
        overflow: hidden !important;
        border-radius: 26px !important;
        border: 1px solid rgba(var(--ios-blue-rgb), 0.50) !important;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.055)),
            radial-gradient(circle at 0% 0%, rgba(var(--ios-blue-rgb), 0.38), transparent 44%),
            rgba(17, 26, 42, 0.70) !important;
        box-shadow: var(--liquid-shadow), inset 0 1px 0 rgba(255,255,255,0.30) !important;
        backdrop-filter: blur(26px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(26px) saturate(180%) !important;
    }
    div[data-testid="stAlert"]::before {
        content: "";
        position: absolute;
        inset: 1px 1px auto 1px;
        height: 48%;
        pointer-events: none;
        border-radius: 25px 25px 18px 18px;
        background: linear-gradient(180deg, rgba(255,255,255,0.22), rgba(255,255,255,0.00));
    }

    /* Red-circled KPI cards. */
    div[data-testid="stMetric"] {
        position: relative !important;
        overflow: hidden !important;
        min-height: 96px !important;
        padding: 18px 18px !important;
        border-radius: 28px !important;
        border: 1px solid rgba(255,255,255,0.24) !important;
        background:
            radial-gradient(circle at 16% 0%, rgba(255,255,255,0.30), transparent 36%),
            radial-gradient(circle at 92% 18%, rgba(var(--ios-blue-rgb), 0.30), transparent 42%),
            linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.060)),
            rgba(16, 24, 39, 0.72) !important;
        box-shadow: var(--liquid-shadow), inset 0 1px 0 rgba(255,255,255,0.27), inset 0 -1px 0 rgba(255,255,255,0.06) !important;
        backdrop-filter: blur(28px) saturate(185%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(185%) !important;
    }
    div[data-testid="stMetric"]::after {
        content: "";
        position: absolute;
        left: 12px;
        right: 12px;
        top: 8px;
        height: 28px;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(255,255,255,0.24), rgba(255,255,255,0.04));
        pointer-events: none;
        opacity: 0.75;
    }
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: rgba(238, 246, 255, 0.90) !important;
        font-weight: 720 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 900 !important;
        letter-spacing: -0.045em !important;
        text-shadow: 0 0 24px rgba(var(--ios-blue-rgb), 0.20) !important;
    }

    /* Red-circled chart panels: glass border/highlight, but no backdrop blur on Plotly canvas itself. */
    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) {
        position: relative !important;
        overflow: hidden !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        background:
            radial-gradient(circle at 18% 0%, rgba(var(--ios-blue-rgb), 0.16), transparent 34%),
            linear-gradient(135deg, rgba(255,255,255,0.11), rgba(255,255,255,0.040)),
            rgba(9, 15, 28, 0.86) !important;
        box-shadow: 0 24px 68px rgba(0,0,0,0.36), 0 0 38px rgba(var(--ios-blue-rgb),0.10), inset 0 1px 0 rgba(255,255,255,0.18) !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        contain: paint;
    }
    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot)::before {
        content: "";
        position: absolute;
        z-index: 0;
        inset: 1px 1px auto 1px;
        height: 90px;
        border-radius: 29px 29px 18px 18px;
        background: linear-gradient(180deg, rgba(255,255,255,0.12), rgba(255,255,255,0.00));
        pointer-events: none;
    }
    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) > * {
        position: relative;
        z-index: 1;
    }

    /* Sidebar glass panel and controls. */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 0% 8%, rgba(var(--ios-blue-rgb), 0.24), transparent 32%),
            radial-gradient(circle at 100% 36%, rgba(var(--ios-blue-rgb), 0.16), transparent 30%),
            rgba(8, 13, 26, 0.86) !important;
        border-right: 1px solid rgba(var(--ios-blue-rgb), 0.24) !important;
        box-shadow: 18px 0 48px rgba(0,0,0,0.36), inset -1px 0 0 rgba(255,255,255,0.06) !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        border-radius: 22px !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.13), rgba(255,255,255,0.045)),
            rgba(10, 16, 31, 0.68) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.18), 0 10px 24px rgba(0,0,0,0.18) !important;
        backdrop-filter: blur(18px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
        border-radius: 999px !important;
        background:
            linear-gradient(135deg, rgba(var(--ios-blue-rgb), 0.98), rgba(30, 144, 255, 0.78)),
            radial-gradient(circle at 24% 18%, rgba(255,255,255,0.42), transparent 36%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.28) !important;
        box-shadow: 0 9px 24px rgba(var(--ios-blue-rgb),0.28), inset 0 1px 0 rgba(255,255,255,0.32) !important;
    }

    /* iOS-blue slider/radio/checkbox accents. */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:nth-child(2) {
        background: rgba(255,255,255,0.18) !important;
    }
    div[data-testid="stSlider"] [role="slider"] {
        background: #ffffff !important;
        border: 2px solid rgba(var(--ios-blue-rgb), 0.95) !important;
        box-shadow: 0 0 0 5px rgba(var(--ios-blue-rgb), 0.15), 0 8px 18px rgba(0,0,0,0.28) !important;
    }
    [data-testid="stRadio"] label:has(input:checked),
    [data-testid="stCheckbox"] label:has(input:checked) {
        color: #ffffff !important;
    }
    [data-testid="stRadio"] input:checked + div,
    [data-testid="stCheckbox"] input:checked + div {
        border-color: rgba(var(--ios-blue-rgb), 0.95) !important;
        background-color: rgba(var(--ios-blue-rgb), 0.95) !important;
    }

    /* Liquid-glass buttons: Apply update and all Streamlit buttons. */
    .stButton > button,
    div[data-testid="stDownloadButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primary"],
    button[kind="secondary"] {
        position: relative !important;
        overflow: hidden !important;
        min-height: 48px !important;
        border-radius: 999px !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.34) !important;
        background:
            radial-gradient(circle at 22% 18%, rgba(255,255,255,0.42), transparent 30%),
            linear-gradient(135deg, rgba(var(--ios-blue-rgb), 0.95), rgba(var(--ios-blue-rgb), 0.52) 58%, rgba(255,255,255,0.16)) !important;
        box-shadow:
            0 18px 38px rgba(var(--ios-blue-rgb),0.26),
            0 12px 28px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.46),
            inset 0 -1px 0 rgba(255,255,255,0.12) !important;
        backdrop-filter: blur(22px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(22px) saturate(190%) !important;
        font-weight: 850 !important;
        letter-spacing: -0.01em !important;
        transition: filter 160ms ease, box-shadow 160ms ease, border-color 160ms ease !important;
        transform: none !important;
    }
    .stButton > button::before,
    div[data-testid="stDownloadButton"] > button::before,
    div[data-testid="stFormSubmitButton"] > button::before,
    button[kind="primary"]::before,
    button[kind="secondary"]::before {
        content: "";
        position: absolute;
        inset: 1px 2px auto 2px;
        height: 48%;
        border-radius: 999px;
        background: linear-gradient(180deg, rgba(255,255,255,0.38), rgba(255,255,255,0.03));
        pointer-events: none;
    }
    .stButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover {
        filter: brightness(1.08) saturate(1.08) !important;
        border-color: rgba(255,255,255,0.54) !important;
        box-shadow:
            0 22px 46px rgba(var(--ios-blue-rgb),0.34),
            0 14px 30px rgba(0,0,0,0.34),
            inset 0 1px 0 rgba(255,255,255,0.56) !important;
        transform: none !important;
    }
    .stButton > button:active,
    div[data-testid="stDownloadButton"] > button:active,
    div[data-testid="stFormSubmitButton"] > button:active,
    button[kind="primary"]:active,
    button[kind="secondary"]:active {
        filter: brightness(0.96) !important;
        box-shadow: 0 10px 24px rgba(var(--ios-blue-rgb),0.22), inset 0 2px 8px rgba(0,0,0,0.18) !important;
    }

    /* Plotly timeline controls use the same blue glass language. */
    .js-plotly-plot .updatemenu-item-rect {
        fill: rgba(0, 122, 255, 0.22) !important;
        stroke: rgba(255,255,255,0.30) !important;
    }
    .js-plotly-plot .slider-bg {
        fill: rgba(0, 122, 255, 0.16) !important;
        stroke: rgba(255,255,255,0.28) !important;
    }
    .js-plotly-plot .slider-grip-rect,
    .js-plotly-plot .slider-handle {
        fill: #007AFF !important;
        stroke: rgba(255,255,255,0.68) !important;
    }

    .glass-caption {
        position: relative !important;
        overflow: hidden !important;
        border-radius: 26px !important;
        border: 1px solid rgba(var(--ios-blue-rgb), 0.44) !important;
        background:
            radial-gradient(circle at 0% 0%, rgba(var(--ios-blue-rgb), 0.28), transparent 44%),
            linear-gradient(135deg, rgba(255,255,255,0.13), rgba(255,255,255,0.055)),
            rgba(13, 22, 39, 0.72) !important;
        box-shadow: var(--liquid-shadow), inset 0 1px 0 rgba(255,255,255,0.24) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    }
    .glass-caption::before {
        content: "";
        position: absolute;
        inset: 1px 2px auto 2px;
        height: 42%;
        border-radius: 24px 24px 16px 16px;
        background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0));
        pointer-events: none;
    }

    /* Mobile keeps the same look without becoming too heavy. */
    @media (max-width: 768px) {
        div[data-testid="stMetric"] { min-height: 82px !important; border-radius: 24px !important; }
        .stButton > button, div[data-testid="stFormSubmitButton"] > button { min-height: 44px !important; }
        div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) { border-radius: 24px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 2.4) Readability + scroll-reactive liquid glass correction
#      Fixes: unreadable Plotly hover/legend boxes, blue text-fill
#      selection on sidebar choices, and makes glass panels visually
#      pick up the changing fixed background while scrolling.
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ios-blue: #007AFF;
        --ios-blue-rgb: 0, 122, 255;
        --page-text: #F8FAFC;
        --page-muted: rgba(226,232,240,0.82);
        --glass-dark: rgba(8, 13, 26, 0.50);
        --glass-dark-strong: rgba(8, 13, 26, 0.72);
        --glass-line: rgba(255,255,255,0.20);
    }

    /* Fixed scenic background: transparent glass cards move over this while scrolling,
       so the perceived color under the glass changes instead of looking like a flat card. */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-image:
            radial-gradient(circle at 12% 8%, rgba(var(--ios-blue-rgb), 0.36), transparent 30%),
            radial-gradient(circle at 86% 12%, rgba(90, 200, 250, 0.22), transparent 28%),
            radial-gradient(circle at 18% 58%, rgba(48, 209, 88, 0.10), transparent 30%),
            radial-gradient(circle at 74% 82%, rgba(191, 90, 242, 0.16), transparent 32%),
            linear-gradient(135deg, #030712 0%, #071426 44%, #06101d 100%) !important;
        background-attachment: fixed !important;
        background-size: 150% 150%, 145% 145%, 135% 135%, 150% 150%, cover !important;
        color: var(--page-text) !important;
    }

    /* A very soft moving light field behind the content. It is fixed, not attached to cards,
       so scrolling creates the 'glass over changing scene' feeling. */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        background:
            linear-gradient(115deg, transparent 0%, rgba(255,255,255,0.050) 34%, transparent 62%),
            radial-gradient(circle at 50% 0%, rgba(255,255,255,0.045), transparent 34%);
        mix-blend-mode: screen;
    }
    [data-testid="stAppViewContainer"] > .main { position: relative; z-index: 1; }

    /* Strong, readable typography everywhere on glass. */
    .block-container, .block-container p, .block-container span, .block-container label,
    .block-container div, .block-container h1, .block-container h2, .block-container h3 {
        color: var(--page-text) !important;
        text-shadow: 0 1px 12px rgba(0,0,0,0.22);
    }

    /* Sidebar: no ugly blue text-fill blocks when an option is selected/focused.
       Keep only the small native radio/checkbox indicator plus a subtle row glow. */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
        background: transparent !important;
        box-shadow: none !important;
        border: 1px solid transparent !important;
        border-radius: 14px !important;
        padding: 4px 6px !important;
        user-select: none !important;
        -webkit-user-select: none !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked),
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label:has(input:checked) {
        background: rgba(var(--ios-blue-rgb), 0.10) !important;
        border-color: rgba(var(--ios-blue-rgb), 0.30) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.10) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label span,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label span,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label p,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
        background: transparent !important;
        color: rgba(248,250,252,0.96) !important;
        text-shadow: none !important;
    }
    section[data-testid="stSidebar"] ::selection {
        background: rgba(var(--ios-blue-rgb), 0.22) !important;
        color: #ffffff !important;
    }

    /* Make selected multiselect tags blue glass, but keep text readable and avoid flat plastic look. */
    div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background:
            linear-gradient(135deg, rgba(0,122,255,0.78), rgba(90,200,250,0.42)),
            radial-gradient(circle at 20% 15%, rgba(255,255,255,0.34), transparent 35%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.24) !important;
        box-shadow: 0 8px 20px rgba(0,122,255,0.22), inset 0 1px 0 rgba(255,255,255,0.28) !important;
    }

    /* Liquid glass panels: less opaque so the fixed scenic background influences the card color. */
    div[data-testid="stAlert"],
    div[data-testid="stMetric"],
    .glass-caption {
        background:
            linear-gradient(135deg, rgba(255,255,255,0.16), rgba(255,255,255,0.055)),
            radial-gradient(circle at 8% 0%, rgba(255,255,255,0.16), transparent 38%),
            rgba(8,13,26,0.48) !important;
        border: 1px solid rgba(255,255,255,0.23) !important;
        backdrop-filter: blur(26px) saturate(190%) brightness(1.08) !important;
        -webkit-backdrop-filter: blur(26px) saturate(190%) brightness(1.08) !important;
        box-shadow: 0 22px 58px rgba(0,0,0,0.30), 0 0 32px rgba(0,122,255,0.10), inset 0 1px 0 rgba(255,255,255,0.26) !important;
    }

    /* Plotly panels keep canvas stability but become more transparent, with a glass highlight layer. */
    div[data-testid="stVerticalBlock"] > div:has(.js-plotly-plot) {
        background:
            linear-gradient(135deg, rgba(255,255,255,0.105), rgba(255,255,255,0.035)),
            rgba(8,13,26,0.66) !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        box-shadow: 0 24px 68px rgba(0,0,0,0.34), 0 0 32px rgba(0,122,255,0.08), inset 0 1px 0 rgba(255,255,255,0.18) !important;
    }

    /* Plotly hover/unified hover box readability. This fixes the white unreadable box. */
    .js-plotly-plot .hoverlayer .hovertext path,
    .js-plotly-plot .hoverlayer .spikeline crisp,
    .js-plotly-plot .hoverlayer path {
        fill: rgba(8,13,26,0.96) !important;
        stroke: rgba(0,122,255,0.62) !important;
    }
    .js-plotly-plot .hoverlayer text {
        fill: #F8FAFC !important;
        font-weight: 650 !important;
        text-shadow: none !important;
    }
    .js-plotly-plot .legend,
    .js-plotly-plot .legend rect.bg {
        fill: rgba(8,13,26,0.50) !important;
        stroke: rgba(255,255,255,0.16) !important;
    }
    .js-plotly-plot .legend text {
        fill: #F8FAFC !important;
        text-shadow: none !important;
    }

    /* Apply button keeps the blue liquid glass look but is not painfully bright. */
    div[data-testid="stFormSubmitButton"] > button, .stButton > button {
        background:
            radial-gradient(circle at 18% 12%, rgba(255,255,255,0.40), transparent 32%),
            linear-gradient(135deg, rgba(0,122,255,0.82), rgba(0,122,255,0.46) 58%, rgba(255,255,255,0.12)) !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# =========================================================
# 2.5) Final UI correction: clean sidebar states + redesigned KPI cards
#      No blue text-fill blocks in sidebar. KPI labels/values use a
#      controlled custom card instead of Streamlit metric internals.
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ios-blue: #007AFF;
        --ios-blue-rgb: 0, 122, 255;
        --card-text: #F8FAFC;
        --card-muted: rgba(226,232,240,0.76);
    }

    /* Hard reset for sidebar option rows: the text itself must NEVER become a
       filled blue pill. Only the small native dot/check indicates selection. */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked),
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label:has(input:checked),
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label:hover,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:focus-within,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label:focus-within {
        background: transparent !important;
        background-color: transparent !important;
        border-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 2px 0 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label *,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label *,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) *,
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label:has(input:checked) * {
        background: transparent !important;
        background-color: transparent !important;
        color: rgba(248,250,252,0.96) !important;
        text-shadow: none !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] p::selection,
    section[data-testid="stSidebar"] span::selection,
    section[data-testid="stSidebar"] label::selection,
    section[data-testid="stSidebar"] div::selection {
        background: transparent !important;
        color: rgba(248,250,252,0.96) !important;
    }

    /* Keep the iOS blue only on the actual radio dot / checkbox mark. */
    section[data-testid="stSidebar"] input[type="radio"],
    section[data-testid="stSidebar"] input[type="checkbox"] {
        accent-color: var(--ios-blue) !important;
    }

    /* The old stMetric internals are not used anymore, but keep them hidden-stable
       in case Streamlit renders any future metric elsewhere. */
    div[data-testid="stMetric"]::after,
    div[data-testid="stMetric"]::before {
        display: none !important;
        content: none !important;
    }

    .kpi-card {
        position: relative;
        overflow: hidden;
        min-height: 112px;
        padding: 22px 22px 20px 22px;
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.22);
        background:
            linear-gradient(135deg, rgba(255,255,255,0.145), rgba(255,255,255,0.045)),
            radial-gradient(circle at 14% 0%, rgba(255,255,255,0.20), transparent 34%),
            radial-gradient(circle at 92% 20%, rgba(var(--ios-blue-rgb),0.22), transparent 42%),
            rgba(8, 13, 26, 0.46);
        box-shadow:
            0 22px 58px rgba(0,0,0,0.30),
            0 0 32px rgba(var(--ios-blue-rgb),0.09),
            inset 0 1px 0 rgba(255,255,255,0.25),
            inset 0 -1px 0 rgba(255,255,255,0.06);
        backdrop-filter: blur(26px) saturate(185%) brightness(1.06);
        -webkit-backdrop-filter: blur(26px) saturate(185%) brightness(1.06);
    }

    .kpi-card::before {
        content: "";
        position: absolute;
        left: 12px;
        right: 12px;
        top: 10px;
        height: 34px;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(255,255,255,0.16), rgba(255,255,255,0.025));
        pointer-events: none;
    }

    .kpi-card::after {
        content: "";
        position: absolute;
        width: 110px;
        height: 110px;
        right: -44px;
        bottom: -52px;
        border-radius: 50%;
        background: rgba(var(--ios-blue-rgb),0.18);
        filter: blur(10px);
        pointer-events: none;
    }

    .kpi-label {
        position: relative;
        z-index: 1;
        display: block;
        margin: 0 0 12px 0;
        color: var(--card-muted) !important;
        font-size: 0.88rem;
        line-height: 1.2;
        font-weight: 740;
        letter-spacing: -0.01em;
        text-shadow: none !important;
        white-space: nowrap;
    }

    .kpi-value {
        position: relative;
        z-index: 1;
        display: block;
        color: var(--card-text) !important;
        font-size: clamp(1.75rem, 2.4vw, 2.45rem);
        line-height: 1.02;
        font-weight: 900;
        letter-spacing: -0.055em;
        text-shadow: 0 8px 28px rgba(0,0,0,0.28), 0 0 22px rgba(var(--ios-blue-rgb),0.13) !important;
        white-space: nowrap;
    }

    @media (max-width: 900px) {
        .kpi-card { min-height: 96px; padding: 18px 18px 16px 18px; }
        .kpi-label { font-size: 0.82rem; }
        .kpi-value { font-size: 1.75rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Use a blue-first Plotly palette so new categorical traces do not default to red.
px.defaults.color_discrete_sequence = [
    "#007AFF", "#64D2FF", "#30D158", "#BF5AF2", "#FFD60A",
    "#5E5CE6", "#00C7BE", "#FF9F0A", "#8E8E93", "#AC8E68",
]

# =========================================================
# 3) Load data
# =========================================================
@st.cache_data(show_spinner=True)
def load_data():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Main CSV dataset not found: {CSV_PATH}"
        )

    if CSV_PATH.name != MAIN_CSV_NAME:
        raise ValueError(
            f"Wrong CSV loaded: {CSV_PATH.name}; expected {MAIN_CSV_NAME}"
        )

    df = pd.read_csv(CSV_PATH)
    df["date"] = pd.to_datetime(df["date"])

    if "Flood_Risk_Binary" not in df.columns:
        df["Flood_Risk_Binary"] = (df["rainfall_risk_label"] == 3).astype(int)

    return df


df = load_data()


# =========================================================
# 3.1) Responsive chart rendering helper
# =========================================================
PLOTLY_CONFIG = {
    "responsive": True,
    "displaylogo": False,
    "scrollZoom": False,
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d",
        "autoScale2d",
    ],
}

# Dedicated map config for the rainfall map.
# v21: keep the user's preferred mouse-wheel zoom interaction.
# To avoid the old flashing problem, hover labels and the floating modebar stay disabled,
# but Mapbox wheel zoom is restored.
PLOTLY_MAP_CONFIG = {
    "responsive": True,
    "displaylogo": False,
    "displayModeBar": False,
    "scrollZoom": True,
    "doubleClick": "reset",
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d",
        "autoScale2d",
    ],
}


def render_plotly(fig):
    """Render Plotly charts with readable title / legend spacing."""
    fig.update_layout(
        autosize=True,
        font=dict(size=13, color="#F8FAFC"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=70, r=45, t=135, b=95),
        title=dict(
            x=0.015,
            xanchor="left",
            y=0.965,
            yanchor="top",
            font=dict(color="#F8FAFC", size=20),
        ),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.02,
            font=dict(color="#F8FAFC", size=11),
            bgcolor="rgba(15,23,42,0.42)",
            bordercolor="rgba(255,255,255,0.14)",
            borderwidth=1,
            itemwidth=30,
        ),
        hoverlabel=dict(
            bgcolor="rgba(8, 13, 26, 0.96)",
            bordercolor="rgba(0, 122, 255, 0.62)",
            font=dict(color="#F8FAFC", size=12),
            namelength=-1,
        ),
    )
    fig.update_xaxes(
        color="#F8FAFC",
        gridcolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.16)",
    )
    fig.update_yaxes(
        color="#F8FAFC",
        gridcolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.16)",
    )
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)


# Apple Weather-like precipitation colors.
# Important: the low end is blue, not transparent/white.
# This creates an all-map light/moderate precipitation veil, while only high-rainfall
# areas turn purple/pink/yellow. It avoids the ugly isolated city-bubble look.
PRECIPITATION_COLORSCALE = [
    [0.00, "rgba(56,189,248,0.20)"],    # very soft edge blue
    [0.18, "rgba(56,189,248,0.40)"],
    [0.36, "rgba(0, 122, 255,0.62)"],     # moderate blue core
    [0.56, "rgba(124,58,237,0.76)"],     # violet
    [0.72, "rgba(236,72,153,0.86)"],     # pink
    [0.88, "rgba(253,224,71,0.94)"],     # heavy yellow
    [1.00, "rgba(255,250,180,1.00)"],
]

HOTSPOT_COLORSCALE = [
    [0.00, "rgba(124,58,237,0.00)"],
    [0.42, "rgba(124,58,237,0.34)"],
    [0.64, "rgba(236,72,153,0.78)"],
    [0.84, "rgba(253,224,71,0.95)"],
    [1.00, "rgba(255,250,180,1.00)"],
]

MAP_STYLE_OPTIONS = {
    # Most reliable token-free option on Streamlit Cloud.
    "OpenStreetMap Standard (recommended, no token)": "open-street-map",
    "CARTO Positron (clean light, no token)": "carto-positron",
    "CARTO Dark Matter (dark, no token)": "carto-darkmatter",
}


def get_mapbox_token():
    """Optional: use a real Mapbox API token from Streamlit secrets or environment."""
    import os
    token = None
    try:
        token = st.secrets.get("MAPBOX_TOKEN", None)
    except Exception:
        token = None
    if not token:
        token = os.environ.get("MAPBOX_TOKEN")
    return token

MALAYSIA_CITY_COORDS = {
    "Kuala Lumpur": (3.1390, 101.6869), "Putrajaya": (2.9264, 101.6964),
    "Shah Alam": (3.0738, 101.5183), "Klang": (3.0449, 101.4456),
    "Petaling Jaya": (3.1073, 101.6067), "Seremban": (2.7258, 101.9378),
    "Melaka": (2.1896, 102.2501), "Malacca": (2.1896, 102.2501),
    "Johor Bahru": (1.4927, 103.7414), "Kuantan": (3.8077, 103.3260),
    "Kota Bharu": (6.1254, 102.2381), "Kuala Terengganu": (5.3296, 103.1370),
    "Alor Setar": (6.1248, 100.3678), "George Town": (5.4141, 100.3288),
    "Sungai Petani": (5.6436, 100.4894), "Taiping": (4.8519, 100.7416),
    "Ipoh": (4.5975, 101.0901), "Kuching": (1.5533, 110.3592),
    "Sibu": (2.2876, 111.8305), "Miri": (4.3995, 113.9914),
    "Bintulu": (3.1713, 113.0419), "Kota Kinabalu": (5.9804, 116.0735),
    "Sandakan": (5.8394, 118.1172), "Tawau": (4.2447, 117.8912),
    "Labuan": (5.2831, 115.2308), "Kangar": (6.4449, 100.2048),
}


def detect_lat_lon_columns(input_df):
    lat_candidates = ["lat", "latitude", "Latitude", "LAT", "y"]
    lon_candidates = ["lon", "lng", "longitude", "Longitude", "LON", "LONG", "x"]
    lat_col = next((c for c in lat_candidates if c in input_df.columns), None)
    lon_col = next((c for c in lon_candidates if c in input_df.columns), None)
    return lat_col, lon_col


def add_city_coordinates(input_df):
    """Use dataset coordinates when available, otherwise fall back to known Malaysia city coordinates."""
    out = input_df.copy()
    lat_col, lon_col = detect_lat_lon_columns(out)

    if lat_col and lon_col:
        out["_lat"] = pd.to_numeric(out[lat_col], errors="coerce")
        out["_lon"] = pd.to_numeric(out[lon_col], errors="coerce")
    else:
        out["_lat"] = np.nan
        out["_lon"] = np.nan

    missing_mask = out["_lat"].isna() | out["_lon"].isna()
    if missing_mask.any():
        coords = out.loc[missing_mask, "city"].map(MALAYSIA_CITY_COORDS)
        out.loc[missing_mask, "_lat"] = coords.map(lambda v: v[0] if isinstance(v, tuple) else np.nan)
        out.loc[missing_mask, "_lon"] = coords.map(lambda v: v[1] if isinstance(v, tuple) else np.nan)

    return out.dropna(subset=["_lat", "_lon"])


def build_animation_period_columns(input_df, agg_level):
    out = input_df.copy()
    if agg_level == "Yearly":
        out["animation_period"] = out["year"].astype(int).astype(str)
        out["period_order"] = out["year"].astype(int)
    elif agg_level == "Monthly":
        out["period_dt"] = out["date"].dt.to_period("M").dt.to_timestamp()
        out["animation_period"] = out["period_dt"].dt.strftime("%Y-%m")
        out["period_order"] = out["period_dt"]
    else:
        out["period_dt"] = out["date"].dt.normalize()
        out["animation_period"] = out["period_dt"].dt.strftime("%Y-%m-%d")
        out["period_order"] = out["period_dt"]
    return out


def expand_precipitation_points(input_df, intensity_col="rainfall_scaled", rings=4, points_per_ring=12):
    """
    Convert sparse city rainfall points into a soft visual field for density_mapbox.

    This does not change the underlying rainfall data. It only creates extra
    nearby weighted points so the map looks like a continuous precipitation
    layer instead of isolated dots. The expansion is deterministic so animation
    frames stay stable and do not jitter.
    """
    if input_df.empty:
        return input_df.copy()

    rows = []
    base = input_df.copy()
    base[intensity_col] = pd.to_numeric(base[intensity_col], errors="coerce").fillna(0.0)

    # Malaysia city-level data is sparse, so these degree offsets create a
    # visible but still geographically local glow around each city.
    ring_offsets = np.linspace(0.10, 0.42, max(1, int(rings)))
    angle_count = max(6, int(points_per_ring))
    angles = np.linspace(0, 2 * np.pi, angle_count, endpoint=False)

    for _, row in base.iterrows():
        lat = float(row["_lat"])
        lon = float(row["_lon"])
        value = float(row[intensity_col])
        if not np.isfinite(lat) or not np.isfinite(lon) or not np.isfinite(value):
            continue

        center = row.copy()
        center["_vis_lat"] = lat
        center["_vis_lon"] = lon
        center["_vis_value"] = value
        rows.append(center)

        # Light rainfall still needs visible blue coverage; heavy rainfall gets
        # a slightly stronger cloud, but the color scale remains data-driven.
        for ring_idx, offset in enumerate(ring_offsets, start=1):
            decay = 1.0 / (1.0 + ring_idx * 0.75)
            for angle in angles:
                expanded = row.copy()
                # Longitude degrees shrink with latitude. Clamp keeps the
                # correction stable near the equator.
                lon_correction = max(0.25, np.cos(np.deg2rad(lat)))
                expanded["_vis_lat"] = lat + offset * np.sin(angle)
                expanded["_vis_lon"] = lon + (offset * np.cos(angle) / lon_correction)
                expanded["_vis_value"] = value * decay
                rows.append(expanded)

    if not rows:
        return base.assign(_vis_lat=base["_lat"], _vis_lon=base["_lon"], _vis_value=base[intensity_col])

    return pd.DataFrame(rows).reset_index(drop=True)


# =========================================================
# 4) Header
# =========================================================
st.title("Malaysia CHIRPS Rainfall & Flood-Risk Dashboard")
st.caption(
    "Interactive dashboard for city-level rainfall analysis, "
    "rainfall intensity level, and rainfall-based Flood_Risk_Binary from 2000 to 2026."
)

st.caption(
    "Mobile-friendly mode is handled automatically by the browser layout: "
    "on phones, controls become touch-friendly and charts stretch to the screen width."
)


# =========================================================
# 5) Sidebar filters — anti-flicker apply panel
# =========================================================
st.sidebar.header("Control Panel")

st.sidebar.markdown(
    """
    <div class="glass-caption" style="margin-bottom:0.75rem;">
        Anti-flicker mode is enabled. Change controls first, then press <b>Apply update</b>.
        The dashboard will rerender once instead of flashing after every click.
    </div>
    """,
    unsafe_allow_html=True,
)

all_states = sorted(df["state"].dropna().unique())
rainfall_variables = [
    "avg_rainfall_mm",
    "max_rainfall_mm",
    "min_rainfall_mm",
    "median_rainfall_mm",
]
min_year = int(df["year"].min())
max_year = int(df["year"].max())

# Keep the previous applied values stable while the user edits the form.
# This is the main fix for Streamlit's normal full-script rerun behavior.
DEFAULT_DASHBOARD_STATE = {
    "selected_states": all_states,
    "selected_cities": [],
    "selected_rain_var": "avg_rainfall_mm",
    "selected_year_range": (2000, min(2026, max_year)),
    "aggregation_level": "Yearly",
    "chart_mode": "Static Trend",
    "show_flood_risk": True,
    "show_raw_data": False,
    "animation_start_year": 2000,
    "animation_speed": 700,
}
for _k, _v in DEFAULT_DASHBOARD_STATE.items():
    st.session_state.setdefault(_k, _v)

# Build city pool from the currently applied states. This avoids expensive rerenders
# while the multiselect dropdown is being edited.
_applied_states = st.session_state.get("selected_states") or all_states
if _applied_states:
    city_pool = sorted(df[df["state"].isin(_applied_states)]["city"].dropna().unique())
else:
    city_pool = sorted(df["city"].dropna().unique())

default_cities = [
    city for city in [
        "Kuala Lumpur",
        "Klang",
        "Shah Alam",
        "Johor Bahru",
        "Kuching",
        "Kota Kinabalu",
    ]
    if city in city_pool
]
if not default_cities:
    default_cities = city_pool[:5]

if not st.session_state.get("selected_cities"):
    st.session_state["selected_cities"] = default_cities

with st.sidebar.form("dashboard_control_form", clear_on_submit=False):
    selected_states = st.multiselect(
        "Select state(s)",
        all_states,
        default=st.session_state.get("selected_states", all_states),
        help="After changing states, press Apply update once. The city list updates after the apply step to prevent sidebar flicker.",
    )

    # Use the previous city pool during form editing; invalid cities are removed safely after apply.
    selected_cities = st.multiselect(
        "Select city/cities",
        city_pool,
        default=[c for c in st.session_state.get("selected_cities", default_cities) if c in city_pool] or default_cities,
    )

    selected_rain_var = st.selectbox(
        "Select rainfall variable",
        rainfall_variables,
        index=rainfall_variables.index(st.session_state.get("selected_rain_var", "avg_rainfall_mm"))
        if st.session_state.get("selected_rain_var", "avg_rainfall_mm") in rainfall_variables else 0,
    )

    selected_year_range = st.slider(
        "Year range",
        min_value=min_year,
        max_value=max_year,
        value=tuple(st.session_state.get("selected_year_range", (2000, min(2026, max_year)))),
        step=1,
    )

    form_single_year_mode = selected_year_range[0] == selected_year_range[1]

    if form_single_year_mode:
        st.info(
            f"Single-year mode: {selected_year_range[0]}. Aggregation will be locked to Daily after applying."
        )
        aggregation_level = "Daily"
        st.radio(
            "Aggregation level",
            ["Daily"],
            index=0,
            disabled=True,
            help="Locked to Daily because Year range is a single year.",
        )
    else:
        _agg_options = ["Yearly", "Monthly", "Daily"]
        _agg_default = st.session_state.get("aggregation_level", "Yearly")
        if _agg_default not in _agg_options:
            _agg_default = "Yearly"
        aggregation_level = st.radio(
            "Aggregation level",
            _agg_options,
            index=_agg_options.index(_agg_default),
        )

    _chart_options = ["Static Trend", "Animated Timeline", "Heatmap Animation"]
    _chart_default = st.session_state.get("chart_mode", "Static Trend")
    if _chart_default not in _chart_options:
        _chart_default = "Static Trend"
    chart_mode = st.radio(
        "Chart mode",
        _chart_options,
        index=_chart_options.index(_chart_default),
    )

    show_flood_risk = st.checkbox(
        "Show Flood_Risk_Binary chart",
        value=bool(st.session_state.get("show_flood_risk", True)),
    )

    show_raw_data = st.checkbox(
        "Show filtered data preview",
        value=bool(st.session_state.get("show_raw_data", False)),
    )

    if chart_mode in ["Animated Timeline", "Heatmap Animation"]:
        if form_single_year_mode:
            animation_start_year = selected_year_range[0]
            st.caption(
                f"Animation starts from {animation_start_year}. Single-year mode plays daily records within this year."
            )
        else:
            _old_start = int(st.session_state.get("animation_start_year", selected_year_range[0]))
            _old_start = max(selected_year_range[0], min(selected_year_range[1], _old_start))
            animation_start_year = st.slider(
                "Animation start year",
                min_value=selected_year_range[0],
                max_value=selected_year_range[1],
                value=_old_start,
                step=1,
            )
    else:
        animation_start_year = selected_year_range[0]

    animation_speed = st.slider(
        "Animation speed",
        min_value=200,
        max_value=2000,
        value=int(st.session_state.get("animation_speed", 700)),
        step=100,
        help="Lower value means faster animation.",
    )

    apply_dashboard_update = st.form_submit_button("Apply update", use_container_width=True)

if apply_dashboard_update:
    # Remove city choices that no longer exist after a state change.
    _new_city_pool = sorted(df[df["state"].isin(selected_states)]["city"].dropna().unique()) if selected_states else sorted(df["city"].dropna().unique())
    selected_cities = [c for c in selected_cities if c in _new_city_pool]
    if not selected_cities:
        selected_cities = [c for c in default_cities if c in _new_city_pool] or _new_city_pool[:5]

    st.session_state["selected_states"] = selected_states
    st.session_state["selected_cities"] = selected_cities
    st.session_state["selected_rain_var"] = selected_rain_var
    st.session_state["selected_year_range"] = tuple(selected_year_range)
    st.session_state["aggregation_level"] = aggregation_level
    st.session_state["chart_mode"] = chart_mode
    st.session_state["show_flood_risk"] = show_flood_risk
    st.session_state["show_raw_data"] = show_raw_data
    st.session_state["animation_start_year"] = int(animation_start_year)
    st.session_state["animation_speed"] = int(animation_speed)
    # No st.rerun() here. A form submit already reruns the script once;
    # calling st.rerun() again causes a second full redraw and visible flash.

# Use only the last applied values for the actual expensive rendering below.
selected_states = st.session_state["selected_states"]
selected_cities = st.session_state["selected_cities"]
selected_rain_var = st.session_state["selected_rain_var"]
selected_year_range = tuple(st.session_state["selected_year_range"])
aggregation_level = st.session_state["aggregation_level"]
chart_mode = st.session_state["chart_mode"]
show_flood_risk = st.session_state["show_flood_risk"]
show_raw_data = st.session_state["show_raw_data"]
animation_start_year = int(st.session_state["animation_start_year"])
animation_speed = int(st.session_state["animation_speed"])

single_year_mode = selected_year_range[0] == selected_year_range[1]
if single_year_mode:
    aggregation_level = "Daily"
    animation_start_year = selected_year_range[0]

# =========================================================
# 11) Filter data
# =========================================================
# =========================================================
filtered = df[
    (df["year"] >= selected_year_range[0])
    & (df["year"] <= selected_year_range[1])
].copy()

if selected_states:
    filtered = filtered[filtered["state"].isin(selected_states)].copy()

if selected_cities:
    filtered = filtered[filtered["city"].isin(selected_cities)].copy()

if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

if single_year_mode:
    st.info(
        f"Daily view is automatically enabled for {selected_year_range[0]}. "
        "This avoids year-slider conflicts and shows the detailed daily rainfall pattern for the selected year."
    )
else:
    st.info(
        f"{aggregation_level} view is enabled for {selected_year_range[0]}–{selected_year_range[1]}."
    )


# =========================================================
# 12) Aggregation helper
# =========================================================
def build_aggregated_data(input_df, agg_level, rain_vars):
    temp = input_df.copy()

    if agg_level == "Yearly":
        temp["period"] = temp["year"].astype(int)
        group_cols = ["period", "city"]

    elif agg_level == "Monthly":
        temp["period"] = temp["date"].dt.to_period("M").dt.to_timestamp()
        group_cols = ["period", "city"]

    else:
        temp["period"] = temp["date"]
        group_cols = ["period", "city"]

    agg_dict = {
        var: "mean" for var in rain_vars
    }

    agg_dict.update({
        "Flood_Risk_Binary": "sum",
        "rainfall_risk_label": "mean",
    })

    out = temp.groupby(group_cols, as_index=False).agg(agg_dict)
    return out


plot_df = build_aggregated_data(
    filtered,
    aggregation_level,
    [selected_rain_var],
)


# =========================================================
# 13) Summary metrics
# =========================================================
total_records = len(filtered)
city_count = filtered["city"].nunique()
avg_rainfall = filtered["avg_rainfall_mm"].mean()
risk_count = int(filtered["Flood_Risk_Binary"].sum())

def render_kpi_card(label, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <span class="kpi-label">{label}</span>
            <span class="kpi-value">{value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card("Filtered Records", f"{total_records:,}")
with col2:
    render_kpi_card("Selected Cities", f"{city_count}")
with col3:
    render_kpi_card("Average Rainfall", f"{avg_rainfall:.2f} mm")
with col4:
    render_kpi_card("Flood Risk Signals", f"{risk_count:,}")


# =========================================================
# 14) Static trend charts
# =========================================================
st.subheader("Rainfall Trend")

if chart_mode == "Static Trend":
    long_df = plot_df.melt(
        id_vars=["period", "city"],
        value_vars=[selected_rain_var],
        var_name="rainfall_variable",
        value_name="rainfall_mm",
    )

    fig_line = px.line(
        long_df,
        x="period",
        y="rainfall_mm",
        color="city",
        line_dash="rainfall_variable",
        markers=True if aggregation_level in ["Yearly", "Daily"] else False,
        title=f"{aggregation_level} Rainfall Trend by City: {selected_rain_var}",
    )

    fig_line.update_layout(
        height=590,
        hovermode="x unified",
        transition_duration=500,
        xaxis_title="Time",
        yaxis_title="Rainfall (mm)",
        title=dict(
            text=f"{aggregation_level} Rainfall Trend by City: {selected_rain_var}",
            x=0.02,
            xanchor="left",
            y=0.98,
            font=dict(size=19, color="#F8FAFC"),
        ),
        legend=dict(
            title=dict(text="City / Rainfall Variable", font=dict(color="#F8FAFC", size=12)),
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="left",
            x=0.0,
            font=dict(color="#F8FAFC", size=11),
            bgcolor="rgba(15,23,42,0.35)",
            bordercolor="rgba(255,255,255,0.12)",
            borderwidth=1,
        ),
        margin=dict(l=70, r=35, t=125, b=65),
    )

    render_plotly(fig_line)


# =========================================================
# 15) Animated timeline chart
# =========================================================
elif chart_mode == "Animated Timeline":
    st.info(
        "Animated Timeline mode shows how rainfall changes over time. "
        "Use the play button inside the chart to animate from the selected start point."
    )

    animated_chart_view = st.radio(
        "Animated chart display mode",
        [
            "Bar Chart Only",
            "Line Chart Only",
            "Bar + Line Chart",
        ],
        index=2,
        horizontal=True,
    )

    show_pie_chart = st.checkbox(
        "Show rainfall share pie chart",
        value=True,
        help="Shows each selected city's rainfall share at each animation time point."
    )

    anim_df = filtered[filtered["year"] >= animation_start_year].copy()

    if aggregation_level == "Daily":
        if single_year_mode:
            st.warning(
                f"Daily animation is enabled for {selected_year_range[0]}. "
                "This gives the full daily pattern for the selected year, but playback may be slower than yearly/monthly mode."
            )
        else:
            st.warning(
                "Daily animation may be too dense and slow. "
                "Monthly or Yearly animation is recommended for smoother playback."
            )

    # ---------------------------------------------------------
    # Build animation period
    # ---------------------------------------------------------
    if aggregation_level == "Yearly":
        anim_df["animation_period"] = anim_df["year"].astype(int)
        group_cols = ["animation_period", "city"]

    elif aggregation_level == "Monthly":
        anim_df["animation_period"] = anim_df["date"].dt.to_period("M").astype(str)
        group_cols = ["animation_period", "city"]

    else:
        anim_df["animation_period"] = anim_df["date"].dt.strftime("%Y-%m-%d")
        group_cols = ["animation_period", "city"]

    selected_anim_var = selected_rain_var

    anim_plot = anim_df.groupby(group_cols, as_index=False).agg(
        rainfall=(selected_anim_var, "mean"),
        flood_risk_count=("Flood_Risk_Binary", "sum"),
    )

    if anim_plot.empty:
        st.warning("No animation data available for the selected filters.")
        st.stop()

    anim_plot = anim_plot.sort_values(["animation_period", "city"]).reset_index(drop=True)

    # ---------------------------------------------------------
    # 15.1 Animated Bar Chart
    # ---------------------------------------------------------
    if animated_chart_view in ["Bar Chart Only", "Bar + Line Chart"]:
        st.subheader("Animated Bar Chart: City Rainfall Comparison")

        fig_anim_bar = px.bar(
            anim_plot,
            x="city",
            y="rainfall",
            color="city",
            animation_frame="animation_period",
            range_y=[0, max(1, anim_plot["rainfall"].quantile(0.995) * 1.15)],
            title=f"Animated {aggregation_level} Rainfall by City: {selected_anim_var}",
            labels={
                "city": "City",
                "rainfall": "Rainfall (mm)",
                "animation_period": "Time",
            },
        )

        fig_anim_bar.update_layout(
            height=620,
            showlegend=False,
            xaxis_tickangle=-35,
            xaxis_title="City",
            yaxis_title="Rainfall (mm)",
            transition_duration=animation_speed,
            margin=dict(l=60, r=40, t=80, b=160),
        )

        if fig_anim_bar.layout.updatemenus:
            fig_anim_bar.layout.updatemenus[0].x = 0.02
            fig_anim_bar.layout.updatemenus[0].y = -0.25
            fig_anim_bar.layout.updatemenus[0].xanchor = "left"
            fig_anim_bar.layout.updatemenus[0].yanchor = "top"

            fig_anim_bar.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = animation_speed
            fig_anim_bar.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = int(animation_speed * 0.6)

        if fig_anim_bar.layout.sliders:
            fig_anim_bar.layout.sliders[0].x = 0.18
            fig_anim_bar.layout.sliders[0].y = -0.15
            fig_anim_bar.layout.sliders[0].len = 0.76

        render_plotly(fig_anim_bar)

    # ---------------------------------------------------------
    # 15.2 Animated Line Chart - Robust cumulative trend animation
    # ---------------------------------------------------------
    if animated_chart_view in ["Line Chart Only", "Bar + Line Chart"]:
        st.subheader("Animated Line Chart: Rainfall Trend Over Time")

        line_base_df = anim_plot.copy()

        if aggregation_level == "Yearly":
            line_base_df["period_order"] = line_base_df["animation_period"].astype(int)
            line_base_df["period_display"] = line_base_df["animation_period"].astype(str)
            x_axis_type = "linear"
            x_values_col = "period_order"

        elif aggregation_level == "Monthly":
            line_base_df["period_datetime"] = pd.to_datetime(line_base_df["animation_period"] + "-01")
            line_base_df["period_order"] = line_base_df["period_datetime"]
            line_base_df["period_display"] = line_base_df["animation_period"].astype(str)
            x_axis_type = "date"
            x_values_col = "period_order"

        else:
            line_base_df["period_datetime"] = pd.to_datetime(line_base_df["animation_period"])
            line_base_df["period_order"] = line_base_df["period_datetime"]
            line_base_df["period_display"] = line_base_df["animation_period"].astype(str)
            x_axis_type = "date"
            x_values_col = "period_order"

        line_base_df = line_base_df.sort_values(["period_order", "city"]).reset_index(drop=True)

        periods_ordered = (
            line_base_df[["period_order", "period_display"]]
            .drop_duplicates()
            .sort_values("period_order")
            .reset_index(drop=True)
        )

        cities_ordered = sorted(line_base_df["city"].unique())

        def build_line_traces_until(current_period_order):
            traces = []
            frame_df = line_base_df[line_base_df["period_order"] <= current_period_order].copy()

            for city_name in cities_ordered:
                city_df = frame_df[frame_df["city"] == city_name].sort_values("period_order")

                traces.append(
                    go.Scatter(
                        x=city_df[x_values_col],
                        y=city_df["rainfall"],
                        mode="lines+markers",
                        name=city_name,
                        line=dict(width=3),
                        marker=dict(size=7),
                        hovertemplate=(
                            "<b>%{fullData.name}</b><br>"
                            "Time: %{x}<br>"
                            "Rainfall: %{y:.2f} mm"
                            "<extra></extra>"
                        ),
                    )
                )

            return traces

        first_period_order = periods_ordered["period_order"].iloc[0]
        initial_traces = build_line_traces_until(first_period_order)

        fig_anim_line = go.Figure(data=initial_traces)

        frames = []

        for _, row in periods_ordered.iterrows():
            current_period_order = row["period_order"]
            current_period_display = row["period_display"]

            frames.append(
                go.Frame(
                    data=build_line_traces_until(current_period_order),
                    name=str(current_period_display),
                )
            )

        fig_anim_line.frames = frames

        y_max = max(1, line_base_df["rainfall"].quantile(0.995) * 1.15)

        if aggregation_level == "Yearly":
            x_min = int(line_base_df["period_order"].min())
            x_max = int(line_base_df["period_order"].max())
        else:
            x_min = line_base_df["period_order"].min()
            x_max = line_base_df["period_order"].max()

        slider_steps = []

        for _, row in periods_ordered.iterrows():
            current_period_display = str(row["period_display"])

            slider_steps.append(
                dict(
                    method="animate",
                    label=current_period_display,
                    args=[
                        [current_period_display],
                        dict(
                            mode="immediate",
                            frame=dict(duration=animation_speed, redraw=True),
                            transition=dict(duration=int(animation_speed * 0.6)),
                        ),
                    ],
                )
            )

        fig_anim_line.update_layout(
            title=f"Animated {aggregation_level} Rainfall Trend by City: {selected_anim_var}",
            height=650,
            xaxis=dict(
                title="Time",
                type=x_axis_type,
                range=[x_min, x_max],
            ),
            yaxis=dict(
                title="Rainfall (mm)",
                range=[0, y_max],
            ),
            hovermode="x unified",
            legend_title="City",
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    direction="left",
                    x=0.02,
                    y=-0.30,
                    xanchor="left",
                    yanchor="top",
                    pad=dict(r=10, t=10),
                    buttons=[
                        dict(
                            label="▶ Play",
                            method="animate",
                            args=[
                                None,
                                dict(
                                    frame=dict(duration=animation_speed, redraw=True),
                                    transition=dict(duration=int(animation_speed * 0.6)),
                                    fromcurrent=True,
                                    mode="immediate",
                                ),
                            ],
                        ),
                        dict(
                            label="■ Pause",
                            method="animate",
                            args=[
                                [None],
                                dict(
                                    frame=dict(duration=0, redraw=False),
                                    transition=dict(duration=0),
                                    mode="immediate",
                                ),
                            ],
                        ),
                    ],
                )
            ],
            sliders=[
                dict(
                    active=0,
                    x=0.18,
                    y=-0.18,
                    len=0.76,
                    xanchor="left",
                    yanchor="top",
                    pad=dict(b=10, t=45),
                    currentvalue=dict(
                        prefix="Current Time = ",
                        visible=True,
                        font=dict(size=14),
                        xanchor="right",
                    ),
                    steps=slider_steps,
                )
            ],
            margin=dict(l=60, r=40, t=80, b=180),
        )

        render_plotly(fig_anim_line)

    # ---------------------------------------------------------
    # 15.3 Animated Pie Chart: Rainfall Share by City
    # ---------------------------------------------------------
    if show_pie_chart:
        st.subheader("Animated Pie Chart: City Rainfall Share")

        pie_df = anim_plot.copy()

        period_total = pie_df.groupby("animation_period")["rainfall"].transform("sum")
        pie_df["rainfall_share"] = pie_df["rainfall"] / period_total
        pie_df["rainfall_share"] = pie_df["rainfall_share"].fillna(0)

        if aggregation_level == "Yearly":
            pie_df["period_order"] = pie_df["animation_period"].astype(int)
            pie_df["period_display"] = pie_df["animation_period"].astype(str)

        elif aggregation_level == "Monthly":
            pie_df["period_datetime"] = pd.to_datetime(pie_df["animation_period"] + "-01")
            pie_df["period_order"] = pie_df["period_datetime"]
            pie_df["period_display"] = pie_df["animation_period"].astype(str)

        else:
            pie_df["period_datetime"] = pd.to_datetime(pie_df["animation_period"])
            pie_df["period_order"] = pie_df["period_datetime"]
            pie_df["period_display"] = pie_df["animation_period"].astype(str)

        pie_df = pie_df.sort_values(["period_order", "city"]).reset_index(drop=True)

        periods_ordered = (
            pie_df[["period_order", "period_display"]]
            .drop_duplicates()
            .sort_values("period_order")
            .reset_index(drop=True)
        )

        def build_pie_trace(current_period_display):
            frame_df = pie_df[pie_df["period_display"] == str(current_period_display)].copy()

            return go.Pie(
                labels=frame_df["city"],
                values=frame_df["rainfall"],
                hole=0.35,
                textinfo="label+percent",
                textposition="inside",
                customdata=frame_df[["rainfall_share"]],
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Rainfall: %{value:.2f} mm<br>"
                    "Share: %{customdata[0]:.2%}"
                    "<extra></extra>"
                ),
            )

        first_period_display = periods_ordered["period_display"].iloc[0]

        fig_pie = go.Figure(
            data=[build_pie_trace(first_period_display)]
        )

        pie_frames = []

        for _, row in periods_ordered.iterrows():
            current_period_display = str(row["period_display"])

            pie_frames.append(
                go.Frame(
                    data=[build_pie_trace(current_period_display)],
                    name=current_period_display,
                )
            )

        fig_pie.frames = pie_frames

        pie_slider_steps = []

        for _, row in periods_ordered.iterrows():
            current_period_display = str(row["period_display"])

            pie_slider_steps.append(
                dict(
                    method="animate",
                    label=current_period_display,
                    args=[
                        [current_period_display],
                        dict(
                            mode="immediate",
                            frame=dict(duration=animation_speed, redraw=True),
                            transition=dict(duration=int(animation_speed * 0.6)),
                        ),
                    ],
                )
            )

        fig_pie.update_layout(
            title=f"Animated Rainfall Share by City: {selected_anim_var}",
            height=650,
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    direction="left",
                    x=0.02,
                    y=-0.28,
                    xanchor="left",
                    yanchor="top",
                    pad=dict(r=10, t=10),
                    buttons=[
                        dict(
                            label="▶ Play",
                            method="animate",
                            args=[
                                None,
                                dict(
                                    frame=dict(duration=animation_speed, redraw=True),
                                    transition=dict(duration=int(animation_speed * 0.6)),
                                    fromcurrent=True,
                                    mode="immediate",
                                ),
                            ],
                        ),
                        dict(
                            label="■ Pause",
                            method="animate",
                            args=[
                                [None],
                                dict(
                                    frame=dict(duration=0, redraw=False),
                                    transition=dict(duration=0),
                                    mode="immediate",
                                ),
                            ],
                        ),
                    ],
                )
            ],
            sliders=[
                dict(
                    active=0,
                    x=0.18,
                    y=-0.17,
                    len=0.76,
                    xanchor="left",
                    yanchor="top",
                    pad=dict(b=10, t=45),
                    currentvalue=dict(
                        prefix="Current Time = ",
                        visible=True,
                        font=dict(size=14),
                        xanchor="right",
                    ),
                    steps=pie_slider_steps,
                )
            ],
            margin=dict(l=60, r=40, t=80, b=180),
            showlegend=True,
            legend_title="City",
        )

        render_plotly(fig_pie)



def build_compact_precipitation_field(input_df, value_col="rainfall_scaled", spread_deg=0.105):
    """
    Build a small, regular precipitation field around each city point.

    This is intentionally NOT a big circular blob. It creates a compact 3x3
    tile-like field so Plotly's Densitymapbox has enough nearby samples to
    draw a visible rainfall layer, while keeping the number of points small
    enough for Streamlit Cloud.
    """
    if input_df.empty:
        return input_df.copy()

    base = input_df.copy()
    base[value_col] = pd.to_numeric(base[value_col], errors="coerce").fillna(0.0)

    offsets = [
        (0.0, 0.0, 1.00),
        ( spread_deg, 0.0, 0.58), (-spread_deg, 0.0, 0.58),
        (0.0,  spread_deg, 0.58), (0.0, -spread_deg, 0.58),
        ( spread_deg,  spread_deg, 0.34), ( spread_deg, -spread_deg, 0.34),
        (-spread_deg,  spread_deg, 0.34), (-spread_deg, -spread_deg, 0.34),
    ]

    rows = []
    for _, row in base.iterrows():
        lat = float(row["_lat"])
        lon = float(row["_lon"])
        val = float(row[value_col])
        if not np.isfinite(lat) or not np.isfinite(lon) or not np.isfinite(val) or val <= 0:
            continue
        lon_correction = max(0.35, np.cos(np.deg2rad(lat)))
        for dlat, dlon, weight in offsets:
            r = row.copy()
            r["_vis_lat"] = lat + dlat
            r["_vis_lon"] = lon + dlon / lon_correction
            r["_vis_value"] = val * weight
            rows.append(r)

    if not rows:
        return pd.DataFrame(columns=list(base.columns) + ["_vis_lat", "_vis_lon", "_vis_value"])
    return pd.DataFrame(rows).reset_index(drop=True)


# =========================================================
# 15.4) Apple Weather-style animated precipitation heatmap
# =========================================================
if chart_mode == "Heatmap Animation":
    st.subheader("Animated Rainfall Heatmap Map")
    st.markdown(
        """
        <div class="glass-caption">
            Apple Weather-style local precipitation patches: rainfall is rendered as fine, feathered particles around real city locations instead of a large rectangular overlay.
            Drag the timeline or press Start/Pause to watch the rainfall field evolve through time. Mouse-wheel map zoom is disabled on purpose so normal page scrolling does not make the map flash.
        </div>
        """,
        unsafe_allow_html=True,
    )

    map_ready = add_city_coordinates(filtered)

    if map_ready.empty:
        st.warning(
            "No latitude/longitude columns were found and the selected cities are not in the built-in coordinate fallback list. "
            "Add latitude/longitude columns to the CSV or select supported Malaysian cities."
        )
    else:
        map_style_options_runtime = dict(MAP_STYLE_OPTIONS)
        mapbox_token = get_mapbox_token()
        if mapbox_token:
            px.set_mapbox_access_token(mapbox_token)
            map_style_options_runtime.update({
                "Mapbox Streets API (token)": "streets",
                "Mapbox Light API (token)": "light",
                "Mapbox Satellite Streets API (token)": "satellite-streets",
            })

        # Heatmap visual controls are also placed in a form. Without this,
        # every small slider movement triggers a full Streamlit rerun and causes a visible flash.
        st.session_state.setdefault("map_style_label", list(map_style_options_runtime.keys())[0])
        st.session_state.setdefault("field_resolution", 520)
        st.session_state.setdefault("field_spread_pct", 56)
        st.session_state.setdefault("heat_opacity_pct", 44)
        st.session_state.setdefault("field_cell_size", 6)
        st.session_state.setdefault("edge_feather_pct", 8)
        st.session_state.setdefault("smooth_transition", 120)

        with st.sidebar.form("heatmap_visual_form", clear_on_submit=False):
            _map_labels = list(map_style_options_runtime.keys())
            _old_map_label = st.session_state.get("map_style_label", _map_labels[0])
            if _old_map_label not in _map_labels:
                _old_map_label = _map_labels[0]
            map_style_label_pending = st.selectbox(
                "Map tile layer",
                _map_labels,
                index=_map_labels.index(_old_map_label),
                help="These visual settings are applied only after pressing Apply heatmap style, preventing slider-by-slider flicker.",
            )

            field_resolution_pending = st.slider(
                "Rain texture detail",
                min_value=160,
                max_value=900,
                value=int(st.session_state.get("field_resolution", 520)),
                step=20,
                help="High-DPI particle density for each city rain patch. Higher values pack many more micro-particles into the same local area, making the patch look smoother and less dot-like when zoomed.",
            )
            field_spread_pct_pending = st.slider(
                "Rainfall influence radius",
                min_value=22,
                max_value=130,
                value=int(st.session_state.get("field_spread_pct", 56)),
                step=4,
                help="Controls the local radius of each rainfall patch. Keep this moderate to preserve location precision.",
            )
            heat_opacity_pct_pending = st.slider(
                "Rain layer opacity",
                min_value=24,
                max_value=76,
                value=int(st.session_state.get("heat_opacity_pct", 44)),
                step=2,
                help="Controls the visual strength of the rainfall layer. Lower values look more elegant and map-like.",
            )
            field_cell_size_pending = st.slider(
                "Rain particle size",
                min_value=2,
                max_value=12,
                value=int(st.session_state.get("field_cell_size", 6)),
                step=1,
                help="Size of each micro-particle. Larger points look fuller; higher texture detail keeps the patch smooth.",
            )
            edge_feather_pct_pending = st.slider(
                "Minimum visible rainfall",
                min_value=4,
                max_value=34,
                value=int(st.session_state.get("edge_feather_pct", 8)),
                step=1,
                help="Hides very weak outer particles so the overlay stays precise instead of covering a large area.",
            )

            smooth_transition_pending = st.slider(
                "Heatmap transition smoothness",
                min_value=0,
                max_value=360,
                value=int(st.session_state.get("smooth_transition", 120)),
                step=10,
                help="Controls the transition when you drag the timeline or press Start.",
            )
            apply_heatmap_style = st.form_submit_button("Apply heatmap style", use_container_width=True)

        if apply_heatmap_style:
            st.session_state["map_style_label"] = map_style_label_pending
            st.session_state["field_resolution"] = int(field_resolution_pending)
            st.session_state["field_spread_pct"] = int(field_spread_pct_pending)
            st.session_state["heat_opacity_pct"] = int(heat_opacity_pct_pending)
            st.session_state["field_cell_size"] = int(field_cell_size_pending)
            st.session_state["edge_feather_pct"] = int(edge_feather_pct_pending)
            st.session_state["smooth_transition"] = int(smooth_transition_pending)
            # No st.rerun() here. Avoid double rerender/flicker after applying style.

        map_style_label = st.session_state["map_style_label"]
        map_style = map_style_options_runtime[map_style_label]
        field_resolution = int(st.session_state["field_resolution"])
        field_spread = int(st.session_state["field_spread_pct"]) / 100.0
        heat_opacity = int(st.session_state["heat_opacity_pct"]) / 100.0
        field_cell_size = int(st.session_state["field_cell_size"])
        edge_feather = int(st.session_state["edge_feather_pct"]) / 100.0
        smooth_transition = int(st.session_state["smooth_transition"])

        heat_anim = map_ready[map_ready["year"] >= animation_start_year].copy()
        heat_anim = build_animation_period_columns(heat_anim, aggregation_level)

        # For a visual rainfall layer, daily mode should not average rainfall away too much.
        # We still respect the selected rainfall variable, but the final display is log-scaled
        # so small but non-zero rainfall remains visible.
        heat_group = heat_anim.groupby(
            ["animation_period", "period_order", "city", "state", "_lat", "_lon"],
            as_index=False,
        ).agg(
            rainfall=(selected_rain_var, "mean"),
            flood_risk_count=("Flood_Risk_Binary", "sum"),
        )
        heat_group = heat_group.sort_values(["period_order", "city"]).reset_index(drop=True)

        if heat_group.empty:
            st.warning("No heatmap animation data is available for the selected filters.")
        else:
            unique_periods = heat_group[["animation_period", "period_order"]].drop_duplicates().sort_values("period_order")
            original_frame_count = len(unique_periods)

            # Plotly map animations become sluggish when thousands of frames are pushed to the browser.
            # This keeps the UI responsive while still showing a clear time evolution.
            if aggregation_level == "Daily":
                max_frames = 90
            elif aggregation_level == "Monthly":
                max_frames = 220
            else:
                max_frames = 360

            if original_frame_count > max_frames:
                stride = int(np.ceil(original_frame_count / max_frames))
                keep_periods = unique_periods.iloc[::stride]["animation_period"].tolist()
                heat_group = heat_group[heat_group["animation_period"].isin(keep_periods)].copy()
                unique_periods = heat_group[["animation_period", "period_order"]].drop_duplicates().sort_values("period_order")
                st.info(
                    f"{aggregation_level} mode has {original_frame_count:,} frames. To stop the browser from freezing, "
                    f"this map renders every {stride}th frame. Narrow the year range for denser animation detail."
                )

            # v21 DATA-TRUE SCALING FIX
            # The old version scaled colors from only the currently selected cities/years.
            # If the selected subset was small, even normal rainfall could become a yellow
            # "extreme" core. That made every city look like the same blue-ring/yellow-center
            # icon, which is visually misleading.
            #
            # This version builds a reference distribution from the full dataset under the
            # selected year range + current aggregation level, then maps each displayed city's
            # rainfall to that stable reference. Therefore color/size reflect the dataset, not
            # just the visible subset. Zero or tiny rainfall will remain invisible or very light.
            ref_df = df[(df["year"] >= selected_year_range[0]) & (df["year"] <= selected_year_range[1])].copy()
            ref_df = build_animation_period_columns(ref_df, aggregation_level)
            ref_group = ref_df.groupby(["animation_period", "city", "state"], as_index=False).agg(
                rainfall=(selected_rain_var, "mean")
            )
            ref_values = pd.to_numeric(ref_group["rainfall"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
            ref_values = ref_values[ref_values > 0]

            if ref_values.empty:
                heat_group["rainfall_scaled"] = 0.0
            else:
                # Robust percentile anchors. p50 should not become yellow; only the upper
                # tail earns pink/yellow. This keeps light/normal cities from being overstated.
                q05, q35, q65, q85, q95, q99 = np.nanpercentile(ref_values, [5, 35, 65, 85, 95, 99])
                anchors_x = np.array([0.0, q05, q35, q65, q85, q95, q99], dtype=float)
                anchors_y = np.array([0.0, 8.0, 24.0, 42.0, 62.0, 82.0, 100.0], dtype=float)
                # Ensure strictly increasing x anchors for np.interp when quantiles are close.
                for i in range(1, len(anchors_x)):
                    if anchors_x[i] <= anchors_x[i - 1]:
                        anchors_x[i] = anchors_x[i - 1] + 1e-6

                rain_values = pd.to_numeric(heat_group["rainfall"], errors="coerce").fillna(0.0).clip(lower=0.0)
                heat_group["rainfall_scaled"] = np.interp(rain_values, anchors_x, anchors_y)
                heat_group.loc[rain_values <= 0, "rainfall_scaled"] = 0.0

                # For real tiny non-zero rain, show a faint blue speck only if the user allows it.
                # Do NOT force all positive rainfall to 10+, because that created fake-looking
                # identical blue rings for places with negligible rain.
                tiny_floor = max(1.0, min(6.0, edge_feather * 35.0))
                heat_group.loc[(rain_values > 0) & (heat_group["rainfall_scaled"] < tiny_floor), "rainfall_scaled"] = tiny_floor

            # Important design fix:
            # Do NOT use a full rectangular interpolation canvas or Plotly Densitymapbox.
            # Both can over-paint huge areas and make city rainfall look geographically false.
            # This version renders each city as a compact, feathered precipitation patch made
            # from many tiny deterministic particles. The patch radius is controlled by rainfall
            # intensity, so light rain stays local and only heavy rain earns a larger glow.
            positive_heat_group = heat_group[heat_group["rainfall"] > 0].copy()

            if positive_heat_group.empty:
                st.warning("The selected period has no positive rainfall values, so no precipitation layer is visible. Try a wider date range or max_rainfall_mm.")
            else:
                center_lat = float(heat_group["_lat"].mean())
                center_lon = float(heat_group["_lon"].mean())
                lat_span = float(heat_group["_lat"].max() - heat_group["_lat"].min())
                lon_span = float(heat_group["_lon"].max() - heat_group["_lon"].min())
                max_span = max(lat_span, lon_span)
                if max_span > 8:
                    zoom_level = 4.35
                elif max_span > 5:
                    zoom_level = 4.85
                elif max_span > 2.5:
                    zoom_level = 5.55
                else:
                    zoom_level = 6.5

                periods = unique_periods["animation_period"].tolist()
                first_period = periods[0]

                # Build a deterministic high-resolution micro-particle stencil once.
                # The earlier version used too few visible particles, so zooming out could reveal
                # dotted circular patches. This version uses Fibonacci-disc supersampling: many
                # tiny points fill the whole local disc evenly, like increasing the texture DPI.
                # Use more actual points than the sidebar value, because Plotly renders marker
                # circles as separate screen glyphs. Oversampling makes each city patch feel
                # like a high-resolution soft disc instead of a cluster of visible dots.
                particle_count = int(field_resolution * 1.35)
                golden_angle = np.pi * (3.0 - np.sqrt(5.0))
                particle_idx = np.arange(max(180, particle_count), dtype=float)
                particle_n = max(1.0, float(len(particle_idx)))
                particle_r = np.sqrt((particle_idx + 0.5) / particle_n)
                particle_theta = particle_idx * golden_angle

                # A tiny deterministic wobble breaks visible rings without changing the city location.
                # It keeps the patch organic and smooth while remaining stable across animation frames.
                wobble = 0.012 * np.sin(particle_idx * 12.9898 + 78.233)
                particle_r = np.clip(particle_r + wobble * (1.0 - particle_r), 0.0, 1.0)
                particle_x = particle_r * np.cos(particle_theta)
                particle_y = particle_r * np.sin(particle_theta)

                # Smooth radial falloff. Values fade gently at the boundary instead of forming
                # a hard circle, while the dense micro-points make the visible patch look continuous.
                particle_weight = np.exp(-3.05 * particle_r * particle_r)

                colorbar = dict(
                    title=dict(text="Precipitation", font=dict(color="#F8FAFC", size=13)),
                    tickmode="array",
                    tickvals=[10, 38, 68, 94],
                    ticktext=["Light", "Moderate", "Heavy", "Extreme"],
                    tickfont=dict(color="#F8FAFC", size=12),
                    len=0.40,
                    thickness=18,
                    x=0.965,
                    y=0.53,
                    bgcolor="rgba(255,255,255,0.16)",
                    bordercolor="rgba(255,255,255,0.38)",
                    borderwidth=1,
                )

                def _field_trace(frame_df):
                    frame_df = frame_df[frame_df["rainfall"] > 0].copy()
                    if frame_df.empty:
                        empty_trace = go.Scattermapbox(
                            lat=[], lon=[], mode="markers",
                            marker=dict(size=field_cell_size, color=[], colorscale=PRECIPITATION_COLORSCALE, cmin=0, cmax=100, opacity=heat_opacity, colorbar=colorbar),
                            hoverinfo="skip", showlegend=False,
                        )
                        return [empty_trace, empty_trace, empty_trace]

                    mist_lat, mist_lon, mist_val, mist_text = [], [], [], []
                    rain_lat, rain_lon, rain_val, rain_text = [], [], [], []
                    core_lat, core_lon, core_val = [], [], []

                    # Visibility floor is now applied to the DATA-TRUE scaled value.
                    # Higher sidebar value hides weak/noisy rain; lower value keeps light drizzle visible.
                    visible_floor = max(3.0, edge_feather * 100.0)

                    for _, row in frame_df.iterrows():
                        lat = float(row["_lat"])
                        lon = float(row["_lon"])
                        scaled = float(row["rainfall_scaled"])
                        rain_mm = float(row["rainfall"])
                        if not np.isfinite(lat) or not np.isfinite(lon) or not np.isfinite(scaled):
                            continue

                        # Rainfall controls BOTH color and physical footprint.
                        # v21 change: footprint grows with true dataset-relative intensity.
                        # Weak rainfall remains a small faint blue dot; only high-percentile rainfall
                        # develops a larger purple/yellow core.
                        intensity = np.clip(scaled / 100.0, 0.0, 1.0)
                        if intensity <= 0:
                            continue
                        radius = (0.018 + field_spread * (0.050 + 0.42 * (intensity ** 1.75)))
                        lon_correction = max(0.35, np.cos(np.deg2rad(lat)))

                        # Feather the outer edge by reducing value toward the boundary. Low edge
                        # values are clipped, giving each patch an organic fade instead of a hard blob.
                        local_val = scaled * particle_weight
                        local_visible = local_val >= visible_floor
                        if not np.any(local_visible):
                            # Keep only a tiny center point for real but very light rain; do not
                            # inflate it into a blue-ring/yellow-center rainfall icon.
                            local_visible = particle_r <= max(0.055, 0.10 + 0.18 * intensity)
                            local_val = np.maximum(local_val, min(10.0, scaled))

                        lats = lat + particle_y[local_visible] * radius
                        lons = lon + particle_x[local_visible] * radius / lon_correction
                        vals = np.clip(local_val[local_visible], 0, 100)

                        text = (
                            f"{row['city']}<br>"
                            f"Frame: {row['animation_period']}<br>"
                            f"Rainfall: {rain_mm:.2f} mm<br>"
                            f"Visual intensity: {scaled:.1f}"
                        )

                        # Blue mist layer: only low/moderate points. Very transparent and fine.
                        mist_mask = vals < 48
                        if np.any(mist_mask):
                            mist_lat.extend(lats[mist_mask])
                            mist_lon.extend(lons[mist_mask])
                            mist_val.extend(vals[mist_mask])
                            mist_text.extend([text] * int(np.sum(mist_mask)))

                        # Main rainfall layer: colored local patch, still compact.
                        rain_mask = vals >= max(12.0, visible_floor)
                        if np.any(rain_mask):
                            rain_lat.extend(lats[rain_mask])
                            rain_lon.extend(lons[rain_mask])
                            rain_val.extend(vals[rain_mask])
                            rain_text.extend([text] * int(np.sum(rain_mask)))

                        # Heavy core: only top intensity points, not the whole area.
                        core_mask = vals >= 68
                        if np.any(core_mask):
                            core_lat.extend(lats[core_mask])
                            core_lon.extend(lons[core_mask])
                            core_val.extend(vals[core_mask])

                    mist_trace = go.Scattermapbox(
                        lat=mist_lat,
                        lon=mist_lon,
                        mode="markers",
                        marker=dict(
                            size=max(3, int(field_cell_size * 0.82)),
                            color=mist_val,
                            colorscale=[
                                [0.00, "rgba(56,189,248,0.00)"],
                                [0.40, "rgba(56,189,248,0.30)"],
                                [1.00, "rgba(0, 122, 255,0.46)"],
                            ],
                            cmin=0,
                            cmax=55,
                            opacity=max(0.14, heat_opacity * 0.48),
                            symbol="circle",
                            allowoverlap=True,
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                        name="Fine rainfall mist",
                    )

                    rain_trace = go.Scattermapbox(
                        lat=rain_lat,
                        lon=rain_lon,
                        mode="markers",
                        marker=dict(
                            size=max(3, field_cell_size),
                            color=rain_val,
                            colorscale=PRECIPITATION_COLORSCALE,
                            cmin=0,
                            cmax=100,
                            opacity=max(0.18, heat_opacity * (0.45 + 0.25 * min(1.0, float(np.nanmax(rain_val)) / 100.0 if len(rain_val) else 0.0))),
                            colorbar=colorbar,
                            symbol="circle",
                            allowoverlap=True,
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                        name="Local rainfall patch",
                    )

                    core_trace = go.Scattermapbox(
                        lat=core_lat,
                        lon=core_lon,
                        mode="markers",
                        marker=dict(
                            size=max(3, int(field_cell_size * 0.95)),
                            color=core_val,
                            colorscale=HOTSPOT_COLORSCALE,
                            cmin=0,
                            cmax=100,
                            opacity=min(0.72, heat_opacity + 0.10),
                            symbol="circle",
                            allowoverlap=True,
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                        name="Heavy rainfall core",
                    )

                    return [mist_trace, rain_trace, core_trace]

                frames = []
                for period in periods:
                    frame_df = heat_group[heat_group["animation_period"] == period]
                    frames.append(go.Frame(name=str(period), data=_field_trace(frame_df)))

                first_field = heat_group[heat_group["animation_period"] == first_period]
                fig_heatmap_anim = go.Figure(data=_field_trace(first_field), frames=frames)

                fig_heatmap_anim.update_layout(
                    height=760,
                    margin=dict(l=0, r=0, t=64, b=132),
                    font=dict(color="#F8FAFC", size=13),
                    title=dict(
                        text=f"Animated {aggregation_level} Rainfall Heatmap: {selected_rain_var}",
                        font=dict(size=19, color="#F8FAFC"),
                        x=0.02,
                        xanchor="left",
                    ),
                    mapbox=dict(
                        style=map_style,
                        center={"lat": center_lat, "lon": center_lon},
                        zoom=zoom_level,
                        bearing=0,
                        pitch=0,
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    transition_duration=smooth_transition,
                    dragmode="pan",
                    hovermode=False,
                    hoverdistance=-1,
                    spikedistance=-1,
                    uirevision="rainfall-map-stable-v21",
                    selectionrevision="rainfall-map-stable-v21",
                    editrevision="rainfall-map-stable-v21",
                    updatemenus=[
                        dict(
                            type="buttons",
                            direction="right",
                            active=-1,
                            x=0.03,
                            y=-0.095,
                            xanchor="left",
                            yanchor="top",
                            pad=dict(r=12, t=12, b=12, l=12),
                            bgcolor="rgba(15,23,42,0.42)",
                            bordercolor="rgba(255,255,255,0.30)",
                            borderwidth=1,
                            font=dict(color="#FFFFFF", size=14),
                            buttons=[
                                dict(
                                    label="▶ Start",
                                    method="animate",
                                    args=[None, {
                                        "frame": {"duration": animation_speed, "redraw": True},
                                        "transition": {"duration": smooth_transition, "easing": "cubic-in-out"},
                                        "fromcurrent": True,
                                        "mode": "immediate",
                                    }],
                                ),
                                dict(
                                    label="Ⅱ Pause",
                                    method="animate",
                                    args=[[None], {
                                        "frame": {"duration": 0, "redraw": False},
                                        "transition": {"duration": 0},
                                        "mode": "immediate",
                                    }],
                                ),
                            ],
                        ),
                        dict(
                            type="buttons",
                            direction="right",
                            active=-1,
                            x=0.50,
                            y=-0.095,
                            xanchor="center",
                            yanchor="top",
                            pad=dict(r=12, t=12, b=12, l=12),
                            bgcolor="rgba(15,23,42,0.42)",
                            bordercolor="rgba(255,255,255,0.30)",
                            borderwidth=1,
                            font=dict(color="#FFFFFF", size=14),
                            buttons=[
                                dict(label="Reset Map", method="relayout", args=[{"mapbox.zoom": zoom_level, "mapbox.center": {"lat": center_lat, "lon": center_lon}}]),
                            ],
                        ),
                    ],
                    sliders=[
                        dict(
                            active=0,
                            x=0.16,
                            y=-0.075,
                            len=0.80,
                            xanchor="left",
                            yanchor="top",
                            pad=dict(t=36, b=12),
                            bgcolor="rgba(238,244,255,0.16)",
                            bordercolor="rgba(255,255,255,0.38)",
                            borderwidth=1,
                            font=dict(color="#F8FAFC", size=10),
                            currentvalue=dict(
                                prefix="Frame = ",
                                visible=True,
                                xanchor="right",
                                font=dict(size=14, color="#FFFFFF"),
                            ),
                            steps=[
                                dict(
                                    label=str(period),
                                    method="animate",
                                    args=[[str(period)], {
                                        "frame": {"duration": 0, "redraw": True},
                                        "transition": {"duration": smooth_transition, "easing": "cubic-in-out"},
                                        "mode": "immediate",
                                    }],
                                )
                                for period in periods
                            ],
                        )
                    ],
                )

                st.plotly_chart(fig_heatmap_anim, width="stretch", config=PLOTLY_MAP_CONFIG, key="rainfall_heatmap_animation_stable_v21")

                with st.expander("Map implementation note", expanded=False):
                    st.markdown(
                        """
                        - This version clips the weak outer field so the precipitation layer no longer appears as a long rectangle.
                        - It uses high-density Fibonacci-disc micro-particles, so each city rainfall patch looks smoother and more circular instead of visibly made from a few dots.
                        - It uses a soft blue rainfall veil plus a separate stronger violet/pink/yellow core for heavy-rain zones.
                        - The field is built from city-level CHIRPS rainfall as local city patches, so it avoids pretending that city-level data is a full radar raster.
                        - Mouse-wheel zoom is enabled again. Hover labels and the floating Plotly modebar remain disabled to reduce mouse-move flicker.
                        - Color and patch radius are scaled against the selected dataset/year-range reference distribution, not only the currently visible city subset. This prevents every city from getting the same blue-ring/yellow-core look.
                        - Daily mode is frame-limited for browser performance. For full daily detail, narrow the year range first.
                        - This is still a city-level CHIRPS dashboard visualization, not official real-time radar.
                        """
                    )


# =========================================================
# 16) Flood risk chart
# =========================================================
if show_flood_risk:
    st.subheader("Flood_Risk_Binary Signal")

    if aggregation_level == "Yearly":
        risk_df = filtered.groupby(["year", "city"], as_index=False)["Flood_Risk_Binary"].sum()
        risk_df = risk_df.rename(columns={"year": "period", "Flood_Risk_Binary": "flood_risk_count"})

    elif aggregation_level == "Monthly":
        risk_df = filtered.copy()
        risk_df["period"] = risk_df["date"].dt.to_period("M").dt.to_timestamp()
        risk_df = risk_df.groupby(["period", "city"], as_index=False)["Flood_Risk_Binary"].sum()
        risk_df = risk_df.rename(columns={"Flood_Risk_Binary": "flood_risk_count"})

    else:
        risk_df = filtered.groupby(["date", "city"], as_index=False)["Flood_Risk_Binary"].sum()
        risk_df = risk_df.rename(columns={"date": "period", "Flood_Risk_Binary": "flood_risk_count"})

    fig_risk = px.bar(
        risk_df,
        x="period",
        y="flood_risk_count",
        color="city",
        title=f"{aggregation_level} Flood_Risk_Binary Count by City",
    )

    fig_risk.update_layout(
        height=520,
        hovermode="x unified",
        xaxis_title="Time",
        yaxis_title="Flood_Risk_Binary Count",
    )

    render_plotly(fig_risk)


# =========================================================
# 17) City comparison chart
# =========================================================
st.subheader("City Comparison Summary")

city_summary = filtered.groupby(["city", "state"], as_index=False).agg(
    avg_rainfall=("avg_rainfall_mm", "mean"),
    max_rainfall=("max_rainfall_mm", "max"),
    min_rainfall=("min_rainfall_mm", "mean"),
    flood_risk_count=("Flood_Risk_Binary", "sum"),
    very_heavy_rate=("Flood_Risk_Binary", "mean"),
)

city_summary = city_summary.sort_values("flood_risk_count", ascending=False)

fig_city = px.bar(
    city_summary,
    x="city",
    y="flood_risk_count",
    color="state",
    title="City-Level Flood Risk Signal Count",
    hover_data=["avg_rainfall", "max_rainfall", "very_heavy_rate"],
)

fig_city.update_layout(
    height=520,
    xaxis_title="City",
    xaxis_tickangle=-35,
    yaxis_title="Flood Risk Signal Count",
)

render_plotly(fig_city)


# =========================================================
# 18) Heatmap
# =========================================================
st.subheader("City × Month Rainfall Heatmap")

heat_df = filtered.copy()
heat_df["month_num"] = heat_df["date"].dt.month

heat_pivot = heat_df.groupby(["city", "month_num"], as_index=False)["avg_rainfall_mm"].mean()

fig_heat = px.density_heatmap(
    heat_pivot,
    x="month_num",
    y="city",
    z="avg_rainfall_mm",
    histfunc="avg",
    title="Average Rainfall Heatmap by City and Month",
    color_continuous_scale="Blues",
)

fig_heat.update_layout(
    height=620,
    xaxis_title="Month",
    yaxis_title="City",
)

render_plotly(fig_heat)


# =========================================================
# 19) Data preview
# =========================================================
if show_raw_data:
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered.head(500), width="stretch")


# =========================================================
# 20) Notes
# =========================================================
st.markdown(
    """
    ---
    **Note:** `Flood_Risk_Binary` is a rainfall-based flood-risk proxy.  
    It does not represent official flood occurrence. It is derived from the rainfall intensity rule where Very Heavy rainfall is treated as a strong rainfall-driven flood-risk signal.
    """
)

# =========================================================
# 2.6) Final correction requested by user:
#      Restore the selected-option glass row / checkbox-radio indicators,
#      but DO NOT fill the option text itself with blue.
#      Keep checkbox/radio/slider accents in iOS #007AFF.
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ios-blue: #007AFF;
        --ios-blue-rgb: 0, 122, 255;
    }

    /* Restore the liquid-glass selected row shape in the sidebar. */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label,
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label {
        display: flex !important;
        align-items: center !important;
        gap: 0.42rem !important;
        min-height: 32px !important;
        width: fit-content !important;
        max-width: 100% !important;
        padding: 5px 9px !important;
        margin: 1px 0 3px 0 !important;
        border-radius: 999px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        box-shadow: none !important;
        outline: none !important;
        cursor: pointer !important;
        transition: background 160ms ease, border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover,
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label:hover {
        background:
            linear-gradient(135deg, rgba(255,255,255,0.070), rgba(255,255,255,0.025)) !important;
        border-color: rgba(255,255,255,0.10) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked),
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label:has(input:checked) {
        background:
            radial-gradient(circle at 18% 15%, rgba(255,255,255,0.20), transparent 36%),
            linear-gradient(135deg, rgba(255,255,255,0.115), rgba(255,255,255,0.035)),
            rgba(var(--ios-blue-rgb), 0.125) !important;
        border-color: rgba(var(--ios-blue-rgb), 0.42) !important;
        box-shadow:
            0 8px 22px rgba(var(--ios-blue-rgb),0.16),
            inset 0 1px 0 rgba(255,255,255,0.18) !important;
    }

    /* The important part: never apply a blue rectangle behind the WORDS.
       Only the row glass and the small dot/check may be blue. */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label p,
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label span,
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label span,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) p,
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label:has(input:checked) p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) span,
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label:has(input:checked) span {
        background: transparent !important;
        background-color: transparent !important;
        color: rgba(248,250,252,0.96) !important;
        -webkit-text-fill-color: rgba(248,250,252,0.96) !important;
        text-shadow: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Do not let browser text selection/focus create a blue text-fill block. */
    section[data-testid="stSidebar"] p::selection,
    section[data-testid="stSidebar"] span::selection,
    section[data-testid="stSidebar"] label::selection,
    section[data-testid="stSidebar"] div::selection {
        background: transparent !important;
        color: rgba(248,250,252,0.96) !important;
        -webkit-text-fill-color: rgba(248,250,252,0.96) !important;
    }

    /* Restore/keep the actual radio dot and checkbox check mark. */
    section[data-testid="stSidebar"] input[type="radio"],
    section[data-testid="stSidebar"] input[type="checkbox"] {
        appearance: auto !important;
        -webkit-appearance: auto !important;
        accent-color: var(--ios-blue) !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: inline-block !important;
        width: 15px !important;
        height: 15px !important;
        min-width: 15px !important;
        margin: 0 2px 0 0 !important;
        filter: drop-shadow(0 0 7px rgba(var(--ios-blue-rgb),0.35)) !important;
    }

    /* If Streamlit/BaseWeb renders an extra custom indicator div after the input,
       keep it blue too, but do not touch the label text. */
    section[data-testid="stSidebar"] input[type="radio"]:checked + div,
    section[data-testid="stSidebar"] input[type="checkbox"]:checked + div {
        border-color: rgba(var(--ios-blue-rgb),0.96) !important;
        background-color: rgba(var(--ios-blue-rgb),0.96) !important;
        box-shadow: 0 0 0 4px rgba(var(--ios-blue-rgb),0.14) !important;
    }

    /* iOS blue sliders: track fill + thumb. */
    section[data-testid="stSidebar"] div[data-testid="stSlider"] [role="slider"] {
        background: #ffffff !important;
        border: 2px solid var(--ios-blue) !important;
        box-shadow:
            0 0 0 5px rgba(var(--ios-blue-rgb),0.16),
            0 0 16px rgba(var(--ios-blue-rgb),0.42),
            0 8px 18px rgba(0,0,0,0.28) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background"] {
        border-radius: 999px !important;
    }

    /* KPI cards: keep the clean fixed layout from v24, with slightly safer top highlight
       so labels never look clipped or misplaced. */
    .kpi-card {
        min-height: 116px !important;
        padding: 24px 22px 20px 22px !important;
    }
    .kpi-card::before {
        top: 9px !important;
        height: 30px !important;
        opacity: 0.55 !important;
    }
    .kpi-label {
        margin-top: 2px !important;
        margin-bottom: 13px !important;
        color: rgba(226,232,240,0.84) !important;
        line-height: 1.15 !important;
    }
    .kpi-value {
        line-height: 1.0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
