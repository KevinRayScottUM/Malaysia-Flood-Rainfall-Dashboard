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
        --ios-red: #ff4d57;
        --ios-blue: #2f9bff;
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
        background: rgba(255, 77, 87, 0.92) !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(255,77,87,0.24) !important;
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
        --tt-accent: #ff4d57;
        --tt-blue: #38bdf8;
        --tt-purple: #d946ef;
        --tt-yellow: #fde047;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 18% 8%, rgba(56, 189, 248, 0.22), transparent 34%),
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
            radial-gradient(circle at 0% 0%, rgba(56, 189, 248, 0.18), transparent 34%),
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
        background: rgba(255, 77, 87, 0.95) !important;
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

# Dedicated map config: normal charts should not steal page scrolling,
# but the rainfall map must support mouse-wheel zoom and drag-pan.
PLOTLY_MAP_CONFIG = {
    "responsive": True,
    "displaylogo": False,
    # Keep mouse-wheel zoom and drag-pan active on the map.
    "scrollZoom": True,
    # Hide the built-in +/- zoom buttons because the dashboard uses wheel zoom + drag-pan
    # and a custom Reset Map button.
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d",
        "autoScale2d",
        "zoomInMapbox",
        "zoomOutMapbox",
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
            bgcolor="rgba(15,23,42,0.20)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            itemwidth=30,
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
    [0.36, "rgba(14,165,233,0.62)"],     # moderate blue core
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
# 5) Sidebar filters
# =========================================================
st.sidebar.header("Control Panel")

all_states = sorted(df["state"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "Select state(s)",
    all_states,
    default=all_states,
)

if selected_states:
    city_pool = sorted(
        df[df["state"].isin(selected_states)]["city"].dropna().unique()
    )
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

selected_cities = st.sidebar.multiselect(
    "Select city/cities",
    city_pool,
    default=default_cities,
)

rainfall_variables = [
    "avg_rainfall_mm",
    "max_rainfall_mm",
    "min_rainfall_mm",
    "median_rainfall_mm",
]

selected_rain_var = st.sidebar.selectbox(
    "Select rainfall variable",
    rainfall_variables,
    index=0,
)


# =========================================================
# 6) Year range first
#    Important:
#    Year range must be selected before aggregation level.
#    If the selected range is a single year, force Daily mode.
# =========================================================
min_year = int(df["year"].min())
max_year = int(df["year"].max())

selected_year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(2000, min(2026, max_year)),
    step=1,
)

single_year_mode = selected_year_range[0] == selected_year_range[1]


# =========================================================
# 7) Aggregation level logic
# =========================================================
if single_year_mode:
    selected_single_year = selected_year_range[0]

    aggregation_level = "Daily"

    st.sidebar.info(
        f"Single-year mode: {selected_single_year}. "
        "Aggregation level is locked to Daily so the dashboard shows all daily records in this year."
    )

    st.sidebar.radio(
        "Aggregation level",
        ["Daily"],
        index=0,
        disabled=True,
        help="Locked to Daily because Year range is a single year.",
    )

else:
    aggregation_level = st.sidebar.radio(
        "Aggregation level",
        ["Yearly", "Monthly", "Daily"],
        index=0,
    )


# =========================================================
# 8) Chart mode and display options
# =========================================================
chart_mode = st.sidebar.radio(
    "Chart mode",
    ["Static Trend", "Animated Timeline", "Heatmap Animation"],
    index=0,
)

show_flood_risk = st.sidebar.checkbox(
    "Show Flood_Risk_Binary chart",
    value=True,
)

show_raw_data = st.sidebar.checkbox(
    "Show filtered data preview",
    value=False,
)


# =========================================================
# 9) Animation start control
# =========================================================
if chart_mode in ["Animated Timeline", "Heatmap Animation"]:
    if single_year_mode:
        animation_start_year = selected_year_range[0]

        st.sidebar.caption(
            f"Animation starts from {animation_start_year}. "
            "Because only one year is selected, the animation will play daily records within this year."
        )

    else:
        animation_start_year = st.sidebar.slider(
            "Animation start year",
            min_value=selected_year_range[0],
            max_value=selected_year_range[1],
            value=selected_year_range[0],
            step=1,
        )
else:
    animation_start_year = selected_year_range[0]


# =========================================================
# 10) Animation speed
# =========================================================
animation_speed = st.sidebar.slider(
    "Animation speed",
    min_value=200,
    max_value=2000,
    value=700,
    step=100,
    help="Lower value means faster animation.",
)


# =========================================================
# 11) Filter data
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

col1, col2, col3, col4 = st.columns(4)

col1.metric("Filtered Records", f"{total_records:,}")
col2.metric("Selected Cities", city_count)
col3.metric("Average Rainfall", f"{avg_rainfall:.2f} mm")
col4.metric("Flood Risk Signals", f"{risk_count:,}")


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
            Apple Weather-style precipitation field: rainfall is rendered as a smooth map layer instead of oversized city bubbles.
            Drag the timeline or press Start/Pause to watch the rainfall field evolve through time.
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

        map_style_label = st.sidebar.selectbox(
            "Map tile layer",
            list(map_style_options_runtime.keys()),
            index=0,
            help="OpenStreetMap is the safest no-token option. Add MAPBOX_TOKEN in Streamlit secrets for Mapbox API styles.",
        )
        map_style = map_style_options_runtime[map_style_label]

        field_resolution = st.sidebar.slider(
            "Heatmap field detail",
            min_value=55,
            max_value=115,
            value=82,
            step=3,
            help="Higher detail makes the precipitation edge smoother. Use 80–100 for a refined Apple Weather-like layer.",
        )
        field_spread = st.sidebar.slider(
            "Heatmap spatial spread",
            min_value=45,
            max_value=220,
            value=96,
            step=5,
            help="Controls how far rainfall influence spreads from each city. Lower values avoid the ugly long rectangle.",
        ) / 100.0
        heat_opacity = st.sidebar.slider(
            "Heatmap opacity",
            min_value=30,
            max_value=84,
            value=56,
            step=2,
            help="Controls the softness of the rainfall veil. Lower values keep the map elegant and readable.",
        ) / 100
        field_cell_size = st.sidebar.slider(
            "Heatmap texture size",
            min_value=6,
            max_value=22,
            value=10,
            step=1,
            help="Controls the size of each soft field particle. Smaller values make the edge less blocky.",
        )
        edge_feather = st.sidebar.slider(
            "Heatmap edge feather",
            min_value=4,
            max_value=28,
            value=12,
            step=1,
            help="Removes the rectangular canvas by clipping weak outer areas and feathering only the real rainfall influence zones.",
        ) / 100.0

        smooth_transition = st.sidebar.slider(
            "Heatmap transition smoothness",
            min_value=0,
            max_value=360,
            value=120,
            step=10,
            help="Controls the transition when you drag the timeline or press Start.",
        )

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

            # Log scaling makes real differences visible. Then remap values into an Apple Weather-like
            # palette where the entire map gets a blue light/moderate veil and only high-rainfall zones
            # become purple/pink/yellow.
            raw_cap = float(heat_group["rainfall"].quantile(0.985))
            raw_cap = max(1.0, raw_cap)
            heat_group["rainfall_scaled"] = np.log1p(heat_group["rainfall"].clip(lower=0, upper=raw_cap)) / np.log1p(raw_cap) * 100.0
            heat_group.loc[(heat_group["rainfall"] > 0) & (heat_group["rainfall_scaled"] < 10), "rainfall_scaled"] = 10

            # Important design fix:
            # Do NOT use Densitymapbox. It recomputes screen-space density after zoom/pan, which was
            # the reason the same frame could suddenly turn blue or collapse into artificial helper dots.
            # This version builds a fixed geographic interpolation field for every frame, then renders
            # that field as many soft raster-like cells. The color is locked to rainfall intensity, so
            # zooming does not recolor the same data.
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

                # Build one fixed geographic canvas for all frames. This makes the rainfall layer
                # feel attached to the map surface instead of floating as large city bubbles.
                pad_lat = max(0.45, lat_span * 0.12)
                pad_lon = max(0.45, lon_span * 0.12)
                grid_lat = np.linspace(
                    float(heat_group["_lat"].min()) - pad_lat,
                    float(heat_group["_lat"].max()) + pad_lat,
                    int(field_resolution),
                )
                grid_lon = np.linspace(
                    float(heat_group["_lon"].min()) - pad_lon,
                    float(heat_group["_lon"].max()) + pad_lon,
                    int(field_resolution),
                )
                grid_lon_mesh, grid_lat_mesh = np.meshgrid(grid_lon, grid_lat)
                grid_lat_flat = grid_lat_mesh.ravel()
                grid_lon_flat = grid_lon_mesh.ravel()

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
                        return [empty_trace, empty_trace]

                    src_lat = frame_df["_lat"].astype(float).to_numpy()
                    src_lon = frame_df["_lon"].astype(float).to_numpy()
                    src_val = frame_df["rainfall_scaled"].astype(float).to_numpy()

                    # Approximate degree distance with longitude correction for Malaysia latitudes.
                    lat0 = np.nanmean(src_lat)
                    lon_scale = max(0.35, np.cos(np.deg2rad(lat0)))
                    dlat = grid_lat_flat[:, None] - src_lat[None, :]
                    dlon = (grid_lon_flat[:, None] - src_lon[None, :]) * lon_scale
                    dist2 = dlat * dlat + dlon * dlon

                    # Gaussian interpolation creates a stable soft precipitation sheet.
                    sigma = max(0.18, float(field_spread))
                    weights = np.exp(-dist2 / (2.0 * sigma * sigma))
                    weight_sum = weights.sum(axis=1)
                    interpolated = (weights @ src_val) / np.maximum(weight_sum, 1e-9)

                    # Design fix for the ugly rectangle:
                    # Instead of painting every grid point, clip the field by a soft support mask.
                    # The blue layer now follows rainfall influence zones and fades out naturally;
                    # only stronger rain forms violet / pink / yellow cores.
                    support = weight_sum / max(float(weight_sum.max()), 1e-9)
                    support_soft = np.power(np.clip(support, 0, 1), 0.42)
                    hotspot = interpolated * support_soft
                    field_val = np.clip(8.0 + hotspot * 1.04, 0, 100)

                    # Clip away weak outer pixels so the precipitation layer no longer looks like a
                    # floating long rectangle. A tiny low-rainfall halo remains around real influence
                    # zones to keep the Apple Weather-like softness.
                    visible = (support > edge_feather) | (field_val >= 24)

                    if not np.any(visible):
                        visible = support >= np.nanpercentile(support, 92)

                    # Separate soft veil + heavy core. Plotly marker opacity is trace-wide, so using
                    # two traces produces a nicer layered-weather look than one blunt rectangular sheet.
                    core_visible = visible & (field_val >= 52)
                    veil_visible = visible

                    hover_text = np.array([
                        f"Frame: {str(frame_df['animation_period'].iloc[0])}<br>Rainfall layer intensity: {v:.1f}"
                        for v in field_val[veil_visible]
                    ])

                    veil_trace = go.Scattermapbox(
                        lat=grid_lat_flat[veil_visible],
                        lon=grid_lon_flat[veil_visible],
                        mode="markers",
                        marker=dict(
                            size=field_cell_size,
                            color=field_val[veil_visible],
                            colorscale=PRECIPITATION_COLORSCALE,
                            cmin=0,
                            cmax=100,
                            opacity=heat_opacity,
                            colorbar=colorbar,
                            symbol="circle",
                            allowoverlap=True,
                        ),
                        text=hover_text,
                        hovertemplate="%{text}<extra></extra>",
                        showlegend=False,
                        name="Soft rainfall field",
                    )

                    core_trace = go.Scattermapbox(
                        lat=grid_lat_flat[core_visible],
                        lon=grid_lon_flat[core_visible],
                        mode="markers",
                        marker=dict(
                            size=max(6, int(field_cell_size * 0.86)),
                            color=field_val[core_visible],
                            colorscale=HOTSPOT_COLORSCALE,
                            cmin=0,
                            cmax=100,
                            opacity=min(0.92, heat_opacity + 0.18),
                            symbol="circle",
                            allowoverlap=True,
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                        name="Heavy rainfall core",
                    )

                    return [veil_trace, core_trace]

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
                    uirevision="rainfall-map",
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

                st.plotly_chart(fig_heatmap_anim, width="stretch", config=PLOTLY_MAP_CONFIG)

                with st.expander("Map implementation note", expanded=False):
                    st.markdown(
                        """
                        - This version clips the weak outer field so the precipitation layer no longer appears as a long rectangle.
                        - It uses a soft blue rainfall veil plus a separate stronger violet/pink/yellow core for heavy-rain zones.
                        - The field is built from city-level CHIRPS rainfall by stable interpolation, so zooming and dragging the map will not recolor the same frame.
                        - Mouse-wheel zoom and drag-pan remain enabled; the built-in +/- map buttons are hidden.
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
