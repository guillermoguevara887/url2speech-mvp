
import tkinter as tk
from tkinter import ttk, messagebox
from .core import process_url

def run_gui():
    root = tk.Tk()
    root.title("URL → Resumen/Audio (local)")
    root.geometry("900x640")
    root.resizable(True, True)

    url_var = tk.StringVar()

    top = ttk.Frame(root); top.pack(fill=tk.X, padx=10, pady=10)
    ttk.Label(top, text="Ingresa URL:").pack(side=tk.LEFT, padx=(0,8))
    url_entry = ttk.Entry(top, textvariable=url_var); url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True); url_entry.focus()
    btn = ttk.Button(top, text="Procesar"); btn.pack(side=tk.LEFT, padx=8)
    status = ttk.Label(root, text="Listo."); status.pack(anchor=tk.W, padx=12)

    tabs = ttk.Notebook(root); tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    frame_clean = ttk.Frame(tabs); frame_summary = ttk.Frame(tabs); frame_spoken = ttk.Frame(tabs)
    tabs.add(frame_clean, text="Texto limpio (scraping)")
    tabs.add(frame_summary, text="Resumen (si aplica)")
    tabs.add(frame_spoken, text="Texto a locutar")

    txt_clean = tk.Text(frame_clean, wrap=tk.WORD); txt_clean.pack(fill=tk.BOTH, expand=True)
    txt_summary = tk.Text(frame_summary, wrap=tk.WORD); txt_summary.pack(fill=tk.BOTH, expand=True)
    txt_spoken = tk.Text(frame_spoken, wrap=tk.WORD); txt_spoken.pack(fill=tk.BOTH, expand=True)

    paths_box = tk.Text(root, height=6, wrap=tk.WORD); paths_box.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0,10))

    def on_process():
        url = (url_var.get() or "").strip()
        if not url: messagebox.showwarning("Falta URL", "Por favor ingresa una URL."); return
        btn.config(state=tk.DISABLED); status.config(text="Procesando...")
        root.after(50, lambda: do_work(url))

    def do_work(url):
        try:
            out_dir, meta = process_url(url)
            def read(p):
                try: return open(p,"r",encoding="utf-8").read().strip()
                except Exception: return ""
            clean = read(meta['files']['clean']); spoken = read(meta['files']['spoken_text']); summary = read(meta['files'].get('summary',"")) if 'summary' in meta['files'] else ""
            txt_clean.delete("1.0", tk.END); txt_clean.insert("1.0", clean)
            txt_summary.delete("1.0", tk.END); txt_summary.insert("1.0", summary if summary else "(No aplica: texto corto)")
            txt_spoken.delete("1.0", tk.END); txt_spoken.insert("1.0", spoken)

            lines=[f"Modo: {'TEXTO CORTO' if meta['mode']=='short' else 'RESUMEN'}  |  Idioma estimado: {meta['lang']}",
                   f"Carpeta: {out_dir}"] + [f" - {k}: {v}" for k,v in meta['files'].items()]
            paths_box.delete("1.0", tk.END); paths_box.insert("1.0", "\n".join(lines))
            status.config(text="Listo ✅ (revisa las pestañas)")
        except Exception as e:
            status.config(text=f"Error: {e}"); messagebox.showerror("Error", str(e))
        finally:
            btn.config(state=tk.NORMAL)

    btn.config(command=on_process)
    root.mainloop()

def main(): run_gui()
