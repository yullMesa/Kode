

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

    cargarFeed()

}; // <--- Esta llave cierra el primer clic. TODO debe estar antes de esta llave.


async function cargarFeed() {
    try {
        const response = await fetch('http://127.0.0.1:8000/historias');
        const historias = await response.json();

        let feedDiv = document.getElementById('feed-dinamico');
        if (!feedDiv) {
            feedDiv = document.createElement('div');
            feedDiv.id = 'feed-dinamico';
            feedDiv.className = 'feed-container';
            contenedor.appendChild(feedDiv);
        }

        feedDiv.innerHTML = '';

        historias.reverse().forEach(post => {
            const btn = document.createElement('button');
            btn.className = 'post-btn';
            
            // 1. Creamos la imagen manualmente (como ya tienes en tu captura)
            const img = document.createElement('img');
            img.src = `http://127.0.0.1:8000/ver-foto/${post.img}`;
            img.crossOrigin = "anonymous";
            img.alt = "Post";

            // 2. IMPORTANTE: Estos estilos obligan a la imagen a "rellenar" el cuadro
            // ignorando esos bordes invisibles que mencionaste.
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'cover'; 
            img.style.display = 'block';

            // 3. Metemos la imagen dentro del botón
            btn.appendChild(img);

            btn.onclick = () => {
                console.log("Historia ID:", post.id);
            };

            feedDiv.appendChild(btn);
        });
    } catch (error) {
        console.error("Error:", error);
    }
}

    

