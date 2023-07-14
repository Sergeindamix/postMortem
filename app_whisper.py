import numpy as np
from flask import Flask, render_template, request
from scipy.io.wavfile import write
from IPython.display import clear_output
import whisper



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    Tarea = "Transcript to Language"  # Cambia esto según tus necesidades

    # Obtener audio grabado y guardarlo en un archivo
    audio = request.files.get("audio")
    audio.save("record.mp3")

    # Determinar la tarea de transcripción o traducción
    task = "translate" if Tarea == "Translate to English" else "transcribe"

    # Ejecutar el comando whisper para transcribir o traducir el archivo de audio
    model = whisper.load_model("base")
    result = model.transcribe("record.mp3")
    print(result["text"])
    
    clear_output()

    if task == "translate":
        print("-- TRADUCCIÓN A INGLÉS --\n")
    else:
        print("-- TRANSCRIPCIÓN A ESPAÑOL --\n")

    # Leer el archivo de texto resultante
    transcript = open('record.txt').read()

    return {"result": "ok", "text": result["text"]}
