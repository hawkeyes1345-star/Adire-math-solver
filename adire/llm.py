import ollama
import sympy as sp
from adire.rag import retrieve

MODEL = "qwen2.5:7b"


def explain(problem_latex, answer, steps, similar=None):
    """Explain the solution, using course notes (RAG) and a similar worked
    example (tier-2) when available. The example guides STYLE, not the answer."""
    step_lines = "\n".join(f"  {s['title']}: {s['math']}" for s in steps)

    # RAG: relevant course notes
    notes = retrieve(problem_latex)
    notes_text = "\n".join(notes) if notes else "No specific course notes available."

    # TIER-2: a similar previously-solved problem, as a worked example
    example_text = ""
    if similar:
        ex_steps = "\n".join(f"  {s['title']}: {s['math']}" for s in similar["steps"])
        example_text = f"""
Here is a SIMILAR problem that was solved before, as a style reference
(do NOT copy its numbers — the current problem is different):
Problem: {similar['latex']}
Steps:
{ex_steps}
"""

    prompt = f"""A student asked to solve this problem: {problem_latex}
The verified answer is: {answer}

Relevant course notes (use this notation and method where possible):
{notes_text}
{example_text}
The solution steps are:
{step_lines}

Write a short, friendly explanation of how to reach the answer.
Follow the method in the course notes, and match the explanation style of the
similar example if one is given. Explain in plain language a student can follow.
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