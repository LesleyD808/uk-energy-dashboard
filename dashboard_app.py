import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Unified settings for static maps: PNG, zoom, etc.
try:
    current = dict(getattr(pio.defaults, "to_image", {}) or {})
    current.setdefault("format", "png")
    current.setdefault("scale", 2)
    current["engine"] = "kaleido"
    current["chromium_args"] = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
    pio.defaults.to_image = current
except Exception:
    pass  # Some versions don't have defaults.to_image

# Backward compatibility
try:
    if hasattr(pio, "kaleido") and hasattr(pio.kaleido, "scope"):
        # Some versions still require this
        pio.kaleido.scope.chromium_args = ("--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu")
        pio.kaleido.scope.default_format = "png"
        pio.kaleido.scope.default_scale = 2
except Exception:
    pass

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
st.markdown("<h1>UK Final Energy Consumption Dashboard</h1>", unsafe_allow_html=True)

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
        showlegend=False,
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
electricity_price_per_kwh = 0.10
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
# ==================== Report: helpers ====================
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Domain hints
REASON_BY_FUEL_DIRECTION = {
    ("Coal", "up"):
        "Coal use rose due to gas price spikes and security-of-supply concerns, temporary coal plant reactivation, and fuel switching by energy-intensive industry while low-carbon capacity was constrained.",
    ("Coal", "down"):
        "Coal declined under phase-out policies and carbon pricing, closures of coal plants and coking capacity, tighter air-quality rules, and sustained switching to gas and electricity across power and industry.",

    ("Coke and breeze", "up"):
        "Coke demand increased with stronger blast-furnace steel output, limited scrap availability that slowed shifts to EAF routes, and delays in decarbonisation projects at integrated mills.",
    ("Coke and breeze", "down"):
        "Coke use fell as steelmaking restructured toward electric-arc furnaces, air-quality and carbon rules tightened, and integrated capacity was rationalised or operated at lower load.",

    ("Natural gas", "up"):
        "Natural gas rose through coal-to-gas switching, expansion of the gas grid and boilers, CCGT growth in power, and favourable relative fuel prices versus coal and oil.",
    ("Natural gas", "down"):
        "Gas demand fell with efficiency upgrades, heat-pump adoption, tighter building codes, high gas prices, industrial output weakness, and warmer winters reducing space-heating needs.",

    ("Electricity", "up"):
        "Electricity increased with electrification of transport, heating and industry, heat-pump and EV uptake, data-centre growth, and population or income effects outpacing efficiency gains.",
    ("Electricity", "down"):
        "Electricity use declined as appliance and building standards improved, economic slowdown reduced activity, rooftop PV increased self-consumption, and mild winters and behaviour changes curbed demand.",

    ("Bioenergy & waste", "up"):
        "Bioenergy grew through landfill diversion, biomass co-firing, waste-to-energy projects, renewable incentives, and combined heat-and-power deployment in municipal and industrial sites.",
    ("Bioenergy & waste", "down"):
        "Bioenergy fell as subsidies expired, biomass supply tightened, air-quality limits constrained plants, and stricter carbon accounting reduced eligibility for projects.",

    ("Petroleum products", "up"):
        "Oil products rose with travel and freight rebounds, aviation recovery, relatively low oil prices, and modal shifts back to private transport.",
    ("Petroleum products", "down"):
        "Oil products declined with tighter vehicle efficiency standards, EV adoption and charging rollout, public-transport and active-travel shifts, higher fuel taxes, and teleworking.",

    ("Other solid fuels", "up"):
        "Other solids increased due to specific industrial process needs, temporary substitution for gas amid price or supply shocks, and short-term fuel availability constraints.",
    ("Other solid fuels", "down"):
        "Other solids declined with the phase-out of legacy industrial fuels, emissions compliance costs, and process modernisation eliminating solid-fuel steps.",

    ("Town gas", "up"):
        "A rise in town gas usually reflects data quirks or small heritage networks; widespread manufactured gas was historically replaced by natural gas decades ago.",
    ("Town gas", "down"):
        "Town gas fell as remaining manufactured-gas services were retired or metered more accurately, leaving only residual or statistical balancing quantities.",
}
# Generic fallback
DEFAULT_REASON = {
    "up":   "The increase likely reflects activity growth, substitution from other fuels, relative price advantages, and policy or technology shifts favouring this fuel.",
    "down": "The decrease likely reflects efficiency gains, substitution to lower-carbon options, price pressures, environmental compliance, and structural economic changes.",
}


def compute_compare_summary(df, sector, year_a, year_b):
    a = df[(df['Sector']==sector) & (df['Year']==year_a)][['Fuel','Consumption_ktoe']].rename(columns={'Consumption_ktoe':f'Consumption_ktoe_{year_a}'})
    b = df[(df['Sector']==sector) & (df['Year']==year_b)][['Fuel','Consumption_ktoe']].rename(columns={'Consumption_ktoe':f'Consumption_ktoe_{year_b}'})
    out = pd.merge(a, b, on='Fuel', how='outer')
    out[[f'Consumption_ktoe_{year_a}', f'Consumption_ktoe_{year_b}']] = out[[f'Consumption_ktoe_{year_a}', f'Consumption_ktoe_{year_b}']].fillna(0.0)

    out['Change_ktoe'] = out[f'Consumption_ktoe_{year_b}'] - out[f'Consumption_ktoe_{year_a}']
    # Avoid dividing by zero
    def pct(row):
        base = row[f'Consumption_ktoe_{year_a}']
        return None if base == 0 else (row['Change_ktoe'] / base) * 100
    out['Change_%'] = out.apply(pct, axis=1)

    # Sorted display (largest absolute change first)
    out = out.sort_values('Change_ktoe', ascending=False).reset_index(drop=True)
    return out

def make_change_bar(summary_df, sector, year_a, year_b):
    # a bar chart based on %
    tmp = summary_df.copy()
    tmp['Change_%_num'] = tmp['Change_%'].fillna(0)
    fig = px.bar(
        tmp, x='Fuel', y='Change_%_num',
        title=f"{sector}: Change % by fuel ({year_a} → {year_b})"
    )
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
    fig.update_yaxes(title="Change %")
    return fig

import plotly.graph_objects as go

def _figure_for_pdf(fig: go.Figure, width=900, height=520, scale=2) -> bytes:
    """Change the figure to black text on a white background and export it as a PNG (for ReportLab)"""
    fig = fig.to_dict()
    fig = go.Figure(fig)
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        width=width,
        height=height,
        margin=dict(l=40, r=20, t=60, b=40)
    )
    # set the axes to black
    fig.update_xaxes(showgrid=True, gridcolor="#e6e6e6", zeroline=False, color="black")
    fig.update_yaxes(showgrid=True, gridcolor="#e6e6e6", zeroline=False, color="black", title="Change %")
    return fig.to_image(format="png", scale=scale)

def _kpi_paragraph(summary_df, sector, year_a, year_b, styles):
    total_a = summary_df[f'Consumption_ktoe_{year_a}'].sum()
    total_b = summary_df[f'Consumption_ktoe_{year_b}'].sum()
    if total_a == 0:
        total_pct = "n/a"
    else:
        total_pct = f"{(total_b-total_a)/total_a*100:+.2f}%"
    text = (f"<b>Sector:</b> {sector} &nbsp;&nbsp; "
            f"<b>Period:</b> {year_a} → {year_b} &nbsp;&nbsp; "
            f"<b>Total:</b> {total_a:,.0f} → {total_b:,.0f} ktoe "
            f"(<b>{total_pct}</b>)")
    return Paragraph(text, styles['Normal'])

def _reason_for(fuel_name: str, direction: str) -> str:
    """direction: 'up' or 'down'"""
    return REASON_BY_FUEL_DIRECTION.get((fuel_name, direction),
                                        DEFAULT_REASON[direction])

def _top_change_paragraphs(summary_df, styles):
    # Exclude total and only look at specific fuels
    dfp = summary_df[~summary_df['Fuel'].str.lower().str.contains('total', na=False)].copy()
    dfp = dfp[~dfp['Change_%'].isna()]
    if dfp.empty:
        return [Paragraph("No valid percentage changes available.", styles['Normal'])]

    # Maximum % increase & decrease
    top_up = dfp.sort_values('Change_%', ascending=False).iloc[0]
    top_dn = dfp.sort_values('Change_%').iloc[0]

    up_reason = _reason_for(top_up['Fuel'], "up")
    dn_reason = _reason_for(top_dn['Fuel'], "down")

    p1_txt = (
        f"<b>Largest % increase:</b> {top_up['Fuel']} "
        f"({top_up['Change_%']:+.2f}%, {top_up['Change_ktoe']:+,.0f} ktoe). "
        f"{up_reason}"
    )
    p2_txt = (
        f"<b>Largest % decrease:</b> {top_dn['Fuel']} "
        f"({top_dn['Change_%']:+.2f}%, {top_dn['Change_ktoe']:+,.0f} ktoe). "
        f"{dn_reason}"
    )

    return [Paragraph(p1_txt, styles['BodySmall']),
            Paragraph(p2_txt, styles['BodySmall'])]

def _summary_table(summary_df, year_a, year_b):
    data = [["Fuel", f"ktoe {year_a}", f"ktoe {year_b}", "Δ ktoe", "Δ %"]]
    for _, r in summary_df.iterrows():
        pct = "n/a" if pd.isna(r['Change_%']) else f"{r['Change_%']:.2f}%"
        data.append([
            r['Fuel'],
            f"{r[f'Consumption_ktoe_{year_a}']:,.2f}",
            f"{r[f'Consumption_ktoe_{year_b}']:,.2f}",
            f"{r['Change_ktoe']:+,.2f}",
            pct
        ])
    t = Table(data, hAlign="LEFT", colWidths=[150, 90, 90, 80, 70])
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2e3a46")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
        ("ALIGN", (1,1), (-1,-1), "RIGHT"),
    ]))
    return t

def build_pdf_report(summary_df, sector, year_a, year_b, change_bar_png: bytes):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=28, rightMargin=28, topMargin=28, bottomMargin=28)

    styles = getSampleStyleSheet()

    # a new style name that doesn't conflict
    if 'BodySmall' not in styles.byName:
        styles.add(ParagraphStyle(
            name='BodySmall',
            parent=styles['BodyText'],   # Inherits BodyText
            fontSize=10,
            leading=14
        ))

    story = []
    story.append(Paragraph(f"UK Final Energy Consumption — {sector} ({year_a} vs {year_b})", styles['Title']))
    story.append(Spacer(1, 8))
    story.append(_kpi_paragraph(summary_df, sector, year_a, year_b, styles))
    story.append(Spacer(1, 10))

    story.append(_summary_table(summary_df, year_a, year_b))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Change % by fuel", styles['Heading3']))
    story.append(Spacer(1, 6))
    story.append(Image(BytesIO(change_bar_png), width=460, height=280))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Highlights", styles['Heading3']))
    for p in _top_change_paragraphs(summary_df, styles):
        story.append(p)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<i>Disclaimer: Percentage changes are relative to the base year values; "
        "n/a indicates zero base. The analyses presented here suggest plausible drivers based on contextual evidence. They are intended as interpretative insights rather than definitive causal claims.</i>",
        styles['BodySmall']
    ))

    doc.build(story)
    return buf.getvalue()
# ==================== /helpers ====================
# --- Button: Generate PDF Report ---
st.markdown("#### 📝 Generate PDF report")

if year_a != year_b:
    # Reuse the df_compare function we calculated in Compare Two Years:
    compare_df = compute_compare_summary(df, selected_sector, year_a, year_b)

    # Draw a "Change % by fuel" chart
    fig_change = make_change_bar(compare_df, selected_sector, year_a, year_b)  # for display only
    change_png = _figure_for_pdf(fig_change)  # exports the white background version to PDF

    if st.button("Generate & download PDF"):
        pdf_bytes = build_pdf_report(compare_df, selected_sector, year_a, year_b, change_png)
        st.download_button(
            label="⬇️ Download report",
            data=pdf_bytes,
            file_name=f"{selected_sector}_{year_a}_vs_{year_b}.pdf",
            mime="application/pdf"
        )
else:
    st.info("Select two different years first.")
