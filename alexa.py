import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Inicializar el reconocimiento de voz
recognizer = sr.Recognizer()

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

# Configurar voces (opcional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Función para que Alexa responda
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Función para realizar acciones según el comando
def alexa(command):
    if 'reproduce' in command:
        song = command.replace('reproduce', '')
        speak('Reproduciendo ' + song)
        pywhatkit.playonyt(song)
    elif 'hora' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak('La hora actual es ' + time)
    elif 'busca' in command:
        topic = command.replace('busca', '')
        info = wikipedia.summary(topic, sentences=1)
        speak('Encontré esto en Wikipedia: ' + info)
    elif 'chiste' in command:
        joke = pyjokes.get_joke()
        speak(joke)
    else:
        speak('Lo siento, no entendí el comando.')

# Ejecutar el asistente
with sr.Microphone() as source:
    print('Di algo...')
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        print('Reconociendo...')
        command = recognizer.recognize_google(audio, language='es-ES').lower()
        if 'alexa' in command:
                command = command.replace('alexa', '')                
                print('Has dicho:', command)
                alexa(command)

    except sr.UnknownValueError:
        print('No se pudo entender el audio')
    except sr.RequestError as e:
        print('Error al hacer la solicitud a Google Speech Recognition:', e)

