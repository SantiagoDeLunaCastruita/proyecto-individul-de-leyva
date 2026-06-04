import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Contraseña vacía como la última prueba exitosa
            database="alumnado"
        )
        # Devolver la conexión directamente; el llamador decidirá qué hacer
        return conexion
    except Error as e:
                    password="",  # Contraseña vacía como la última prueba exitosa
                    database="alumnado"
                )
                # Devolver la conexión directamente; el llamador decidirá qué hacer
                return conexion