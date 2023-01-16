import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded", )
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pycountry
import plotly.express as px


import streamlit.components.v1 as components



# Load the available data and overview

covid=pd.read_csv(r"https://covid19.who.int/WHO-COVID-19-global-data.csv")
def get_iso3(iso2):
    """Function takes in iso_alpha2 country codes and returns the iso_alpha 3 codes"""
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except:
       #In case we have errors that row of data will be left out.
        # Try except is a good way to handle possible errors that might occur while running a function"""
        pass

covid['iso_alpha'] = covid.Country_code.apply(lambda x: get_iso3(x))

menu = ['Cases and Deaths Overview','Cases Snapshot','To be used later']
selection = st.sidebar.selectbox("Covid 19 Statistsics ", menu)

st.sidebar.write('WHO Coronavirus (COVID-19) Dashboard.')

if selection== 'Cases Snapshot':
    # Use the full page instead of a narrow central column
    #st.beta_set_page_config(layout="wide")
    st.markdown('Cumulative Cases Overview')
    #st.table(covid.head())
    our_map=px.choropleth(covid,
               locations="iso_alpha",
               color="Cumulative_cases", # lifeExp is a column of gapminde
               hover_name="Country", # column to add to hover information
               #color_continuous_scale=px.colors.sequential.Viridis,#color scales can be changed to your heart's content.If you need examples there is a code exmaple listed down below
               animation_frame="Date_reported")# animation based on the years

    st.plotly_chart(our_map)
    


if selection== 'Cases and Deaths Overview':
    col1, col2 = st.columns(2)
    
    with col1:
      st.markdown('Daily Deaths Overview')
     #st.write(covid.head())
      #barplot=sns.barplot(x="Date_reported", y="Cumulative_deaths", data=covid)
      covid["Year"]=pd.DatetimeIndex(covid["Date_reported"]).year
      covid_deaths_daily=covid.groupby(['Date_reported'])['New_deaths'].sum().reset_index()
      fig = px.bar(covid_deaths_daily, x='Date_reported', y='New_deaths',#  DataFrame or array-like or dict
             hover_data=['Date_reported'], 
             color='New_deaths',
             #animation_frame="Date_reported",
             labels={'pop':'population of Canada'},  #By default, column names are used in the figure for axis titles,
             height=400)
      st.plotly_chart(fig)
    with col2:
      st.markdown('Daily New Cases Overview')

     
    #st.table(covid.head())
      
      covid_cases_daily=covid.groupby(['Date_reported'])['New_cases'].sum().reset_index()
      fig_daily_cases = px.bar(covid_cases_daily, x='Date_reported', y='New_cases',#  DataFrame or array-like or dict
             hover_data=['Date_reported'], 
             color='New_cases',
             #animation_frame="Date_reported",
             labels={'pop':'population of Canada'},  #By default, column names are used in the figure for axis titles,
             height=400)
      st.plotly_chart(fig_daily_cases)
      
      

    col3, col4 = st.columns(2)
    with col3:
      st.markdown('Cumulative Deaths Overview')
      deaths=px.choropleth(covid,
               locations="iso_alpha",
               color="Cumulative_deaths", # lifeExp is a column of gapminde
               hover_name="Country", # column to add to hover information
               #color_continuous_scale=px.colors.sequential.Viridis,#color scales can be changed to your heart's content.If you need examples there is a code exmaple listed down below
               animation_frame="Date_reported")# animation based on the years

      st.plotly_chart(deaths)
 











# adding html  Template

footer_temp = """
	 

	"""

if selection== 'To be used later':
    st.subheader("About App")
    components.html(footer_temp, height=500)
