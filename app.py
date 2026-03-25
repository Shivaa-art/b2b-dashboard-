import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="B2B Dashboard", layout="wide")

# Load data
df = pd.read_excel("B2B_Client_Dataset_1000.xlsx")

# Title
st.title("📊 B2B Client Engagement & Revenue Dashboard")

# Sidebar Filters
st.sidebar.header("🔍 Filters")

industry = st.sidebar.multiselect("Select Industry", df["Industry"].unique(), default=df["Industry"].unique())
region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())

filtered_df = df[(df["Industry"].isin(industry)) & (df["Region"].isin(region))]

# ---------------- KPI SECTION ----------------
st.subheader("📌 Key Performance Indicators")

total_clients = len(filtered_df)
avg_engagement = filtered_df['Engagement_Score'].mean()
total_revenue = filtered_df['Revenue'].sum()
retention_rate = (filtered_df['Retention_Status'] == 'Retained').mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Clients", total_clients)
col2.metric("📊 Avg Engagement", round(avg_engagement, 2))
col3.metric("💰 Revenue", f"₹{total_revenue:,}")
col4.metric("🔄 Retention Rate", f"{round(retention_rate, 2)}%")

# ---------------- CHARTS ----------------

st.subheader("📊 Engagement by Industry")
fig1 = px.bar(filtered_df.groupby('Industry')['Engagement_Score'].mean().reset_index(),
              x='Industry', y='Engagement_Score', color='Industry', title="Engagement Score by Industry")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📈 Revenue Trend")
fig2 = px.line(filtered_df, y='Revenue', title="Revenue Trend", markers=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🔄 Retention Analysis")
fig3 = px.pie(filtered_df, names='Retention_Status', title="Retention Distribution")
st.plotly_chart(fig3, use_container_width=True)

# ---------------- LOW ENGAGEMENT ----------------
st.subheader("⚠️ Low Engagement Clients")

low_engagement = filtered_df[filtered_df['Engagement_Score'] < 50]
st.dataframe(low_engagement, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("💡 Key Insights")

st.write("""
- Higher engagement leads to higher revenue.
- Low engagement clients are at risk of churn.
- Certain industries show stronger retention.
""")
