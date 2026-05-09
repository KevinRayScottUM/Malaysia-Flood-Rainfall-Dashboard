from pathlib import Path

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
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).parent
CSV_PATH = APP_DIR / "malaysia_chirps_2000_2026_city_rainfall_clean_eda.csv"
MAIN_CSV_NAME = "malaysia_chirps_2000_2026_city_rainfall_clean_eda.csv"

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
# 4) Header
# =========================================================
st.title("Malaysia CHIRPS Rainfall & Flood-Risk Dashboard")
st.caption(
    "Interactive dashboard for city-level rainfall analysis, "
    "rainfall intensity level, and rainfall-based Flood_Risk_Binary from 2000 to 2026."
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
    ["Static Trend", "Animated Timeline"],
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
if chart_mode == "Animated Timeline":
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
        height=550,
        hovermode="x unified",
        transition_duration=500,
        xaxis_title="Time",
        yaxis_title="Rainfall (mm)",
        legend_title="City / Rainfall Variable",
    )

    st.plotly_chart(fig_line, width="stretch")


# =========================================================
# 15) Animated timeline chart
# =========================================================
else:
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
            height=600,
            showlegend=False,
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

        st.plotly_chart(fig_anim_bar, width="stretch")

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

        st.plotly_chart(fig_anim_line, width="stretch")

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

        st.plotly_chart(fig_pie, width="stretch")


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
        height=500,
        hovermode="x unified",
        xaxis_title="Time",
        yaxis_title="Flood_Risk_Binary Count",
    )

    st.plotly_chart(fig_risk, width="stretch")


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
    height=500,
    xaxis_title="City",
    yaxis_title="Flood Risk Signal Count",
)

st.plotly_chart(fig_city, width="stretch")


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
    height=600,
    xaxis_title="Month",
    yaxis_title="City",
)

st.plotly_chart(fig_heat, width="stretch")


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