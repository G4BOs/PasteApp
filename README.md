## INSTALACIÓN DE ENTORNO
- `python3 -m venv .venv`
- `source .venv/bin/activate` *O en Fish* `...activate.fish`
- `pip install -r requirements.txt`

## OBTENER PUBLIC KEY PARA CLIENTE JS
`vapid --applicationServerKey`

## Crear entorno virtual *.env*
### */.env*
HTTPS=true *false si no activaste mkcert*
HOST='0.0.0.0'
PORT=9000 *O el puerto que vas a usar*
SECRET_KEY=tu_secret_key_para_flask
PUBLIC_KEY=ruta_de_tu_public_key.pem
PRIVATE_KEY=ruta_de_tu_private_key.pem
SSL_CERTFILE=ruta_de_tu_certfile.pem
SSL_CERTFILE_key=ruta_de_tu_certfile_key.pem

## SERVIR 
`python app.py`
