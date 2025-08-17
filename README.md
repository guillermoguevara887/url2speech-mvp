# URL2Speech – Desktop MVP (100% Local)

Convert any web page into **clean text** and **audio** in seconds.  
If the page is **short** (≤60 words), it is read as-is.  
If it’s **long**, the app creates an **extractive summary (~180 words)** and reads that instead.  
Everything runs **offline** on your computer — no cloud, no external APIs.

---

## ✨ Features
- **Local-only**: privacy-friendly; no external services required.
- **Two modes**:
  - **Short text** → read everything.
  - **Long text** → extractive summary (frequency-based sentence scoring).
- **Offline TTS** with `pyttsx3` → generates a `.wav` file.
- **Transparent outputs**: saves `clean.txt`, `summary.txt` (if applicable), `spoken_text.txt`, `audio.wav`, and `meta.json`.
- Works via **GUI (Tkinter)** or **CLI**.

---

## 📂 Project Structure
```
url2speech-mvp/
├─ src/
│  └─ url2speech/
│     ├─ __init__.py
│     ├─ core.py        # extraction/cleanup/summarization/TTS
│     ├─ gui.py         # Tkinter GUI
│     └─ cli.py         # CLI entry point
├─ outputs/             # runtime results (one folder per processed URL)
│  └─ .gitkeep
├─ web/                 # optional static landing for Vercel
│  ├─ index.html
│  └─ vercel.json
├─ .gitignore
├─ LICENSE
├─ README.md
├─ requirements.txt
└─ main.py              # convenience launcher for the GUI
```

---

## ⚙️ Requirements
- **Python 3.10+**
- OS notes:
  - **Windows**: built-in voices (SAPI5) usually work out of the box.
  - **Linux**: may require `python3-tk` (for Tkinter) and `espeak` for TTS.
  - **macOS**: ships with Tk; TTS works via system voices.

---

## 🚀 Quick Start

### 1) Create and activate a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> If activation is blocked, run PowerShell as Administrator:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Linux extra (if GUI/TTS fails):**
```bash
sudo apt-get update
sudo apt-get install -y python3-tk espeak
```

### 3) Run the GUI (recommended)
```bash
python main.py
```

### 4) Run the CLI (optional)
```bash
python -m url2speech.cli "https://mars.nasa.gov/all-about-mars/facts/" --show=summary
```

---

## 📤 Outputs
For each processed URL, the app creates a timestamped folder in `outputs/`:

- `clean.txt` → cleaned full text  
- `summary.txt` → only if text was long  
- `spoken_text.txt` → the exact text used for speech  
- `audio.wav` → offline TTS output  
- `meta.json` → metadata (mode, lang guess, file paths)  

---

## 🔧 Configuration
Inside `src/url2speech/core.py`:
- `DEFAULT_SHORT_WORDS = 60` → threshold for short vs. long
- `TARGET_SUMMARY_WORDS = 180` → target summary length
- In `synthesize_audio(...)`:
  - `rate=175` → TTS speed
  - `voice_hint=("spanish" if lang=="es" else "english")` → basic language-based voice choice

---

## 🌐 Example URLs
- Short: https://www.example.com/  
- Long (English): https://mars.nasa.gov/all-about-mars/facts/  
- Long (English): https://www.harvard.edu/about/  
- Long (Spanish): https://www.unam.mx/  

---

## 🛠️ Troubleshooting
- **`ModuleNotFoundError: No module named 'url2speech'`**  
  → Run `python main.py`, or set `PYTHONPATH=$PWD/src`.

- **Tkinter window doesn’t open (Linux)**  
  → Install `python3-tk`: `sudo apt-get install python3-tk`.

- **No audio / empty WAV**  
  - Windows: check system voices.  
  - Linux: install `espeak`.  
  - Confirm that `audio.wav` was created in `outputs/...`.  

---

## 📌 Roadmap
- Export to MP3 (`pydub` + `ffmpeg`)  
- Advanced summarizers (TextRank, LexRank)  
- Cross-platform executables (PyInstaller)  
- Web version with backend API  

---

## 📄 License

MIT License

Copyright (c) 2025 Guillermo Guevara

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
