
self.addEventListener('install', ()=> self.skipWaiting() );
self.addEventListener('activate', ()=> self.clients.claim() );

self.addEventListener('push',(event)=>{
  const data = event.data.json();
  console.log(data);
  event.waitUntil(  
    self.registration.showNotification(data.title,{
      body: data.body,
      icon: data.icon,
      badge: data.badge,
      image: data.image,
      actions: data.actions,
      vibrate: data.vibrate,
      tag: data.tag
    })
    )
});
self.addEventListener('notificationclick',(event)=>{
  event.notification.close();
  event.waitUntil(
    clients.openWindow('/')
  )
});
