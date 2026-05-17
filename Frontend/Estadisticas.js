// 1. Exportación principal de la interfaz
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
                <div class="card">
                    <h3>Proporción historias buenas vs malas</h3>
                    <div class="chart-container">
                        <canvas id="chart-balance"></canvas>
                    </div>
                </div>

                <div class="card">
                    <h3>Métricas Financieras por Reporte</h3>
                    <div class="chart-container">
                        <canvas id="chart-timeline"></canvas>
                    </div>
                </div>

                <div class="card">
                    <h3>Palabras más Repetidas</h3>
                    <div class="chart-container">
                        <canvas id="chart-palabras"></canvas>
                    </div>
                </div>

                <div class="card card-contador">
                    <h3>Historias Registradas</h3>
                    <div class="contador-numero" id="total-historias-contador">-</div>
                </div>
                <div class="card"><h3>Core Topics</h3><canvas id="chart-topics"></canvas></div>
                <div class="card"><h3>Variables</h3><canvas id="chart-vars"></canvas></div>
                <div class="card"><h3>Victim Count</h3><canvas id="chart-victims"></canvas></div>
            </main>
        </div>
    `;

    // Orquestamos la carga de datos
    obtenerDatosBackend();
}

// 2. Centralizador de peticiones asíncronas al Backend
async function obtenerDatosBackend() {
    try {
        // --- PETICIÓN 1: Tabla Historias (Pie Chart) ---
        // --- PETICIÓN 1: Tabla Historias (Pie Chart + Contador Central) ---
        const resHistorias = await fetch('http://127.0.0.1:8000/api/metricas-totales');
        const dataHistorias = await resHistorias.json();

        if (dataHistorias.status !== "error") {
            // 1. Contamos cuántas buenas y malas hay para el Pie Chart
            const buenas = dataHistorias.filter(h => h.es_buena === 1).length;
            const malas = dataHistorias.filter(h => h.es_buena === 0).length;
            crearPieChart(buenas, malas);
            
            // 🚀 2. Inyectamos el total de historias directamente en la nueva tarjeta
            const totalHistoriasContador = document.getElementById('total-historias-contador');
            if (totalHistoriasContador) {
                totalHistoriasContador.innerText = dataHistorias.length;
            }
        }

        // --- PETICIÓN 2: Tabla Métricas (Bar Chart Vertical) ---
        const resMetricas = await fetch('http://127.0.0.1:8000/api/metricas-detalle');
        const dataMetricas = await resMetricas.json();

        if (dataMetricas.status !== "error") {
            const etiquetas = dataMetricas.map(m => m.historia_id.replace('.txt', ''));
            const valores = dataMetricas.map(m => m.cifra_financiera);
            crearBarChart(etiquetas, valores);
        }

        // --- 🚀 PETICIÓN 3: Tabla Análisis Palabras (Bar Chart Horizontal) ---
        const resPalabras = await fetch('http://127.0.0.1:8000/api/palabras-repetidas');
        const dataPalabras = await resPalabras.json();

        if (dataPalabras.status !== "error") {
            const etiquetasPalabras = dataPalabras.map(item => item.palabra);
            const valoresPalabras = dataPalabras.map(item => item.frecuencia);
            crearHorizontalBarChart(etiquetasPalabras, valoresPalabras);
        }

    } catch (err) {
        console.error("Error cargando los datos analíticos en el Dashboard:", err);
    }
}

// ==========================================
// FUNCIÓNES DEDICADAS DE RENDERIZADO (CHART.JS)
// ==========================================

// Gráfico 1: Torta
function crearPieChart(cantidadBuenas, cantidadMalas) {
    const ctx = document.getElementById('chart-balance');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Luz (Buenas)', 'Sombra (Malas)'],
            datasets: [{
                data: [cantidadBuenas, cantidadMalas],
                backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                borderColor: ['rgb(75, 192, 192)', 'rgb(255, 99, 132)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#ffffff' } }
            }
        }
    });
}

// Gráfico 2: Barras Verticales Financieras
function crearBarChart(labels, valores) {
    const ctx = document.getElementById('chart-timeline');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Valor Analizado',
                data: valores,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { color: '#ffffff' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                y: { type: 'logarithmic', ticks: { color: '#ffffff' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
            },
            plugins: {
                legend: { labels: { color: '#ffffff' } }
            }
        }
    });
}

// Gráfico 3: Barras Horizontales de Vocabulario
function crearHorizontalBarChart(labels, valores) {
    const ctx = document.getElementById('chart-palabras');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Frecuencia Global',
                data: valores,
                backgroundColor: 'rgba(235, 94, 40, 0.6)', // Óxido / Naranja neo-gótico
                borderColor: 'rgba(235, 94, 40, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y', // 🚀 Esto acuesta las barras horizontalmente
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { ticks: { color: '#a0a0a0' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                y: { ticks: { color: '#e0e0e0', font: { weight: 'bold' } }, grid: { display: false } }
            }
        }
    });
}