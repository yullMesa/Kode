from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import json

app = FastAPI()

# Permitir que el Frontend se comunique con el Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de carpetas
UPLOAD_DIR = "uploads"
folders = ["metadata", "nombres_png", "personajes", "historias_txt"]

for folder in folders:
    os.makedirs(os.path.join(UPLOAD_DIR, folder), exist_ok=True)

@app.post("/publicar-historia")
async def publicar_historia(
    nombre_img: UploadFile = File(...),
    bg_color: str = Form(...),
    personaje_img: UploadFile = File(...),
    historia: str = Form(...)
):
    # Usamos un ID o el nombre del archivo para vincular todo
    file_id = nombre_img.filename.split('.')[0]

    # 1. Guardar Imagen del Nombre
    path_nombre = f"{UPLOAD_DIR}/nombres_png/{nombre_img.filename}"
    with open(path_nombre, "wb") as buffer:
        shutil.copyfileobj(nombre_img.file, buffer)

    # 2. Guardar Imagen del Personaje
    path_personaje = f"{UPLOAD_DIR}/personajes/{personaje_img.filename}"
    with open(path_personaje, "wb") as buffer:
        shutil.copyfileobj(personaje_img.file, buffer)

    # 3. Guardar Historia en Texto Plano (.txt)
    path_txt = f"{UPLOAD_DIR}/historias_txt/{file_id}.txt"
    with open(path_txt, "w", encoding="utf-8") as f:
        f.write(historia)

    # 4. Guardar JSON con toda la info (Metadata)
    datos = {
        "id": file_id,
        "color_fondo": bg_color,
        "archivo_nombre": nombre_img.filename,
        "archivo_personaje": personaje_img.filename,
        "historia_path": path_txt
    }
    
    path_json = f"{UPLOAD_DIR}/metadata/{file_id}.json"
    with open(path_json, "w") as jf:
        json.dump(datos, jf, indent=4)

    return {"status": "success", "message": "¡Todo guardado en sus carpetas!"}