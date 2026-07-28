import ollama
import sympy as sp
from adire.rag import retrieve

MODEL = "qwen2.5:7b"


def explain(problem_latex, answer, steps):
    """Ask the local model to explain the solution, using retrieved course notes."""
    step_lines = "\n".join(f"  {s['title']}: {s['math']}" for s in steps)

    # RAG: pull relevant course notes for this problem
    notes = retrieve(problem_latex)
    notes_text = "\n".join(notes) if notes else "No specific course notes available."

    prompt = f"""A student asked to solve this problem: {problem_latex}
The verified answer is: {answer}

Relevant course notes (use this notation and method where possible):
{notes_text}

The solution steps are:
{step_lines}

Write a short, friendly explanation of how to reach the answer.
Follow the method shown in the course notes above.
Explain the reasoning in plain language a student can follow.
Keep it under 100 words. Do not change the answer."""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def check_explanation(explanation, answer):
    """Guard: the prose must not contradict the verified answer."""
    roots = sp.sympify(answer)
    if not isinstance(roots, (list, tuple)):
        roots = [roots]

    missing = [str(r) for r in roots if str(r) not in explanation]
    if missing:
        return False, f"explanation is missing the root(s): {missing}"
    return True, "explanation mentions all verified roots"