import yfinance as yf
import os

def generar_reporte_economico():
    # Instanciamos el ticker de Apple (puedes cambiarlo por MSFT, TSLA, BTC-USD, etc.)
    nombre_ticker = "AAPL"
    ticker = yf.Ticker(nombre_ticker)
    
    # 1. Traemos el historial para precios del mercado de hoy
    historial = ticker.history(period="1d")
    if historial.empty:
        print("No se pudieron traer datos históricos.")
        return

    precio_cierre = round(historial['Close'].iloc[0], 2)
    volumen = int(historial['Volume'].iloc[0])

    # 2. 🚀 LA MAGIA: Acceder al diccionario .info para sacar métricas avanzadas
    info = ticker.info
    
    # Sacamos datos que sirvan para contrastar (Luz/Sombra económica)
    empleados = info.get('fullTimeEmployees', 0)
    margen_ganancia = info.get('profitMargins', 0) * 100  # Convertir a porcentaje (ej: 26.5%)
    efectivo_total = info.get('totalCash', 0)
    deuda_total = info.get('totalDebt', 0)

    # 3. Redactamos un texto plano corporativo denso en números para que el Regex se de un banquete
    contenido = (
        f"Informe Analitico de Mercado: {nombre_ticker}\n"
        f"El dia de hoy las acciones cerraron con un valor de {precio_cierre} dolares en la bolsa, "
        f"registrando un movimiento de {volumen} acciones negociadas.\n"
        f"La empresa cuenta actualmente con una fuerza laboral de {empleados} empleados a tiempo completo. "
        f"En su ultimo balance, reportaron un margen de ganancia neta del {round(margen_ganancia, 2)} por ciento.\n"
        f"Financieramente, la entidad dispone de {efectivo_total} dolares en efectivo total, "
        f"frente a una deuda acumulada en sus libros de {deuda_total} dolares."
    )

    # Guardamos en la carpeta limpia del sistema
    ruta = os.path.join("Backend", "data_source", "textos", f"reporte_{nombre_ticker.lower()}.txt")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
        
    print(f"📰 ¡Reporte avanzado creado en Backend/data_source/textos/reporte_{nombre_ticker.lower()}.txt!")

if __name__ == "__main__":
    generar_reporte_economico()