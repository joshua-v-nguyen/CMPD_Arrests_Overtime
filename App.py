import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

#importing CMPD data
@st.cache_data
def load_data(seattle):
    df = pd.read_csv(seattle)
    return df
seattle = load_data("Seattle_Arrests.csv")
seattle = seattle[seattle['Year']<2023]
seattle = seattle[seattle['Year']>2019]
seattle = seattle[ (seattle['Subject Perceived Race'] != '-') 
                  & (seattle['Subject Perceived Race'] != 'Unknown')
                  & (seattle['Subject Perceived Race'] != 'DUPLICATE')
                  & (seattle['Subject Perceived Race'] != 'Native Hawaiian or Other Pacific Islander')]


#import APD data
@st.cache_data
def load_data(fv):
    df = pd.read_csv(fv)
    return df
fv = load_data("Fayettville_Arrests.csv")
fv = fv[fv['Year']<2023]
fv = fv[fv['Year']>2019]

st.title("Police Arrest Data")


tab1, tab2 = st.tabs(["Seattle, WA", "Fayetteville, NC"])

#Seattle, WA Arrest Data
with tab1:
    s_chart = alt.Chart(seattle).mark_bar().encode(
    x= alt.X('Subject Perceived Race:O',title='Race',axis=alt.Axis(labels=False)).sort('-y'),
    y='count():Q',
    color='Subject Perceived Race:N',
    column='Year'
    ).properties(
        title='Arrests by Traffic Stops in Seattle, WA'
    ).configure_title(fontSize=24)
    st.altair_chart(s_chart)

#Fayetteville, NC Arrest Data
with tab2:
    fv_chart = alt.Chart(fv).mark_bar().encode(
    x= alt.X('ar_race:O',title='Race',axis=alt.Axis(labels=False)).sort('-y'),
    y='count():Q',
    color= alt.Color('ar_race:N').sort('-y'),
    column= 'Year'
    ).properties(
        title='Arrests by Traffic Stops in Fayetteville, NC'
    ).configure_title(fontSize=24)
    st.altair_chart(fv_chart)