import flet as ft
from conexion import conectar
from crud import vista_crud
import bcrypt


def vista_login(page: ft.Page):

    txt_usuario = ft.TextField(label="Usuario")
    txt_password = ft.TextField(label="Contraseña", password=True)

    lbl_error = ft.Text(color="red")

    def autenticar(e):

        try:
            db = conectar()

            if db is None:
                lbl_error.value = "Sin conexión a BD"
                page.update()
                return

            cursor = db.cursor()

            cursor.execute(
                "SELECT password FROM usuarios WHERE usuario=%s",
                (txt_usuario.value,)
            )

            resultado = cursor.fetchone()

            if not resultado:
                lbl_error.value = "Usuario no existe"
                page.update()
                return

            password_bd = resultado[0].encode("utf-8")

            if bcrypt.checkpw(txt_password.value.encode("utf-8"), password_bd):

                print("LOGIN OK")

                page.clean()
                page.add(vista_crud(page))
                page.update()

            else:
                lbl_error.value = "Contraseña incorrecta"

        except Exception as e:
            lbl_error.value = f"Error: {e}"
            print("LOGIN ERROR:", e)

        finally:
            try:
                cursor.close()
                db.close()
            except:
                pass

        page.update()

    return ft.Container(
        # ✅ FIX IMPORTANTE (NO center en minúscula)
        alignment=ft.Alignment.CENTER,

        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text("LOGIN", size=30),

                txt_usuario,
                txt_password,

                ft.ElevatedButton(
                    "Ingresar",
                    on_click=autenticar
                ),

                lbl_error
            ]
        )
    )