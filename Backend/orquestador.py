import os
import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3


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


@app.get("/api/metricas-totales")
async def get_metricas_totales():
    try:
        # Conectamos directo a tu DB relacional
        # Ajusta la ruta si tu archivo python está en otra subcarpeta
        conn = sqlite3.connect(os.path.join(BASE_DIR, "..", "kode.db"))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Traemos todas las historias con su estado analítico real
        cursor.execute("SELECT id, titulo, es_buena FROM historias")
        rows = cursor.fetchall()
        conn.close()
        
        # Retornamos la lista completa de la DB sin depender de ningún JSON
        return [dict(row) for row in rows]
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
@app.get("/api/metricas-detalle")
async def get_metricas_detalle():
    try:
        conn = sqlite3.connect(os.path.join(BASE_DIR, "..", "kode.db"))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Traemos la información financiera para graficar
        # Usamos COALESCE para tomar 'precio_cierre' o en su defecto el 'valor' antiguo si existe
        cursor.execute("""
            SELECT historia_id, 
                   COALESCE(precio_cierre, valor) as cifra_financiera 
            FROM metricas 
            WHERE cifra_financiera IS NOT NULL
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    

@app.get("/api/palabras-repetidas")
def obtener_palabras_repetidas():
    import sqlite3
    import os
    
    # Apuntamos a la DB central en la raíz
    base_dir = os.path.dirname(__file__)
    db_path = os.path.abspath(os.path.join(base_dir, "..", "kode.db"))
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Agrupamos por palabra, sumamos sus frecuencias y limitamos a las 10 más dominantes
    cursor.execute('''
        SELECT palabra, SUM(frecuencia) as total 
        FROM analisis_palabras 
        GROUP BY palabra 
        ORDER BY total DESC 
        LIMIT 10
    ''')
    
    datos = cursor.fetchall()
    conn.close()
    
    # Formateamos la respuesta para que el Frontend la entienda directo
    return [{"palabra": fila[0], "frecuencia": fila[1]} for fila in datos]