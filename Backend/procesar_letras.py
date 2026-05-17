import sqlite3
import os
import re
from collections import Counter

# Palabras ultra comunes que filtramos para que la gráfica muestre palabras clave reales
STOP_WORDS = {'DE', 'LA', 'EL', 'EN', 'Y', 'A', 'LOS', 'QUE', 'UN', 'UNA', 'CON', 'POR', 'PARA', 'DEL', 'LAS', 'O', 'E', 'SU', 'SUS'}

def limpiar_y_tokenizar(texto):
    texto = texto.upper()
    # Extraemos solo palabras alfanuméricas limpias
    palabras = re.findall(r'\b\w+\b', texto)
    return [p for p in palabras if p not in STOP_WORDS and not p.isdigit()]

def procesar_directorio_historias():
    # 📌 Aseguramos las rutas exactas según tu árbol de VS Code
    base_dir = os.path.dirname(__file__)  # Carpeta Backend/
    db_path = os.path.abspath(os.path.join(base_dir, "..", "kode.db"))  # Raíz/kode.db
    carpeta_textos = os.path.join(base_dir, "uploads", "textos")  # Backend/uploads/textos/
    
    if not os.path.exists(db_path):
        print(f"❌ Error crítico: No se encontró la DB central en {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Traemos las historias registradas en la tabla
    cursor.execute("SELECT id FROM historias")
    historias_en_db = [row[0] for row in cursor.fetchall()]
    
    print(f"Iniciando escaneo analítico sobre las historias guardadas...")
    
    contador_procesadas = 0

    for historia_id in historias_en_db:
        ruta_archivo = os.path.join(carpeta_textos, historia_id)
        
        # 📌 Si el archivo NO existe físicamente en 'uploads/textos' (ej. los reportes automáticos de Yfinance),
        # simplemente lo saltamos en silencio sin generar alertas molestas.
        if not os.path.exists(ruta_archivo):
            continue
            
        # Si el archivo sí existe en tu carpeta de textos, lo procesamos con toda la lógica
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        palabras_limpias = limpiar_y_tokenizar(contenido)
        conteo = Counter(palabras_limpias)
        
        try:
            # Limpiamos registros anteriores de esta historia para evitar duplicados al re-correrlo
            cursor.execute("DELETE FROM analisis_palabras WHERE historia_id = ?", (historia_id,))
            
            # Insertamos palabra por palabra heredando el FK (historia_id)
            for palabra, frecuencia in conteo.most_common():
                cursor.execute('''
                    INSERT INTO analisis_palabras (historia_id, palabra, frecuencia)
                    VALUES (?, ?, ?)
                ''', (historia_id, palabra, frecuencia))
                
            print(f" -> ✓ Vocabulario indexado con éxito: {historia_id} ({len(conteo)} palabras únicas)")
            contador_procesadas += 1
            
        except sqlite3.Error as e:
            print(f"❌ Error en DB con {historia_id}: {e}")
            
    conn.commit()
    conn.close()
    print(f"\n¡Sincronización completada! Se procesaron {contador_procesadas} historias físicas de la carpeta textos.")

if __name__ == "__main__":
    procesar_directorio_historias()