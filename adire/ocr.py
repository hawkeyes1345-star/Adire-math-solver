import ollama

VISION_MODEL = "minicpm-v"

PROMPT = """Transcribe the mathematics in this image to a single LaTeX expression.
Output ONLY the LaTeX, nothing else. No dollar signs, no explanation, no markdown.
Keep the operation: if it shows an integral, use \\int; a derivative, use \\frac{d}{dx}.
If nothing mathematical is legible, output exactly: UNREADABLE"""


def image_to_latex(image_path):
    """Read an image file and return the LaTeX it contains."""
    response = ollama.chat(
        model=VISION_MODEL,
        messages=[{
            "role": "user",
            "content": PROMPT,
            "images": [image_path],
        }],
    )
    text = response["message"]["content"].strip()
    text = text.strip("$").replace("```latex", "").replace("```", "").strip()
    return text