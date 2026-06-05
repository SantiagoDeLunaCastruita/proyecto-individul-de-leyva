import bcrypt
from conexion import conectar

usuario = "admin"
password = "1234"

db = conectar()

cursor = db.cursor(dictionary=True)

cursor.execute(
    "SELECT * FROM usuarios WHERE usuario=%s",
    (usuario,)
)

dato = cursor.fetchone()

print("Usuario encontrado:")
print(dato)

if dato:

    password_guardada = dato["password"]

    if isinstance(password_guardada, str):
        password_guardada = password_guardada.encode("utf-8")

    resultado = bcrypt.checkpw(
        password.encode("utf-8"),
        password_guardada
    )

    print("Resultado bcrypt:", resultado)

cursor.close()
db.close()