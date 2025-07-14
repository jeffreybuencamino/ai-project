import streamlit as st
import os
import pandas as pd

#=== Title ===
st.title("Title: Streamlit project ")

#=== Dataframe Section
st.subheader('Streamlit Dataframe Demo (Elements)')
df = pd.DataFrame({
    'Name': ["Geo", "Mike", "Jeff", "Jemima"],
    "Age": [62, 27, 27, 18],
    "Occupation": ["Senior Dev", "Aerospace Engineer", "Unemployed", "Unemployed"]
})
st.dataframe(df)

#=== Data Editor Section (Editable dataframe) ====
st.subheader("Data Editor")
editable_df = st.data_editor(df)
#===xtra code ===
st.markdown('# Markdown Header\n\n Here is a .txt in **Markdown** format.')
st.caption('small text bitch')
code_example = """
# ==== How to make function ====
def greet(name):
    print('hello', name)

user_name = "jeffrey"
greet(user_name)
"""
st.code(code_example, language="Python")
st.image(os.path.join(os.getcwd(),'static', "IMG_5815 2.jpeg"))