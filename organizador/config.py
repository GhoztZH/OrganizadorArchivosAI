"""Configuración de categorías y mapeo de extensiones."""

CATEGORIA_OTROS = "Otros"

EXTENSIONES_POR_CATEGORIA = {
    "Documentos": {".pdf", ".docx", ".doc", ".txt", ".pptx", ".ppt"},
    "Hojas de cálculo": {".xlsx", ".xls", ".csv"},
    "Imágenes": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"},
    "Videos": {".mp4", ".avi", ".mkv", ".mov"},
    "Audio": {".mp3", ".wav", ".flac", ".aac"},
    "Comprimidos": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Instaladores": {".exe", ".msi"},
    "Codigo": {
    ".py", ".js", ".html", ".css",
    ".java", ".cs", ".cpp",
    ".c", ".php", ".sql",
    ".json", ".xml", ".yaml"
    },
}

EXTENSION_A_CATEGORIA = {
    extension: categoria
    for categoria, extensiones in EXTENSIONES_POR_CATEGORIA.items()
    for extension in extensiones
}

# Extensiones de descargas en progreso: se ignoran hasta que el navegador
# las renombre a su nombre final.
EXTENSIONES_TEMPORALES = {".tmp", ".crdownload", ".part", ".download"}
