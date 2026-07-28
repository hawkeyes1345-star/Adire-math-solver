from adire.normalize import parse, detect_task, canonical, make_key
from adire.solver import solve
from adire.cache import Cache
from adire.classify import classify
from adire.verify import verify_solution
from adire.steps import build_steps
from adire.llm import explain, check_explanation

_cache = Cache()


def solve_problem(latex):
    """normalize -> tier1 cache -> solve -> verify -> tier2 example -> store."""
    info = make_key(latex)
    key = info["key"]

    # TIER 1: exact match
    hit = _cache.get(key)
    if hit is not None:
        return {"cached": True, "task": hit["task"], "answer": hit["answer"],
                "difficulty": "cached", "score": None, "verified": True,
                "steps": hit["steps"], "explanation": None, "similar_used": None}

    # MISS — solve, verify, build steps
    obj = parse(latex)
    answer = solve(obj, info["task"])
    band = classify(obj, info["task"])
    ok, reason = verify_solution(obj, info["task"], answer)

    steps = build_steps(obj, info["task"], answer) if ok else []

    # TIER 2: find a similar past problem (as an example, not the answer)
    similar = _cache.find_similar(latex, info["task"]) if ok else None

    explanation = None
    if ok:
        try:
            text = explain(latex, answer, steps)
            good, _ = check_explanation(text, answer)
            explanation = text if good else None
        except Exception:
            explanation = None

    if ok:
        _cache.put(key, info["task"], answer, steps=steps, latex=latex)
    else:
        answer = None

    return {"cached": False, "task": info["task"], "answer": answer,
            "difficulty": band["difficulty"], "score": band["score"],
            "verified": ok, "steps": steps, "explanation": explanation,
            "similar_used": similar["latex"] if similar else None}