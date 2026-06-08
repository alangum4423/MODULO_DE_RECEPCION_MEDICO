import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import json
import os

ARCHIVO_DOCTORES = "doctores.json"
ARCHIVO_PACIENTES = "pacientes.json"
ARCHIVO_CITAS = "citas.json"

#RUTAS Y ARCHIVOS
if os.path.exists(ARCHIVO_PACIENTES):
    with open(ARCHIVO_PACIENTES, "r", encoding="utf-8") as archivo:
        pacientes_db = json.load(archivo)
else:
    pacientes_db = {}

if os.path.exists(ARCHIVO_CITAS):
    with open(ARCHIVO_CITAS, "r", encoding="utf-8") as archivo:
        citas = json.load(archivo)
else:
    citas = []

if os.path.exists(ARCHIVO_DOCTORES):
    with open(ARCHIVO_DOCTORES, "r", encoding="utf-8") as archivo:
        especialidades = json.load(archivo)
else:
    especialidades = {}

#AQUI INICIAMOS LO SERIO
class SaladeRecepcion:

    def __init__(self, window):
        self.window = window
        self.window.title("SISTEMA MÉDICO | Hospital Obrero")
        self.window.geometry("1100x800+0+0")
        self.window.configure(bg="#0067c0")
        self.window.resizable(True, True)
        self.window.iconbitmap("hosp.ico")
        self.color_bg = "#d5e3ec"
        self.color_accent = "#0E7AA8"
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.mostrar_panel_recepcion()


#BARRA LATERAL (AUN EN PROCESO)    
    def sidebar(self, subtitulo):

        side = tk.Frame(self.window, bg="#0067c0", width=240)
        side.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        side.grid_propagate(False)

        tk.Label(
            side,
            text="🏥",
            font=("Segoe UI", 45),
            bg="#0067c0",
            fg="white"
        ).pack(pady=(40, 0))  
        tk.Label(side, text="HOSPITAL\n" "OBRERO", font=("Segoe UI", 10, "bold"), bg= "#0067c0", fg="white").pack()

        tk.Button(
            side,
            text="🏠",
            bg="#2474B5",
            fg="white",
            bd=0,
            font=("Segoe UI", 15, "bold"),
            command=self.mostrar_panel_recepcion
        ).pack(fill="x", pady=(40,0))  
        tk.Label(side, text="             INICIO              ", font=("Segoe UI", 7), bg= "#2474B5", fg="white").pack()

        tk.Button(
            side,
            text="📖",
            bg="#2474B5",
            fg="white",
            bd=0,
            font=("Segoe UI", 15, "bold"),
            command=self.mostrar_panel_recepcion
        ).pack(fill="x", pady=(40,0))  
        tk.Label(side, text="           HISTORIA            ", font=("Segoe UI", 7), bg= "#2474B5", fg="white").pack()

        tk.Button(
            side,
            text="🏠",
            bg="#2474B5",
            fg="white",
            bd=0,
            font=("Segoe UI", 15, "bold"),
            command=self.mostrar_panel_recepcion
        ).pack(fill="x", pady=(40,0))  
        tk.Label(side, text="             INICIO3             ", font=("Segoe UI", 7), bg= "#2474B5", fg="white").pack()

        tk.Button(
            side,
            text="📍",
            bg="#2474B5",
            fg="white",
            bd=0,
            font=("Segoe UI", 15, "bold"),
            command=self.mostrar_panel_recepcion
        ).pack(fill="x", pady=(40,0))  
        tk.Label(side, text="         UBICACION         ", font=("Segoe UI", 7), bg= "#2474B5", fg="white").pack()

        tk.Button(
            side,
            text="🚪",
            bg="#C0392B",
            fg="white",
            bd=0,
            command=self.window.quit
        ).pack(side="bottom", fill="x", ipady=15)  

#EL INFIERNO DE LA INTERFAZ PRINCIPAL (AUNQUE SI SE VE MODERNA)
    def limpiar(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def mostrar_panel_recepcion(self):
        self.limpiar()
        self.sidebar("Sala de Recepción")
          
        main = tk.Frame(self.window, bg=self.color_bg, padx=40, pady=40)
        main.grid(row=0, column=1, sticky="nsew", pady=5)   
        
        self.fuente_tit = font.Font(family="Segoe UI", size=26, weight="bold")
        tk.Label(main, text="Buenos Días", font=self.fuente_tit, bg=self.color_bg, fg="Black").pack()

        self.fuente_bienvenida = font.Font(family="Segoe UI", size=14)
        tk.Label(main,
            text="Bienvenido al Hospital Obrero.\n",
            font=self.fuente_bienvenida, bg=self.color_bg, fg="Black", wraplength=1000).pack()
        
        grid = tk.Frame(main, bg=self.color_bg)
        grid.pack(fill="both", expand=True)
        grid.columnconfigure((0, 1, 2), weight=1)
        grid.rowconfigure((0, 1), weight=1) 
        self.card(grid, "RESERVAR CITA", "citas.jpg", "Agenda médica y turnos", 0, 1, self.vista_citas, "#3f4fda", 2, 1)
        self.card(grid, "REGISTRO\n" "PACIENTES", "registro.jpg", "Registro de\n" "nuevos pacientes\n" "en sistema", 0, 0, self.vista_registro, "#3f4fda", 1, 2)
        self.card(grid, "ENFERMERÍA", "enfermeria.jpg", "Triaje y signos vitales", 1, 1, self.vista_enfermeria, "#3f4fda", 1, 1)
        self.card(grid, "VER AGENDA", "agenda.jpg", "Listado completo", 1, 2, self.vista_agenda, "#3f4fda", 1, 1)

#CUADROS
    def card(self, p, t, img_ruta, d, r, c, cmd, col, colspan=1, rowspan=1):

        ancho = 760 if colspan == 2 else 360
        alto = 460 if rowspan == 2 else 210

        try:
            img_or = Image.open(img_ruta).resize((ancho, alto), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img_or)
        except Exception as e:
            print(f"Error cargando {img_ruta}: {e}")
            foto = None

        f = tk.Label(p, bg=col, bd=0)
        f.grid(row=r, column=c, columnspan=colspan, rowspan=rowspan, padx=10, pady=10, sticky="nsew")

        try:
            img_original = Image.open(img_ruta)
        except Exception as e:
            print(f"Error al abrir la imagen {img_ruta}: {e}")
            img_original = None

        def ajustar_imagen_al_contenedor(event):
            if img_original:
                ancho_real = event.width
                alto_real = event.height
                img_redimensionada = img_original.resize((ancho_real, alto_real), Image.Resampling.LANCZOS)
                foto_tk = ImageTk.PhotoImage(img_redimensionada)
                f.config(image=foto_tk)
                f.image = foto_tk

        f.bind("<Configure>", ajustar_imagen_al_contenedor)

        if rowspan == 2:
            lbl_tit = tk.Label(f, text=t, font=("Segoe UI", 16, "bold"), fg="white", bg="#2A2A2A", justify="left")
            lbl_tit.place(relx=0.05, rely=0.3, anchor="w")
            lbl_desc = tk.Label(f, text=d, font=("Segoe UI", 10), fg="#E0E6ED", bg="#2A2A2A", wraplength=ancho-40, justify="left")
            lbl_desc.place(relx=0.05, rely=0.42, anchor="w")
            btn_abrir = tk.Button(f, text="ABRIR", bg="#3f4fda", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=30, pady=6, command=cmd)
            btn_abrir.place(relx=0.05, rely=0.58, anchor="w")
        else:
            lbl_tit = tk.Label(f, text=t, font=("Segoe UI", 14, "bold"), fg="white", bg="#2A2A2A", justify="left")
            lbl_tit.place(relx=0.05, rely=0.25, anchor="w")
            lbl_desc = tk.Label(f, text=d, font=("Segoe UI", 9), fg="#E0E6ED", bg="#2A2A2A", wraplength=ancho-40, justify="left")
            lbl_desc.place(relx=0.05, rely=0.48, anchor="w")
            btn_abrir = tk.Button(f, text="ABRIR", bg="#3f4fda", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=25, pady=4, command=cmd)
            btn_abrir.place(relx=0.05, rely=0.75, anchor="w")

#ENTRADAS DEL USUARIO
    def input(self, p, t):
        tk.Label(p, text=t, bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        e = tk.Entry(p, font=("Segoe UI", 11), bg="#F3F7FB", bd=0)
        e.pack(fill="x", pady=(5, 15), ipady=5)
        return e

#REGISTRO DE PACIENTES
    def guardar_pacientes(self):
        with open(ARCHIVO_PACIENTES, "w", encoding="utf-8") as archivo:
            json.dump(pacientes_db, archivo, indent=4, ensure_ascii=False)
    def guardar_citas(self):
        with open(ARCHIVO_CITAS, "w", encoding="utf-8") as archivo:
            json.dump(citas, archivo, indent=4, ensure_ascii=False)
    
    def vista_registro(self):
        self.limpiar()
        self.sidebar("Registro")

        main = tk.Frame(self.window, bg=self.color_bg, padx=50, pady=40)
        main.grid(row=0, column=1, sticky="nsew", pady=5)

        card = tk.Frame(main, bg="white", padx=30, pady=30)
        card.pack(fill="x")

        self.e_ci = self.input(card, "Carnet de Identidad")
        self.e_nombre = self.input(card, "Nombre Completo")
        self.e_edad = self.input(card, "Edad")

        tk.Button(card, text="REGISTRAR PACIENTE", bg="#3f4fda", fg="white", bd=0, font=("Segoe UI", 11, "bold"), 
                  command=self.registrar_paciente).pack(fill="x", ipady=10)

    def registrar_paciente(self):

        ci = self.e_ci.get()
        nombre = self.e_nombre.get()
        edad = self.e_edad.get()

        if not ci or not nombre:
            messagebox.showerror("ERROR", "Porfavor, complete todos los datos")
            return

        pacientes_db[ci] = {"nombre": nombre, "edad": edad}
        self.guardar_pacientes()

        messagebox.showinfo("EXCELENTE", "El Paciente fue registrado correctamente")

#MODULO CITAS

    def vista_citas(self):

        self.limpiar()
        self.sidebar("Citas")

        main = tk.Frame(self.window, bg=self.color_bg, padx=50, pady=40)
        main.grid(row=0, column=1, sticky="nsew", pady=5)

        card = tk.Frame(main, bg="white", padx=30, pady=30)
        card.pack(fill="x")

#PACIENTES
        lista_pacientes = []

        for ci, datos in pacientes_db.items():
            texto = f"{datos['nombre']} - CI: {ci}"
            lista_pacientes.append(texto)

        tk.Label(card, text="Paciente").pack(anchor="w")
        self.c_paciente = ttk.Combobox(card, values=lista_pacientes, state="readonly")
        self.c_paciente.pack(fill="x", pady=10)

#ESPECIALIDADES
        tk.Label(card, text="Especialidad").pack(anchor="w")
        self.c_especialidad = ttk.Combobox(card, values=list(especialidades.keys()), state="readonly")
        self.c_especialidad.pack(fill="x", pady=10)
        self.c_especialidad.bind("<<ComboboxSelected>>", self.actualizar_doctores)

        # LA GRILLA DE DOCTORES (Xd)
        tk.Label(card, text="Doctor").pack(anchor="w")
        self.c_doctor = ttk.Combobox(card, state="readonly")
        self.c_doctor.pack(fill="x", pady=10)

        tk.Button(card, text="RESERVAR CITA", bg="#3f4fda", fg="white", bd=0, font=("Segoe UI", 11, "bold"), 
                  command=self.guardar_cita).pack(fill="x", ipady=10)

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
                "Complete todos los campos")
            return

        ci = paciente.split("CI: ")[1]
        nombre = pacientes_db[ci]["nombre"]
        nueva_cita = {"paciente": nombre, "ci": ci, "especialidad": especialidad, "doctor": doctor, "triaje": "Pendiente"}
        citas.append(nueva_cita)
        self.guardar_citas()
        messagebox.showinfo("ÉXITO", "Cita registrada correctamente")
#MODULO DE ENFERMERIA Y TRIAJE
    def vista_enfermeria(self):

        self.limpiar()
        self.sidebar("Enfermería")

        main = tk.Frame(self.window, bg=self.color_bg, padx=50, pady=40)
        main.grid(row=0, column=1, sticky="nsew", pady=5)
        card = tk.Frame(main, bg="white", padx=30, pady=30)
        card.pack(fill="x")

        pendientes = []

        for c in citas:
            if c["triaje"] == "Pendiente":
                pendientes.append(f"{c['paciente']} - CI: {c['ci']}")
        tk.Label(card, text="Paciente").pack(anchor="w")

        self.c_triaje = ttk.Combobox(card, values=pendientes, state="readonly")
        self.c_triaje.pack(fill="x", pady=10)
        self.e_pa = self.input(card, "Presión Arterial")
        self.e_temp = self.input(card, "Temperatura")
        self.e_peso = self.input(card, "Peso")

        tk.Button(card, text="GUARDAR TRIAJE", bg="#3f4fda", fg="white", bd=0, font=("Segoe UI", 11, "bold"), 
                  command=self.guardar_triaje).pack(fill="x", ipady=10)

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
                    f"PESO: {self.e_peso.get()}")
        self.guardar_citas()

        messagebox.showinfo("EXCELENTE", "Sus datos han sido guardado correctamente")

#AGENDA DE PACIENTES
    def vista_agenda(self):
        self.limpiar()
        self.sidebar("Agenda")

        main = tk.Frame(self.window, bg="#d5e3ec", padx=20, pady=20)
        main.grid(row=0, column=1, sticky="nsew", pady=5)

        tabla = ttk.Treeview(
            main,
            columns=("Paciente", "CI", "Especialidad", "Doctor", "Triaje"), show="headings")
        columnas = ["Paciente", "CI", "Especialidad", "Doctor", "Triaje"]

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=150, anchor="center")
        for c in citas:
            tabla.insert("", "end", values=(c["paciente"], c["ci"], c["especialidad"], c["doctor"], c["triaje"]))
        tabla.pack(fill="both", expand=True)

root = tk.Tk()
app = SaladeRecepcion(root)  
root.mainloop()