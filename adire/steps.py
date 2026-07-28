import sympy as sp
from sympy import Eq, Matrix


def build_steps(obj, task, answer):
    """Produce a list of step dicts: {title, math}. Correct by construction."""
    if task == "solve":
        return _solve_steps(obj)
    if task == "integrate":
        return _integrate_steps(obj)
    if task == "differentiate":
        return _differentiate_steps(obj)
    if task == "system":
        return _system_steps(obj)
    if task == "limit":
        return _limit_steps(obj)
    if task == "matrix":
        return _matrix_steps(obj)
    return [{"title": "Simplify", "math": sp.latex(sp.simplify(obj))}]


def _solve_steps(obj):
    eq = obj if isinstance(obj, Eq) else Eq(obj, 0)
    steps = [{"title": "Given equation", "math": sp.latex(eq)}]
    moved = sp.expand(eq.lhs - eq.rhs)
    steps.append({"title": "Move everything to one side",
                  "math": sp.latex(Eq(moved, 0))})
    factored = sp.factor(moved)
    if factored != moved:
        steps.append({"title": "Factor", "math": sp.latex(Eq(factored, 0))})
    roots = sp.solve(eq)
    x = list(eq.free_symbols)[0]
    root_str = ",\\; ".join(sp.latex(Eq(x, r)) for r in roots)
    steps.append({"title": "Solutions", "math": root_str})
    return steps


def _integrate_steps(obj):
    var = obj.limits[0][0]
    result = sp.integrate(obj.function, var)
    return [
        {"title": "Integrand", "math": sp.latex(obj.function)},
        {"title": "Integrate", "math": sp.latex(result) + " + C"},
    ]


def _differentiate_steps(obj):
    result = obj.doit()
    return [
        {"title": "Function", "math": sp.latex(obj.expr)},
        {"title": "Differentiate", "math": sp.latex(result)},
    ]


def _system_steps(obj):
    """obj is a list of equations."""
    steps = [{"title": "Given system",
              "math": r"\\ ".join(sp.latex(e) for e in obj)}]
    syms = sorted(set().union(*[e.free_symbols for e in obj]), key=str)
    sol = sp.solve(obj, syms, dict=True)
    if sol:
        parts = []
        for var, val in sorted(sol[0].items(), key=lambda kv: str(kv[0])):
            parts.append(sp.latex(Eq(var, val)))
        steps.append({"title": "Solution", "math": ",\\; ".join(parts)})
    return steps


def _limit_steps(obj):
    """obj is a Limit."""
    result = obj.doit()
    return [
        {"title": "Given limit", "math": sp.latex(obj)},
        {"title": "Evaluate", "math": sp.latex(result)},
    ]


def _matrix_steps(obj):
    """obj is {"op": ..., "matrix": Matrix}."""
    M = obj["matrix"]
    op = obj["op"]
    steps = [{"title": "Given matrix", "math": sp.latex(M)}]
    if op == "det":
        steps.append({"title": "Determinant", "math": sp.latex(M.det())})
    elif op == "inv":
        steps.append({"title": "Inverse", "math": sp.latex(M.inv())})
    elif op == "eigenvals":
        vals = list(M.eigenvals().keys())
        steps.append({"title": "Eigenvalues",
                      "math": ",\\; ".join(sp.latex(v) for v in vals)})
    return steps