const btnHistorias = document.getElementById('btn-historias');
const mainContent = document.querySelector('main');

btnHistorias.addEventListener('click', () => {
    // Aquí es donde "renuevas" la página inyectando el nuevo HTML
    mainContent.innerHTML = `
        <section class='upload-container'>
        <!-- El rectangulo gris -->
        <button class='btn-upload'>Subir historia +</button>
        
    
        </section>
    `;
});