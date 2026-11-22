import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

class SimuladorRadar:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Smart Antenna — MIMO Masivo 360°")
        self.root.configure(bg='#0E1117')
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        # Protocolo para cerrar con la X de Windows de forma segura
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)

        self.anim = None
        self.detectados = [False] * 6
        self.colores = ['#FF3B30', '#34C759', '#007AFF', '#FFCC00', '#AF52DE', '#5AC8FA']
        self.labels = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6']
        self.freq_actual = 28.0

        self.crear_interfaz()
        self.inicializar_grafico()

    def crear_interfaz(self):
        # --- Panel Izquierdo (Gráfico) ---
        self.frame_grafico = tk.Frame(self.root, bg='#0E1117')
        self.frame_grafico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Panel Derecho (Controles) ---
        self.frame_controles = tk.Frame(self.root, bg='#161920', width=380, padx=20, pady=20)
        self.frame_controles.pack(side=tk.RIGHT, fill=tk.Y)

        # Encabezados de la tabla
        headers = ['', '', 'AZ (°)', 'EL (°)', 'Pot (W)']
        for i, h in enumerate(headers):
            tk.Label(self.frame_controles, text=h, bg='#161920', fg='#AAAAAA',
                     font=('Arial', 9, 'bold')).grid(row=0, column=i, padx=6, pady=(10, 15))

        self.entries_az = []
        self.entries_el = []
        self.entries_pot = []

        # Valores iniciales (para que se vea como el video)
        valores_iniciales_az = [35, 135, 165, 210, 260, 315]
        valores_iniciales_el = [10, 20, 25, 15, 10, 18]
        valores_iniciales_pot = [0.95, 0.75, 0.65, 0.85, 0.90, 0.80]

        for u in range(6):
            # Cuadro de color
            tk.Label(self.frame_controles, bg=self.colores[u], width=2, height=1).grid(
                row=u+1, column=0, pady=12, padx=(5, 5))

            # Etiqueta de usuario
            tk.Label(self.frame_controles, text=self.labels[u], bg='#161920', fg='white',
                     font=('Arial', 10, 'bold'), width=3).grid(row=u+1, column=1, pady=12, padx=(0, 10))

            # Campo Azimut
            e_az = tk.Entry(self.frame_controles, width=8, bg='#222630', fg='white',
                            relief='solid', bd=1, insertbackground='white', justify='center')
            e_az.insert(0, str(valores_iniciales_az[u]))
            e_az.grid(row=u+1, column=2, padx=6, pady=12)
            self.entries_az.append(e_az)

            # Campo Elevación
            e_el = tk.Entry(self.frame_controles, width=8, bg='#222630', fg='white',
                            relief='solid', bd=1, insertbackground='white', justify='center')
            e_el.insert(0, str(valores_iniciales_el[u]))
            e_el.grid(row=u+1, column=3, padx=6, pady=12)
            self.entries_el.append(e_el)

            # Campo Potencia
            e_pot = tk.Entry(self.frame_controles, width=8, bg='#222630', fg='white',
                             relief='solid', bd=1, insertbackground='white', justify='center')
            e_pot.insert(0, str(valores_iniciales_pot[u]))
            e_pot.grid(row=u+1, column=4, padx=6, pady=12)
            self.entries_pot.append(e_pot)

        # Etiqueta de estado
        self.lbl_estado = tk.Label(self.frame_controles, text="● Esperando inicio de barrido...",
                                   bg='#161920', fg='#AAAAAA', font=('Arial', 9, 'bold'))
        self.lbl_estado.grid(row=8, column=0, columnspan=5, pady=(40, 10), sticky='w')

        # Campo de Frecuencia
        tk.Label(self.frame_controles, text="Frecuencia (GHz)", bg='#161920', fg='#CCCCCC',
                 font=('Arial', 9)).grid(row=9, column=0, columnspan=3, sticky='w', pady=5)
        self.entry_freq = tk.Entry(self.frame_controles, width=10, bg='#222630', fg='white',
                                   insertbackground='white', justify='center')
        self.entry_freq.insert(0, "28")
        self.entry_freq.grid(row=9, column=3, columnspan=2, sticky='e', pady=5)

        # Botones
        btn_iniciar = tk.Button(self.frame_controles, text="▶  INICIAR BARRIDO 360°", bg='#2C313C', fg='white',
                                font=('Arial', 10, 'bold'), activebackground='#3E4452', activeforeground='white',
                                relief='flat', command=self.iniciar_barrido)
        btn_iniciar.grid(row=10, column=0, columnspan=5, pady=(10, 8), sticky='we', ipady=6)

        btn_cerrar = tk.Button(self.frame_controles, text="CERRAR SIMULADOR", bg='#8E2822', fg='white',
                               font=('Arial', 9, 'bold'), activebackground='#C0392B', activeforeground='white',
                               relief='flat', command=self.cerrar_app)
        btn_cerrar.grid(row=11, column=0, columnspan=5, pady=4, sticky='we', ipady=4)

    def inicializar_grafico(self):
        plt.style.use('dark_background')
        self.fig = plt.Figure(figsize=(7.5, 6), facecolor='#0E1117')
        self.ax = self.fig.add_subplot(111, polar=True, facecolor='#0E1117')

        # Configuración del radar
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_rlim(0, 1.05)
        self.ax.set_rticks([0.25, 0.50, 0.75, 1.0])
        self.ax.set_yticklabels(['0.25', '0.50', '0.75', '1.0'], color='#888888', fontsize=8)
        self.ax.set_rlabel_position(45)
        self.ax.set_thetagrids(range(0, 360, 45), color='#888888', fontsize=9)
        self.ax.grid(color='#444444', linestyle='-', linewidth=0.6, alpha=0.6)
        self.ax.spines['polar'].set_color('#555555')

        # Título dinámico
        self.title = self.ax.set_title(
            "MIMO Masivo — Barrido 360° | UPA 8×8=64 elem | f=28.0 GHz | λ=10.71 mm",
            color='white', fontsize=11, fontweight='bold', pad=20
        )

        # Líneas y rellenos para los usuarios
        self.lineas_usuarios = {}
        self.rellenos_usuarios = {}
        for u in range(6):
            line, = self.ax.plot([], [], color=self.colores[u], linewidth=2)
            self.lineas_usuarios[self.labels[u]] = line
            fill = self.ax.fill_between([], [], [], color=self.colores[u], alpha=0.25)
            self.rellenos_usuarios[self.labels[u]] = fill

        # Línea de escaneo
        self.linea_escaneo, = self.ax.plot([], [], color='#00FFCC', alpha=0.7, linewidth=1.8)

        # Integrar en Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def calcular_haz(self, angulo_centro, elevacion_deg, potencia_w):
        theta = np.linspace(0, 2 * np.pi, 720)
        ang_rad = np.radians(angulo_centro % 360)
        diff = np.abs(theta - ang_rad)
        diff = np.where(diff > np.pi, 2 * np.pi - diff, diff)

        # Factor de elevación (a mayor elevación, menor proyección horizontal)
        factor_el = np.cos(np.radians(np.clip(elevacion_deg, 0, 85)))
        amplitud = np.clip(potencia_w, 0.1, 1.0) * factor_el

        # HPBW inversamente proporcional a la frecuencia
        ancho_haz = np.clip(14.0 * (28.0 / self.freq_actual), 4.0, 150.0)
        sigma = np.radians(ancho_haz) / 2.355
        r = amplitud * np.exp(-(diff ** 2) / (2 * sigma ** 2))
        return theta, r

    def iniciar_barrido(self):
        # Detener animación previa si existe
        if self.anim is not None and self.anim.event_source is not None:
            self.anim.event_source.stop()

        # Validar la frecuencia
        try:
            freq_ghz = float(self.entry_freq.get())
            if freq_ghz <= 0:
                raise ValueError
            self.freq_actual = freq_ghz
            lambda_mm = (3e8 / (freq_ghz * 1e9)) * 1000
            self.title.set_text(
                f"MIMO Masivo — Barrido 360° | UPA 8×8=64 elem | f={freq_ghz:.1f} GHz | λ={lambda_mm:.2f} mm"
            )
        except ValueError:
            messagebox.showerror("Error", "Ingrese una frecuencia válida en GHz.")
            return

        # Validar todos los campos de los usuarios
        for u in range(6):
            try:
                float(self.entries_az[u].get())
                float(self.entries_el[u].get())
                float(self.entries_pot[u].get())
            except ValueError:
                messagebox.showerror("Error", f"Verifique los datos del usuario {self.labels[u]}.")
                return

        # Reiniciar estado
        self.detectados = [False] * 6
        self.lbl_estado.config(text="⟳ Escaneando 360°... (0/6 usuarios)", fg='#F39C12')

        # Limpiar gráficos
        for u in range(6):
            lbl = self.labels[u]
            self.lineas_usuarios[lbl].set_data([], [])
            self.rellenos_usuarios[lbl].remove()
            self.rellenos_usuarios[lbl] = self.ax.fill_between([], [], [], color=self.colores[u], alpha=0.25)

        # Iniciar animación
        self.anim = animation.FuncAnimation(
            self.fig, self.actualizar_frame, frames=np.arange(0, 362, 2),
            interval=20, blit=False, repeat=False
        )
        self.canvas.draw()

    def actualizar_frame(self, frame):
        angulo_actual = frame % 360
        theta_scan = np.radians([angulo_actual, angulo_actual])
        self.linea_escaneo.set_data(theta_scan, [0, 1.0])

        for u in range(6):
            if not self.detectados[u]:
                try:
                    az_user = float(self.entries_az[u].get()) % 360
                    el_user = float(self.entries_el[u].get())
                    pot_user = float(self.entries_pot[u].get())
                except ValueError:
                    continue

                diff = abs(angulo_actual - az_user)
                if diff > 180:
                    diff = 360 - diff

                # Si el haz de escaneo está a ±2° del usuario, se detecta
                if diff <= 2:
                    self.detectados[u] = True
                    theta_u, r_u = self.calcular_haz(az_user, el_user, pot_user)

                    lbl = self.labels[u]
                    self.lineas_usuarios[lbl].set_data(theta_u, r_u)
                    self.rellenos_usuarios[lbl].remove()
                    self.rellenos_usuarios[lbl] = self.ax.fill_between(
                        theta_u, np.zeros_like(r_u), r_u, color=self.colores[u], alpha=0.28
                    )
                    
                    total = sum(self.detectados)
                    self.lbl_estado.config(text=f"⟳ Escaneando 360°... ({total}/6 usuarios)", fg='#F39C12')

        # Fin del barrido
        if frame >= 360:
            self.linea_escaneo.set_data([], [])
            total = sum(self.detectados)
            self.lbl_estado.config(text=f"✓ Barrido completo — {total}/6 usuarios detectados", fg='#2ECC71')

        return list(self.lineas_usuarios.values()) + [self.linea_escaneo]

    def cerrar_app(self):
        # Detener animación y cerrar ventana de forma segura
        if self.anim is not None:
            self.anim.event_source.stop()
            self.anim = None
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorRadar(root)
    root.mainloop()