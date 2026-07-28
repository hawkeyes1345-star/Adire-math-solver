# Adire — Step-by-Step Mathematics Solver

Adire solves mathematics problems step by step. Type or photograph a problem and get a difficulty rating, a **verified** answer, a worked solution, and a plain-language explanation — all rendered in the browser, running entirely on a local machine at zero API cost.

**Core principle — verified generation:** a computer algebra system (SymPy) computes and independently verifies every answer. The language model only writes the explanation around an already-proven result, and its output is itself checked against the verified answer. Nothing unverified is ever stored or shown.

## Features

- **Seven problem types:** linear & quadratic equations, integration, differentiation, simplification, **systems of equations, limits, and matrices** (determinant / inverse / eigenvalues).
- **Verified answers** — SymPy solves and verifies; a wrong explanation is caught and replaced with deterministic steps.
- **Difficulty classification** — easy / medium / hard (90% agreement with human labels).
- **Two-tier cache** — exact-match (served free) and semantic similarity (provides a worked example without reusing the answer).
- **RAG** — explanations grounded in course notes for correct notation.
- **OCR** — photograph a problem; transcription returned for confirmation before solving.
- **Local & free** — SymPy + Ollama (Qwen2.5, minicpm-v, nomic-embed-text). No external API.
  ###Architecture

input (typed or photographed)
-> OCR (image -> LaTeX, user-confirmed)
-> normalise (LaTeX -> canonical form -> cache key)
-> classify difficulty
-> cache tier 1 (exact) -> hit: serve instantly
-> cache tier 2 (semantic) -> similar problem as a worked example
-> SymPy solve (authoritative answer)
-> RAG (retrieve course notes)
-> LLM explain (local model)
-> verify (LLM output checked against SymPy)
-> store (verified only) -> render (KaTeX)


## Tech stack

| Layer | Technology |
|---|---|
| Symbolic solver + verifier | SymPy |
| Difficulty classifier | rule-based feature scoring |
| Explanation LLM | Qwen2.5-7B (Ollama) |
| OCR | minicpm-v (Ollama) |
| Embeddings (RAG + tier-2) | nomic-embed-text (Ollama) |
| Cache / storage | SQLite |
| API | FastAPI |
| Frontend | HTML + MathLive + KaTeX |

## Setup

Requires Python 3.10+ and [Ollama](https://ollama.com) with:

ollama pull qwen2.5:7b
ollama pull minicpm-v
ollama pull nomic-embed-text


Install and run:

pip install -r requirements.txt
uvicorn adire.api:app --reload

Then open `web.html` in a browser.

## Usage examples

| Type | Input |
|---|---|
| Linear | `2x + 3 = 7` |
| Quadratic | `x^2 - 5x + 6 = 0` |
| Integration | `\int x^2 dx` |
| Differentiation | `\frac{d}{dx} x^2` |
| System | `2x+y=5, x-y=1` |
| Limit | `\lim_{x \to 0} \frac{\sin x}{x}` |
| Matrix | `det([[1,2],[3,4]])` |

## Evaluation

python evaluate.py


| Metric | Result |
|---|---|
| Solve accuracy | 30/30 (100%) |
| Difficulty classification | 27/30 (90%) |
| Parse/solve failures | 0/30 |

## Limitations

- OCR is unreliable on handwriting (a known limit of local vision models); treated as assisted input requiring user confirmation.
- The rule-based classifier misses ~10% of borderline cases.
- Scope is standard curriculum problems; competition-style tricks are out of scope.
