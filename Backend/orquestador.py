from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.post("/publicar-historia")
async def crear_historia(
    nombre_img: UploadFile = File(...),
    bg_color: str = Form(...),
    personaje_img: UploadFile = File(...),
    historia: str = Form(...)
):
    # Aquí guardarías los archivos en una carpeta y la info en base de datos
    return {"status": "recibido", "personaje": nombre_img.filename}