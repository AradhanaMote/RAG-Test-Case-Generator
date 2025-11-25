import json
from pathlib import Path
import fitz  # pymupdf
from bs4 import BeautifulSoup

def parse_file_to_text(path: str) -> str:
    p = Path(path)
    suf = p.suffix.lower()
    if suf in ['.md', '.txt']:
        return p.read_text(encoding='utf-8')
    if suf in ['.json']:
        return json.dumps(json.load(open(p, 'r', encoding='utf-8')), indent=2)
    if suf in ['.pdf']:
        return parse_pdf(path)
    if suf in ['.html', '.htm']:
        return parse_html(path)
    # fallback
    return p.read_text(encoding='utf-8', errors='ignore')

def parse_pdf(path: str) -> str:
    doc = fitz.open(path)
    txt = []
    for page in doc:
        txt.append(page.get_text())
    return '\n'.join(txt)

def parse_html(path: str) -> str:
    html = Path(path).read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    # remove script/style
    for s in soup(['script', 'style']):
        s.decompose()
    return soup.get_text(separator=' ', strip=True)
