"""Interfaz de escritorio: panel de control del servicio de organización."""

import queue
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import ttk

from organizador.service import OrganizadorService

CARPETA_DESCARGAS = Path.home() / "Downloads"

# Paleta oscura tipo aplicación moderna.
COLOR_FONDO = "#0f172a"
COLOR_TARJETA = "#1a2338"
COLOR_BORDE = "#293349"
COLOR_TEXTO = "#e5eaf3"
COLOR_TEXTO_SECUNDARIO = "#8b96ad"
COLOR_ACTIVO = "#34d399"
COLOR_INACTIVO = "#5b6579"
COLOR_ACCION = "#3b82f6"
COLOR_ACCION_HOVER = "#2f6fe0"
COLOR_DETENER = "#ef4444"
COLOR_DETENER_HOVER = "#dc2626"

FUENTE_TITULO = ("Segoe UI Semibold", 17)
FUENTE_SUBTITULO = ("Segoe UI", 10)
FUENTE_ESTADO = ("Segoe UI Semibold", 11)
FUENTE_BOTON = ("Segoe UI Semibold", 11)
FUENTE_SECCION = ("Segoe UI Semibold", 10)
FUENTE_LOG = ("Consolas", 10)


class OrganizadorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cola: "queue.Queue[tuple]" = queue.Queue()
        self.servicio = OrganizadorService(
            CARPETA_DESCARGAS, on_organizado=self._on_organizado_hilo
        )
        self._trabajando = False

        self._configurar_ventana()
        self._configurar_estilos()
        self._construir_layout()
        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar)
        self.root.after(150, self._procesar_cola)

    # ---- construcción de la ventana ----------------------------------

    def _configurar_ventana(self):
        self.root.title("OrganizadorArchivosAI")
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry("600x680")
        self.root.minsize(480, 520)

    def _configurar_estilos(self):
        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")

        estilo.configure("Fondo.TFrame", background=COLOR_FONDO)
        estilo.configure("Tarjeta.TFrame", background=COLOR_TARJETA)

        estilo.configure(
            "Titulo.TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TITULO
        )
        estilo.configure(
            "Subtitulo.TLabel",
            background=COLOR_FONDO,
            foreground=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_SUBTITULO,
        )
        estilo.configure(
            "Seccion.TLabel",
            background=COLOR_FONDO,
            foreground=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_SECCION,
        )
        estilo.configure(
            "Estado.TLabel", background=COLOR_TARJETA, foreground=COLOR_TEXTO, font=FUENTE_ESTADO
        )
        estilo.configure(
            "EstadoDetalle.TLabel",
            background=COLOR_TARJETA,
            foreground=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_SUBTITULO,
        )

        estilo.configure(
            "Accion.TButton",
            background=COLOR_ACCION,
            foreground="#ffffff",
            font=FUENTE_BOTON,
            borderwidth=0,
            focuscolor=COLOR_ACCION,
            padding=(18, 10),
        )
        estilo.map(
            "Accion.TButton",
            background=[("active", COLOR_ACCION_HOVER), ("disabled", COLOR_INACTIVO)],
        )

        estilo.configure(
            "Detener.TButton",
            background=COLOR_DETENER,
            foreground="#ffffff",
            font=FUENTE_BOTON,
            borderwidth=0,
            focuscolor=COLOR_DETENER,
            padding=(18, 10),
        )
        estilo.map(
            "Detener.TButton",
            background=[("active", COLOR_DETENER_HOVER), ("disabled", COLOR_INACTIVO)],
        )

    def _construir_layout(self):
        contenedor = ttk.Frame(self.root, style="Fondo.TFrame", padding=24)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(3, weight=1)

        self._construir_encabezado(contenedor)
        self._construir_tarjeta_estado(contenedor)
        self._construir_boton(contenedor)
        self._construir_log(contenedor)

    def _construir_encabezado(self, padre):
        encabezado = ttk.Frame(padre, style="Fondo.TFrame")
        encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        ttk.Label(encabezado, text="OrganizadorArchivosAI", style="Titulo.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            encabezado,
            text=f"Vigilando: {CARPETA_DESCARGAS}",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(4, 0))

    def _construir_tarjeta_estado(self, padre):
        tarjeta = tk.Frame(
            padre, bg=COLOR_TARJETA, highlightbackground=COLOR_BORDE, highlightthickness=1
        )
        tarjeta.grid(row=1, column=0, sticky="ew", pady=(0, 16))

        interior = ttk.Frame(tarjeta, style="Tarjeta.TFrame", padding=16)
        interior.pack(fill="both", expand=True)

        self.canvas_estado = tk.Canvas(
            interior, width=14, height=14, bg=COLOR_TARJETA, highlightthickness=0
        )
        self.canvas_estado.grid(row=0, column=0, rowspan=2, padx=(0, 12))
        self._punto_estado = self.canvas_estado.create_oval(2, 2, 12, 12, fill=COLOR_INACTIVO, outline="")

        self.etiqueta_estado = ttk.Label(interior, text="Detenido", style="Estado.TLabel")
        self.etiqueta_estado.grid(row=0, column=1, sticky="w")

        self.etiqueta_detalle = ttk.Label(
            interior,
            text="La vigilancia aún no ha comenzado.",
            style="EstadoDetalle.TLabel",
        )
        self.etiqueta_detalle.grid(row=1, column=1, sticky="w")

        interior.columnconfigure(1, weight=1)

    def _construir_boton(self, padre):
        fila = ttk.Frame(padre, style="Fondo.TFrame")
        fila.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        self.boton_accion = ttk.Button(
            fila,
            text="Iniciar vigilancia",
            style="Accion.TButton",
            command=self._alternar_servicio,
        )
        self.boton_accion.pack(anchor="w")

    def _construir_log(self, padre):
        seccion = ttk.Frame(padre, style="Fondo.TFrame")
        seccion.grid(row=3, column=0, sticky="nsew")
        seccion.columnconfigure(0, weight=1)
        seccion.rowconfigure(1, weight=1)

        ttk.Label(seccion, text="ACTIVIDAD", style="Seccion.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        marco_log = tk.Frame(
            seccion, bg=COLOR_TARJETA, highlightbackground=COLOR_BORDE, highlightthickness=1
        )
        marco_log.grid(row=1, column=0, sticky="nsew")
        marco_log.columnconfigure(0, weight=1)
        marco_log.rowconfigure(0, weight=1)

        self.texto_log = tk.Text(
            marco_log,
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            font=FUENTE_LOG,
            relief="flat",
            padx=14,
            pady=12,
            wrap="word",
            state="disabled",
        )
        self.texto_log.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(marco_log, command=self.texto_log.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.texto_log.configure(yscrollcommand=scrollbar.set)

        self.texto_log.tag_configure("hora", foreground=COLOR_TEXTO_SECUNDARIO)
        self.texto_log.tag_configure("categoria", foreground=COLOR_ACTIVO)
        self.texto_log.tag_configure("aviso", foreground=COLOR_TEXTO_SECUNDARIO)

    # ---- lógica de estado ----------------------------------------------

    def _alternar_servicio(self):
        if self._trabajando:
            return
        if self.servicio.activo:
            self._detener_servicio()
        else:
            self._iniciar_servicio()

    def _iniciar_servicio(self):
        self._trabajando = True
        self.boton_accion.configure(state="disabled")
        self._actualizar_estado("Iniciando…", "Organizando archivos existentes.", COLOR_INACTIVO)

        def tarea():
            error = None
            try:
                self.servicio.iniciar()
            except FileNotFoundError as e:
                error = str(e)
            self.cola.put(("iniciado", error))

        threading.Thread(target=tarea, daemon=True).start()

    def _detener_servicio(self):
        self._trabajando = True
        self.boton_accion.configure(state="disabled")
        self._actualizar_estado("Deteniendo…", "Cerrando la vigilancia.", COLOR_INACTIVO)

        def tarea():
            self.servicio.detener()
            self.cola.put(("detenido", None))

        threading.Thread(target=tarea, daemon=True).start()

    def _on_organizado_hilo(self, nombre_archivo, categoria):
        # Llamado desde el hilo del watcher: solo encola, no toca la UI directamente.
        self.cola.put(("organizado", (nombre_archivo, categoria)))

    def _procesar_cola(self):
        try:
            while True:
                tipo, datos = self.cola.get_nowait()
                if tipo == "organizado":
                    nombre, categoria = datos
                    self._agregar_log(nombre, categoria)
                elif tipo == "iniciado":
                    self._trabajando = False
                    self.boton_accion.configure(state="normal")
                    if datos:
                        self._actualizar_estado("Error", datos, COLOR_DETENER)
                    else:
                        self.boton_accion.configure(text="Detener vigilancia", style="Detener.TButton")
                        self._actualizar_estado(
                            "Vigilando", "Organizando archivos nuevos automáticamente.", COLOR_ACTIVO
                        )
                elif tipo == "detenido":
                    self._trabajando = False
                    self.boton_accion.configure(state="normal", text="Iniciar vigilancia", style="Accion.TButton")
                    self._actualizar_estado("Detenido", "La vigilancia está pausada.", COLOR_INACTIVO)
        except queue.Empty:
            pass
        self.root.after(150, self._procesar_cola)

    def _actualizar_estado(self, titulo, detalle, color_punto):
        self.etiqueta_estado.configure(text=titulo)
        self.etiqueta_detalle.configure(text=detalle)
        self.canvas_estado.itemconfigure(self._punto_estado, fill=color_punto)

    def _agregar_log(self, nombre_archivo, categoria):
        hora = datetime.now().strftime("%H:%M:%S")
        self.texto_log.configure(state="normal")
        self.texto_log.insert("end", f"{hora}  ", "hora")
        self.texto_log.insert("end", f"{nombre_archivo}  →  ")
        self.texto_log.insert("end", f"{categoria}\n", "categoria")
        self.texto_log.configure(state="disabled")
        self.texto_log.see("end")

    def _al_cerrar(self):
        if self.servicio.activo:
            self.servicio.detener()
        self.root.destroy()


def main():
    root = tk.Tk()
    OrganizadorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
