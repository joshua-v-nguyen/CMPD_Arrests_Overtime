import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

#import SPD data
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


#import FPD data
@st.cache_data
def load_data(fv):
    df = pd.read_csv(fv)
    return df
fv = load_data("Fayettville_Arrests.csv")
fv = fv[fv['Year']<2023]
fv = fv[fv['Year']>2019]

st.title("Police Arrest Data")

#importing NOPD data
@st.cache_data
def load_data(nola):
    df = pd.read_csv(nola)
    return df
nola = load_data("NOPD_Arrests.csv")
nola = nola[nola['Year']<2023]
nola = nola[nola['Year']>2019]

tab1, tab2, tab3 = st.tabs(["Seattle, WA", "Fayetteville, NC","New Orleans, LA"])

#Seattle, WA Arrest Data
with tab1:
    s_chart = alt.Chart(seattle).mark_bar().encode(
    x= alt.X('Subject Perceived Race:O',title='').sort('-y'),
    y='count():Q',
    color= alt.Color('Subject Perceived Race:N').sort('-y'),
    column= alt.Column('Year',title='')
    ).properties(
        title='Arrests by Traffic Stops in Seattle, WA',
        width=125,
        height=400
    ).configure_title(fontSize=24)
    st.altair_chart(s_chart)

#Fayetteville, NC Arrest Data
with tab2:
    fv_chart = alt.Chart(fv).mark_bar().encode(
    x= alt.X('ar_race:O',title='Race').sort('-y'),
    y='count():Q',
    color= alt.Color('ar_race:N',title='').sort('-y'),
    column= alt.Column('Year',title='')
    ).properties(
        title='Arrests by Traffic Stops in Fayetteville, NC',
        width=125,
        height=400
    ).configure_title(fontSize=24)
    st.altair_chart(fv_chart)

with tab3:
    nola_chart = alt.Chart(nola).mark_bar().encode(
    x= alt.X('Offender_Race:O',title='Race').sort('-y'),
    y='count():Q',
    color= alt.Color('Offender_Race:N',title='').sort('-y'),
    column= alt.Column('Year',title='')
    ).properties(
        title='Arrests by Traffic Stops in New Orleans, LA',
        width=125,
        height=400
    ).configure_title(fontSize=24)
    st.altair_chart(nola_chart)