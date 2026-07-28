import os
from adire.embed import embed, similarity

CORPUS_DIR = "corpus"


def load_corpus():
    """Read all note files and embed each paragraph."""
    chunks = []
    if not os.path.isdir(CORPUS_DIR):
        return chunks
    for fname in os.listdir(CORPUS_DIR):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(CORPUS_DIR, fname), encoding="utf-8") as f:
            text = f.read()
        # split into paragraphs (blank-line separated)
        for para in text.split("\n\n"):
            para = para.strip()
            if para:
                chunks.append({"text": para, "vec": embed(para)})
    return chunks


# load once at import
_CHUNKS = load_corpus()


def retrieve(query, k=2, threshold=0.5):
    """Find the k most relevant note chunks for a query."""
    if not _CHUNKS:
        return []
    q = embed(query)
    scored = [(similarity(q, c["vec"]), c["text"]) for c in _CHUNKS]
    scored.sort(reverse=True)
    return [text for score, text in scored[:k] if score >= threshold]