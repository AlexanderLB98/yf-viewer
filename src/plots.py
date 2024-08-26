import streamlit as st
import pandas as pd
import plotly.graph_objects as go

########################################## Company ##########################################   


def plot_company(data):
    # Crear el gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], y=data['close'], mode='lines', name=f'{data["company_name"]} - Close'))
    # Configurar el diseño del gráfico
    fig.update_layout(title='Rendimiento de Compañías', 
                    xaxis_title='Fecha', 
                    yaxis_title='Precio', 
                    xaxis_tickformat='%Y-%m-%d',
                    width=900,
                        legend=dict(
                    title="Leyenda",  # Título de la leyenda
                    x=0.01,  # Posición en el eje x
                    y=0.99,  # Posición en el eje y
                    traceorder="normal",  # Orden de las trazas en la leyenda
                    bgcolor="LightSteelBlue",  # Color de fondo de la leyenda
                    bordercolor="Black",  # Color del borde de la leyenda
                    borderwidth=2  # Ancho del borde de la leyenda
                ))  # Ancho ajustado para ocupar la mayoría del espacio disponible

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)  # use_container_width=True ajusta automáticamente el ancho al contenedor de Streamlit








def plot_companies_history(data):
    """_summary_:
        

    Args:
        data (_type_): _description_
    """
    # Inicializar el estado de Streamlit para mantener la lista de compañías seleccionadas
    if 'selected_companies' not in st.session_state:
        st.session_state.selected_companies = []

    # Selector de Compañía
    company = st.selectbox("Seleccione una compañía:", data['company_name'].unique())

    # Filtrar datos por compañía seleccionada
    company_data = data[data['company_name'] == company]


    col1, col2 = st.columns(2)
    # Selector de Fecha Inicial con valor por defecto 30 días antes de la fecha máxima
    default_start_date = company_data['date'].min()
    # default_start_date = (company_data['date'].min() - pd.Timedelta(days=30)).date()
    start_date = col1.date_input("Seleccione la fecha inicial:", value=default_start_date, format="YYYY-MM-DD")

    # Selector de Fecha Final con valor por defecto como la fecha máxima en los datos
    default_end_date = company_data['date'].max()
    # default_end_date = company_data['date'].max().date()
    end_date = col2.date_input("Seleccione la fecha final:", value=default_end_date, format="YYYY-MM-DD")


    col1, col2, col3, col4, col5 = st.columns(5)

    # Checkbox para seleccionar métricas a graficar
    show_close = col2.checkbox("Mostrar Close", value=True)
    show_7_day_m = col3.checkbox("Mostrar 7 Day Moving Average", value=False)
    show_30_day_m = col4.checkbox("Mostrar 30 Day Moving Average", value=False)

    # Botón para añadir compañía
    if col1.button('Añadir Compañía'):
        if company not in st.session_state.selected_companies:
            st.session_state.selected_companies.append(company)

    # Botón para limpiar/resetear la selección de compañías
    if col5.button('Clear'):
        st.session_state.selected_companies = []

    # Filtrar datos por fechas seleccionadas
    filtered_data = company_data[(company_data['date'] >= start_date) & (company_data['date'] <= end_date)]
    # filtered_data = company_data[(company_data['date'] >= pd.to_datetime(start_date)) & (company_data['date'] <= pd.to_datetime(end_date))]

    # Crear el gráfico
    fig = go.Figure()

    # Añadir datos de la compañía seleccionada
    for company in st.session_state.selected_companies:
        company_data = data[data['company_name'] == company]
        filtered_data = company_data[(company_data['date'] >= start_date) & (company_data['date'] <= end_date)]
        # filtered_data = company_data[(company_data['date'] >= pd.to_datetime(start_date)) & (company_data['date'] <= pd.to_datetime(end_date))]
        
        if show_close:
            fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['close'], mode='lines', name=f'{company} - Close'))
        if show_7_day_m:
            fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['7_day_m'], mode='lines', name=f'{company} - 7 Day Moving Average'))
        if show_30_day_m:
            fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['30_day_m'], mode='lines', name=f'{company} - 30 Day Moving Average'))

    # Configurar el diseño del gráfico
    fig.update_layout(title='Rendimiento de Compañías', 
                    xaxis_title='Fecha', 
                    yaxis_title='Precio', 
                    xaxis_tickformat='%Y-%m-%d',
                    width=900,
                        legend=dict(
                    title="Leyenda",  # Título de la leyenda
                    x=0.01,  # Posición en el eje x
                    y=0.99,  # Posición en el eje y
                    traceorder="normal",  # Orden de las trazas en la leyenda
                    bgcolor="LightSteelBlue",  # Color de fondo de la leyenda
                    bordercolor="Black",  # Color del borde de la leyenda
                    borderwidth=2  # Ancho del borde de la leyenda
                ))  # Ancho ajustado para ocupar la mayoría del espacio disponible

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)  # use_container_width=True ajusta automáticamente el ancho al contenedor de Streamlit






