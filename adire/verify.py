import sympy as sp
from sympy import Eq


def verify_solution(obj, task, answer):
    """Check that `answer` really solves `obj`. Returns (ok, reason)."""
    if task == "solve":
        eq = obj if isinstance(obj, Eq) else Eq(obj, 0)
        symbols = list(eq.free_symbols)
        if not symbols:
            return True, "no variable to check"
        x = symbols[0]

        # answer is a string like "[2, 3]" — turn it back into numbers
        roots = sp.sympify(answer)
        if not isinstance(roots, (list, tuple)):
            roots = [roots]

        for r in roots:
            residual = (eq.lhs - eq.rhs).subs(x, r)
            if sp.simplify(residual) != 0:
                return False, f"{x}={r} does not satisfy the equation"
        return True, "all roots check out"

    # For integrate: differentiate the answer, should give back the integrand.
    if task == "integrate":
        integrand = obj.function
        var = obj.limits[0][0]
        answer_expr = sp.sympify(answer)
        if sp.simplify(sp.diff(answer_expr, var) - integrand) == 0:
            return True, "derivative of answer matches integrand"
        return False, "derivative of answer does not match"

    return True, "no check for this task type"