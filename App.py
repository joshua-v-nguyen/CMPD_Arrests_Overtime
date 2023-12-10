import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

#import LAPD data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df
lapd = load_data("LAPD_Arrests.csv")
#Editing LAPD data
@st.cache_data
def change_lapd(data):
    df = data
    df = df[df['Year']<2023]
    df = df[df['Year']>2019]
    df = df.replace(
        {'A':'Asian American/Pacific Islander',
        'B':'Black',
        'C':'Asian American/Pacific Islander',
        'D':'Asian American/Pacific Islander',
        'F':'Asian American/Pacific Islander',
        'G':'Asian American/Pacific Islander',
        'H':'Hispanic/Latin/Mexican',
        'I':'Native American/Indigenous',
        'J':'Asian American/Pacific Islander',
        'K':'Asian American/Pacific Islander',
        'L':'Asian American/Pacific Islander',
        'O':'Other',
        'P':'Asian American/Pacific Islander',
        'S':'Asian American/Pacific Islander',
        'U':'Asian American/Pacific Islander',
        'V':'Asian American/Pacific Islander',
        'W':'White',
        'X':'Unknown',
        'Z':'Asian American/Pacific Islander'
        })
    return df
lapd = change_lapd(lapd)


#import FPD data
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df
fpd = load_data("Fayettville_Arrests.csv")
#Editing FPD data
@st.cache_data
def change_fpd(data):
    df = data
    df = df[df['Year']<2023]
    df = df[df['Year']>2019]
    df = df.replace(
        {'A':'Asian American/Pacific Islander',
        'B':'Black',
        'I':'Native American/Indigenous',
        'U':'Unknown',
        'W':'White'
        })
    return df
fpd = change_fpd(fpd)

#importing NOPD data
nola = load_data("NOPD_Arrests.csv")
#Editing FPD data
@st.cache_data
def change_nola(data):
    df = data
    df = df.replace(
        {'BLACK':'Black',
        'WHITE':'White',
        'HISPANIC':'Hispanic/Latin/Mexican',
        'ASIAN':'Asian American/Pacific Islander',
        'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER':'AAPI',
        'AMER. IND.':'Native American/Indigenous',
        'WHITE':'White'
        }) 
    return df
nola = change_nola(nola)

st.title("Police Arrest Data")


tab1, tab2, tab3 = st.tabs(["Los Angeles, CA", "Fayetteville, NC","New Orleans, LA"])

#Los Angeles, CA Arrest Data
with tab1:
    @st.cache_data
    def load_lapd_chart(df):
        chart = alt.Chart(df).mark_bar().encode(
                x= alt.X('Descent Code:O',title='').sort('-y'),
                y='count():Q',
                color= alt.Color('Descent Code:N').sort('-y'),
                column= alt.Column('Year',title='')
                ).properties(
                    title='Arrests in Los Angeles, CA (2020-2022)',
                    width=125,
                    height=400
                ).configure_title(fontSize=24)
        return chart
    st.altair_chart(load_lapd_chart(lapd))

#Fayetteville, NC Arrest Data
with tab2:
    @st.cache_data
    def load_fpd_chart(df):
        chart = alt.Chart(df).mark_bar().encode(
                x= alt.X('ar_race:O',title='Race').sort('-y'),
                y='count():Q',
                color= alt.Color('ar_race:N',title='').sort('-y'),
                column= alt.Column('Year',title='')
                ).properties(
                    title='Arrests in Fayetteville, NC (2020-2022)',
                    width=125,
                    height=400
                ).configure_title(fontSize=24)
        return chart
    st.altair_chart(load_fpd_chart(fpd))

with tab3:
    @st.cache_data
    def load_nola_chart(df):
        chart = alt.Chart(df).mark_bar().encode(
                x= alt.X('Offender_Race:O',title='Race').sort('-y'),
                y='count():Q',
                color= alt.Color('Offender_Race:N',title='').sort('-y'),
                column= alt.Column('Year',title='')
                ).properties(
                    title='Arrests in New Orleans, LA (2020-2022)',
                    width=125,
                    height=400
                ).configure_title(fontSize=24)
        return chart
    st.altair_chart(load_nola_chart(nola))