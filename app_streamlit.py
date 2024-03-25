import streamlit as st
import numpy as np
import folium
from maps import main
from DB import df # import du DataFrame df depuis la DB

st.markdown("""# Bienvenue sur notre app !!
## DataFrames """)


code_departement = st.selectbox('Code département', np.sort(df['code_departement'].unique()))

df_filtered = df[df['code_departement'] == code_departement]


line_count = st.slider('Select a line count', 1, 1000, 50)


head_df = df_filtered.head(line_count)

head_df

st.markdown("""## Carte des régions de France""")

main()