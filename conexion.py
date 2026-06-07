import bcrypt
import mysql.connector
from datetime import datetime
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "alumnado"
}


def conectar(allow_create_db: bool = False):
    try:
        config = DB_CONFIG.copy()
        if allow_create_db:
            config.pop("database", None)

        conexion = mysql.connector.connect(**config)
        if conexion.is_connected():
            return conexion
        return None
    except Error as e:
        print("❌ Error BD:", e)
        return None


def table_columns(cursor, table_name: str):
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]


def rename_table(cursor, old_name: str, new_name: str):
    cursor.execute(f"RENAME TABLE {old_name} TO {new_name}")


def inicializar_bd():
    db = conectar(allow_create_db=True)
    if db is None:
        return False

    cursor = db.cursor()
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS alumnado CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        db.commit()
        return True
    except Error as e:
        print("❌ Error al crear la base de datos:", e)
        return False
    finally:
        cursor.close()
        db.close()


def asegurar_tablas():
    if not inicializar_bd():
        return False

    db = conectar()
    if db is None:
        return False

    cursor = db.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        )

        cursor.execute("SHOW TABLES LIKE 'alumnos'")
        table_exists = cursor.fetchone() is not None

        expected_columns = {
            "matricula",
            "apellido_paterno",
            "apellido_materno",
            "nombres",
            "curp",
            "especialidad",
            "telefono",
            "ciudad_origen",
            "estado",
            "disciplina",
            "foto",
        }
        if table_exists:
            columns = set(table_columns(cursor, "alumnos"))
            if not expected_columns.issubset(columns):
                backup_name = "alumnos_backup"
                suffix = 1
                while True:
                    cursor.execute("SHOW TABLES LIKE %s", (backup_name,))
                    if cursor.fetchone() is None:
                        break
                    suffix += 1
                    backup_name = f"alumnos_backup_{suffix}"

                rename_table(cursor, "alumnos", backup_name)
                print(f"⚠ Tabla existente `alumnos` renombrada a `{backup_name}` por esquema incompatible.")
                table_exists = False

        if not table_exists:
            cursor.execute(
                """
                CREATE TABLE alumnos (
                    matricula VARCHAR(20) PRIMARY KEY,
                    apellido_paterno VARCHAR(50) NOT NULL,
                    apellido_materno VARCHAR(50),
                    nombres VARCHAR(100) NOT NULL,
                    curp CHAR(18) NOT NULL,
                    especialidad VARCHAR(100),
                    telefono CHAR(10),
                    ciudad_origen VARCHAR(100),
                    estado VARCHAR(50),
                    disciplina VARCHAR(255),
                    foto VARCHAR(255)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            db.commit()

        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = %s", ("admin",))
        result = cursor.fetchone()
        if result and result[0] == 0:
            password_hash = bcrypt.hashpw(
                "1234".encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
            cursor.execute(
                "INSERT INTO usuarios(usuario,password) VALUES(%s,%s)",
                ("admin", password_hash)
            )
            db.commit()
            print("✔ Usuario admin creado con contraseña 1234")

        return True
    except Error as e:
        print("❌ Error al asegurar tablas:", e)
        return False
    finally:
        cursor.close()
        db.close()
