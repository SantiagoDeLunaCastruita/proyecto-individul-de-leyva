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

Notas:
- Ajusta los datos de conexión en `conexion.py` si usas contraseña o puerto distintos.
- Asegúrate de que la tabla `usuarios` tenga una columna `password` con hashes generados por `bcrypt`.
