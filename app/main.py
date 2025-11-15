# app/main.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from windrose import WindroseAxes
import numpy as np

# -------------------------------
# Utility functions
# -------------------------------
@st.cache_data
def load_country_data(country_name):
    file_map = {
        "Benin": "data/benin-malanville.csv",
        "Sierra Leone": "data/sierraleone-bumbuna.csv",
        "Togo": "data/togo-dapaong_qc.csv"
    }
    df = pd.read_csv(file_map[country_name], parse_dates=["Timestamp"])
    return df

def get_summary_stats(df, columns=["GHI", "DNI", "DHI"]):
    return df[columns].agg(["mean", "median", "std"]).T.reset_index().rename(columns={"index": "Metric"})

def get_top_regions(df, metric="GHI", top_n=5):
    if "Region" in df.columns:
        return df.nlargest(top_n, metric)[["Region", metric]]
    else:
        return df.nlargest(top_n, metric)[[metric]]

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="🌞 Solar Farm Dashboard", layout="wide")
# -------------------------------
# Custom Styling for Sidebar
# -------------------------------
st.markdown("""
    <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #F8FBFF; /* light sky blue */
            padding: 20px;
        }

        /* Sidebar title */
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: #FFB000; /* Solar orange */
            margin-bottom: 10px;
        }

        /* Sidebar labels */
        [data-testid="stSidebar"] label {
            font-size: 16px;
            font-weight: 600;
            color: #333 !important; 
        }

        /* Sidebar multiselect box */
        .stMultiSelect > div > div {
            border: 2px solid #FFB000 !important;
            border-radius: 8px;
        }

        /* Sidebar text */
        [data-testid="stSidebar"] p {
            color: #444;
            font-size: 15px;
        }

        /* Hover effect for options */
        .css-1n76uvr:hover {
            background-color: #FFECB3 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌞 Cross-Country Solar Farm Dashboard")
st.sidebar.markdown('<p class="sidebar-title">🌍 Dashboard Controls</p>', unsafe_allow_html=True)

st.markdown("Compare solar potential across Benin, Sierra Leone, and Togo")

# -------------------------------
# Sidebar - Country Selection
# -------------------------------
st.sidebar.header("Select Countries")
countries = st.sidebar.multiselect(
    "Choose countries to visualize:",
    options=["Benin", "Sierra Leone", "Togo"],
    default=["Benin", "Sierra Leone", "Togo"]
)

if not countries:
    st.warning("Please select at least one country!")
    st.stop()

# -------------------------------
# Load Data
# -------------------------------
data_dict = {country: load_country_data(country) for country in countries}

# -------------------------------
# Boxplots for GHI, DNI, DHI
# -------------------------------
st.header("☀️ Solar Irradiance Comparison by Country")
for metric in ["GHI", "DNI", "DHI"]:
    st.subheader(f"{metric} Comparison")
    fig, ax = plt.subplots(figsize=(8, 5))
    combined_df = pd.concat([df[[metric]].assign(Country=country) for country, df in data_dict.items()])
    sns.boxplot(x="Country", y=metric, data=combined_df, ax=ax, palette="Set2")
    sns.stripplot(x="Country", y=metric, data=combined_df, color="black", alpha=0.3, jitter=0.2, ax=ax)
    st.pyplot(fig)

# -------------------------------
# Summary Table
# -------------------------------
st.header("📊 Summary Table of Solar Metrics")
for country, df in data_dict.items():
    st.subheader(country)
    st.table(get_summary_stats(df))

# -------------------------------
# Interactive Time Series Plot
# -------------------------------
st.header("📈 Interactive Solar Trends")
country_to_plot = st.selectbox("Select a country for time series plot:", countries)
metric_to_plot = st.selectbox("Select metric:", ["GHI", "DNI", "DHI"])
df_plot = data_dict[country_to_plot]

fig2 = px.line(
    df_plot,
    x="Timestamp",
    y=metric_to_plot,
    title=f"{metric_to_plot} Over Time - {country_to_plot}",
    labels={"Timestamp": "Time", metric_to_plot: metric_to_plot}
)
fig2.update_layout(height=400)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Top Regions by GHI
# -------------------------------
st.header("🏆 Top 5 Regions by GHI")
for country, df in data_dict.items():
    st.subheader(country)
    st.table(get_top_regions(df, metric="GHI"))

# -------------------------------
# Bubble Chart: GHI vs Tamb with RH as bubble size
# -------------------------------
st.header("💨 Bubble Chart: GHI vs Ambient Temperature")
country_for_bubble = st.selectbox("Select country for bubble chart:", countries, key="bubble")
df_bubble = data_dict[country_for_bubble]

fig3 = px.scatter(
    df_bubble,
    x="Tamb",
    y="GHI",
    size="RH",
    color="DHI",
    hover_data=["Timestamp"],
    title=f"GHI vs Ambient Temperature with RH as bubble size - {country_for_bubble}",
    labels={"Tamb": "Ambient Temp (°C)", "GHI": "Global Horizontal Irradiance"}
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Cleaning Impact: ModA & ModB pre/post-clean
# -------------------------------
st.header("🧹 Cleaning Impact on Solar Modules")
country_clean = st.selectbox("Select country for cleaning impact:", countries, key="cleaning")
df_clean = data_dict[country_clean]
if "Cleaning" in df_clean.columns:
    cleaned_df = df_clean.groupby("Cleaning")[["ModA", "ModB"]].mean().reset_index()
    fig4, ax = plt.subplots(figsize=(8,5))
    cleaned_df.plot(kind="bar", x="Cleaning", y=["ModA", "ModB"], ax=ax, color=["#FFA500", "#32CD32"])
    ax.set_xticklabels(["Before Cleaning", "After Cleaning"], rotation=0)
    ax.set_ylabel("Average Module Irradiance (W/m²)")
    ax.set_title(f"Effect of Cleaning on Module Performance - {country_clean}")
    st.pyplot(fig4)
else:
    st.info("Cleaning column not found in dataset.")

# -------------------------------
# Wind Rose Plot
# -------------------------------
st.header("🌬 Wind Rose Analysis")
country_wind = st.selectbox("Select country for wind rose:", countries, key="wind")
df_wind = data_dict[country_wind]

if "WS" in df_wind.columns and "WD" in df_wind.columns:
    fig5 = plt.figure(figsize=(6,6))
    ax = WindroseAxes.from_ax(fig=fig5)
    ax.bar(df_wind["WD"], df_wind["WS"], normed=True, opening=0.8, edgecolor='white', cmap=plt.cm.viridis)
    ax.set_legend(title="Wind Speed (m/s)")
    ax.set_title(f"Wind Rose - {country_wind}")
    st.pyplot(fig5)
else:
    st.info("Wind data not available for this country.")

st.markdown("---")
st.markdown("Created by Samrawit Haileeyesus | Solar Data Discovery Challenge")
