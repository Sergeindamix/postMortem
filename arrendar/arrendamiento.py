import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image
import pytesseract
import json
import fitz  # PyMuPDF
import os
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

# Declarar la variable global nombre_inquilino
nombre_inquilino = ""  # Declarar la variable global nombre_inquilino

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        text = extract_text_from_file(file_path)
        text_box.delete(1.0, tk.END)  # Limpiar el contenido anterior
        text_box.insert(tk.END, text)
        process_text(text, file_path)

def extract_text_from_file(file_path):
    if file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    else:
        return "Formato de archivo no compatible."

def process_text(text, file_path):
    lines = text.split('\n')
    name = None
    clave_elector = None
    for i, line in enumerate(lines):
        if "NOMBRE" in line:
            # Encontramos la palabra "NOMBRE", ahora guardamos los 3 párrafos siguientes como nombre del inquilino
            name = "\n".join(lines[i+1:i+4])
        elif clave_elector is None and "CLAVE DE ELECTOR" in line:
            # Encontramos "CLAVE DE ELECTOR", ahora guardamos el resto del párrafo sin espaciado ni ":"
            clave_elector = line.strip(":").strip()
            if name and clave_elector:
                # Si tenemos tanto el nombre como la clave del elector, guardamos en JSON
                json_filename = extract_filename(file_path) + "_clave_elector.json"
                save_data_to_json(json_filename, {"nombre_inquilino": name.strip(), "clave_elector": clave_elector})

def extract_filename(file_path):
    # Extraer el nombre de archivo sin extensión y sin la ruta
    return os.path.splitext(os.path.basename(file_path))[0]

def clean_filename(filename):
    # Elimina caracteres no permitidos en nombres de archivo
    valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(c if c in valid_chars else '_' for c in filename)

def save_data_to_json(json_filename, data):
    # Limpia el nombre del archivo
    json_filename = clean_filename(json_filename)

    # Guardar los datos en un archivo JSON
    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

def open_file():
    global nombre_inquilino  # Declarar la variable global para acceder a ella
    global file_path  # Declarar la variable global para acceder a ella
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        text = extract_text_from_file(file_path)
        text_box.delete(1.0, tk.END)  # Limpiar el contenido anterior
        text_box.insert(tk.END, text)
        nombre_inquilino = load_nombre_inquilino_from_json(extract_filename(file_path) + "_clave_elector.json")
        process_text(text, file_path)

# Función para cargar el nombre del inquilino desde un archivo JSON
def load_nombre_inquilino_from_json(json_filename):
    try:
        with open(json_filename, "r") as json_file:
            data = json.load(json_file)
            return data.get("nombre_inquilino", "")  # Obtener el nombre del inquilino o cadena vacía si no se encuentra
    except FileNotFoundError:
        return ""  # Si el archivo no existe, retornar cadena vacía

# Función para guardar la información del contrato
def save_contract_info():
    arrendador = arrendador_entry.get()
    cantidad_renta = cantidad_renta_entry.get()
    fecha_inicio_str = fecha_inicio_cal.get()  # Obtener la fecha como cadena
    fecha_finalizacion_str = fecha_finalizacion_cal.get()  # Obtener la fecha como cadena

    # Convertir las cadenas de fecha a objetos datetime con el nuevo formato "día/mes/año"
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%y")
    fecha_finalizacion = datetime.strptime(fecha_finalizacion_str, "%d/%m/%y")

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Aquí puedes guardar la información en un JSON o hacer lo que necesites con ella
    contract_info = {
        "Nombre del arrendador": arrendador,
        "Nombre del arrendatario": nombre_inquilino,  # Recuperar el nombre del inquilino del JSON
        "Cantidad de renta": cantidad_renta,
        "Fecha de inicio": fecha_inicio.strftime("%d/%m/%y"),  # Formatear la fecha de nuevo
        "Fecha de finalización": fecha_finalizacion.strftime("%d/%m/%y"),  # Formatear la fecha de nuevo
        "Fecha actual": fecha_actual.strftime("%d/%m/%Y")  # Formatear la fecha actual
    }

    # Generar el contrato con los datos del JSON
    contrato_text = generar_contrato(contract_info)

    # Mostrar el contrato en la caja de texto
    text_box.delete(1.0, tk.END)  # Limpiar el contenido anterior
    text_box.insert(tk.END, contrato_text)

# ...

def generar_contrato(contract_info):
    contrato_text = f"""CONTRATO DE ARRENDAMIENTO PARA EL EDO. DE MÉXICO PARA CASA HABITACION O NEGOCIO

De acuerdo con lo dispuesto en el Artículo 2560 del Código Civil del Estado de México, celebran el presente contrato de Arrendamiento, el arrendador(a) {contract_info["Nombre del arrendador"]} da en arrendamiento al Sr(a) {contract_info["Nombre del arrendatario"]} la casa ubicada en la calle Primero de Mayo con número 12 y 13, en la colonia Plan de Ayala 2a, C.P. 53710 sujetándose a las siguientes cláusulas:

PRIMERA. - El arrendatario pagará al arrendador o a quien sus derechos represente, la cantidad de ${contract_info["Cantidad de renta"]} ({contract_info["Cantidad de renta"]}) por el arrendamiento mensual de la localidad mencionada arriba, que se cubrirá en moneda del cuño nacional con toda puntualidad al arrendador o de quien sus derechos represente, de acuerdo con lo que previenen los artículos 2279 y 2281.

SEGUNDA.- De acuerdo al artículo 2283 el arrendatario está obligado a pagar la renta que se venza hasta el día que entregue la casa arrendada.

TERCERA.- El inicio del arrendamiento será a partir de la fecha {contract_info["Fecha de inicio"]} y concluirá el {contract_info["Fecha de finalización"]}

CUARTA.- El arrendatario no podrá traspasar o subarrendar la localidad arrendada y en caso de hacerlo será con permiso y por escrito del arrendador.

QUINTA. - Si el arrendatario recibió la finca con expresa descripción de las partes que se compone, debe devolverla, al concluir el arrendamiento, tal como la recibió, salvo lo que hubiese perecido o se hubiere menoscabado por el tiempo por causa inevitable, de acuerdo al Artículo 2296.

SEXTA.- De acuerdo al Artículo 2295, el arrendatario no puede, sin consentimiento expreso del arrendador, variar la forma de la finca, y si lo hace, cuando la devuelva deberá restablecerla, siendo, además responsable de los daños y perjuicios.

SEPTIMA.- El arrendatario hará uso de la casa únicamente para habitación, si infringiere esta cláusula se dará por rescindido dicho contrato.

OCTAVA.-De acuerdo al Artículo 2266, Fracción I, II, III el arrendador está obligado a entregar al arrendatario la finca arrendada con todas sus pertenencias y en estado de servir para el uso convenido; así como las condiciones que ofrezcan al arrendatario la higiene y seguridad del inmueble, así como también, a conservar la casa arrendada en el mismo estado, durante el arrendamiento, haciendo para ello todas las reparaciones necesarias y a no estorbar de manera alguna el uso de la casa arrendada, a no ser por causa de reparaciones urgentes e indispensables.

NOVENA.- El arrendatario deberá cuidar de no tener substancias corrosivas, material inflamable o peligroso y de ser así, deberá observar las leyes que regulen el manejo adecuado de dichas substancias según al Articulo 2294.
DÉCIMA. De acuerdo a lo previsto en el Artículo 2298 el arrendatario debe hacer las reparaciones de aquellos deterioros de poca importancia, que regularmente son causados, por las personas que habitan la finca o estructura.

DÉCIMA PRIMERA.- El arrendador no puede, durante el arrendamiento mudar la forma de la finca ni intervenir en el uso legítimo de ella, por su parte, el arrendatario está obligado a poner el conocimiento del arrendador, a la brevedad posible, la necesidad de las reparaciones, bajo pena de pagar los daños y perjuicios que su omisión cause, si el arrendador no cumpliere con hacer las reparaciones necesarias para el uso que está destinada la finca, quedará a elección del arrendatario rescindir el arrendamiento u ocurrir al juez para que estreche al arrendador para dar cumplimiento de su obligación, Articulo 2268, 22'79 y 2299.

DÉCIMA SEGUNDA.- Para garantizar el cumplimiento de este contrato entrega el arrendatario la cantidad de: $ {contract_info["Cantidad de renta"]} ({contract_info["Cantidad de renta"]}) la cual se devolverá cuando desocupe la localidad siempre que no deba nada por renta, según constancia por escrito del arrendador.

DÉCIMA TERCERA.- Para garantizar el cumplimiento de este contrato firma como aval el Sr. (a)  N/A
Y señala como su domicilio la calle N/A
Colonia N/A
 C.P.N/A
Ciudad  N/A
Tel. N/A
la cual se identifica con credencial de: N/A
 con Folio No. N/A

DÉCIMA CUARTA.- Ambas partes establecen que el presente contrato de arrendamiento concluya el día prefijado y cuando este no sea por tiempo determinado, cada una de las partes lo dará por terminado previo aviso con quince días de anticipación.

DÉCIMA QUINTA.- En caso de alguna controversia ambas partes se apegan al Código Civil vigente en el Edo. de México.
 Las parte contratantes, perfectamente enteradas del contenido y alcance de todas y cada una de las cláusulas anteriores, firman el presente contrato y están conformes en que el presente contrato empiece a regir.

EN EL ESTADO DE MEXICO, A: {contract_info["Fecha actual"]}

FIRMAS:

_______________________                                   ___________________________
El arrendador                                                           El arrendatario
"""

    return contrato_text

# ...



# Crear la ventana principal
root = tk.Tk()
root.title("Extractor de Texto y Generador de Contratos")

# Botón para abrir archivos
open_button = tk.Button(root, text="Abrir archivo", command=open_file)
open_button.pack(pady=10)

# Caja de texto para mostrar el texto extraído
text_box = ScrolledText(root, width=96, height=32)
text_box.pack()

# Campo de entrada para el nombre del arrendador
arrendador_label = tk.Label(root, text="Nombre del arrendador:")
arrendador_label.pack()
arrendador_entry = tk.Entry(root)
arrendador_entry.pack()

# Campo de entrada para la cantidad de renta
cantidad_renta_label = tk.Label(root, text="Cantidad de renta:")
cantidad_renta_label.pack()
cantidad_renta_entry = tk.Entry(root)
cantidad_renta_entry.pack()

# Calendario para seleccionar la fecha de inicio
fecha_inicio_label = tk.Label(root, text="Fecha de inicio:")
fecha_inicio_label.pack()
fecha_inicio_cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
fecha_inicio_cal.pack()

# Calendario para seleccionar la fecha de finalización
fecha_finalizacion_label = tk.Label(root, text="Fecha de finalización:")
fecha_finalizacion_label.pack()
fecha_finalizacion_cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
fecha_finalizacion_cal.pack()

# Botón para guardar la información del contrato
save_button = tk.Button(root, text="Guardar Contrato", command=save_contract_info)
save_button.pack(pady=10)

# Iniciar la aplicación
root.mainloop()
