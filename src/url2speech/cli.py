
import sys
from .core import process_url

def main():
    if len(sys.argv) <= 1:
        print("Uso: python -m url2speech.cli <URL> [--show=clean|summary|spoken]"); return
    url = sys.argv[1]; show = None
    if len(sys.argv) > 2 and sys.argv[2].startswith("--show="): show = sys.argv[2].split("=",1)[1].strip()
    out_dir, meta = process_url(url)
    print("\nModo:", meta['mode']); print("Idioma estimado:", meta['lang']); print("Carpeta:", out_dir); print("Archivos:")
    for k, v in meta['files'].items(): print(f"  - {k}: {v}")
    if show:
        path = meta['files'].get('clean') if show=="clean" else meta['files'].get('summary') if show=="summary" else meta['files'].get('spoken_text') if show=="spoken" else None
        if path and (show!="summary" or 'summary' in meta['files']):
            print(f"\n=== CONTENIDO: {show.upper()} ===\n"); print(open(path,"r",encoding="utf-8").read())
        else: print(f"\n(No hay contenido para --show={show})")

if __name__ == "__main__": main()
