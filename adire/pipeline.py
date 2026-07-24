from adire.normalize import parse, detect_task, canonical, make_key
from adire.solver import solve
from adire.cache import Cache
from adire.classify import classify

_cache = Cache()


def solve_problem(latex):
    """normalize -> check cache -> hit serves free, miss solves then stores."""
    info = make_key(latex)
    key = info["key"]

    hit = _cache.get(key)
    if hit is not None:
        return {"cached": True, "task": hit["task"], "answer": hit["answer"]}

# MISS — solve it, then store it
    obj = parse(latex)
    answer = solve(obj, info["task"])
    band = classify(obj, info["task"])          # NEW
    _cache.put(key, info["task"], answer, steps=[])

    return {"cached": False, "task": info["task"], "answer": answer,
            "difficulty": band["difficulty"], "score": band["score"]}   # NEW