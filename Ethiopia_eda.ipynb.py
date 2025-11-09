import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes
df = pd.read_csv("data/benin-malanville.csv")
print(df.head())
print(df.info())
df.describe()           # Summary stats for numeric columns
df.isna().sum()         # Count missing values per column
missing_cols = df.isna().sum()[df.isna().sum()/len(df) > 0.05]  # Columns >5% null
print(missing_cols)

numeric_cols = ["GHI", "DNI", "DHI", "ModA", "ModB", "WS", "WSgust"]
z_scores = np.abs(stats.zscore(df[numeric_cols].dropna()))
outliers = (z_scores > 3).any(axis=1)
df_clean = df[~outliers]  # Remove outliers
df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
print(df_clean)
print(df_clean[numeric_cols] )
df_clean['Timestamp'] = pd.to_datetime(df_clean['Timestamp'])
print(df_clean['Timestamp'])


plt.figure(figsize=(12,6))
sns.lineplot(x='Timestamp', y='GHI', data=df_clean)
plt.title("GHI over Time")
plt.show()
df_clean.groupby('Cleaning')[['ModA','ModB']].mean().plot(kind='bar')
plt.title("Average Module Output Pre/Post Cleaning")
plt.show()
plt.figure(figsize=(10,8))
sns.heatmap(df_clean[['GHI','DNI','DHI','TModA','TModB']].corr(), annot=True)
plt.show()
sns.scatterplot(x='WS', y='GHI', data=df_clean)
sns.scatterplot(x='RH', y='Tamb', data=df_clean)
df_clean['GHI'].hist(bins=30)
plt.show()
ax = WindroseAxes.from_ax()
ax.bar(df_clean['WD'], df_clean['WS'], normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
plt.show()
sns.scatterplot(x='RH', y='Tamb', data=df_clean)
sns.scatterplot(x='RH', y='GHI', data=df_clean)
plt.scatter(df_clean['Tamb'], df_clean['GHI'], s=df_clean['RH']*2, alpha=0.5)
plt.xlabel("Ambient Temp (°C)")
plt.ylabel("GHI (W/m²)")
plt.title("GHI vs Temperature (Bubble = RH)")
plt.show()
df_clean.to_csv("data/benin_clean.csv", index=False)
