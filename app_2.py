import asyncio
import websockets
import json
import redis

r = redis.Redis(host='192.168.88.244', port=6379, decode_responses=True)
texto = r.get('texto')

async def handler(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            match data['event']:
                case 'saludar':
                    await websocket.send( json.dumps({'event': 'respuesta', 'message': 'Hola Godot desde Python'}))
                case 'cambiar_texto':
                    r.set('texto', data['texto'])



    except Exception as e:
        print(f"Cliente desconectado: {e}")

async def main():
    async with websockets.serve(handler, '0.0.0.0', 9001):
        await asyncio.Future()

asyncio.run(main())
