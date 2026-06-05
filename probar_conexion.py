import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="alumnado"
        )
        return conexion
    except Exception as e:
        print("Error de conexión:", e)
        return Nones