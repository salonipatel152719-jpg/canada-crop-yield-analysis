from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Canadian Crop Yield Dashboard", layout="wide")


@st.cache_data
def load_data():
    path = Path(__file__).resolve().parent.parent / "data" / "clean" / "crop_yield_clean.csv"
    return pd.read_csv(path)


df = load_data()

st.title("Canadian Crop Yield Dashboard")
st.caption(
    "Source: Statistics Canada, Table 32-10-0359-01. "
    "Yield in kilograms per hectare. 2026 values are preliminary."
)

# Sidebar filters
st.sidebar.header("Filters")
crop = st.sidebar.selectbox("Crop", sorted(df["crop"].unique()))

available = sorted(df[df["crop"] == crop]["province"].unique())
selected = st.sidebar.multiselect("Provinces", available, default=available)

year_min, year_max = int(df["year"].min()), int(df["year"].max())
years = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))

filtered = df[
    (df["crop"] == crop)
    & (df["province"].isin(selected))
    & (df["year"].between(years[0], years[1]))
]

if filtered.empty:
    st.warning("No data for this selection. Choose at least one province.")
    st.stop()

# Summary numbers
by_province = filtered.groupby("province")["yield_kg_ha"].mean().sort_values(ascending=False)
by_year = filtered.groupby("year")["yield_kg_ha"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average yield (kg/ha)", f"{filtered['yield_kg_ha'].mean():,.0f}")
col2.metric("Highest-yield province", by_province.index[0])
col3.metric("Best year", int(by_year.idxmax()))
col4.metric("Provinces shown", len(selected))

# Charts
left, right = st.columns(2)

with left:
    st.subheader(f"{crop} yield over time")
    trend = filtered.pivot(index="year", columns="province", values="yield_kg_ha")
    st.line_chart(trend)

with right:
    st.subheader("Average yield by province")
    st.bar_chart(by_province)

# Table
st.subheader("Data")
st.dataframe(
    filtered.sort_values(["province", "year"]).reset_index(drop=True),
    use_container_width=True,
)

st.caption(
    "Rankings use yield per hectare, not total production. "
    "Series with fewer than 15 years of data were excluded."
)