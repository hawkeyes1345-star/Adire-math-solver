from sympy.parsing.latex import parse_latex


def parse(latex: str):
    """Turn a LaTeX string into a SymPy object."""
    cleaned = latex.strip().strip("$").strip()
    try:
        return parse_latex(cleaned)
    except Exception as exc:
        raise ValueError(f"could not parse: {latex!r}") from exc
import sympy as sp
from sympy import Eq, srepr


import sympy as sp
from sympy import Eq, srepr


def canonical(obj) -> str:
    """A fingerprint string that is identical for equivalent problems."""
    if isinstance(obj, Eq):
        diff = sp.expand(obj.lhs - obj.rhs)          # e.g.  2x - 4
        neg = sp.expand(-diff)                        # e.g.  4 - 2x
        a, b = srepr(diff), srepr(neg)
        chosen = a if a <= b else b                   # always pick the same one
        return "EQ0(" + chosen + ")"
    return srepr(sp.expand(obj))

def detect_task(obj) -> str:
    """What is the student asking for?"""
    if isinstance(obj, sp.Integral):
        return "integrate"
    if isinstance(obj, sp.Derivative):
        return "differentiate"
    if isinstance(obj, Eq):
        return "solve"
    return "simplify"
import hashlib


def make_key(latex: str) -> dict:
    """Full pipeline: latex -> parsed -> task + canonical -> hash key."""
    obj = parse(latex)
    task = detect_task(obj)
    canon = canonical(obj)
    key = hashlib.sha256(f"{task}|{canon}".encode()).hexdigest()
    return {"task": task, "canonical": canon, "key": key}