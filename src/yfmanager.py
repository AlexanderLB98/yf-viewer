
import pandas as pd
from datetime import date, timedelta
import yfinance as yf
import streamlit as st

class Yfmanager:
    
    def __init__(self, config=None):
        self.config = config
    
    def download_historical_data(self, companies: list, verbose: int= 1) -> pd.DataFrame():
        df = pd.DataFrame()

        for company in companies:
            try:
                data = yf.download(company, start=date(1900,1,1), end=date.today())
                data = data.reset_index()
                data["company_code"] = company
                df = pd.concat([df, data])
            except Exception as e:
                print(e)
            
        if verbose > 0:
            print(df.head())
        
        return df    
            
        

    def download_all_historical_data(self, companies: list):
        """
        Function to download all historical data for all companies in the Database    
        """
        

        # First fetch the list of all companies
        if not isinstance(companies, list):
            companies = list(companies)
        
        st.write(companies)
        print(type(companies))
        
        df = self.download_historical_data(companies)
        
        return df
        
        