import altair as alt
import geopandas as gpd
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

#importing CMPD data
@st.cache_data
def load_data(cmpd_data):
    cmpd_data = pd.read_csv('Data\CMPD_Arrests.csv')
    return cmpd_data
cmpd_data = load_data("<path to csv>")

#import APD data
@st.cache_data
def load_data(apd_data):
    apd_data = pd.read_csv('Data\APD_Arrests.csv')
    return apd_data
apd_data = load_data("<path to csv>")

st.title("Police Traffic Stops")

#CMPD Arrests by Race from 2020
st.subheader('CMPD Arrests by Race from 2020')

#Filtering only stops that resulted in Arrest
cmpd_data = cmpd_data[cmpd_data['Result_of_Stop']=='Arrest']
#Filtering only 2020 data
cmpd_data[['Year', 'Month']] = cmpd_data['Month_of_Stop'].str.split('/', expand=True)
cmpd_data = cmpd_data[cmpd_data['Year']=='2020']

cmpd_data_black = cmpd_data['Driver_Race'].value_counts()['Black']
cmpd_data_white = cmpd_data['Driver_Race'].value_counts()['White']
cmpd_data_asian = cmpd_data['Driver_Race'].value_counts()['Asian']
cmpd_data_native = cmpd_data['Driver_Race'].value_counts()['Native American']
cmpd_data_other = cmpd_data['Driver_Race'].value_counts()['Other/Unknown']

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.write(f'Black: ', cmpd_data_black)
with col2:
    st.write(f'White: ', cmpd_data_white)
with col3:
    st.write(f'Asian: ', cmpd_data_asian)
with col4:
    st.write(f'Native American: ', cmpd_data_native)
with col5:
    st.write(f'Other/Unknown: ', cmpd_data_other)

cmpd_bar = alt.Chart(cmpd_data).mark_bar().encode(
    x=alt.X('Driver_Race',axis=alt.Axis(labelAngle=0)).sort('-y'),
    y='count()',
    color=alt.Color('Driver_Race')
).properties(
    width=600,
    height=500
)
st.altair_chart(cmpd_bar)

#APD Arrests by Race from 2020
st.subheader('APD Arrests by Race from 2020')

#Transforming APD data
apd_data["Standardized Race"]= apd_data["Standardized Race"].str.title()
apd_data = apd_data[apd_data['Type']=='Arrests']

apd_data_black = apd_data['Standardized Race'].value_counts()['Black']
apd_data_white = apd_data['Standardized Race'].value_counts()['White']
apd_data_asian = apd_data['Standardized Race'].value_counts()['Asian']
apd_data_native = apd_data['Standardized Race'].value_counts()['American Indian/Alaskan Native']

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write(f'Black: ', apd_data_black)
with col2:
    st.write(f'White: ', apd_data_white)
with col3:
    st.write(f'Asian: ', apd_data_asian)
with col4:
    st.write(f'American Indian/Alaskan Native: ', apd_data_native)

apd_bar = alt.Chart(apd_data).mark_bar().encode(
    x=alt.X('Standardized Race',axis=alt.Axis(labelAngle=0)).sort('-y'),
    y='count()',
    color=alt.Color('Standardized Race')
).properties(
    width=800,
    height=500
)
st.altair_chart(apd_bar)