import flet as ft
from login import vista_login
from crud import vista_crud
import flet as ft
from login import vista_login
from crud import vista_crud

def main(page: ft.Page):
    page.title = "Sistema de Control Escolar - UV"
    page.window_width = 1100
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.LIGHT

    def ruta_cambiada(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(vista_login(page))
        elif page.route == "/crud":
            page.views.append(vista_crud(page))
            
        page.update()

    def ir_atras(view):
        page.views.pop()
        top_view = page.views[-1]
        page.push_route(top_view.route)

    page.on_route_change = ruta_cambiada
    page.on_view_pop = ir_atras
    
    # Método moderno para arrancar la app en la raíz
    page.push_route("/")

if __name__ == "__main__":
    # Método moderno de arranque que exige Flet 0.85+
    ft.run(main)