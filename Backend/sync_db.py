import os
import sqlite3
import re


def extraer_numeros_de_texto(texto):
    """
    Busca todos los números en el texto. Soporta números limpios (150000)
    y formatos con puntos o comas (150.000 o 45.5).
    """
    patron = r'\d+[\.,]\d+|\d+'
    hallazgos = re.findall(patron, texto)
    
    numeros_limpios = []
    for num in hallazgos:
        # Si tiene un punto de miles (ej: 150.000), le quitamos el punto
        if "." in num and len(num.split(".")[1]) == 3:
            num = num.replace(".", "")
        # Si tiene una coma de miles (ej: 150,000)
        elif "," in num and len(num.split(",")[1]) == 3:
            num = num.replace(",", "")
            
        try:
            if "." in num or "," in num:
                numeros_limpios.append(float(num.replace(",", ".")))
            else:
                numeros_limpios.append(int(num))
        except ValueError:
            continue
            
    return numeros_limpios


def clasificador_terminal():
    # Conexión a la DB
    conn = sqlite3.connect('kode.db')
    cursor = conn.cursor()
    
    # Habilitamos las llaves foráneas en SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # TABLA 1: Historias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historias (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            es_buena INTEGER
        )
    ''')
    
    # TABLA 2: Métricas (Aquí la FK historia_id se puede repetir muchas veces)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metricas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id TEXT,
            valor REAL,
            FOREIGN KEY (historia_id) REFERENCES historias(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

    # Ruta exacta de tus textos
    ruta_textos = os.path.join("Backend", "uploads", "textos")
    
    if not os.path.exists(ruta_textos):
        print(f"❌ Error: No se encontró la carpeta en: {ruta_textos}")
        return

    # Revisar qué historias ya clasificaste
    cursor.execute("SELECT id FROM historias")
    procesados = {row[0] for row in cursor.fetchall()}

    archivos = [f for f in os.listdir(ruta_textos) if f.endswith('.txt')]
    nuevos = [f for f in archivos if f not in procesados]

    if not nuevos:
        print("✨ Todo al día. No hay textos nuevos en Backend/uploads/textos")
        conn.close()
        return

    print(f"🚀 Tienes {len(nuevos)} historias pendientes por clasificar.")

    for archivo in nuevos:
        ruta_archivo = os.path.join(ruta_textos, archivo)
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                primera_linea = contenido.split('\n')[0].strip()
                titulo_historia = primera_linea[:50] if primera_linea else archivo

            print("\n" + "="*60)
            print(f"📄 ARCHIVO: {archivo}")
            print("-" * 60)
            print(f"{contenido[:400]}...") 
            print("-" * 60)

            while True:
                opcion = input("¿Es buena historia? (1: SÍ / 0: NO / s: Salir): ").lower()
                
                if opcion in ['1', '0']:
                    opcion_int = int(opcion)
                    
                    # PASO A: Guardamos la historia en su tabla principal
                    cursor.execute("INSERT INTO historias (id, titulo, es_buena) VALUES (?, ?, ?)",
                                   (archivo, titulo_historia, opcion_int))
                    
                    # PASO B: AQUÍ SE CONECTA LA FUNCIÓN. Sacamos los números del texto de esta historia
                    numeros_extraidos = extraer_numeros_de_texto(contenido)
                    
                    # PASO C: Guardamos cada número en la tabla débil repitiendo la FK (archivo)
                    for numero in numeros_extraidos:
                        cursor.execute("INSERT INTO metricas (historia_id, valor) VALUES (?, ?)",
                                       (archivo, numero))
                    
                    conn.commit()
                    print(f"✅ Guardado como: {'LUZ' if opcion == '1' else 'SOMBRA'}")
                    print(f"📊 Se extrajeron y vincularon {len(numeros_extraidos)} números a esta historia.")
                    break
                    
                elif opcion == 's':
                    print("👋 Saliendo del clasificador...")
                    conn.close()
                    return
                else:
                    print("⚠️ Por favor, marca 1 (Bien) o 0 (Mal).")
        
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")

    conn.close()
    print("\n✅ ¡Clasificación y extracción terminadas!")

if __name__ == "__main__":
    clasificador_terminal()