"""Clasificación de archivos según su extensión."""

from pathlib import Path

from organizador.config import CATEGORIA_OTROS, EXTENSION_A_CATEGORIA


def clasificar(nombre_archivo: str) -> str:
    """Devuelve la categoría correspondiente a un archivo según su extensión."""
    extension = Path(nombre_archivo).suffix.lower()
    return EXTENSION_A_CATEGORIA.get(extension, CATEGORIA_OTROS)
