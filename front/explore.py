from io import StringIO
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

@st.cache
def load_data():
    raw_data = requests.get('https://desolate-oasis-06152.herokuapp.com/dataset')
    data = pd.read_csv(StringIO(str(raw_data.content,'utf-8')))
    return data

def display_explore_page():
    st.title('Explore the diabetes study data.')

    st.write(
        """
        ### Diabetes tests alongside personal health data.
        """
    )
    data_load_state = st.text('Loading data...')
    data = load_data()
    data = data.drop('Unnamed: 0', axis = 1)
    data_load_state.text('Finished fetching data!')
    st.subheader('Raw data')
    st.write(data )
    
    import plotly.graph_objects as go
    fig_bmi = go.Figure()
    fig_bmi.add_trace(go.Histogram(x=data[data['Diabetes_binary'] == 0]['BMI'], name = 'Diabetes'))
    fig_bmi.add_trace(go.Histogram(x=data[data['Diabetes_binary'] == 1]['BMI'], name = 'No diabetes'))
    fig_bmi.update_layout(barmode='overlay', xaxis_title_text='Body mass index', yaxis_title_text='Count')
    fig_bmi.update_traces(opacity=0.6)

    st.subheader('Diabetes cases per BMI distribution')
    st.plotly_chart(fig_bmi, use_container_width = True)
    
    fig_income = go.Figure()
    fig_income.add_trace(go.Histogram(x=data[data['Diabetes_binary'] == 0]['Income'], name = 'Diabetes'))
    fig_income.add_trace(go.Histogram(x=data[data['Diabetes_binary'] == 1]['Income'], name = 'No diabetes'))
    fig_income.update_layout(barmode='overlay', xaxis_title_text='Income category', yaxis_title_text='Count')
    fig_income.update_xaxes(type='category')
    fig_income.update_traces(opacity=0.6)

    st.subheader('Confirmed diabetes cases per household income category.')

    st.plotly_chart(fig_income, use_container_width = True)
    st.write(""">Household income categories are calculated as following:
    Category: 1 -> less than 10k USD annual income.
    Category: 2 -> less than 15k USD annual income.
                    ...
    Category: 7 -> less than 75k USD annaul income.
    Category: 8 -> more or equal than 75k USD annual income.
    """)
    # Correlation matrix of all dataset columns

    fig_mental = go.Figure()
    fig_mental.add_trace(go.Histogram(x=data[data['Diabetes_binary'] == 0]['MentHlth'], name = 'Diabetes'))
    fig_mental.add_trace(go.Histogram(x=data[data['Diabetes_binary'] == 1]['MentHlth'], name = 'No diabetes'))
    fig_mental.update_layout(barmode='overlay', xaxis_title_text='Days with mental health issues during last month', yaxis_title_text='Count')
    fig_mental.update_traces(opacity=0.6)

    st.subheader('Confirmed diabetes cases per mental health issues in last 30 days')
    st.plotly_chart(fig_mental, use_container_width = True)

     
    corr_matrix = data.corr()
    fig_corr =px.imshow(corr_matrix,
        labels = dict(color = 'Correlation'),
        x = data.columns,
        y = data.columns
    )

    st.subheader('Correlation of all dataset columns') 
    st.plotly_chart(fig_corr, use_container_width=True)
    

    
    

    



    