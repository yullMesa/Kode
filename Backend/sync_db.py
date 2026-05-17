import os
import sqlite3
import re
import json

def extraer_numeros_de_texto(texto):
    """Respaldo: Extrae números sueltos si el archivo no tiene JSON estructurado."""
    patron = r'\d+[\.,]\d+|\d+'
    hallazgos = re.findall(patron, texto)
    numeros_limpios = []
    for num in hallazgos:
        if "." in num and len(num.split(".")[1]) == 3:
            num = num.replace(".", "")
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
    conn = sqlite3.connect('kode.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # TABLA 1: Historias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historias (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            es_buena INTEGER
        )
    ''')
    
    # TABLA 2: Métricas con COLUMNAS TOTALMENTE EXPLICITAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metricas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            historia_id TEXT,
            precio_cierre REAL,
            volumen REAL,
            empleados INTEGER,
            margen_ganancia REAL,
            efectivo_total REAL,
            deuda_total REAL,
            valor_generico REAL,
            FOREIGN KEY (historia_id) REFERENCES historias(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

    # Apuntar a data_source/textos para no mezclar canales
    ruta_textos = os.path.join("Backend", "data_source", "textos")
    
    if not os.path.exists(ruta_textos):
        print(f"❌ Error: No se encontró la carpeta en: {ruta_textos}")
        return

    cursor.execute("SELECT id FROM historias")
    procesados = {row[0] for row in cursor.fetchall()}

    archivos = [f for f in os.listdir(ruta_textos) if f.endswith('.txt')]
    nuevos = [f for f in archivos if f not in procesados]

    if not nuevos:
        print("✨ Todo al día. No hay textos nuevos en Backend/data_source/textos")
        conn.close()
        return

    print(f"🚀 Tienes {len(nuevos)} historias pendientes por clasificar.")

    for archivo in nuevos:
        ruta_archivo = os.path.join(ruta_textos, archivo)
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                if not lineas:
                    continue
                
                primera_linea = lineas[0].strip()
                
                # Procesar el resto del texto para la previsualización
                contenido_narrativo = "".join(lineas[1:])
                titulo_historia = lineas[1].strip()[:50] if len(lineas) > 1 else archivo

            print("\n" + "="*60)
            print(f"📄 ARCHIVO: {archivo}")
            print("-" * 60)
            print(f"{contenido_narrativo[:400]}...") 
            print("-" * 60)

            while True:
                opcion = input("¿Es buena historia? (1: SÍ / 0: NO / s: Salir): ").lower()
                
                if opcion in ['1', '0']:
                    opcion_int = int(opcion)
                    
                    # Guardar historia principal
                    cursor.execute("INSERT INTO historias (id, titulo, es_buena) VALUES (?, ?, ?)",
                                   (archivo, titulo_historia, opcion_int))
                    
                    # Intentar leer los datos explícitos del JSON en la línea 1
                    try:
                        datos_api = json.loads(primera_linea)
                        
                        # Inserción directa en columnas dedicadas
                        cursor.execute('''
                            INSERT INTO metricas (
                                historia_id, precio_cierre, volumen, empleados, 
                                margen_ganancia, efectivo_total, deuda_total, valor_generico
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL)
                        ''', (
                            archivo,
                            datos_api.get("precio_cierre"),
                            datos_api.get("volumen"),
                            datos_api.get("empleados"),
                            datos_api.get("margen_ganancia"),
                            datos_api.get("efectivo_total"),
                            datos_api.get("deuda_total")
                        ))
                        print("📊 Métricas estructuradas guardadas en columnas independientes.")
                        
                    except json.JSONDecodeError:
                        # Si el archivo es un texto plano común sin JSON, usamos el Regex de respaldo
                        numeros_extraidos = extraer_numeros_de_texto(primera_linea + contenido_narrativo)
                        for numero in numeros_extraidos:
                            cursor.execute('''
                                INSERT INTO metricas (
                                    historia_id, precio_cierre, volumen, empleados, 
                                    margen_ganancia, efectivo_total, deuda_total, valor_generico
                                ) VALUES (?, NULL, NULL, NULL, NULL, NULL, NULL, ?)
                            ''', (archivo, numero))
                        print(f"⚠️ Formato plano: Se guardaron {len(numeros_extraidos)} valores en la columna genérica.")

                    conn.commit()
                    print(f"✅ Guardado como: {'LUZ' if opcion == '1' else 'SOMBRA'}")
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
    print("\n✅ ¡Clasificación terminada!")

if __name__ == "__main__":
    clasificador_terminal()