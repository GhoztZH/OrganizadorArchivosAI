"""Punto de entrada: organiza Descargas y vigila cambios en tiempo real."""

import time
from pathlib import Path

from organizador.config import EXTENSIONES_TEMPORALES
from organizador.organizer import organizar_archivo
from organizador.watcher import iniciar_watcher

CARPETA_DESCARGAS = Path.home() / "Downloads"


def organizar_existentes(carpeta_base: Path) -> None:
    """Organiza los archivos que ya están en `carpeta_base` antes de vigilar nuevos."""
    for ruta in list(carpeta_base.iterdir()):
        if not ruta.is_file():
            continue
        if ruta.suffix.lower() in EXTENSIONES_TEMPORALES:
            continue
        try:
            organizar_archivo(ruta, carpeta_base)
        except OSError as error:
            print(f"No se pudo organizar {ruta.name}: {error}")


def main() -> None:
    if not CARPETA_DESCARGAS.is_dir():
        print(f"No se encontró la carpeta de Descargas en: {CARPETA_DESCARGAS}")
        return

    print(f"Organizando archivos existentes en {CARPETA_DESCARGAS}...")
    organizar_existentes(CARPETA_DESCARGAS)

    print("Vigilando nuevos archivos. Presiona Ctrl+C para detener.")
    observer = iniciar_watcher(CARPETA_DESCARGAS)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo...")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
