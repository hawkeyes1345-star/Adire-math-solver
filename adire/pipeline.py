from adire.normalize import parse, detect_task, canonical, make_key
from adire.solver import solve
from adire.cache import Cache
from adire.classify import classify
from adire.verify import verify_solution
from adire.steps import build_steps

_cache = Cache()


def solve_problem(latex):
    """normalize -> check cache -> hit serves free, miss solves then stores."""
    info = make_key(latex)
    key = info["key"]

    hit = _cache.get(key)
    if hit is not None:
        return {"cached": True, "task": hit["task"], "answer": hit["answer"]}

# MISS — solve, verify, build steps, then store only if verified
    obj = parse(latex)
    answer = solve(obj, info["task"])
    band = classify(obj, info["task"])
    ok, reason = verify_solution(obj, info["task"], answer)

    steps = build_steps(obj, info["task"], answer) if ok else []   # NEW

    if ok:
        _cache.put(key, info["task"], answer, steps=steps)          # store steps too
    else:
        answer = None

    return {"cached": False, "task": info["task"], "answer": answer,
            "difficulty": band["difficulty"], "score": band["score"],
            "verified": ok, "steps": steps}                          # NEW