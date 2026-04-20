socket = io();
const codigo = document.querySelector("#codigo");
const txt_area = document.querySelector("#txt_area_paste");
const progress_barr = document.querySelector("#progress_barr");
const porcentaje_barr = document.querySelector("#porcentaje");
const video_a = document.querySelector("#video");

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

socket.emit("verific_video");
socket.on("video", (data)=>{
    if (data){
        video_a.style.display = "inline-block";
    }
    else{
        video_a.style.display = "none"
    }
});

socket.on('ult_archivo', (data)=>{
    document.getElementById('txt_archivo').innerHTML = `<strong>Archivo disponible:</strong> ${data}`;
    socket.emit("verific_video");
});

//SUBIR ARCHIVO
const xhr = new XMLHttpRequest();
xhr.upload.onprogress = function(e){
    const porcentaje = Math.round((e.loaded/e.total)* 100);
    progress_barr.style.width = `${porcentaje}%`;
    progress_barr.innerText = `${porcentaje}%`
};

xhr.onload = function(){
    const respuesta = JSON.parse(xhr.responseText);
    console.log(respuesta);
};

const input_file = document.querySelector("#input_file");

function subir(){
    const formData = new FormData();
    formData.append('archivo', input_file.files[0]);
    xhr.open('POST', '/upload');
    xhr.send(formData);
};

