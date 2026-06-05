import flet as ft
from login import vista_login


def main(page: ft.Page):

    page.title = "Sistema de Control Escolar"

    page.window_width = 1100
    page.window_height = 750

    # mostrar errores en consola
    def error(e):
        print("FLET ERROR:", e.data)

    page.on_error = error

    page.add(vista_login(page))


# ✅ IMPORTANTE: usar run() en tu versión
ft.run(main)