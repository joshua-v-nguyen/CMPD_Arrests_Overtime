import geopandas as gpd
import pandas as pd
import streamlit as st

cmpd_data = pd.read_csv('Data\Officer_Traffic_Stops.csv')

st.title("Police Traffic Stops")
