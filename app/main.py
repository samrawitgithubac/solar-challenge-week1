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
def load_uploaded_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def get_summary_stats(df, columns=["GHI", "DNI", "DHI"]):
    available_cols = [col for col in columns if col in df.columns]
    return df[available_cols].agg(["mean", "median", "std"]).T.reset_index().rename(columns={"index": "Metric"})

def get_top_regions(df, metric="GHI", top_n=5):
    if "Region" in df.columns:
        return df.nlargest(top_n, metric)[["Region", metric]]
    elif metric in df.columns:
        return df.nlargest(top_n, metric)[[metric]]
    else:
        return pd.DataFrame()

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="🌞 Solar Farm Dashboard", layout="wide")

# -------------------------------
# Sidebar - File Upload
# -------------------------------
st.sidebar.header("Upload your dataset")
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file for analysis:",
    type=["csv"]
)

if not uploaded_file:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Load dataset
df = load_uploaded_data(uploaded_file)
if df is None or df.empty:
    st.warning("No valid data loaded.")
    st.stop()

# Limit dataset size for plotting (memory-friendly)
MAX_ROWS = 5000
if len(df) > MAX_ROWS:
    st.warning(f"Dataset is large ({len(df)} rows). Only first {MAX_ROWS} rows will be used for plots.")
    df_plot = df.head(MAX_ROWS)
else:
    df_plot = df.copy()

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("🌞 Solar Farm Dashboard (User Upload Mode)")
st.markdown("Analyze solar potential from your uploaded dataset.")

# -------------------------------
# Boxplots for GHI, DNI, DHI
# -------------------------------
st.header("☀️ Solar Irradiance Comparison")
for metric in ["GHI", "DNI", "DHI"]:
    if metric in df_plot.columns:
        st.subheader(f"{metric} Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(y=df_plot[metric], ax=ax, palette="Set2")
        sns.stripplot(y=df_plot[metric], color="black", alpha=0.3, jitter=0.2, ax=ax)
        st.pyplot(fig)
    else:
        st.info(f"{metric} column not found in dataset.")

# -------------------------------
# Summary Table
# -------------------------------
st.header("📊 Summary Table of Solar Metrics")
st.table(get_summary_stats(df))

# -------------------------------
# Interactive Time Series Plot
# -------------------------------
st.header("📈 Interactive Solar Trends")
available_metrics = [col for col in ["GHI", "DNI", "DHI"] if col in df.columns]
if "Timestamp" in df.columns and available_metrics:
    metric_to_plot = st.selectbox("Select metric for time series:", available_metrics)
    fig2 = px.line(
        df_plot,
        x="Timestamp",
        y=metric_to_plot,
        title=f"{metric_to_plot} Over Time",
        labels={"Timestamp": "Time", metric_to_plot: metric_to_plot}
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Timestamp or solar metric columns not found for time series plot.")

# -------------------------------
# Top Regions by GHI
# -------------------------------
st.header("🏆 Top 5 Regions by GHI")
if "GHI" in df.columns:
    top_regions = get_top_regions(df, metric="GHI")
    if not top_regions.empty:
        st.table(top_regions)
    else:
        st.info("Region column not found for top regions analysis.")
else:
    st.info("GHI column not found for top regions analysis.")

# -------------------------------
# Bubble Chart: GHI vs Ambient Temperature
# -------------------------------
st.header("💨 Bubble Chart: GHI vs Ambient Temperature")
if all(col in df_plot.columns for col in ["Tamb", "GHI", "RH", "DHI"]):
    fig3 = px.scatter(
        df_plot,
        x="Tamb",
        y="GHI",
        size="RH",
        color="DHI",
        hover_data=["Timestamp"] if "Timestamp" in df_plot.columns else None,
        title="GHI vs Ambient Temperature with RH as bubble size",
        labels={"Tamb": "Ambient Temp (°C)", "GHI": "Global Horizontal Irradiance"}
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Columns required for bubble chart (Tamb, GHI, RH, DHI) not found.")

# -------------------------------
# Cleaning Impact
# -------------------------------
st.header("🧹 Cleaning Impact on Solar Modules")
if "Cleaning" in df.columns and all(col in df.columns for col in ["ModA", "ModB"]):
    cleaned_df = df.groupby("Cleaning")[["ModA", "ModB"]].mean().reset_index()
    fig4, ax = plt.subplots(figsize=(8,5))
    cleaned_df.plot(kind="bar", x="Cleaning", y=["ModA", "ModB"], ax=ax, color=["#FFA500", "#32CD32"])
    ax.set_xticklabels(["Before Cleaning", "After Cleaning"], rotation=0)
    ax.set_ylabel("Average Module Irradiance (W/m²)")
    ax.set_title("Effect of Cleaning on Module Performance")
    st.pyplot(fig4)
else:
    st.info("Cleaning, ModA, or ModB columns not found in dataset.")

# -------------------------------
# Wind Rose Plot
# -------------------------------
st.header("🌬 Wind Rose Analysis")
if all(col in df_plot.columns for col in ["WS", "WD"]):
    fig5 = plt.figure(figsize=(6,6))
    ax = WindroseAxes.from_ax(fig=fig5)
    ax.bar(df_plot["WD"], df_plot["WS"], normed=True, opening=0.8, edgecolor='white', cmap=plt.cm.viridis)
    ax.set_legend(title="Wind Speed (m/s)")
    ax.set_title("Wind Rose")
    st.pyplot(fig5)
else:
    st.info("WS or WD columns not found for wind rose plot.")

# -------------------------------
st.markdown("---")
st.markdown("Created by Samrawit Haileeyesus | Solar Data Discovery Challenge")
