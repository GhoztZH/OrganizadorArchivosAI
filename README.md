# OrganizadorArchivosAI

Aplicación de escritorio en Python para Windows que organiza automáticamente los archivos de la carpeta Descargas, clasificándolos por categoría según su extensión.

## Categorías

| Categoría | Extensiones |
|---|---|
| Documentos | pdf, docx, doc, txt |
| Hojas de cálculo | xlsx, xls, csv |
| Imágenes | jpg, jpeg, png, gif, bmp, svg |
| Videos | mp4, avi, mkv, mov |
| Audio | mp3, wav, flac, aac |
| Comprimidos | zip, rar, 7z, tar, gz |
| Instaladores | exe, msi |
| Otros | cualquier extensión no listada |

## Estado del proyecto

En desarrollo. Actualmente implementado:

- [x] Clasificación de archivos por extensión (`organizador/classifier.py`)
- [x] Movimiento automático de archivos a su carpeta de categoría (`organizador/organizer.py`)
- [x] Detección de archivos nuevos en Descargas (`organizador/watcher.py`)
- [ ] Interfaz de escritorio (Tkinter)

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

_Pendiente: se documentará cuando el punto de entrada (`main.py`) esté disponible._
