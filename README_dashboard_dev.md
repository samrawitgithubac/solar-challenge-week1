# 🌞 Solar Challenge Week 1 - Dashboard (dashboard-dev branch)

This branch (`dashboard-dev`) contains the **interactive Streamlit dashboard** developed for the **Cross-Country Solar Farm Analysis** challenge.  
The dashboard is designed to analyze solar data from **Benin, Sierra Leone, and Togo** and provide actionable insights for MoonLight Energy Solutions.

---

## 🗂 What We Did in this Branch

1. **Created the Streamlit App**  
   - `app/main.py`: Main dashboard script.  
   - `app/utils.py`: Utility functions for loading data, computing summaries, and handling visualizations.

2. **Interactive Dashboard Features**
   - Sidebar to **select one or multiple countries**.  
   - **Boxplots**: Compare `GHI`, `DNI`, `DHI` across countries.  
   - **Summary Tables**: Mean, median, standard deviation of solar metrics.  
   - **Time Series Plots**: Interactive visualization of solar irradiance over time.  
   - **Bubble Chart**: `GHI` vs `Ambient Temperature` with `RH` as bubble size.  
   - **Cleaning Impact Analysis**: Compare `ModA` and `ModB` before and after cleaning events.  
   - **Wind Rose Plot**: Visualize wind speed and direction patterns.  
   - **Top 5 Regions Table**: Highlight regions with the highest `GHI`.

3. **Data Handling**
   - **Local CSV files** read from the `data/` folder:
     - `benin_clean.csv`  
     - `sierra_leone_clean.csv`  
     - `togo_clean.csv`  
   - **CSV files ignored by Git** via `.gitignore` for privacy and Git hygiene.

4. **Git Hygiene & Workflow**
   - `.gitignore` updated to ignore `data/` and CSV files.  
   - Single **descriptive commit** for this branch:  
     `"feat: basic Streamlit UI with interactive solar dashboard"`  
   - Branch ready to merge into `main` via Pull Request.

---

## 🏃‍♂️ How to Run the Dashboard

1. **Place the cleaned CSV files** in the `data/` folder at the root of the project. Your folder structure should look like this:

solar-challenge-week1/
│
├── app/
│ ├── main.py
│ └── utils.py
├── data/
│ ├── benin_clean.csv
│ ├── sierra_leone_clean.csv
│ └── togo_clean.csv
├── notebooks/
├── requirements.txt
└── README.md
**Install required dependencies**. Make sure you have Python 3.10+ installed, then run:

```bash
pip install -r requirements.txt
Launch the Streamlit dashboard:streamlit run app/main.py
Use the sidebar in the dashboard to:

Select one or multiple countries for analysis.

View boxplots for GHI, DNI, DHI.

Explore summary tables (mean, median, standard deviation).

Check time series plots of solar metrics over time.

Visualize bubble charts (GHI vs Temperature with RH as bubble size).

Analyze cleaning impact on module measurements.

Inspect wind rose plots for wind speed and direction.

See the Top 5 regions with the highest GHI.

Close the dashboard by pressing Ctrl+C in the terminal when finished.