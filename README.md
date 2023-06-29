# postMortem
 How to:
 
git clone https://github.com/Sergeindamix/postMortem

cd postMortem

pip install -r requirements.txt

ngrok config add-authtoken API-KEY

Name_extension = "regs.py" #@param [ "None", "0app.py", "decryptKey.py", "encryptKey.py", "record.py", "regs.py"]

if Name_extension != "None":
    try:
        exec(open(Name_extension).read())
    except FileNotFoundError:
        print("El archivo especificado no existe.")
else:
    print("No se seleccionó ningún archivo para ejecutar.")

