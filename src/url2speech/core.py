
import os, re, string, urllib.parse
from datetime import datetime
import requests, trafilatura, pyttsx3
from bs4 import BeautifulSoup

DEFAULT_SHORT_WORDS = 60
TARGET_SUMMARY_WORDS = 180
OUTPUT_ROOT = os.path.join(os.getcwd(), "outputs")

STOPWORDS_ES = set("a al algo algunas algunos ante antes como con contra cual cuando de del desde donde dos el ella ellas ellos en entre era eran es esa esas ese eso esos esta estaba estaban estar este estos fue fueron ha han haber había habían hasta hay la las le les lo los mas más me mi mis muy nada ni no nos o otra otros para pero poco por porque que quien quien(es) se sin sobre su sus te tiene tienen tuvo un una unas uno unos y ya yo tú usted ustedes él ésta éste esos esas esas estas estos este esta esto eso esa aquel aquella aquello aquellos aquellas serán será serán ser soy estás está estamos están estás estaban estaban estaré estarás estará estaremos estarán seremos serán sería serían sería serían será serán fui fuiste fue fuimos fueron".split())
STOPWORDS_EN = set("a an and are as at be by for from has have he her hers him his i if in into is it its itself me more most my myself no nor not of on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why with you your yours yourself yourselves".split())

def ensure_dir(path): os.makedirs(path, exist_ok=True); return path
def slugify(text, maxlen=64):
    text = re.sub(r"https?://","",text,flags=re.I).lower()
    text = re.sub(r"[^a-z0-9._-]+","-",text); text = re.sub(r"-+","-",text).strip("-"); 
    return text[:maxlen] if len(text)>maxlen else text

def cleanup_text(text):
    lines=[ln.strip() for ln in text.splitlines() if ln.strip()]
    if sum(len(ln.split()) for ln in lines)>80: lines=[ln for ln in lines if len(ln.split())>=3]
    return re.sub(r"\n{3,}","\n\n","\n".join(lines)).strip()

def extract_text(url, timeout=20):
    try:
        dl = trafilatura.fetch_url(url, no_ssl=True)
        if dl:
            txt = trafilatura.extract(dl, include_comments=False, include_tables=False, with_metadata=False, favor_recall=True)
            if txt and txt.strip(): return txt.strip()
    except Exception: pass
    r = requests.get(url, timeout=timeout, headers={"User-Agent":"Mozilla/5.0"}); r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    for bad in soup(["script","style","noscript"]): bad.extract()
    return cleanup_text(soup.get_text(separator="\n"))

def detect_language_simple(text):
    words=[w.lower().strip(string.punctuation) for w in text.split()]
    return "es" if sum(1 for w in words if w in STOPWORDS_ES) >= sum(1 for w in words if w in STOPWORDS_EN) else "en"

def clip_words(text, n): return " ".join(text.split()[:n])

def summarize_frequency(text, target_words=TARGET_SUMMARY_WORDS, lang="es"):
    import re
    sents=re.split(r"(?<=[.!?])\s+", text.strip()); stop=STOPWORDS_ES if lang=="es" else STOPWORDS_EN
    freqs={}; total=0
    for s in sents:
        for w in re.findall(r"\b\w+\b", s.lower()):
            if w in stop or w.isdigit(): continue
            freqs[w]=freqs.get(w,0)+1; total+=1
    if not total: return clip_words(text, target_words)
    for k in list(freqs.keys()): freqs[k]/=total
    scored=[]
    for i,s in enumerate(sents):
        sc=sum(freqs.get(w,0) for w in re.findall(r"\b\w+\b", s.lower()))
        if s.strip(): scored.append((i,s.strip(),sc))
    scored.sort(key=lambda x:x[2], reverse=True)
    chosen=[]; wc=0
    for i,s,sc in scored:
        w=len(s.split())
        if wc+w<=target_words or not chosen: chosen.append((i,s)); wc+=w
        if wc>=target_words: break
    chosen.sort(key=lambda x:x[0])
    res=" ".join(s for _,s in chosen).strip()
    return res if len(res.split())>=min(60,target_words//2) else clip_words(text,target_words)

def decide_short_or_long(text, short_words=DEFAULT_SHORT_WORDS): return "short" if len(text.split())<=short_words else "long"

def synthesize_audio(text, wav_path, voice_hint=None, rate=None):
    eng=pyttsx3.init()
    if rate: eng.setProperty("rate", rate)
    if voice_hint:
        for v in eng.getProperty("voices"):
            name=(v.name or "").lower(); lang=(getattr(v,"languages",[""])[0] or "").lower()
            if voice_hint in name or voice_hint in lang: eng.setProperty("voice", v.id); break
    eng.save_to_file(text, wav_path); eng.runAndWait()

def process_url(url):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    parsed = urllib.parse.urlparse(url); base = parsed.netloc + parsed.path
    out_dir = ensure_dir(os.path.join(OUTPUT_ROOT, f"{slugify(base)}__{stamp}"))
    raw = extract_text(url); cleaned = cleanup_text(raw)
    mode = decide_short_or_long(cleaned); lang = detect_language_simple(cleaned)
    if mode=="short": summary=None; spoken=cleaned.strip()
    else: summary=summarize_frequency(cleaned, TARGET_SUMMARY_WORDS, lang=lang); spoken=summary
    def write(p,t): open(p,"w",encoding="utf-8").write(t)
    write(os.path.join(out_dir,"clean.txt"), cleaned)
    if mode=="long": write(os.path.join(out_dir,"summary.txt"), summary)
    write(os.path.join(out_dir,"spoken_text.txt"), spoken)
    wav=os.path.join(out_dir,"audio.wav"); synthesize_audio(spoken, wav, voice_hint=("spanish" if lang=="es" else "english"), rate=175)
    import json
    meta={"url":url,"timestamp":stamp,"mode":mode,"lang":lang,"files":{"clean":os.path.abspath(os.path.join(out_dir,"clean.txt")),"spoken_text":os.path.abspath(os.path.join(out_dir,"spoken_text.txt")),"audio_wav":os.path.abspath(wav)}}
    if mode=="long": meta["files"]["summary"]=os.path.abspath(os.path.join(out_dir,"summary.txt"))
    open(os.path.join(out_dir,"meta.json"),"w",encoding="utf-8").write(json.dumps(meta,ensure_ascii=False,indent=2))
    return out_dir, meta
