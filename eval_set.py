# Gold set: (latex, expected_answer, expected_difficulty)
# Answers as SymPy would produce them; difficulty is human-judged.
GOLD = [
    # --- easy: linear equations ---
    ("2x+3=7", "[2]", "easy"),
    ("x+5=12", "[7]", "easy"),
    ("3x=15", "[5]", "easy"),
    ("4x-8=0", "[2]", "easy"),
    ("x-9=1", "[10]", "easy"),
    ("5x+2=17", "[3]", "easy"),
    ("2x-6=4", "[5]", "easy"),
    ("7x=21", "[3]", "easy"),
    ("x+1=1", "[0]", "easy"),
    ("6x-3=9", "[2]", "easy"),
    # --- medium: quadratics & simple calculus ---
    ("x^2-5x+6=0", "[2, 3]", "medium"),
    ("x^2-9=0", "[-3, 3]", "medium"),
    ("x^2-7x+12=0", "[3, 4]", "medium"),
    ("x^2+2x+1=0", "[-1]", "medium"),
    ("x^2-4=0", "[-2, 2]", "medium"),
    ("x^2-8x+15=0", "[3, 5]", "medium"),
    ("x^2-x-6=0", "[-2, 3]", "medium"),
    ("x^2-6x+9=0", "[3]", "medium"),
    ("x^2-1=0", "[-1, 1]", "medium"),
    ("x^2+5x+6=0", "[-3, -2]", "medium"),
    # --- integration / differentiation (medium-hard) ---
    (r"\int x^2 dx", "x**3/3", "medium"),
    (r"\int x^3 dx", "x**4/4", "medium"),
    (r"\int 2x dx", "x**2", "medium"),
    (r"\int x dx", "x**2/2", "medium"),
    (r"\frac{d}{dx} x^2", "2*x", "medium"),
    (r"\frac{d}{dx} x^3", "3*x**2", "medium"),
    (r"\frac{d}{dx} x^4", "4*x**3", "medium"),
    # --- simplification ---
    (r"\frac{x^2-1}{x-1}", "x + 1", "easy"),
    (r"\frac{x^2-4}{x-2}", "x + 2", "easy"),
    ("(x+1)^2", "x**2 + 2*x + 1", "easy"),
]