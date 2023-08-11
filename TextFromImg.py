from pdf_utils import convert_pdf_to_images  # Asume que tienes esta función en un archivo llamado "convert_pdf_to_images.py"
import streamlit as st
from PIL import Image
from io import BytesIO
import tempfile
import os

import pytesseract
from pytesseract import image_to_string

def extract_text_from_img(list_dict_final_images):
    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []

    for index, image_bytes in enumerate(image_list):
        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)

def main():
    st.title("Extracción de Texto desde Imágenes en Streamlit")

    uploaded_file = st.file_uploader("Sube un PDF", type=["pdf"])
    if uploaded_file is not None:
        # Crear un archivo temporal para el PDF cargado
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())

        images = convert_pdf_to_images(temp_file.name)
        text = extract_text_from_img(images)
        
        st.subheader("Texto Extraído de las Imágenes:")
        st.text(text)

        # Cerrar y eliminar el archivo temporal
        temp_file.close()
        os.unlink(temp_file.name)

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Ruta al ejecutable de Tesseract en tu sistema
    main()

