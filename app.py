import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Agriculture Production Dashboard",
    page_icon="🌾",
    layout="wide"
)

# ---------- Load data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("crop_production.csv")
    df["Production"] = pd.to_numeric(df["Production"], errors="coerce").fillna(0)
    df["Area"] = pd.to_numeric(df["Area"], errors="coerce").fillna(0)
    df["Crop_Year"] = pd.to_numeric(df["Crop_Year"], errors="coerce").astype("Int64")
    return df

df = load_data()

# ---------- Header ----------
st.title("🌾 Agriculture Crop Production Dashboard")
st.markdown(
    "Interactive analysis of crop production in India. "
    "Use the filters in the sidebar — **all KPIs and graphs update together**."
)

# ---------- Sidebar filters ----------
st.sidebar.header("🔎 Dashboard Filters")

# State
states = sorted(df["State_Name"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Select State(s)",
    states,
    default=states
)

# Apply state first so the remaining filter options are relevant
temp = df[df["State_Name"].isin(selected_states)].copy()

# District
districts = sorted(temp["District_Name"].dropna().unique().tolist())
selected_districts = st.sidebar.multiselect(
    "Select District(s)",
    districts,
    default=[]
)

# Year
year_values = sorted(temp["Crop_Year"].dropna().astype(int).unique().tolist())
if year_values:
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=min(year_values),
        max_value=max(year_values),
        value=(min(year_values), max(year_values))
    )
else:
    selected_years = (0, 0)

# Season
seasons = sorted(temp["Season"].dropna().unique().tolist())
selected_seasons = st.sidebar.multiselect(
    "Select Season(s)",
    seasons,
    default=seasons
)

# Crop
crop_source = temp.copy()
if selected_districts:
    crop_source = crop_source[crop_source["District_Name"].isin(selected_districts)]
if selected_seasons:
    crop_source = crop_source[crop_source["Season"].isin(selected_seasons)]

crops = sorted(crop_source["Crop"].dropna().unique().tolist())
selected_crops = st.sidebar.multiselect(
    "Select Crop(s)",
    crops,
    default=[]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Every chart uses the same filtered dataset. "
    "Changing a sidebar option updates the complete dashboard."
)

# ---------- Apply ALL filters to one dataframe ----------
filtered_df = df[
    df["State_Name"].isin(selected_states)
    & df["Crop_Year"].between(selected_years[0], selected_years[1])
    & df["Season"].isin(selected_seasons)
].copy()

if selected_districts:
    filtered_df = filtered_df[
        filtered_df["District_Name"].isin(selected_districts)
    ]

if selected_crops:
    filtered_df = filtered_df[
        filtered_df["Crop"].isin(selected_crops)
    ]

# ---------- Empty result check ----------
if filtered_df.empty:
    st.warning("No data matches the selected filters. Please change the sidebar selections.")
    st.stop()

# ---------- KPI calculations ----------
total_production = filtered_df["Production"].sum()
total_area = filtered_df["Area"].sum()
number_of_crops = filtered_df["Crop"].nunique()
number_of_states = filtered_df["State_Name"].nunique()

# ---------- KPI cards ----------
c1, c2, c3, c4 = st.columns(4)

c1.metric("🌾 Total Production", f"{total_production:,.0f}")
c2.metric("📐 Total Area", f"{total_area:,.0f}")
c3.metric("🌱 Number of Crops", f"{number_of_crops:,}")
c4.metric("📍 States Covered", f"{number_of_states:,}")

st.markdown("---")

# ---------- Chart 1: Production by year ----------
year_data = (
    filtered_df.groupby("Crop_Year", as_index=False)["Production"]
    .sum()
    .sort_values("Crop_Year")
)

fig_year = px.line(
    year_data,
    x="Crop_Year",
    y="Production",
    markers=True,
    title="📈 Total Crop Production by Year",
    labels={"Crop_Year": "Year", "Production": "Production"}
)
fig_year.update_layout(height=430)
st.plotly_chart(fig_year, use_container_width=True)

# ---------- Charts 2 and 3 ----------
col1, col2 = st.columns(2)

# Production by crop
crop_data = (
    filtered_df.groupby("Crop", as_index=False)["Production"]
    .sum()
    .sort_values("Production", ascending=False)
    .head(10)
)

fig_crop = px.bar(
    crop_data,
    x="Production",
    y="Crop",
    orientation="h",
    title="🌱 Top 10 Crops by Production",
    labels={"Production": "Production", "Crop": "Crop"}
)
fig_crop.update_layout(height=500, yaxis={"categoryorder": "total ascending"})

with col1:
    st.plotly_chart(fig_crop, use_container_width=True)

# Production by state
state_data = (
    filtered_df.groupby("State_Name", as_index=False)["Production"]
    .sum()
    .sort_values("Production", ascending=False)
    .head(10)
)

fig_state = px.bar(
    state_data,
    x="Production",
    y="State_Name",
    orientation="h",
    title="🗺️ Top 10 States by Production",
    labels={"Production": "Production", "State_Name": "State"}
)
fig_state.update_layout(height=500, yaxis={"categoryorder": "total ascending"})

with col2:
    st.plotly_chart(fig_state, use_container_width=True)

# ---------- Charts 4 and 5 ----------
col3, col4 = st.columns(2)

# Area vs Production
scatter_data = filtered_df.copy()
if len(scatter_data) > 15000:
    scatter_data = scatter_data.sample(15000, random_state=42)

fig_scatter = px.scatter(
    scatter_data,
    x="Area",
    y="Production",
    color="Season",
    hover_data=["State_Name", "District_Name", "Crop", "Crop_Year"],
    title="📊 Area vs Production",
    labels={"Area": "Cultivated Area", "Production": "Production"}
)
fig_scatter.update_layout(height=500)

with col3:
    st.plotly_chart(fig_scatter, use_container_width=True)

# Season production
season_data = (
    filtered_df.groupby("Season", as_index=False)["Production"]
    .sum()
    .sort_values("Production", ascending=False)
)

fig_season = px.pie(
    season_data,
    names="Season",
    values="Production",
    title="🥕 Production Distribution by Season",
    hole=0.35
)
fig_season.update_layout(height=500)

with col4:
    st.plotly_chart(fig_season, use_container_width=True)

# ---------- Crop-area summary ----------
st.markdown("---")
st.subheader("📋 Crop Production Summary")

summary = (
    filtered_df.groupby("Crop", as_index=False)
    .agg(
        Area=("Area", "sum"),
        Production=("Production", "sum")
    )
    .sort_values("Production", ascending=False)
)

st.dataframe(summary, use_container_width=True, height=350)

# ---------- Download filtered data ----------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_agriculture_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Agriculture Data Visualization Project | Built with Python, Pandas, Plotly and Streamlit")
