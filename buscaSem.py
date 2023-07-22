import streamlit as st
import pandas as pd
from scipy import spatial
from transformers import BertModel, BertTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity

def embed_text(df):

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    embeddings = []

    for text in df['texto']:

        inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            embedding = outputs[0][0][0]

        embeddings.append(embedding.numpy())

    df['Embedding'] = embeddings

    return df

def get_embedding(query):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    # Tokenizar consulta
    inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt")

    # Obtener embedding
    with torch.no_grad():
        outputs = model(**inputs)
        return outputs[0][0][0].numpy()

def buscar(busqueda, texto_emb, n_resultados=5):

    # Obtener embedding de la consulta
    embedding_consulta = get_embedding(busqueda)

    # Calcular similitud con cada fila
    similitudes = []
    for embedding in texto_emb['Embedding']:
        similarity = cosine_similarity([embedding_consulta], [embedding])
        similitudes.append(similarity[0][0])

    # Verificar que el número de similitudes coincida con el número de filas
    if len(similitudes) != len(texto_emb):
        raise ValueError("La cantidad de similitudes no coincide con la cantidad de filas en el DataFrame")

    # Agregar las similitudes al dataframe
    texto_emb['Similarity'] = similitudes

    # Ordenar el dataframe por similitud de mayor a menor
    df_sorted = texto_emb.sort_values(by='Similarity', ascending=False)

    # Devolver filas correspondientes
    return df_sorted[['texto', 'Similarity']].head(n_resultados)

def main():
    st.title("Búsqueda de Texto con Bert Embeddings")

    # Obtener la consulta del usuario
    consulta = st.text_input("Escribe tu consulta:")

    uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Leer el archivo CSV cargado por el usuario
        df = pd.read_csv(uploaded_file)

        # Procesar el texto y obtener los embeddings
        texto_emb = embed_text(df)

        if consulta:
            # Realizar la búsqueda con la consulta ingresada
            resultados = buscar(consulta, texto_emb)

            # Mostrar los resultados en una tabla
            st.table(resultados)


if __name__ == "__main__":
    main()
