import pandas as pd
from scipy import spatial
from transformers import BertModel, BertTokenizer
import torch

def get_embedding(query):

  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertModel.from_pretrained('bert-base-uncased')
  # Tokenizar consulta
  inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt")  

  # Obtener embedding
  with torch.no_grad():
    outputs = model(**inputs)
    return outputs[0][0][0].numpy()

def buscar(busqueda, datos, n_resultados=5):

  # Obtener embedding de la consulta
  # Obtener embedding
  embedding_consulta = get_embedding(busqueda)
  # Aplanar a 1D
  embedding_consulta = embedding_consulta.flatten()
  
    
  # Calcular similitud con cada fila
  similitudes = []
  import numpy as np

  for i, fila in datos.iterrows():
    emb_texto = fila['Embedding']    
    emb_texto = np.array(emb_texto)    
    emb_texto = emb_texto.ravel()
    emb_texto = emb_texto.astype(np.float32)
    # calcular similitud
    similitud = 1 - spatial.distance.cosine(embedding_consulta, emb_texto) 
    similitudes.append((similitud, i))
  
  # Ordenar por similitud descendente
  similitudes.sort(reverse=True)
  
  # Obtener los índices de resultados top
  indices_top = [indice for similitud, indice in similitudes[:n_resultados]]
  
  # Devolver filas correspondientes
  return datos.loc[indices_top]
