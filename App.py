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

##CMPD Arrests by Race from 2020-2021
st.subheader('CMPD Arrests by Race from 2020-2021')

cmpd_data = cmpd_data[cmpd_data['Result_of_Stop']=='Arrest']

cmpd_data_black = cmpd_data[cmpd_data['Driver_Race']=='Black']
cmpd_data_white = cmpd_data[cmpd_data['Driver_Race']=='White']
cmpd_data_asian = cmpd_data[cmpd_data['Driver_Race']=='Asian']
cmpd_data_native = cmpd_data[cmpd_data['Driver_Race']=='Native American']
cmpd_data_other = cmpd_data[cmpd_data['Driver_Race']=='Other/Unknown']


print('Black: ', cmpd_data_black['Driver_Race'].count())
print('White: ', cmpd_data_white['Driver_Race'].count())
print('Asian: ', cmpd_data_asian['Driver_Race'].count())
print('Native American: ', cmpd_data_native['Driver_Race'].count())
print('Other/Unknown: ', cmpd_data_other['Driver_Race'].count())