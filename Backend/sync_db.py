import os
import sqlite3

def inicializar_db():
    conn = sqlite3.connect('kode.db')
    cursor = conn.cursor()
    # Creamos la tabla con el ID del archivo y el Booleano de clasificación
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historias (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            es_buena INTEGER
        )
    ''')
    conn.commit()
    return conn


def clasificador_terminal():
    # 1. Conexión a la DB (se crea en la raíz donde estás parado)
    conn = sqlite3.connect('kode.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historias (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            es_buena INTEGER
        )
    ''')
    conn.commit()

    # 2. Ruta exacta según tu imagen: Backend -> uploads -> textos
    # Usamos join para que no haya lio con los slashes / o \
    ruta_textos = os.path.join("Backend", "uploads", "textos")
    
    if not os.path.exists(ruta_textos):
        print(f"❌ Error: No se encontró la carpeta en: {ruta_textos}")
        return

    # 3. Revisar qué historias ya clasificaste
    cursor.execute("SELECT id FROM historias")
    procesados = {row[0] for row in cursor.fetchall()}

    # Listar solo archivos .txt
    archivos = [f for f in os.listdir(ruta_textos) if f.endswith('.txt')]
    nuevos = [f for f in archivos if f not in procesados]

    if not nuevos:
        print("✨ Todo al día. No hay textos nuevos en Backend/uploads/textos")
        return

    print(f"🚀 Tienes {len(nuevos)} historias pendientes por clasificar.")

    for archivo in nuevos:
        ruta_archivo = os.path.join(ruta_textos, archivo)
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                # Título: primera línea o nombre del archivo si está vacío
                primera_linea = contenido.split('\n')[0].strip()
                titulo_historia = primera_linea[:50] if primera_linea else archivo

            print("\n" + "="*60)
            print(f"📄 ARCHIVO: {archivo}")
            print("-" * 60)
            print(f"{contenido[:400]}...") # Muestra un resumen del texto
            print("-" * 60)

            while True:
                opcion = input("¿Es buena historia? (1: SÍ / 0: NO / s: Salir): ").lower()
                
                if opcion in ['1', '0']:
                    cursor.execute("INSERT INTO historias (id, titulo, es_buena) VALUES (?, ?, ?)",
                                   (archivo, titulo_historia, int(opcion)))
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