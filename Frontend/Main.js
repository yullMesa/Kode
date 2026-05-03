

const contenedor=document.querySelector('main')
const botonHistorias = document.getElementById('btn-historias')


botonHistorias.addEventListener('click',() => {

    contenedor.innerHTML='<div class="capsula-historias"><button class="btn-historias">Subir Historia +</button></div>';

});
