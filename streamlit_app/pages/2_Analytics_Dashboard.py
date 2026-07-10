import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (get_dashboard_summary, get_wellness_distribution,
                   get_age_group_analysis, get_health_concerns,
                   get_device_analysis, get_urban_rural)

st.set_page_config(page_title="Dashboard — ParentCare", page_icon="📊", layout="wide")
st.title("📊 Analytics Dashboard")
st.markdown("Population insights from **9,668 Indian children** in the ParentCare dataset.")
st.divider()

@st.cache_data(ttl=300)
def load():
    return {
        "summary":  get_dashboard_summary(),
        "wellness": get_wellness_distribution(),
        "age":      get_age_group_analysis(),
        "health":   get_health_concerns(),
        "devices":  get_device_analysis(),
        "urban":    get_urban_rural(),
    }

try:
    with st.spinner("Loading..."):
        data = load()
except Exception as e:
    st.error(f"Cannot connect to FastAPI. Start the server first.\n\n{e}")
    st.stop()

s = data["summary"]

# ── KPIs ─────────────────────────────────────────────────
k1,k2,k3,k4 = st.columns(4)
k1.metric("Total Children",      f"{s['total_children']:,}")
k2.metric("Avg Screen Time",     f"{s['average_screen_time']} hrs/day")
k3.metric("High Risk Children",  f"{s['high_risk_pct']}%")
k4.metric("Critical Cases",      f"{s['critical_cases']:,}")
st.divider()

# ── Chart 1: Wellness Category ────────────────────────────
# ── Chart 2: Health Concerns ──────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Wellness Category")
    w = data["wellness"]
    fig = px.bar(
        x=list(w.keys()), y=list(w.values()),
        color=list(w.keys()),
        color_discrete_map={"Critical":"#b71c1c","High Risk":"#e65100",
                            "Moderate":"#f57f17","Healthy":"#2e7d32"},
        labels={"x":"Category","y":"Children"},
    )
    fig.update_layout(showlegend=False, height=300, margin=dict(t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Health Concerns")
    hc   = data["health"]
    fig2 = px.bar(
        x=list(hc.keys()), y=list(hc.values()),
        color=list(hc.keys()),
        color_discrete_sequence=["#ef5350","#ff9800","#9c27b0","#2196f3"],
        labels={"x":"Concern","y":"Children"},
    )
    fig2.update_layout(showlegend=False, height=300, margin=dict(t=10,b=10))
    st.plotly_chart(fig2, use_container_width=True)

# ── Chart 3: Screen Time by Age ──────────────────────────
# ── Chart 4: Device Usage ─────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Screen Time by Age Group")
    adf = pd.DataFrame(data["age"])
    fig3 = px.bar(
        adf, x="Age_Group", y="avg_screen_time",
        color="avg_screen_time", color_continuous_scale="Reds",
        labels={"avg_screen_time":"Avg Hours/Day","Age_Group":"Age Group"},
    )
    fig3.update_layout(height=300, margin=dict(t=10,b=10))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Device Usage")
    ddf = pd.DataFrame(data["devices"])
    fig4 = px.bar(
        ddf, x="Primary_Device", y="avg_screen_time",
        color="avg_screen_time", color_continuous_scale="Blues",
        labels={"avg_screen_time":"Avg Hours/Day","Primary_Device":"Device"},
    )
    fig4.update_layout(showlegend=False, height=300, margin=dict(t=10,b=10))
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.caption("ParentCare Analytics | Data: ParentCare Final Dataset | 9,668 Indian children aged 8–18")
