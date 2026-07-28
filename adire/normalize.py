import hashlib
import re
import sympy as sp
from sympy import Eq, srepr
from sympy.parsing.latex import parse_latex


def parse(latex: str):
    cleaned = latex.strip().strip("$").strip()
    cleaned = cleaned.replace(r"\displaystyle", "")
    cleaned = cleaned.replace(r"\,", " ").replace(r"\!", "").replace(r"\;", " ").replace(r"\:", " ")
    cleaned = cleaned.replace("d x", "dx")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    try:
        return parse_latex(cleaned)
    except Exception as exc:
        raise ValueError(f"could not parse: {latex!r}") from exc


def canonical(obj):
    if isinstance(obj, Eq):
        diff = sp.expand(obj.lhs - obj.rhs)
        a, b = srepr(diff), srepr(sp.expand(-diff))
        return "EQ0(" + (a if a <= b else b) + ")"
    return srepr(sp.expand(obj))


def detect_task(obj):
    if isinstance(obj, sp.Integral):
        return "integrate"
    if isinstance(obj, sp.Derivative):
        return "differentiate"
    if isinstance(obj, Eq):
        return "solve"
    return "simplify"


def make_key(latex):
    obj = parse(latex)
    task = detect_task(obj)
    canon = canonical(obj)
    key = hashlib.sha256(f"{task}|{canon}".encode()).hexdigest()
    return {"task": task, "canonical": canon, "key": key}