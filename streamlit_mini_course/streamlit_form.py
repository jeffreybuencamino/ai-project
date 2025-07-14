import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title('User info form')

form_values = {
    'name': None,
    "height": None,
    "gender": None,
    "dob": None
}

min_date = datetime(1990, 1, 1)
maximum_date = datetime.now()

with st.form(key='user-info_form'):
    form_values['name'] = st.text_input("enter your name: ")
    form_values['height'] = st.number_input('enter your age: ')
    form_values['gender'] = st.selectbox('Gender', ["Male", 'Female'])
    form_values['dob'] = st.date_input("Enter your birthdate", max_value=maximum_date, min_value=min_date)

    submit_button = st.form_submit_button(label="Submit Form")
    if submit_button:
        if not all(form_values.values()):
            st.warning('Please fill in all of the fields.')
        else:
            st.balloons()
            st.write('### Info')
            print(form_values)
            for (key, value) in form_values.items():
                st.write(f'{key}: {value}')