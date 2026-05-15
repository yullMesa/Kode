import yfinance as yf
import os

def generar_reporte_economico():
    # Traemos la info de Apple (AAPL)
    ticker = yf.Ticker("AAPL")
    historial = ticker.history(period="1d")
    
    if historial.empty:
        print("No se pudieron traer datos de Yahoo Finance.")
        return

    precio_cierre = round(historial['Close'].iloc[0], 2)
    volumen = int(historial['Volume'].iloc[0])

    contenido = f"Reporte Financiero de Apple\n" \
                f"El dia de hoy las acciones de Apple cerraron con un valor de {precio_cierre} dolares en la bolsa. " \
                f"Se registro un volumen total de transacciones de {volumen} acciones."

    # 🚨 AQUÍ ESTÁ EL CAMBIO: Guardamos en Backend/data_source/textos
    ruta = os.path.join("Backend", "data_source", "textos", "reporte_apple.txt")
    
    # Creamos las carpetas si no existen, sin tocar uploads
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
        
    print("📰 ¡Reporte del sistema creado con éxito en Backend/data_source/textos/reporte_apple.txt!")

if __name__ == "__main__":
    generar_reporte_economico()