import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os

#EJECUTABLE.EXE



#GUARDADO DE PACIENTES

ARCHIVO_DOCTORES = "doctores.json"
ARCHIVO_PACIENTES = "pacientes.json"
ARCHIVO_CITAS = "citas.json"

#LISTA DE DOCTORES

if os.path.exists(ARCHIVO_DOCTORES):

    with open(ARCHIVO_DOCTORES, "r", encoding="utf-8") as archivo:

        especialidades = json.load(archivo)

else:

    especialidades = {}

#RECUPERACION DE PACIENTES 

if os.path.exists(ARCHIVO_PACIENTES):

    with open(ARCHIVO_PACIENTES, "r", encoding="utf-8") as archivo:

        pacientes_db = json.load(archivo)

else:

    pacientes_db = {}

#RECUPERACION DE CITAS, XD EN TEORIA SE DEBERIA CARGAR AQUI 

if os.path.exists(ARCHIVO_CITAS):

    with open(ARCHIVO_CITAS, "r", encoding="utf-8") as archivo:

        citas = json.load(archivo)

else:

    citas = []


#AQUI INICIAMOS LO SERIO

class AppHospitalCompleto:

    def __init__(self, root):

        self.root = root

        self.root.title("SISTEMA MÉDICO | Hospital Obrero")
        self.root.geometry("1100x800+0+0")
        self.root.resizable(True, True)
        self.root.iconbitmap("hosp.ico")
        self.color_bg = "#d5e3ec"
        self.color_accent = "#0E56A8"
        self.color_enfermeria = "#3f4fda"
        self.color_pacientes = "#3f4fda"
        self.color_texto_tit = "#3f4fda"
        self.color_texto_sub = "#3f4fda"

        self.fuente_tit = font.Font(family="Segoe UI", size=26, weight="bold")
        self.fuente_bienvenida = font.Font(family="Segoe UI", size=14)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.mostrar_panel_recepcion()

#GUARDADO EN JSON

    def guardar_pacientes(self):

        with open(ARCHIVO_PACIENTES, "w", encoding="utf-8") as archivo:

            json.dump(
                pacientes_db,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def guardar_citas(self):

        with open(ARCHIVO_CITAS, "w", encoding="utf-8") as archivo:

            json.dump(
                citas,
                archivo,
                indent=4,
                ensure_ascii=False
            )

#LIMPIEZA

    def limpiar(self):

        for widget in self.root.winfo_children():

            widget.destroy()

#BARRA LATERAL (AUN EN PROCESO)

    def sidebar(self, subtitulo):

        side = tk.Frame(self.root, bg="#0067c0", width=240)

        side.grid(row=0, column=0, sticky="ns")

        side.grid_propagate(False)

        tk.Label(
            side,
            text="🏥",
            font=("Segoe UI", 45),
            bg="#0067c0",
            fg="white"
        ).pack(pady=(40, 0))

        tk.Label(
            side,
            text="HOSPITAL",
            font=("Segoe UI", 14, "bold"),
            bg="#0067c0",
            fg="white"
        ).pack()

        tk.Label(
            side,
            text="OBRERO",
            font=("Segoe UI", 14, "bold"),
            bg="#0067c0",
            fg="#5B9DDF"
        ).pack()

        tk.Label(
            side,
            text=subtitulo.upper(),
            font=("Segoe UI", 9, "bold"),
            bg="#0067c0",
            fg="white"
        ).pack(pady=30)

        tk.Button(
            side,
            text="🏠 INICIO",
            bg="#1D3E5C",
            fg="white",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            command=self.mostrar_panel_recepcion
        ).pack(fill="x", pady=2)

        tk.Button(
            side,
            text="🚪 SALIR",
            bg="#C0392B",
            fg="white",
            bd=0,
            command=self.root.quit
        ).pack(side="bottom", fill="x", ipady=15)

#INTERFAZ PRINCIPAL

    def mostrar_panel_recepcion(self):

        self.limpiar()
        self.sidebar("Sala de Recepción")

        main = tk.Frame(
            self.root,
            bg=self.color_bg,
            padx=50,
            pady=40
        )

        main.grid(row=0, column=1, sticky="nsew")

        tk.Label(
            main,
            text="Buenos Días",
            font=self.fuente_tit,
            bg=self.color_bg,
            fg="Black"
        ).pack(anchor="w")

        tk.Label(
            main,
            text="Bienvenido al Hospital Obrero.\n"
                 "Agradecemos su confianza en nuestra institución, nuestro personal trabaja "
                 "día a día para ofrecer servicios de salud con profesionalismo, respeto y "
                 "calidad humana.\n"
                 "Mediante este sistema podrá realizar diferentes trámites y consultas "
                 "relacionados con la atención médica y administrativa.\n"
                 "Por favor, seleccione una opción del menú para continuar:",
            font=self.fuente_bienvenida,
            bg=self.color_bg,
            fg="Black",
            justify="left",
            anchor="w",
        ).pack(anchor="w", fill="both", expand=True, padx=10, pady=10)

        grid = tk.Frame(main, bg=self.color_bg)

        grid.pack(fill="both", expand=True)

        grid.columnconfigure((0, 1), weight=1)

        self.card(grid, "REGISTRO PACIENTES", "👤", "Alta de pacientes", 0, 0, self.vista_registro, self.color_pacientes)
        self.card(grid, "RESERVAR CITA", "📅", "Agenda médica", 0, 1, self.vista_citas, self.color_enfermeria)
        self.card(grid, "ENFERMERÍA", "🩺", "Triaje y signos vitales", 1, 0, self.vista_enfermeria, self.color_enfermeria)
        self.card(grid, "VER AGENDA", "📋", "Listado completo", 1, 1, self.vista_enfermeria, self.color_enfermeria)

#CUADROS

    def card(self, p, t, e, d, r, c, cmd, col):

        f = tk.Frame(
            p,
            bg="#eef2fb",
            highlightthickness=1,
            highlightbackground="#D8E2EC",
            cursor="hand2"
        )

        f.grid(
            row=r,
            column=c,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        tk.Label(
            f,
            text=e,
            font=("Segoe UI", 35),
            bg="#eef2fb"
        ).pack(pady=15)

        tk.Label(
            f,
            text=t,
            font=("Segoe UI", 11, "bold"),
            fg=col,
            bg="#eef2fb"
        ).pack()

        tk.Label(
            f,
            text=d,
            font=("Segoe UI", 9),
            fg="#8193A5",
            bg="#eef2fb"
        ).pack(pady=10)

        tk.Button(
            f,
            text="ABRIR",
            bg=col,
            fg="white",
            bd=0,
            command=cmd
        ).pack(fill="x", padx=20, pady=20, ipady=10)

#ENTRADAS DEL USUARIO

    def input(self, p, t):

        tk.Label(
            p,
            text=t,
            bg="white",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        e = tk.Entry(
            p,
            font=("Segoe UI", 11),
            bg="#F3F7FB",
            bd=0
        )

        e.pack(fill="x", pady=(5, 15), ipady=5)

        return e

#REGISTRO DE PACIENTES

    def vista_registro(self):

        self.limpiar()

        self.sidebar("Registro")

        main = tk.Frame(
            self.root,
            bg=self.color_bg,
            padx=50,
            pady=40
        )

        main.grid(row=0, column=1, sticky="nsew")

        card = tk.Frame(
            main,
            bg="white",
            padx=30,
            pady=30
        )

        card.pack(fill="x")

        self.e_ci = self.input(card, "Carnet de Identidad")

        self.e_nombre = self.input(card, "Nombre Completo")

        self.e_edad = self.input(card, "Edad")

        tk.Button(
            card,
            text="REGISTRAR PACIENTE",
            bg=self.color_pacientes,
            fg="white",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            command=self.registrar_paciente
        ).pack(fill="x", ipady=10)

    def registrar_paciente(self):

        ci = self.e_ci.get()

        nombre = self.e_nombre.get()

        edad = self.e_edad.get()

        if not ci or not nombre:

            messagebox.showerror(
                "ERROR",
                "Complete todos los datos"
            )

            return

        pacientes_db[ci] = {
            "nombre": nombre,
            "edad": edad
        }

        self.guardar_pacientes()

        messagebox.showinfo(
            "ÉXITO",
            "Paciente registrado correctamente"
        )

#MODULO CITAS

    def vista_citas(self):

        self.limpiar()

        self.sidebar("Citas")

        main = tk.Frame(
            self.root,
            bg=self.color_bg,
            padx=50,
            pady=40
        )

        main.grid(row=0, column=1, sticky="nsew")

        card = tk.Frame(
            main,
            bg="white",
            padx=30,
            pady=30
        )

        card.pack(fill="x")

#PACIENTES
        lista_pacientes = []

        for ci, datos in pacientes_db.items():

            texto = f"{datos['nombre']} - CI: {ci}"

            lista_pacientes.append(texto)

        tk.Label(
            card,
            text="Paciente"
        ).pack(anchor="w")

        self.c_paciente = ttk.Combobox(
            card,
            values=lista_pacientes,
            state="readonly"
        )

        self.c_paciente.pack(fill="x", pady=10)

#ESPECIALIDADES
        tk.Label(
            card,
            text="Especialidad"
        ).pack(anchor="w")

        self.c_especialidad = ttk.Combobox(
            card,
            values=list(especialidades.keys()),
            state="readonly"
        )

        self.c_especialidad.pack(fill="x", pady=10)

        self.c_especialidad.bind(
            "<<ComboboxSelected>>",
            self.actualizar_doctores
        )

        # DOCTOR
        tk.Label(
            card,
            text="Doctor"
        ).pack(anchor="w")

        self.c_doctor = ttk.Combobox(
            card,
            state="readonly"
        )

        self.c_doctor.pack(fill="x", pady=10)

        tk.Button(
            card,
            text="RESERVAR CITA",
            bg=self.color_accent,
            fg="white",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            command=self.guardar_cita
        ).pack(fill="x", ipady=10)

    def actualizar_doctores(self, event):

        especialidad = self.c_especialidad.get()

        lista = []

        for doctor in especialidades[especialidad]:

            texto = f"{doctor['nombre']} - {doctor['hora']}"

            lista.append(texto)

        self.c_doctor["values"] = lista

    def guardar_cita(self):

        paciente = self.c_paciente.get()

        especialidad = self.c_especialidad.get()

        doctor = self.c_doctor.get()

        if not paciente or not especialidad or not doctor:

            messagebox.showerror(
                "ERROR",
                "Complete todos los campos"
            )

            return

        ci = paciente.split("CI: ")[1]

        nombre = pacientes_db[ci]["nombre"]

        nueva_cita = {
            "paciente": nombre,
            "ci": ci,
            "especialidad": especialidad,
            "doctor": doctor,
            "triaje": "Pendiente"
        }

        citas.append(nueva_cita)

        self.guardar_citas()

        messagebox.showinfo(
            "ÉXITO",
            "Cita registrada correctamente"
        )

    #MODULO DE ENFERMERIA Y TRIAJE

    def vista_enfermeria(self):

        self.limpiar()

        self.sidebar("Enfermería")

        main = tk.Frame(
            self.root,
            bg=self.color_bg,
            padx=50,
            pady=40
        )

        main.grid(row=0, column=1, sticky="nsew")

        card = tk.Frame(
            main,
            bg="white",
            padx=30,
            pady=30
        )

        card.pack(fill="x")

        pendientes = []

        for c in citas:

            if c["triaje"] == "Pendiente":

                pendientes.append(
                    f"{c['paciente']} - CI: {c['ci']}"
                )

        tk.Label(
            card,
            text="Paciente"
        ).pack(anchor="w")

        self.c_triaje = ttk.Combobox(
            card,
            values=pendientes,
            state="readonly"
        )

        self.c_triaje.pack(fill="x", pady=10)

        self.e_pa = self.input(card, "Presión Arterial")

        self.e_temp = self.input(card, "Temperatura")

        self.e_peso = self.input(card, "Peso")

        tk.Button(
            card,
            text="GUARDAR TRIAJE",
            bg=self.color_enfermeria,
            fg="white",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            command=self.guardar_triaje
        ).pack(fill="x", ipady=10)

    def guardar_triaje(self):

        paciente = self.c_triaje.get()

        if not paciente:
            return

        ci = paciente.split("CI: ")[1]

        for c in citas:

            if c["ci"] == ci:

                c["triaje"] = (
                    f"PA: {self.e_pa.get()} | "
                    f"TEMP: {self.e_temp.get()} | "
                    f"PESO: {self.e_peso.get()}"
                )

        self.guardar_citas()

        messagebox.showinfo(
            "ÉXITO",
            "Triaje guardado correctamente"
        )

    #AGENDA DE PACIENTES

    def vista_agenda(self):

        self.limpiar()

        self.sidebar("Agenda")

        main = tk.Frame(
            self.root,
            bg=self.color_bg,
            padx=20,
            pady=20
        )

        main.grid(row=0, column=1, sticky="nsew")

        tabla = ttk.Treeview(
            main,
            columns=(
                "Paciente",
                "CI",
                "Especialidad",
                "Doctor",
                "Triaje"
            ),
            show="headings"
        )

        columnas = [
            "Paciente",
            "CI",
            "Especialidad",
            "Doctor",
            "Triaje"
        ]

        for col in columnas:

            tabla.heading(col, text=col)

            tabla.column(
                col,
                width=150,
                anchor="center"
            )

        for c in citas:

            tabla.insert(
                "",
                "end",
                values=(
                    c["paciente"],
                    c["ci"],
                    c["especialidad"],
                    c["doctor"],
                    c["triaje"]
                )
            )

        tabla.pack(fill="both", expand=True)


root = tk.Tk()

app = AppHospitalCompleto(root)

root.mainloop()