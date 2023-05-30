from flask import Flask, render_template, request
from pyngrok import ngrok
import json
import os

# Verificar si el archivo JSON existe
if not os.path.isfile('beneficiarios.json'):
    # Crear una lista vacía si el archivo no existe
    with open('beneficiarios.json', 'w') as file:
        json.dump([], file)

# Cargar los datos existentes del archivo JSON
with open('beneficiarios.json', 'r') as file:
    beneficiarios = json.load(file)

app = Flask(__name__)

# Ruta de inicio
@app.route('/')
def index():
    return render_template('formulario.html')

# Ruta para procesar el formulario
@app.route('/registrar', methods=['POST'])
def registrar():
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    relacion = request.form['relacion']
    # Aquí puedes realizar las acciones necesarias para guardar los datos en una base de datos o en otro lugar
    nuevo_beneficiario = {
        'nombre': nombre,
        'apellido': apellido,
        'relacion': relacion
    }

    # Verificar si el beneficiario ya existe en la lista
    existe = False
    for beneficiario in beneficiarios:
        if beneficiario['nombre'] == nombre and beneficiario['apellido'] == apellido:
            existe = True
            break

    # Agregar el nuevo beneficiario a la lista solo si no existe
    if not existe:
        beneficiarios.append(nuevo_beneficiario)
        print('El beneficiario ha sido agregado correctamente.')
    else:
        print('El beneficiario ya existe en la lista.')

    # Guardar la lista actualizada en el archivo JSON
    with open('beneficiarios.json', 'w') as file:
        json.dump(beneficiarios, file, indent=4)
    # Redireccionar a una página de confirmación o agradecimiento
    return render_template('confirmacion.html', nombre=nombre)


# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url
print('Public URL:', public_url)

if __name__ == '__main__':
    app.run()
