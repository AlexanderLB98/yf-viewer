import streamlit as st
import os

import json
import pandas as pd
import psycopg2 as sql

import datetime

class Database:
    
    def __init__(self, scheme = "dbo"):
        try:
            config = self._load_config()
        except Exception as e:
            st.write(e)
            
        self.host = config["host"]
        self.port = config["port"]
        self.dbname = config["database"]
        self.user = config["user"]
        self.password = config["password"]
        self.connection = None
        self.scheme = scheme
        
    def _load_config(self):
        config_path = os.path.expanduser('~/.creds/config_postgres.json')
        with open(config_path, "r") as f:
            config = json.load(f)
            return config['postgres']


    def _connect(self):
        try:
            self.connection = sql.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Succesfully conected to PostgreSQL")
            return self.connection
        except (Exception, sql.Error) as error:
            print("Error connecting to PostgreSQL:", error)
            return False
            
    def _close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed correctly.")
            
    def get_companies(self, market = None):
        """_summary_
        Get a pd.DataFrame with every company in the database
        """
        self._connect()
        if market is None:
            self.df_companies = pd.read_sql("SELECT * FROM dbo.company", con = self.connection)
            self._close_connection()
            return self.df_companies
        else:
            self.df_companies_market = pd.read_sql("SELECT * FROM dbo.company WHERE market = %(market)s", con = self.connection, params={"market": market})
            self._close_connection()
            return self.df_companies_market
        
    
    def get_markets(self):
        if self.df_companies is None:
            self.get_companies()
        else:
            self.markets = self.df_companies["market"].unique()
            return self.markets
            
    def get_data(self, company):
        self._connect()
        df = pd.read_sql("SELECT * FROM dbo.stock_data WHERE company_code = %(company)s", con = self.connection, params={"company": company})
        df_merge = pd.merge(df, self.df_companies, on="company_code")
        self._close_connection()
        return df_merge
        

    def _add_individual_share(self, table_name: str = "stock_data", values: list = []):
        """Add 1 line to the database 

        Args:
            table_name (_type_): 
                Nombre de la tabla:
                    - company, shares...
            valores (list): 
                Lista de valores a añadir:
                    - company_code: string
                    - date: datetime
                    - open: float
                    - High: float
                    - Low: flaot
                    - close: float
                    - Adj Close: float
                    - volume: integer
        """   
        
        try:
            values, flag = self._check_data(values)
            if flag:
                cursor = self.connection.cursor()
                
                values = ', '.join([f"'{val}'" for val in values])
                print(values)
                consulta = f"INSERT INTO {self.scheme}.{table_name} VALUES ({values});"
                cursor.execute(consulta)
                
                #self.connection.autocommit(True)
                self.connection.commit()
                print(f"Valores agregados a la tabla '{self.scheme}.{table_name}' exitosamente.")
                cursor.close()
        except (Exception, sql.Error) as error:
            print("Error al agregar valores:", error)
            self.connection.rollback() # Revert transaction in case of error


    def add_df_to_postgresql(self, df, company: str = None):
        
        result = []
        
        self._connect()
        for index, df in df.iterrows():        
            """
                cada linea del df tendrá que lanzar la query de añadir dato
            """
            try:
                if isinstance(df["Date"], pd.Timestamp):
                    # df["Date"] = df["Date"].strftime("%Y-%m-%d")  # Convertir Timestamp a cadena
                    df["Date"] = df["Date"].to_pydatetime()
                    #print(df)
                    date = df["Date"]
                    #print(type(date))
                    # date = df["Date"].date()
                else:
                    date = datetime.datetime.strptime(df["Date"], "%Y-%m-%d")
                #print(date)
                if company == None:
                    company_str = df["company_code"]
                else:
                    company_str = company
                    
                values = [company_str, date, float(df["Open"]), float(df["High"]), float(df["Low"]), float(df["Close"]), float(df["Adj Close"]), int(df["Volume"])]
                
                self._add_individual_share(table_name="stock_data", values=values)
                print('Data added correctly.')
                result.append(values)
                
            except Exception as e:
                print("Error ocurred: " + str(e))
                
        self._close_connection()
        return result



    def _check_data(self, valores, table="stock_data"):
        if table == "stock_data":
            # Verificar que la lista de valores tenga el formato correcto
            if len(valores) != 8:
                print("Error: La lista 'valores' debe contener exactamente 7 elementos.")
                """
                Lista de valores a añadir:        
                    - company_code: string
                    - date: datetime
                    - open: float
                    - High: float
                    - Low: flaot
                    - close: float
                    - Adj Close: float
                    - volume: integer
                """
                return valores, False

            # Desempaquetar los valores de la lista
            company_code, date, open_val, high_val, low_val, close_val, adj_close, volume = valores

            # Verificar que los valores estén en el formato correcto
            if not isinstance(company_code, str):
                print("Error: 'company_code' debe ser una cadena de caracteres.")
                return valores, False
            
            if not isinstance(date, datetime.date):
                print("Error: 'date' debe ser un objeto de fecha.")
                if isinstance(date, datetime.datetime.timestamp):
                    date_str = valores["Date"].strftime("%Y-%m-%d")  # Convertir Timestamp a cadena
                    return date_str, True
                return valores, False
            
                
            if open_val is not None and not isinstance(open_val, (int, float)):
                print("Error: 'open_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if high_val is not None and not isinstance(high_val, (int, float)):
                print("Error: 'high_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if low_val is not None and not isinstance(low_val, (int, float)):
                print("Error: 'low_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if close_val is not None and not isinstance(close_val, (int, float)):
                print("Error: 'close_val' debe ser un número entero o de punto flotante.")
                return valores, False
            if adj_close is not None and not isinstance(adj_close, (int, float)):
                print("Error: 'adj_close' debe ser un número entero o de punto flotante.")
                return valores, False
            if volume is not None and not isinstance(volume, int):
                print("Error: 'volume' debe ser un número entero.")
                return valores, False
            else:
                print("data in correct format")
                return valores, True
            
            
        elif table == "company":
            # Desempaquetar los valores de la lista
            company_code, company_name, market = valores

            # Verificar que los valores estén en el formato correcto
            if not isinstance(company_code, str):
                print("Error: 'company_code' debe ser una cadena de caracteres.")
                return valores, False
            if not isinstance(company_name, str):
                print("Error: 'company_name' debe ser una cadena de caracteres.")
                return valores, False
            if not isinstance(market, str):
                print("Error: 'market' debe ser una cadena de caracteres.")
                return valores, False
            else:
                print("data in correct format")
                return valores, True
        