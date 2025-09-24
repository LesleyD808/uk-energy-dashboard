# uk-energy-dashboard
Streamlit-based dashboard for UK final energy consumption visualization
# uk-energy-dashboard

A Streamlit-powered dashboard to explore **UK final energy consumption** with interactive trends, year-to-year comparisons, and one-click PDF export.

**🔗 Live app:** https://uk-energy-dashboard-56xuus4qga5eeb8zpa7dh5.streamlit.app/  
*(No local setup required — open and use in the browser.)*

---

## ✨ Features

- **Interactive Trend View** – filter by sector/fuel and explore multi-year consumption trends.  
- **Year-to-Year Comparison** – compare adjacent years side-by-side and see deltas immediately.  
- **Downloadable Report** – export the current view to a **PDF** for sharing/citations.  
- **Clean, standardized data** – ECUK tables are pre-processed for consistent analysis.  

> The app emphasizes clarity & reproducibility: a minimal UI, transparent data prep, and exportable insights.

---

## 🧪 User Evaluation (Questionnaire)

A short **questionnaire-based user evaluation** validated usability and usefulness with non-expert users.

- Participants used the **live dashboard** and then completed a **Likert-scale** survey + **open-ended** questions.  
- Feedback focused on the clarity of the **Trend View**, usefulness of **Year-to-Year** comparison, and the value of **PDF export** for coursework/reports.  
- Suggestions implemented: clearer legends, persistent filters across pages, and additional sector presets.

> The questionnaire materials (form and anonymized responses) are in **`/User Study/`**.

---

## 🖼️ Screenshots

| Trend View | Year-to-Year Comparison | PDF Export |
|---|---|---|
| ![Trend](screenshots/Trend%20View.png) | ![Y2Y](screenshots/Year-to-Year%20Comparison.png) | ![PDF](screenshots/PDF%20Export.png) |

> Place images in the `screenshots/` folder with the above filenames (spaces URL-encoded as shown) so links resolve.

---

## 🗂️ Project Structure
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

## 🛠️ Tech Stack

- **App:** Python, **Streamlit**  
- **Viz:** Altair/Plotly (via Streamlit), PDF export utilities  
- **Data:** ECUK (UK Govt / BEIS) + curated CSV/XLSX  
- **Repro:** `requirements.txt`

---

## ▶️ How to Use

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

---

## 📊 Data & Pre-processing

Primary data: ECUK 2024 consumption tables (`ECUK_2024_Consumption_tables.xlsx`, `TableC2023.xlsx`).  

Cleaning/standardization workflow lives in `preprocess_energy_data.py` and produces `Standardized_Energy_Data.csv` used by the app.  

Electricity price references are provided for contextual analyses.

---

## 🔍 Key Pages

- **Trend View** – long-term consumption with filters & hover cues.  
- **Year-to-Year Comparison** – adjacent-year deltas to surface changes quickly.  
- **Report Export** – generate a PDF snapshot of the current state.  

---

## 🗓️ Timeline

| Period   | Task                                  |
|----------|---------------------------------------|
| Jun 2025 | Topic selection & literature review   |
| Jul 2025 | Data collection & system architecture |
| Aug 2025 | System development & user evaluation  |
| Sep 2025 | Final optimization & feature testing  |

---

## ✅ Roadmap

- More sector presets & saved filter states  
- Additional contextual indicators (e.g., economic/weather normalization)  
- CSV export with current filters  
- Accessibility & keyboard navigation improvements  

---

## 👩‍💻 Author
Xinyu Dai

Email: xinyudai2002.career@gmail.com
