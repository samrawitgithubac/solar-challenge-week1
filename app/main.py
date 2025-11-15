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
def load_uploaded_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

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
# Sidebar - File Upload
# -------------------------------
st.sidebar.header("Upload your dataset(s)")
uploaded_files = st.sidebar.file_uploader(
    "Upload CSV files for analysis (one per country):",
    type=["csv"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.warning("Please upload at least one CSV file to continue.")
    st.stop()

# Load all uploaded datasets into a dictionary
data_dict = {}
for uploaded_file in uploaded_files:
    country_name = uploaded_file.name.split(".")[0]  # filename without extension
    df = load_uploaded_data(uploaded_file)
    if df is not None:
        data_dict[country_name] = df

if not data_dict:
    st.warning("No valid CSV files loaded.")
    st.stop()

countries = list(data_dict.keys())

# -------------------------------
# Boxplots for GHI, DNI, DHI
# -------------------------------
st.title("🌞 Solar Farm Dashboard (User Upload Mode)")
st.markdown("Compare solar potential across uploaded datasets")

st.header("☀️ Solar Irradiance Comparison")
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
country_to_plot = st.selectbox("Select dataset for time series plot:", countries)
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
# Bubble Chart
# -------------------------------
st.header("💨 Bubble Chart: GHI vs Ambient Temperature")
country_for_bubble = st.selectbox("Select dataset for bubble chart:", countries, key="bubble")
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
# Cleaning Impact
# -------------------------------
st.header("🧹 Cleaning Impact on Solar Modules")
country_clean = st.selectbox("Select dataset for cleaning impact:", countries, key="cleaning")
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
country_wind = st.selectbox("Select dataset for wind rose:", countries, key="wind")
df_wind = data_dict[country_wind]

if "WS" in df_wind.columns and "WD" in df_wind.columns:
    fig5 = plt.figure(figsize=(6,6))
    ax = WindroseAxes.from_ax(fig=fig5)
    ax.bar(df_wind["WD"], df_wind["WS"], normed=True, opening=0.8, edgecolor='white', cmap=plt.cm.viridis)
    ax.set_legend(title="Wind Speed (m/s)")
    ax.set_title(f"Wind Rose - {country_wind}")
    st.pyplot(fig5)
else:
    st.info("Wind data not available for this dataset.")

st.markdown("---")
st.markdown("Created by Samrawit Haileeyesus | Solar Data Discovery Challenge")
