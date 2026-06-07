import asyncio
import flet as ft
import bcrypt
from conexion import conectar, asegurar_tablas


def vista_login(page: ft.Page):
    txt_usuario = ft.TextField(label="Usuario", icon=ft.icons.Icons.PERSON, width=300)
    txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, icon=ft.icons.Icons.LOCK, width=300)
    lbl_error = ft.Text(value="", color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD)

    def autenticar(e):
        lbl_error.value = ""
        page.update()

        if not txt_usuario.value or not txt_password.value:
            lbl_error.value = "Por favor, llena todos los campos."
            page.update()
            return

        if not asegurar_tablas():
            lbl_error.value = "Error al preparar la base de datos."
            page.update()
            return

        db = conectar()
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
                    asyncio.create_task(page.push_route("/crud"))
                else:
                    lbl_error.value = "Usuario o contraseña incorrectos."
            else:
                lbl_error.value = "Usuario o contraseña incorrectos."
        except Exception as ex:
            lbl_error.value = f"Error en el sistema: {ex}"
        finally:
            try:
                if cursor:
                    cursor.close()
            except Exception:
                pass
            try:
                if db:
                    db.close()
            except Exception:
                pass

        page.update()

    return ft.View(
        route="/",
        controls=[
            ft.AppBar(
                title=ft.Text("Control de Acceso - UV"),
                bgcolor=ft.Colors.BLUE_GREY_800,
                color=ft.Colors.WHITE,
                center_title=True
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.Icons.ACCOUNT_CIRCLE, size=90, color=ft.Colors.BLUE_700),
                        ft.Text("Iniciar Sesión", size=26, weight=ft.FontWeight.BOLD),
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
                    spacing=20
                ),
                alignment=ft.Alignment.CENTER,
                margin=ft.Margin.only(top=60)
            )
        ]
    )
