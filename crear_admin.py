import bcrypt
from conexion import conectar, asegurar_tablas


def main():
    if not asegurar_tablas():
        print("No se pudieron asegurar las tablas de la base de datos.")
        return

    db = conectar()
    if db is None:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE usuario = %s", ("admin",))

        password_hash = bcrypt.hashpw(
            "1234".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            "INSERT INTO usuarios(usuario,password) VALUES(%s,%s)",
            ("admin", password_hash)
        )

        db.commit()
        print("Usuario creado correctamente")
        print("Usuario: admin")
        print("Contraseña: 1234")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()