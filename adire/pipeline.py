from adire.normalize import parse, detect_task, canonical, make_key
from adire.solver import solve
from adire.cache import Cache
from adire.classify import classify
from adire.verify import verify_solution

_cache = Cache()


def solve_problem(latex):
    """normalize -> check cache -> hit serves free, miss solves then stores."""
    info = make_key(latex)
    key = info["key"]

    hit = _cache.get(key)
    if hit is not None:
        return {"cached": True, "task": hit["task"], "answer": hit["answer"]}

# MISS — solve it, verify it, then store only if it passes
    obj = parse(latex)
    answer = solve(obj, info["task"])
    band = classify(obj, info["task"])

    ok, reason = verify_solution(obj, info["task"], answer)   # NEW
    if ok:
        _cache.put(key, info["task"], answer, steps=[])       # store only if verified
    else:
        answer = None                                          # don't serve unverified

    return {"cached": False, "task": info["task"], "answer": answer,
            "difficulty": band["difficulty"], "score": band["score"],
            "verified": ok, "reason": reason}                 # NEW