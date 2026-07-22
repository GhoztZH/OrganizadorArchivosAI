"""Punto de entrada: organiza Descargas y vigila cambios en tiempo real."""

import time
from pathlib import Path

from organizador.service import OrganizadorService

CARPETA_DESCARGAS = Path.home() / "Downloads"


def main() -> None:
    servicio = OrganizadorService(CARPETA_DESCARGAS)

    print(f"Organizando archivos existentes en {CARPETA_DESCARGAS}...")
    try:
        servicio.iniciar()
    except FileNotFoundError as error:
        print(error)
        return

    print("Vigilando nuevos archivos. Presiona Ctrl+C para detener.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo...")
    finally:
        servicio.detener()


if __name__ == "__main__":
    main()
