import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Music Royalty Analytics",
    page_icon="🎵",
    layout="wide"
)

@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account   = os.getenv("SNOWFLAKE_ACCOUNT"),
        user      = os.getenv("SNOWFLAKE_USER"),
        password  = os.getenv("SNOWFLAKE_PASSWORD"),
        role      = os.getenv("SNOWFLAKE_ROLE"),
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE"),
        database  = os.getenv("SNOWFLAKE_DATABASE"),
        schema    = "MUSIC_SCHEMA_MARTS",
    )

@st.cache_data(ttl=300)
def query(_conn, sql):
    return pd.read_sql(sql, _conn)

conn = get_connection()

# ── Header ────────────────────────────────────────
st.title("🎵 Music Royalty Analytics Platform")
st.caption("Powered by Snowflake + dbt | Refreshes every 5 minutes")

# ── Load data ─────────────────────────────────────
dq = query(conn, "SELECT * FROM mart_data_quality")
lp = query(conn, "SELECT * FROM mart_label_performance ORDER BY total_royalties DESC")
sb = query(conn, "SELECT * FROM mart_store_benchmarks ORDER BY total_value DESC")

# ── KPI row ───────────────────────────────────────
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue",    f"${lp['TOTAL_REVENUE'].sum():,.2f}")
col2.metric("Total Royalties",  f"${lp['TOTAL_ROYALTIES'].sum():,.2f}")
col3.metric("Avg Royalty Rate", f"{lp['ROYALTY_RATE_PCT'].mean():.1f}%")
col4.metric("ISRC Coverage",    f"{dq['ISRC_COVERAGE_PCT'].iloc[0]:.1f}%")

st.divider()

# ── Store performance ─────────────────────────────
st.subheader("Revenue by Store")
fig = px.bar(
    sb,
    x="STORE_NAME",
    y="TOTAL_VALUE",
    color="ROYALTY_RATE_PCT",
    color_continuous_scale="Viridis",
    labels={
        "TOTAL_VALUE": "Revenue ($)",
        "STORE_NAME": "Store",
        "ROYALTY_RATE_PCT": "Royalty Rate %"
    }
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Label performance table ───────────────────────
st.subheader("Label Performance")
st.dataframe(
    lp[[
        "LABEL_NAME", "TOTAL_REVENUE", "TOTAL_ROYALTIES",
        "ROYALTY_RATE_PCT", "CATALOG_SIZE", "STORES_PRESENT"
    ]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ── Data quality ──────────────────────────────────
st.subheader("Data Quality")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rows",      f"{dq['TOTAL_ROWS'].iloc[0]:,}")
col2.metric("ISRC Missing",    f"{dq['ISRC_MISSING'].iloc[0]:,}")
col3.metric("Unique Stores",   f"{dq['UNIQUE_STORES'].iloc[0]:,}")