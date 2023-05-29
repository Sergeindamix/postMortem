import os
import docx
from cryptography.fernet import Fernet

# Ruta del archivo DOCX a subir
archivo_docx = 'file.docx'

# Generar una clave de encriptación
clave = Fernet.generate_key()

# Guardar la clave en un archivo
archivo_clave = 'clave.key'
with open(archivo_clave, 'wb') as file:
    file.write(clave)

print('La clave se ha guardado correctamente en el archivo', archivo_clave)

cipher_suite = Fernet(clave)

# Leer el contenido del archivo DOCX
doc = docx.Document(archivo_docx)
contenido = '\n'.join([p.text for p in doc.paragraphs])

# Encriptar el contenido del archivo
contenido_encriptado = cipher_suite.encrypt(contenido.encode())

# Guardar el contenido encriptado en un nuevo archivo
archivo_encriptado = 'archivo_encriptado.txt'
with open(archivo_encriptado, 'wb') as file:
    file.write(contenido_encriptado)

print('El archivo se ha encriptado correctamente:')
