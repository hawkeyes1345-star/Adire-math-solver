import ollama

MODEL = "qwen2.5:7b"


def explain(problem_latex, answer, steps):
    """Ask the local model to write a friendly explanation of the solution.
    The maths is already solved and verified — the model only writes prose."""
    step_lines = "\n".join(f"  {s['title']}: {s['math']}" for s in steps)

    prompt = f"""A student asked to solve this problem: {problem_latex}
The verified answer is: {answer}
The solution steps are:
{step_lines}

Write a short, friendly explanation of how to reach the answer.
Explain the reasoning in plain language a student can follow.
Keep it under 100 words. Do not change the answer."""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]
