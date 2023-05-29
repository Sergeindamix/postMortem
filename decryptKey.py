from cryptography.fernet import Fernet

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

print('Contenido desencriptado:')
print(contenido_texto)
