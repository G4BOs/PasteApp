from flask import Flask, jsonify, request, render_template, redirect, send_file
from flask_socketio import SocketIO, emit, disconnect
import gevent
import os
from dotenv import load_dotenv
load_dotenv()
import secrets

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
socketio = SocketIO(app, async_mode='gevent')
port = int( os.getenv('PORT', '9000') )

#SERVIDOR INICIADO 
print(f"SERVIDOR INICIADO EN PUERTO: {port}")


txt = ''
ult_arch = ''

def cargar_nombre():
    global ult_arch
    try:


        with open('uploads/info.txt', 'r') as f:
            ult_arch = f.read()
    except FileNotFoundError:
        ult_arch = ""
        with open('uploads/info.txt', "w") as f:
            f.write("")




cargar_nombre()

def verificar_video():
    cargar_nombre()
    if '.mp4' in ult_arch:
        return True
    else:
        return False

def verificar_imagen():
    cargar_nombre()
    if '.png' in ult_arch or '.jpg' in ult_arch:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=["POST"])
def upload():
    archivo = request.files['archivo']
    archivo.save('uploads/ultimo')
    with open('uploads/info.txt','w') as f:
        f.write(archivo.filename )
    cargar_nombre()
    socketio.emit('ult_archivo',ult_arch)
    return jsonify({'ok':True})

@app.route('/download', methods=['GET'])
def download():
    return send_file('uploads/ultimo', download_name=ult_arch, as_attachment=True)

@app.route('/video',methods=['GET'])
def video():
    if '.mp4' in ult_arch:
        print("es un video")
        return send_file('uploads/ultimo', download_name=ult_arch, as_attachment=True)
    else:
        print("No es un video")
        return '404'

@app.route('/imagen', methods=['GET'])
def imagen():
    if '.jpg' in ult_arch or '.png' in ult_arch:
        return send_file('uploads/ultimo', download_name=ult_arch, as_attachment=True)
    else:
        return '404'

# -------------------------------------------------------------------|
def tipo_de_archivo(archivo):
    formats = {
            'video': ['mp4','avi'],
            'imagen': ['png', 'jpg', 'jepg'],
            'sonido': ['mp3']
            }
    for types in formats: # Itera sobre todos los tipos de archivos
        for frmts in formats[types]: # itera por cada formato
            if frmts in archivo: # Si un formato coincide con alguno
                return types # retorna el tipo



#--------------------------------------------------------------------|
def enviar_archivo(archivo):
    tipo = tipo_de_archivo(archivo)
    socketio.emit('cargar_archivo',{'tipo': tipo, 'ruta': f'/{tipo}'})


# -------------------------------------------------------------------|

@socketio.on('verific_video')
def verific_video():
    emit("video", verificar_video(),broadcast=True)

@socketio.on('verific_imagen')
def verific_imagen():
    emit('imagen',verificar_imagen(),broadcast=True)

@socketio.on('txt_change')
def handle_txtChange(data):
    global txt
    txt = data
    emit("txt_recive",data, broadcast=True)
    enviar_archivo(ult_arch)

@socketio.on('connect')
def handle_connect():
    cargar_nombre()
    emit('ult_archivo', ult_arch)
    emit('txt_recive', txt)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=False, port=9000)
