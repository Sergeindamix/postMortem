# app.py
import streamlit as st
from embeddings import embed_text 
from search import buscar
import pandas as pd


df = pd.read_csv('embeddings.csv') 

st.title("Buscador Semántico")

query = st.text_input("Consulta")
n_results = st.number_input("Número de resultados", min_value=1, max_value=10, value=5)

if query:

  results = buscar(query, df, n_results)
  
  with st.expander("Resultados"):
  
    for i, row in results.iterrows():
      st.write(row['texto'])
