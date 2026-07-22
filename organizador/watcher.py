"""Detección de archivos nuevos en una carpeta y organización automática."""

import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from organizador.config import EXTENSIONES_TEMPORALES
from organizador.organizer import organizar_archivo

INTERVALO_ESTABILIDAD_SEGUNDOS = 1.0
INTENTOS_MAXIMOS_ESTABILIDAD = 30


def _es_temporal(ruta: Path) -> bool:
    return ruta.suffix.lower() in EXTENSIONES_TEMPORALES


def _esperar_archivo_estable(ruta: Path) -> bool:
    """Espera hasta que el tamaño del archivo deje de cambiar (descarga finalizada).

    Devuelve False si el archivo desaparece antes de estabilizarse.
    """
    tamano_anterior = -1
    for _ in range(INTENTOS_MAXIMOS_ESTABILIDAD):
        if not ruta.exists():
            return False
        tamano_actual = ruta.stat().st_size
        if tamano_actual == tamano_anterior:
            return True
        tamano_anterior = tamano_actual
        time.sleep(INTERVALO_ESTABILIDAD_SEGUNDOS)
    return True


class ManejadorDescargas(FileSystemEventHandler):
    """Reacciona a archivos nuevos o renombrados y los organiza por categoría."""

    def __init__(self, carpeta_base: Path, on_organizado=None):
        self.carpeta_base = Path(carpeta_base)
        self.on_organizado = on_organizado

    def on_created(self, event):
        if event.is_directory:
            return
        self._procesar(Path(event.src_path))

    def on_moved(self, event):
        # Los navegadores suelen descargar a un archivo temporal y luego
        # renombrarlo (evento "moved") al nombre final dentro de la misma carpeta.
        if event.is_directory:
            return
        self._procesar(Path(event.dest_path))

    def _procesar(self, ruta: Path):
        if _es_temporal(ruta):
            return
        if not _esperar_archivo_estable(ruta):
            return
        nombre_original = ruta.name
        try:
            destino = organizar_archivo(ruta, self.carpeta_base)
        except FileNotFoundError:
            return
        if self.on_organizado is not None:
            self.on_organizado(nombre_original, destino.parent.name)


def iniciar_watcher(carpeta_base: Path, on_organizado=None) -> Observer:
    """Inicia la vigilancia de `carpeta_base` y devuelve el observador en marcha.

    Si se indica `on_organizado`, se llama con (nombre_archivo, categoria)
    cada vez que un archivo nuevo es organizado.
    """
    carpeta_base = Path(carpeta_base)
    manejador = ManejadorDescargas(carpeta_base, on_organizado=on_organizado)
    observer = Observer()
    observer.schedule(manejador, str(carpeta_base), recursive=False)
    observer.start()
    return observer
