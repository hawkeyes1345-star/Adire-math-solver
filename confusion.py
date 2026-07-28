from adire.normalize import parse, make_key
from adire.classify import classify
from eval_set import GOLD

print(f"{'problem':30} {'human':8} {'system':8} {'match'}")
print("-" * 55)
for latex, ans, human_diff in GOLD:
    info = make_key(latex)
    obj = parse(latex)
    sys_diff = classify(obj, info["task"])["difficulty"]
    mark = "OK" if sys_diff == human_diff else "MISS"
    print(f"{latex:30} {human_diff:8} {sys_diff:8} {mark}")