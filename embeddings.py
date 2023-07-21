import pandas as pd
from transformers import BertModel, BertTokenizer
import torch

def embed_text(path="texto.csv"):

  df = pd.read_csv(path)
  
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

  df.to_csv('embeddings.csv', index=False)
  
  return df
