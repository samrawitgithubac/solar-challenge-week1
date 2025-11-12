# app/utils.py
import pandas as pd

def load_country_data(country_name):
    """Load cleaned CSV for the specified country"""
    file_map = {
        "Benin": "data/benin_clean.csv",
        "Sierra Leone": "data/sierra_leone_clean.csv",
        "Togo": "data/togo_clean.csv"
    }
    df = pd.read_csv(file_map[country_name], parse_dates=["Timestamp"])
    return df

def get_summary_stats(df, columns=["GHI", "DNI", "DHI"]):
    """Return mean, median, and std for key solar metrics"""
    return df[columns].agg(["mean", "median", "std"]).T.reset_index().rename(columns={"index": "Metric"})
