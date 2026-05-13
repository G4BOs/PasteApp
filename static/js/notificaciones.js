

async function get_public_key(){
  let respuesta = await fetch('/obt_publicKey',{
    method: 'GET'
  });
  let datos = await respuesta.json();
  let public_key_data = datos.public_key;
  return public_key_data
  
};


let registration;

document.addEventListener('DOMContentLoaded', async ()=>{
  if ('serviceWorker' in navigator){
    registration = await navigator.serviceWorker.register('/static/js/sw.js')
  }
});


export async function suscribirse(){
  const permiso = await Notification.requestPermission();
  if (permiso != 'granted'){
    alert('Permiso Denegado')
    return
  }
  const suscripcion = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: await get_public_key() 

  });
  await fetch('/suscribir',{
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(suscripcion)
  })

}

export async function notificar(mensaje){
  await fetch('/notificar',{
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({'mensaje': mensaje})
  })
}
