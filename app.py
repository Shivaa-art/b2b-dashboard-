import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="B2B Revenue Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS (UI DESIGN) ----------------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #1f2937, #111827);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
        text-align: center;
    }
    .metric-title {
        font-size: 16px;
        color: #9ca3af;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #22c55e;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_excel("B2B_Client_Dataset_1000.xlsx")

# ---------------- HEADER ----------------
st.markdown('<p class="title">📊 B2B Revenue Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown("#### Real-time Client Engagement & Revenue Insights")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Filter Panel")

industry = st.sidebar.multiselect(
    "Select Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region))
]

# ---------------- KPI SECTION ----------------
total_clients = len(filtered_df)
avg_engagement = filtered_df["Engagement_Score"].mean()
total_revenue = filtered_df["Revenue"].sum()
retention_rate = (filtered_df["Retention_Status"] == "Retained").mean() * 100

col1, col2, col3, col4 = st.columns(4)

def metric_card(title, value):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

col1.markdown(metric_card("👥 Total Clients", total_clients), unsafe_allow_html=True)
col2.markdown(metric_card("📊 Avg Engagement", round(avg_engagement, 2)), unsafe_allow_html=True)
col3.markdown(metric_card("💰 Revenue", f"₹{total_revenue:,}"), unsafe_allow_html=True)
col4.markdown(metric_card("🔄 Retention Rate", f"{round(retention_rate,2)}%"), unsafe_allow_html=True)

st.markdown("---")

# ---------------- CHARTS ----------------

colA, colB = st.columns(2)

with colA:
    st.subheader("📊 Engagement by Industry")
    fig1 = px.bar(
        filtered_df.groupby('Industry')['Engagement_Score'].mean().reset_index(),
        x='Industry',
        y='Engagement_Score',
        color='Industry',
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.subheader("📈 Revenue Trend")
    fig2 = px.line(
        filtered_df,
        y='Revenue',
        template='plotly_dark',
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- FULL WIDTH CHART ----------------
st.subheader("🔄 Retention Analysis")

fig3 = px.pie(
    filtered_df,
    names='Retention_Status',
    template='plotly_dark',
    hole=0.4
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- LOW ENGAGEMENT ----------------
st.markdown("### ⚠️ Low Engagement Clients (Risk Zone)")

low_engagement = filtered_df[filtered_df["Engagement_Score"] < 50]

st.dataframe(low_engagement, use_container_width=True)

# ---------------- INSIGHTS PANEL ----------------
st.markdown("### 💡 Executive Insights")

st.info("""
• High engagement clients generate significantly more revenue  
• Low engagement clients are at high risk of churn  
• Retention is strongest in industries with consistent meetings  
• Strategic focus on engagement can improve profitability  
""")
