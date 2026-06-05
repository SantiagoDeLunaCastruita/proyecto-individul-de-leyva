import mysql.connector
from mysql.connector import Error


def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="alumnado"
        )

        if conexion.is_connected():
            print("✔ Conexión exitosa")
            return conexion

        return None

    except Error as e:
        print("❌ Error BD:", e)
        return None