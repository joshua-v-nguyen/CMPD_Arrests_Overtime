import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()
alt.themes.enable('dark')

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
    df = df[df['Descent Code']!='NA/I']
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
    df = df[df['ar_race']!='NA/I']
    return df
fpd = change_fpd(fpd)

@st.cache_data
def load_demo(data):
    df = pd.read_csv(data)
    return df

#TITLE
st.markdown('''
    ## **DISPROPORTIONATE ARRESTS ON BLACK AND BROWN INDIVIDUALS**
            ''')

with st.sidebar:
        st.title("ABBREVIATIONS:")
        st.subheader("Police Departments")
        st.write(":red[FPD] = Fayetteville Police Department")
        st.write(":red[LAPD] = Los Angeles Police Department")
        st.subheader("Racial Identities:")
        st.write(":red[AA/PI] = Asian American/Pacific Islander")
        st.write(":red[H/L/M] = Hispanic/Latinx/Mexican")

@st.cache_data
def year_select(df,year_slider):
    df = df[df['Year']==year_slider]
    return df

tab1, tab2, tab3, tab4 = st.tabs(["Background Information", "Proportional Arrests by Race","Call to Action","Sources"])

#==============POPULATION TAB==============#
with tab1:
    st.markdown('''
        ###### :gray[This app was made to highlight the disproportionate arrests made on Black and Brown individuals by the police.] 
                
        ###### :gray[Here, I compare two cities; :red[Fayetteville, NC] and :red[Los Angeles, CA] across a 3 year period :red[(2020-2022)]. To the left includes some filters to switch between cities and year, as well as an abbreviations glossary.]
        ''')
    
    st.image('./background.png')
    st.markdown('''
        :gray[*sourced from Prisoners in 2020 – Statistical Tables, NCJ 302776, December 2021. https://bjs.ojp.gov/library/publications/prisoners-2020-statistical-tables.*]

        ''')

    st.markdown('''
        \n
        ###### :gray[The inspiration for this project came to me after reading [this article](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7162705/) by Am Psychol that discusses the impacts and repercussions of discrimination on Black youth.]
        ''')
    

#==============ARREST TAB==============#
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        #SELECTING THE CITY
        city = st.radio(
                    "Choose a police department to view arrest data",
                    ["FPD","LAPD"],
                    captions=["Fayettville, NC", "Los Angeles, CA"],horizontal=True)
    with col2:
        #SELECTING THE YEAR
        slider = st.radio('Select a year', [2020, 2021, 2022],horizontal=True)  

    st.write(f"**Arrests in :red[{city}] in :red[{slider}]**")

    #LOADING DEMOGRAPHIC DATA
    demo = load_demo("Demographics.csv")

    #==========STATISTICS==========#

    #POPULATION NUMBERS
    totpop = 0
    
    if city=='FPD':
        fpd = year_select(fpd,slider)
        cityname = 'Fayetteville\'s'
        totpop = 208501
        arrested_pop = len(fpd)
        black_fpd = round(((fpd['ar_race'].value_counts()['Black']) / arrested_pop),2)
        white_fpd = round(((fpd['ar_race'].value_counts()['White']) / arrested_pop),2)
        asn_fpd = round(((fpd['ar_race'].value_counts()['AA/PI']) / arrested_pop),2)
        
        source_data = [
                   [black_fpd,'Black Individuals Arrested'],
                   [white_fpd,'White Individuals Arrested'],
                   [asn_fpd,'AA/PI Individuals Arrested']]
        
        source = pd.DataFrame(source_data, columns=['y','x'])
        source['y'] = source['y'].astype(float)
        chart = alt.Chart(source).mark_bar().encode(
            x=alt.X('y',title="%",scale=alt.Scale(domain=[0, 1.0]),),
            y=alt.Y('x',title="").sort('-x'),
            color = alt.Color('x',legend=None,
                                scale=alt.Scale(
                                domain=source.sort_values(['y'])['x'].tolist(),
                                range=['#B7B7B7','#B7B7B7','#FF6361'])),
            text=alt.Text('y', format='.2%')
        ).properties(
            title='Proportional Arrests by Race',
            width=600,
            height=400
        )

    elif city=='LAPD':
        lapd = year_select(lapd,slider)
        cityname = 'Los Angeles\''
        totpop = 3898747
        arrested_pop = len(lapd)
        black_lapd = round(((lapd['Descent Code'].value_counts()['Black']) / arrested_pop),2)
        white_lapd = round(((lapd['Descent Code'].value_counts()['White']) / arrested_pop),2)
        hsp_lapd = round(((lapd['Descent Code'].value_counts()['H/L/M']) / arrested_pop),2)
        asn_lapd = round(((lapd['Descent Code'].value_counts()['AA/PI']) / arrested_pop),2)

        source_data = [
                    [hsp_lapd,'H/L/M Individuals Arrested'],
                   [black_lapd,'Black Individuals Arrested'],
                   [white_lapd,'White Individuals Arrested'],
                   [asn_lapd,'AA/PI Individuals Arrested']]
        
        source = pd.DataFrame(source_data, columns=['y','x'])
        source['y'] = source['y'].astype(float)

        chart = alt.Chart(source).mark_bar().encode(
                x=alt.X('y',title="%",scale=alt.Scale(domain=[0, 1.0]),),
                y=alt.Y('x',title="").sort('-x'),
                color = alt.Color('x',legend=None,
                                    scale=alt.Scale(
                                    domain=source.sort_values(['y'])['x'].tolist(),
                                    range=['#B7B7B7','#B7B7B7','#FF6361','#FF6361'])),
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

    st.markdown('''

        ###### :gray[Across both cities, we see that :red[*arrests of Black and Brown individuals are very disproportionate to White individuals*].]

                ''')
with tab3:
    st.markdown('''

        ###### :gray[According to Psychol, there are several factors that affect the higher proportions of arrests we see in this data. Some early-life factors include :red[socioeconomic status], :red[neighborhood risk], and :red[inequalities in the criminal justice system] (which historically is associated with increased rates of harassment and arrests among Black and Brown individuals).] 

                ''')
    
    st.image('./incarceration.png')
    st.markdown('''
        :gray[*Image courtesy of "Where Incarceration Isn’t the Answer" from [YesMagazine](https://www.yesmagazine.org/issue/what-the-rest-of-the-world-knows/2020/11/03/where-incarceration-isnt-the-answer).*]

                ''')

    st.markdown('''
        ###### :gray[What I want people to take away from this is that although this is a relatively low-scale comparison, :red[the fact that two cities], which have completely different populations and are on different sides of the United States, :red[can have the same amount of disproportionate arrests on Black and/or Brown individuals should be alarming]. Black and Brown individuals are not getting arrested more because they are “predispositioned to”. There are systemic issues that need to be addressed **early** to prevent this cycle from continuing.]
                ''')
    
    st.markdown('''
        ###### :gray[Below are some interesting articles that talk about the history of the United States' incarceration system and the overwhelming amount of BIPOC and LGBTQ+ folks who are incarcerated at higher proportion than their White, heterosexual counterparts.]
        
                
        ###### - [Beyond the count: A deep dive into state prison populations](https://www.prisonpolicy.org/reports/beyondthecount.html#demographics) :gray[*by Leah Wang, Wendy Sawyer, Tiana Herring, and Emily Widra*]
        ###### - [Where Incarceration Isn’t the Answer](https://www.yesmagazine.org/issue/what-the-rest-of-the-world-knows/2020/11/03/where-incarceration-isnt-the-answer) :gray[*by Mark P. Fancher*]
                ''')
    
with tab4:
    st.markdown('''
        **ARREST DATA**\n
        - [Fayettville Police Department](https://data.fayettevillenc.gov/datasets/faync::arrests/about)\n
        - [Los Angeles Police Department](https://data.lacity.org/Public-Safety/Arrest-Data-from-2020-to-Present/amvf-fr72/about_data)\n

        **OTHER STATISTICS**\n
        - [Prisoner Statistics (2020)](https://bjs.ojp.gov/library/publications/prisoners-2020-statistical-tables)\n

        **OTHER SOURCES**\n
        - [The Impact of Early Racial Discrimination on Illegal Behavior, Arrest and Incarceration among African Americans](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7162705/) :gray[*by Am Psychol*]\n
        - [Beyond the count: A deep dive into state prison populations](https://www.prisonpolicy.org/reports/beyondthecount.html#demographics) :gray[*by Leah Wang, Wendy Sawyer, Tiana Herring, and Emily Widra*]\n
        - [Where Incarceration Isn’t the Answer](https://www.yesmagazine.org/issue/what-the-rest-of-the-world-knows/2020/11/03/where-incarceration-isnt-the-answer) :gray[*by Mark P. Fancher*]\n

                ''')