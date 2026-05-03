

const contenedor=document.querySelector('main')
const botonHistorias = document.getElementById('btn-historias')


botonHistorias.addEventListener('click',() => {

    // 2. Generamos el HTML dinámico
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
                    <button id="publicar-historia" class="btn-principal">Publicar</button>
                </div>
            </div>
        </div>
    `;

    // 3. ¡IMPORTANTE! Buscamos los botones RECIÉN CREADOS aquí adentro
    const modal = document.getElementById('mi-modal');
    const btnAbrir = document.getElementById('abrir-modal');
    const btnCerrar = document.getElementById('cerrar-modal');
    const btnPublicar = document.getElementById('publicar-historia');

    // 4. Ahora sí, como ya existen, les ponemos los eventos
    btnAbrir.addEventListener('click', () => {
        modal.style.display = 'flex';
    });

    btnCerrar.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    btnPublicar.addEventListener('click', () => {
        const texto = document.getElementById('texto-historia').value;
        if (texto) {
            alert("Publicado con éxito");
            modal.style.display = 'none';
        } else {
            alert("Escribe algo primero");
        }
    });

}); // <--- Esta llave cierra el primer clic. TODO debe estar antes de esta llave.

    



