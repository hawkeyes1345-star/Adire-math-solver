import sympy as sp
from sympy import Eq, Matrix


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

    if task == "system":
        # obj is a list of equations
        symbols = sorted(set().union(*[e.free_symbols for e in obj]), key=str)
        sol = sp.solve(obj, symbols, dict=True)
        return str(sol)

    if task == "limit":
        # obj is a Limit object
        return str(obj.doit())

    if task == "matrix":
        # obj is a dict: {"op": ..., "matrix": Matrix}
        M = obj["matrix"]
        op = obj["op"]
        if op == "det":
            return str(M.det())
        if op == "inv":
            return str(M.inv().tolist())
        if op == "eigenvals":
            return str(list(M.eigenvals().keys()))
        return str(M)

    # simplify / fallback
    return str(sp.simplify(obj))