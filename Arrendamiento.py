import streamlit as st
import re
from datetime import datetime

def fill_contract_template(contract_text, fill_values):
    for placeholder, value in fill_values.items():
        contract_text = contract_text.replace(placeholder, value)
    return contract_text

def main():
    st.title("Generador de Contrato de Arrendamiento")

    # Contrato de arrendamiento con campos de relleno
    contract_template = """
    CONTRATO DE ARRENDAMIENTO PARA EL EDO. DE MEXICO PARA CASA HABITACION O NEGOCIO 

    ... (resto del contrato) ...
    
    EN EL ESTADO DE MEXICO, A: {FECHA}

    FIRMAS:

    _______________________           ___________________________
    El arrendador                    El arrendatario
    """

    # Mostrar el contrato con campos de relleno
    st.subheader("Contrato de Arrendamiento:")
    st.text(contract_template)

    # Campos de relleno
    fill_values = {
        "{arrendador}": st.text_input("Nombre del arrendador:"),
        "{arrendatario}": st.text_input("Nombre del arrendatario:"),
        "{cantidad}": st.text_input("Cantidad de renta:"),
        "{fechaInicio}": st.text_input("Fecha de inicio:"),
        "{fechaFinal}": st.text_input("Fecha de finalización:")
        # Agregar más campos aquí
    }

    # Obtener la fecha actual
    current_date = datetime.now().strftime("%d/%m/%Y")
    fill_values["{FECHA}"] = current_date

    if all(value for value in fill_values.values()):
        filled_contract = fill_contract_template(contract_template, fill_values)
        st.subheader("Contrato de Arrendamiento Rellenado:")
        st.text(filled_contract)

if __name__ == "__main__":
    main()
