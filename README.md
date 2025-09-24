# uk-energy-dashboard
英国能源仪表盘

A Streamlit-powered dashboard to explore **UK final energy consumption** with interactive trends, year-to-year comparisons, and one-click PDF export.

**Live app:** https://uk-energy-dashboard-56xuus4qga5eeb8zpa7dh5.streamlit.app/  *(No local setup required — open and use in the browser.)*

---

## Overview

This project integrates official UK energy statistics with interactive visual analytics to help researchers, policy analysts, and the general public understand how energy use changes over time and across sectors.

The dashboard lets you:

- Filter by sector, fuel, and year range
- Inspect time-series trends with auto-highlighted anomalies
- Compare two years side-by-side (Δ in ktoe and %)
- Estimate cost by converting ktoe → kWh and applying a configurable unit price
- Export a multi-page PDF report (KPI sparkline, comparison tables, change bars, and auto-generated highlights)

---

## Features

- **Interactive Trend View** – filter by sector/fuel and explore multi-year consumption trends.  
- **Year-to-Year Comparison** – compare adjacent years side-by-side and see deltas immediately.  
- **Downloadable Report** – export the current view to a **PDF** for sharing/citations.  
- **Clean, standardized data** – ECUK tables are pre-processed for consistent analysis.  

> The app emphasizes clarity & reproducibility: a minimal UI, transparent data prep, and exportable insights.

---

## User Evaluation (Questionnaire)

A short **questionnaire-based user evaluation** validated usability and usefulness with non-expert users.

- Participants used the **live dashboard** and then completed a **Likert-scale** survey + **open-ended** questions.  
- Feedback focused on the clarity of the **Trend View**, usefulness of **Year-to-Year** comparison, and the value of **PDF export** for coursework/reports.  
- Suggestions implemented: clearer legends, persistent filters across pages, and additional sector presets.

---

## Tech Stack

- **App:** Python, **Streamlit**  
- **Viz:** Altair/Plotly (via Streamlit), PDF export utilities  
- **Data:** ECUK (UK Govt / BEIS) + curated CSV/XLSX  
- **Repro:** `requirements.txt`

---

## Project Structure
```
uk-energy-dashboard/
├─ .devcontainer/ # Dev container config (optional)
├─ User Study/ # Questionnaire + anonymized feedback
├─ ECUK_2024_Consumption_tables.xlsx # Primary source (ECUK 2024)
├─ TableC2023.xlsx # Supplemental table
├─ Standardized_Energy_Data.csv # Cleaned & standardized dataset
├─ electricitypricesdataset240725.xlsx # Electricity price reference (supporting)
├─ static_price.xlsx # Static price table (supporting)
├─ preprocess_energy_data.py # Data cleaning & standardization
├─ dashboard_app.py # Streamlit application (entry point)
├─ requirements.txt # Python dependencies
└─ README.md
```


---

## Screenshots

| Trend View | Year-to-Year Comparison | PDF Export |
|---|---|---|
| ![Trend](screenshots/Trend%20View.png) | ![Y2Y](screenshots/Year-to-Year%20Comparison.png) | ![PDF](screenshots/PDF%20Export.png) |

---

## How to Use

### Option A — Use the hosted app *(recommended)*
Open: **https://uk-energy-dashboard-56xuus4qga5eeb8zpa7dh5.streamlit.app/**

### Option B — Run locally
```bash
# 1) Clone
git clone https://github.com/LesleyD808/uk-energy-dashboard.git
cd uk-energy-dashboard

# 2) (Optional) create a virtual environment
# macOS/Linux
python -m venv .venv && source .venv/bin/activate
# Windows
python -m venv .venv && .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Launch the app
streamlit run dashboard_app.py
```


## Timeline

| Period   | Task                                  |
|----------|---------------------------------------|
| Jun 2025 | Topic selection & literature review   |
| Jul 2025 | Data collection & system architecture |
| Aug 2025 | System development & user evaluation  |
| Sep 2025 | Final optimization & feature testing  |

---

## Data Sources

UK final energy consumption tables (ECUK / DUKES / Table C series)
Used for sector & fuel breakdowns; cleaned into Standardized_Energy_Data.csv.

Exact table versions are listed in the repo (e.g., ECUK_2024_Consumption_tables.xlsx, TableC2023.xlsx).
This project is for academic use; please refer to the official publications for authoritative figures.

---

## Timeline

| Period   | Task                                  |
|----------|---------------------------------------|
| Jun 2025 | Topic selection & literature review   |
| Jul 2025 | Data collection & system architecture |
| Aug 2025 | System development & user evaluation  |
| Sep 2025 | Final optimization & feature testing  |

---

## Future Work

- Add scenario modelling (e.g., fuel switching, price sensitivity, sector policies)
- Enrich anomaly logic (seasonality, SARIMAX residuals)
- Add forecasting (Prophet / sklearn pipelines)
- Optional auth + saved dashboards for repeat users

---

## Author
Xinyu Dai

Email: xinyudai2002.career@gmail.com
