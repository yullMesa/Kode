

// Exportamos la función para que Main.js la pueda ver
export function renderEstadisticas(contenedor) {
    contenedor.innerHTML = `
        <div class="dashboard-wrapper">
            <header class="dashboard-header">
                <select id="category-filter">
                <option value="">FILTRAR NARRATIVAS</option>
                <option value="real">Real</option>
                <option value="ficticia">Ficticia</option>
                </select>
            </header>

            <main class="stats-grid">
                <div class="card"><h3>Timeline</h3><canvas id="chart-timeline"></canvas></div>
                <div class="card"><h3>Frenzy Level</h3><canvas id="chart-frenzy"></canvas></div>
                <div class="card"><h3>Sentiment</h3><canvas id="chart-sentiment"></canvas></div>
                <div class="card"><h3>Core Topics</h3><canvas id="chart-topics"></canvas></div>
                <div class="card"><h3>Variables</h3><canvas id="chart-vars"></canvas></div>
                <div class="card"><h3>Victim Count</h3><canvas id="chart-victims"></canvas></div>
            </main>
        </div>
    `;

    // Aquí puedes llamar a tu backend para pedir datos reales
    obtenerDatosBackend();

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