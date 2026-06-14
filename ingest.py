"""
ingest.py — Milestone 3: Document Ingestion and Chunking
NYU Campus Dining Unofficial Guide RAG Pipeline

Sources handled:
  - Scrapable URLs: fetched with BeautifulSoup + requests
  - Manually saved sources (Reddit, Yelp, blocked NYU pages): loaded from data/ as .txt files
  - Allergen PDF: extracted with pdfplumber

Output: chunks.json — list of chunk dicts with keys: text, source
"""

import os
import json
import re
import requests
import pdfplumber
from bs4 import BeautifulSoup

# ── Config ────────────────────────────────────────────────────────────────────

SCRAPABLE_URLS = [
    "https://www.hercampus.com/school/nyu/definitive-ranking-nyu-s-dining-halls/",
    "https://www.ratemydorm.com/blog/student-guide-to-nyu-dining",
    "https://www.uswib.com/lifestyle/dining-hall-superlatives",
]

ALLERGEN_PDF_PATH = "data/allergen_guide.pdf"

DATA_DIR = "data/"  # manually saved .txt files go here

CHUNK_SIZE = 300    # tokens (approximated as words)
OVERLAP = 75        # tokens overlap between chunks

OUTPUT_PATH = "chunks.json"


# ── Cleaning ──────────────────────────────────────────────────────────────────

def clean_document(text: str, source: str = "") -> str:
    """
    Remove noise from raw document text.
    - Strips extra whitespace and blank lines
    - Removes short lines likely to be nav/button/ad text (under 4 words)
    - Removes common Reddit artifacts (upvote counts, timestamps, usernames)
    - Removes common Yelp artifacts (star ratings boilerplate, "Useful/Funny/Cool")
    """
    # Normalize whitespace
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    # Strip author bio blocks (common in Her Campus, WSN articles)
    text = re.sub(
        r'(is a (freshman|sophomore|junior|senior).{0,300}(university|college|campus))',
        '',
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Skip very short lines (nav items, buttons, labels)
        if len(line.split()) < 4:
            continue

        # Skip Reddit-specific noise
        if re.match(r'^\d+\s*(points?|comments?|Posted by|u/|•)', line, re.IGNORECASE):
            continue
        if re.match(r'^(share|save|hide|report|reply|give award|crosspost)', line, re.IGNORECASE):
            continue

        # Skip Yelp-specific noise
        if re.match(r'^(Useful|Funny|Cool|Elite|Check-in|Photo)', line, re.IGNORECASE):
            continue
        if re.match(r'^\d+\s*star', line, re.IGNORECASE):
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


# ── Loading ───────────────────────────────────────────────────────────────────

def scrape_url(url: str) -> str:
    """Fetch a URL and extract visible text using BeautifulSoup."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script, style, nav, footer tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator='\n')
        return clean_document(text, source=url)
    except Exception as e:
        print(f"  ⚠️  Failed to scrape {url}: {e}")
        return ""


def load_pdf(path: str) -> str:
    """Extract text from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(path) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        text = '\n'.join(pages)
        return clean_document(text, source=path)
    except Exception as e:
        print(f"  ⚠️  Failed to load PDF {path}: {e}")
        return ""


def load_txt_files(data_dir: str) -> list[dict]:
    """Load all .txt files from data_dir (manually saved sources)."""
    docs = []
    if not os.path.exists(data_dir):
        print(f"  ⚠️  data/ folder not found — skipping manual sources")
        return docs
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw = f.read()
            cleaned = clean_document(raw, source=filename)
            docs.append({"text": cleaned, "source": filename})
            print(f"  ✅ Loaded {filename} ({len(cleaned.split())} words)")
    return docs


def load_documents(urls: list[str], data_dir: str = "data/") -> list[dict]:
    """
    Load all documents from three source types:
      1. Scrapable URLs (BeautifulSoup)
      2. Manually saved .txt files in data_dir
      3. Allergen PDF (pdfplumber)
    Returns a list of dicts: [{text, source}, ...]
    """
    docs = []

    # 1. Scrape URLs
    print("\n📥 Scraping URLs...")
    for url in urls:
        print(f"  Fetching: {url}")
        text = scrape_url(url)
        if text:
            docs.append({"text": text, "source": url})
            # Spot-check: print first 200 characters
            print(f"  ✅ Success — preview: {text[:200]!r}\n")
        else:
            print(f"  ❌ No content retrieved\n")

    # 2. Load manually saved .txt files
    print("\n📂 Loading manual .txt files from data/...")
    txt_docs = load_txt_files(data_dir)
    docs.extend(txt_docs)

    # 3. Load allergen PDF
    print(f"\n📄 Loading allergen PDF from {ALLERGEN_PDF_PATH}...")
    if os.path.exists(ALLERGEN_PDF_PATH):
        pdf_text = load_pdf(ALLERGEN_PDF_PATH)
        if pdf_text:
            docs.append({"text": pdf_text, "source": ALLERGEN_PDF_PATH})
            print(f"  ✅ PDF loaded — preview: {pdf_text[:200]!r}\n")
    else:
        print(f"  ⚠️  PDF not found at {ALLERGEN_PDF_PATH} — skipping\n")

    print(f"\n📊 Total documents loaded: {len(docs)}")
    return docs


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_documents(
    docs: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP
) -> list[dict]:
    """
    Split each document into chunks of approximately chunk_size words,
    with overlap words carried over between consecutive chunks.
    Returns a list of chunk dicts: [{text, source, chunk_index}, ...]
    Saves output to chunks.json.
    """
    all_chunks = []

    for doc in docs:
        words = doc["text"].split()
        source = doc["source"]
        chunk_index = 0
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)

            all_chunks.append({
                "text": chunk_text,
                "source": source,
                "chunk_index": chunk_index,
                "token_count": len(chunk_words)
            })

            chunk_index += 1
            start += chunk_size - overlap  # slide forward with overlap

    # Save to chunks.json
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Chunking complete — {len(all_chunks)} chunks saved to {OUTPUT_PATH}")
    return all_chunks


# ── Verification ──────────────────────────────────────────────────────────────

def verify_chunks(chunks: list[dict], sample_size: int = 5) -> None:
    """Print chunk stats and randomly sample chunks for manual inspection."""
    import random

    token_counts = [c["token_count"] for c in chunks]
    print(f"\n📊 Chunk stats:")
    print(f"  Total chunks:      {len(chunks)}")
    print(f"  Min token count:   {min(token_counts)}")
    print(f"  Max token count:   {max(token_counts)}")
    print(f"  Avg token count:   {sum(token_counts) / len(token_counts):.1f}")

    print(f"\n🔍 Random sample of {sample_size} chunks:")
    for chunk in random.sample(chunks, min(sample_size, len(chunks))):
        print(f"\n  Source: {chunk['source']} | Chunk #{chunk['chunk_index']} | Tokens: {chunk['token_count']}")
        print(f"  Text:   {chunk['text'][:300]!r}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    docs = load_documents(urls=SCRAPABLE_URLS, data_dir=DATA_DIR)
    chunks = chunk_documents(docs, chunk_size=CHUNK_SIZE, overlap=OVERLAP)
    verify_chunks(chunks)