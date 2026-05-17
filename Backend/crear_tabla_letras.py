import sqlite3
import os

def inicializar_tabla_palabras():
    # 📌 Subimos un nivel para encontrar el kode.db que está en la raíz real del proyecto
    base_dir = os.path.dirname(__file__)  # Carpeta Backend/
    db_path = os.path.abspath(os.path.join(base_dir, "..", "kode.db"))  # Raíz/kode.db
    
    print(f"Conectando a la DB central en: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # Creamos la tabla analítica vinculada mediante FK a 'historias'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analisis_palabras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id TEXT,
            palabra TEXT,
            frecuencia INTEGER,
            FOREIGN KEY (historia_id) REFERENCES historias(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("✓ Tabla 'analisis_palabras' creada/actualizada en la DB central.")

if __name__ == "__main__":
    inicializar_tabla_palabras()