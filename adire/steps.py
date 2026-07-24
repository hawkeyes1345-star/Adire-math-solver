import sympy as sp
from sympy import Eq


def build_steps(obj, task, answer):
    """Produce a list of step dicts: {title, math}. Correct by construction."""
    if task == "solve":
        return _solve_steps(obj)
    if task == "integrate":
        return _integrate_steps(obj)
    if task == "differentiate":
        return _differentiate_steps(obj)
    return [{"title": "Simplify", "math": sp.latex(sp.simplify(obj))}]


def _solve_steps(obj):
    eq = obj if isinstance(obj, Eq) else Eq(obj, 0)
    steps = [{"title": "Given equation", "math": sp.latex(eq)}]

    moved = sp.expand(eq.lhs - eq.rhs)
    steps.append({"title": "Move everything to one side",
                  "math": sp.latex(Eq(moved, 0))})

    factored = sp.factor(moved)
    if factored != moved:
        steps.append({"title": "Factor",
                      "math": sp.latex(Eq(factored, 0))})

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