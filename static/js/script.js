if ('ServiceWorker' in navigator){
  navigator.serviceWorker.register('/static/js/sw.js');
};
// Coneccion con SocketIo
socket = io();
// -------------------------------------------------------------|
const codigo = document.querySelector("#codigo");
const txt_area = document.querySelector("#txt_area_paste");
const progress_barr = document.querySelector("#progress_barr");
const porcentaje_barr = document.querySelector("#porcentaje");
const imagen_a= document.querySelector("#imagen");
const inp_file = document.querySelector('#input_file');
const inp_file_btn = document.querySelector('.btn-subir');
const contenedor_multimedia = document.querySelector('.contenedor_multimedia');
// ------------------------------------------------------------|

// ------------------------------------------------------------|
function crear_elemento_media(tipo){
  let elemento_multimedia ;
  contenedor_multimedia.replaceChildren();
  if (tipo == 'video' || tipo == 'audio'){
    elemento_multimedia = document.createElement(`${tipo}`);
    elemento_multimedia.src = `/${tipo}`;
    elemento_multimedia.className = `media ${tipo}`;
    elemento_multimedia.controls = true;
    contenedor_multimedia.appendChild(elemento_multimedia);
  }
  else if (tipo == 'imagen'){
    elemento_multimedia = document.createElement('img');
    elemento_multimedia.src = '/imagen';
    elemento_multimedia.className = 'imagen';
    contenedor_multimedia.appendChild(elemento_multimedia);
  };
  let media = document.querySelector('.media');
   if (media.localName == 'video'){
      media.src = `/video?t=${Date.now()}`;
      media.load();
   };
};
// --------------------------------------------------------------------|

socket.on('cargar_archivo', (data)=>{
  crear_elemento_media(data.tipo);
});


// --------------------------------------------------------------------|
let contenedores = {
  'portapapeles': document.querySelector('#contenedor_area_texto'),
  'archivo':      document.querySelector('#contenedor_area_archivo'),
  'li_portapapeles': document.querySelector('.li_portapapeles'),
  'li_archivo': document.querySelector('.li_archivo')
};

function desactivar(elemento){
  switch (elemento){
    case 'portapapeles':
      contenedores['portapapeles'].classList.add('desactive');
      contenedores['archivo'].classList.remove('desactive');
      contenedores['li_archivo'].classList.add('active');
      contenedores['li_portapapeles'].classList.remove('active');
      break;
    case 'archivo':
      contenedores['archivo'].classList.add('desactive');
      contenedores['portapapeles'].classList.remove('desactive');
      contenedores['li_portapapeles'].classList.add('active');
      contenedores['li_archivo'].classList.remove('active');
  }
};










// --------------------------------------------------------------------|

inp_file.addEventListener('change', ()=>{
  inp_file_btn.textContent = `Archivo elegido: ${inp_file.files[0]?.name}`
});

// -----------------------------------------------------------------|

const copiar_btn = document.querySelector("#btn_copiar");
copiar_btn.addEventListener('click', ()=>{
    const texto = codigo.textContent;
    const temp = document.createElement('textarea');
    temp.value = texto;
    document.body.appendChild(temp);
    temp.select();
    document.execCommand('copy');
    document.body.removeChild(temp);
});

// -----------------------------------------------------------------|

txt_area.addEventListener("input",()=>{
    socket.emit("txt_change",txt_area.value)
});

socket.on('txt_recive', (data)=>{
    txt_area.value = data;
    codigo.textContent = data;
    codigo.removeAttribute('data-highlighted');
    const result = hljs.highlightAuto(data);
    codigo.innerHTML = result.value;
});



socket.on('ult_archivo', (data)=>{
    document.getElementById('txt_archivo').innerHTML = `<strong>Archivo disponible:</strong> ${data}`;
    socket.emit("verificar_archivo_disponible");
});

//SUBIR ARCHIVO --------------------------------------------------|
const xhr = new XMLHttpRequest();
xhr.upload.onprogress = function(e){
    const porcentaje = Math.round((e.loaded/e.total)* 100);
    progress_barr.style.width = `${porcentaje}%`;
    progress_barr.innerText = `${porcentaje}%`
};

xhr.onload = function(){
    const respuesta = JSON.parse(xhr.responseText);
};
// ---------------------------------------------------------------|

const input_file = document.querySelector("#input_file");

function subir(){
    const formData = new FormData();
    formData.append('archivo', input_file.files[0]);
    xhr.open('POST', '/upload');
    xhr.send(formData);
};
// ---------------------------------------------------------------|

