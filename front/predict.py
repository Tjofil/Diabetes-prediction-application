import json
import streamlit as st
import requests as rq
import plotly.express as px
from explore import load_data
import numpy as np

def predict(features):
    return json.loads(rq.post('https://desolate-oasis-06152.herokuapp.com/predict', json=features).content)['Outcome']
    

def display_predict_page():
    st.title('Diabetes prediction using Machine Learning')
    st.write('''### Plug in your personal information to predict the disease.''')
    sex = st.selectbox('Sex', ('Male', 'Female'))
    high_bp = st.checkbox('Do you have high blood preasure ?', value = False)
    st.write('>Having 130 or more for systolic and 80 or more for diastolic blood pressure is considered having a high blood pressure.')
    chol_check = st.checkbox('Have you checked your blood cholesterol in last 5 years ?', value = False)
    high_chol = st.checkbox('Do you have high cholesterol ?', value = False)
    st.write('>Having 240 or more total blood cholesterol level is considered having a high cholesterol.')
    bmi = st.slider('Body mass index', max_value= 98, min_value= 12)
    st.write('>[Find about and calculate your BMI.](https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm)')
    smoker = st.checkbox('Have you smoked at least 100 cigarettes in your entire life ?', value = False)
    stroke = st.checkbox('Have you experienced a stroke in your life ?', value = False)
    heart = st.checkbox('Have you experienced a heart attack or are suffering from heart diseases ?', value = False)
    phys_act = st.checkbox('Have you had any physical activity in past 30 days?', value = False)
    fruits = st.checkbox('Do you consume at least one fruit per day ?', value = False)
    veggies = st.checkbox('Do you consume at least one vegetable per day ?', value = False)
    hvy_alcohol = st.checkbox('Do you practice heavy alcohol consumption ?', value = False)
    st.write('>Consuming at least 14 for men and at least 7 for women alcoholic drinks per week is considered heavy alcohol consumption.')
    healthcare = st.checkbox('Do you have any kind of health care coverage, including health insurance and prepaid plans?', value= False)
    cost = st.checkbox('Was there a time in the past 12 months when you needed to see a doctor but could not because of the cost? ', value=False)
    gen_hlth = st.slider('You would say that in general your health is (on scale from 1 to 5)',  min_value=1, max_value=5, step = 1) 
    diff_walk = st.checkbox('Do you have any difficulties walking ?', value = False)
    age = st.number_input('Your age', value= 24)
    age_category = 1 if age<= 24 else 2 + (age - 25)//5

    menth_hlth = st.slider('Number days of poor mental health in previous 30 days', min_value = 0, max_value = 30)
    phys_htlh = st.slider('Number days of poor physical health in previous 30 days', min_value = 0, max_value = 30)

    education = st.slider('Education level on scale 1-6', min_value=1, max_value=6, step = 1)
    income = st.number_input('Your annual household income in $', value = 15000)
    income_category = 1 + (income - 10000)//5000
    if income_category < 1: income_category = 1
    if income_category > 8: income_category = 8

    features = {
    "HighBP":  high_bp,
    "HighChol":  high_chol,
    "CholCheck":  chol_check,
    "BMI":  bmi,
    "Smoker":  smoker,
    "Stroke":  stroke,
    "HeartDiseaseorAttack":  heart,
    "PhysActivity":  phys_act,
    "Fruits":  fruits,
    "Veggies":  veggies,
    "HvyAlcoholConsump":  hvy_alcohol,
    "AnyHealthcare":  healthcare,
    "NoDocbcCost":  cost,
    "GenHlth":  gen_hlth,
    "MentHlth":  menth_hlth,
    "PhysHlth":  phys_htlh,
    "DiffWalk":  diff_walk,
    "Sex":  1 if sex == 'Male' else 0,
    "Age":  age_category,
    "Education":  education,
    "Income":  income_category
    }

    calc = st.button('Calculate the diabetes prediction')
    if calc:
        prediction = predict(features)
        st.write(f'### Based on the model prediction you likely {"" if prediction else "_dont_"} have diabetes')


        data = load_data()
        data = data.drop('Unnamed: 0', axis = 1)
        data = data.rename(columns={'Diabetes_binary' : 'Class'})
        features['Class'] = 2
        data = data.append(dict(features), ignore_index=True)
        data['Class'] = data['Class'].astype(str)
        data = data.replace({"Class": {"1" : "Has diabetes", "0" : "Doesn't have diabetes", "2" : "You"}})
        fig = px.scatter(data, x="BMI", y="Age", color="Class", hover_data=list(features.keys()))

        st.plotly_chart(fig, use_container_width=True)

        st.write(""">Age categories are calculated as following:
    Category: 1 -> 24y old or younger.
    Category: 2 -> 25-29y old.
                    ...
    Category: 12 -> 75-79y old.
    Category: 13 -> more than 79 y old.
    """)




