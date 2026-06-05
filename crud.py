import flet as ft
from conexion import conectar


def vista_crud(page: ft.Page):

    # ================= CAMPOS =================
    txt_matricula = ft.TextField(label="Matrícula")
    txt_ap_pat = ft.TextField(label="Apellido Paterno")
    txt_ap_mat = ft.TextField(label="Apellido Materno")
    txt_nombre = ft.TextField(label="Nombre(s)")
    txt_curp = ft.TextField(label="CURP")
    txt_especialidad = ft.TextField(label="Especialidad")
    txt_telefono = ft.TextField(label="Teléfono")
    txt_ciudad = ft.TextField(label="Ciudad")

    txt_buscar = ft.TextField(label="Buscar alumno")

    mensaje = ft.Text(color="red")

    # ================= TABLA =================
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Matrícula")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("CURP")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    # ================= LIMPIAR =================
    def limpiar(e=None):
        txt_matricula.value = ""
        txt_ap_pat.value = ""
        txt_ap_mat.value = ""
        txt_nombre.value = ""
        txt_curp.value = ""
        txt_especialidad.value = ""
        txt_telefono.value = ""
        txt_ciudad.value = ""
        page.update()

    # ================= CARGAR =================
    def cargar_datos(filtro=""):

        try:
            tabla.rows.clear()

            db = conectar()
            if db is None:
                mensaje.value = "Sin conexión a BD"
                page.update()
                return

            cursor = db.cursor()

            if filtro:
                cursor.execute("""
                    SELECT matricula, nombres, curp
                    FROM alumnos
                    WHERE matricula LIKE %s OR nombres LIKE %s
                """, (f"%{filtro}%", f"%{filtro}%"))
            else:
                cursor.execute("SELECT matricula, nombres, curp FROM alumnos")

            for fila in cursor.fetchall():

                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(fila[0]))),
                            ft.DataCell(ft.Text(str(fila[1]))),
                            ft.DataCell(ft.Text(str(fila[2]))),

                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        icon_color="blue",
                                        on_click=lambda e, m=fila[0]: editar(m)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color="red",
                                        on_click=lambda e, m=fila[0]: confirmar_eliminar(m)
                                    ),
                                ])
                            )
                        ]
                    )
                )

        except Exception as e:
            mensaje.value = f"Error: {e}"
            print("ERROR:", e)

        finally:
            try:
                cursor.close()
                db.close()
            except:
                pass

        page.update()

    # ================= GUARDAR =================
    def guardar(e):

        if txt_matricula.value == "":
            mensaje.value = "Matrícula requerida"
            page.update()
            return

        try:
            db = conectar()
            if db is None:
                mensaje.value = "Sin conexión"
                page.update()
                return

            cursor = db.cursor()

            cursor.execute("""
                INSERT INTO alumnos VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                txt_matricula.value,
                txt_ap_pat.value,
                txt_ap_mat.value,
                txt_nombre.value,
                txt_curp.value,
                txt_especialidad.value,
                txt_telefono.value,
                txt_ciudad.value
            ))

            db.commit()

            mensaje.value = "✔ Alumno guardado"
            limpiar()
            cargar_datos()

        except Exception as e:
            mensaje.value = f"Error: {e}"

        finally:
            try:
                cursor.close()
                db.close()
            except:
                pass

        page.update()

    # ================= EDITAR =================
    def editar(matricula):

        db = conectar()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM alumnos WHERE matricula=%s", (matricula,))
        fila = cursor.fetchone()

        if fila:
            txt_matricula.value = fila[0]
            txt_ap_pat.value = fila[1]
            txt_ap_mat.value = fila[2]
            txt_nombre.value = fila[3]
            txt_curp.value = fila[4]
            txt_especialidad.value = fila[5]
            txt_telefono.value = fila[6]
            txt_ciudad.value = fila[7]

        page.update()

    # ================= ELIMINAR CON CONFIRMACIÓN =================
    def confirmar_eliminar(matricula):

        def eliminar(e):

            db = conectar()
            cursor = db.cursor()

            cursor.execute("DELETE FROM alumnos WHERE matricula=%s", (matricula,))
            db.commit()

            mensaje.value = "✔ Eliminado"
            dialog.open = False
            cargar_datos()

            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text("¿Seguro que quieres eliminar este alumno?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close()),
                ft.TextButton("Eliminar", on_click=eliminar),
            ]
        )

        def close():
            dialog.open = False
            page.update()

        page.dialog = dialog
        dialog.open = True
        page.update()

    # ================= UI =================
    cargar_datos()

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[

            ft.Text("CRUD ALUMNOS PRO", size=25),

            txt_buscar,
            ft.ElevatedButton("Buscar", on_click=lambda e: cargar_datos(txt_buscar.value)),

            ft.Row([
                txt_matricula,
                txt_nombre
            ]),

            txt_ap_pat,
            txt_ap_mat,
            txt_curp,
            txt_especialidad,
            txt_telefono,
            txt_ciudad,

            ft.Row([
                ft.ElevatedButton("Guardar", on_click=guardar),
                ft.ElevatedButton("Limpiar", on_click=limpiar),
            ]),

            mensaje,

            ft.Divider(),

            tabla
        ]
    )