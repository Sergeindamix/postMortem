import streamlit as st
from transformers.tools import HfAgent
    
agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")

st.title("Image Generation") 

prompt = st.text_input("Enter prompt:")

def create_image_module():
    from PIL import Image
    from sd import sd
    st.header("Crear imagen")
    # Agrega aquí el código para crear la imagen
    sd(prompt)

if prompt:
  create_image_module()

  full_prompt = "Generate an image of " + prompt
  image = agent.run(full_prompt)
  if image is None:
    st.error("No se pudo generar la imagen")
  else:
    st.image(image)  

  col1, col2 = st.columns(2)

  with col1:
    st.write("Prompt:")
    st.write(full_prompt)

  with col2:      
    
  
    # Mostrar caption
    st.write("Caption:")
