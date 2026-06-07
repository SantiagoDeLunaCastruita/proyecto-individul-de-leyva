import asyncio
import flet as ft
from conexion import conectar

STATES = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
    "Coahuila", "Colima", "Chiapas", "Chihuahua", "Ciudad de México",
    "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México",
    "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
    "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora",
    "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]

DISCIPLINES = [
    "Fútbol", "Básquetbol", "Natación", "Atletismo", "Voleibol", "Taekwondo"
]


def obtener_alumnos(filtro: str = ""):
    db = conectar()
    if db is None:
        return []

    cursor = db.cursor(dictionary=True)
    try:
        if filtro:
            filtro_like = f"%{filtro}%"
            cursor.execute(
                """
                SELECT matricula, apellido_paterno, apellido_materno, nombres, curp,
                        especialidad, telefono, ciudad_origen, estado, disciplina, foto
                FROM alumnos
                WHERE matricula LIKE %s
                    OR apellido_paterno LIKE %s
                    OR apellido_materno LIKE %s
                    OR nombres LIKE %s
                ORDER BY matricula
                """,
                (filtro_like, filtro_like, filtro_like, filtro_like)
            )
        else:
            cursor.execute(
                """
                SELECT matricula, apellido_paterno, apellido_materno, nombres, curp,
                            especialidad, telefono, ciudad_origen, estado, disciplina, foto
                FROM alumnos
                ORDER BY matricula
                """
            )
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        cursor.close()
        db.close()


def ejecutar_sql(query: str, params: tuple = ()) -> tuple[bool, str]:
    db = conectar()
    if db is None:
        return False, "Error de conexión con la base de datos."

    cursor = db.cursor()
    try:
        cursor.execute(query, params)
        db.commit()
        return True, ""
    except Exception as ex:
        return False, str(ex)
    finally:
        cursor.close()
        db.close()


def vista_crud(page: ft.Page):
    selected_matricula = None
    txt_matricula = ft.TextField(label="Matrícula", width=300)
    txt_apellido_paterno = ft.TextField(label="Apellido paterno", width=300)
    txt_apellido_materno = ft.TextField(label="Apellido materno", width=300)
    txt_nombres = ft.TextField(label="Nombre(s)", width=300)
    txt_curp = ft.TextField(label="CURP", width=300)
    txt_especialidad = ft.TextField(label="Especialidad", width=300)
    txt_telefono = ft.TextField(label="Teléfono", width=300)
    txt_ciudad_origen = ft.TextField(label="Ciudad de origen", width=300)
    ddl_estado = ft.Dropdown(
        label="Estado",
        width=300,
        options=[ft.dropdown.Option(s) for s in STATES],
        value=STATES[0]
    )
    ddl_disciplina = ft.Dropdown(
        label="Disciplina",
        width=300,
        options=[ft.dropdown.Option(d) for d in DISCIPLINES],
        value=DISCIPLINES[0]
    )
    txt_foto = ft.TextField(label="Foto (ruta local)", width=300)
    txt_buscar = ft.TextField(label="Buscar por matrícula o apellido", width=720)
    lbl_mensaje = ft.Text(value="", color=ft.Colors.RED_700)
    detalles_panel = ft.Column(controls=[ft.Text("Detalles", size=16, weight=ft.FontWeight.BOLD), ft.Text("No hay alumno seleccionado.")])

    # Mostrar sólo las columnas principales para evitar solapamiento en pantallas pequeñas.
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Matrícula")),
            ft.DataColumn(ft.Text("Nombre(s)")),
            ft.DataColumn(ft.Text("Apellido paterno")),
            ft.DataColumn(ft.Text("Apellido materno")),
            ft.DataColumn(ft.Text("CURP")),
            ft.DataColumn(ft.Text("Especialidad")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Ciudad")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Disciplina")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        column_spacing=30,
        vertical_lines=ft.BorderSide.none(),
        heading_row_color=ft.Colors.BLUE_100,
        width=1400,
        height=420,
        expand=1,
    )

    def actualizar_tabla(filtro: str = ""):
        alumnos = obtener_alumnos(filtro)
        rows = []
        for alumno in alumnos:
            # Crear celdas con on_tap para garantizar selección al hacer clic
            cells = [
                ft.DataCell(ft.Text(alumno["matricula"]), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno["nombres"]), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno["apellido_paterno"]), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno["apellido_materno"] or ""), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno.get("curp","") or ""), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno.get("especialidad","") or ""), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno.get("telefono","") or ""), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno.get("ciudad_origen","") or ""), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno.get("estado","") or ""), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
                ft.DataCell(ft.Text(alumno.get("disciplina","") or ""), on_tap=lambda e, a=alumno: seleccionar_alumno(a)),
            ]

            # Botones de acción independientes que actúan directamente sobre la matrícula
            acciones = ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.Icons.EDIT, tooltip="Editar", on_click=lambda e, a=alumno: seleccionar_alumno(a)),
                    ft.IconButton(icon=ft.icons.Icons.DELETE, tooltip="Eliminar", on_click=lambda e, m=alumno["matricula"]: eliminar_alumno_por_matricula(m)),
                ],
                spacing=6,
            )
            # Añadir celda de acciones
            cells.append(ft.DataCell(acciones))
            rows.append(
                ft.DataRow(
                    selected=alumno["matricula"] == selected_matricula,
                    cells=cells,
                    on_select_change=lambda e, a=alumno: seleccionar_alumno(a),
                )
            )
        table.rows = rows
        page.update()

    def limpiar_formulario():
        nonlocal selected_matricula
        selected_matricula = None
        txt_matricula.value = ""
        txt_apellido_paterno.value = ""
        txt_apellido_materno.value = ""
        txt_nombres.value = ""
        txt_curp.value = ""
        txt_especialidad.value = ""
        txt_telefono.value = ""
        txt_ciudad_origen.value = ""
        ddl_estado.value = STATES[0]
        ddl_disciplina.value = DISCIPLINES[0]
        txt_foto.value = ""
        lbl_mensaje.value = ""
        page.update()

    def seleccionar_alumno(alumno: dict):
        nonlocal selected_matricula
        selected_matricula = alumno["matricula"]
        txt_matricula.value = alumno["matricula"]
        txt_apellido_paterno.value = alumno["apellido_paterno"]
        txt_apellido_materno.value = alumno["apellido_materno"] or ""
        txt_nombres.value = alumno["nombres"]
        txt_curp.value = alumno["curp"]
        txt_especialidad.value = alumno["especialidad"] or ""
        txt_telefono.value = alumno["telefono"] or ""
        txt_ciudad_origen.value = alumno["ciudad_origen"] or ""
        ddl_estado.value = alumno["estado"] or STATES[0]
        ddl_disciplina.value = alumno["disciplina"] or DISCIPLINES[0]
        txt_foto.value = alumno["foto"] or ""
        lbl_mensaje.value = f"Alumno seleccionado: {alumno['nombres']} {alumno['apellido_paterno']}"
        # Actualizar panel de detalles con CURP, teléfono y ciudad
        detalles_panel.controls.clear()
        detalles_panel.controls.append(ft.Text("Detalles", size=16, weight=ft.FontWeight.BOLD))
        detalles_panel.controls.append(ft.Text(f"CURP: {alumno.get('curp','')}"))
        detalles_panel.controls.append(ft.Text(f"Teléfono: {alumno.get('telefono','') or ''}"))
        detalles_panel.controls.append(ft.Text(f"Ciudad: {alumno.get('ciudad_origen','') or ''}"))
        page.update()

    def validar_curp(curp: str) -> bool:
        return len(curp.strip()) == 18

    def validar_telefono(telefono: str) -> bool:
        return telefono.isdigit() and len(telefono) == 10

    def guardar_alumno(e):
        nonlocal selected_matricula
        lbl_mensaje.value = ""

        if not txt_matricula.value.strip():
            lbl_mensaje.value = "La matrícula es obligatoria."
            page.update()
            return
        if not txt_apellido_paterno.value.strip() or not txt_nombres.value.strip():
            lbl_mensaje.value = "Apellido paterno y nombre son obligatorios."
            page.update()
            return
        if not validar_curp(txt_curp.value):
            lbl_mensaje.value = "CURP debe tener 18 caracteres."
            page.update()
            return
        if txt_telefono.value.strip() and not validar_telefono(txt_telefono.value):
            lbl_mensaje.value = "Teléfono debe tener 10 dígitos."
            page.update()
            return

        curp_value = txt_curp.value.strip().upper()
        success, error = ejecutar_sql(
            "INSERT INTO alumnos(matricula, apellido_paterno, apellido_materno, nombres, curp, especialidad, telefono, ciudad_origen, estado, disciplina, foto) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                txt_matricula.value.strip(),
                txt_apellido_paterno.value.strip(),
                txt_apellido_materno.value.strip() or None,
                txt_nombres.value.strip(),
                curp_value,
                txt_especialidad.value.strip() or None,
                txt_telefono.value.strip() or None,
                txt_ciudad_origen.value.strip() or None,
                ddl_estado.value,
                ddl_disciplina.value,
                txt_foto.value.strip() or None,
            )
        )

        if not success:
            lbl_mensaje.value = f"Error al guardar: {error}"
            page.update()
        else:
            lbl_mensaje.value = "Alumno guardado correctamente."
            limpiar_formulario()
            actualizar_tabla()

    def actualizar_alumno(e):
        if selected_matricula is None:
            lbl_mensaje.value = "Selecciona un alumno antes de actualizar."
            page.update()
            return
        if not txt_apellido_paterno.value.strip() or not txt_nombres.value.strip():
            lbl_mensaje.value = "Apellido paterno y nombre son obligatorios."
            page.update()
            return
        if not validar_curp(txt_curp.value):
            lbl_mensaje.value = "CURP debe tener 18 caracteres."
            page.update()
            return
        if txt_telefono.value.strip() and not validar_telefono(txt_telefono.value):
            lbl_mensaje.value = "Teléfono debe tener 10 dígitos."
            page.update()
            return

        curp_value = txt_curp.value.strip().upper()
        success, error = ejecutar_sql(
            "UPDATE alumnos SET apellido_paterno=%s, apellido_materno=%s, nombres=%s, curp=%s, especialidad=%s, telefono=%s, ciudad_origen=%s, estado=%s, disciplina=%s, foto=%s WHERE matricula=%s",
            (
                txt_apellido_paterno.value.strip(),
                txt_apellido_materno.value.strip() or None,
                txt_nombres.value.strip(),
                curp_value,
                txt_especialidad.value.strip() or None,
                txt_telefono.value.strip() or None,
                txt_ciudad_origen.value.strip() or None,
                ddl_estado.value,
                ddl_disciplina.value,
                txt_foto.value.strip() or None,
                selected_matricula,
            )
        )

        if not success:
            lbl_mensaje.value = f"Error al actualizar: {error}"
            page.update()
        else:
            lbl_mensaje.value = "Alumno actualizado correctamente."
            limpiar_formulario()
            actualizar_tabla()

    def confirmar_eliminar(e):
        if selected_matricula is None:
            lbl_mensaje.value = "Selecciona un alumno antes de eliminar."
            page.update()
            return

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Deseas eliminar este alumno?") ,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialog(e)),
                ft.ElevatedButton("Eliminar", on_click=lambda e: eliminar_alumno(e, dialog)),
            ],
            modal=True,
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def cerrar_dialog(e):
        page.dialog.open = False
        page.update()

    def eliminar_alumno(e, dialog=None):
        nonlocal selected_matricula
        if selected_matricula is None:
            lbl_mensaje.value = "Selecciona un alumno antes de eliminar."
            page.update()
            return
        # Delegar eliminación a la función por matrícula
        eliminar_alumno_por_matricula(selected_matricula, dialog)

    def buscar_alumnos(e):
        actualizar_tabla(txt_buscar.value.strip())

    def reset_busqueda(e):
        txt_buscar.value = ""
        actualizar_tabla()

    actualizar_tabla()

    def eliminar_alumno_por_matricula(matricula: str, dialog: ft.AlertDialog | None = None):
        nonlocal selected_matricula
        if not matricula:
            lbl_mensaje.value = "Matrícula inválida para eliminar."
            page.update()
            return

        success, error = ejecutar_sql(
            "DELETE FROM alumnos WHERE matricula=%s",
            (matricula,)
        )

        if dialog is not None:
            try:
                dialog.open = False
            except Exception:
                pass

        if not success:
            lbl_mensaje.value = f"Error al eliminar: {error}"
        else:
            lbl_mensaje.value = "Alumno eliminado correctamente."
            if selected_matricula == matricula:
                limpiar_formulario()
            actualizar_tabla()
        page.update()

    formulario = ft.Column(
        controls=[
            ft.Text("Registro de Alumnos", size=22, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Datos de identificación", size=18, weight=ft.FontWeight.BOLD),
                        txt_matricula,
                        txt_apellido_paterno,
                        txt_apellido_materno,
                        txt_nombres,
                        txt_curp,
                    ],
                    spacing=10,
                ),
                padding=16,
                border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                border_radius=10,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Datos de contacto", size=18, weight=ft.FontWeight.BOLD),
                        txt_telefono,
                        txt_ciudad_origen,
                        ddl_estado,
                    ],
                    spacing=10,
                ),
                padding=16,
                border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                border_radius=10,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Datos académicos", size=18, weight=ft.FontWeight.BOLD),
                        txt_especialidad,
                        ddl_disciplina,
                        txt_foto,
                    ],
                    spacing=10,
                ),
                padding=16,
                border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                border_radius=10,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton("Guardar", on_click=guardar_alumno, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Actualizar", on_click=actualizar_alumno, bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Eliminar", on_click=confirmar_eliminar, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Nuevo", on_click=lambda e: limpiar_formulario(), bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                ],
                spacing=10,
            ),
            lbl_mensaje,
        ],
        spacing=16,
        width=340,
    )

    return ft.View(
        route="/crud",
        controls=[
            ft.AppBar(
                title=ft.Text("Panel CRUD Alumnos"),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                actions=[
                    ft.ElevatedButton("Cerrar sesión", on_click=lambda e: asyncio.create_task(page.push_route("/")), bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
                ]
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            txt_buscar,
                            ft.ElevatedButton("Buscar", on_click=buscar_alumnos, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
                            ft.ElevatedButton("Reset", on_click=reset_busqueda, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    ft.Row(
                        controls=[
                            formulario,
                            ft.Container(width=20),
                            ft.Column(
                                controls=[
                                    ft.Text("Lista de alumnos", size=22, weight=ft.FontWeight.BOLD),
                                    ft.Row(controls=[table], scroll=ft.ScrollMode.AUTO, height=440),
                                    detalles_panel,
                                ],
                                spacing=10,
                                expand=True,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=20,
                        expand=True,
                    )
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        ]
    )