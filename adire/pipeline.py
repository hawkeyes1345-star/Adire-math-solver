from adire.normalize import make_key
from adire.cache import Cache

_cache = Cache()


def solve_problem(latex):
    """The pipeline so far: normalize -> check cache -> hit or miss."""
    info = make_key(latex)          # stage 1: key
    key = info["key"]

    hit = _cache.get(key)           # stage 4: cache lookup
    if hit is not None:
        return {"cached": True, "task": hit["task"], "answer": hit["answer"]}

    # MISS — for now we just report it. Stage 3 (SymPy) fills this in next.
    return {"cached": False, "task": info["task"], "answer": None,
            "note": "not solved yet — SymPy comes next"}