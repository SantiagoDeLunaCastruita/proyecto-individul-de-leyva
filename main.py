import asyncio
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
        asyncio.create_task(page.push_route(top_view.route))

    page.on_route_change = ruta_cambiada
    page.on_view_pop = ir_atras
    
    ruta_cambiada(page.route or "/")


ft.run(main)
# Y si las noches fueran más largas y más largo el fin de semana
# Si tuviera más vacaciones ¿qué estuviera haciendo entonces?
# Perdón por no salir de la rutina, ya me extrañan en la cantina
# Pero no, pero no, no sé qué pasa
# No me dejan hacer todas las cosas que me gustan hacer
# No me interesa si no me dejan hacer todas las cosas que me gustan hacer
# Trabajar, trabajar, trabajar, trabajar, trabajar
# Ya no quiero trabajar, trabajar, trabajar, trabajar, trabajar, trabajar
# Solo quiero escapar
# Y si mañana no despiertas, es que la muerte tocó a tu puerta
# Y si mañana no regresas, mejor allá te quedas
# Mejor allá, mejor allá, mejor allá todo olvidarlo de vez en cuando
# Porque la vida se está acabando
# Pero no, no sé qué pasa
# No me dejan hacer todas las cosas que me gustan hacer
# No me interesa si no me dejan hacer todas las cosas que me gustan hacer
# Morirán, morirán, morirán, morirán, morirán, todos morirán
# Morirán, morirán, morirán, morirán, morirán, todos morirán
# Sabes descansar, quieres de seguro ocupado desde hace mucho tiempo
# Alteración de la respiración sin control en lo que siento
# Necesitas tiempo pero no te dejan descansar
# Disfrutar para sentir la libertad