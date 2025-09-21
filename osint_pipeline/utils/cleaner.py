import re
from langdetect import detect

def clean_text(text):
    text = re.sub(r"http\S+", "", text) # remove URLs
    text = re.sub(r"[^A-Za-z0-9\s]", "", text) # remove symbols
    return text.strip()

def _is_english(text, min_len=3):
    if not text or not text.strip():
        return False
    if len(text.strip()) < min_len:
        return False
    try:
        return detect(text) == "en"
    except Exception:
        return False

def filter_english(records):
    return [r for r in records if _is_english(r.get("text", ""))]