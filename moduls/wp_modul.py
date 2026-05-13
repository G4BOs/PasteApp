"""
Módulo para registrar suscripciones y enviar notificaciones Push 

"""


import json
import pywebpush
import os
from dotenv import load_dotenv 
load_dotenv()
suscriptions = []


def notificar(mensaje: str):
    """
    Notificar a todos los registrados, recibe un dict de 'request.get_json()'
    """
    
    datos = json.dumps({
        'title': 'Paste App',
        'body': mensaje,
        'icon': '/static/android-chrome-192x192.png',
        'badge': '/static/badge-mensaje.png',
        'image': '/imagen',
        'actions': [
            {"action": "open", "title": "Abrir"},
            {"action": "dismiss", "title": "Ignorar"}
            ],
        "vibrate": [200,100,200],
        "tag": "Notificacion-mensaje"
        })
    
    for sub in suscriptions[:]:
        try:
            pywebpush.webpush(
                    subscription_info=sub,
                    data=datos,
                    vapid_private_key=os.getenv('PRIVATE_KEY') ,
                    vapid_claims={"sub": f'mailto:{os.getenv("VAPID_MAIL")}'}
                    )
        except pywebpush.WebPushException as ex:
            if ex.response.status_code in [404,410]: # type: ignore
                print('Usuario no encontrado, borrando')
                suscriptions.remove(sub)
                print(suscriptions)

def check_endpoint(endpoint: str)->bool:
    """
    Verifica si un endpoint existe en la base de datos
    """
    for usr in suscriptions:
        if usr['endpoint'] == endpoint:
            return True
    return False

def suscribir(data: dict):
    if not check_endpoint(data['endpoint']):
        suscriptions.append(data)
        print('Usuario nuevo registrado')
    print(suscriptions)
    print('==='*20, len(suscriptions))

