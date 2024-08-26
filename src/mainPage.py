import pandas as pd
import streamlit as st

from src.database import Database
from src.plots import plot_companies_history, plot_company
from src.yfmanager import Yfmanager
from src.sidebar import sideBar



def mainPage():
    st.header("Hello World")
    
    
    selected_models = sideBar()
    
    # Display selected models in different columns
    if selected_models:
        st.write("Selected Models:")
        cols = st.columns(len(selected_models))
        for idx, model in enumerate(selected_models):
            cols[idx].write(model)
    else:
        st.write("No models selected")
    
    
    
    db = Database()
    
    conn = db._connect()
    
    #st.session_state.df_stocks = pd.read_sql("SELECT * FROM dbo.stock_data ORDER BY date", con=conn)
    # st.write(st.session_state.df_stocks.head())
    
    st.session_state.df_companies = db.get_companies()
    st.write(st.session_state.df_companies)
    st.write("Number of companies: " + str(len(st.session_state.df_companies)))
    
    
    
    
    st.write(db.get_markets())
    st.session_state.selected_market = st.selectbox("Select Market", db.get_markets())
    
    
    
    
    
    
    # st.write(db.get_companies(st.session_state.selected_market))
    # st.session_state.selected_company = st.selectbox("Select Company", db.get_companies(st.session_state.selected_market)["company_name"])
    # st.write(st.session_state.selected_company)
    
    
    
    

    # Muestra el DataFrame de compañías basado en el mercado seleccionado
    st.write(db.get_companies(st.session_state.selected_market))

    # Obtén el DataFrame de compañías
    companies_df = db.get_companies(st.session_state.selected_market)

    # Crear el selectbox que muestra 'company_name' pero devuelve 'company_code'
    selected_name = st.selectbox("Select Company", companies_df["company_name"])

    # Usar el nombre seleccionado para obtener el código de la compañía correspondiente
    st.session_state.selected_company = companies_df.loc[companies_df["company_name"] == selected_name, "company_code"].values[0]

    # Mostrar el código de la compañía seleccionada
    st.write(st.session_state.selected_company)
    st.session_state.df_selected_company = db.get_data(st.session_state.selected_company)
    st.write(st.session_state.df_selected_company)
    ############
    

    
    # st.session_state.df = pd.merge(st.session_state.df_stocks, st.session_state.df_companies, on="company_code")
    # st.write(st.session_state.df.head())
    

    # Tengo que hacer el join para sacar el company name en el df
    plot_company(st.session_state.df_selected_company)
    
    # plot_companies_history(st.session_state.df)
    
    st.write()
    
    if st.sidebar.button('Download historical Data (DONT TOUCH!)'):
        yf = Yfmanager()
        st.session_state.historical_data = yf.download_all_historical_data(st.session_state.df_companies["company_code"])
        st.write(st.session_state.historical_data)    
    
        if st.session_state.historical_data is not None:
            st.write(st.session_state.historical_data)
            db.add_df_to_postgresql(st.session_state.historical_data)