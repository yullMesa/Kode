import os
import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Definimos las rutas exactas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, "uploads")
IMG_DIR = os.path.join(UPLOAD_PATH, "imagenes")
TEXT_DIR = os.path.join(UPLOAD_PATH, "textos")
JSON_FILE = os.path.join(UPLOAD_PATH, "data.json")
app.mount("/ver-foto", StaticFiles(directory=IMG_DIR), name="imagenes")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que cualquier origen (como tu Live Server) se conecte
    allow_credentials=True,
    allow_methods=["*"], # Permite POST, GET, etc.
    allow_headers=["*"], # Permite todos los encabezados
)

# Creamos las carpetas si no existen (Seguridad extra)
for folder in [IMG_DIR, TEXT_DIR]:
    os.makedirs(folder, exist_ok=True)

@app.post("/upload")
async def upload_story(file: UploadFile = File(...), text: str = Form(...)):
    try:
        # 1. Guardar Imagen físicamente
        nombre_limpio = file.filename.replace(" ", "_") # Evitamos errores de espacios
        img_path = os.path.join(IMG_DIR, nombre_limpio)
        
        with open(img_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 2. Guardar el Texto en su propio archivo .txt
        txt_filename = f"{os.path.splitext(nombre_limpio)[0]}.txt"
        txt_path = os.path.join(TEXT_DIR, txt_filename)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(str(text))
            f.flush()  # Empuja el texto al disco
            os.fsync(f.fileno()) # Asegura que el sistema operativo escriba el archivo

        # 3. Actualizar el JSON como índice
        datos = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                try:
                    datos = json.load(f)
                except: datos = []

        nuevo_item = {
            "id": len(datos) + 1,
            "img": nombre_limpio,
            "txt_ref": txt_filename,
            "revisado": False
        }
        datos.append(nuevo_item)

        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        return {"status": "ok", "message": "Todo guardado perfectamente"}
    
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    

@app.get("/historias")
async def get_stories():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
                # Solo enviamos las historias donde revisado == True
                historias_publicas = [h for h in datos if h.get("revisado") == True]
                return historias_publicas
            except:
                return []
    return []


@app.get("/leer-texto/{filename}")
async def leer_texto(filename: str):
    txt_path = os.path.join(TEXT_DIR, filename)
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            contenido = f.read()
        return {"texto": contenido}
    return {"error": "Archivo no encontrado"}, 404