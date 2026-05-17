import yfinance as yf
import os
import json

def generar_reporte_economico(ticker_name="AAPL"):
    ticker = yf.Ticker(ticker_name)
    historial = ticker.history(period="1d")
    
    if historial.empty:
        print(f"❌ No se encontraron datos para {ticker_name}")
        return

    # 1. Extraer los datos reales
    precio_cierre = round(historial['Close'].iloc[0], 2)
    volumen = int(historial['Volume'].iloc[0])
    
    info = ticker.info
    empleados = info.get('fullTimeEmployees', None)
    margen_ganancia = round(info.get('profitMargins', 0) * 100, 2) if info.get('profitMargins') else None
    efectivo_total = info.get('totalCash', None)
    deuda_total = info.get('totalDebt', None)

    # 2. Creamos un diccionario con las métricas etiquetadas
    metricas = {
        "precio_cierre": precio_cierre,
        "volumen": volumen,
        "empleados": empleados,
        "margen_ganancia": margen_ganancia,
        "efectivo_total": efectivo_total,
        "deuda_total": deuda_total
    }

    # 3. Empacamos las métricas en una sola línea de texto (JSON compacto)
    linea_metricas = json.dumps(metricas)

    # 4. Redactamos el archivo. La línea 1 tiene los datos estructurados, el resto es la historia narrativa
    contenido = (
        f"{linea_metricas}\n"  # <--- Línea 1 oculta para el sistema
        f"Informe Analitico de Mercado: {ticker_name}\n"
        f"El dia de hoy las acciones cerraron con un valor de {precio_cierre} dolares en la bolsa, "
        f"registrando un movimiento de {volumen} acciones negociadas.\n"
        f"La entidad dispone de {efectivo_total} dolares en efectivo total, "
        f"frente a una deuda acumulada en sus libros de {deuda_total} dolares."
    )

    # Guardamos en la carpeta de datos del sistema
    ruta = os.path.join("Backend", "data_source", "textos", f"reporte_{ticker_name.lower()}.txt")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
        
    print(f"📰 Reporte estructurado creado para {ticker_name}")

if __name__ == "__main__":
    generar_reporte_economico("AAPL")
    generar_reporte_economico("TSLA")  # Puedes meter los que quieras probar