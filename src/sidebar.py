
import streamlit as st
import yaml



def get_models_list():
    
    try:
        with open('../config/config_training.yaml', 'r') as file:
            config = yaml.safe_load(file)
            model_list = list(config['ml']['models'].keys())
    except Exception as e:
        print(e)
        # Predefined model list
        model_list = [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "Gradient Boosting",
            "Support Vector Machine",
            "K-Nearest Neighbors",
            "Neural Network"
        ]
        
        

    return model_list



def initialize_session_state(model_list):
    if 'model_states' not in st.session_state:
        st.session_state.model_states = {model: True for model in model_list}
    if 'select_all' not in st.session_state:
        st.session_state.select_all = False
        

def select_all_models():
    for model in st.session_state.model_states:
        st.session_state.model_states[model] = True
    st.session_state.select_all = True

def sideBar():
    model_list = get_models_list()
    initialize_session_state(model_list)
    
    # Title of the sidebar
    st.sidebar.title('Select Machine Learning Models')
    
    # Button to select all models
    if st.sidebar.button("Select All Models"):
        select_all_models()
    
    # Checkboxes for different machine learning models
    models = {}
    for model in st.session_state.model_states:
        if st.session_state.select_all:
            st.session_state[f"checkbox_{model}"] = True
        
        checkbox_value = st.sidebar.checkbox(
            model, 
            value=st.session_state.model_states[model],
            key=f"checkbox_{model}"
        )
        models[model] = checkbox_value
        st.session_state.model_states[model] = checkbox_value
    
    # Reset select_all flag
    st.session_state.select_all = False

    # Store selected models in a list
    selected_models = [model for model, selected in models.items() if selected]
    
    
    # display_CTlogo_sidebar()
    
    return selected_models