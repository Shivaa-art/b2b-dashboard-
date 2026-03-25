import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="B2B Dashboard", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Background */
body {
    background-color: #0e1117;
}

/* Glass Card */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

/* KPI Card */
.kpi-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}

.kpi-title {
    color: #9ca3af;
    font-size: 14px;
}

.kpi-value {
    font-size: 26px;
    font-weight: bold;
    color: #22c55e;
}

/* Section Titles */
.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Insight Box */
.insight-box {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.4);
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_excel("B2B_Client_Dataset_1000.xlsx")

# ---------------- TITLE ----------------
st.title("📊 B2B Client Engagement & Revenue Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

industry = st.sidebar.multiselect(
    "Select Industry",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region))
]

# ---------------- KPI SECTION ----------------
st.markdown('<div class="section-title">📌 Key Performance Indicators</div>', unsafe_allow_html=True)

total_clients = len(filtered_df)
avg_engagement = filtered_df['Engagement_Score'].mean()
total_revenue = filtered_df['Revenue'].sum()
retention_rate = (filtered_df['Retention_Status'] == 'Retained').mean() * 100

col1, col2, col3, col4 = st.columns(4)

def kpi(title, value):
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """

col1.markdown(kpi("👥 Total Clients", total_clients), unsafe_allow_html=True)
col2.markdown(kpi("📊 Avg Engagement", round(avg_engagement, 2)), unsafe_allow_html=True)
col3.markdown(kpi("💰 Revenue", f"₹{total_revenue:,}"), unsafe_allow_html=True)
col4.markdown(kpi("🔄 Retention Rate", f"{round(retention_rate, 2)}%"), unsafe_allow_html=True)

# ---------------- CHARTS ----------------

colA, colB = st.columns(2)

with colA:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Engagement by Industry")
    fig1 = px.bar(
        filtered_df.groupby('Industry')['Engagement_Score'].mean().reset_index(),
        x='Industry',
        y='Engagement_Score',
        color='Industry',
        template="plotly_dark"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Revenue Trend")
    fig2 = px.line(
        filtered_df,
        y='Revenue',
        markers=True,
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RETENTION ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 🔄 Retention Analysis")

fig3 = px.pie(
    filtered_df,
    names='Retention_Status',
    template="plotly_dark",
    hole=0.4
)

st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOW ENGAGEMENT ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### ⚠️ Low Engagement Clients")

low_engagement = filtered_df[filtered_df['Engagement_Score'] < 50]
st.dataframe(low_engagement, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INSIGHTS ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### 💡 Executive Insights")

st.markdown("""
<div class="insight-box">
• High engagement clients generate significantly higher revenue<br>
• Low engagement clients are at high risk of churn<br>
• Retention is stronger in industries with frequent interaction<br>
• Increasing engagement directly improves business performance
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
