"""_summary_
    Main script to run the streamlit app using "streamlit run app.py"
"""


import streamlit as st

from src.mainPage import mainPage

def main():
    
    
    st.set_page_config(layout="wide")
    
    

        
    mainPage()
    
if __name__ == "__main__":
    main()