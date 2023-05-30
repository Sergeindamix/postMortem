import os
from flask import Flask, render_template, request, redirect

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

    # Guardar el archivo de audio en la carpeta de grabaciones
    audio.save(os.path.join('static/recordings', audio.filename))

    # Redireccionar al inicio después de la grabación
    return redirect('/')

# Ruta para eliminar un archivo de audio
@app.route('/delete/<filename>')
def delete(filename):
    # Eliminar el archivo de audio de la carpeta de grabaciones
    os.remove(os.path.join('static/recordings', filename))

    # Redireccionar al inicio después de eliminar el archivo
    return redirect('/')

!ngrok config add-authtoken 2PvAm0udpW3DJmtEimTfGfsWe24_4tLCLKofoNNPk28rrT72F
# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url
print('Public URL:', public_url)

if __name__ == '__main__':
    app.run()
