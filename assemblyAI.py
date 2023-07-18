import streamlit as st 
import json 
import os 
import time
import requests
import assemblyai as aai
from moviepy.editor import *
from pytube import YouTube
from pathlib import Path
from transformers.tools import HfAgent

agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")


aai.settings.api_key = "ea6b2c6813224320a800cd47529d3bc6"
transcriber = aai.Transcriber()

aai.settings.api_key = "ea6b2c6813224320a800cd47529d3bc6"
api_token = "ea6b2c6813224320a800cd47529d3bc6"

base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "ea6b2c6813224320a800cd47529d3bc6"
}

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


# Assembly AI speech to text
def assemblyai_stt(audio_filename):
    with open(audio_filename, "rb") as f:
        response = requests.post(
            base_url + "/transcript",
            headers=headers,
            files={"audio": f}
        )

    transcript = transcriber.transcribe(audio_filename)
    st.write(transcript.text) 
    return transcript

    

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
        query = st.text_area("Ask your Query here...")
        if query is not None:
            if st.button("Ask"):
                st.info("Your Query is: " + query)
                transcription_text = assemblyai_stt(audio_filename)
                st.info("Transcription:")
                st.write(transcription_text)
                
                response = agent.run(query)

                
                # Mostrar la respuesta en la interfaz de Streamlit
                st.write(response)

