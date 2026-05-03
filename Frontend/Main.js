

const contenedor=document.querySelector('main')
const botonHistorias = document.getElementById('btn-historias')


botonHistorias.onclick = (e) => {
    e.preventDefault(); // Evita cualquier salto al inicio de la página
    
    contenedor.innerHTML = `
        <div class="capsula-historias">
            <button class="btn-historias" id="abrir-modal">Subir Historia +</button>
        </div>

        <div id="mi-modal" class="modal-overlay">
            <div class="modal-content">
                <h3>Nueva Publicación</h3>
                <label for="input-foto" class="label-archivo">Seleccionar Imagen</label>
                <input type="file" id="input-foto" accept="image/*" style="display: none;">
                <textarea id="texto-historia" placeholder="Escribe tu historia aquí..."></textarea>
                <div class="modal-botones">
                    <button id="cerrar-modal" class="btn-secundario">Cerrar</button>
                    <!-- EL CAMBIO CLAVE: type="button" y return false -->
                    <button id="publicar-historia" class="btn-principal" type="button">Publicar</button>
                </div>
            </div>
        </div>
    `;

    // 3. ¡IMPORTANTE! Buscamos los botones RECIÉN CREADOS aquí adentro
    const modal = document.getElementById('mi-modal');
    const btnAbrir = document.getElementById('abrir-modal');
    const btnCerrar = document.getElementById('cerrar-modal');
    const btnPublicar = document.getElementById('publicar-historia');

    contenedor.onclick = async (event) => {
        const target = event.target;

        // Si clickean Abrir
        if (target.id === 'abrir-modal') {
            modal.style.display = 'flex';
        }

        // Si clickean Cerrar
        if (target.id === 'cerrar-modal') {
            modal.style.display = 'none';
        }

        // Si clickean Publicar
        if (target.id === 'publicar-historia') {
            event.preventDefault(); // BLOQUEO TOTAL de recarga
            event.stopPropagation(); // Evita que el evento suba más

            const inputFoto = document.getElementById('input-foto');
            const areaTexto = document.getElementById('texto-historia');

            if (!inputFoto.files[0]) {
                alert("Selecciona una imagen");
                return;
            }

            const formData = new FormData();
            formData.append("file", inputFoto.files[0]);
            formData.append("text", areaTexto.value);

            try {
                const response = await fetch('http://127.0.0.1:8000/upload', {
                    method: 'POST',
                    body: formData
                });

                const resultado = await response.json();
                if (resultado.status === "ok") {
                    alert("¡Publicado con éxito!");
                    modal.style.display = 'none';
                }
            } catch (err) {
                console.error("Error:", err);
            }
        }
    };

}; // <--- Esta llave cierra el primer clic. TODO debe estar antes de esta llave.

    

