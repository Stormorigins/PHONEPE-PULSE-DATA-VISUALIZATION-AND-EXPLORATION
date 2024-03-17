#LIBRARIES

import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
from streamlit_option_menu import option_menu
import requests
import json
from PIL import Image


#SQL CONNECTION
myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='root',database = "phonepe",port=3306)
cur = myconnection.cursor()

#DATAFRAMES COVERT

#Agg_TX_data
cur.execute("select * from agg_tx")
myconnection.commit()
F1 = cur.fetchall()

AGG_TX_DF= pd.DataFrame(F1, columns=('States', 'Years', 'Quaters', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))


#Agg_US_data
cur.execute("select * from agg_us")
myconnection.commit()
F2 = cur.fetchall()

AGG_US_DF= pd.DataFrame(F2, columns=('States', 'Years', 'Quaters', 'Brands', 'Transaction_count', 'Percentage'))


#Agg_INS_data
cur.execute("select * from agg_ins")
myconnection.commit()
F3 = cur.fetchall()

AGG_INS_DF= pd.DataFrame(F3, columns=('States', 'Years', 'Quaters', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))


#MAP_TX_data
cur.execute("select * from map_tx")
myconnection.commit()
F4 = cur.fetchall()

MAP_TX_DF= pd.DataFrame(F4, columns=('States', 'Years', 'Quaters', 'Districts', 'Transaction_count', 'Transaction_amount'))


#MAP_US_data
cur.execute("select * from map_user")
myconnection.commit()
F5 = cur.fetchall()

MAP_US_DF= pd.DataFrame(F5, columns=('States', 'Years', 'Quaters', 'Districts', 'Registered_Users', 'App_Opens'))


#MAP_INS_data
cur.execute("select * from map_ins")
myconnection.commit()
F6 = cur.fetchall()

MAP_INS_DF= pd.DataFrame(F6, columns=('States', 'Years', 'Quaters', 'Districts', 'Transaction_count', 'Transaction_amount'))


#TOP_TX_data
cur.execute("select * from top_tx")
myconnection.commit()
F7 = cur.fetchall()

TOP_TX_DF= pd.DataFrame(F7, columns=('States', 'Years', 'Quaters', 'Pincodes', 'Transaction_count', 'Transaction_amount'))


#TOP_US_data
cur.execute("select * from top_user")
myconnection.commit()
F8 = cur.fetchall()

TOP_US_DF= pd.DataFrame(F8, columns=('States', 'Years', 'Quaters', 'Pincodes', 'Registered_Users'))


#MAP_INS_data
cur.execute("select * from top_ins")
myconnection.commit()
F9 = cur.fetchall()

TOP_INS_DF= pd.DataFrame(F9, columns=('States', 'Years', 'Quaters', 'Pincodes', 'Transaction_count', 'Transaction_amount'))

#FUNCTIONS

#TRANSACTION COUNT AND AMOUNT SORTED BY YEAR

def TX_count_amount(DF, YR):    
    year=DF[DF["Years"]==YR]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group_year.reset_index(inplace = True)

    col1, col2= st.columns(2)
    with col1:

        fig_count= px.bar(group_year, x="States", y="Transaction_count", title=f"{YR} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluyl_r,height=600, width=600)
        st.plotly_chart(fig_count)

    with col2:

        fig_amount= px.bar(group_year, x="States", y="Transaction_amount", title=f"{YR} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Reds, height=600, width=600)
        st.plotly_chart(fig_amount)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    data = requests.get(url)
    coordinate=json.loads(data.content)
    state_names=[]
    for i in coordinate["features"]:
        A=i["properties"]["ST_NM"]
        state_names.append(A)

    state_names.sort()

    col1, col2= st.columns(2)
    with col1:

        fig_geo_count=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="ylgnbu",height=600,width=600,
                                range_color=(group_year["Transaction_count"].min(),group_year["Transaction_count"].max()),
                                hover_name="States", title= f"{YR} TRANSACTION COUNT",fitbounds="locations")
        fig_geo_count.update_geos(visible= False)
        st.plotly_chart(fig_geo_count)
    
    with col2:

        fig_geo_amount=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="ylorrd",height=600,width=600,
                                range_color=(group_year["Transaction_amount"].min(),group_year["Transaction_amount"].max()),
                                hover_name="States", title= f"{YR} TRANSACTION AMOUNT",fitbounds="locations")
        fig_geo_amount.update_geos(visible= False)
        st.plotly_chart(fig_geo_amount)
    
    return year

#SORTED TRANSACTION COUNT AND AMOUNT GROUPED BY QUARTER

def TX_count_amount_Q(DF, Q):    
    year=DF[DF["Quaters"]==Q]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    group_year.reset_index(inplace = True)

    col1, col2= st.columns(2)
    with col1:

        fig_count= px.bar(group_year, x="States", y="Transaction_count", title=f"{year["Years"].min()} YEAR {Q} QUATER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluyl_r,height=600, width=600)
        st.plotly_chart(fig_count)
        
    with col2:

        fig_amount= px.bar(group_year, x="States", y="Transaction_amount", title=f"{year["Years"].min()} YEAR {Q} QUATER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Reds, height=600, width=600)
        st.plotly_chart(fig_amount)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    data = requests.get(url)
    coordinate=json.loads(data.content)
    state_names=[]
    for i in coordinate["features"]:
        A=i["properties"]["ST_NM"]
        state_names.append(A)

    state_names.sort()
    col1, col2= st.columns(2)
    with col1:

        fig_geo_count=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Tealgrn",height=600,width=600,
                                range_color=(group_year["Transaction_count"].min(),group_year["Transaction_count"].max()),
                                hover_name="States", title= f"{year["Years"].min()} YEAR {Q} QUATER TRANSACTION COUNT",fitbounds="locations")
        fig_geo_count.update_geos(visible= False)
        st.plotly_chart(fig_geo_count)

    with col2:

        fig_geo_amount=px.choropleth(group_year, geojson=coordinate, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="solar",height=600,width=600,
                                range_color=(group_year["Transaction_amount"].min(),group_year["Transaction_amount"].max()),
                                hover_name="States", title= f"{year["Years"].min()} YEAR {Q} QUATER TRANSACTION AMOUNT",fitbounds="locations")
        fig_geo_amount.update_geos(visible= False)
        st.plotly_chart(fig_geo_amount)
    return year

#AGGRATED DATA FUNCTIONS

#TRANSACTION

def agg_txtype(DF,state):

    year=DF[DF["States"]== state]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby(["States","Transaction_type"])[["Transaction_count","Transaction_amount"]].sum()
    group_year.reset_index(inplace = True)

    col1, col2= st.columns(2)
    with col1:

        figpie_count=px.pie(data_frame=group_year,names="Transaction_type", values="Transaction_count",title=f"{state.upper()} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluyl_r, hole= 0.1, width=600)
        st.plotly_chart(figpie_count)

    with col2:
        
        figpie_amount=px.pie(data_frame=group_year,names="Transaction_type", values="Transaction_amount",title=f"{state.upper()} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r,hole= 0.1, width=600)
        st.plotly_chart(figpie_amount)   
    

#USER

def aggusbra(DF,YR):

    year=DF[DF["Years"]==YR]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby("Brands")[["Transaction_count","Percentage"]].sum()
    group_year.reset_index(inplace = True)

    
    fig_count= px.bar(group_year, x="Brands", y="Transaction_count", title=f"{YR} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Blackbody_r, width=1000,hover_name="Brands")
    st.plotly_chart(fig_count)


    fig_amount= px.bar(group_year, x="Brands", y="Percentage", title=f"{YR} PERCENTAGE",
                    color_discrete_sequence=px.colors.sequential.Rainbow, width=1000, hover_name="Brands")
    st.plotly_chart(fig_amount)

    return year




def Agguser_yr_b(DF,state):
    year=DF[DF["States"]==state]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby(["Brands", "Quaters"])[[ "Transaction_count"]].sum()
    group_year.reset_index(inplace = True)

    fig_count= px.bar(year, x="Brands", y="Transaction_count", title=f"{year["Years"].min()} YEAR {state.upper()} Transaction Count",
                            color_continuous_scale=px.colors.sequential.tempo_r, height=800,width=1000, hover_name="Quaters")  

    st.plotly_chart(fig_count)
    return year

#MAP DATA FUNCTIONS

#INSURANCE

def Mapins_yr_dis(DF,Dis):

    year=DF[DF["States"]== Dis]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    group_year.reset_index(inplace = True)

    col1, col2= st.columns(2)
    with col1:
        fig_count= px.bar(group_year, x="Transaction_count", y="Districts",orientation="h", title=f"{Dis.upper()} DISTRICT & TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_count)

    with col2:
        fig_amount= px.bar(group_year, x="Transaction_amount", y="Districts",orientation="h", title=f"{Dis.upper()} DISTRICT & TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.Cividis)
        st.plotly_chart(fig_amount)
    
    return year

#USER

def Mapuser(DF,YR):
    year=DF[DF["Years"]==YR]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby("States")[[ "Registered_Users","App_Opens"]].sum()
    group_year.reset_index(inplace = True)

    fig_count= px.line(group_year, x="States", y=["Registered_Users","App_Opens"], title=f"{YR} REGISTERED USERS & APP OPENS",
                        markers= True, width=1000, height=800)

    st.plotly_chart(fig_count)

    return year

def Mapuser_Q(DF,Q):
    year=DF[DF["Quaters"]==Q]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby("States")[[ "Registered_Users","App_Opens"]].sum()
    group_year.reset_index(inplace = True)

    fig_count= px.line(group_year, x="States", y=["Registered_Users","App_Opens"], title=f"{DF['Years'].min()} YEAR {Q} QUATER REGISTERED USERS & APP OPENS",
                        markers= True, width=1000, height=800)
    st.plotly_chart(fig_count)

    return year

def MapuserY_Q_S(DF,State):
    year=DF[DF["States"]==State]
    year.reset_index(drop= True, inplace = True)

    col1, col2= st.columns(2)
    with col1:
        fig_rig= px.bar(year, x="Registered_Users", y="Districts", title=f"{year["Years"].min()} YEAR {year["Quaters"].min()} QUATER {State.upper()} REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.tempo_r, height=800)
        st.plotly_chart(fig_rig)

    with col2:   

        fig_apps= px.bar(year, x="App_Opens", y="Districts", title=f"{year["Years"].min()} YEAR {year["Quaters"].min()} QUATER {State.upper()} App_Opens",
                            color_discrete_sequence=px.colors.sequential.Redor, height=800)
        st.plotly_chart(fig_apps)
        
    return year

#TOP DATA FUNCTIONS

#INSURANCE


def Topins_yr_pin(DF,state):

    year=DF[DF["States"]==state]
    year.reset_index(drop= True, inplace = True)

    col1, col2= st.columns(2)
    with col1:
        fig_count= px.bar(year, x="Quaters", y="Transaction_count", title=f"{year["Years"].min()} YEAR  TRANSACTION COUNT & PINCODES ",
                        color_discrete_sequence=px.colors.sequential.tempo_r, hover_name="Pincodes",width= 600)  

        st.plotly_chart(fig_count)
    with col2:

        fig_amount= px.bar(year, x="Quaters", y="Transaction_amount", title=f"{year["Years"].min()} YEAR  TRANSACTION AMOUNT & PINCODES ",
                        color_discrete_sequence=px.colors.sequential.Electric_r ,hover_name="Pincodes",width= 600)  

        st.plotly_chart(fig_amount)

#USER
        
def Topuser_yr(DF,YR):

    year=DF[DF["Years"]==YR]
    year.reset_index(drop= True, inplace = True)

    group_year=year.groupby(["States", "Quaters"])[[ "Registered_Users"]].sum()
    group_year.reset_index(inplace = True)

    fig_count= px.bar(group_year, x="States", y="Registered_Users",hover_name="States", title=f"{YR} REGISTERED USERS",color="Quaters",
                       color_discrete_sequence=px.colors.sequential.Emrld_r,height=800, width= 1100)

    st.plotly_chart(fig_count)

    return year


def Topuser_yr_pin(DF,state):
    year=DF[DF["States"]==state]
    year.reset_index(drop= True, inplace = True)

    fig_count= px.bar(year, x="Quaters", y="Registered_Users", title=f"{year["Years"].min()} YEAR {state.upper()} REGISTERED USERS & PINCODES",
                            color_continuous_scale=px.colors.sequential.tempo_r, width=1000, hover_name="Pincodes")  

    st.plotly_chart(fig_count)
    return year


#STREAMLIT PART


st.set_page_config(layout="wide")
st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select = option_menu("Main menu",["Home", "Data Exploration", "Top charts"],)

if select=="Home":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Aishwarya MMPL\Documents\GUVI_PYTHON\Projects\Phonepeproject\Image\Logo.jpg"))

    col3,col4= st.columns(2)
    
    with col3:

        st.image(Image.open(r"C:\Users\Aishwarya MMPL\Documents\GUVI_PYTHON\Projects\Phonepeproject\Image\phonepes-1682424517.jpg"))

    with col4:
            st.write("****Easy Transactions****")
            st.write("****One App For All Your Payments****")
            st.write("****Your Bank Account Is All You Need****")
            st.write("****Multiple Payment Modes****")
            st.write("****PhonePe Merchants****")
            st.write("****Multiple Ways To Pay****")
            st.write("****1.Direct Transfer & More****")
            st.write("****2.QR Code****")
            st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:

            st.write("****No Wallet Top-Up Required****")
            st.write("****Pay Directly From Any Bank To Any Bank A/C****")
            st.write("****Instantly & Free****")

    with col6:

        st.image(Image.open(r"C:\Users\Aishwarya MMPL\Documents\GUVI_PYTHON\Projects\Phonepeproject\Image\download.jpg"))


elif select == "Data Exploration":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method1= st.radio("select the method", ["Aggregated Transaction Analysis", "Aggregated User Analysis", "Aggregated Insurance Analysis"])

        if method1 == "Aggregated Transaction Analysis":
            col1, col2, col3= st.columns(3)
            with col2:

                YR=st.slider('Select the year of Aggregated Transaction',AGG_TX_DF["Years"].min(), AGG_TX_DF["Years"].max(), AGG_TX_DF["Years"].min())
            AGGTX_Y_DATA= TX_count_amount(AGG_TX_DF,YR)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the state',(AGGTX_Y_DATA["States"].unique()))
            agg_txtype(AGGTX_Y_DATA,state)    

            col1, col2, col3= st.columns(3)
            with col2:

                Quat=st.slider('Select the Quater',AGGTX_Y_DATA["Quaters"].min(), AGGTX_Y_DATA["Quaters"].max(), AGGTX_Y_DATA["Quaters"].min())
            AGGTX_Y_Q_DATA=TX_count_amount_Q(AGGTX_Y_DATA,Quat)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the state of Aggregated Quater)',(AGGTX_Y_Q_DATA["States"].unique()))
            agg_txtype(AGGTX_Y_Q_DATA,state) 

        elif method1 == "Aggregated User Analysis":
            col1, col2, col3= st.columns(3)
            with col2:
                YR=st.slider('Select the year',AGG_US_DF["Years"].min(), AGG_US_DF["Years"].max(), AGG_US_DF["Years"].min())
            AGGUSYEAR=aggusbra(AGG_US_DF,YR)

            

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the state',(AGGUSYEAR["States"].unique()))
            AGGUSY_Q_S=Agguser_yr_b(AGGUSYEAR,state)

        elif method1 == "Aggregated Insurance Analysis":
                col1, col2, col3= st.columns(3)
                with col2:
                    YR=st.slider('Select the year',AGG_INS_DF["Years"].min(), AGG_INS_DF["Years"].max(), AGG_INS_DF["Years"].min())
                AGGINSDATA= TX_count_amount(AGG_INS_DF,YR)

                col1, col2, col3= st.columns(3)
                with col2:
                    Quat=st.slider('Select the Quater',AGGINSDATA["Quaters"].min(), AGGINSDATA["Quaters"].max(), AGGINSDATA["Quaters"].min())
                TX_count_amount_Q(AGGINSDATA,Quat)

    with tab2:

        method2= st.radio("select the method", ["Map Transaction Analysis", "Map User Analysis", "Map Insurance Analysis"])

        if method2 == "Map Transaction Analysis":
            col1, col2, col3= st.columns(3)
            with col2:
                    YR=st.slider('Select the year of Map Transaction',MAP_TX_DF["Years"].min(), MAP_TX_DF["Years"].max(), MAP_TX_DF["Years"].min())
            MAPTXDATA_Y= TX_count_amount(MAP_TX_DF,YR)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the Districts (state)',(MAPTXDATA_Y["States"].unique()))
            Mapins_yr_dis(MAPTXDATA_Y,state)
            
            col1, col2, col3= st.columns(3)
            with col2:
                Quat=st.slider('Select the Quater of Transaction',MAPTXDATA_Y["Quaters"].min(), MAPTXDATA_Y["Quaters"].max(), MAPTXDATA_Y["Quaters"].min())
            MAPTXDATA_Y_Q= TX_count_amount_Q(MAPTXDATA_Y,Quat)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the State of Map Quater)',(MAPTXDATA_Y_Q["States"].unique()))
            Mapins_yr_dis(MAPTXDATA_Y_Q,state) 

        elif method2 == "Map User Analysis":
            col1, col2, col3= st.columns(3)
            with col2:
                    YR=st.slider('Select the year of Map User',MAP_US_DF["Years"].min(), MAP_US_DF["Years"].max(), MAP_US_DF["Years"].min())
            MAPUSERDATA_Y= Mapuser(MAP_US_DF,YR)

            col1, col2, col3= st.columns(3)
            with col2:
                Quat=st.slider('Select the Quater of Map User',MAPUSERDATA_Y["Quaters"].min(), MAPUSERDATA_Y["Quaters"].max(), MAPUSERDATA_Y["Quaters"].min())
            MAPUSERDATA_Y_Q= Mapuser_Q(MAPUSERDATA_Y, Quat)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the state of map User',(MAPUSERDATA_Y_Q["States"].unique()))
            MapuserY_Q_S(MAPUSERDATA_Y_Q,state)

        elif method2 == "Map Insurance Analysis":
            col1, col2, col3= st.columns(3)
            with col2:
                    YR=st.slider('Select the year of Insurance',MAP_INS_DF["Years"].min(), MAP_INS_DF["Years"].max(), MAP_INS_DF["Years"].min())
            MAPINSDATA_Y= TX_count_amount(MAP_INS_DF,YR)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the state of map insurance',(MAPINSDATA_Y["States"].unique()))
            Mapins_yr_dis(MAPINSDATA_Y,state)
            
            col1, col2, col3= st.columns(3)
            with col2:
                Quat=st.slider('Select the Quater of Insurance',MAPINSDATA_Y["Quaters"].min(), MAPINSDATA_Y["Quaters"].max(), MAPINSDATA_Y["Quaters"].min())
            MAPINSDATA_Y_Q= TX_count_amount_Q(MAPINSDATA_Y,Quat)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the Quater (state)',(MAPINSDATA_Y_Q["States"].unique()))
            Mapins_yr_dis(MAPINSDATA_Y_Q,state)         

    with tab3:

        method3= st.radio("select the method", ["Top Transaction Analysis", "Top User Analysis", "Top Insurance Analysis"])

        if method3 == "Top Transaction Analysis":
            col1, col2, col3= st.columns(3)
            with col2:

                YR=st.slider('Select the year of Top Transaction',TOP_TX_DF["Years"].min(), TOP_TX_DF["Years"].max(), TOP_TX_DF["Years"].min())
            TOPTXDATA_Y= TX_count_amount(TOP_TX_DF,YR)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the state of Top Transaction',(TOPTXDATA_Y["States"].unique()))
            Topins_yr_pin(TOPTXDATA_Y,state)  

            col1, col2, col3= st.columns(3)
            with col2:

                Quat=st.slider('Select the Quater of Top Transaction',TOPTXDATA_Y["Quaters"].min(), TOPTXDATA_Y["Quaters"].max(), TOPTXDATA_Y["Quaters"].min())
            TOPINSDATA_Y_Q= TX_count_amount_Q(TOPTXDATA_Y,Quat)

        elif method3 == "Top User Analysis":
            col1, col2, col3= st.columns(3)
            with col2:

                YR=st.slider('Select the year of Top User',TOP_US_DF["Years"].min(), TOP_US_DF["Years"].max(), TOP_US_DF["Years"].min())
            TOPUSDATA_Y_S_Q=Topuser_yr(TOP_US_DF,YR)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the state of Top User',(TOPUSDATA_Y_S_Q["States"].unique()))
            Topuser_yr_pin(TOPUSDATA_Y_S_Q,state)

        elif method3 == "Top Insurance Analysis":
            col1, col2, col3= st.columns(3)
            with col2:

                YR=st.slider('Select the year of Top Insurance',TOP_INS_DF["Years"].min(), TOP_INS_DF["Years"].max(), TOP_INS_DF["Years"].min())
            TOPINSDATA_Y= TX_count_amount(TOP_INS_DF,YR)

            col1, col2, col3= st.columns(3)
            with col2:

                state = st.selectbox('Please Select the stateof Top Insurance',(TOPINSDATA_Y["States"].unique()))
            TOPINSDATA_Y_PIN= Topins_yr_pin(TOPINSDATA_Y,state)   

            col1, col2, col3= st.columns(3)
            with col2:

                Quat=st.slider('Select the Quater of Top Insurance',TOPINSDATA_Y["Quaters"].min(), TOPINSDATA_Y["Quaters"].max(), TOPINSDATA_Y["Quaters"].min())
            TOPINSDATA_Y_Q=TX_count_amount_Q(TOPINSDATA_Y,Quat)

elif select == "Top charts":

    myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='root',database = "phonepe",port=3306)
    cur = myconnection.cursor()

    Questions = st.selectbox('Please Select Your Question',
                            ('1. Top 10 states With Highest Aggregated Trasaction Amount?','2. Top 10 states With Lowest Aggregated Trasaction Amount?',
                             '3. Top 10 mobile brands with Highest transaction count?', '4. Top 10 mobile brands with lowest transaction count?', 
                             '5. Top 10 Registered-users based on District?','6. Top 10 Districts based on states with highest amount of transaction?',
                             '7. Top 10 Districts based on states with Lowest amount of transaction?', '8. Top 10 States based on Districts with Highest amount of APP OPENS?',
                             '9. Top 10 States based on Districts with Lowest amount of APP OPENS?', '10. Plot a bar chart with all the pincodes based on transaction amount by each states?'),index = None)
    


    if Questions =='1. Top 10 states With Highest Aggregated Trasaction Amount?':
        Query1 = '''select States, sum(Transaction_amount) as Transaction_Amount from agg_tx group by States order by Transaction_Amount desc limit 10;'''
        cur.execute(Query1)
        myconnection.commit()
        F1=cur.fetchall()
        DF1 = pd.DataFrame(F1,columns = ["States", "Transaction_Amount"])
        fig_count= px.bar(DF1, x="States", y="Transaction_Amount", title="Highest Trasaction Amount",
                                    color_continuous_scale=px.colors.sequential.deep_r, height=600, width=1000, hover_name="States") 
        st.write(DF1)
        st.plotly_chart(fig_count)

    elif Questions =='2. Top 10 states With Lowest Aggregated Trasaction Amount?':
        Query2 = '''select States, sum(Transaction_amount) as Transaction_Amount from agg_tx group by States order by Transaction_Amount asc limit 10;'''
        cur.execute(Query2)
        myconnection.commit()
        F2=cur.fetchall()
        DF2 = pd.DataFrame(F2,columns = ["States", "Transaction_Amount"])

        fig_count= px.bar(DF2, x="States", y="Transaction_Amount", title="Lowest Trasaction Amount",
                                    color_continuous_scale=px.colors.sequential.deep_r, height=600, width=1000, hover_name="States")  
        st.write(DF2)
        st.plotly_chart(fig_count)

    elif Questions =='3. Top 10 mobile brands with Highest transaction count?':

        Query3 = '''select Brands, sum(Transaction_count) as Transaction_Count  from agg_us group by Brands order by Transaction_Count desc limit 10;'''
        cur.execute(Query3)
        myconnection.commit()
        F3=cur.fetchall()

        DF3 = pd.DataFrame(F3,columns = ["Brands", "Transaction_Count"])

        fig_count= px.bar(DF3, x="Brands", y="Transaction_Count", title="Highest Trasaction count",
                                    color_continuous_scale=px.colors.sequential.deep_r, height=600, width=1000, hover_name="Brands")  

        st.write(DF3)
        st.plotly_chart(fig_count)

    elif Questions =='4. Top 10 mobile brands with lowest transaction count?':

        Query4 = '''select Brands, sum(Transaction_count) as Transaction_Count  from agg_us group by Brands order by Transaction_Count asc limit 10; '''
        cur.execute(Query4)
        myconnection.commit()
        F4=cur.fetchall()

        DF4 = pd.DataFrame(F4,columns = ["Brands", "Transaction_Count"])

        fig_count= px.bar(DF4, x="Brands", y="Transaction_Count", title="Lowest Trasaction count",
                                    color_continuous_scale=px.colors.sequential.deep_r, height=600,width=1000, hover_name="Brands")  

        st.write(DF4)
        st.plotly_chart(fig_count)

    elif Questions =='5. Top 10 Registered-users based on District?':

        Query5 = '''select States, Districts,  Registered_Users from map_user group by Districts order by Registered_Users desc limit 10;'''
        cur.execute(Query5)
        myconnection.commit()
        F5=cur.fetchall()

        DF5 = pd.DataFrame(F5,columns = ["States", "Districts", "Registered_Users"])

        fig_count= px.line(DF5, x="Districts", y="Registered_Users", title="REGISTERED USERS", orientation="h",
                                    height=600,width=1000, hover_name="States", markers= True)  

        st.write(DF5)
        st.plotly_chart(fig_count)

    elif Questions =='6. Top 10 Districts based on states with highest amount of transaction?':

        Query6 = '''select States, Districts, sum(Transaction_amount) as Transaction_Amount from map_tx group by Districts order by Transaction_Amount desc limit 10;'''
        cur.execute(Query6)
        myconnection.commit()
        F6=cur.fetchall()

        DF6 = pd.DataFrame(F6,columns = ["States", "Districts", "Transaction_Amount"])

        fig_count= px.bar(DF6, x="Districts", y="Transaction_Amount", title="Transaction_Amount by District", orientation="v",
                                    height=600,width=1000, hover_name="States")  

        st.write(DF6)
        st.plotly_chart(fig_count)

    elif Questions =='7. Top 10 Districts based on states with Lowest amount of transaction?':

        Query7 = '''select States, Districts, sum(Transaction_amount) as Transaction_Amount from map_tx group by Districts order by Transaction_Amount asc limit 10;'''
        cur.execute(Query7)
        myconnection.commit()
        F7=cur.fetchall()

        DF7 = pd.DataFrame(F7,columns = ["States", "Districts", "Transaction_Amount"])

        fig_count= px.bar(DF7, x="Districts", y="Transaction_Amount", title="Transaction_Amount by District", orientation="v",
                                    height=600,width=1000, hover_name="States")  

        st.write(DF7)
        st.plotly_chart(fig_count)

    elif Questions =='8. Top 10 States based on Districts with Highest amount of APP OPENS?':

        Query8 = '''select States, Districts, sum(App_Opens) as APP_OPENS from map_user group by States order by APP_OPENS desc limit 10;'''
        cur.execute(Query8)
        myconnection.commit()
        F8=cur.fetchall()

        DF8 = pd.DataFrame(F8,columns = ["States", "Districts", "APP_OPENS"])

        fig_count= px.line(DF8, x="States", y="APP_OPENS", title="APP OPENS", orientation="h",
                                    height=600, width=1000,hover_name="Districts", markers= True)  

        st.write(DF8)
        st.plotly_chart(fig_count)

    elif Questions =='9. Top 10 States based on Districts with Lowest amount of APP OPENS?':

        Query9 = '''select States, Districts, sum(App_Opens) as APP_OPENS from map_user group by States order by APP_OPENS asc limit 10;'''
        cur.execute(Query9)
        myconnection.commit()
        F9=cur.fetchall()

        DF9 = pd.DataFrame(F9,columns = ["States", "Districts", "APP_OPENS"])

        fig_count= px.bar(DF9, x="States", y="APP_OPENS", title="APP OPENS",
                                    height=600,width=1000, hover_name="Districts")  

        st.write(DF9)
        st.plotly_chart(fig_count)

    elif Questions =='10. Plot a bar chart with all the pincodes based on transaction amount by each states?':

        Query10 = '''select States, Pincodes, sum(Transaction_amount) as Transaction_Amount from top_ins group by Pincodes'''
        cur.execute(Query10)
        myconnection.commit()
        F10=cur.fetchall()

        DF10 = pd.DataFrame(F10,columns = ["States", "Pincodes", "Transaction_Amount"])

        fig_count= px.bar(DF10, x="States", y="Transaction_Amount", title="Pincodes",
                                    height=600,width=1000, hover_name="Pincodes")  

        st.write(DF10)
        st.plotly_chart(fig_count)

        
