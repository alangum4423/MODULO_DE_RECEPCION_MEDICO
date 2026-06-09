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
        tk.Label(side, text="              INICIO               ", font=("Segoe UI", 7), bg= "#2474B5", fg="white").pack()

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
            text="🩺",
            bg="#2474B5",
            fg="white",
            bd=0,
            font=("Segoe UI", 15, "bold"),
            command=self.mostrar_panel_recepcion
        ).pack(fill="x", pady=(40,0))  
        tk.Label(side, text="    ESPECIALIDADES   ", font=("Segoe UI", 7), bg= "#2474B5", fg="white").pack()

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

        # Frame principal adaptado con grillas expandibles
        main = tk.Frame(self.window, bg=self.color_bg)
        main.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        card = tk.Frame(main, bg="white", padx=50, pady=50)
        card.pack(fill="both", expand=True, padx=40, pady=30)
        tk.Label(card, text="👤 Registro de Nuevos Pacientes", 
                 font=("Segoe UI", 26, "bold"), bg="white", fg="#1e3a8a").pack(anchor="w", pady=(0, 35))
        campos_frame = tk.Frame(card, bg="white")
        campos_frame.pack(fill="x", pady=10)
        tk.Label(campos_frame, text="Carnet de Identidad (CI)", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.e_ci = tk.Entry(campos_frame, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        self.e_ci.pack(fill="x", pady=(5, 18), ipady=8)
        tk.Label(campos_frame, text="Nombre Completo", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.e_nombre = tk.Entry(campos_frame, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        self.e_nombre.pack(fill="x", pady=(5, 18), ipady=8)
        tk.Label(campos_frame, text="Edad", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.e_edad = tk.Entry(campos_frame, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        self.e_edad.pack(fill="x", pady=(5, 30), ipady=8)
        tk.Button(card, text="REGISTRAR PACIENTE", bg="#3f4fda", fg="white", bd=0, 
                  font=("Segoe UI", 13, "bold"), height=2,
                  command=self.registrar_paciente).pack(fill="x", pady=10)

    def registrar_paciente(self):
        ci = self.e_ci.get()
        nombre = self.e_nombre.get()
        edad = self.e_edad.get()

        if not ci or not nombre:
            messagebox.showerror("ERROR", "Porfavor, complete todos los datos")
            return

        pacientes_db[ci] = {"nombre": nombre, "edad": edad}
        self.guardar_pacientes()

        self.e_ci.delete(0, tk.END)
        self.e_nombre.delete(0, tk.END)
        self.e_edad.delete(0, tk.END)

        messagebox.showinfo("EXCELENTE", "El Paciente fue registrado correctamente")

#MODULO CITAS
    def vista_citas(self):
        self.limpiar()
        self.sidebar("Citas")

        main = tk.Frame(self.window, bg=self.color_bg)
        main.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)
        
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        left = tk.Frame(main, bg=self.color_bg, padx=30, pady=30)
        left.grid(row=0, column=0, sticky="nsew")
        card = tk.Frame(left, bg="white", padx=40, pady=40, relief="flat")
        card.pack(fill="both", expand=True)

        tk.Label(card, text="📅 Reservar Nueva Cita", 
                 font=("Segoe UI", 24, "bold"), bg="white", fg="#1e3a8a").pack(anchor="w", pady=(0, 30))

        tk.Label(card, text="Paciente", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        lista_pacientes = [f"{datos['nombre']} - CI: {ci}" for ci, datos in pacientes_db.items()]
        self.c_paciente = ttk.Combobox(card, values=lista_pacientes, state="readonly", font=("Segoe UI", 10))
        self.c_paciente.pack(fill="x", pady=(5, 18), ipady=6)
        tk.Label(card, text="Especialidad", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.c_especialidad = ttk.Combobox(card, values=list(especialidades.keys()), 
                                         state="readonly", font=("Segoe UI", 10))
        self.c_especialidad.pack(fill="x", pady=(5, 18), ipady=6)
        self.c_especialidad.bind("<<ComboboxSelected>>", self.actualizar_doctores)
        tk.Label(card, text="Doctor", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.c_doctor = ttk.Combobox(card, state="readonly", font=("Segoe UI", 10))
        self.c_doctor.pack(fill="x", pady=(5, 30), ipady=6)

        tk.Button(card, text="RESERVAR CITA", bg="#3f4fda", fg="white", bd=0,
                  font=("Segoe UI", 12, "bold"), height=2,
                  command=self.guardar_cita).pack(fill="x", pady=10)

    def actualizar_doctores(self, event):
        especialidad = self.c_especialidad.get()
        lista = []
        if especialidad in especialidades:
            for doctor in especialidades[especialidad]:
                texto = f"{doctor['nombre']} - {doctor['hora']}"
                lista.append(texto)
        self.c_doctor["values"] = lista

    def guardar_cita(self):
        paciente = self.c_paciente.get()
        especialidad = self.c_especialidad.get()
        doctor = self.c_doctor.get()

        if not paciente or not especialidad or not doctor:
            messagebox.showerror("ERROR", "Porfavor complete todos los campos")
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
        messagebox.showinfo("EXCELENTE", "Cita registrada correctamente")



#MODULO DE ENFERMERIA Y TRIAJE
    def vista_enfermeria(self):

        self.limpiar()
        self.sidebar("Enfermería")

        main = tk.Frame(self.window, bg=self.color_bg, padx=50, pady=40)
        main.grid(row=0, column=1, sticky="nsew", pady=5)
        card = tk.Frame(main, bg="white", padx=50, pady=50)
        card.pack(fill="both", expand=True, padx=40, pady=30)

        pendientes = []

        tk.Label(card, text="🩺 Triaje y Signos Vitales", 
                 font=("Segoe UI", 26, "bold"), bg="white", fg="#1e3a8a").pack(anchor="w", pady=(0, 35))

        tk.Label(card, text="Paciente Pendiente", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
        pendientes = [f"{c['paciente']} - CI: {c['ci']}" for c in citas if c.get("triaje") == "Pendiente"]
        self.c_triaje = ttk.Combobox(card, values=pendientes, state="readonly", font=("Segoe UI", 10))
        self.c_triaje.pack(fill="x", pady=(5, 25), ipady=6)

        signos_frame = tk.Frame(card, bg="white")
        signos_frame.pack(fill="x", pady=10)
        tk.Label(signos_frame, text="Presión Arterial (PA)", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.e_pa = tk.Entry(signos_frame, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        self.e_pa.pack(fill="x", pady=(5, 18), ipady=8)
        tk.Label(signos_frame, text="Temperatura (°C)", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.e_temp = tk.Entry(signos_frame, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        self.e_temp.pack(fill="x", pady=(5, 18), ipady=8)
        tk.Label(signos_frame, text="Peso (kg)", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w")
        self.e_peso = tk.Entry(signos_frame, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        self.e_peso.pack(fill="x", pady=(5, 30), ipady=8)

        tk.Button(card, text="GUARDAR DATOS", bg="#3f4fda", fg="white", bd=0, font=("Segoe UI", 13, "bold"), height=2,
                  command=self.guardar_triaje).pack(fill="x", pady=10)

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

        main = tk.Frame(self.window, bg=self.color_bg)
        main.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        header = tk.Frame(main, bg="white", height=100)
        header.pack(fill="x", padx=30, pady=(30, 0))
        header.pack_propagate(False)

        tk.Label(header, text="📋 Agenda General de Citas", 
                 font=("Segoe UI", 26, "bold"), bg="white", fg="#1e3a8a").pack(side="left", padx=40, pady=25)
        total_citas = len(citas)
        pendientes = len([c for c in citas if c.get("triaje") == "Pendiente"])
        info_frame = tk.Frame(header, bg="white")
        info_frame.pack(side="right", padx=40)
        tk.Label(info_frame, text=f"Total: {total_citas}", 
                 font=("Segoe UI", 12, "bold"), bg="white", fg="#334155").pack(anchor="e")
        tk.Label(info_frame, text=f"Pendientes: {pendientes}", 
                 font=("Segoe UI", 12), bg="white", fg="#ef4444").pack(anchor="e")
        table_frame = tk.Frame(main, bg="white", padx=30, pady=20)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#f8fafc",
                       foreground="#1e2937",
                       fieldbackground="#f8fafc",
                       font=("Segoe UI", 10),
                       rowheight=28)
        style.configure("Treeview.Heading", 
                       background="#1e40af", 
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))
        style.map("Treeview.Heading", background=[('active', '#3b82f6')])
        columnas = ("Paciente", "CI", "Especialidad", "Doctor", "Triaje")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", style="Treeview")
        anchos = [220, 100, 160, 200, 280]
        for col, ancho in zip(columnas, anchos):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")
        for c in citas:
            triaje_text = c.get("triaje", "Pendiente")
            self.tabla.insert("", "end", values=(
                c["paciente"], 
                c["ci"], 
                c["especialidad"], 
                c["doctor"], 
                triaje_text
            ))
        self.tabla.pack(fill="both", expand=True)

root = tk.Tk()
app = SaladeRecepcion(root)  
root.mainloop()