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

## Architecture
