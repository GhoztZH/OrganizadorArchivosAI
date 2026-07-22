# OrganizadorArchivosAI

Aplicación de escritorio en Python para Windows que organiza automáticamente los archivos de la carpeta Descargas, clasificándolos por categoría según su extensión.

## Categorías

| Categoría | Extensiones |
|---|---|
| Documentos | pdf, docx, doc, txt, pptx, ppt |
| Hojas de cálculo | xlsx, xls, csv |
| Imágenes | jpg, jpeg, png, gif, bmp, svg |
| Videos | mp4, avi, mkv, mov |
| Audio | mp3, wav, flac, aac |
| Comprimidos | zip, rar, 7z, tar, gz |
| Instaladores | exe, msi |
| Codigo | py, js, html, css, java, cs, cpp, c, php, sql, json, xml, yaml |
| Otros | cualquier extensión no listada |

El mapeo completo vive en `organizador/config.py`.

## Estado del proyecto

En desarrollo. Actualmente implementado:

- [x] Clasificación de archivos por extensión (`organizador/classifier.py`)
- [x] Movimiento automático de archivos a su carpeta de categoría (`organizador/organizer.py`)
- [x] Detección de archivos nuevos en Descargas (`organizador/watcher.py`)
- [x] Servicio reutilizable de arranque/parada (`organizador/service.py`)
- [x] Interfaz de escritorio (`gui.py`, Tkinter)

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

**Interfaz de escritorio:**

```bash
python gui.py
```

Muestra el estado de la vigilancia y un registro de actividad. El botón alterna entre iniciar y detener; al iniciar, organiza primero lo que ya esté en Descargas y luego vigila archivos nuevos en tiempo real.

**Modo consola:**

```bash
python main.py
```

Mismo comportamiento que la GUI pero por línea de comandos, hasta presionar `Ctrl+C`.
