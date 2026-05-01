const btnHistorias = document.getElementById('btn-historias');
const mainContent = document.querySelector('main');


btnHistorias.addEventListener('click', () => {
    // Aquí es donde "renuevas" la página inyectando el nuevo HTML
    mainContent.innerHTML = `
    <div class="upload-container">
        <button id="open-modal" class="btn-upload">Subir historia +</button>
    </div>

    <div id="modal-container" class="modal-overlay">
        <div class="modal-content">
            <h3>Nueva Publicación</h3>
            
            <div class="form-group">
                <label>1. Nombre del Personaje (Imagen)</label>
                <input type="file" id="char-name-img" accept="image/*">
            </div>

            <div class="form-group">
                <label>2. Color de Fondo</label>
                <input type="color" id="bg-color" value="#f2f2f2">
            </div>

            <div class="form-group">
                <label>3. Imagen del Personaje</label>
                <input type="file" id="char-img" accept="image/*">
            </div>

            <div class="form-group">
                <label>4. Tu Historia</label>
                <textarea id="story-text" placeholder="Escribe la historia aquí..."></textarea>
            </div>

            <div class="modal-actions">
                <button id="close-modal" class="btn-secondary">Cancelar</button>
                <button id="publish-btn" class="btn-primary">Publicar</button>
            </div>
        </div>
    </div>
`;
});

// Escuchamos los clics en todo el main
mainContent.addEventListener('click', (e) => {
    
    // Si el elemento que clickearon es el de abrir el modal
    if (e.target.id === 'open-modal') {
        document.getElementById('modal-container').classList.add('active');
    }

    // Si el elemento es el de cerrar el modal
    if (e.target.id === 'close-modal') {
        document.getElementById('modal-container').classList.remove('active');
    }
    
    // Cerrar si hacen clic en el fondo oscuro (opcional, muy pro)
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});