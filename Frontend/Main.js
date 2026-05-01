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

           <!-- 3. La Grilla de Historias (El feed que va al fondo) -->
        <div class="feed-grid">
            <div class="story-card" style="background-color: #ffe0e0;"></div>
            <div class="story-card" style="background-color: #e0f2ff;"></div>
            <div class="story-card" style="background-color: #e0ffe0;"></div>
            <!-- Aquí es donde el backend irá metiendo las tarjetas nuevas -->
        </div> 
    </div>
`;
});

// Escuchamos los clics en todo el main
mainContent.addEventListener('click', (e) => { // La 'e' nace aquí
    
    // Abrir
    if (e.target.closest('#open-modal')) {
        document.getElementById('modal-container').classList.add('active');
    }

    // Cerrar
    if (e.target.id === 'close-modal') {
        document.getElementById('modal-container').classList.remove('active');
    }

    // --- AQUÍ DEBE IR EL DE PUBLICAR PARA QUE RECONOZCA LA 'e' ---
    if (e.target.id === 'publish-btn') {
        const formData = new FormData();
        formData.append('nombre_img', document.getElementById('char-name-img').files[0]);
        formData.append('bg_color', document.getElementById('bg-color').value);
        formData.append('personaje_img', document.getElementById('char-img').files[0]);
        formData.append('historia', document.getElementById('story-text').value);

        fetch('http://localhost:8000/publicar-historia', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            console.log('Éxito:', data);
            document.getElementById('modal-container').classList.remove('active');
        });
    }
}); // Aquí termina la 'e'});
