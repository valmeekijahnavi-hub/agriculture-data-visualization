# 🌾 Agriculture Data Visualization Dashboard

An interactive agriculture data visualization dashboard built with **Python, Pandas, Plotly and Streamlit**.

## Dataset

The project uses `crop_production.csv`, containing Indian agricultural crop production data.

Main columns:

- `State_Name`
- `District_Name`
- `Crop_Year`
- `Season`
- `Crop`
- `Area`
- `Production`

## Dashboard Features

The sidebar contains interactive filters for:

- State
- District
- Year range
- Season
- Crop

### Important feature

All dashboard elements use the same filtered dataset. Therefore, when a user changes a sidebar filter, the **KPI cards, line chart, bar charts, scatter plot, pie chart and summary table all update automatically**.

## Visualizations

1. Total crop production by year
2. Top 10 crops by production
3. Top 10 states by production
4. Cultivated area vs production scatter plot
5. Production distribution by season
6. Filtered crop production summary table

## How to Run Locally

Install Python first.

Open Command Prompt/Terminal in this project folder and run:

```bash
pip install -r requirements.txt
```

Then run:

```bash
streamlit run app.py
```
dashboard link:https://agriculture-data-visualization-hzsarpz5pxfxact8b5s4yx.streamlit.app/

The dashboard will open in your browser.

## GitHub Upload

Create a new GitHub repository and upload:

```text
app.py
crop_production.csv
requirements.txt
README.md
```

Do not upload Python's virtual environment folder (`venv`).

## Project Title

**Agriculture Data Visualization and Interactive Dashboard Using Streamlit**
