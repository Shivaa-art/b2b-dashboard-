import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Executive Intelligence Dashboard", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body {background-color: #0e1117;}

.glass {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

.kpi {
    background: linear-gradient(135deg,#111827,#1f2937);
    border-radius: 15px;
    padding: 20px;
    text-align:center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
}

.kpi h3 {color:#9ca3af;}
.kpi h1 {color:#22c55e;}

.alert {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.4);
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
df = pd.read_excel("B2B_Client_Dataset_1000.xlsx")

# ---------------- HEADER ----------------
st.title("🚀 Executive Intelligence Dashboard")
st.caption("AI-Powered Client Engagement & Revenue Monitoring System")

# ---------------- TOP FILTER BAR ----------------
colf1, colf2 = st.columns(2)

with colf1:
    industry = st.multiselect("Industry", df["Industry"].unique(), default=df["Industry"].unique())

with colf2:
    region = st.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())

filtered_df = df[(df["Industry"].isin(industry)) & (df["Region"].isin(region))]

# ---------------- KPI ----------------
total_clients = len(filtered_df)
avg_engagement = filtered_df['Engagement_Score'].mean()
total_revenue = filtered_df['Revenue'].sum()
retention_rate = (filtered_df['Retention_Status'] == 'Retained').mean() * 100

# Previous simulation (for trend)
prev_engagement = df['Engagement_Score'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Clients", total_clients)
col2.metric("📊 Engagement", round(avg_engagement,2), delta=round(avg_engagement-prev_engagement,2))
col3.metric("💰 Revenue", f"₹{total_revenue:,}")
col4.metric("🔄 Retention", f"{round(retention_rate,2)}%")

# ---------------- AI INSIGHTS ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("🤖 AI Smart Insights")

insight_text = ""

if avg_engagement < 50:
    insight_text += "⚠️ Engagement is LOW — Immediate action required.\n\n"

if retention_rate < 60:
    insight_text += "⚠️ Retention rate is weak — churn risk detected.\n\n"

if total_revenue > 1000000:
    insight_text += "✅ Strong revenue performance observed.\n\n"

if insight_text == "":
    insight_text = "✅ System performing optimally with balanced engagement and retention."

st.write(insight_text)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CHARTS ----------------
colA, colB = st.columns(2)

with colA:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📊 Engagement by Industry")
    fig1 = px.bar(filtered_df.groupby('Industry')['Engagement_Score'].mean().reset_index(),
                  x='Industry', y='Engagement_Score',
                  color='Industry', template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📈 Revenue Trend")
    fig2 = px.line(filtered_df, y='Revenue', markers=True, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RETENTION ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("🔄 Retention Analysis")

fig3 = px.pie(filtered_df, names='Retention_Status', hole=0.4, template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RISK TABLE ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("🚨 High-Risk Clients (Low Engagement)")

risk_df = filtered_df[filtered_df['Engagement_Score'] < 50]

st.dataframe(risk_df.style.highlight_max(axis=0), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
