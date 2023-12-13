import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

#==============IMPPRTING DATA==============#

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
    df = df[df['Descent Code']!='Unknown']
    df = df[df['Descent Code']!='Other']
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
    df['ar_race'] = df['ar_race'].apply(lambda x: x.strip())
    df = df.replace(
        {'A':'Asian American/Pacific Islander',
        'B':'Black',
        'I':'Native American/Indigenous',
        'U':'Unknown',
        'W':'White',
        'H':'Hispanic/Latin/Mexican',
        'O':'Unknown',
        'F':'Unknown',
        'P':'Unknown'
        })
    df = df[df['ar_race']!='Unknown']
    return df
fpd = change_fpd(fpd)

#importing NOPD data
nola = load_data("NOPD_Arrests.csv")
#Editing NOPD data
@st.cache_data
def change_nola(data):
    df = data
    df = df[df['OffenderStatus']!= ""]
    df = df[df['Year']>2019]
    df = df[df['Year']<2023]
    df = df.replace(
        {'BLACK':'Black',
        'WHITE':'White',
        'HISPANIC':'Hispanic/Latin/Mexican',
        'ASIAN':'Asian American/Pacific Islander',
        'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER':'Asian American/Pacific Islander',
        'AMER. IND.':'Native American/Indigenous',
        'WHITE':'White'
        }) 
    return df
nola = change_nola(nola)

@st.cache_data
def load_demo(data):
    df = pd.read_csv(data)
    return df

#TITLE
st.title("Police Arrest Data")

#SELECTING THE CITY
city = st.radio(
            "Choose a police department to view arrest data",
            ["FPD","LAPD", "NOPD"],
            captions=["Fayettville, NC", "Los Angeles, CA", "New Orleans, LA"],
            horizontal=True
            )
slider = st.slider('Select a year', 2020, 2022, 2020)

@st.cache_data
def year_select(df,year_slider):
    df = df[df['Year']==year_slider]
    return df

tab1, tab2 = st.tabs(["Arrest Graphs", "Comparative Statistics"])

#==============GRAPH TAB==============#
with tab1:
    if city == "FPD":
        #Fayetteville, NC Arrest Data
        fpd = year_select(fpd,slider)
        @st.cache_data
        def load_fpd_chart(df):
            chart = alt.Chart(df).mark_bar().encode(
                    x= alt.X('count():Q',title=''),
                    y=alt.Y('ar_race:O',title='').sort('-x'),
                    color= alt.Color('ar_race:N',legend=None).sort('-x'),
                    text='count():Q'
                    ).properties(
                        title='Arrests in Fayetteville, NC (2020-2022)',
                        width=500,
                        height=400
                    )
            return chart
        st.altair_chart(load_fpd_chart(fpd).mark_bar() + load_fpd_chart(fpd).mark_text(align='left', dx=2))
    elif city =="LAPD":
        #Los Angeles, CA Arrest Data
        lapd = year_select(lapd,slider)
        @st.cache_data
        def load_lapd_chart(df):
            chart = alt.Chart(df).mark_bar().encode(
                    x= alt.X('count():Q',title=''),
                    y=alt.Y('Descent Code:O',title='').sort('-x'),
                    color= alt.Color('Descent Code:N',legend=None).sort('-x'),
                    text='count():Q'
                    ).properties(
                        title='Arrests in Los Angeles, CA (2020-2022)',
                        width=600,
                        height=400
                    )
            return chart
        st.altair_chart(load_lapd_chart(lapd).mark_bar() + load_lapd_chart(lapd).mark_text(align='left', dx=2))
    elif city =="NOPD":
        #New Orleans, LA Arrest Data
        nola = year_select(nola,slider)
        @st.cache_data
        def load_nola_chart(df):
            chart = alt.Chart(df).mark_bar().encode(
                    x= alt.X('count():Q',title=''),
                    y=alt.Y('Offender_Race:O',title='').sort('-x'),
                    color= alt.Color('Offender_Race:N',legend=None).sort('-x'),
                    text='count():Q'
                    ).properties(
                        title='Arrests in New Orleans, LA (2020-2022)',
                        width=600,
                        height=400
                    )
            return chart
        st.altair_chart(load_nola_chart(nola).mark_bar() + load_nola_chart(nola).mark_text(align='left', dx=2))

#==============STATISTICS TAB==============#
with tab2:    
    st.write(f"**Comparisons with :red[{city}] Demographics**")
    if city == "FPD":
        display = fpd['ar_race'].unique()
    elif city =="LAPD":
        display = lapd['Descent Code'].unique()
    elif city == "NOPD":
        display = nola['Offender_Race'].unique()
    
    options = list(range(len(display)))
    value = st.selectbox("Please select a racial identity to compare:", options, format_func=lambda x: display[x])

    #LOADING DEMOGRAPHIC DATA
    demo = load_demo("Demographics.csv")

    #FPD
    if value == 0 and city == "FPD":
        race="White"
    elif value == 1 and city == "FPD":
        race="Black"
    elif value == 2 and city == "FPD":
        race="Native American/Indigenous"
    elif value == 3 and city == "FPD":
        race="Asian American/Pacific Islander"
    #LAPD
    elif value == 0 and city == "LAPD":
        race="Hispanic/Latin/Mexican"
    elif value == 1 and city == "LAPD":
        race="Black"
    elif value == 2 and city == "LAPD":
        race="White"
    elif value == 3 and city == "LAPD":
        race="Asian American/Pacific Islander"
    elif value == 4 and city == "LAPD":
        race="Native American/Indigenous"
    #NOPD
    elif value == 0 and city == "NOPD":
        race="Black"
    elif value == 1 and city == "NOPD":
        race="White"
    elif value == 2 and city == "NOPD":
        race="Hispanic/Latin/Mexican"
    elif value == 3 and city == "NOPD":
        race="Asian American/Pacific Islander"
    elif value == 4 and city == "NOPD":
        race="Native American/Indigenous"

    #==========STATISTICS==========#
    filtered_df = demo[demo["City"].isin([f"{city}"]) & demo["Race"].isin([race])]
    population = filtered_df['Count'].sum()

    #POPULATION NUMBERS
    totpop = 0
    if city=='FPD':
        cityname = 'Fayetteville\'s'
        totpop = 208501
        fpd = fpd[fpd['ar_race']==race]
        race_arrest = fpd['ar_race'].count()
    elif city=='LAPD':
        cityname = 'Los Angeles\''
        totpop = 3898747
        lapd = lapd[lapd['Descent Code']==race]
        race_arrest = lapd['Descent Code'].count()
    elif city=='NOPD':
        cityname = 'New Orlean\'s'
        totpop = 383997
        nola = nola[nola['Offender_Race']==race]
        race_arrest = nola['Offender_Race'].count()

    source_data = [[totpop,'Total Population'],[population,f'{race} Population'],[race_arrest,'# Arrested']]
    source = pd.DataFrame(source_data, columns=['y','x'])
    source['y'] = source['y'].astype(float)


    chart = alt.Chart(source).mark_bar().encode(
            x=alt.X('y',title=""),
            y=alt.Y('x',title="").sort('-x'),
            color = alt.Color('x',legend=None,
                                scale=alt.Scale(
                                domain=source.sort_values(['y'])['x'].tolist(),
                                range=['#1d4289','orange','grey'])),
            text='y'
        ).properties(
            title='Population Comparisons',
            width=500,
            height=400
        )
    st.altair_chart(chart.mark_bar() + chart.mark_text(align='left', dx=2))