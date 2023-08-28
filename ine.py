import streamlit as st
from PIL import Image
from io import BytesIO

import pytesseract
from pytesseract import image_to_string

def extract_text_from_img(image_list):
    image_content = []

    for image_bytes in image_list:
        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)

def generate_lease_agreement(arrendador_name, arrendador_address, inquilino_name, inquilino_address, lease_term):
    # Definir la plantilla del contrato de arrendamiento
    lease_agreement = f"""CONTRATO DE ARRENDAMIENTO
    
    Yo, {arrendador_name}, con domicilio en {arrendador_address}, en adelante llamado "El Arrendador", y el Sr./Sra. {inquilino_name}, con domicilio en {inquilino_address}, en adelante llamado "El Inquilino", celebramos el presente Contrato de Arrendamiento bajo las siguientes cláusulas:
    
    CLÁUSULA 1: OBJETO
    El Arrendador arrienda al Inquilino la propiedad ubicada en [Dirección de la Propiedad], por un período de {lease_term} meses, comenzando el [Fecha de Inicio].
    
    CLÁUSULA 2: RENTA
    El Inquilino se compromete a pagar una renta mensual de [Monto de la Renta] en las primeras [Día del Mes] de cada mes.
    
    ...
    
    CLÁUSULA N: [Otras cláusulas]
    
    FIRMAS:
    
    ____________________________            ____________________________
    El Arrendador                                       El Inquilino
    """
    return lease_agreement

def extract_name_and_address(text):
    paragraphs = text.split('\n\n')
    uppercase_paragraphs = [p for p in paragraphs if p.isupper()]
    if len(uppercase_paragraphs) < 2:
        return None, None
    
    name = uppercase_paragraphs[0]
    address = uppercase_paragraphs[1]
    
    return name.strip(), address.strip()

def main():
    st.title("Generador de Contrato de Arrendamiento")

    arrendador_name = st.text_input("Nombre del Arrendador:")
    arrendador_address = st.text_input("Dirección del Arrendador:")
    
    uploaded_file = st.file_uploader("Sube un PDF o una imagen", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            pass
        else:
            image = Image.open(uploaded_file)
            text = image_to_string(image)
            
            st.subheader("Texto Extraído de la Imagen:")
            st.text(text)
            
            # Extracción de nombre y domicilio del inquilino
            inquilino_name, inquilino_address = extract_name_and_address(text)
            start_index_name = text.find("NOMBRE") + len("NOMBRE")
            end_index_name = text.find("DOMICILIO")
            inquilino_name = text[start_index_name:end_index_name].strip()
            
            if inquilino_name and inquilino_address:
                st.subheader("Datos del Inquilino:")
                st.text(f"Nombre: {inquilino_name}")
                st.text(f"Domicilio: {inquilino_address}")
                
                # Autollenado de contrato de arrendamiento
                lease_term = st.number_input("Plazo de Arrendamiento (meses):", value=12)
                
                if lease_term:
                    lease_agreement = generate_lease_agreement(arrendador_name, arrendador_address, inquilino_name, inquilino_address, lease_term)
                    st.subheader("Contrato de Arrendamiento:")
                    st.text(lease_agreement)

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Ruta al ejecutable de Tesseract en tu sistema
    main()
