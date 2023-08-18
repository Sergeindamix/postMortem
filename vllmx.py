import streamlit as st
from vllm import LLM

# Crear un LLM y almacenarlo en caché para reutilización
@st.cache_resource
def get_model():
    # Crear una instancia del modelo LLM (lenguaje generativo de lenguaje natural)
    llm = LLM(model="gpt2")
    return llm

# Obtener el modelo (o cargar desde caché si ya existe)
model = get_model()

def main():
    # Título de la aplicación
    st.title("LLM Text Generator")
    
    # Cuadro de texto para ingresar frases de inicio (prompts)
    prompts = st.text_area("Ingrese las frases de inicio (una por línea):")
    prompts = prompts.split("\n") if prompts else []

    # Botón para generar textos
    if st.button("Generar Textos"):
        if prompts:
            # Generar textos para cada prompt utilizando el modelo LLM
            outputs = model.generate(prompts)
            st.subheader("Resultados:")
            for i, output in enumerate(outputs):
                generated_text = output.outputs[0].text
                st.write(f"Resultado {i + 1}: {generated_text}")
        else:
            st.warning("Por favor, ingrese al menos un prompt.")

if __name__ == "__main__":
    main()
