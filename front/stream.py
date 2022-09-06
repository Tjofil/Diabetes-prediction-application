import streamlit as st 
import pandas as pd
import numpy as np
from predict import display_predict_page
from explore import display_explore_page

page = st.sidebar.selectbox('Explore or predict the data', ('Explore', 'Predict'))
if page == 'Explore':
    display_explore_page()
else:
    display_predict_page()
