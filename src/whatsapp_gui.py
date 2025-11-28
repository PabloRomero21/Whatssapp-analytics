import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wordcloud import WordCloud
from datetime import date
import whatsapp_utiles as utiles
from whatsapp_loader import leer_log_whatsapp

class RangeSlider(tk.Canvas):
    def __init__(self, master, min_val, max_val, width=400, height=40, 
                 line_color="#cccccc", active_color="#075E54", handle_color="#128C7E",
                 command_update=None, command_drag=None, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.min_val = min_val
        self.max_val = max_val
        self.padding = 20
        self.enabled = True  
        
        # Colores
        self.col_active = active_color
        self.col_handle = handle_color
        self.col_disabled = "#999999"
        
        self.command_update = command_update 
        self.command_drag = command_drag

        # Geometría inicial
        self.width_canvas = width
        self.height_canvas = height
        self.line_y = height // 2
        self.line_start = self.padding
        self.line_end = width - self.padding
        self.pixel_range = self.line_end - self.line_start
        
        self.pos_left = self.line_start
        self.pos_right = self.line_end
        
        # Elementos Gráficos
        self.bg_line = self.create_line(self.line_start, self.line_y, self.line_end, self.line_y, 
                                        fill=line_color, width=4, capstyle=tk.ROUND)
        
        self.active_line = self.create_line(self.pos_left, self.line_y, self.pos_right, self.line_y, 
                                            fill=self.col_active, width=4, capstyle=tk.ROUND)
        
        self.handle_left = self.create_oval(0, 0, 0, 0, fill=self.col_handle, outline="white", width=2, tags="left")
        self.handle_right = self.create_oval(0, 0, 0, 0, fill=self.col_handle, outline="white", width=2, tags="right")
        
        self.update_graphics()

        # Bindings
        self.tag_bind("left", "<Button-1>", self.start_drag)
        self.tag_bind("right", "<Button-1>", self.start_drag)
        self.tag_bind("left", "<B1-Motion>", self.on_drag_left)
        self.tag_bind("right", "<B1-Motion>", self.on_drag_right)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Configure>", self.on_resize)

    def set_state(self, state="normal"):
        """Habilita o deshabilita la interacción y cambia colores visualmente."""
        self.enabled = (state == "normal")
        
        color_line = self.col_active if self.enabled else self.col_disabled
        color_handle = self.col_handle if self.enabled else self.col_disabled
        
        self.itemconfig(self.active_line, fill=color_line)
        self.itemconfig(self.handle_left, fill=color_handle)
        self.itemconfig(self.handle_right, fill=color_handle)

    def on_resize(self, event):
        val_l, val_r = self.get_values()
        self.width_canvas = event.width
        self.line_end = self.width_canvas - self.padding
        self.pixel_range = self.line_end - self.line_start
        self.coords(self.bg_line, self.line_start, self.line_y, self.line_end, self.line_y)
        self.pos_left = self.value_to_pixel(val_l)
        self.pos_right = self.value_to_pixel(val_r)
        self.update_graphics()

    def start_drag(self, event):
        if not self.enabled: return
        self.start_x = event.x

    def pixel_to_value(self, pixel):
        if self.pixel_range <= 0: return self.min_val
        ratio = (pixel - self.line_start) / self.pixel_range
        return int(self.min_val + (self.max_val - self.min_val) * ratio)

    def value_to_pixel(self, value):
        if self.max_val == self.min_val: return self.line_start
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return self.line_start + (ratio * self.pixel_range)

    def on_drag_left(self, event):
        if not self.enabled: return
        new_x = min(max(event.x, self.line_start), self.pos_right - 10) 
        self.pos_left = new_x
        self.update_graphics()
        if self.command_drag: self.command_drag(*self.get_values())

    def on_drag_right(self, event):
        if not self.enabled: return
        new_x = max(min(event.x, self.line_end), self.pos_left + 10) 
        self.pos_right = new_x
        self.update_graphics()
        if self.command_drag: self.command_drag(*self.get_values())
        
    def on_release(self, event):
        if not self.enabled: return
        if self.command_update: self.command_update(*self.get_values())

    def update_graphics(self):
        r = 8
        self.coords(self.handle_left, self.pos_left-r, self.line_y-r, self.pos_left+r, self.line_y+r)
        self.coords(self.handle_right, self.pos_right-r, self.line_y-r, self.pos_right+r, self.line_y+r)
        self.coords(self.active_line, self.pos_left, self.line_y, self.pos_right, self.line_y)

    def get_values(self):
        v1 = self.pixel_to_value(self.pos_left)
        v2 = self.pixel_to_value(self.pos_right)
        return sorted((v1, v2))

    def set_range(self, min_v, max_v):
        self.min_val = min_v
        self.max_val = max_v
        self.pos_left = self.line_start
        self.pos_right = self.line_end
        self.update_graphics()


class WhatsAppAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Analytics")
        self.root.geometry("1000x900")
        
        self.mensajes_todos = [] 
        self.mensajes = []      
        self.filename = None

        style = ttk.Style()
        style.theme_use('clam')
        
        # --- Panel Superior ---
        frame_top = ttk.Frame(self.root, padding="10")
        frame_top.pack(fill=tk.X)
        
        self.btn_load = ttk.Button(frame_top, text="📂 Cargar Chat (.txt)", command=self.cargar_fichero)
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        self.lbl_status = ttk.Label(frame_top, text="Ningún archivo cargado", font=("Arial", 10, "italic"))
        self.lbl_status.pack(side=tk.LEFT, padx=10)
        
        self.lbl_stats = ttk.Label(frame_top, text="", font=("Arial", 10, "bold"), foreground="#075E54")
        self.lbl_stats.pack(side=tk.RIGHT, padx=10)

        # --- Panel de Filtro ---
        self.crear_panel_filtro()

        # --- Notebook ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_users = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_users, text="👥 Actividad por Usuario")
        
        self.tab_time = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_time, text="🕒 Análisis Temporal")
        
        self.tab_words = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_words, text="💬 Nube de Palabras")

        self.crear_panel_usuarios()
        self.crear_panel_tiempo()
        self.crear_panel_palabras()

        self.toggle_interface(enable=False)

    def toggle_interface(self, enable=True):
        """Habilita o deshabilita los controles de la interfaz (excepto cargar)."""
        state_val = "normal" if enable else "disabled"
        
        # 1. Slider
        self.range_slider.set_state(state_val)
        
        # 2. Pestañas del Notebook (Iteramos para deshabilitarlas)
        for tab_id in self.notebook.tabs():
            self.notebook.tab(tab_id, state=state_val)
            
        # 3. Combo box de usuarios
        if enable:
            self.combo_users.config(state="readonly")
        else:
            self.combo_users.config(state="disabled")

    def crear_panel_filtro(self):
        self.frame_filtro = ttk.LabelFrame(self.root, text="📅 Filtrar por rango de fechas", padding="10")
        self.frame_filtro.pack(fill=tk.X, padx=10, pady=5)

        self.str_fecha_inicio = tk.StringVar(value="--/--/--")
        self.str_fecha_fin = tk.StringVar(value="--/--/--")

        frame_interno = ttk.Frame(self.frame_filtro)
        frame_interno.pack(fill=tk.X)
        
        ttk.Label(frame_interno, textvariable=self.str_fecha_inicio, font=("Arial", 10, "bold"), foreground="#075E54").pack(side=tk.LEFT, padx=10)
        ttk.Label(frame_interno, textvariable=self.str_fecha_fin, font=("Arial", 10, "bold"), foreground="#075E54").pack(side=tk.RIGHT, padx=10)

        self.range_slider = RangeSlider(self.frame_filtro, min_val=0, max_val=100, height=40, width=900,
                                        command_drag=self.actualizar_etiquetas_drag,
                                        command_update=self.ejecutar_filtro_release)
        self.range_slider.pack(fill=tk.X, padx=10, pady=5)

    def cargar_fichero(self):
        filepath = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")])
        if not filepath: return
        
        try:
            self.mensajes_todos = leer_log_whatsapp(filepath)
            if not self.mensajes_todos:
                messagebox.showwarning("Aviso", "No se han encontrado mensajes válidos.")
                return
                
            self.filename = filepath.split("/")[-1]
            self.lbl_status.config(text=f"Archivo: {self.filename}")

            self.toggle_interface(enable=True)

            fecha_min, fecha_max = utiles.calcula_rango_fechas(self.mensajes_todos)
            min_ord = fecha_min.toordinal()
            max_ord = fecha_max.toordinal()
            
            self.range_slider.set_range(min_ord, max_ord)
            self.actualizar_etiquetas_drag(min_ord, max_ord)
            self.ejecutar_filtro_release(min_ord, max_ord)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo:\n{e}")
            print(e)
            if not self.mensajes_todos:
                self.toggle_interface(enable=False)

    def actualizar_etiquetas_drag(self, val_min, val_max):
        f_ini = date.fromordinal(int(val_min))
        f_fin = date.fromordinal(int(val_max))
        self.str_fecha_inicio.set(f_ini.strftime("%d/%m/%Y"))
        self.str_fecha_fin.set(f_fin.strftime("%d/%m/%Y"))

    def ejecutar_filtro_release(self, val_min, val_max):
        if not self.mensajes_todos: return
        f_ini = date.fromordinal(int(val_min))
        f_fin = date.fromordinal(int(val_max))
        
        self.mensajes = utiles.filtra_mensajes_por_fechas(self.mensajes_todos, fecha_inicio=f_ini, fecha_fin=f_fin)
        
        self.lbl_stats.config(text=f"Mostrando: {len(self.mensajes)} / {len(self.mensajes_todos)} msgs")
        self.actualizar_graficas()

    def crear_panel_usuarios(self):
        self.fig_users = plt.Figure(figsize=(10, 5), dpi=100)
        self.ax_pie = self.fig_users.add_subplot(121)
        self.ax_len = self.fig_users.add_subplot(122)
        self.fig_users.tight_layout(pad=4.0)
        self.canvas_users = FigureCanvasTkAgg(self.fig_users, master=self.tab_users)
        self.canvas_users.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def crear_panel_tiempo(self):
        self.fig_time = plt.Figure(figsize=(10, 8), dpi=100)
        self.ax_hour = self.fig_time.add_subplot(211)
        self.ax_week = self.fig_time.add_subplot(212)
        self.fig_time.subplots_adjust(hspace=0.5)
        self.canvas_time = FigureCanvasTkAgg(self.fig_time, master=self.tab_time)
        self.canvas_time.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.lbl_dia_top = ttk.Label(self.tab_time, text="", font=("Arial", 12, "bold"))
        self.lbl_dia_top.pack(side=tk.BOTTOM, pady=5)

    def crear_panel_palabras(self):
        frame_ctrl = ttk.Frame(self.tab_words)
        frame_ctrl.pack(fill=tk.X, pady=5)
        ttk.Label(frame_ctrl, text="Generar nube para:").pack(side=tk.LEFT, padx=5)
        self.combo_users = ttk.Combobox(frame_ctrl, state="disabled") 
        self.combo_users.pack(side=tk.LEFT, padx=5)
        self.combo_users.bind("<<ComboboxSelected>>", self.actualizar_palabras)
        self.fig_words = plt.Figure(figsize=(10, 5), dpi=100)
        self.ax_words = self.fig_words.add_subplot(111)
        self.ax_words.axis("off")
        self.fig_words.tight_layout(pad=1.0)
        self.canvas_words = FigureCanvasTkAgg(self.fig_words, master=self.tab_words)
        self.canvas_words.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def actualizar_graficas(self):
        if not self.mensajes:
            self.ax_pie.clear()
            self.ax_len.clear()
            self.ax_hour.clear()
            self.ax_week.clear()
            self.canvas_users.draw()
            self.canvas_time.draw()
            self.lbl_dia_top.config(text="Sin mensajes en este rango")
            return

        dict_msgs = utiles.cuenta_mensajes_por_usuario(self.mensajes)
        self.ax_pie.clear()
        if dict_msgs:
            self.ax_pie.pie(dict_msgs.values(), labels=dict_msgs.keys(), autopct='%1.1f%%', startangle=90)
            self.ax_pie.set_title("Mensajes por Usuario")
        
        dict_len = utiles.calcula_longitud_media_por_usuario(self.mensajes)
        self.ax_len.clear()
        if dict_len:
            usuarios = list(dict_len.keys())
            longitudes = list(dict_len.values())
            colores = plt.cm.Paired(range(len(usuarios)))
            self.ax_len.bar(usuarios, longitudes, color=colores)
            self.ax_len.set_title("Longitud Media (caracteres)")
            self.ax_len.tick_params(axis='x', rotation=45)
        self.canvas_users.draw()

        dict_horas = utiles.cuenta_mensajes_por_hora(self.mensajes)
        self.ax_hour.clear()
        self.ax_hour.bar(dict_horas.keys(), dict_horas.values(), color='skyblue', edgecolor='black')
        self.ax_hour.set_xticks(range(0, 24))
        self.ax_hour.set_xlabel("Hora")
        self.ax_hour.set_ylabel("Mensajes")
        self.ax_hour.set_title("Actividad por hora")
        self.ax_hour.grid(axis='y', linestyle='--', alpha=0.7)
        
        dict_dias = utiles.cuenta_mensajes_por_dia_semana(self.mensajes)
        self.ax_week.clear()
        if dict_dias:
            dias = list(dict_dias.keys())
            conteos = list(dict_dias.values())
            self.ax_week.bar(dias, conteos, color='salmon', edgecolor='black')
            self.ax_week.set_title("Actividad por Día de la Semana")
            self.ax_week.set_xlabel("Día")
            self.ax_week.set_ylabel("Mensajes")
            self.ax_week.grid(axis='y', linestyle='--', alpha=0.6)
        self.canvas_time.draw()

        dia_top = utiles.detecta_dia_mas_activo(self.mensajes)
        if dia_top:
            fecha_obj = dia_top[0]
            fecha_str = fecha_obj.strftime("%d/%m/%Y")
            self.lbl_dia_top.config(text=f"📅 Día más activo: {fecha_str} ({dia_top[1]} msgs)")
        else:
            self.lbl_dia_top.config(text="")

        seleccion_actual = self.combo_users.get()
        usuarios_disponibles = list(dict_msgs.keys())
        self.combo_users['values'] = usuarios_disponibles
        if usuarios_disponibles:
            if seleccion_actual in usuarios_disponibles:
                self.combo_users.set(seleccion_actual)
            else:
                self.combo_users.current(0)
            self.actualizar_palabras()
        else:
            self.combo_users.set('')
            self.ax_words.clear()
            self.ax_words.axis("off")
            self.canvas_words.draw()

    def actualizar_palabras(self, event=None):
        if not self.mensajes: return
        user_sel = self.combo_users.get()
        if not user_sel: return
        frecuencias = dict(utiles.analiza_palabras_caracteristicas(self.mensajes, user_sel, n=100))
        
        self.ax_words.clear()
        self.ax_words.axis("off") 
        if not frecuencias:
            self.ax_words.text(0.5, 0.5, "Sin datos suficientes", ha='center', va='center', fontsize=14)
        else:
            wc = WordCloud(background_color="white", width=800, height=400, colormap="viridis", max_words=100).generate_from_frequencies(frecuencias)
            self.ax_words.imshow(wc, interpolation='bilinear')
            self.ax_words.set_title(f"Nube de palabras: {user_sel}", fontsize=14)
        self.canvas_words.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppAnalyzerApp(root)
    root.mainloop()