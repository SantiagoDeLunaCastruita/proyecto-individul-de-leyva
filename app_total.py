import flet as ft
import mysql.connector
from mysql.connector import Error
import bcrypt

# 1. FUNCIÓN DE CONEXIÓN
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="alumnado"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error de base de datos: {e}")
        return None

# 2. APLICACIÓN PRINCIPAL
def main(page: ft.Page):
    page.title = "Sistema de Control Escolar - UV"
    page.window_width = 1100
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Forzamos la alineación nativa de la página para centrar todo perfectamente
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # --- COMPONENTES VISUALES DEL LOGIN ---
    txt_usuario = ft.TextField(label="Usuario", icon="person", width=300)
    txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, icon="lock", width=300)
    lbl_error = ft.Text(value="", color=ft.Colors.RED_700, weight="bold")

    # --- LÓGICA DE AUTENTICACIÓN ---
    def autenticar(e):
        lbl_error.value = ""
        page.update()

        if not txt_usuario.value or not txt_password.value:
            lbl_error.value = "Por favor, llena todos los campos."
            page.update()
            return

        db = conectar_bd()
        if db is None:
            lbl_error.value = "Error de conexión con la base de datos."
            page.update()
            return

        cursor = None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (txt_usuario.value,))
            usuario_db = cursor.fetchone()

            if usuario_db:
                password_ingresada = txt_password.value.encode('utf-8')
                password_encriptada = usuario_db.get('password')

                if isinstance(password_encriptada, str):
                    password_encriptada = password_encriptada.encode('utf-8')

                if bcrypt.checkpw(password_ingresada, password_encriptada):
                    mostrar_pantalla_crud()
                else:
                    lbl_error.value = "Usuario o contraseña incorrectos."
            else:
                lbl_error.value = "Usuario o contraseña incorrectos."
        except Exception as ex:
            lbl_error.value = f"Error en el sistema: {ex}"
        finally:
            if cursor:
                try: cursor.close()
                except: pass
            if db:
                try: db.close()
                except: pass

        page.update()

    # --- CAMBIADORES DE VISTA ---
    def mostrar_pantalla_login():
        page.controls.clear()
        
        # Configuramos la barra superior
        page.appbar = ft.AppBar(
            title=ft.Text("Control de Acceso - UV"), 
            bgcolor=ft.Colors.BLUE_GREY_800, 
            color=ft.Colors.WHITE, 
            center_title=True
        )
        
        # Columna principal con el diseño del login
        formulario = ft.Column(
            controls=[
                ft.Icon("account_circle", size=90, color=ft.Colors.BLUE_700),
                ft.Text("Iniciar Sesión", size=26, weight="bold"),
                txt_usuario,
                txt_password,
                lbl_error,
                ft.ElevatedButton(
                    "Ingresar al Sistema", 
                    on_click=autenticar, 
                    bgcolor=ft.Colors.BLUE_700, 
                    color=ft.Colors.WHITE, 
                    width=220, 
                    height=45
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            tight=True  # Evita que la columna intente expandirse de más
        )
        
        # Agregamos directo a la página usando una fila contenedora simple
        page.add(
            ft.Row(
                controls=[formulario],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def mostrar_pantalla_crud():
        page.controls.clear()
        page.appbar = ft.AppBar(
            title=ft.Text("Panel CRUD Alumnos"), 
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE
        )
        page.add(
            ft.Row(
                controls=[
                    ft.Text("¡Lograste entrar al panel del CRUD!", size=30, color=ft.Colors.GREEN_700, weight="bold")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    # Arrancamos cargando la vista de login
    mostrar_pantalla_login()

if __name__ == "__main__":
    ft.run(main)