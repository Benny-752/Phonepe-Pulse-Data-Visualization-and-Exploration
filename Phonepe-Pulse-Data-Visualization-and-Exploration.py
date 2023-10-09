# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:56:28 2023

@author: DELL
"""

#pip install mysql-connector-python
#pip install streamlit plotly mysql-connector-python
#pip install streamlit
#pip install streamlit_extras

import mysql.connector 
import pandas as pd
#import psycopg2
import streamlit as st
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import requests
import geopandas as gpd
# connect to the database
import mysql.connector
import pymysql
config = {
    'host': 'localhost',
    'port': 3307,  # Default MySQL port is 3306
    'user': 'root',
    'password': '153@sherly',
    'database': 'phonepe',
}
#establishing the connection
conn = pymysql.connect(**config)
# create a cursor object
cursor = conn.cursor()


#with st.sidebar:
SELECT = option_menu(
    menu_title = None,
    options = ["About","Home","Basic insights",],
    icons =["bar-chart","house","toggles","at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})


#---------------------Basic Insights -----------------#


if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and Count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_Count based on Districts and states",
               "Top 10 RegisteredUsers based on states and District"]
    
               #1
               
    select = st.selectbox("Select the option",options)
    if select=="Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT States, Transaction_Year, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM top_tran GROUP BY States, Transaction_Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Transaction_Year', 'Transaction_Amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 states and amount of transaction")
            st.bar_chart(data=df,x="Transaction_Amount",y="States")
            
            #2
            
    elif select=="List 10 states based on type and amount of transaction":
        cursor.execute("SELECT DISTINCT States, SUM(Transaction_Count) as Total FROM top_tran GROUP BY States ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','Total_Transaction'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("List 10 states based on type and amount of transaction")
            st.bar_chart(data=df,x="Total_Transaction",y="States")
            
            #3
            
    elif select == "Top 5 Transaction_Type based on Transaction_Amount":
        cursor.execute("SELECT DISTINCT Transaction_Type, SUM(Transaction_Amount) AS Amount FROM agg_user GROUP BY Transaction_Type ORDER BY Amount DESC LIMIT 5")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_Type', 'Transaction_Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 5 Transaction_Type based on Transaction_Amount")
            st.bar_chart(data=df, y="Transaction_Type", x="Transaction_Amount")

            #4
            
    elif select=="Top 10 Registered-users based on States and District":
        cursor.execute("SELECT DISTINCT State, District, SUM(RegisteredUsers) AS Users FROM top_user GROUP BY State, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','RegisteredUsers'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Registered-users based on States and District")
            st.bar_chart(data=df,y="State",x="RegisteredUsers")
            
            #5
            
    elif select=="Top 10 Districts based on states and Count of transaction":
        cursor.execute("SELECT DISTINCT States,District,SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on states and Count of transaction")
            st.bar_chart(data=df,y="States",x="Transaction_Count")
            
            #6
            
    elif select=="List 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT States,Transaction_year,SUM(Transaction_Amount) AS Amount FROM agg_trans GROUP BY States, Transaction_year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','Transaction_year','Transaction_Amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df,y="States",x="Transaction_Amount")
            
            #7
            
    elif select=="List 10 Transaction_Count based on Districts and states":
        cursor.execute("SELECT DISTINCT States, District, SUM(Transaction_Count) AS Counts FROM map_tran GROUP BY States,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("List 10 Transaction_Count based on Districts and states")
            st.bar_chart(data=df,y="States",x="Transaction_Count")
            
            #8
             
    elif select=="Top 10 RegisteredUsers based on states and District":
        cursor.execute("SELECT DISTINCT States,District, SUM(RegisteredUsers) AS Users FROM map_user GROUP BY States,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['States','District','RegisteredUsers'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 RegisteredUsers based on states and District")
            st.bar_chart(data=df,y="States",x="RegisteredUsers")


#----------------Home----------------------#
conn = pymysql.connect(**config)
cursor = conn.cursor()

# execute a SELECT statement
cursor.execute("SELECT * FROM agg_trans")

# fetch all rows
rows = cursor.fetchall()
from streamlit_extras.add_vertical_space import add_vertical_space

if SELECT == "Home":
    col1,col2, = st.columns(2)
    col1.image(("data:image/png;base64,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"),width = 5)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image("data:image/png;base64,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")
        
    st.subheader(':blue[Registered Users Hotspots - States]')


    

    
      
      
    Data_Aggregated_Transaction_df= pd.read_csv(r'C:/Users/DELL/Downloads/agg_trans.csv')
    Data_Aggregated_User_Summary_df= pd.read_csv(r'C:/Users/DELL/Downloads/Data_Aggregated_User_Summary_Table.csv')
    Data_Aggregated_User_df= pd.read_csv(r'C:/Users/DELL/Downloads/agg_user.csv')
    Scatter_Geo_Dataset =  pd.read_csv(r'C:/Users/DELL/Downloads/Data_Map_Districts_Longitude_Latitude.csv')
    Coropleth_Dataset =  pd.read_csv(r'C:/Users/DELL/Downloads/Data_Map_IndiaStates_TU.csv')
    Data_Map_Transaction_df = pd.read_csv(r'C:/Users/DELL/Downloads/Data_Map_Transaction_Table.csv')
    Data_Map_User_Table= pd.read_csv(r'C:/Users/DELL/Downloads/Data_Map_User_Table.csv')
    Indian_States= pd.read_csv(r'C:/Users/DELL/Downloads/Longitude_Latitude_State_Table.csv')
    
    c1,c2=st.columns(2)
    with c1:
        Year = st.selectbox(
                'Please select the Year',
                ('2018', '2019', '2020','2021','2022'))
    with c2:
        Quarter = st.selectbox(
                'Please select the Quarter',
                ('1', '2', '3','4'))
    year=int(Year)
    quarter=int(Quarter)
    
    Transaction_scatter_districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['Year'] == year ) & (Data_Map_Transaction_df['Quarter']==quarter) ].copy()
    Transaction_Coropleth_States=Transaction_scatter_districts[Transaction_scatter_districts["State"] == "india"]
    Transaction_scatter_districts.drop(Transaction_scatter_districts.index[(Transaction_scatter_districts["State"] == "india")],axis=0,inplace=True)
    # Dynamic Scattergeo Data Generation
    
    Transaction_scatter_districts = Transaction_scatter_districts.sort_values(by=['Place_Name'], ascending=False)
    Scatter_Geo_Dataset = Scatter_Geo_Dataset.sort_values(by=['District'], ascending=False) 
    Total_Amount=[]
    for i in Transaction_scatter_districts['Total_Amount']:
        Total_Amount.append(i)
    Scatter_Geo_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_scatter_districts['Total_Transactions_count']:
        Total_Transaction.append(i)
    Scatter_Geo_Dataset['Total_Transactions']=Total_Transaction
    Scatter_Geo_Dataset['Year_Quarter']=str(year)+'-Q'+str(quarter)
    # Dynamic Coropleth
    
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['state'], ascending=False)
    Transaction_Coropleth_States = Transaction_Coropleth_States.sort_values(by=['Place_Name'], ascending=False)
    Total_Amount=[]
    for i in Transaction_Coropleth_States['Total_Amount']:
        Total_Amount.append(i)
    Coropleth_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_Coropleth_States['Total_Transactions_count']:
        Total_Transaction.append(i)
    Coropleth_Dataset['Total_Transactions']=Total_Transaction 
    
    
    
    
    #scatter plotting the states codes 
    Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
    Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
    Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
    Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
    Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)
    fig=px.scatter_geo(Indian_States,
                        lon=Indian_States['Longitude'],
                        lat=Indian_States['Latitude'],                                
                        text = Indian_States['code'], #It will display district names on map
                        hover_name="state", 
                        hover_data=['Total_Amount',"Total_Transactions","Year_Quarter"],
                        )
    fig.update_traces(marker=dict(color="white" ,size=0.3))
    fig.update_geos(fitbounds="locations", visible=False,)
    # scatter plotting districts
    Scatter_Geo_Dataset['col']=Scatter_Geo_Dataset['Total_Transactions']
    fig1=px.scatter_geo(Scatter_Geo_Dataset,
                        lon=Scatter_Geo_Dataset['Longitude'],
                        lat=Scatter_Geo_Dataset['Latitude'],
                        color=Scatter_Geo_Dataset['col'],
                        size=Scatter_Geo_Dataset['Total_Transactions'],     
                    #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                        hover_name="District", 
                        hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                        title='District',
                        size_max=22)
    
    fig1.update_traces(marker=dict(color="rebeccapurple" ,line_width=1))    #rebeccapurple
#coropleth mapping india
    fig_ch = px.choropleth(
                        Coropleth_Dataset,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',                
                        locations='state',
                        color="Total_Transactions",                                       
                        )
    fig_ch.update_geos(fitbounds="locations", visible=False,)
#combining districts states and coropleth
    fig_ch.add_trace( fig.data[0])
    fig_ch.add_trace(fig1.data[0])
    st.write("### **:blue[PhonePe India Map]**")
    colT1,colT2 = st.columns([6,4])
    with colT1:
        st.plotly_chart(fig_ch, use_container_width=True)
    with colT2:
        st.info(
        """
        Details of Map:
        - The darkness of the state color represents the total transactions
        - The Size of the Circles represents the total transactions dictrict wise
        - The bigger the Circle the higher the transactions
        - Hover data will show the details like Total transactions, Total amount
        """
        )
        st.info(
        """
        Important Observations:
        - User can observe Transactions of PhonePe in both statewide and Districtwide.
        - We can clearly see the states with highest transactions in the given year and quarter
        - We get basic idea about transactions district wide
        """
        )
# -----------------------------------------------FIGURE2 HIDDEN BARGRAPH------------------------------------------------------------------------
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['Total_Transactions'])
    fig = px.bar(Coropleth_Dataset, x='state', y='Total_Transactions',title=str(year)+" Quarter-"+str(quarter))
    with st.expander("See Bar graph for the same data"):
        st.plotly_chart(fig, use_container_width=True)
        st.info('**:blue[The above bar graph showing the increasing order of PhonePe Transactions according to the states of India, Here we can observe the top states with highest Transaction by looking at graph]**')

    
    
#----------------About-----------------------#

if SELECT == "About":
    col1,col2 = st.columns(2)
    with col1:
        st.image("data:image/png;base64,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")
    with col2:
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1,col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(("data:image/png;base64,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"),width = 400)
        with open("C:/Users/DELL/Downloads/annual report.pdf","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    with col2:
        st.image(("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANEAAADxCAMAAABiSKLrAAAAulBMVEX///9nOrfh4eHX19cAAABlN7ZkNbZcJ7NeKrRwSLtgLrTWzepfLLRcJrNiMrVlNrZZILLPxuaGZ8TMweWVe8tsQLqCYsJXHLHCs+Dv6veyn9jg2fCNcMfy7/nGuOKnktOMb8d1T716Vr/59/ysm9W8rd3v6/e2ptrn4fOdhc7PxOZ9WsChi9Dg2u9uRLqvr690dHSDg4OZf8zDw8MlJSWYmJi4uLg4ODgPDw+UlJRTDrCpqaltbW1bW1t9J8Y2AAANjElEQVR4nO2de3vauBLGrS2+YCzZ4SbuYAgBQqDddLdntz3n+3+tI+ObSLGtkeXg5PH7T1tqhH6WNB5dZqy1Yn37+uWPj6ovX78lHFr4x1/ftY+uH//wRH/fuzpK9GdK9PEbKNSPmOjLvWuiTD9Col/3rodC/RkQ/efetVCqfxjR5+lzgX60tL/uXQfFamn/3rsKivVN+yyWO9ZX7Y97V0GxPpdZCPTZWqgh+ghqiOqvhqj+aojqr4ao/mqI6q+GqP5qiOqvhqj+aojqr6qJ5tPR42v32EaB2sfu62QxnVf6ixUSbTqTLvGwZRPD1UO5BrEtTNFq0qnsZ6si2u+GHrYNdFO6YWPc3Y4r+eVKiJ4mbc/JoElkOHS9raADVkD0PKS2XoATynW8mfLup5xoi3BR6/AiuL1QWwHFRDvHEmueVLqJRiqroJRoQSwgTsQ0eFZXCYVEJx9D2ydh8obKDJ86ohfqSvIEMuijonqoIprqdgmeQNZ5r6QmioiWVLbDpXLpTkVVlBBtjlIW4TfhroLKqCA62UQJEEL24KkORL2cHkdMHMoU9CK86f2JtjS7guQw7UTyBQca7d2b6NHLqR5JrzvlXXeFtC1XobJEuUDI4nzrV1HzXtLklSTKB0LGML10bgoSIVrKzytHtC3qSibnCeyETXypsVSKqJdjFOLKcfOfgfBTuIzFK0O0FxjsOtkk1z+LGgekO/LPpRJEG0PknhNuKA2F54JG+x5EQzFPwUxNl0ijRrL770/0KGq7uEFxEHfQPVmDJ000FR8UejKUNgCP1pOcA0oTiRsuRFbJt8QtODLW70u0dMTvNsLpUDqL3whTzneQJAKM8UBeMj19AHwRS61PShIdIWtybCgNkm92xedSZPZ+RD0MAuKNMaR1pVwHOSKAWYiEE2P8Im7BpYyDFNFWYlkhGUobwKIRfngnIldi4cdN/Jqt8LQCuRKNJEO0EK8SJ/s1/n5bfKkSw7cuZIjacmtzXrwJ0RE3DvyUsTqiDtTQxTJjv2YlbsE98EKrBBGgPtcy/KiEMcAHf6meaA5zF3g5cfWW4vbOqZ5oC/Ho3siLFhDEJosXmdA1BzjROt9SOWaO8M9oKI1+ph/m3yGwKwQmKhgD7qKTq1NUDPfRNr8Lmpvc+pQnyu90tswM4CXX1JjAHU0wUTfX63Zk5tKPuY1EDrDSoEQF82pHZtE6n0hHsNKgRNP8x2sFRAjDFhygRLt8y1QFkQU7wgElmuU7DFUQAd0GKBHKfzRWQQScUgCJ5gVeqpStmxT4RDaoNCBRgWFAhsRu96bAC0EeaFkfSLQomo8TMrgo3ZKYOgNedjrR9tHlE6doAgib9gGJijoIChaFA6W+y9TTeXFLB23j8klhiTBjByTKd1j4WqRE1x3V5IgEHXB7UiHRSnTlUSURAZlvIFHRIK6GCLSXBCQSXohXSQRbPgESCS93qyRyj5+NSAdtyn4IonNDVHcimKsKJBLeZvkwlkF4yVup9QYtcAGJhE+NKH3CgtZOgESvd/HrlhUSCS9YqySCTSOBRCPRRW+VRLA1SCBRR3R7TyURBu0hAYnGorthOCE6lSayQCvf0LUg4eOzSS3e7DdxU2xBIu54RxVEoodNuJ5yXXFuq0GQCDY9AhOJGjuuc12d10p3zIWJgGuAUKJnQdNgc4eIB+nEV+dPLwkSYdhZGihR0RJkLNdPv7O34q6q80eLhdsIVkPw/pGogeK37cftS/ylYbkdeFHQRU0wUcEidaLr9fdFl1B7+GZAiBFBl9LBREXrxImKz/uJEUHPq8L3ykWPORUbXSEifkBWRCR8Ps4rcseEiBzoXjWcSDiQCDkF/UWICLYxIUUkPo91B/lDSaQg+OEtCSLxE5DGILeVRIgwOD5bgmgDOMNo5Z3qESCCbv3LEUFOXiFvlt1MAkRguyBH9AQ5j0Zwn/fL9oe0G4kQAQ8FSRJBQlQuTIPXbec03ncWL22PQmZ8jkT4vBQR9NCgThwTexhbRIfNYSWaSPIEO2QkvRGEyJI5HSFHtBFMzVKOCDgdL0WkjWTPE0OIPIkT+fLxR8DgFhkiudAWaSJgAJIMEWxRqzSRtpMKNQAQeZJ5hORjLY9yB9lFiWy5PleGaO5I2TtBIlfKzpUj0jrFUeXyRPB4CQVE2k7GhIsRyQ6ikkTaq0SsmBARBu2BKSTShnBviJsxZR7JsaSDyksTaWuwwTOO8VQ98/ShXSptUEmiTRuO5NFQmUDwuDCFRNrGV5X9SBGQgnxBx7IpxK5lrUrWR0FOp5mkP3RTGBj3UQmRtpSPg3srBenRlORGW5RKxpfKkAh//U1q8tftzyoGk+WrSK+qKsfgq1c2JZ9OSzgKnJTlgeyQcs1kDUrneQulMFfngcrO1NkMXFliS6X5VPdHT85CGF63fG7BWGpz3j74GM5keGtFHe4i1XmJH3wP5hYRelSbbFl97ujOTDR1dJAxjPZPxUWCVEV+7/nk7AlAubbnb+VWsPJUUQ7202ObBuv2mY1DLOpP1CS5faPq8uSPF31ETYe8CfPXDeJgej70qsr/X+27DOad3esQUS9IqGoGqVU9D3UP206VbzN4l/dNzPen6cPDw/S0r/bFDBc1b9Covxqi+qshqr8aovqrIaq/GqL6qyGqvxqi+qshqr8aovqrIaq/pIgo/SmZxP4dlEfUG6V6nnIr1LoukS9YRPtt+ouLjtyeUh7REFuJTOytklNXlRH1fqa/aGF6nig+wR6k5TQi6cHO1TD6geqIrGBhPJQbbMY48JcpFhAZ3dlF3TO2ESJ6uMpbJZG+Dn9xtibYRTr8XUgFRF6yUD2fYB2R0CBUScTlmO347C5S6I5ZEREXPbRnXQJfTltWSsSndusSePZ/AFGQTd64JLp5NyKNjV/oGVwIURAKe8m7EBONp53TG2u0WSz7s8OtVyjPf79Ye17OZi+jdAvmN6KJzcUsb0aHWX9ZZCtARH0S5l0IiXaDYKeL8mFtmxdq2YQQhw6TOztDgy5rX59iE9Mhv8+/JZhdbFu0H5P+RtTBaSaaA7VY0baJ8893gYhebIRPIVF3c7b0S3JVQpNa7g02lG3LsnVk0Ph8c5ewoTAM7BZC3MfsP5ipCS+2jXkG0QnH2YKCsnV2OWGDeaWM6JC0kb4+Gw42EA4eIHZ0i8eBNbSXi97kzD6O6941dH9o25ggM3gVJI0bb2gj4ix7vUeDDf9BBtEURyH3T6aLrPautwiOVFl5xwpBROdkHCHd9XbBXxd2GsrVNpATRTtMvCTEnZWiG95L8I8OKyAON380kR09sWdssCxvE22dKNzSZ3cvPDo0Zo1Ncw6pQIjYDQuT4wUZQ+3oXrOeHhpAbWQikpxr3llx/FDgecQh5nP2BA3fDPnkcTHwvhuF5vxG5OthCo0RN572lH9HVBmizYC19y4i8pKjL2326eUvrAG4DAZrF9FxVEoa1fpKoiKXNpft49mMEvy/JVo6UYzvmXV0jS8k2+ET9hk2C5sN7jBFsK5zCdgOUfkn7yrlV8+MQFgp6Qs7WS8KT24OdD1NU7Axo9Fy7TNMh1b0+gNWNkf6YOalwS3y61b9wMfqD880MG1R/716wrK7feFmleXTSW0s9uWoFDf5dGEhM6jM2LvK7bLWw5578esuvzhbrXGQSsR7iW9E6g2xHpuTWKPQ9yYXBb63a6Jo7NwkeiHXo87Xw0F3k4jdZnJYxOqt9TCu8uJ7R78Y+N52dLaY9QN7m1w+cvLSpRUR2elsZZ24wTeJVqyPvvm2kUk0YlUn6VSINb8eExnJlMwjy2jSt+JrYjm5Ke0KiOxddFt6mXPYmGhoXOfBYd++GLCbRME7HqLmjxURGf3oFxedMV8Wuro454kkbBl4ZbWR9fZ+aDlEbIheKSK6mVY5eKZdX53tCYGesLlErK9T3qb60di4SRT/+UZZRDMingdJHdHEvsontXGijB43idhz+Za5yiIKnl6iSXbUEQVuMmeQk3/eJNp4NzOYZBGxrwmnTlRHpBH+uR689yl8nd5NoiCK+0bqwCyiORVPTqyQaMk/Jh5wPJ++TdTD/Hx77IT9NYvoMpDSR9DWz1n1UkgUvKYJR/UJ8kVGDsZtosCZjn1vrWMb4ZpPJtGYotj3Dl7ATXJGlUKiS8iveeztx51XnEaAZhCN2WSJkMfp0763wrpujXOJtBENYl9Gp6fptm3lRsapJNKeKfMTLOyZhLmAcW60DCJtb7PpqI09bDFX1gnHVDaRtqUuch12uaOz25ZT61wiotObRIbBvQ966eg0fg7vj55tMF6CURL2ymblqe+9wHoyD9nMqG24umvYdBbPyrFuZb24YNq+lO0Sy8uNGskjmrX9wc3VdN9vp5H5j+yq1LOYLoe+fzxwiY/6bT+dN/TO/iB9so53K9/3V+m57+ezf872BjrLLiu7v8hfDG/2j+qvhqj+aojqr4ao/mqI6q+GqP5qiOqvhqj+aojqr4ao/mqI6q8/Ph3TF+37vaugWF+1f+9dBcX6pv1z7yooVktrfa5u95UR/XXvSihVixG1PtNI+nYh+kT97lcrJGr9uHdNFCkAColaf967Lkr031ZK1Gp9vXd1SutXRBITtVr//fX9y0fV97//l3D8H1WEA1U/uGdXAAAAAElFTkSuQmCC"),width = 8)





