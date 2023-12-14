import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

#==============IMPORTING DATA==============#

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
        {'A':'AA/PI',
        'B':'Black',
        'C':'AA/PI',
        'D':'AA/PI',
        'F':'AA/PI',
        'G':'AA/PI',
        'H':'H/L/M',
        'I':'NA/I',
        'J':'AA/PI',
        'K':'AA/PI',
        'L':'AA/PI',
        'O':'Other',
        'P':'AA/PI',
        'S':'AA/PI',
        'U':'AA/PI',
        'V':'AA/PI',
        'W':'White',
        'X':'Unknown',
        'Z':'AA/PI'
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
        {'A':'AA/PI',
        'B':'Black',
        'I':'NA/I',
        'U':'Unknown',
        'W':'White',
        'H':'H/L/M',
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
        'HISPANIC':'H/L/M',
        'ASIAN':'AA/PI',
        'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER':'AA/PI',
        'AMER. IND.':'NA/I',
        'WHITE':'White'
        }) 
    return df
nola = change_nola(nola)

@st.cache_data
def load_demo(data):
    df = pd.read_csv(data)
    return df

#TITLE
st.markdown('''
    ### **DISPROPORTIONATE ARRESTS ON BLACK AND BROWN INDIVIDUALS**: :gray[*Comparing population to proportion*]
            ''')

with st.sidebar:
        st.title("FILTERS:")
        #SELECTING THE CITY
        city = st.radio(
                    "Choose a police department to view arrest data",
                    ["FPD","LAPD", "NOPD"],
                    captions=["Fayettville, NC", "Los Angeles, CA", "New Orleans, LA"],horizontal=True)
        #SELECTING THE YEAR
        slider = st.radio('Select a year', [2020, 2021, 2022],horizontal=True)
        st.write("------------------------------------")
        st.title("ABBREVIATIONS:")
        st.subheader("Police Departments")
        st.write("FPD = Fayetteville Police Department")
        st.write("LAPD = Los Angeles Police Department")
        st.write("NOPD = New Orleans Police Department")
        st.write("------------------------------------")
        st.subheader("Racial Identities")
        st.write("AA/PI = Asian American/Pacific Islander")
        st.write("H/L/M = Hispanic/Latinx/Mexican")
        st.write("NA/I = Native American/Indigenous")

@st.cache_data
def year_select(df,year_slider):
    df = df[df['Year']==year_slider]
    return df

tab1, tab2, tab3 = st.tabs(["Background Information", "Population Graphs", "Proportional Arrests by Race"])

#==============POPULATION TAB==============#
with tab1:
    st.write("Hello, I need information here lawl")

#==============POPULATION TAB==============#
with tab2:
    if city == "FPD":
        #Fayetteville, NC Arrest Data
        fpd = year_select(fpd,slider)
        cityname = "Fayetteville, NC"
        pop = load_demo('Demographics.csv')
        pop = pop[pop['City']=="FPD"]
        @st.cache_data
        def load_fpd_chart(df):
            chart = alt.Chart(df).mark_bar(stroke='transparent').encode(
                x=alt.X('Count:Q',title='',scale=alt.Scale(domain=[0, 100000])),
                y= alt.Y('Race:N',title='').sort('-x'),
                color = alt.Color('Race:N',legend=None,
                                scale=alt.Scale(
                                domain=df.sort_values(['Count'])['Race'].tolist(),
                                range=['#003F5C','#58508D','#BC5090','#FF6361','#FFA600'])),
                text=alt.Text('Count:Q',format=',.0f')
            ).properties(
                title=f"Population of {cityname} in {slider}",
                width=600,
                height=400
            )
            return chart
        
        chart = load_fpd_chart(pop)
        text = chart.mark_text(align='left', dx=2,fontSize=15)

        layer_chart= alt.layer(text,chart).configure_view(
            stroke='transparent'
        ).configure_axisY(
            labelLimit=200,
            labelFontSize=12,
            labelColor='black'
        )
        st.altair_chart(layer_chart)

    elif city =="LAPD":
        #Los Angeles, CA Arrest Data
        lapd = year_select(lapd,slider)
        cityname = "Los Angeles, CA"
        pop = load_demo('Demographics.csv')
        pop = pop[pop['City']=="LAPD"]
        @st.cache_data
        def load_lapd_chart(df):
            chart = alt.Chart(df).mark_bar(stroke='transparent').encode(
                x=alt.X('Count:Q',title='',scale=alt.Scale(domain=[0, 2500000])),
                y= alt.Y('Race:N',title='').sort('-x'),
                color = alt.Color('Race:N',legend=None,
                                scale=alt.Scale(
                                domain=df.sort_values(['Count'])['Race'].tolist(),
                                range=['#003F5C','#58508D','#BC5090','#FF6361','#FFA600'])),
                text=alt.Text('Count:Q',format=',.0f')
            ).properties(
                title=f"Population of {cityname} in {slider}",
                width=600,
                height=400
            )
            return chart
        
        chart = load_lapd_chart(pop)
        text = chart.mark_text(align='left', dx=2,fontSize=15)

        layer_chart= alt.layer(text,chart).configure_view(
            stroke='transparent'
        ).configure_axisY(
            labelLimit=200,
            labelFontSize=12,
            labelColor='black'
        )
        st.altair_chart(layer_chart)

    elif city =="NOPD":
        #New Orleans, LA Arrest Data
        nola = year_select(nola,slider)
        cityname = "New Orleans, LA"
        pop = load_demo('Demographics.csv')
        pop = pop[pop['City']=="NOPD"]
        @st.cache_data
        def load_nopd_chart(df):
            chart = alt.Chart(df).mark_bar(stroke='transparent').encode(
                x=alt.X('Count:Q',title='',scale=alt.Scale(domain=[0, 250000])),
                y= alt.Y('Race:N',title='').sort('-x'),
                color = alt.Color('Race:N',legend=None,
                                scale=alt.Scale(
                                domain=df.sort_values(['Count'])['Race'].tolist(),
                                range=['#003F5C','#58508D','#BC5090','#FF6361','#FFA600'])),
                text=alt.Text('Count:Q',format=',.0f')
            ).properties(
                title=f"Population of {cityname} in {slider}",
                width=600,
                height=400
            )
            return chart
        
        chart = load_nopd_chart(pop)
        text = chart.mark_text(align='left', dx=2,fontSize=15)

        layer_chart= alt.layer(text,chart).configure_view(
            stroke='transparent'
        ).configure_axisY(
            labelLimit=200,
            labelFontSize=12,
            labelColor='black'
        )
        st.altair_chart(layer_chart)

#==============ARREST TAB==============#
with tab3:    
    st.write(f"**Arrests in :red[{city}]**")

    #LOADING DEMOGRAPHIC DATA
    demo = load_demo("Demographics.csv")

    #==========STATISTICS==========#

    #POPULATION NUMBERS
    totpop = 0

    if city=='FPD':
        cityname = 'Fayetteville\'s'
        totpop = 208501
        arrested_pop = len(fpd)
        black_fpd = round(((fpd['ar_race'].value_counts()['Black']) / arrested_pop),2)
        white_fpd = round(((fpd['ar_race'].value_counts()['White']) / arrested_pop),2)
        asn_fpd = round(((fpd['ar_race'].value_counts()['AA/PI']) / arrested_pop),2)
        native_fpd = round(((fpd['ar_race'].value_counts()['NA/I']) / arrested_pop),2)

        source_data = [
                   [black_fpd,'Black Individuals Arrested'],
                   [white_fpd,'White Individuals Arrested'],
                   [asn_fpd,'AA/PI Individuals Arrested'],
                   [native_fpd,'NA/I Individuals Arrested']]
        
        source = pd.DataFrame(source_data, columns=['y','x'])
        source['y'] = source['y'].astype(float)

    elif city=='LAPD':
        cityname = 'Los Angeles\''
        totpop = 3898747
        arrested_pop = len(lapd)
        black_lapd = round(((lapd['Descent Code'].value_counts()['Black']) / arrested_pop),2)
        white_lapd = round(((lapd['Descent Code'].value_counts()['White']) / arrested_pop),2)
        hsp_lapd = round(((lapd['Descent Code'].value_counts()['H/L/M']) / arrested_pop),2)
        asn_lapd = round(((lapd['Descent Code'].value_counts()['AA/PI']) / arrested_pop),2)
        native_lapd = round(((lapd['Descent Code'].value_counts()['NA/I']) / arrested_pop),2)

        source_data = [
                    [hsp_lapd,'H/L/M Individuals Arrested'],
                   [black_lapd,'Black Individuals Arrested'],
                   [white_lapd,'White Individuals Arrested'],
                   [asn_lapd,'AA/PI Individuals Arrested'],
                   [native_lapd,'NA/I Individuals Arrested']]
        
        source = pd.DataFrame(source_data, columns=['y','x'])
        source['y'] = source['y'].astype(float)

    elif city=='NOPD':
        cityname = 'New Orlean\'s'
        totpop = 383997
        arrested_pop = len(nola)
        black_nopd = round(((nola['Offender_Race'].value_counts()['Black']) / arrested_pop),2)
        white_nopd = round(((nola['Offender_Race'].value_counts()['White']) / arrested_pop),2)
        if slider == 2022:
            hsp_nopd = 0
        else:
            hsp_nopd = round(((nola['Offender_Race'].value_counts()['H/L/M']) / arrested_pop),2)
        asn_nopd = round(((nola['Offender_Race'].value_counts()['AA/PI']) / arrested_pop),2)
        native_nopd = round(((nola['Offender_Race'].value_counts()['NA/I']) / arrested_pop),2)
        
        
        source_data = [
                    [hsp_nopd,'H/L/M Individuals Arrested'],
                   [black_nopd,'Black Individuals Arrested'],
                   [white_nopd,'White Individuals Arrested'],
                   [asn_nopd,'AA/PI Individuals Arrested'],
                   [native_nopd,'NA/I Individuals Arrested']]
        
        source = pd.DataFrame(source_data, columns=['y','x'])
        source['y'] = source['y'].astype(float)


    chart = alt.Chart(source).mark_bar().encode(
            x=alt.X('y',title="%",scale=alt.Scale(domain=[0, 1.0]),),
            y=alt.Y('x',title="").sort('-x'),
            color = alt.Color('x',legend=None,
                                scale=alt.Scale(
                                domain=source.sort_values(['y'])['x'].tolist(),
                                range=['#003F5C','#58508D','#BC5090','#FF6361','#FFA600'])),
            text=alt.Text('y', format='.2%')
        ).properties(
            title='Proportional Arrests by Race',
            width=600,
            height=400
        )
    
    text = chart.mark_text(align='left', dx=2)

    layer_chart= alt.layer(text,chart).configure_view(
        stroke='transparent'
    ).configure_axisY(
        labelLimit=150,
        labelFontSize=12,
        labelColor='black'
    )

    st.altair_chart(layer_chart)