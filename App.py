import altair as alt
import geopandas as gpd
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()
cmpd_data = pd.read_csv('Data\Officer_Traffic_Stops.csv')

st.title("Police Traffic Stops")

chart = alt.Chart(cmpd_data).mark_bar().encode(
    alt.X("Driver_Age:Q", bin=True),
    y='count()',
)

st.altair_chart(chart)