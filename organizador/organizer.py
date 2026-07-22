"""Movimiento de archivos a su carpeta de categoría."""

import shutil
from pathlib import Path

from organizador.classifier import clasificar


def _ruta_disponible(destino: Path) -> Path:
    """Devuelve `destino` si no existe, o una variante con sufijo numérico si ya existe."""
    if not destino.exists():
        return destino

    contador = 1
    while True:
        candidato = destino.with_name(f"{destino.stem} ({contador}){destino.suffix}")
        if not candidato.exists():
            return candidato
        contador += 1


def organizar_archivo(ruta_archivo: Path, carpeta_base: Path) -> Path:
    """Mueve un archivo a la subcarpeta de su categoría dentro de `carpeta_base`.

    Devuelve la ruta final del archivo movido.
    """
    ruta_archivo = Path(ruta_archivo)
    carpeta_base = Path(carpeta_base)

    categoria = clasificar(ruta_archivo.name)
    carpeta_categoria = carpeta_base / categoria
    carpeta_categoria.mkdir(parents=True, exist_ok=True)

    destino = _ruta_disponible(carpeta_categoria / ruta_archivo.name)
    shutil.move(str(ruta_archivo), str(destino))
    return destino
