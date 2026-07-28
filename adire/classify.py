import sympy as sp
from sympy import Eq

# How "hard" each operation is, as a base weight.
TASK_WEIGHT = {
    "simplify": 0.5,
    "solve": 1.0,
    "differentiate": 2.0,
    "integrate": 3.0,
}


def features(obj, task):
    """Read complexity signals off the parsed problem."""
    core = obj.lhs - obj.rhs if isinstance(obj, Eq) else obj

    ops = int(sp.count_ops(core))          # number of operations
    n_symbols = len(core.free_symbols)     # how many variables

    degree = 0                             # highest power
    for s in core.free_symbols:
        try:
            d = sp.degree(sp.expand(core), s)
            if d.is_number:
                degree = max(degree, int(d))
        except Exception:
            pass

    return {
        "task_weight": TASK_WEIGHT.get(task, 1.0),
        "ops": ops,
        "degree": degree,
        "n_symbols": n_symbols,
    }

def score(f):
    """Combine features into one number. Higher = harder."""
    return (
        2.0 * f["task_weight"]
        + 0.25 * f["ops"]
        + 1.5 * max(0, f["degree"] - 1)     # degree 1 is free; 2+ adds up
        + 0.8 * max(0, f["n_symbols"] - 1)  # 1 variable is free; 2+ adds up
    )


def classify(obj, task):
    """Return the difficulty band and the score behind it."""
    f = features(obj, task)
    s = score(f)
    if s < 4.0:
        band = "easy"
    elif s < 7.0:
        band = "medium"
    else:
        band = "hard"
    return {"difficulty": band, "score": round(s, 2)}