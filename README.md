Proyecto: Sistema de Control Escolar - UV

Requisitos:
- Python 3.8+
- MySQL en localhost con la base `alumnado` configurada

Instalación:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ejecución:

- Probar conexión:

```bash
python probar_conexion.py
```

- Ejecutar aplicación (Flet):

```bash
python main.py
```

- Opcional: crear o restaurar el usuario administrador:

```bash
python crear_admin.py
```

Notas:
- `conexion.py` ahora inicializa la base `alumnado` y crea las tablas `usuarios` y `alumnos` si no existen.
- El usuario administrador por defecto es `admin` con contraseña `1234`.
- Ajusta los datos de conexión en `conexion.py` si usas contraseña o puerto distintos.
