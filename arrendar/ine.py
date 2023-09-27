import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image
import pytesseract
import json
import fitz  # PyMuPDF
import os

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

# Crear la ventana principal
root = tk.Tk()
root.title("Extractor de Texto")

# Botón para abrir archivos
open_button = tk.Button(root, text="Abrir archivo", command=open_file)
open_button.pack(pady=10)

# Caja de texto para mostrar el texto extraído
text_box = ScrolledText(root, width=96, height=32)
text_box.pack()

# Iniciar la aplicación
root.mainloop()
