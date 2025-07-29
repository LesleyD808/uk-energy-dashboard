import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------- Page Config ----------------
st.set_page_config(page_title="UK Energy Dashboard", layout="wide")

# ---------------- Background Style ----------------
st.markdown("""
    <style>
        body {
            background-color: #111111;
        }
        .main {
            background-color: #111111;
            padding: 30px;
        }
        h1 {
            color: white;
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
        }
        .stPlotlyChart > div {
            background-color: rgba(255, 255, 255, 0.04) !important;
            border-radius: 12px;
            padding: 10px;
        }
        .stDataFrame, .stTable {
            background-color: rgba(255, 255, 255, 0.04) !important;
            border-radius: 12px;
        }
        thead tr th, tbody tr td {
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- Load Data ----------------
df = pd.read_csv("Standardized_Energy_Data.csv")
df['Consumption_ktoe'] = pd.to_numeric(df['Consumption_ktoe'].astype(str).str.replace('[x]', '', regex=False), errors='coerce')

# ---------------- Sidebar ----------------
st.sidebar.title("🔧 Controls")
sectors = sorted(df['Sector'].dropna().unique())
years = sorted(df['Year'].dropna().unique().astype(int))
selected_sector = st.sidebar.selectbox("Select Sector", sectors)
selected_year = st.sidebar.selectbox("Select Year", years)

# ---------------- Title ----------------
st.markdown("<h1>🇬🇧 UK Final Energy Consumption Dashboard</h1>", unsafe_allow_html=True)

# ---------------- Filter Data ----------------
df_sector = df[df['Sector'] == selected_sector]
df_year = df[df['Year'] == selected_year]
df_sector_year = df_sector[df_sector['Year'] == selected_year]
df_sector_sum = df[df['Year'] == selected_year].groupby('Sector')['Consumption_ktoe'].sum().reset_index()

# ---------------- Line Chart with Anomaly Highlight ----------------
window_years = 5
highlight = []
for fuel in df_sector['Fuel'].unique():
    df_fuel = df_sector[df_sector['Fuel'] == fuel].sort_values(by='Year')
    for i in range(window_years, len(df_fuel)):
        current = df_fuel.iloc[i]
        past_mean = df_fuel.iloc[i-window_years:i]['Consumption_ktoe'].mean()
        if current['Consumption_ktoe'] > 1.2 * past_mean:
            highlight.append((fuel, current['Year'], current['Consumption_ktoe']))

fig1 = px.line(df_sector, x="Year", y="Consumption_ktoe", color="Fuel",
               title=f"{selected_sector}: Energy Consumption Trend by Fuel (1970–2023)",
               markers=True)
for fuel, year, value in highlight:
    fig1.add_trace(go.Scatter(
        x=[year], y=[value],
        mode='markers',
        marker=dict(color='red', size=12, symbol='triangle-up'),
        showlegend=False,  # 🚫 不显示图例
        hovertemplate=f"Fuel={fuel}<br>Year={year}<br>Consumption={value:.0f} ktoe"
    ))

fig1.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
st.plotly_chart(fig1, use_container_width=True)

# ---------------- Heatmap + Radar Chart ----------------
col1, col2 = st.columns(2)
pivot_heat = df_year.pivot_table(index='Fuel', columns='Sector', values='Consumption_ktoe', aggfunc='sum')
fig_heat = px.imshow(pivot_heat, text_auto=True, color_continuous_scale='YlOrRd',
                     title=f"Heatmap: Sector vs Fuel ({selected_year})")
fig_heat.update_layout(paper_bgcolor='black', font_color='white')
col1.plotly_chart(fig_heat, use_container_width=True)

radar_df = df_sector_year.dropna()
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=radar_df['Consumption_ktoe'],
    theta=radar_df['Fuel'],
    fill='toself',
    name='Fuel Share'
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False,
    title="Radar Chart: Fuel Composition",
    paper_bgcolor='black', font_color='white'
)
col2.plotly_chart(fig_radar, use_container_width=True)

# ---------------- Scatter + Box Chart ----------------
col3, col4 = st.columns(2)
fig_scatter = px.scatter(df, x="Year", y="Consumption_ktoe", color="Sector", hover_data=["Fuel"],
                         title="All Sectors: Consumption over Time")
fig_scatter.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
col3.plotly_chart(fig_scatter, use_container_width=True)

fig_box = px.box(df_sector, x="Fuel", y="Consumption_ktoe", points="all",
                 title=f"Box Plot: {selected_sector} Fuel Distribution (1970–2023)")
fig_box.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
col4.plotly_chart(fig_box, use_container_width=True)

# ---------------- Yearly Calendar Heatmap ----------------
st.markdown("### 📆 Yearly Calendar Heatmap")
pivot_year = df[df['Sector'] == selected_sector].pivot_table(
    index='Fuel', columns='Year', values='Consumption_ktoe', aggfunc='sum')
fig_year = px.imshow(pivot_year, color_continuous_scale='Viridis',
                     title=f"{selected_sector} - Yearly Fuel Usage")
fig_year.update_layout(paper_bgcolor='black', font_color='white')
st.plotly_chart(fig_year, use_container_width=True)

# ---------------- Cost Estimation ----------------
st.subheader("💰 Cost Estimation")
electricity_price_per_kwh = 0.34
conversion_factor = 11630
df_cost = df_sector_year.copy()
df_cost['Cost (£)'] = df_cost['Consumption_ktoe'] * conversion_factor * electricity_price_per_kwh
styled_cost = df_cost[['Fuel', 'Consumption_ktoe', 'Cost (£)']].style.format({
    'Consumption_ktoe': '{:,.0f}',
    'Cost (£)': '£{:,.2f}'
}).set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center')]},
    {'selector': 'td', 'props': [('text-align', 'center')]},
], overwrite=False)
st.table(styled_cost)

# ---------------- Yearly Comparison ----------------
st.subheader("📊 Compare Two Years")
col_a, col_b = st.columns(2)
with col_a:
    year_a = st.selectbox("Compare Year A", years, index=0)
with col_b:
    year_b = st.selectbox("Compare Year B", years, index=len(years)-1)

if year_a != year_b:
    df_a = df[(df['Year'] == year_a) & (df['Sector'] == selected_sector)]
    df_b = df[(df['Year'] == year_b) & (df['Sector'] == selected_sector)]
    df_compare = pd.merge(
        df_a[['Fuel', 'Consumption_ktoe']],
        df_b[['Fuel', 'Consumption_ktoe']],
        on='Fuel', suffixes=(f'_{year_a}', f'_{year_b}')
    )
    df_compare['Change (%)'] = ((df_compare[f'Consumption_ktoe_{year_b}'] - df_compare[f'Consumption_ktoe_{year_a}']) /
                                 df_compare[f'Consumption_ktoe_{year_a}']) * 100
    formatted = df_compare.copy()
    for col in formatted.columns[1:]:
        formatted[col] = formatted[col].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "—")
    styled_compare = formatted.style.set_properties(**{'text-align': 'center'}).set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]},
    ])
    st.table(styled_compare)
else:
    st.warning("Please select two different years for comparison.")
