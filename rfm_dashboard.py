
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------
# 📥 Load RFM data
# -----------------------------------------
rfm = pd.read_csv('rfm_segments.csv')

# -----------------------------------------
# 🎨 Dashboard Styling
# -----------------------------------------
st.set_page_config(page_title="CLV Dashboard", page_icon="💸", layout="wide")
st.title("💸 Customer Segmentation, CLV & Churn Dashboard")

# -----------------------------------------
# 📊 KPI Summary Cards
# -----------------------------------------
total_customers = len(rfm)
gold_customers = len(rfm[rfm['Segment'] == 'Gold'])
avg_clv = rfm['CLV_6M'].mean(skipna=True)
total_predicted_revenue = rfm['CLV_6M'].sum(skipna=True)

# 🔥 Churn Calculation
churn_threshold = st.sidebar.slider("📆 Churn Threshold (days)", 90, 365, 180)
churned_mask = rfm['Recency'] > churn_threshold
churned_customers = rfm[churned_mask]
active_customers = rfm[~churned_mask]
churn_rate = round(len(churned_customers) / total_customers * 100, 2)

# 🧪 Filters
show_clv_only = st.sidebar.checkbox("💸 Show only customers with CLV", value=False)
show_churn_only = st.sidebar.checkbox("📉 Show only churned customers", value=False)
segment = st.sidebar.selectbox("🎯 Select Segment", ['All'] + sorted(rfm['Segment'].unique().tolist()))

# Apply Filters
filtered = rfm.copy()
if show_clv_only:
    filtered = filtered[filtered['CLV_6M'].notnull()]
if show_churn_only:
    filtered = filtered[churned_mask]
if segment != 'All':
    filtered = filtered[filtered['Segment'] == segment]

# 🚩 Display KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("👥 Total Customers", f"{total_customers}")
col2.metric("🏆 Gold Customers", f"{gold_customers}")
col3.metric("💰 Avg CLV (6M)", f"${avg_clv:.2f}")
col4.metric("📈 Predicted Revenue (6M)", f"${total_predicted_revenue:.2f}")
col5.metric("📉 Churn Rate", f"{churn_rate}%")

# 📄 Data Table
st.subheader("📄 Filtered Customer Data")
st.dataframe(filtered[['customer_id', 'Recency', 'Frequency', 'Monetary',
                       'RFM_Score', 'Segment', 'Predicted_Purchases_6M', 
                       'Predicted_Avg_Monetary', 'CLV_6M']], height=400)

# 📊 Charts
st.subheader("📊 Insights")
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("**Segment Distribution**")
    fig1, ax1 = plt.subplots(figsize=(4,3))
    seg_counts = rfm['Segment'].value_counts()
    sns.barplot(x=seg_counts.index, y=seg_counts.values, palette="viridis", ax=ax1)
    ax1.set_title("Customer Segments")
    st.pyplot(fig1)

with chart2:
    st.markdown("**Active vs Churned Customers**")
    fig2, ax2 = plt.subplots(figsize=(4,3))
    ax2.pie([len(active_customers), len(churned_customers)],
            labels=["Active", "Churned"],
            autopct="%1.1f%%", startangle=90,
            colors=["#2ecc71", "#e74c3c"],
            wedgeprops={"edgecolor":"white"})
    ax2.set_title("Customer Retention")
    st.pyplot(fig2)

# 🏆 Top 10 CLV Customers
st.subheader("🏆 Top 10 Customers by Predicted CLV (6M)")
if 'CLV_6M' in rfm.columns and rfm['CLV_6M'].notnull().sum() > 0:
    top_10 = rfm.sort_values('CLV_6M', ascending=False).head(10)
    fig3, ax3 = plt.subplots(figsize=(6,3))
    sns.barplot(y=top_10['customer_id'].astype(str), x=top_10['CLV_6M'], palette="rocket", ax=ax3)
    ax3.set_title("Top 10 Customers by CLV")
    ax3.set_xlabel("Predicted CLV")
    ax3.set_ylabel("Customer ID")
    st.pyplot(fig3)
else:
    st.info("Not enough CLV data to show top customers.")
