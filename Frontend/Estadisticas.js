

// Exportamos la función para que Main.js la pueda ver
export function renderEstadisticas(contenedor) {
    contenedor.innerHTML = `
        <div class="seccion-estadisticas">
            <h2>Panel de Estadísticas</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h4>Historias Totales</h4>
                    <p id="total-historias">Cargando...</p>
                </div>
                <div class="stat-card">
                    <h4>Palabras Narradas</h4>
                    <p id="total-palabras">0</p>
                </div>
            </div>
            <button id="btn-volver" class="btn-secundario">Volver al Feed</button>
        </div>
    `;

    // Aquí puedes llamar a tu backend para pedir datos reales
    obtenerDatosBackend();

    // Lógica para el botón volver (ejemplo)
    document.getElementById('btn-volver').onclick = () => {
        location.reload(); // O llamar a la función que carga el feed
    };
}

async function obtenerDatosBackend() {
    try {
        const res = await fetch('http://127.0.0.1:8000/historias');
        const data = await res.json();
        document.getElementById('total-historias').innerText = data.length;
    } catch (err) {
        console.error("Error en stats:", err);
    }
}