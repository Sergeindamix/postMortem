import streamlit as st
import os
import requests
import assemblyai as aai
from moviepy.editor import *
from pytube import YouTube
from pathlib import Path
from transformers.tools import HfAgent

# Configurar el agente de Hugging Face
agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")

# Configurar AssemblyAI
aai.settings.api_key = "ea6b2c6813224320a800cd47529d3bc6"
transcriber = aai.Transcriber()

base_url = "https://api.assemblyai.com/v2"
headers = {"authorization": "ea6b2c6813224320a800cd47529d3bc6"}

def save_audio(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    file_name = base + '.mp3'
    try:
        os.rename(out_file, file_name)
    except WindowsError:
        os.remove(file_name)
        os.rename(out_file, file_name)
    audio_filename = Path(file_name).stem+'.mp3'
    return audio_filename

#Streamlit Code
st.set_page_config(layout="wide", page_title="ChatAudio", page_icon="🔊")

st.title("Chat with Your Audio using LLM")

input_source = st.text_input("Enter the YouTube video URL", "https://youtu.be/B_D3dCSylCg")

if input_source is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.info("Your uploaded video")
        st.video(input_source)
        audio_filename = save_audio(input_source)
    
    with col2:
        st.info("Chat Below")
        transcript = transcriber.transcribe(audio_filename)
        st.write(transcript.text)
        query = st.text_area("Ask your Query here...", f"summarize the content of: {input_source}")
        
        if query is not None:
            if st.button("Ask"):
                st.info("Your Query is: " + query)
                
                # Ejecutar la consulta con el agente de Hugging Face
                response = agent.run(query)
                
                # Mostrar la respuesta en la interfaz de Streamlit
                st.write(response)
