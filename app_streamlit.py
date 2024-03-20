import streamlit as st
import numpy as np
import pandas as pd
from DB import df

st.markdown("""# Bienvenue sur notre app !
## DataFrames 
This is text""")

df = pd.read_csv('conso-elec-gaz-commune.csv', sep=';')


line_count = st.slider('Select a line count', 1, 10, 3)


head_df = df.head(line_count)

head_df