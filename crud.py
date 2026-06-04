import flet as ft

def vista_crud(page: ft.Page):
    return ft.View(
        "/crud",
        controls=[
            ft.AppBar(title=ft.Text("Panel CRUD Alumnos"), bgcolor=ft.colors.BLUE_700),
            ft.Container(
                content=ft.Text("¡Lograste entrar al panel del CRUD!", size=30, color=ft.colors.GREEN_700),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )