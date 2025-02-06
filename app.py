"""_summary_
    Main script to run the streamlit app using "streamlit run app.py"
"""


import streamlit as st

from src.mainPage import mainPage
from src.view_local_data_page import view_local_data_page

def main():
    
    
    st.set_page_config(layout="wide")
    view_local_data_page()
    
    

    
        
   #  mainPage()
    
if __name__ == "__main__":
    main()
