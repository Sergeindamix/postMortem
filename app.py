import os
import streamlit as st
import json
from datetime import datetime
import docx
from cryptography.fernet import Fernet

# Título de la aplicación
#st.title('Formulario de Información Personal')

# Barra lateral para seleccionar el módulo de Python
selected_module = st.sidebar.selectbox('Seleccionar módulo de Python', ['Formulario', 'Módulo 1', 'Módulo 2', 'Módulo 3', 'Módulo 4'])

# Módulo de Formulario
if selected_module == 'Formulario':
    # Sección de Contactos de Emergencia
    st.header('Contactos de Emergencia')

    # Formulario de Contactos de Emergencia
    emergency_contact1_name = st.text_input('Nombre del Contacto 1:')
    emergency_contact1_phone = st.text_input('Teléfono del Contacto 1:')
    emergency_contact2_name = st.text_input('Nombre del Contacto 2:')
    emergency_contact2_phone = st.text_input('Teléfono del Contacto 2:')

    # Sección de Detalles de Seguros
    st.header('Detalles de Seguros')

    # Formulario de Detalles de Seguros
    insurance_company = st.text_input('Compañía de Seguros:')
    insurance_policy_number = st.text_input('Número de Póliza:')

    # Sección de Información Médica Relevante
    st.header('Información Médica Relevante')

    # Formulario de Información Médica Relevante
    blood_type = st.text_input('Tipo de Sangre:')
    allergies = st.text_input('Alergias:')
    medications = st.text_input('Medicamentos:')

    # Sección de Cuentas en Línea y Contraseñas
    st.header('Cuentas en Línea y Contraseñas')

    # Formulario de Cuentas en Línea y Contraseñas
    online_account1 = st.text_input('Cuenta en Línea 1:')
    online_account1_password = st.text_input('Contraseña de la Cuenta 1:', type='password')
    online_account2 = st.text_input('Cuenta en Línea 2:')
    online_account2_password = st.text_input('Contraseña de la Cuenta 2:', type='password')

    # Botón para mostrar y guardar los datos
    if st.button('Mostrar y Guardar Datos'):
        # Crear un diccionario con los datos
        datos = {
            'emergencyContact1': {
                'nombre': emergency_contact1_name,
                'telefono': emergency_contact1_phone
            },
            'emergencyContact2': {
                'nombre': emergency_contact2_name,
                'telefono': emergency_contact2_phone
            },
            'insuranceDetails': {
                'compania': insurance_company,
                'numeroPoliza': insurance_policy_number
            },
            'medicalInfo': {
                'tipoSangre': blood_type,
                'alergias': allergies,
                'medicamentos': medications
            },
            'onlineAccounts': {
                'cuenta1': {
                    'cuenta': online_account1,
                    'contrasena': online_account1_password
                },
                'cuenta2': {
                    'cuenta': online_account2,
                    'contrasena': online_account2_password
                }
            }
        }

        # Mostrar los datos en el navegador
        st.json(datos)

        # Guardar los datos en un archivo JSON
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'datos_{timestamp}.json'
        with open(filename, 'w') as file:
            json.dump(datos, file, indent=4)
        st.success(f'Los datos han sido guardados en el archivo {filename}')

# Módulo 1
elif selected_module == 'Módulo 1':
    st.header('Beneficiarios')

    # Verificar si el archivo JSON existe
    if not os.path.isfile('beneficiarios.json'):
        # Crear una lista vacía si el archivo no existe
        with open('beneficiarios.json', 'w') as file:
            json.dump([], file)

    # Cargar los datos existentes del archivo JSON
    with open('beneficiarios.json', 'r') as file:
        beneficiarios = json.load(file)

    # Ruta de inicio
    def index():
        st.title('Formulario de Registro')
        nombre = st.text_input('Nombre')
        apellido = st.text_input('Apellido')
        relacion = st.text_input('Relación')
        if st.button('Registrar'):
            registrar(nombre, apellido, relacion)

    # Función para procesar el formulario
    def registrar(nombre, apellido, relacion):
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
            st.success('El beneficiario ha sido agregado correctamente.')
        else:
            st.warning('El beneficiario ya existe en la lista.')

        # Guardar la lista actualizada en el archivo JSON
        with open('beneficiarios.json', 'w') as file:
            json.dump(beneficiarios, file, indent=4)
        # Mostrar mensaje de confirmación
        st.write(f'¡Gracias {nombre} por registrarte!')

    # Llamar a la función de inicio
    index()

# Módulo 2
elif selected_module == 'Módulo 2':
    st.header('Grabaciones')

    # Ruta del directorio "static/recordings"
    directorio = "static/recordings"

    # Verificar si el directorio existe
    if not os.path.exists(directorio):
        # Crear el directorio si no existe
        os.makedirs(directorio)

    # Título de la aplicación
    st.title('Mensajes y Deseos Personales')

    # Variables de control para la grabación de audio
    recording = False
    chunks = []

    # Función para reproducir el archivo de audio seleccionado
    def play_audio(filename):
        st.audio(f'static/recordings/{filename}')

    # Función para grabar el mensaje de audio
    def record_audio():
        global recording, chunks
        recording = True
        chunks = []
        st.warning('Grabando mensaje...')
        st.info('Haz clic en "Detener" cuando hayas terminado.')

    # Función para detener la grabación de audio
    def stop_recording():
        global recording, chunks
        recording = False
        st.success('Mensaje grabado exitosamente!')

        # Lógica para guardar el mensaje de audio aquí

    # Botón para grabar un nuevo mensaje de audio
    if not recording:
        if st.button('Grabar nuevo mensaje'):
            record_audio()
    else:
        if st.button('Detener'):
            stop_recording()

    # Lista de mensajes grabados
    st.header('Mensajes Grabados')
    files = os.listdir('static/recordings')
    for file in files:
        st.write(file)
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Reproducir'):
                play_audio(file)
        with col2:
            if st.button('Borrar'):
                os.remove(os.path.join('static/recordings', file))
                st.success(f'El archivo "{file}" ha sido borrado.')

# Módulo 3
elif selected_module == 'Módulo 3':
    st.header('Encriptar')

    # Título de la aplicación
    st.title('Encriptador de Archivos DOCX')

    # Cargar archivo DOCX
    uploaded_file = st.file_uploader('Cargar archivo DOCX', type=['docx'])
    if uploaded_file:
        # Leer el contenido del archivo DOCX
        doc = docx.Document(uploaded_file)
        contenido = '\n'.join([p.text for p in doc.paragraphs])

        # Generar una clave de encriptación
        clave = Fernet.generate_key()

        # Guardar la clave en un archivo
        archivo_clave = 'clave.key'
        with open(archivo_clave, 'wb') as file:
            file.write(clave)

        # Encriptar el contenido del archivo
        cipher_suite = Fernet(clave)
        contenido_encriptado = cipher_suite.encrypt(contenido.encode())

        # Guardar el contenido encriptado en un nuevo archivo
        archivo_encriptado = 'archivo_encriptado.txt'
        with open(archivo_encriptado, 'wb') as file:
            file.write(contenido_encriptado)

        # Mostrar el resultado en la interfaz
        st.header('Resultado de Encriptación')
        st.markdown('**Clave Generada:**')
        st.code(clave.decode(), language='text')
        st.markdown('**Contenido Encriptado:**')
        st.code(contenido_encriptado.decode(), language='text')

# Módulo 4
elif selected_module == 'Módulo 4':
    st.header('Desencriptar')

    # Título de la aplicación
    st.title('Desencriptador de Archivos DOCX')

    # Ruta del archivo encriptado
    archivo_encriptado = 'archivo_encriptado.txt'

    # Leer el contenido encriptado del archivo
    with open(archivo_encriptado, 'rb') as file:
        contenido_encriptado = file.read()

    # Leer la clave de encriptación del archivo
    archivo_clave = 'clave.key'
    with open(archivo_clave, 'rb') as file:
        clave = file.read()

    # Crear el objeto de encriptación
    cipher_suite = Fernet(clave)

    # Desencriptar el contenido
    contenido_desencriptado = cipher_suite.decrypt(contenido_encriptado)

    # Convertir el contenido desencriptado a texto
    contenido_texto = contenido_desencriptado.decode()

    # Mostrar el resultado en la interfaz
    st.header('Resultado de Desencriptación')
    st.markdown('**Clave Utilizada:**')
    st.code(clave.decode(), language='text')
    st.markdown('**Contenido Desencriptado:**')
    st.code(contenido_texto, language='text')
