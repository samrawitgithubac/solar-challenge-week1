# app/main.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from windrose import WindroseAxes
import numpy as np

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="🌞 Solar Farm Dashboard", layout="wide")
st.title("🌞 Solar Farm Dashboard (Memory-Efficient)")

# -------------------------------
# Sidebar - File Upload
# -------------------------------
st.sidebar.header("Upload your dataset(s)")
uploaded_files = st.sidebar.file_uploader(
    "Upload CSV files (one per country):",
    type=["csv"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.warning("Please upload at least one CSV file to continue.")
    st.stop()

# -------------------------------
# Utility Functions
# -------------------------------
def load_data(uploaded_file, max_rows=5000):
    """Load CSV and limit rows for memory efficiency."""
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
        if len(df) > max_rows:
            df = df.head(max_rows)
        return df
    except Exception as e:
        st.error(f"Failed to load {uploaded_file.name}: {e}")
        return None

def get_summary_stats(df, columns=["GHI", "DNI", "DHI"]):
    cols = [c for c in columns if c in df.columns]
    if not cols:
        return pd.DataFrame()
    return df[cols].agg(["mean","median","std"]).T.reset_index().rename(columns={"index":"Metric"})

def get_top_regions(df, metric="GHI", top_n=5):
    if "Region" in df.columns and metric in df.columns:
        return df.nlargest(top_n, metric)[["Region", metric]]
    elif metric in df.columns:
        return df.nlargest(top_n, metric)[[metric]]
    return pd.DataFrame()

# -------------------------------
# Load datasets (lazy)
# -------------------------------
data_dict = {}
for f in uploaded_files:
    df = load_data(f)
    if df is not None:
        country = f.name.split(".")[0]
        data_dict[country] = df

if not data_dict:
    st.warning("No valid CSV files loaded.")
    st.stop()

countries = list(data_dict.keys())

# -------------------------------
# Sidebar - Select dataset for plots
# -------------------------------
selected_country = st.sidebar.selectbox("Select country for analysis:", countries)
df = data_dict[selected_country]

# -------------------------------
# Boxplots for GHI, DNI, DHI
# -------------------------------
st.header("☀️ Solar Irradiance Comparison")
for metric in ["GHI","DNI","DHI"]:
    if metric in df.columns:
        st.subheader(f"{metric} Distribution")
        fig, ax = plt.subplots(figsize=(8,5))
        sns.boxplot(y=df[metric], ax=ax, palette="Set2")
        sns.stripplot(y=df[metric], color="black", alpha=0.3, jitter=0.2, ax=ax)
        st.pyplot(fig)
    else:
        st.info(f"{metric} column not found.")

# -------------------------------
# Summary Table
# -------------------------------
st.header("📊 Summary Table")
summary_df = get_summary_stats(df)
if not summary_df.empty:
    st.table(summary_df)
else:
    st.info("No valid solar metrics found in this dataset.")

# -------------------------------
# Time Series Plot
# -------------------------------
st.header("📈 Interactive Solar Trends")
available_metrics = [c for c in ["GHI","DNI","DHI"] if c in df.columns]
if "Timestamp" in df.columns and available_metrics:
    metric = st.selectbox("Select metric:", available_metrics)
    fig2 = px.line(df, x="Timestamp", y=metric, title=f"{metric} Over Time - {selected_country}")
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Timestamp or solar metrics not found for time series.")

# -------------------------------
# Top Regions by GHI
# -------------------------------
st.header("🏆 Top 5 Regions by GHI")
top_regions = get_top_regions(df, "GHI")
if not top_regions.empty:
    st.table(top_regions)
else:
    st.info("Region or GHI column not available.")

# -------------------------------
# Bubble Chart: GHI vs Tamb
# -------------------------------
st.header("💨 Bubble Chart: GHI vs Ambient Temp")
if all(c in df.columns for c in ["Tamb","GHI","RH","DHI"]):
    fig3 = px.scatter(
        df, x="Tamb", y="GHI", size="RH", color="DHI",
        hover_data=["Timestamp"] if "Timestamp" in df.columns else None,
        title="GHI vs Ambient Temp with RH as bubble size"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Columns required for bubble chart missing.")

# -------------------------------
# Cleaning Impact
# -------------------------------
st.header("🧹 Cleaning Impact on Modules")
if "Cleaning" in df.columns and all(c in df.columns for c in ["ModA","ModB"]):
    cleaned_df = df.groupby("Cleaning")[["ModA","ModB"]].mean().reset_index()
    fig4, ax = plt.subplots(figsize=(8,5))
    cleaned_df.plot(kind="bar", x="Cleaning", y=["ModA","ModB"], ax=ax, color=["#FFA500","#32CD32"])
    ax.set_xticklabels(["Before Cleaning","After Cleaning"], rotation=0)
    ax.set_ylabel("Average Module Irradiance (W/m²)")
    st.pyplot(fig4)
else:
    st.info("Cleaning, ModA, or ModB column missing.")

# -------------------------------
# Wind Rose Plot
# -------------------------------
st.header("🌬 Wind Rose Analysis")
if all(c in df.columns for c in ["WS","WD"]):
    fig5 = plt.figure(figsize=(6,6))
    ax = WindroseAxes.from_ax(fig=fig5)
    ax.bar(df["WD"], df["WS"], normed=True, opening=0.8, edgecolor='white', cmap=plt.cm.viridis)
    ax.set_legend(title="Wind Speed (m/s)")
    st.pyplot(fig5)
else:
    st.info("WS or WD column missing.")

# -------------------------------
st.markdown("---")
st.markdown("Created by Samrawit Haileeyesus | Solar Data Discovery Challenge")
