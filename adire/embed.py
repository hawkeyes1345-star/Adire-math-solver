import ollama
import numpy as np

EMBED_MODEL = "nomic-embed-text"


def embed(text):
    """Turn text into a vector (list of numbers)."""
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return np.array(response["embedding"])


def similarity(vec1, vec2):
    """How similar are two vectors? 1.0 = identical, 0 = unrelated."""
    dot = np.dot(vec1, vec2)
    norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return float(dot / norm) if norm else 0.0