from pdf_utils import convert_pdf_to_images  # Asume que tienes esta función en un archivo llamado "convert_pdf_to_images.py"

import streamlit as st
from PIL import Image
from io import BytesIO
import tempfile
import os

def main():
    st.title("Visualización de Imágenes desde PDF en Streamlit")

    uploaded_file = st.file_uploader("Sube un PDF", type=["pdf"])
    if uploaded_file is not None:
        # Crear un archivo temporal para el PDF cargado
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())

        images = convert_pdf_to_images(temp_file.name)

        for i, image_data in enumerate(images):
            image_byte_array = image_data[i]
            image = Image.open(BytesIO(image_byte_array))
            st.image(image, caption=f"Página {i+1}", use_column_width=True)

        # Cerrar y eliminar el archivo temporal
        temp_file.close()
        os.unlink(temp_file.name)

if __name__ == "__main__":
    main()

