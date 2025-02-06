import pandas as pd
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

from src.local_data.fetch_local_data import fetch_index_dict, fetch_local_data


def view_local_data_page(load_csv=False, config=None):
    st.header("Data downloaded")
    if load_csv:
        st.session_state.df = fetch_local_data("/home/lucas/projects/DE-yf-raspi/data")
        st.metric("Number of rows", len(st.session_state.df))
        st.metric("Number of tickers", int(st.session_state.df["Ticker"].nunique()))
        st.dataframe(st.session_state.df["Ticker"].unique())
        df = st.session_state.df 
        st.dataframe(df.head())
        analysis_template(st.session_state.df)
    else:
        st.session_state.index_dict = fetch_index_dict("/home/lucas/projects/DE-yf-raspi/data")

        index_df = pd.DataFrame([(key, value, len(value)) for key, value in st.session_state.index_dict.items()], columns=["Index", "Companies", "n_companies"])
        st.dataframe(index_df)



def preprocess_data(df):
    data = df.drop(df.columns[0], axis=1)
    
    data['date'] = pd.to_datetime(data['Date'])

    # Daily return
    data['daily_return'] = data['Close'].pct_change() # pct_change es como el diff()

    # Season info
    data['month'] = data['date'].dt.month
    data['season'] = data['month'] % 12 // 3 + 1
    data['season'] = data['season'].replace({1: 'winter', 2: 'spring', 3: 'summer', 4: 'autumn'})

    data['7_day_m'] = data['Close'].rolling(window=7).mean()
    data['30_day_m'] = data['Close'].rolling(window=30).mean()

    data['price_std'] = data['Close'].rolling(window=30).std()
    
    data = data[30:]
    
    return data

def display_basic_information(data: pd.DataFrame):
    """
    This function displays a quick preview of the data.
    The following colunmns are required in the dataset
        - Country
        - Market
        - Region
    """
    col1, col2, col3 = st.columns(3)
    # Mostrar la distribución por país, mercado y región en círculos de quesos (pie charts)
    
    # Calcular el número de entradas por país
    country_counts = data['country'].value_counts()
    # Preparar datos para el pie chart
    labels = country_counts.index.tolist()
    values = country_counts.values.tolist()

    # Mostrar el círculo de quesos (pie chart)
    fig = px.pie(names=labels, values=values, title='Distribución de Entradas por País')
    col1.plotly_chart(fig, use_container_width=True)
    
    country_counts = data['market'].value_counts()
    # Preparar datos para el pie chart
    labels = country_counts.index.tolist()
    values = country_counts.values.tolist()

    # Mostrar el círculo de quesos (pie chart)
    fig = px.pie(names=labels, values=values, title='Distribución de Entradas por mercado')
    col2.plotly_chart(fig, use_container_width=True)

    country_counts = data['region'].value_counts()
    # Preparar datos para el pie chart
    labels = country_counts.index.tolist()
    values = country_counts.values.tolist()

    # Mostrar el círculo de quesos (pie chart)
    fig = px.pie(names=labels, values=values, title='Distribución de Entradas por región')
    col3.plotly_chart(fig, use_container_width=True)
    
 
def display_region_info(data: pd.DataFrame):
    st.header("Region")
    # Selector de Región
    region = st.selectbox(
        "Seleccione una región:",
        ("All", "Europa", "América del Norte")
    )

    
    
    # Selecciono los datos según la opción
    if region != "All":
        # Filter data
        df_region = data[data["region"] == region]
    else:
        df_region = data
        

        
        
    col11, col12 = st.columns(2)
        
    # Gráfico de Barras - Retorno Diario Promedio por Empresa
    mean_daily_return_by_company = df_region.groupby('company_name')['daily_return'].mean().sort_values(ascending=False)
    fig_company = px.bar(mean_daily_return_by_company, 
                        x=mean_daily_return_by_company.index, 
                        y=mean_daily_return_by_company, 
                        labels={'x': 'Empresa', 'y': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por Empresa en la región seleccionada')
    fig_company.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col11.plotly_chart(fig_company)


    # Gráfico de Barras - Retorno Diario Promedio por Empresa
    mean_daily_return_by_company = df_region.groupby('season')['daily_return'].mean()
    fig_company = px.bar(mean_daily_return_by_company, 
                        x=mean_daily_return_by_company.index, 
                        y=mean_daily_return_by_company, 
                        labels={'x': 'Empresa', 'y': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por estación en la región seleccionada')
    col12.plotly_chart(fig_company)




            
    col11, col12 = st.columns(2)

    # Gráfico de Barras - Retorno Diario Promedio por Mercado
    mean_daily_return_by_market = df_region.groupby('market')['daily_return'].mean().sort_values(ascending=False).reset_index()
    fig_market = px.bar(mean_daily_return_by_market, 
                        x='market', 
                        y='daily_return', 
                        labels={'market': 'Mercado', 'daily_return': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por Mercado en la región seleccionada')
    fig_market.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col11.plotly_chart(fig_market)
                
                
                
    # Gráfico de Barras - Retorno Diario Promedio por País
    mean_daily_return_by_country = df_region.groupby('country')['daily_return'].mean().sort_values(ascending=False).reset_index()
    fig_country = px.bar(mean_daily_return_by_country, 
                        x='country', 
                        y='daily_return', 
                        labels={'country': 'País', 'daily_return': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por País en la región seleccionada')
    fig_country.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col12.plotly_chart(fig_country)
                    

def display_country_info(data):
    st.header("Country")
    
    # Selector de País
    all_countries = data['country'].unique()
    selected_countries = st.multiselect("Seleccione uno o varios países:", all_countries, default=all_countries)

    # Filtrar los datos según los países seleccionados
    df_country = data[data['country'].isin(selected_countries)]
            
   
    col11, col12 = st.columns(2)
  
    # Gráfico de Barras - Retorno Diario Promedio por Empresa
    mean_daily_return_by_company = df_country.groupby('company_name')['daily_return'].mean().sort_values(ascending=False)
    fig_company = px.bar(mean_daily_return_by_company, 
                        x=mean_daily_return_by_company.index, 
                        y=mean_daily_return_by_company, 
                        labels={'x': 'Empresa', 'y': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por Empresa en los paises seleccionados')
    fig_company.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col11.plotly_chart(fig_company)


    # Gráfico de Barras - Retorno Diario Promedio por Empresa
    mean_daily_return_by_company = df_country.groupby('season')['daily_return'].mean()
    fig_company = px.bar(mean_daily_return_by_company, 
                        x=mean_daily_return_by_company.index, 
                        y=mean_daily_return_by_company, 
                        labels={'x': 'Empresa', 'y': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por estación en los paises seleccionados')
    col12.plotly_chart(fig_company)


            
    col11, col12 = st.columns(2)

    # Gráfico de Barras - Retorno Diario Promedio por Mercado
    mean_daily_return_by_market = df_country.groupby('market')['daily_return'].mean().sort_values(ascending=False).reset_index()
    fig_market = px.bar(mean_daily_return_by_market, 
                        x='market', 
                        y='daily_return', 
                        labels={'market': 'Mercado', 'daily_return': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por Mercado en los paises seleccionados')
    fig_market.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col11.plotly_chart(fig_market)
                            
    # Gráfico de Barras - Retorno Diario Promedio por País
    mean_daily_return_by_country = df_country.groupby('country')['daily_return'].mean().sort_values(ascending=False).reset_index()
    fig_country = px.bar(mean_daily_return_by_country, 
                        x='country', 
                        y='daily_return', 
                        labels={'country': 'País', 'daily_return': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por País en los paises seleccionados')
    fig_country.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col12.plotly_chart(fig_country)
                    

def display_market_info(data):
    st.header("Market")
       
    # Selector de País
    all_markets = data['market'].unique()
    selected_markets = st.multiselect("Seleccione uno o varios países:", all_markets, default=all_markets)

    # Filtrar los datos según los países seleccionados
    df_market = data[data['market'].isin(selected_markets)]
            
   
    col11, col12 = st.columns(2)
        
    # Gráfico de Barras - Retorno Diario Promedio por Empresa
    mean_daily_return_by_company = df_market.groupby('company_name')['daily_return'].mean().sort_values(ascending=False)
    fig_company = px.bar(mean_daily_return_by_company, 
                        x=mean_daily_return_by_company.index, 
                        y=mean_daily_return_by_company, 
                        labels={'x': 'Empresa', 'y': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por Empresa en los mercados seleccionados')
    fig_company.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col11.plotly_chart(fig_company)


    # Gráfico de Barras - Retorno Diario Promedio por Empresa
    mean_daily_return_by_company = df_market.groupby('season')['daily_return'].mean()
    fig_company = px.bar(mean_daily_return_by_company, 
                        x=mean_daily_return_by_company.index, 
                        y=mean_daily_return_by_company, 
                        labels={'x': 'Empresa', 'y': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por estación en los mercados seleccionados')
    col12.plotly_chart(fig_company)




            
    col11, col12 = st.columns(2)


    # Gráfico de Barras - Retorno Diario Promedio por Mercado
    mean_daily_return_by_market = df_market.groupby('market')['daily_return'].mean().sort_values(ascending=False).reset_index()
    fig_market = px.bar(mean_daily_return_by_market, 
                        x='market', 
                        y='daily_return', 
                        labels={'market': 'Mercado', 'daily_return': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por Mercado en los mercados seleccionados')
    fig_market.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col11.plotly_chart(fig_market)
                
                
                
    # Gráfico de Barras - Retorno Diario Promedio por País
    mean_daily_return_by_market = df_market.groupby('market')['daily_return'].mean().sort_values(ascending=False).reset_index()
    fig_market = px.bar(mean_daily_return_by_market, 
                        x='market', 
                        y='daily_return', 
                        labels={'market': 'País', 'daily_return': 'Retorno Diario Promedio'},
                        title='Retorno Diario Promedio por País en los mercados seleccionados')
    fig_market.update_layout(xaxis_tickangle=-45)  # Girar los nombres del eje x 45 grados
    col12.plotly_chart(fig_market)
                    


def display_company_info(data):
    # Selector de Compañía
    company = st.selectbox("Seleccione una compañía:", data['Ticker'].unique())

    # Filtrar datos por compañía seleccionada
    company_data = data[data['Ticker'] == company]


    col1, col2 = st.columns(2)
    # Selector de Fecha Inicial con valor por defecto 30 días antes de la fecha máxima
    default_start_date = (company_data['date'].min() - pd.Timedelta(days=30)).date()
    start_date = col1.date_input("Seleccione la fecha inicial:", value=default_start_date, format="YYYY-MM-DD")

    # Selector de Fecha Final con valor por defecto como la fecha máxima en los datos
    default_end_date = company_data['date'].max().date()
    end_date = col2.date_input("Seleccione la fecha final:", value=default_end_date, format="YYYY-MM-DD")


    col1, col2, col3, col4, col5 = st.columns(5)

    # Checkbox para seleccionar métricas a graficar
    show_close = col2.checkbox("Mostrar Close", value=True)
    show_7_day_m = col3.checkbox("Mostrar 7 Day Moving Average", value=True)
    show_30_day_m = col4.checkbox("Mostrar 30 Day Moving Average", value=True)

    # Botón para añadir compañía
    if col1.button('Añadir Compañía'):
        if company not in st.session_state.selected_companies:
            st.session_state.selected_companies.append(company)

    # Botón para limpiar/resetear la selección de compañías
    if col5.button('Clear'):
        st.session_state.selected_companies = []

    # Filtrar datos por fechas seleccionadas
    filtered_data = company_data[(company_data['date'] >= pd.to_datetime(start_date)) & (company_data['date'] <= pd.to_datetime(end_date))]

    # Crear el gráfico
    fig = go.Figure()

    # Añadir datos de la compañía seleccionada
    for company in st.session_state.selected_companies:
        company_data = data[data['Ticker'] == company]
        filtered_data = company_data[(company_data['date'] >= pd.to_datetime(start_date)) & (company_data['date'] <= pd.to_datetime(end_date))]
        
        
        if show_close:
            fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['Close'], mode='lines', name=f'{company} - Close'))
        if show_7_day_m:
            fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['7_day_m'][7:], mode='lines', name=f'{company} - 7 Day Moving Average'))
        if show_30_day_m:
            fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['30_day_m'][30:], mode='lines', name=f'{company} - 30 Day Moving Average'))

    # Configurar el diseño del gráfico
    fig.update_layout(title='Rendimiento de Compañías', 
                    xaxis_title='Fecha', 
                    yaxis_title='Precio', 
                    xaxis_tickformat='%Y-%m-%d',
                    width=900)  # Ancho ajustado para ocupar la mayoría del espacio disponible

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)  # use_container_width=True ajusta automáticamente el ancho al contenedor de Streamlit


def display_map(data):
    # Diccionario de traducción de nombres de países
    translation_dict = {
        'Bélgica': 'Belgium',
        'España': 'Spain',
        'Estados Unidos': 'United States of America',
        'Europa': 'Europe',
        'Países Bajos': 'Netherlands'
    }

    # Traducir los nombres de los países en el DataFrame
    data['country'] = data['country'].map(translation_dict)
    
    col1, col2 = st.columns(2)
    min_date = data['date'].min().date()
    max_date = data['date'].max().date()
    # Selector de Fecha Inicial con valor por defecto 30 días antes de la fecha máxima
    default_start_date = (data['date'].min() + pd.Timedelta(days=30)).date()
    start_date = col1.date_input("Seleccione la fecha inicial:", 
                                value=default_start_date, 
                                format="YYYY-MM-DD", 
                                min_value=min_date,
                                max_value=max_date,
                                key="begin date for map")

    # Selector de Fecha Final con valor por defecto como la fecha máxima en los datos
    default_end_date = data['date'].max().date()
    end_date = col2.date_input("Seleccione la fecha final:", 
                                value=default_end_date, 
                                format="YYYY-MM-DD", 
                                min_value=min_date,
                                max_value=max_date,
                                key="end date for map")


    # Filtrar datos por fechas seleccionadas
    df_volume =  data[(data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))]

    
    # Sumar el volumen por país
    sum_volume = df_volume.groupby('country')['volume'].sum().reset_index()
    

    # Cargar el archivo GeoJSON de los países
    geojson_path = 'data/countries.geo.json'
    gdf = gpd.read_file(geojson_path)

    # Filtrar el GeoDataFrame para conservar solo los países que tienen datos en sum_volume
    gdf_filtered = gdf.merge(sum_volume, left_on='name', right_on='country', how='inner')

    # Plotear el mapa interactivo con Plotly Express
    fig = px.choropleth(gdf_filtered, 
                        geojson=gdf_filtered.geometry, 
                        locations=gdf_filtered.index,  # Utilizar el índice de gdf_filtered como locations
                        color='volume',  # Usar 'sales' como medida de color
                        hover_name='country',
                        projection='mercator',
                        color_continuous_scale='Viridis',
                        range_color=(0, sum_volume['volume'].max()),  # Ajustar el rango según los datos
                        labels={'volume': 'Ventas'},
                        title='Volumen por País en el periodo del ' + str(start_date) + ' al ' + str(end_date),
                        height=1200)  # Ajustar la altura del gráfico

    fig.update_geos(showcountries=True, countrycolor="darkgrey")

    # Centrar el título del gráfico
    fig.update_layout(title_x=0.38)
    
    # Mostrar el mapa en Streamlit
    st.plotly_chart(fig, use_container_width=True)






def analysis_template(df: pd.DataFrame):
    # REF: all this functions are inherited from my previous project (https://github.com/AlexanderLB98/Visualization-Proyect)
    # Includes month, season, and rolling means
    data = preprocess_data(df)

    # Mostrar el número total de filas del dataset
    st.subheader('Basic Information')
    st.write(f"Dataset has {len(data)} rows.")
    
   
            
    if 'country' and 'market' and 'region' in data.columns:
        display_basic_information(data)

    ########################################## REGION ##########################################
    if 'region' in data.columns:
        display_region_info(data)

    ########################################## COUNTRY ##########################################           
    if 'country' in data.columns:
        display_country_info(data)
        
    ########################################## MARKET ##########################################                   
    if 'market' in data.columns:
        display_market_info(data)

    ########################################## Company ##########################################   
    display_company_info(data)
    # Inicializar el estado de Streamlit para mantener la lista de compañías seleccionadas
#     if 'selected_companies' not in st.session_state:
#         st.session_state.selected_companies = []

    ########################################## Mapa ##########################################   
    if False:
        display_map(data)



