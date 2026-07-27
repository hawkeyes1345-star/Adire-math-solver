import os
import re
import ollama

# Model is config-driven, not hardcoded. Override with env var in production.
OCR_MODELS = os.getenv("ADIRE_OCR_MODELS", "minicpm-v,llama3.2-vision").split(",")

PROMPT = """Transcribe the mathematics in this image to a single LaTeX expression.
Output ONLY the LaTeX, nothing else. No dollar signs, no explanation, no markdown.

Be precise about operators:
- A short horizontal line between terms is a MINUS sign (-), not multiplication.
- Only use \\cdot or * if there is a clear dot or times symbol.
- Preserve exponents: a small raised number is a power, e.g. x^{2}.
- Keep the operation: integral \\int, derivative \\frac{d}{dx}, equals =.

If nothing mathematical is legible, output exactly: UNREADABLE"""

def _clean(text):
    """Tidy the raw model output into parseable LaTeX."""
    text = text.strip().strip("$").replace("```latex", "").replace("```", "").strip()
    text = re.sub(r"\s+", " ", text)          # collapse whitespace
    return text


def image_to_latex(image_path):
    """Read an image and return LaTeX. Tries each model in order until one works."""
    last_error = None
    for model in OCR_MODELS:
        model = model.strip()
        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": PROMPT,
                           "images": [image_path]}],
            )
            text = _clean(response["message"]["content"])
            if text and text.upper() != "UNREADABLE":
                return {"latex": text, "model": model, "ok": True}
            last_error = "model returned UNREADABLE"
        except Exception as exc:
            last_error = str(exc)
            continue      # this model failed — try the next one

    return {"latex": None, "model": None, "ok": False, "error": last_error}