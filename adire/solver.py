import sympy as sp
from sympy import Eq


def solve(obj, task):
    """Given a parsed problem and its task, compute the answer with SymPy."""
    if task == "solve":
        eq = obj if isinstance(obj, Eq) else Eq(obj, 0)
        roots = sp.solve(eq)
        return str(roots)

    if task == "integrate":
        return str(sp.integrate(obj.function, obj.limits[0][0]))

    if task == "differentiate":
        return str(obj.doit())

    # simplify / fallback
    return str(sp.simplify(obj))