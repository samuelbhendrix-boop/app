import streamlit as st
import pandas as pd
import plotly.express as px
import json

# -------------------------------
# Load public data
# -------------------------------
@st.cache_data
def load_market_share():
    return pd.read_csv("data/market_share.csv")

@st.cache_data
def load_plans():
    with open("data/plans.json") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_competitors():
    with open("data/competitors.json") as f:
        return json.load(f)

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.set_page_config(page_title="Point32Health Market Intelligence", layout="wide")

st.title("🏥 Point32Health Market Intelligence Dashboard")
st.markdown("""
This dashboard uses **publicly available data** (Massachusetts Division of Insurance, AMA reports, CMS Marketplace PUFs) 
to provide insights into Point32Health’s products, competitors, and market share.
""")

# Sidebar filters
st.sidebar.header("Filters")
segment = st.sidebar.selectbox("Segment", ["Small Group", "Large Group", "ACA Marketplace"])
product_type = st.sidebar.selectbox("Product Type", ["HMO", "PPO", "Tiered", "Limited"])

# -------------------------------
# Market Share Visualization
# -------------------------------
st.subheader("📊 Massachusetts HMO Market Share")
market_share_df = load_market_share()
fig = px.pie(market_share_df, names="Carrier", values="MarketShare", title="HMO Market Share (Massachusetts)")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Plan Comparison
# -------------------------------
st.subheader("⚖️ Plan Comparison")
plans_df = load_plans()
filtered_plans = plans_df[(plans_df["segment"] == segment) & (plans_df["product_type"] == product_type)]
st.dataframe(filtered_plans[[
    "carrier", "plan_name", "product_type", "segment",
    "deductible_individual", "oop_max_individual",
    "premium_index", "network_breadth_index"
]])

# -------------------------------
# Competitor Profiles
# -------------------------------
st.subheader("🏆 Competitor Profiles")
competitors = load_competitors()
for comp in competitors:
    st.markdown(f"### {comp['carrier']}")
    st.markdown(f"- **Strengths:** {', '.join(comp['strengths'])}")
    st.markdown(f"- **Weaknesses:** {', '.join(comp['weaknesses'])}")

# -------------------------------
# Insights
# -------------------------------
st.subheader("🔎 Key Insights")
st.markdown("""
- Point32Health holds ~20–25% of the Massachusetts HMO market.
- Blue Cross Blue Shield of MA dominates with ~40–45%.
- Tiered/limited network products are Point32Health’s differentiator.
- National carriers (Aetna, UHC) have smaller shares but broader networks.
""")
