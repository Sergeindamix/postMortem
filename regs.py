from flask import Flask, render_template, request, redirect
from pyngrok import ngrok

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener los datos del formulario
        # y guardarlos en una base de datos o archivo
        
        # Redireccionar a una página de éxito o inicio
        return redirect('/success')

    return render_template('regDocs.html')

@app.route('/success')
def success():
    return "¡La información ha sido guardada con éxito!"

# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url
print('Public URL:', public_url)

if __name__ == '__main__':
    app.run()
