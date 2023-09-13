import streamlit as st
import os

# Campo de entrada de texto para la carpeta de videos
video_folder = st.text_input("Ruta de la carpeta de videos", "/content/drive/MyDrive/01/movies/")

# Obtener la lista de archivos de video en la carpeta
video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]

# Verificar si hay videos en la carpeta
if len(video_files) == 0:
    st.write("No se encontraron videos en la carpeta.")
else:
    # Crear una lista desplegable para seleccionar un video
    selected_video = st.selectbox("Selecciona un video", ["Selecciona un video"] + video_files)

    # Mostrar el video seleccionado si no es el valor predeterminado
    if selected_video != "Selecciona un video":
        video_path = os.path.join(video_folder, selected_video)
        st.video(video_path)
