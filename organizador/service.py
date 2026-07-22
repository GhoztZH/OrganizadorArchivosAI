"""Servicio que encapsula el arranque, la organización inicial y el control del watcher."""

from pathlib import Path

from organizador.config import EXTENSIONES_TEMPORALES
from organizador.organizer import organizar_archivo
from organizador.watcher import iniciar_watcher


class OrganizadorService:
    """Coordina el barrido inicial y la vigilancia continua de una carpeta."""

    def __init__(self, carpeta_base: Path, on_organizado=None):
        self.carpeta_base = Path(carpeta_base)
        self.on_organizado = on_organizado
        self._observer = None

    @property
    def activo(self) -> bool:
        return self._observer is not None

    def organizar_existentes(self) -> None:
        """Organiza los archivos que ya están en la carpeta antes de vigilar nuevos."""
        for ruta in list(self.carpeta_base.iterdir()):
            if not ruta.is_file():
                continue
            if ruta.suffix.lower() in EXTENSIONES_TEMPORALES:
                continue
            try:
                destino = organizar_archivo(ruta, self.carpeta_base)
            except OSError as error:
                print(f"No se pudo organizar {ruta.name}: {error}")
                continue
            if self.on_organizado is not None:
                self.on_organizado(ruta.name, destino.parent.name)

    def iniciar(self) -> None:
        """Organiza lo existente y arranca la vigilancia de nuevos archivos."""
        if self.activo:
            return
        if not self.carpeta_base.is_dir():
            raise FileNotFoundError(f"No se encontró la carpeta: {self.carpeta_base}")
        self.organizar_existentes()
        self._observer = iniciar_watcher(self.carpeta_base, on_organizado=self.on_organizado)

    def detener(self) -> None:
        """Detiene la vigilancia si está activa."""
        if not self.activo:
            return
        self._observer.stop()
        self._observer.join()
        self._observer = None
