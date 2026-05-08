import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import re
from database import DATA_FALSA
import json

TEXT_DIR = "Backend/uploads/textos"
JSON_FILE = "Backend/uploads/data.json"
TEXT_DIR = "Backend/uploads/textos"


class ValidadorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Kode - Refactor Ético (Layout Corregido)")
        # Maximizar para mejor visibilidad
        self.root.state('zoomed') 
        
        self.archivos = [f for f in os.listdir(TEXT_DIR) if f.endswith('.txt')]
        self.indice = 0
        self.mapeo_cambios = {}

        # --- Interfaz Superior ---
        self.lbl_info = tk.Label(root, text="", font=('Consolas', 12, 'bold'), fg="#2c3e50")
        self.lbl_info.pack(pady=10)

        # --- Contenedor Principal (Grid para control total) ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill='both', padx=20)
        self.main_frame.columnconfigure(0, weight=1, uniform="group1") # Izquierda
        self.main_frame.columnconfigure(1, weight=0)                  # Centro (Menu)
        self.main_frame.columnconfigure(2, weight=1, uniform="group1") # Derecha
        self.main_frame.rowconfigure(0, weight=1)

        # 1. Panel Izquierdo: Original
        self.txt_original = scrolledtext.ScrolledText(self.main_frame, wrap='word', font=('Segoe UI', 11))
        self.txt_original.grid(row=0, column=0, sticky='nsew', padx=5)
        
        # 2. Panel Central: Gestión
        self.frame_gestion = tk.Frame(self.main_frame, width=200)
        self.frame_gestion.grid(row=0, column=1, sticky='ns', padx=10)

        tk.Label(self.frame_gestion, text="Añadir Manual:", font=('Arial', 9)).pack()
        self.ent_manual = tk.Entry(self.frame_gestion)
        self.ent_manual.pack(pady=2)
        tk.Button(self.frame_gestion, text="➕ Añadir", command=self.agregar_manual).pack(pady=5)

        tk.Label(self.frame_gestion, text="Detectadas:").pack(pady=(10,0))
        self.lista_palabras = tk.Listbox(self.frame_gestion, width=20, height=10)
        self.lista_palabras.pack(pady=5)
        
        self.combo_opciones = ttk.Combobox(self.frame_gestion, state="readonly")
        self.combo_opciones.pack(pady=5)

        for cat in DATA_FALSA.keys():
            tk.Button(self.frame_gestion, text=cat, width=15, 
                      command=lambda c=cat: self.cargar_opciones(c)).pack(pady=2)

        tk.Button(self.frame_gestion, text="REEMPLAZAR ➔", bg="#3498db", fg="white", font=('Arial', 10, 'bold'),
                  command=self.aplicar_cambio).pack(pady=20)

        # 3. Panel Derecho: Resultado
        self.txt_preview = scrolledtext.ScrolledText(self.main_frame, wrap='word', font=('Segoe UI', 11), bg="#f8f9fa")
        self.txt_preview.grid(row=0, column=2, sticky='nsew', padx=5)

        # --- Barra Inferior ---
        nav_frame = tk.Frame(root, height=50)
        nav_frame.pack(fill='x', side='bottom', pady=10)
        tk.Button(nav_frame, text="Siguiente Historia ➔", command=self.cargar_siguiente).pack(side='right', padx=20)
        tk.Button(nav_frame, text="💾 GUARDAR CAMBIOS", bg="#27ae60", fg="white", font=('Arial', 10, 'bold'),
                  command=self.guardar_final).pack(side='right')

        # Sincronización de Scroll (Opcional pero útil)
        def sync_scroll(*args):
            self.txt_original.yview(*args)
            self.txt_preview.yview(*args)
        
        self.txt_original.config(yscrollcommand=lambda *args: self.sync_views(self.txt_preview, *args))
        self.txt_preview.config(yscrollcommand=lambda *args: self.sync_views(self.txt_original, *args))

        self.cargar_siguiente()

    def sync_views(self, other_widget, *args):
        other_widget.yview_moveto(args[0])

    def agregar_manual(self):
        nueva = self.ent_manual.get().strip()
        if nueva and nueva not in self.lista_palabras.get(0, tk.END):
            self.lista_palabras.insert(tk.END, nueva)
            self.ent_manual.delete(0, tk.END)

    def cargar_opciones(self, categoria):
        self.combo_opciones['values'] = DATA_FALSA[categoria]
        self.combo_opciones.set(f"Ver {categoria}")

    def aplicar_cambio(self):
        palabra_real = self.lista_palabras.get(tk.ACTIVE)
        falsa_opcion = self.combo_opciones.get()
        if palabra_real and falsa_opcion and not falsa_opcion.startswith("Ver"):
            self.mapeo_cambios[palabra_real] = falsa_opcion
            self.actualizar_preview()

    def actualizar_preview(self):
        texto = self.txt_original.get('1.0', tk.END)
        for original, reemplazo in self.mapeo_cambios.items():
            pattern = re.compile(re.escape(original), re.IGNORECASE)
            texto = pattern.sub(reemplazo, texto)
        self.txt_preview.delete('1.0', tk.END)
        self.txt_preview.insert(tk.END, texto)

    def cargar_siguiente(self):
        if self.indice < len(self.archivos):
            self.mapeo_cambios = {}
            nombre = self.archivos[self.indice]
            self.lbl_info.config(text=f"ARCHIVO ACTUAL: {nombre}")
            with open(os.path.join(TEXT_DIR, nombre), 'r', encoding='utf-8') as f:
                contenido = f.read()
            self.txt_original.delete('1.0', tk.END)
            self.txt_original.insert(tk.END, contenido)
            sugerencias = set(re.findall(r'(?<![.!?]\s)\b[A-Z][a-z]+\b', contenido))
            self.lista_palabras.delete(0, tk.END)
            for s in sorted(sugerencias):
                self.lista_palabras.insert(tk.END, s)
            self.actualizar_preview()
            self.indice += 1
        else:
            messagebox.showinfo("Fin", "Revisiones completadas.")

    def guardar_final(self):
        # 1. Obtener el nombre del archivo que estamos editando
        nombre_archivo = self.archivos[self.indice - 1]
        
        # 2. Guardar el contenido de texto modificado (lo que ves en el panel derecho)
        # Por esto (la forma correcta y segura):
        nuevo_texto = self.txt_preview.get('1.0', tk.END).strip()
        ruta_txt = os.path.join(TEXT_DIR, nombre_archivo)
        
        with open(ruta_txt, 'w', encoding='utf-8') as f:
            f.write(nuevo_texto)

        # 3. ACTUALIZAR EL JSON PARA VOLVERLO TRUE
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
            
            # Buscamos la historia en la lista por su nombre de archivo
            modificado = False
            for historia in datos:
                # Comparamos con el campo 'txt_ref' que tienes en tu JSON
                if historia.get("txt_ref") == nombre_archivo:
                    historia["revisado"] = True  # <--- AQUÍ SE HACE LA MAGIA
                    modificado = True
                    break
            
            # 4. Sobrescribir el JSON con el nuevo estado
            if modificado:
                with open(JSON_FILE, "w", encoding="utf-8") as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                
                messagebox.showinfo("Éxito", f"Historia '{nombre_archivo}' validada y publicada.")
            else:
                messagebox.showwarning("Aviso", "Se guardó el texto pero no se encontró la referencia en data.json")
        else:
            messagebox.showerror("Error", "No se encontró el archivo data.json")



if __name__ == "__main__":
    root = tk.Tk()
    app = ValidadorPro(root)
    root.mainloop()