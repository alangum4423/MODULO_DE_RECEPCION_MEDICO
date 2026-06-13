import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DOCTORES  = os.path.join(BASE_DIR, "doctores.json")
ARCHIVO_PACIENTES = os.path.join(BASE_DIR, "pacientes.json")
ARCHIVO_CITAS     = os.path.join(BASE_DIR, "citas.json")

def cargar_json(ruta, default):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                data = [item for item in data if item]
            return data
    return default

def guardar_json(ruta, data):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

pacientes_db  = cargar_json(ARCHIVO_PACIENTES, {})
citas         = cargar_json(ARCHIVO_CITAS, [])
especialidades = cargar_json(ARCHIVO_DOCTORES, {})

#COLORES
C = {
    "azul_oscuro": "#0067c0",
    "azul_medio":  "#1A4A7A",
    "azul_claro":  "#2563EB",
    "azul_hover":  "#1D4ED8",
    "acento":      "#38BDF8",
    "fondo":       "#d5e3ec",
    "blanco":      "#FFFFFF",
    "gris_claro":  "#E2E8F0",
    "gris_texto":  "#475569",
    "texto":       "#0F172A",
    "rojo":        "#EF4444",
    "verde":       "#22C55E",
    "amarillo":    "#F59E0B",
    "sidebar_btn": "#1E3A5F",
    "sidebar_act": "#2563EB",
}

FUENTES = {
    "titulo":    ("Segoe UI", 24, "bold"),
    "subtitulo": ("Segoe UI", 16, "bold"),
    "cuerpo":    ("Segoe UI", 11),
    "label":     ("Segoe UI", 10, "bold"),
    "pequeño":   ("Segoe UI", 9),
    "boton":     ("Segoe UI", 11, "bold"),
    "sidebar":   ("Segoe UI", 9, "bold"),
    "icono_sb":  ("Segoe UI Emoji", 18),
    "grande":    ("Segoe UI", 32, "bold"),
}

"""
A partir de aqui se inicia con el desarrollo del sistema.
Iniciando po r el contenedor principal Xd.
"""

class SistemaRecepcion:

    def __init__(self, window):
        self.window = window
        self.window.title("Sistema Médico — Hospital Obrero")
        self.window.geometry("1200x800+0+0")
        self.window.configure(bg=C["azul_oscuro"])
        self.window.resizable(True, True)
        self.window.minsize(960, 660)
        self.window.iconbitmap("hosp.ico")
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self._sidebar_btn_refs = {}
        self.vista_actual = None
        self._aplicar_estilos_ttk()
        self.mostrar_panel_recepcion()

    def _aplicar_estilos_ttk(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", bg=C["blanco"], fg=C["texto"], fieldbackground=C["blanco"], font=("Segoe UI", 10), rowheight=32)
        style.configure("Treeview.Heading", bg=C["azul_medio"], fg=C["blanco"], font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Treeview", bg=[("selected", C["azul_claro"])], fg=[("selected", C["blanco"])])
        style.map("Treeview.Heading", bg=[("active", C["azul_claro"])])
        style.configure("TCombobox", fieldbackground=C["fondo"], bg=C["blanco"],fg=C["texto"], arrowcolor=C["azul_claro"], padding=6)
        style.map("TCombobox", fieldbackground=[("readonly", C["fondo"])], selectbg=[("readonly", C["azul_claro"])])
        style.configure("Vertical.TScrollbar", bg=C["gris_claro"], troughcolor=C["fondo"], arrowcolor=C["gris_texto"],
            borderwidth=0)

    def guardar_pacientes(self):
        guardar_json(ARCHIVO_PACIENTES, pacientes_db)

    def guardar_citas(self):
        guardar_json(ARCHIVO_CITAS, citas)

    def limpiar(self):
        for w in self.window.winfo_children():
            w.destroy()
        self._sidebar_btn_refs = {}

    def _hover_in(self, btn, color):
        btn.configure(bg=color)

    def _hover_out(self, btn, color):
        btn.configure(bg=color)

#Barra de tareas (en proceso). Joseeeee cambias el color please
    def sidebar(self, vista_activa="inicio"):
        side = tk.Frame(self.window, bg=C["azul_oscuro"], width=220)
        side.grid(row=0, column=0, sticky="ns")
        side.grid_propagate(False)

        logo_frame = tk.Frame(side, bg=C["azul_oscuro"])
        logo_frame.pack(fill="x", pady=(30, 0))
        tk.Label(logo_frame, text="🏥", font=("Segoe UI Emoji", 40), bg=C["azul_oscuro"], fg=C["blanco"]).pack()
        tk.Label(logo_frame, text="HOSPITAL OBRERO", font=("Segoe UI", 9, "bold"), bg=C["azul_oscuro"], fg=C["acento"]).pack(pady=(4, 0))
        tk.Frame(side, bg=C["azul_medio"], height=1).pack(fill="x", padx=20, pady=20)

        nav_items = [
            ("inicio",      "🏠", "Inicio"),
            ("citas",       "📅", "Reservar Cita"),
            ("registro",    "👤", "Registrar Paciente"),
            ("enfermeria",  "🩺", "Enfermería"),
            ("agenda",      "📋", "Ver Agenda"),
        ]

        comandos = {
            "inicio":     self.mostrar_panel_recepcion,
            "citas":      self.vista_citas,
            "registro":   self.vista_registro,
            "enfermeria": self.vista_enfermeria,
            "agenda":     self.vista_agenda,
        }

        for key, icono, texto in nav_items:
            activo = (key == vista_activa)
            bg_btn = C["azul_claro"] if activo else C["azul_oscuro"]
            border_color = C["acento"] if activo else C["azul_oscuro"]

            row = tk.Frame(side, bg=border_color)
            row.pack(fill="x", pady=1)

            inner = tk.Frame(row, bg=bg_btn)
            inner.pack(fill="x", padx=(3, 0))

            btn_row = tk.Frame(inner, bg=bg_btn, cursor="hand2")
            btn_row.pack(fill="x", ipady=10, padx=14)

            tk.Label(btn_row, text=icono,
                     font=("Segoe UI Emoji", 14),
                     bg=bg_btn, fg=C["blanco"]).pack(side="left")
            tk.Label(btn_row, text=f"  {texto}",
                     font=("Segoe UI", 10, "bold") if activo else ("Segoe UI", 10),
                     bg=bg_btn, fg=C["blanco"]).pack(side="left")

            cmd = comandos[key]
            for w in (btn_row, *btn_row.winfo_children()):
                w.bind("<Button-1>", lambda e, c=cmd: c())
                if not activo:
                    w.bind("<Enter>", lambda e, f=btn_row, ic=inner: [
                        f.configure(bg=C["sidebar_btn"]),
                        ic.configure(bg=C["sidebar_btn"]),
                        [child.configure(bg=C["sidebar_btn"])
                         for child in f.winfo_children()]])
                    w.bind("<Leave>", lambda e, f=btn_row, ic=inner: [
                        f.configure(bg=C["azul_oscuro"]),
                        ic.configure(bg=C["azul_oscuro"]),
                        [child.configure(bg=C["azul_oscuro"])
                         for child in f.winfo_children()]])

        tk.Frame(side, bg=C["azul_medio"], height=1).pack(
            fill="x", padx=20, pady=20)

        salir_row = tk.Frame(side, bg=C["rojo"], cursor="hand2")
        salir_row.pack(fill="x", ipady=10, padx=14)
        tk.Label(salir_row, text="🚪", font=("Segoe UI Emoji", 14), bg=C["rojo"], fg=C["blanco"]).pack(side="left")
        tk.Label(salir_row, text="  Salir", font=("Segoe UI", 10), bg=C["rojo"], fg=C["blanco"]).pack(side="left")
        for w in (salir_row, *salir_row.winfo_children()):
            w.bind("<Button-1>", lambda e: self._confirmar_salir())

        tk.Label(side, text="v1.25.1.1.1  |  2026", font=("Segoe UI", 8), bg=C["azul_oscuro"], fg="#FFFFFF").pack(
            side="bottom", pady=12)

    def _confirmar_salir(self):
        if messagebox.askyesno("Salir", "¿Desea cerrar el sistema?",
                               icon="question"):
            self.window.quit()

    def _campo(self, parent, label):
        tk.Label(parent, text=label, font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w")
        e = tk.Entry(parent, font=FUENTES["cuerpo"], bg=C["fondo"], fg=C["texto"], relief="flat", bd=0, 
                     insertbackground=C["azul_claro"])
        e.pack(fill="x", pady=(4, 16), ipady=9)

        tk.Frame(parent, bg=C["gris_claro"], height=1).pack(fill="x", pady=(0, 8))

        def on_focus_in(ev):
            parent.winfo_children()[-1].configure(bg=C["azul_claro"])
        def on_focus_out(ev):
            parent.winfo_children()[-1].configure(bg=C["gris_claro"])

        e.bind("<FocusIn>", on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
        return e

    def _boton_primario(self, parent, texto, cmd, color=None):
        color = color or C["azul_claro"]
        btn = tk.Button(parent, text=texto, bg=color, fg=C["blanco"], font=FUENTES["boton"], relief="flat", bd=0, 
                        activebackground=C["azul_hover"], activeforeground=C["blanco"], cursor="hand2", command=cmd, padx=20, pady=12)
        btn.pack(fill="x", pady=(8, 0))
        btn.bind("<Enter>", lambda e: btn.configure(bg=C["azul_hover"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        return btn

    def _badge(self, parent, texto, color_bg, color_fg=C["blanco"]):
        tk.Label(parent, text=texto, bg=color_bg, fg=color_fg, font=("Segoe UI", 9, "bold"), padx=10, pady=3,
                 relief="flat").pack(side="left", padx=4)

    def _stat_card(self, parent, icono, numero, label, color_acento, col):
        card = tk.Frame(parent, bg=C["blanco"], pady=20, padx=20)
        card.grid(row=0, column=col, padx=8, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        top = tk.Frame(card, bg=C["blanco"])
        top.pack(fill="x")
        tk.Label(top, text=icono, font=("Segoe UI Emoji", 24), bg=C["blanco"], fg=color_acento).pack(side="left")

        tk.Label(card, text=str(numero), font=("Segoe UI", 28, "bold"), bg=C["blanco"], fg=C["texto"]).pack(anchor="w", pady=(8, 0))
        tk.Label(card, text=label, font=FUENTES["pequeño"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w")
        tk.Frame(card, bg=color_acento, height=3).pack(fill="x", side="bottom")

#El infierno de la Interfaz o Panel Principal. Si lo esta viendo, se aceptan criticas constructivas OJO
    def mostrar_panel_recepcion(self):
        self.limpiar()
        self.sidebar("inicio")

        main = tk.Frame(self.window, bg=C["azul_oscuro"], pady=5)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        header = tk.Frame(main, bg=C["blanco"], pady=24, padx=40)
        header.grid(row=0, column=0, sticky="ew")

        hora = datetime.now().strftime("%H:%M")
        fecha = datetime.now().strftime("%A, %d de %B de %Y").capitalize()

        saludo = "Buenos Días" if int(datetime.now().strftime("%H")) < 12 else \
                 "Buenas Tardes" if int(datetime.now().strftime("%H")) < 19 else \
                 "Buenas Noches"

        tk.Label(header, text=f"{saludo} 👋", font=("Segoe UI", 22, "bold"), bg=C["blanco"], fg=C["texto"]).pack(anchor="w")
        tk.Label(header, text=fecha, font=FUENTES["cuerpo"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w", pady=(2, 0))

        stats_frame = tk.Frame(main, bg=C["fondo"], pady=20, padx=30)
        stats_frame.grid(row=1, column=0, sticky="new")

        total_p   = len(pacientes_db)
        total_c   = len(citas)
        pendientes = len([c for c in citas if c.get("triaje") == "Pendiente"])
        atendidos  = total_c - pendientes

        self._stat_card(stats_frame, "👥", total_p,   "Pacientes Registrados", C["azul_claro"], 0)
        self._stat_card(stats_frame, "📅", total_c,   "Citas Totales",         C["acento"],     1)
        self._stat_card(stats_frame, "⏳", pendientes, "Pendientes de Triaje",  C["amarillo"],   2)
        self._stat_card(stats_frame, "✅", atendidos,  "Atendidos Hoy",         C["verde"],      3)

        grid_frame = tk.Frame(main, bg=C["fondo"], padx=30, pady=10)
        grid_frame.grid(row=2, column=0, sticky="nsew")
        main.grid_rowconfigure(2, weight=1)
        grid_frame.columnconfigure((0, 1, 2), weight=1)
        grid_frame.rowconfigure((0, 1), weight=1)

        tarjetas = [
            ("📅\nRESERVAR CITA",    "citas.jpg", "Agenda médica, turnos\ny asignación de especialistas.",
             0, 1, self.vista_citas, 2, 1),
            ("👤\nREGISTRO\nPACIENTES", "registro.jpg", "Alta de nuevos\npacientes\nen el sistema.",
             0, 0, self.vista_registro, 1, 2),
            ("🩺\nENFERMERÍA",       "enfermeria.jpg", "Triaje y toma\nde signos vitales.",
             1, 1, self.vista_enfermeria, 1, 1),
            ("📋\nVER AGENDA",       "agenda.jpg", "Listado completo\nde citas del día.",
             1, 2, self.vista_agenda, 1, 1),
        ]

        for titulo, img_ruta, desc, r, c, cmd, colspan, rowspan in tarjetas:
            self._tarjeta(grid_frame, titulo, img_ruta, desc, r, c, cmd, colspan, rowspan)

    def _tarjeta(self, parent, titulo, img_ruta, desc, r, c, cmd, colspan=1, rowspan=1):
        ruta = os.path.join(BASE_DIR, img_ruta)

        outer = tk.Frame(parent, bg=C["azul_medio"], cursor="hand2")
        outer.grid(row=r, column=c, columnspan=colspan, rowspan=rowspan, padx=8, pady=8, sticky="nsew")

        canvas = tk.Label(outer, bg=C["azul_medio"])
        canvas.pack(fill="both", expand=True)

        img_orig = None
        try:
            img_orig = Image.open(ruta)
        except Exception:
            pass

        def on_resize(event, img=img_orig):
            if img:
                w, h = event.width, event.height
                if w > 1 and h > 1:
                    resized = img.resize((w, h), Image.Resampling.LANCZOS)
                    overlay = Image.new("RGBA", resized.size, (13, 43, 78, 140))
                    base = resized.convert("RGBA")
                    combined = Image.alpha_composite(base, overlay).convert("RGB")
                    photo = ImageTk.PhotoImage(combined)
                    canvas.configure(image=photo)
                    canvas.image = photo

        canvas.bind("<Configure>", on_resize)

        bg_overlay = "#1a2b3e"
        text_frame = tk.Frame(canvas, bg=bg_overlay, bd=0)
        text_frame.place(relx=0.06, rely=0.5, anchor="w")

        tk.Label(text_frame, text=titulo, font=("Segoe UI", 13 if rowspan == 1 else 16, "bold"), fg=C["blanco"], bg=bg_overlay,
                 justify="left").pack(anchor="w")
        tk.Label(text_frame, text=desc, font=("Segoe UI", 9), fg="#CBD5E1", bg=bg_overlay, wraplength=240, 
                 justify="left").pack(anchor="w", pady=(4, 10))

        btn = tk.Button(text_frame, text="Abrir →", bg=C["azul_claro"], fg=C["blanco"], font=("Segoe UI", 9, "bold"),
                        relief="flat", bd=0, padx=16, pady=5, cursor="hand2", command=cmd)
        btn.pack(anchor="w")

        def card_enter(e):
            outer.configure(bg=C["azul_claro"])
        def card_leave(e):
            outer.configure(bg=C["azul_medio"])

        for widget in (outer, canvas):
            widget.bind("<Enter>", card_enter)
            widget.bind("<Leave>", card_leave)
            widget.bind("<Button-1>", lambda e, c=cmd: c())

#Registro de Pacientes
    def vista_registro(self):
        self.limpiar()
        self.sidebar("registro")

        main = tk.Frame(self.window, bg=C["azul_oscuro"], pady=5)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        center = tk.Frame(main, bg=C["fondo"], pady=5, padx=30)
        center.pack(fill="both", expand=True)

        left = tk.Frame(center, bg=C["fondo"],pady=30)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        right = tk.Frame(center, bg=C["fondo"], pady=30)
        right.pack(side="right", fill="both", expand=True, padx=(15, 0))

        form_card = tk.Frame(left, bg=C["blanco"], padx=40, pady=36)
        form_card.pack(fill="both", expand=True)

        tk.Label(form_card, text="👤  Registrar Paciente", font=FUENTES["titulo"], bg=C["blanco"], fg=C["texto"]).pack(anchor="w", pady=(0, 6))
        tk.Label(form_card, text="Complete los datos del nuevo paciente.", font=FUENTES["cuerpo"],bg=C["blanco"], 
                 fg=C["gris_texto"]).pack(anchor="w", pady=(0, 24))

        self.e_ci     = self._campo(form_card, "Carnet de Identidad (CI)")
        self.e_nombre = self._campo(form_card, "Nombre Completo")
        self.e_edad   = self._campo(form_card, "Edad")
        self.e_tel    = self._campo(form_card, "Teléfono (opcional)")

        self._boton_primario(form_card, "REGISTRAR PACIENTE →", self.registrar_paciente)

        list_card = tk.Frame(right, bg=C["blanco"], padx=30, pady=30)
        list_card.pack(fill="both", expand=True)

        header_r = tk.Frame(list_card, bg=C["blanco"])
        header_r.pack(fill="x", pady=(0, 16))
        tk.Label(header_r, text="Pacientes Registrados", font=FUENTES["subtitulo"], bg=C["blanco"], fg=C["texto"]).pack(side="left")
        tk.Label(header_r, text=f"{len(pacientes_db)} total", font=FUENTES["pequeño"], bg=C["azul_claro"], fg=C["blanco"],
                 padx=8, pady=3).pack(side="right")

        cols = ("CI", "Nombre", "Edad")
        tree = ttk.Treeview(list_card, columns=cols,
                            show="headings", height=12)
        anchos = [110, 220, 60]
        for col, w in zip(cols, anchos):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")
#Jose, no seria mejor eliminar esta barra? xd 
#No tiene mucha funcion
        vsb = ttk.Scrollbar(list_card, orient="vertical",
                            command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._poblar_pacientes(tree)
        self._tree_pacientes = tree

        def eliminar():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Sin selección", "Seleccione un paciente para eliminar.")
                return
            ci = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirmar", f"¿Eliminar al paciente con CI {ci}?"):
                del pacientes_db[str(ci)]
                self.guardar_pacientes()
                self._poblar_pacientes(tree)
                tree.delete(sel[0])

        tk.Button(list_card, text="🗑  Eliminar seleccionado", bg=C["rojo"], fg=C["blanco"], font=FUENTES["pequeño"],
                  relief="flat", bd=0, padx=12, pady=6, cursor="hand2", command=eliminar).pack(pady=(8, 0))

    def _poblar_pacientes(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for ci, datos in pacientes_db.items():
            tree.insert("", "end", values=(
                ci,
                datos.get("nombre", ""),
                datos.get("edad", ""),
            ))

    def registrar_paciente(self):
        ci     = self.e_ci.get().strip()
        nombre = self.e_nombre.get().strip()
        edad   = self.e_edad.get().strip()
        tel    = self.e_tel.get().strip()

        if not ci or not nombre:
            messagebox.showerror("Datos incompletos", "El CI y el nombre son obligatorios.")
            return

        if not ci.isdigit():
            messagebox.showerror("CI inválido", "El Carnet de Identidad solo debe contener números.")
            return

        if ci in pacientes_db:
            messagebox.showwarning("Paciente existente", f"Ya existe un paciente con CI {ci}.")
            return

        if edad and not edad.isdigit():
            messagebox.showerror("Edad inválida", "La edad debe ser un número entero.")
            return

        pacientes_db[ci] = {
            "nombre": nombre,
            "edad": edad,
            "telefono": tel,
        }
        self.guardar_pacientes()

        for e in (self.e_ci, self.e_nombre, self.e_edad, self.e_tel):
            e.delete(0, tk.END)

        self._poblar_pacientes(self._tree_pacientes)
        messagebox.showinfo("✅ Registrado", f"Paciente '{nombre}' registrado correctamente.")

#Sector de citas 😈
    def vista_citas(self):
        self.limpiar()
        self.sidebar("citas")

        main = tk.Frame(self.window, bg=C["azul_oscuro"], pady=5)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        left = tk.Frame(main, bg=C["fondo"], padx=30, pady=30)
        left.grid(row=0, column=0, sticky="nsew")

        form = tk.Frame(left, bg=C["blanco"], padx=40, pady=36)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="📅  Reservar Nueva Cita", font=FUENTES["titulo"], bg=C["blanco"], fg=C["texto"]).pack(anchor="w", pady=(0, 4))
        tk.Label(form, text="Seleccione paciente, especialidad y médico.", font=FUENTES["cuerpo"], bg=C["blanco"], 
                 fg=C["gris_texto"]).pack(anchor="w", pady=(0, 24))

        tk.Label(form, text="Paciente", font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w")
        lista_p = [f"{d['nombre']}  —  CI: {ci}"
                   for ci, d in pacientes_db.items()]
        self.c_paciente = ttk.Combobox(form, values=lista_p, state="readonly", font=FUENTES["cuerpo"])
        self.c_paciente.pack(fill="x", pady=(4, 16), ipady=6)

        tk.Label(form, text="Especialidad", font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w")
        self.c_especialidad = ttk.Combobox(form, values=sorted(especialidades.keys()), state="readonly", font=FUENTES["cuerpo"])
        self.c_especialidad.pack(fill="x", pady=(4, 16), ipady=6)
        self.c_especialidad.bind("<<ComboboxSelected>>", self._actualizar_doctores)

        tk.Label(form, text="Doctor / Horario", font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w")
        self.c_doctor = ttk.Combobox(form, state="readonly", font=FUENTES["cuerpo"])
        self.c_doctor.pack(fill="x", pady=(4, 16), ipady=6)

        tk.Label(form, text="Motivo de consulta (opcional)", font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w")
        self.e_motivo = tk.Text(form, font=FUENTES["cuerpo"], bg=C["fondo"], fg=C["texto"], relief="flat", height=4, bd=0,
                                insertbackground=C["azul_claro"])
        self.e_motivo.pack(fill="x", pady=(4, 20))

        self._boton_primario(form, "RESERVAR CITA →", self.guardar_cita)

        right = tk.Frame(main, bg=C["fondo"], padx=30, pady=30)
        right.grid(row=0, column=1, sticky="nsew")

        panel = tk.Frame(right, bg=C["blanco"], padx=30, pady=30)
        panel.pack(fill="both", expand=True)

        header_r = tk.Frame(panel, bg=C["blanco"])
        header_r.pack(fill="x", pady=(0, 16))
        tk.Label(header_r, text="Citas del Día", font=FUENTES["subtitulo"], bg=C["blanco"], fg=C["texto"]).pack(side="left")
        tk.Label(header_r, text=f"{len(citas)} total", font=FUENTES["pequeño"], bg=C["azul_claro"], fg=C["blanco"],
                 padx=8, pady=3).pack(side="right")

        cols = ("Paciente", "Especialidad", "Doctor", "Estado")
        tree = ttk.Treeview(panel, columns=cols, show="headings", height=15)
        for col, w in zip(cols, [160, 120, 160, 90]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        tree.tag_configure("pendiente", foreground=C["amarillo"])
        tree.tag_configure("atendido",  foreground=C["verde"])

        vsb2 = ttk.Scrollbar(panel, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb2.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb2.pack(side="right", fill="y")

        for c in reversed(citas):
            estado = c.get("triaje", "Pendiente")
            tag = "pendiente" if estado == "Pendiente" else "atendido"
            tree.insert("", "end", values=(
                c["paciente"],
                c["especialidad"],
                c["doctor"].split(" - ")[0],
                estado if estado == "Pendiente" else "✓ Atendido",
            ), tags=(tag,))

        self._tree_citas = tree

    def _actualizar_doctores(self, event=None):
        esp = self.c_especialidad.get()
        lista = []
        if esp in especialidades:
            for doc in especialidades[esp]:
                lista.append(f"{doc['nombre']}  —  {doc['hora']}")
        self.c_doctor["values"] = lista
        self.c_doctor.set("")

    def guardar_cita(self):
        paciente    = self.c_paciente.get()
        especialidad = self.c_especialidad.get()
        doctor      = self.c_doctor.get()
        motivo      = self.e_motivo.get("1.0", tk.END).strip()

        if not paciente or not especialidad or not doctor:
            messagebox.showerror("Campos incompletos", "Por favor seleccione paciente, especialidad y doctor.")
            return

        ci = paciente.split("CI: ")[1].strip()
        nombre = pacientes_db[ci]["nombre"]

        nueva = {
            "paciente":     nombre,
            "ci":           ci,
            "especialidad": especialidad,
            "doctor":       doctor.replace("  —  ", " - "),
            "triaje":       "Pendiente",
            "motivo":       motivo,
            "fecha":        datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
        citas.append(nueva)
        self.guardar_citas()

        estado = "⏳ Pendiente"
        self._tree_citas.insert("", 0, values=(nombre, especialidad, doctor.split("  —  ")[0], estado), tags=("pendiente",))
        self.c_paciente.set("")
        self.c_especialidad.set("")
        self.c_doctor.set("")
        self.e_motivo.delete("1.0", tk.END)

        messagebox.showinfo("✅ Cita registrada", f"Cita para '{nombre}' reservada correctamente.")

#Sector de enfermos xd,
# okno, de enfermeria
    def vista_enfermeria(self):
        self.limpiar()
        self.sidebar("enfermeria")

        main = tk.Frame(self.window, bg=C["azul_oscuro"], pady=5)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        left = tk.Frame(main, bg=C["fondo"], padx=30, pady=30)
        left.grid(row=0, column=0, sticky="nsew")

        form = tk.Frame(left, bg=C["blanco"], padx=40, pady=36)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="🩺  Triaje y Signos Vitales", font=FUENTES["titulo"], bg=C["blanco"], 
                 fg=C["texto"]).pack(anchor="w", pady=(0, 4))
        tk.Label(form, text="Registre los signos vitales del paciente.", font=FUENTES["cuerpo"], bg=C["blanco"], 
                 fg=C["gris_texto"]).pack(anchor="w", pady=(0, 24))

        tk.Label(form, text="Paciente pendiente", font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w")
        pendientes = [f"{c['paciente']}  —  CI: {c['ci']}"
                      for c in citas if c.get("triaje") == "Pendiente"]
        self.c_triaje = ttk.Combobox(form, values=pendientes, state="readonly", font=FUENTES["cuerpo"])
        self.c_triaje.pack(fill="x", pady=(4, 20), ipady=6)

        disp_lbl = tk.Label(form,
            text=f"{'⚠️  No hay pacientes pendientes.' if not pendientes else f'✅  {len(pendientes)} paciente(s) en espera.'}",
            font=FUENTES["pequeño"], bg=C["amarillo"] if not pendientes else C["verde"], fg=C["blanco"], padx=10, pady=5)
        disp_lbl.pack(fill="x", pady=(0, 16))

        sv = tk.Frame(form, bg=C["blanco"])
        sv.pack(fill="x")
        sv.columnconfigure((0, 1), weight=1)

        def campo_sv(parent, label, row, col, unidad=""):
            tk.Label(parent, text=label, font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).grid(row=row*2, column=col, 
                                                                                                         sticky="w", padx=(0, 10))
            frame = tk.Frame(parent, bg=C["fondo"])
            frame.grid(row=row*2+1, column=col, sticky="ew", pady=(4, 16), padx=(0, 10))
            e = tk.Entry(frame, font=FUENTES["cuerpo"], bg=C["fondo"], fg=C["texto"], relief="flat", bd=0, insertbackground=C["azul_claro"])
            e.pack(side="left", fill="x", expand=True, ipady=8, padx=(8, 0))
            if unidad:
                tk.Label(frame, text=unidad, font=FUENTES["pequeño"], bg=C["fondo"], fg=C["gris_texto"], padx=8).pack(side="right")
            tk.Frame(form, bg=C["gris_claro"], height=1).pack(
                fill="x") if False else None
            return e

        self.e_pa    = campo_sv(sv, "Presión Arterial",   0, 0, "mmHg")
        self.e_temp  = campo_sv(sv, "Temperatura",        0, 1, "°C")
        self.e_peso  = campo_sv(sv, "Peso",               1, 0, "kg")
        self.e_talla = campo_sv(sv, "Talla",              1, 1, "cm")
        self.e_fc    = campo_sv(sv, "Frec. Cardíaca",     2, 0, "lpm")
        self.e_sat   = campo_sv(sv, "Saturación O₂",     2, 1, "%")

        tk.Label(form, text="Observaciones", font=FUENTES["label"], bg=C["blanco"], fg=C["gris_texto"]).pack(anchor="w", pady=(8, 0))
        self.e_obs = tk.Text(form, font=FUENTES["cuerpo"], bg=C["fondo"], fg=C["texto"], relief="flat", height=3, bd=0)
        self.e_obs.pack(fill="x", pady=(4, 20))

        self._boton_primario(form, "GUARDAR TRIAJE →", self.guardar_triaje)

        right = tk.Frame(main, bg=C["fondo"], padx=30, pady=30)
        right.grid(row=0, column=1, sticky="nsew")

        panel = tk.Frame(right, bg=C["blanco"], padx=30, pady=30)
        panel.pack(fill="both", expand=True)

        tk.Label(panel, text="Historial de Triaje", font=FUENTES["subtitulo"], bg=C["blanco"], fg=C["texto"]).pack(anchor="w", pady=(0, 16))
        cols = ("Paciente", "Signos", "Estado")
        tree = ttk.Treeview(panel, columns=cols, show="headings", height=16)
        for col, w in zip(cols, [150, 260, 100]):
            tree.heading(col, text=col)
            tree.column(col, width=w)
        tree.tag_configure("pendiente", foreground=C["amarillo"])
        tree.tag_configure("ok", foreground=C["verde"])

        vsb = ttk.Scrollbar(panel, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        for c in citas:
            t = c.get("triaje", "Pendiente")
            tag = "pendiente" if t == "Pendiente" else "ok"
            est = "⏳ Pendiente" if t == "Pendiente" else "✓ Triaje OK"
            tree.insert("", "end", values=(c["paciente"], t, est), tags=(tag,))

        self._tree_triaje = tree

    def guardar_triaje(self):
        paciente = self.c_triaje.get()
        if not paciente:
            messagebox.showwarning("Sin selección",
                "Seleccione un paciente de la lista.")
            return

        pa   = self.e_pa.get().strip()
        temp = self.e_temp.get().strip()
        peso = self.e_peso.get().strip()

        if not pa or not temp or not peso:
            messagebox.showerror("Datos incompletos", "Presión, temperatura y peso son obligatorios.")
            return

        ci = paciente.split("CI: ")[1].strip()
        partes = []
        if pa:   partes.append(f"PA: {pa} mmHg")
        if temp: partes.append(f"T°: {temp}°C")
        if peso: partes.append(f"Peso: {peso} kg")
        talla = self.e_talla.get().strip()
        fc    = self.e_fc.get().strip()
        sat   = self.e_sat.get().strip()
        if talla: partes.append(f"Talla: {talla} cm")
        if fc:    partes.append(f"FC: {fc} lpm")
        if sat:   partes.append(f"SpO₂: {sat}%")
        obs = self.e_obs.get("1.0", tk.END).strip()
        if obs:   partes.append(f"Obs: {obs}")
        resumen = "  |  ".join(partes)

        for c in citas:
            if c["ci"] == ci and c.get("triaje") == "Pendiente":
                c["triaje"] = resumen
                break

        self.guardar_citas()

        pendientes = [f"{c['paciente']}  —  CI: {c['ci']}"
                      for c in citas if c.get("triaje") == "Pendiente"]
        self.c_triaje["values"] = pendientes
        self.c_triaje.set("")

        for e in (self.e_pa, self.e_temp, self.e_peso, self.e_talla, self.e_fc, self.e_sat):
            e.delete(0, tk.END)
        self.e_obs.delete("1.0", tk.END)

        for item in self._tree_triaje.get_children():
            vals = self._tree_triaje.item(item)["values"]
            if vals and str(vals[0]) == str(pacientes_db.get(ci, {}).get("nombre", "")):
                self._tree_triaje.item(item, values=(vals[0], resumen, "✓ Triaje OK"), tags=("ok",))
                break

        messagebox.showinfo("✅ Triaje guardado", "Los signos vitales fueron registrados correctamente.")

    def vista_agenda(self):
        self.limpiar()
        self.sidebar("agenda")

        main = tk.Frame(self.window, bg=C["azul_oscuro"], pady=5)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        header = tk.Frame(main, bg=C["blanco"], pady=20, padx=40)
        header.grid(row=0, column=0, sticky="ew")

        tk.Label(header, text="📋  Agenda General de Citas", font=FUENTES["titulo"], bg=C["blanco"], fg=C["texto"]).pack(side="left")

        total_c   = len(citas)
        pendientes = len([c for c in citas if c.get("triaje") == "Pendiente"])

        badge_frame = tk.Frame(header, bg=C["blanco"])
        badge_frame.pack(side="right")
        tk.Label(badge_frame, text=f"  {total_c} total  ", bg=C["azul_claro"], fg=C["blanco"], font=("Segoe UI", 10, "bold"), 
                 padx=6, pady=4).pack(side="left", padx=4)
        tk.Label(badge_frame, text=f"  {pendientes} pendientes  ", bg=C["amarillo"], fg=C["blanco"], font=("Segoe UI", 10, "bold"), 
                 padx=6, pady=4).pack(side="left", padx=4)

        search_bar = tk.Frame(main, bg=C["fondo"], pady=10, padx=30)
        search_bar.grid(row=1, column=0, sticky="ew")
        main.grid_rowconfigure(1, weight=0)

        tk.Label(search_bar, text="🔍",
                 font=("Segoe UI Emoji", 13),
                 bg=C["fondo"], fg=C["gris_texto"]).pack(side="left")
        self.e_buscar = tk.Entry(search_bar, font=FUENTES["cuerpo"], bg=C["blanco"], fg=C["texto"], relief="flat", bd=0)
        self.e_buscar.pack(side="left", fill="x", expand=True, ipady=8, padx=(8, 0))
        self.e_buscar.insert(0, "Buscar por nombre, CI o especialidad...")
        self.e_buscar.configure(fg=C["gris_texto"])

        def clear_placeholder(e):
            if self.e_buscar.get() == "Buscar por nombre, CI o especialidad...":
                self.e_buscar.delete(0, tk.END)
                self.e_buscar.configure(fg=C["texto"])
        self.e_buscar.bind("<FocusIn>", clear_placeholder)
        self.e_buscar.bind("<KeyRelease>", lambda e: self._filtrar_agenda())

        table_frame = tk.Frame(main, bg=C["fondo"], padx=30)
        table_frame.grid(row=2, column=0, sticky="nsew")
        main.grid_rowconfigure(2, weight=1)

        cols = ("Paciente", "CI", "Especialidad", "Doctor", "Horario", "Estado", "Fecha")
        self._tabla_agenda = ttk.Treeview(table_frame, columns=cols, show="headings")
        anchos = [180, 100, 140, 180, 80, 120, 120]
        for col, w in zip(cols, anchos):
            self._tabla_agenda.heading(col, text=col)
            self._tabla_agenda.column(col, width=w, anchor="center")

        self._tabla_agenda.tag_configure("pendiente", background="#FFFBEB", foreground="#92400E")
        self._tabla_agenda.tag_configure("atendido", background="#F0FDF4", foreground="#166534")
        self._tabla_agenda.tag_configure("impar", background="#F8FAFC")
        self._tabla_agenda.tag_configure("par", background=C["blanco"])

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self._tabla_agenda.yview)
        self._tabla_agenda.configure(yscrollcommand=vsb.set)
        self._tabla_agenda.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._poblar_agenda(citas)

        btn_frame = tk.Frame(main, bg=C["fondo"], padx=30, pady=8)
        btn_frame.grid(row=3, column=0, sticky="ew")
        main.grid_rowconfigure(3, weight=0)

        tk.Button(btn_frame, text="⬇  Exportar a CSV", bg=C["azul_medio"], fg=C["blanco"], font=FUENTES["pequeño"], relief="flat", 
                  bd=0, padx=16, pady=8, cursor="hand2", command=self._exportar_csv).pack(side="left")

        tk.Button(btn_frame, text="🗑️  Cancelar cita", bg=C["rojo"], fg=C["blanco"], font=FUENTES["pequeño"],
                  relief="flat", bd=0, padx=16, pady=8, cursor="hand2", command=self._cancelar_cita).pack(side="left", padx=10)

    def _poblar_agenda(self, lista):
        for row in self._tabla_agenda.get_children():
            self._tabla_agenda.delete(row)
        for i, c in enumerate(lista):
            triaje = c.get("triaje", "Pendiente")
            estado_txt = "⏳ Pendiente" if triaje == "Pendiente" else "✓ Atendido"
            tag = "pendiente" if triaje == "Pendiente" else "atendido"
            doc_parts = c.get("doctor", "").split(" - ")
            doctor_nombre = doc_parts[0]
            horario = doc_parts[1] if len(doc_parts) > 1 else ""
            self._tabla_agenda.insert("", "end", values=(
                c.get("paciente", ""),
                c.get("ci", ""),
                c.get("especialidad", ""),
                doctor_nombre,
                horario,
                estado_txt,
                c.get("fecha", "—"),
            ), tags=(tag,), iid=str(i))

    def _filtrar_agenda(self):
        texto = self.e_buscar.get().lower()
        if texto == "buscar por nombre, ci o especialidad...":
            texto = ""
        filtrados = [c for c in citas if
                     texto in c.get("paciente", "").lower() or
                     texto in c.get("ci", "").lower() or
                     texto in c.get("especialidad", "").lower()] if texto else citas
        self._poblar_agenda(filtrados)

    def _exportar_csv(self):
        ruta = os.path.join(BASE_DIR, "agenda_export.csv")
        try:
            import csv
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "paciente", "ci", "especialidad",
                    "doctor", "triaje", "fecha"])
                writer.writeheader()
                writer.writerows(citas)
            messagebox.showinfo("✅ Exportado", f"Agenda exportada a:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cancelar_cita(self):
        sel = self._tabla_agenda.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Seleccione una cita para cancelar.")
            return
        idx = int(sel[0])
        c = citas[idx]
        if messagebox.askyesno("Confirmar cancelación", f"¿Cancelar la cita de '{c['paciente']}'?"):
            citas.pop(idx)
            self.guardar_citas()
            self._poblar_agenda(citas)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaRecepcion(root)
    root.mainloop()