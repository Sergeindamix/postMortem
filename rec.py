import os
from flask import Flask, render_template, request, redirect
from pyngrok import ngrok
from datetime import datetime

# Ruta del directorio "static/recordings"
directorio = "static/recordings"

# Verificar si el directorio existe
if not os.path.exists(directorio):
    # Crear el directorio si no existe
    os.makedirs(directorio)
    
app = Flask(__name__)

# Ruta de inicio
@app.route('/')
def index():
    # Obtener la lista de archivos de audio existentes
    files = os.listdir('static/recordings')
    return render_template('index.html', files=files)

# Ruta para grabar un nuevo mensaje de audio
@app.route('/record', methods=['POST'])
def record():
    # Obtener el archivo de audio grabado desde el formulario
    audio = request.files['audio']

    # Generar un nombre de archivo único utilizando la fecha y hora actual
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'recording_{timestamp}.wav'

    # Guardar el archivo de audio en la carpeta de grabaciones
    audio.save(os.path.join('static/recordings', filename))

    # Redireccionar al inicio después de la grabación
    return redirect('/')

# Ruta para eliminar un archivo de audio
@app.route('/delete/<filename>')
def delete(filename):
    # Eliminar el archivo de audio de la carpeta de grabaciones
    os.remove(os.path.join('static/recordings', filename))

    # Redireccionar al inicio después de eliminar el archivo
    return redirect('/')




if __name__ == '__main__':
    app.run()
