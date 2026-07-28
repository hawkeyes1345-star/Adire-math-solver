import sympy as sp
from adire.normalize import parse, make_key
from adire.solver import solve
from adire.classify import classify
from eval_set import GOLD


def answers_match(got, expected):
    """Compare answers symbolically (handles ordering, form differences)."""
    try:
        g = sp.sympify(got)
        e = sp.sympify(expected)
        if isinstance(g, (list, tuple)) or isinstance(e, (list, tuple)):
            gs = set(sp.sympify(x) for x in (g if isinstance(g, (list, tuple)) else [g]))
            es = set(sp.sympify(x) for x in (e if isinstance(e, (list, tuple)) else [e]))
            return gs == es
        return sp.simplify(g - e) == 0
    except Exception:
        return str(got).strip() == str(expected).strip()


def run():
    total = len(GOLD)
    solve_correct = 0
    difficulty_correct = 0
    parse_fail = 0
    results = []

    for latex, exp_answer, exp_diff in GOLD:
        try:
            info = make_key(latex)
            obj = parse(latex)
            got = solve(obj, info["task"])
            cls = classify(obj, info["task"])
            got_diff = cls["difficulty"]

            ans_ok = answers_match(got, exp_answer)
            diff_ok = (got_diff == exp_diff)
            solve_correct += ans_ok
            difficulty_correct += diff_ok
            results.append((latex, ans_ok, diff_ok, got, got_diff))
        except Exception as exc:
            parse_fail += 1
            results.append((latex, False, False, f"ERROR: {exc}", "?"))

    print("=" * 60)
    print("ADIRE EVALUATION RESULTS")
    print("=" * 60)
    print(f"Total problems:        {total}")
    print(f"Solved correctly:      {solve_correct}/{total}  ({100*solve_correct//total}%)")
    print(f"Difficulty correct:    {difficulty_correct}/{total}  ({100*difficulty_correct//total}%)")
    print(f"Parse/solve failures:  {parse_fail}/{total}")
    print("=" * 60)
    print("\nFailures (if any):")
    for latex, ans_ok, diff_ok, got, got_diff in results:
        if not ans_ok:
            print(f"  {latex:30} got={got}")

    return results


if __name__ == "__main__":
    run()