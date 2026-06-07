from conexion import conectar

print("Intentando conectar a la base de datos...")
db = conectar()

if db:
    print("¡CONEXIÓN EXITOSA! Python y HeidiSQL ya están hablando el mismo idioma.")
    db.close()
else:
    print("❌ ERROR: No se pudo conectar. Revisa tu contraseña en conexion.py o que tu servidor MySQL esté encendido.")