import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent.parent / 'database' / 'database.db'
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            imagen TEXT NOT NULL
            )"""
            )
    conn.commit()
    conn.close()
create_table()

def create_user(nombre,password,endpoint,imagen):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (nombre,password,endpoint,imagen) VALUES (?,?,?,?)",
                   (nombre,password,endpoint,imagen)
                   )
    conn.commit()
    conn.close()



def change(value,nombre,nvalue):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {value} = ? WHERE nombre = ?",
                   (nvalue,nombre)
                   )
    conn.commit()
    conn.close()

def get_endpoint(endpoint,nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS (SELECT 1 FROM users WHERE nombre = ? AND endpoint = ?)",
                   (nombre,endpoint)
                   )
    resultado = cursor.fetchone()[0]
    conn.close()
    if resultado:
        return 'Si es su endpoint'
    else:
        return 'No es su endpoint'

def get_all_endpoints():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT endpoint FROM users")
    resultado = cursor.fetchall()
    conn.close()
    lista = []
    for end in resultado:
        if end[0] != 'none':
            lista.append(end[0])
    return lista

def del_user(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE nombre = ?",
                   (nombre)
                   )
    conn.commit()
    conn.close()


