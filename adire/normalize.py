import hashlib
import re
import sympy as sp
from sympy import Eq, srepr, Matrix, symbols
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import parse_expr


def _clean(latex):
    cleaned = latex.strip().strip("$").strip()
    cleaned = cleaned.replace(r"\displaystyle", "")
    cleaned = cleaned.replace(r"\,", " ").replace(r"\!", "").replace(r"\;", " ").replace(r"\:", " ")
    cleaned = cleaned.replace("d x", "dx")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def parse(latex: str):
    """Parse LaTeX into a SymPy object. Handles systems, limits, matrices, and
    ordinary expressions/equations."""
    raw = latex.strip().strip("$").strip()

    # --- MATRIX: det([[1,2],[3,4]]) / inv(...) / eigen(...) ---
    m = re.match(r"\s*(det|inv|eigen|eigenvals)\s*\(\s*(\[\[.*\]\])\s*\)\s*$", raw)
    if m:
        op = {"det": "det", "inv": "inv", "eigen": "eigenvals", "eigenvals": "eigenvals"}[m.group(1)]
        rows = eval(m.group(2), {"__builtins__": {}})   # safe: only [[...]] shape
        return {"op": op, "matrix": Matrix(rows)}

    # --- SYSTEM: multiple equations separated by commas ---
    # e.g. "2x+y=5, x-y=1"
    if "," in raw and raw.count("=") >= 2:
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        eqs = []
        for p in parts:
            eqs.append(_parse_single(p))
        return eqs

    # --- LIMIT: \lim_{x \to a} expr ---
    if "\\lim" in raw:
        return _parse_limit(raw)

    # --- ordinary expression / equation ---
    return _parse_single(raw)


def _parse_single(latex):
    cleaned = _clean(latex)
    try:
        return parse_latex(cleaned)
    except Exception as exc:
        raise ValueError(f"could not parse: {latex!r}") from exc


def _parse_limit(latex):
    """Parse \\lim_{x \\to a} expr into a SymPy Limit."""
    cleaned = _clean(latex)
    # extract variable and point: \lim_{x \to 0}
    m = re.search(r"\\lim_\{?\s*([a-zA-Z])\s*\\to\s*([^}]+?)\s*\}?", cleaned)
    if not m:
        raise ValueError(f"could not parse limit: {latex!r}")
    var = sp.Symbol(m.group(1))
    point_str = m.group(2).replace("\\infty", "oo").strip()
    point = sp.sympify(point_str)
    # the expression is whatever comes after the lim clause
    expr_part = cleaned[m.end():].strip()
    expr = parse_latex(expr_part)
    return sp.Limit(expr, var, point)


def canonical(obj):
    if isinstance(obj, dict):  # matrix
        return "MATRIX(" + obj["op"] + "," + srepr(obj["matrix"]) + ")"
    if isinstance(obj, list):  # system
        return "SYSTEM(" + ",".join(sorted(canonical(e) for e in obj)) + ")"
    if isinstance(obj, sp.Limit):
        return "LIMIT(" + srepr(obj) + ")"
    if isinstance(obj, Eq):
        diff = sp.expand(obj.lhs - obj.rhs)
        a, b = srepr(diff), srepr(sp.expand(-diff))
        return "EQ0(" + (a if a <= b else b) + ")"
    return srepr(sp.expand(obj))


def detect_task(obj):
    if isinstance(obj, dict):
        return "matrix"
    if isinstance(obj, list):
        return "system"
    if isinstance(obj, sp.Limit):
        return "limit"
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