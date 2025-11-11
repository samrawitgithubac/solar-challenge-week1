# compare-countries Branch Documentation

## Purpose
The `compare-countries` branch focuses on analyzing and comparing solar data across **Benin, Sierra Leone, and Togo**. The goal is to identify regions with high solar potential and provide actionable insights for **MoonLight Energy Solutions** to support strategic solar farm investments.

---

## Files
- `compare_countries.ipynb` – Jupyter Notebook containing:
  - Data loading and cleaning verification
  - Exploratory Data Analysis (EDA)
  - Visualizations: boxplots for GHI, DNI, DHI and bar chart ranking countries by average GHI
  - Summary statistics table (mean, median, standard deviation)
  - One-way ANOVA test for statistical significance
  - Strategy report with actionable recommendations

- `data/` – Folder containing cleaned CSV datasets:
  - `benin_clean.csv`
  - `sierra_leone_clean.csv`
  - `togo_clean.csv`

---

## Key Features
1. **Cross-Country Comparison**
   - Side-by-side boxplots for GHI, DNI, and DHI
   - Average, median, and standard deviation summary table
   - One-way ANOVA test to determine statistical significance

2. **Visual Insights**
   - Bar chart ranking countries by average GHI for quick interpretation
   - Clear visualization of variability and stability of solar metrics

3. **Strategic Recommendations**
   - Highlighting high-potential regions for solar installation
   - Insights for maintenance scheduling based on variability
   - Recommendations for consistent and reliable energy generation

---

## Instructions to Run
1. Make sure the `data/` folder contains all three CSV files (`benin_clean.csv`, `sierra_leone_clean.csv`, `togo_clean.csv`).
2. Open `compare_countries.ipynb` in **Jupyter Notebook** or **VS Code**.
3. Run all cells sequentially to generate:
   - Boxplots
   - Summary tables
   - Statistical analysis (p-values)
   - Strategy report and visualizations

---

## Branch-Specific Notes
- This branch is intended for **exploratory data analysis and visualization**.
- All plots and tables are designed to support the strategy report.
- After completion and review, this branch should be **merged into `main`** for integration with the main project.

---

## Author
Samrawit Haileeyesus  
Date: November 11, 2025
