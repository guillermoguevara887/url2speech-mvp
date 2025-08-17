# URL2Speech MVP (Desktop, 100% local)

Objetivo: URL → texto limpio → si es corto lo lee, si es largo lo resume → audio WAV offline.

## Entorno virtual e instalación
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar
```bash
# GUI
python -m url2speech.gui

# CLI
python -m url2speech.cli "https://www.ufg.edu.sv/"
```
