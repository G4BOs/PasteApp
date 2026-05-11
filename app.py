# IMPORTS 
from flask import Flask, jsonify, request, render_template, redirect, send_file, session
from flask_socketio import SocketIO, emit, disconnect
from flask_sock import Sock
import gevent
import os
from dotenv import load_dotenv
load_dotenv()
import secrets
import redis

# -------------------------------------------------|
# -------------------------------------------------|
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
socketio = SocketIO(app, async_mode='gevent')
sock = Sock(app)

port = int( os.getenv('PORT', '9000') )
#SERVIDOR INICIADO 
print(f"SERVIDOR INICIADO EN PUERTO: {port}")
# -------------------------------------------------|
r = redis.Redis(host='192.168.88.244',port=6379, decode_responses=True)

txt = ''
ult_arch = ''

# -------------------------------------------------|
#                     Funciones                    |
# -------------------------------------------------|
def cargar_nombre():
    """
    Cargar el nombre del archivo alojado
    """
    global ult_arch
    try:
        with open('uploads/info.txt', 'r') as f:
            ult_arch = f.read()
    except FileNotFoundError:
        ult_arch = ""
        with open('uploads/info.txt', "w") as f:
            f.write("")

# Carga el nombre del ultimo archivo al iniciar servidor
cargar_nombre()

@app.route('/api',methods=['GET'])
def api():
    datos = {'prueba': 'OK', 'dato': 999, 'nombre': 'Daniel', 'message': 'Hola DANIEL'}
    return jsonify(datos)

@sock.route('/ws')
def websocket(ws):
    while True:
        data = ws.receive()
        ws.send(data)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=["POST"])
def upload():
    archivo = request.files['archivo']
    archivo.save('uploads/ultimo')
    with open('uploads/info.txt','w') as f:
        f.write(archivo.filename or 'noname')
    cargar_nombre()
    socketio.emit('ult_archivo',ult_arch)
    return jsonify({'ok':True})

@app.route('/download', methods=['GET'])
def download():
    return send_file('uploads/ultimo', download_name=ult_arch, as_attachment=True)

@app.route('/video',methods=['GET'])
def video():
    return send_file('uploads/ultimo', download_name=ult_arch, as_attachment=True)

@app.route('/imagen', methods=['GET'])
def imagen():
    return send_file('uploads/ultimo', download_name=ult_arch, as_attachment=True)

@app.route('/audio', methods=['GET'])
def audio():
    return send_file('uploads/ultimo', download_name=ult_arch, as_attachment=True)

# -------------------------------------------------------------------|
def tipo_de_archivo(archivo):
    formats = {
            'video': ['mp4','avi'],
            'imagen': ['png', 'jpg', 'jepg'],
            'audio': ['mp3']
            }
    for types in formats: # Itera sobre todos los tipos de archivos
        for frmts in formats[types]: # itera por cada formato
            if frmts in archivo: # Si un formato coincide con alguno
                return types # retorna el tipo
    return 'otro'


#--------------------------------------------------------------------|
def enviar_archivo(archivo):
    tipo = tipo_de_archivo(archivo)
    socketio.emit('cargar_archivo',{'tipo': tipo, 'ruta': f'/{tipo}'}, to=session.get('usr_sid'))


# -------------------------------------------------------------------|

@socketio.on('verificar_archivo_disponible')
def handle_verificar_archivo_disponible():
    enviar_archivo(ult_arch)



# -------------------------------------------------------------------------|
@socketio.on('txt_change')
def handle_txtChange(data):
    global txt
    txt = data
    r.set('texto',txt)
    emit("txt_recive",data, broadcast=True, skip_sid=session.get('usr_sid'))
    enviar_archivo(ult_arch)

# *************************************************************************|
@socketio.on('connect')
def handle_connect():
    if not 'usr_sid' in session:
        session['usr_sid'] = request.sid # type: ignore
    cargar_nombre()
    emit('ult_archivo', ult_arch)
    emit('txt_recive', txt)

# *************************************************************************|
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=False, port=port)
