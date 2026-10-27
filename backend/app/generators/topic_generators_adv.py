from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any, Dict, Optional

from backend.app.core.base import ProblemDifficulty
from backend.app.core.svg_utils import (
    svg_coordinate_plane,
    svg_data_table,
    svg_number_line,
    svg_polar_grid,
    svg_venn_diagram,
)


def gen_adv_problem(
    topic_id: str,
    topic_name: str,
    category_name: str,
    course_key: str,
    difficulty: ProblemDifficulty,
    rng: random.Random,
) -> Optional[Dict[str, Any]]:
    """Generate a topic-specific problem for Algebra 2, Precalculus, or Calculus subtopics."""
    t_low = topic_name.lower()
    c_low = category_name.lower()
    scale = 1 if difficulty == ProblemDifficulty.MILD else (2 if difficulty == ProblemDifficulty.MEDIUM else 3)
    a: Any
    b: Any
    c: Any
    d: Any
    h: Any
    k: Any
    n: Any
    p: Any
    r: Any
    ans: Any
    ans_v: Any
    val: Any
    vol: Any

    # ------------------------------------------------------------------
    # 1. 3D POINTS, PLANES, 3-VARIABLE SYSTEMS, MATRICES & PARTIAL FRACTIONS
    # ------------------------------------------------------------------
    if "points in three dimensions" in t_low:
        x1, y1, z1 = rng.randint(-4, 4), rng.randint(-4, 4), rng.randint(-4, 4)
        dx, dy, dz = rng.choice([(2, 3, 6), (1, 4, 8), (3, 4, 12), (2, 6, 9)])
        d = int(math.isqrt(dx * dx + dy * dy + dz * dz))
        x2, y2, z2 = x1 + dx, y1 + dy, z1 + dz
        return {
            "prompt_text": "Find the distance and midpoint between the two points in three-dimensional space.",
            "equation_typst": f"$ A({x1}, {y1}, {z1}) \" and \" B({x2}, {y2}, {z2}) $",
            "answer_typst": f"$ d = {d}, quad M({(x1+x2)/2:g}, {(y1+y2)/2:g}, {(z1+z2)/2:g}) $",
            "steps_typst": [
                f"Apply the 3D Distance Formula: $d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2) = sqrt({dx}^2 + {dy}^2 + {dz}^2) = {d}$.",
                f"Apply the 3D Midpoint Formula: $M = (({x1}+{x2})/2, ({y1}+{y2})/2, ({z1}+{z2})/2)$.",
                f"Result: $d = {d}, M({(x1+x2)/2:g}, {(y1+y2)/2:g}, {(z1+z2)/2:g})$.",
            ],
            "distractors": [
                f"$ d = {dx + dy + dz}, quad M({x2 - x1}, {y2 - y1}, {z2 - z1}) $",
                f"$ d = {d + 2}, quad M({(x1+x2)/2:g}, {(y1+y2)/2:g}, {(z1+z2)/2:g}) $",
                f"$ d = {d}, quad M({x1 + dx}, {y1 + dy}, {z1 + dz}) $",
            ],
        }

    if t_low == "planes":
        pool = [-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]
        ix = rng.choice(pool)
        iy = rng.choice([x for x in pool if x != ix])
        iz = rng.choice([x for x in pool if x not in (ix, iy)])
        d_val = abs(math.lcm(ix, iy, iz))
        a, b, c = d_val // ix, d_val // iy, d_val // iz
        if a < 0:
            a, b, c, d_val = -a, -b, -c, -d_val
        return {
            "prompt_text": "Find the x-, y-, and z-intercepts of the given plane in three dimensions.",
            "equation_typst": f"$ {a}x + {b}y + {c}z = {d_val} $",
            "answer_typst": f"$ ({ix}, 0, 0), quad (0, {iy}, 0), quad (0, 0, {iz}) $",
            "steps_typst": [
                f"Set $y = 0, z = 0$ to find the $x$-intercept: ${a}x = {d_val} arrow.r.double ({ix}, 0, 0)$.",
                f"Set $x = 0, z = 0$ to find the $y$-intercept: ${b}y = {d_val} arrow.r.double (0, {iy}, 0)$.",
                f"Set $x = 0, y = 0$ to find the $z$-intercept: ${c}z = {d_val} arrow.r.double (0, 0, {iz})$.",
            ],
            "distractors": [
                f"$ ({a}, 0, 0), quad (0, {b}, 0), quad (0, 0, {c}) $",
                f"$ ({-ix}, 0, 0), quad (0, {-iy}, 0), quad (0, 0, {-iz}) $",
                f"$ ({d_val}, 0, 0), quad (0, {d_val}, 0), quad (0, 0, {d_val}) $",
            ],
        }

    if "three variables" in t_low or "multivariable linear systems" in t_low:
        xv = rng.randint(-3, 4)
        yv = rng.randint(-3, 4)
        zv = rng.randint(1, 5)
        r1 = xv + yv + zv
        r2 = 2 * xv - yv + zv
        r3 = xv + 2 * yv - zv
        return {
            "prompt_text": "Solve the system of three linear equations in three variables (x, y, z).",
            "equation_typst": f"$ cases(x + y + z = {r1}, 2x - y + z = {r2}, x + 2y - z = {r3}) $",
            "answer_typst": f"$ ({xv}, {yv}, {zv}) $",
            "steps_typst": [
                f"Add the first and second equations to eliminate $y$: $3x + 2z = {r1 + r2}$.",
                f"Add the first and third equations to eliminate $z$: $2x + 3y = {r1 + r3}$.",
                f"Back-substitute to find the ordered triple: $(x, y, z) = ({xv}, {yv}, {zv})$.",
            ],
            "distractors": [
                f"$ ({yv}, {xv}, {zv}) $",
                f"$ ({xv + 1}, {yv - 1}, {zv}) $",
                f"$ ({-xv}, {-yv}, {zv}) $",
            ],
        }

    if "cramer's rule" in t_low:
        xv, yv = rng.randint(1, 5), rng.randint(1, 5)
        a, b, c, d = 2, 1, 1, 3
        e = a * xv + b * yv
        f_v = c * xv + d * yv
        det_D = a * d - b * c
        det_Dx = e * d - b * f_v
        det_Dy = a * f_v - e * c
        return {
            "prompt_text": "Use Cramer's Rule and coefficient matrix determinants to solve the linear system.",
            "equation_typst": f"$ cases({a}x + y = {e}, x + {d}y = {f_v}) $",
            "answer_typst": f"$ D = {det_D}, quad x = {xv}, quad y = {yv} $",
            "steps_typst": [
                f"Compute the coefficient determinant: $D = ({a})({d}) - ({b})({c}) = {det_D}$.",
                f"Compute $D_x = ({e})({d}) - ({b})({f_v}) = {det_Dx}$ and $D_y = ({a})({f_v}) - ({e})({c}) = {det_Dy}$.",
                f"Divide by $D$: $x = D_x / D = {xv}$ and $y = D_y / D = {yv}$.",
            ],
            "distractors": [
                f"$ D = {det_D}, quad x = {yv}, quad y = {xv} $",
                f"$ D = {a * d + b * c}, quad x = {xv + 1}, quad y = {yv} $",
                f"$ D = {det_D}, quad x = {det_Dx}, quad y = {det_Dy} $",
            ],
        }

    if "partial fraction" in t_low:
        r1 = rng.randint(1, 4)
        r2 = rng.randint(r1 + 1, 6)
        A = rng.randint(1, 5)
        B = rng.randint(1, 5)
        # A/(x - r1) + B/(x + r2) = ((A+B)x + (A*r2 - B*r1)) / ((x - r1)(x + r2))
        num_x = A + B
        num_c = A * r2 - B * r1
        c_str = f"+ {num_c}" if num_c >= 0 else f"- {abs(num_c)}"
        return {
            "prompt_text": "Find the partial fraction decomposition of the rational expression.",
            "equation_typst": f"$ ({num_x}x {c_str})/((x - {r1})(x + {r2})) $",
            "answer_typst": f"$ ({A})/(x - {r1}) + ({B})/(x + {r2}) $",
            "steps_typst": [
                f"Set up the decomposition: $({num_x}x {c_str})/((x - {r1})(x + {r2})) = A/(x - {r1}) + B/(x + {r2})$.",
                f"Clear denominators: ${num_x}x {c_str} = A(x + {r2}) + B(x - {r1})$.",
                f"Evaluate at $x = {r1}$ to get $A = {A}$ and at $x = {-r2}$ to get $B = {B}$.",
            ],
            "distractors": [
                f"$ ({B})/(x - {r1}) + ({A})/(x + {r2}) $",
                f"$ ({A})/(x - {r1}) - ({B})/(x + {r2}) $",
                f"$ ({A + 1})/(x - {r1}) + ({B - 1})/(x + {r2}) $",
            ],
        }

    if c_low in ("matrices", "matrices and systems") and "geometric transformation" in t_low:
        px, py = rng.randint(2, 6), rng.randint(1, 5)
        # 90 deg counterclockwise rotation matrix [0 -1; 1 0]
        nx, ny = -py, px
        return {
            "prompt_text": "Multiply the transformation matrix by the point matrix and plot both on the coordinate plane.",
            "equation_typst": f"$ mat(0, -1; 1, 0) mat({px}; {py}) $",
            "answer_typst": f"$ mat({nx}; {ny}) quad (90^circle \" CCW rotation\") $",
            "steps_typst": [
                f"Multiply the first row by the column vector: $0({px}) + (-1)({py}) = {nx}$.",
                f"Multiply the second row by the column vector: $1({px}) + 0({py}) = {ny}$.",
                f"Image point: $({nx}, {ny})$.",
            ],
            "distractors": [
                f"$ mat({py}; {-px}) $",
                f"$ mat({-px}; {-py}) $",
                f"$ mat({px}; {-py}) $",
            ],
            "diagram_svg": svg_coordinate_plane(points=[(px, py, f"P({px},{py})", True)]),
            "answer_svg": svg_coordinate_plane(points=[(px, py, f"P({px},{py})", True), (nx, ny, f"P'({nx},{ny})", True)]),
        }

    # ------------------------------------------------------------------
    # 2. COMPLEX NUMBERS (GRAPHING, ABSOLUTE VALUE, POLAR FORM)
    # ------------------------------------------------------------------
    if c_low == "complex numbers":
        if "graphing" in t_low:
            a = rng.choice([-6, -4, -3, 2, 4, 6])
            b = rng.choice([-5, -3, 3, 5, 7])
            b_str = f"+ {b}i" if b > 0 else f"- {abs(b)}i"
            return {
                "prompt_text": "Plot the complex number on the complex (Argand) plane and identify its real and imaginary parts.",
                "equation_typst": f"$ z = {a} {b_str} $",
                "answer_typst": f"$ \"Re\"(z) = {a}, quad \"Im\"(z) = {b}, quad \"Point\": ({a}, {b}) $",
                "steps_typst": [
                    f"The horizontal axis represents the real part $\"Re\"(z) = {a}$.",
                    f"The vertical axis represents the imaginary part $\"Im\"(z) = {b}$.",
                    f"Plot the point $({a}, {b})$ on the complex plane.",
                ],
                "distractors": [
                    f"$ \"Re\"(z) = {b}, quad \"Im\"(z) = {a}, quad \"Point\": ({b}, {a}) $",
                    f"$ \"Re\"(z) = {-a}, quad \"Im\"(z) = {-b}, quad \"Point\": ({-a}, {-b}) $",
                    f"$ \"Re\"(z) = {a}, quad \"Im\"(z) = {-b}, quad \"Point\": ({a}, {-b}) $",
                ],
                "diagram_svg": svg_coordinate_plane(),
                "answer_svg": svg_coordinate_plane(vectors=[{"x1": 0, "y1": 0, "x2": a, "y2": b, "color": "#2563eb", "label": f"{a}{b_str}"}], points=[(a, b, "", True)]),
            }
        if "absolute value" in t_low:
            a, b, r = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10)])
            a *= rng.choice([-1, 1])
            b *= rng.choice([-1, 1])
            b_str = f"+ {b}i" if b > 0 else f"- {abs(b)}i"
            return {
                "prompt_text": "Find the absolute value (modulus) of the complex number.",
                "equation_typst": f"$ |{a} {b_str}| $",
                "answer_typst": f"$ {r} $",
                "steps_typst": [
                    "The modulus of $a + b i$ is $|a + b i| = sqrt(a^2 + b^2)$.",
                    f"Substitute $a = {a}$ and $b = {b}$: $sqrt(({a})^2 + ({b})^2) = sqrt({a*a + b*b})$.",
                    f"Simplify: ${r}$.",
                ],
                "distractors": [f"$ {abs(a) + abs(b)} $", f"$ {r * r} $", f"$ {r + 2} $"],
                "diagram_svg": svg_coordinate_plane(),
                "answer_svg": svg_coordinate_plane(vectors=[{"x1": 0, "y1": 0, "x2": max(-8, min(8, a)), "y2": max(-8, min(8, b)), "color": "#dc2626", "label": f"|z|={r}"}]),
            }

    if "complex numbers in polar form" in t_low:
        r = rng.choice([2, 4, 6, 8])
        deg = rng.choice([30, 45, 60, 120, 135, 150, 240, 300])
        return {
            "prompt_text": "Plot the complex number in polar form on the polar grid and find its modulus and argument.",
            "equation_typst": f"$ z = {r}(cos({deg}^circle) + i sin({deg}^circle)) $",
            "answer_typst": f"$ |z| = {r}, quad theta = {deg}^circle $",
            "steps_typst": [
                f"In polar form $z = r(cos theta + i sin theta)$, the modulus is $r = {r}$.",
                f"The argument (angle from the positive real axis) is $theta = {deg}^circle$.",
                f"Plot at radius $r = {min(r, 4)}$ along ray ${deg}^circle$.",
            ],
            "distractors": [
                f"$ |z| = {r * r}, quad theta = {deg}^circle $",
                f"$ |z| = {r}, quad theta = {360 - deg}^circle $",
                f"$ |z| = {r // 2}, quad theta = {deg + 90}^circle $",
            ],
            "diagram_svg": svg_polar_grid(),
            "answer_svg": svg_polar_grid(points=[(min(r / 2, 4), deg, "z")]),
        }

    # ------------------------------------------------------------------
    # 3. BINOMIAL THEOREM, POLYNOMIAL THEOREMS, END BEHAVIOR & GRAPHING
    # ------------------------------------------------------------------
    if "binomial theorem" in t_low:
        n = rng.choice([3, 4, 5])
        b = rng.randint(1, 3)
        k = rng.randint(1, n - 1)
        comb = math.comb(n, k)
        coeff = comb * (b ** k)
        exp_x = n - k
        return {
            "prompt_text": "Use the Binomial Theorem to find the specified term in the expansion.",
            "equation_typst": f"\"Find the coefficient of \" x^{exp_x} \" in \" (x + {b})^{n}",
            "answer_typst": f"$ {coeff}x^{exp_x} $",
            "steps_typst": [
                f"By the Binomial Theorem, the general term is $binom(n, k) x^(n-k) b^k$ with $n = {n}, k = {k}, b = {b}$.",
                f"Compute $binom({n}, {k}) = {comb}$ and ${b}^{k} = {b ** k}$.",
                f"Multiply: ${comb} times {b ** k} x^{exp_x} = {coeff}x^{exp_x}$.",
            ],
            "distractors": [
                f"$ {comb}x^{exp_x} $",
                f"$ {coeff + b}x^{exp_x} $",
                f"$ {b ** k}x^{exp_x} $",
            ],
        }

    if "sum/difference of cubes" in t_low or "sum/differenc" in t_low:
        a_base = rng.choice([1, 1, 1, 2, 3, 4, 5])
        b_base = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        while math.gcd(a_base, b_base) > 1:
            b_base = rng.randint(1, 10)
        is_sum = rng.choice([True, False])
        sgn1 = "+" if is_sum else "-"
        sgn2 = "-" if is_sum else "+"
        a3 = a_base ** 3
        b3 = b_base ** 3
        a_term = f"{a_base}x" if a_base > 1 else "x"
        a3_term = f"{a3}x^3" if a3 > 1 else "x^3"
        a2_term = f"{a_base * a_base}x^2" if a_base > 1 else "x^2"
        mid_term = f"{a_base * b_base}x"
        b2 = b_base * b_base
        return {
            "prompt_text": "Factor the sum or difference of cubes completely.",
            "equation_typst": f"$ {a3_term} {sgn1} {b3} $",
            "answer_typst": f"$ ({a_term} {sgn1} {b_base})({a2_term} {sgn2} {mid_term} + {b2}) $",
            "steps_typst": [
                f"Rewrite as cubes: $({a_term})^3 {sgn1} {b_base}^3$.",
                f"Apply the identity $A^3 {sgn1} B^3 = (A {sgn1} B)(A^2 {sgn2} A B + B^2)$.",
                f"Substitute $A = {a_term}$ and $B = {b_base}$: $({a_term} {sgn1} {b_base})({a2_term} {sgn2} {mid_term} + {b2})$.",
            ],
            "distractors": [
                f"$ ({a_term} {sgn1} {b_base})({a2_term} {sgn1} {mid_term} + {b2}) $",
                f"$ ({a_term} {sgn1} {b_base})^3 $",
                f"$ ({a_term} {sgn2} {b_base})({a2_term} {sgn1} {mid_term} - {b2}) $",
            ],
        }

    if "remainder theorem" in t_low:
        c = rng.choice([-3, -2, -1, 2, 3])
        a2, a1, a0 = rng.randint(1, 3), rng.randint(-5, 5), rng.randint(-6, 6)
        rem = (c ** 3) + a2 * (c ** 2) + a1 * c + a0
        s2 = f"+ {a2}x^2" if a2 > 0 else (f"- {abs(a2)}x^2" if a2 < 0 else "")
        s1 = f"+ {a1}x" if a1 > 0 else (f"- {abs(a1)}x" if a1 < 0 else "")
        s0 = f"+ {a0}" if a0 > 0 else (f"- {abs(a0)}" if a0 < 0 else "")
        div_str = f"x - {c}" if c > 0 else f"x + {abs(c)}"
        return {
            "prompt_text": "Use the Remainder Theorem to evaluate P(c) and find the remainder of the division.",
            "equation_typst": f"$ P(x) = x^3 {s2} {s1} {s0} quad \"divided by\" quad ({div_str}) $",
            "answer_typst": f"$ P({c}) = {rem} $",
            "steps_typst": [
                f"By the Remainder Theorem, the remainder when $P(x)$ is divided by $({div_str})$ is $P({c})$.",
                f"Substitute $x = {c}$: $({c})^3 + ({a2})({c})^2 + ({a1})({c}) + ({a0})$.",
                f"Simplify: $P({c}) = {rem}$.",
            ],
            "distractors": [f"$ P({c}) = {rem + c} $", f"$ P({c}) = {-rem} $", f"$ P({c}) = {rem - 2 * a0} $"],
        }

    if "descartes" in t_low:
        c2, c1, c0 = -rng.randint(2, 6), rng.randint(2, 7), -rng.randint(1, 8)
        return {
            "prompt_text": "Use Descartes' Rule of Signs to state the possible number of positive and negative real zeros.",
            "equation_typst": f"$ P(x) = x^3 - {abs(c2)}x^2 + {c1}x - {abs(c0)} $",
            "answer_typst": "$ \"Positive real zeros\": 3 \" or \" 1; quad \"Negative real zeros\": 0 $",
            "steps_typst": [
                "Count sign changes in $P(x)$: $+ arrow.r - arrow.r + arrow.r -$ has $3$ sign changes, so $3$ or $1$ positive real zeros.",
                f"Evaluate $P(-x) = -x^3 - {abs(c2)}x^2 - {c1}x - {abs(c0)}$, which has $0$ sign changes.",
                "Therefore: $3$ or $1$ positive real zeros, and $0$ negative real zeros.",
            ],
            "distractors": [
                "$ \"Positive\": 2 \" or \" 0; quad \"Negative\": 1 $",
                "$ \"Positive\": 3; quad \"Negative\": 3 \" or \" 1 $",
                "$ \"Positive\": 1; quad \"Negative\": 2 \" or \" 0 $",
            ],
        }

    if "rational zero" in t_low:
        p = rng.choice([3, 5, 6, 8, 10])
        divs = [d for d in range(1, p + 1) if p % d == 0]
        pm_str = ", ".join(f"plus.minus {d}" for d in divs)
        return {
            "prompt_text": "Use the Rational Zero Theorem to list all possible rational zeros of the polynomial.",
            "equation_typst": f"$ P(x) = x^3 + {rng.randint(2, 6)}x^2 - {rng.randint(2, 5)}x + {p} $",
            "answer_typst": f"$ {pm_str} $",
            "steps_typst": [
                f"Identify factors of the constant term $p = {p}$: ${pm_str}$.",
                "Identify factors of the leading coefficient $q = 1$: $plus.minus 1$.",
                f"Possible rational zeros $p/q$: ${pm_str}$.",
            ],
            "distractors": [
                f"$ {', '.join(str(d) for d in divs)} $",
                f"$ plus.minus 1, plus.minus {p + 1} $",
                "$ plus.minus 2, plus.minus 4 $",
            ],
        }

    if "fundamental theorem of algebra" in t_low or "complex zeros" in t_low:
        deg_case = rng.choice(["deg3", "deg4", "deg5"])
        if deg_case == "deg4":
            r1 = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            r2 = rng.choice([k for k in range(-5, 6) if k != 0 and k != r1])
            b = rng.randint(1, 8)
            s_r1 = f"- {r1}" if r1 > 0 else f"+ {abs(r1)}"
            s_r2 = f"- {r2}" if r2 > 0 else f"+ {abs(r2)}"
            return {
                "prompt_text": "State the total number of complex zeros (counting multiplicity) and find all zeros of the polynomial.",
                "equation_typst": f"$ P(x) = (x {s_r1})(x {s_r2})(x^2 + {b * b}) $",
                "answer_typst": f"$ 4 \" zeros\": x = {r1}, {r2}, plus.minus {b}i $",
                "steps_typst": [
                    "By the Fundamental Theorem of Algebra, a degree-4 polynomial has exactly $4$ complex zeros.",
                    f"Set linear factors to zero: $x = {r1}$ and $x = {r2}$.",
                    f"Set quadratic factor $x^2 + {b * b} = 0 ==> x = plus.minus {b}i$.",
                ],
                "distractors": [f"$ 4 \" zeros\": x = {-r1}, {-r2}, plus.minus {b} $", f"$ 2 \" zeros\": x = {r1}, {r2} $", f"$ 4 \" zeros\": x = {r1}, {r2}, plus.minus {b} $"],
            }
        elif deg_case == "deg5":
            r1 = rng.randint(1, 5)
            b = rng.randint(1, 6)
            c = rng.randint(b + 1, b + 6)
            return {
                "prompt_text": "State the total number of complex zeros (counting multiplicity) and find all zeros of the polynomial.",
                "equation_typst": f"$ P(x) = (x - {r1})(x^2 + {b * b})(x^2 + {c * c}) $",
                "answer_typst": f"$ 5 \" zeros\": x = {r1}, plus.minus {b}i, plus.minus {c}i $",
                "steps_typst": [
                    "By the Fundamental Theorem of Algebra, a degree-5 polynomial has exactly $5$ complex zeros.",
                    f"Linear root: $x = {r1}$.",
                    f"Quadratic factors yield $x = plus.minus {b}i$ and $x = plus.minus {c}i$.",
                ],
                "distractors": [f"$ 3 \" zeros\": x = {r1}, {b}, {c} $", f"$ 5 \" zeros\": x = {-r1}, plus.minus {b}, plus.minus {c} $", "$ 1 \" zero\" $"],
            }
        else:
            r = rng.randint(-8, 8)
            while r == 0:
                r = rng.randint(-8, 8)
            b = rng.randint(1, 12)
            s_r = f"- {r}" if r > 0 else f"+ {abs(r)}"
            return {
                "prompt_text": "State the total number of complex zeros (counting multiplicity) and find all zeros of the polynomial.",
                "equation_typst": f"$ P(x) = (x {s_r})(x^2 + {b * b}) $",
                "answer_typst": f"$ 3 \" zeros\": x = {r}, plus.minus {b}i $",
                "steps_typst": [
                    "By the Fundamental Theorem of Algebra, a degree-3 polynomial has exactly $3$ complex zeros.",
                    f"Set linear factor to zero: $x = {r}$.",
                    f"Set quadratic factor $x^2 + {b * b} = 0 ==> x = plus.minus {b}i$.",
                ],
                "distractors": [f"$ 2 \" zeros\": x = {r}, {b} $", f"$ 3 \" zeros\": x = {-r}, plus.minus {b} $", f"$ 1 \" zero\": x = {r} $"],
            }

    if "end behavior" in t_low or ("polynomial" in c_low and "graph" in t_low and "rational" not in t_low):
        r1 = rng.randint(-4, -1)
        r2 = rng.choice([0, rng.randint(-1, 1)])
        if r2 == r1:
            r2 = 0
        r3 = rng.randint(max(r1 + 1, r2 + 1), 5)
        roots = sorted(list({r1, r2, r3}))
        if len(roots) < 3:
            roots = [-3, 0, 3]
        r1, r2, r3 = roots
        sgn = rng.choice([1, -1])

        def _fn_poly(x, _s=sgn, _r1=r1, _r2=r2, _r3=r3):
            return _s * 0.12 * (x - _r1) * (x - _r2) * (x - _r3)
        eb_left = "-infinity" if sgn > 0 else "+infinity"
        eb_right = "+infinity" if sgn > 0 else "-infinity"
        p1 = f"(x {'+' if r1 < 0 else '-'} {abs(r1)})" if r1 != 0 else "x"
        p2 = f"(x {'+' if r2 < 0 else '-'} {abs(r2)})" if r2 != 0 else "x"
        p3 = f"(x {'+' if r3 < 0 else '-'} {abs(r3)})" if r3 != 0 else "x"
        fac_str = f"{p1}{p2}{p3}"
        return {
            "prompt_text": "Describe the end behavior, find the real zeros, and sketch the graph of the polynomial function.",
            "equation_typst": f"$ f(x) = {'-' if sgn < 0 else ''}{fac_str} $",
            "answer_typst": f"$ \"Zeros\": x = {r1}, {r2}, {r3}; quad x arrow.r -infinity, f(x) arrow.r {eb_left}; quad x arrow.r +infinity, f(x) arrow.r {eb_right} $",
            "steps_typst": [
                f"Set each factor to zero to find the $x$-intercepts: $x = {r1}, {r2}, {r3}$.",
                f"The degree is $3$ (odd) and leading coefficient is ${sgn}$, so as $x arrow.r -infinity, f(x) arrow.r {eb_left}$.",
                f"As $x arrow.r +infinity, f(x) arrow.r {eb_right}$.",
            ],
            "distractors": [
                f"$ \"Zeros\": x = {r1}, {r2}, {r3}; quad x arrow.r -infinity, f(x) arrow.r {eb_right}; quad x arrow.r +infinity, f(x) arrow.r {eb_left} $",
                f"$ \"Zeros\": x = {r1}, {r3}; quad x arrow.r plus.minus infinity, f(x) arrow.r +infinity $",
                f"$ \"Zeros\": x = {r2}, {r1 * r3}; quad x arrow.r plus.minus infinity, f(x) arrow.r -infinity $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                functions=[{"fn": _fn_poly, "color": "#2563eb"}],
                points=[(r1, 0, f"({r1},0)", True), (r2, 0, f"({r2},0)", True), (r3, 0, f"({r3},0)", True)],
            ),
        }

    # ------------------------------------------------------------------
    # 4. RADICAL & RATIONAL GRAPHING, TRANSFORMATIONS, PIECEWISE, INEQUALITIES
    # ------------------------------------------------------------------
    if "graphing radical" in t_low or "domain and range of radical" in t_low:
        h = rng.randint(-4, 2)
        k = rng.randint(-3, 3)
        h_str = f"- {h}" if h > 0 else (f"+ {abs(h)}" if h < 0 else "")
        k_str = f"+ {k}" if k > 0 else (f"- {abs(k)}" if k < 0 else "")

        def _fn_rad(x, _h=h, _k=k):
            return (math.sqrt(x - _h) + _k) if x >= _h else float("nan")
        return {
            "prompt_text": "State the domain and range of the radical function and sketch its graph.",
            "equation_typst": f"$ f(x) = sqrt(x {h_str}) {k_str} $",
            "answer_typst": f"$ \"Domain\": [{h}, infinity), quad \"Range\": [{k}, infinity) $",
            "steps_typst": [
                f"The radicand must be non-negative: ${'x ' + h_str if h_str else 'x'} >= 0 ==> x >= {h}$.",
                f"Since $sqrt(x {h_str}) >= 0$, the minimum output is $y = {k}$ at the endpoint $({h}, {k})$.",
                f"Domain: $[{h}, infinity)$, Range: $[{k}, infinity)$.",
            ],
            "distractors": [
                f"$ \"Domain\": [{-h}, infinity), quad \"Range\": [{-k}, infinity) $",
                f"$ \"Domain\": (-infinity, {h}], quad \"Range\": (-infinity, {k}] $",
                f"$ \"Domain\": [{k}, infinity), quad \"Range\": [{h}, infinity) $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                functions=[{"fn": _fn_rad, "color": "#2563eb", "x_start": h, "x_end": 10}],
                points=[(h, k, f"({h},{k})", True), (h + 4, k + 2, f"({h+4},{k+2})", True)],
            ),
        }

    if ("rational" in c_low and "graph" in t_low) or "graphs of rational" in t_low:
        h = rng.choice([-3, -2, 2, 3])
        k = rng.choice([-2, -1, 1, 2])
        a = rng.choice([2, 4])
        h_str = f"- {h}" if h > 0 else f"+ {abs(h)}"
        k_str = f"+ {k}" if k > 0 else f"- {abs(k)}"

        def _fn_rat(x, _a=a, _h=h, _k=k):
            return (_a / (x - _h) + _k) if abs(x - _h) > 0.25 else float("nan")
        return {
            "prompt_text": "Identify the vertical and horizontal asymptotes and sketch the graph of the rational function.",
            "equation_typst": f"$ f(x) = ({a})/(x {h_str}) {k_str} $",
            "answer_typst": f"$ \"VA\": x = {h}, quad \"HA\": y = {k} $",
            "steps_typst": [
                f"Set the denominator to zero to find the vertical asymptote: $x = {h}$.",
                f"Read the vertical shift for the horizontal asymptote: $y = {k}$.",
                "Plot branches in the regions separated by the asymptotes.",
            ],
            "distractors": [
                f"$ \"VA\": x = {-h}, quad \"HA\": y = {-k} $",
                f"$ \"VA\": x = {k}, quad \"HA\": y = {h} $",
                f"$ \"VA\": y = {h}, quad \"HA\": x = {k} $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                functions=[{"fn": _fn_rat, "color": "#2563eb"}],
                vertical_lines=[{"x": h, "color": "#dc2626", "dashed": True}],
                asymptotes=[{"y": k, "color": "#dc2626"}],
            ),
        }

    if "transformations of graphs" in t_low:
        h = rng.choice([-4, -3, -2, 2, 3, 4])
        k = rng.choice([-3, -2, 2, 3])
        h_dir = "right" if h > 0 else "left"
        k_dir = "up" if k > 0 else "down"
        h_str = f"- {h}" if h > 0 else f"+ {abs(h)}"
        k_str = f"+ {k}" if k > 0 else f"- {abs(k)}"
        return {
            "prompt_text": "Describe the transformations from the parent function f(x) = x^2 to g(x) and sketch both graphs.",
            "equation_typst": f"$ g(x) = (x {h_str})^2 {k_str} $",
            "answer_typst": f"$ \"Shift {abs(h)} units {h_dir} and {abs(k)} units {k_dir}\" $",
            "steps_typst": [
                f"Inside the parentheses, $x {h_str}$ shifts the graph horizontally ${abs(h)}$ units {h_dir}.",
                f"Outside the parentheses, ${k_str}$ shifts the graph vertically ${abs(k)}$ units {k_dir}.",
                f"New vertex is $({h}, {k})$.",
            ],
            "distractors": [
                f"$ \"Shift {abs(h)} units {'left' if h > 0 else 'right'} and {abs(k)} units {'down' if k > 0 else 'up'}\" $",
                f"$ \"Shift {abs(k)} units {h_dir} and {abs(h)} units {k_dir}\" $",
                f"$ \"Stretch by {abs(h)} and shift {abs(k)} units {k_dir}\" $",
            ],
            "diagram_svg": svg_coordinate_plane(functions=[{"fn": lambda x: 0.25 * x * x, "color": "#94a3b8", "dashed": True}]),
            "answer_svg": svg_coordinate_plane(
                functions=[
                    {"fn": lambda x: 0.25 * x * x, "color": "#94a3b8", "dashed": True},
                    {"fn": lambda x, _h=h, _k=k: 0.25 * ((x - _h) ** 2) + _k, "color": "#2563eb"},
                ],
                points=[(h, k, f"({h},{k})", True)],
            ),
        }

    if "piecewise functions" in t_low:
        c = rng.randint(-1, 2)
        m1, b1 = 1, rng.randint(1, 3)
        m2, b2 = -1, rng.randint(2, 5)
        x_eval = c + rng.choice([-3, 3])
        val = (m1 * x_eval + b1) if x_eval < c else (m2 * x_eval + b2)
        return {
            "prompt_text": "Evaluate the piecewise function at the given input and sketch its graph.",
            "equation_typst": f"$ f(x) = cases(x + {b1} & \"if \" x < {c}, -x + {b2} & \"if \" x >= {c}); quad \"Find \" f({x_eval}) $",
            "answer_typst": f"$ f({x_eval}) = {val} $",
            "steps_typst": [
                f"Compare $x = {x_eval}$ with the boundary $x = {c}$.",
                f"Since ${x_eval} {'<' if x_eval < c else '>='} {c}$, use the {'first' if x_eval < c else 'second'} branch.",
                f"Compute $f({x_eval}) = {val}$.",
            ],
            "distractors": [
                f"$ f({x_eval}) = {(m2 * x_eval + b2) if x_eval < c else (m1 * x_eval + b1)} $",
                f"$ f({x_eval}) = {c + b1} $",
                f"$ f({x_eval}) = {val + 2} $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                functions=[
                    {"fn": lambda x, _b1=b1: x + _b1, "x_start": -10, "x_end": c, "color": "#2563eb"},
                    {"fn": lambda x, _b2=b2: -x + _b2, "x_start": c, "x_end": 10, "color": "#dc2626"},
                ],
                points=[(c, c + b1, "", False), (c, -c + b2, "", True)],
            ),
        }

    if "polynomial inequalities" in t_low or "rational inequalities" in t_low:
        r1 = rng.randint(-6, -1)
        r2 = rng.randint(1, 6)
        is_rat = "rational" in t_low
        eq = f"$ (x + {abs(r1)})/(x - {r2}) <= 0 $" if is_rat else f"$ (x + {abs(r1)})(x - {r2}) <= 0 $"
        ans = f"$ [{r1}, {r2}) $" if is_rat else f"$ [{r1}, {r2}] $"
        return {
            "prompt_text": f"Solve the {'rational' if is_rat else 'polynomial'} inequality and graph the solution set on the number line.",
            "equation_typst": eq,
            "answer_typst": ans,
            "steps_typst": [
                f"Find the critical boundary values: $x = {r1}$ and $x = {r2}$.",
                f"Test signs on the intervals $(-infinity, {r1})$, $({r1}, {r2})$, and $({r2}, infinity)$: the expression is negative on $({r1}, {r2})$.",
                f"Include endpoints where defined: {ans.strip('$ ')}.",
            ],
            "distractors": [
                f"$ (-infinity, {r1}] union [{r2}, infinity) $",
                f"$ ({r1}, {r2}) $",
                f"$ [{r1}, {r2}{']' if is_rat else ')'} $",
            ],
            "diagram_svg": svg_number_line(),
            "answer_svg": svg_number_line(segments=[(r1, r2, True, not is_rat)]),
        }

    # ------------------------------------------------------------------
    # 5. CONIC SECTIONS, PARAMETRIC, POLAR, VECTORS
    # ------------------------------------------------------------------
    if c_low == "conic sections":
        h, k = rng.randint(-2, 2), rng.randint(-2, 2)
        hx = f"(x - {h})^2" if h > 0 else (f"(x + {abs(h)})^2" if h < 0 else "x^2")
        f"(y - {k})^2" if k > 0 else (f"(y + {abs(k)})^2" if k < 0 else "y^2")
        if "parabola" in t_low:
            p = rng.choice([1, 2, -1, -2])

            def _fn_parab(x, _h=h, _k=k, _p=p):
                return ((x - _h) ** 2) / (4 * _p) + _k
            return {
                "prompt_text": "Identify the vertex, focus, and directrix of the parabola and sketch its graph.",
                "equation_typst": f"$ {hx} = {4 * p}(y - {k}) $" if k != 0 else f"$ {hx} = {4 * p}y $",
                "answer_typst": f"$ \"Vertex\": ({h}, {k}), quad \"Focus\": ({h}, {k + p}), quad \"Directrix\": y = {k - p} $",
                "steps_typst": [
                    f"Match $(x - h)^2 = 4p(y - k)$ with $(h, k) = ({h}, {k})$ and $4p = {4 * p} arrow.r.double p = {p}$.",
                    f"The focus is $(h, k + p) = ({h}, {k + p})$.",
                    f"The directrix is $y = k - p = {k - p}$.",
                ],
                "distractors": [
                    f"$ \"Vertex\": ({h}, {k}), quad \"Focus\": ({h + p}, {k}), quad \"Directrix\": x = {h - p} $",
                    f"$ \"Vertex\": ({-h}, {-k}), quad \"Focus\": ({-h}, {-k + p}), quad \"Directrix\": y = {-k - p} $",
                    f"$ \"Vertex\": ({h}, {k}), quad \"Focus\": ({h}, {k + 4 * p}), quad \"Directrix\": y = {k - 4 * p} $",
                ],
                "diagram_svg": svg_coordinate_plane(),
                "answer_svg": svg_coordinate_plane(
                    functions=[{"fn": _fn_parab, "color": "#2563eb"}],
                    asymptotes=[{"y": k - p, "color": "#dc2626"}],
                    points=[(h, k, "V", True), (h, k + p, "F", True)],
                ),
            }
        if "hyperbola" in t_low:
            a = rng.randint(2, 6)
            b = rng.randint(2, 6)
            h = rng.choice([-3, -2, -1, 0, 0, 1, 2, 3]) if scale >= 2 else 0
            k = rng.choice([-3, -2, -1, 0, 0, 1, 2, 3]) if scale >= 2 else 0
            c_sq = a * a + b * b
            x_term = "x^2" if h == 0 else f"(x {'+' if h < 0 else '-'} {abs(h)})^2"
            y_term = "y^2" if k == 0 else f"(y {'+' if k < 0 else '-'} {abs(k)})^2"

            def fn_r(x, _a=a, _b=b, _h=h, _k=k):
                val = ((x - _h) / _a) ** 2 - 1.0
                return _k + _b * math.sqrt(val) if abs(x - _h) >= _a and val >= 0 else float("nan")

            def fn_rb(x, _a=a, _b=b, _h=h, _k=k):
                val = ((x - _h) / _a) ** 2 - 1.0
                return _k - _b * math.sqrt(val) if abs(x - _h) >= _a and val >= 0 else float("nan")
            return {
                "prompt_text": "Identify the center, vertices, foci, and asymptotes of the hyperbola and sketch its graph.",
                "equation_typst": f"$ {x_term}/({a * a}) - {y_term}/({b * b}) = 1 $",
                "answer_typst": f"$ \"Center\": ({h}, {k}), quad \"Vertices\": ({h} plus.minus {a}, {k}), quad \"Foci\": ({h} plus.minus sqrt({c_sq}), {k}) $",
                "steps_typst": [
                    f"From $(x - h)^2/a^2 - (y - k)^2/b^2 = 1$, center is $({h}, {k})$ with $a = {a}$ and $b = {b}$.",
                    f"Vertices are at $({h} plus.minus {a}, {k}) = ({h + a}, {k})$ and $({h - a}, {k})$.",
                    f"Compute $c^2 = a^2 + b^2 = {a * a} + {b * b} = {c_sq}$, giving foci $({h} plus.minus sqrt({c_sq}), {k})$.",
                    f"Asymptotes have slopes $plus.minus b/a = plus.minus ({b})/({a})$ passing through $({h}, {k})$.",
                ],
                "distractors": [
                    f"$ \"Center\": ({k}, {h}), quad \"Vertices\": ({k}, {h} plus.minus {a}), quad \"Foci\": ({k}, {h} plus.minus sqrt({c_sq})) $",
                    f"$ \"Center\": ({h}, {k}), quad \"Vertices\": ({h} plus.minus {a * a}, {k}), quad \"Foci\": ({h} plus.minus {c_sq}, {k}) $",
                    f"$ \"Center\": (0, 0), quad \"Vertices\": (plus.minus {b}, 0), quad \"Foci\": (plus.minus sqrt({c_sq}), 0) $",
                ],
                "diagram_svg": svg_coordinate_plane(),
                "answer_svg": svg_coordinate_plane(
                    functions=[{"fn": fn_r, "color": "#2563eb"}, {"fn": fn_rb, "color": "#2563eb"}],
                    lines=[{"m": b / a, "b": k - (b / a) * h, "color": "#94a3b8", "dashed": True}, {"m": -b / a, "b": k + (b / a) * h, "color": "#94a3b8", "dashed": True}],
                    points=[(h + a, k, f"({h+a},{k})", True), (h - a, k, f"({h-a},{k})", True)],
                ),
            }
        if "ellipse" in t_low:
            a = rng.randint(3, 8)
            b = rng.randint(2, a - 1)
            h = rng.choice([-3, -2, -1, 0, 0, 1, 2, 3]) if scale >= 2 else 0
            k = rng.choice([-3, -2, -1, 0, 0, 1, 2, 3]) if scale >= 2 else 0
            c_sq = a * a - b * b
            x_term = "x^2" if h == 0 else f"(x {'+' if h < 0 else '-'} {abs(h)})^2"
            y_term = "y^2" if k == 0 else f"(y {'+' if k < 0 else '-'} {abs(k)})^2"
            return {
                "prompt_text": "Identify the center, vertices, co-vertices, and foci of the ellipse and sketch its graph.",
                "equation_typst": f"$ {x_term}/({a * a}) + {y_term}/({b * b}) = 1 $",
                "answer_typst": f"$ \"Center\": ({h}, {k}), quad \"Vertices\": ({h} plus.minus {a}, {k}), quad \"Co-vertices\": ({h}, {k} plus.minus {b}) $",
                "steps_typst": [
                    f"Here center is $({h}, {k})$, $a^2 = {a * a} arrow.r.double a = {a}$ and $b^2 = {b * b} arrow.r.double b = {b}$.",
                    f"Major vertices are $({h} plus.minus {a}, {k})$ and co-vertices are $({h}, {k} plus.minus {b})$.",
                    f"Compute $c^2 = a^2 - b^2 = {c_sq}$, so foci are $({h} plus.minus sqrt({c_sq}), {k})$.",
                ],
                "distractors": [
                    f"$ \"Center\": ({h}, {k}), quad \"Vertices\": ({h}, {k} plus.minus {a}), quad \"Co-vertices\": ({h} plus.minus {b}, {k}) $",
                    f"$ \"Center\": (0, 0), quad \"Vertices\": (plus.minus {a}, 0), quad \"Co-vertices\": (0, plus.minus {b}) $",
                    f"$ \"Center\": ({h}, {k}), quad \"Vertices\": ({h} plus.minus {a * a}, {k}), quad \"Co-vertices\": ({h}, {k} plus.minus {b * b}) $",
                ],
                "diagram_svg": svg_coordinate_plane(),
                "answer_svg": svg_coordinate_plane(
                    circles=[{"h": h, "k": k, "rx": a, "ry": b, "color": "#2563eb"}],
                    points=[(h + a, k, f"({h+a},{k})", True), (h - a, k, f"({h-a},{k})", True), (h, k + b, f"({h},{k+b})", True), (h, k - b, f"({h},{k-b})", True)],
                ),
            }
        if "classifying" in t_low:
            kind = rng.choice(["Circle", "Ellipse", "Parabola", "Hyperbola"])
            h_c, k_c = rng.randint(-5, 5), rng.randint(-5, 5)
            if kind == "Circle":
                A = C = rng.choice([1, 2, 3])
                D = -2 * A * h_c
                E = -2 * A * k_c
                r_val = rng.randint(2, 6)
                F = A * (h_c ** 2 + k_c ** 2 - r_val ** 2)
            elif kind == "Ellipse":
                A = rng.choice([2, 3, 4, 9])
                C = rng.choice([x for x in [1, 2, 4, 5, 16] if x != A])
                D = -2 * A * h_c
                E = -2 * C * k_c
                F = A * h_c ** 2 + C * k_c ** 2 - 36
            elif kind == "Parabola":
                if rng.choice([True, False]):
                    A, C = 0, rng.choice([1, 2, 3])
                    D = rng.choice([-8, -6, -4, 4, 6, 8])
                    E = -2 * C * k_c
                    F = C * k_c ** 2 + rng.randint(-15, 15)
                else:
                    A, C = rng.choice([1, 2, 3]), 0
                    D = -2 * A * h_c
                    E = rng.choice([-8, -6, -4, 4, 6, 8])
                    F = A * h_c ** 2 + rng.randint(-15, 15)
            else:  # Hyperbola
                A = rng.choice([1, 2, 4, 9])
                C = -rng.choice([1, 2, 4, 9])
                D = -2 * A * h_c
                E = -2 * C * k_c
                F = A * h_c ** 2 + C * k_c ** 2 - 36

            terms = []
            if A != 0:
                terms.append(f"{A if A != 1 else ''}x^2")
            if C != 0:
                terms.append(f"{'+' if C > 0 else '-'} {abs(C) if abs(C) != 1 else ''}y^2")
            if D != 0:
                terms.append(f"{'+' if D > 0 else '-'} {abs(D)}x")
            if E != 0:
                terms.append(f"{'+' if E > 0 else '-'} {abs(E)}y")
            if F != 0:
                terms.append(f"{'+' if F > 0 else '-'} {abs(F)}")
            conic_eq = " ".join(terms).lstrip("+ ").replace("+ -", "- ") + " = 0"
            others = [k for k in ["Circle", "Ellipse", "Parabola", "Hyperbola"] if k != kind]
            return {
                "prompt_text": "Classify the conic section from its general second-degree equation.",
                "equation_typst": f"$ {conic_eq} $",
                "answer_typst": f"$ \"{kind}\" $",
                "steps_typst": [
                    "Examine the coefficients $A$ and $C$ of $x^2$ and $y^2$ in $A x^2 + C y^2 + D x + E y + F = 0$.",
                    f"Here $A = {A}$ and $C = {C}$.",
                    "Circle: $A = C != 0$; Ellipse: $A C > 0, A != C$; Parabola: $A C = 0$; Hyperbola: $A C < 0$.",
                    f"Classification: {kind}.",
                ],
                "distractors": [f"$ \"{o}\" $" for o in others],
            }

    if "parametric" in c_low:
        if "projectile" in t_low:
            t_peak = rng.randint(2, 7)
            h0 = rng.choice([0, 16, 32, 48, 64, 80])
            v0 = 32 * t_peak
            h_max = h0 + v0 * t_peak - 16 * (t_peak ** 2)
            eq_str = f"y(t) = {h0} + {v0}t - 16t^2" if h0 > 0 else f"y(t) = {v0}t - 16t^2"
            return {
                "prompt_text": f"A projectile is launched vertically with height {eq_str}. Find the time to reach maximum height and the maximum height.",
                "equation_typst": f"$ {eq_str} $",
                "answer_typst": f"$ t = {t_peak} \" s\", quad h_\"max\" = {h_max} \" ft\" $",
                "steps_typst": [
                    f"Find the vertex time $t = -b/(2a) = -{v0}/(2(-16)) = {t_peak}$ seconds.",
                    f"Evaluate $y({t_peak}) = {h0 + v0 * t_peak} - 16({t_peak})^2 = {h_max}$ feet.",
                    f"Answer: $t = {t_peak}$ s, $h_\"max\" = {h_max}$ ft.",
                ],
                "distractors": [
                    f"$ t = {2 * t_peak} \" s\", quad h_\"max\" = {h_max * 2} \" ft\" $",
                    f"$ t = {t_peak} \" s\", quad h_\"max\" = {v0 * t_peak} \" ft\" $",
                    f"$ t = {t_peak + 1} \" s\", quad h_\"max\" = {h_max + 16} \" ft\" $",
                ],
            }
        a = rng.randint(1, 3)
        b = rng.randint(1, 4)
        return {
            "prompt_text": "Eliminate the parameter t to write the rectangular equation and sketch the parametric curve.",
            "equation_typst": f"$ x(t) = t + {a}, quad y(t) = t^2 + {b} $",
            "answer_typst": f"$ y = (x - {a})^2 + {b} $",
            "steps_typst": [
                f"Solve the first equation for $t$: $t = x - {a}$.",
                f"Substitute $t = x - {a}$ into $y(t)$: $y = (x - {a})^2 + {b}$.",
                f"Rectangular equation: $y = (x - {a})^2 + {b}$.",
            ],
            "distractors": [
                f"$ y = (x + {a})^2 + {b} $",
                f"$ y = x^2 + {a + b} $",
                f"$ y = (x - {b})^2 + {a} $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(functions=[{"fn": lambda x, _a=a, _b=b: 0.4 * ((x - _a) ** 2) + _b, "color": "#2563eb"}], points=[(a, b, f"({a},{b})", True)]),
        }

    if c_low == "polar coordinates":
        r_val = rng.randint(2, 9)
        ang_deg = rng.choice([15 * k for k in range(1, 24)])

        if "polar_forms_of_conic_sect" in t_low or "conic" in t_low:
            conic_choice = rng.choice(["ellipse", "parabola", "hyperbola"])
            sign_str = rng.choice(["+", "-"])
            fn_trig = rng.choice(["cos", "sin"])
            directrix_var = "x" if fn_trig == "cos" else "y"
            directrix_sign = sign_str
            if conic_choice == "parabola":
                e_val = 1
                e_str = "1"
                d_val = rng.randint(2, 8)
                ed_val = d_val
                conic_name = "Parabola"
            elif conic_choice == "ellipse":
                num_e, den_e = rng.choice([(1, 2), (1, 3), (2, 3), (3, 4), (2, 5), (3, 5), (4, 5)])
                e_val = num_e / den_e
                e_str = f"{num_e}/{den_e}"
                d_val = den_e * rng.randint(1, 4)
                ed_val = int(num_e * (d_val // den_e))
                conic_name = "Ellipse"
            else:
                num_e, den_e = rng.choice([(2, 1), (3, 1), (3, 2), (4, 3), (5, 2), (5, 3), (5, 4)])
                e_val = num_e / den_e
                e_str = f"{num_e}" if den_e == 1 else f"{num_e}/{den_e}"
                d_val = den_e * rng.randint(1, 4)
                ed_val = int(num_e * (d_val // den_e))
                conic_name = "Hyperbola"

            dir_val_str = f"{directrix_sign}{d_val}" if directrix_sign == "-" else f"{d_val}"
            eq_typ = f"$ r = ({ed_val}) / (1 {sign_str} ({e_str}) {fn_trig}(theta)) $"
            ans_typ = f"$ \"{conic_name}, \" e = {e_str}, quad {directrix_var} = {dir_val_str} $"
            return {
                "prompt_text": "Identify the type of conic section, eccentricity e, and directrix from the polar equation.",
                "equation_typst": eq_typ,
                "answer_typst": ans_typ,
                "steps_typst": [
                    f"Match equation with standard polar conic form $r = (e d) / (1 {sign_str} e {fn_trig}(theta))$.",
                    f"Identify eccentricity $e = {e_str}$. Since {'e = 1' if e_val == 1 else ('e < 1' if e_val < 1 else 'e > 1')}, the conic is a {conic_name}.",
                    f"From the numerator $e d = {ed_val}$, solve for directrix $d = {ed_val} / ({e_str}) = {d_val}$. Directrix: ${directrix_var} = {dir_val_str}$.",
                ],
                "distractors": [
                    f"$ \"{'Hyperbola' if conic_name == 'Ellipse' else 'Ellipse'}, \" e = {e_str}, quad {directrix_var} = {dir_val_str} $",
                    f"$ \"{conic_name}, \" e = {d_val}, quad {directrix_var} = {ed_val} $",
                    f"$ \"{conic_name}, \" e = {e_str}, quad {directrix_var} = {-d_val if directrix_sign == '+' else d_val} $",
                ],
                "diagram_svg": svg_polar_grid(),
                "answer_svg": svg_polar_grid(),
            }

        if "polar_and_rectangular_for" in t_low or "rectangular" in t_low:
            sub = rng.choice(["p_to_r", "r_to_p"])
            if sub == "p_to_r":
                # Special angles with clean coordinates
                special = [
                    (0, "1", "0", 1, 0),
                    (30, "sqrt(3)/2", "1/2", math.sqrt(3)/2, 0.5),
                    (45, "sqrt(2)/2", "sqrt(2)/2", math.sqrt(2)/2, math.sqrt(2)/2),
                    (60, "1/2", "sqrt(3)/2", 0.5, math.sqrt(3)/2),
                    (90, "0", "1", 0, 1),
                    (120, "-1/2", "sqrt(3)/2", -0.5, math.sqrt(3)/2),
                    (135, "-sqrt(2)/2", "sqrt(2)/2", -math.sqrt(2)/2, math.sqrt(2)/2),
                    (180, "-1", "0", -1, 0),
                    (210, "-sqrt(3)/2", "-1/2", -math.sqrt(3)/2, -0.5),
                    (240, "-1/2", "-sqrt(3)/2", -0.5, -math.sqrt(3)/2),
                    (270, "0", "-1", 0, -1),
                    (300, "1/2", "-sqrt(3)/2", 0.5, -math.sqrt(3)/2),
                    (315, "sqrt(2)/2", "-sqrt(2)/2", math.sqrt(2)/2, -math.sqrt(2)/2),
                ]
                deg_item = rng.choice(special)
                d_ang, cos_s, sin_s, c_val, s_val = deg_item
                r_mult = rng.choice([2, 4, 6, 8, 10])
                x_val_clean = round(r_mult * c_val, 2)
                y_val_clean = round(r_mult * s_val, 2)
                return {
                    "prompt_text": "Convert the polar coordinates (r, theta) to exact rectangular coordinates (x, y).",
                    "equation_typst": f"$ (r, theta) = ({r_mult}, {d_ang}^circle) $",
                    "answer_typst": f"$ (x, y) = ({x_val_clean}, {y_val_clean}) $",
                    "steps_typst": [
                        f"Compute x-coordinate: $x = r cos(theta) = {r_mult} cos({d_ang}^circle) = {r_mult}({cos_s}) = {x_val_clean}$.",
                        f"Compute y-coordinate: $y = r sin(theta) = {r_mult} sin({d_ang}^circle) = {r_mult}({sin_s}) = {y_val_clean}$.",
                        f"Result: $(x, y) = ({x_val_clean}, {y_val_clean})$.",
                    ],
                    "distractors": [
                        f"$ (x, y) = ({y_val_clean}, {x_val_clean}) $",
                        f"$ (x, y) = ({-x_val_clean}, {y_val_clean}) $",
                        f"$ (x, y) = ({r_mult}, {d_ang}) $",
                    ],
                    "diagram_svg": svg_polar_grid(max_r=max(5, r_mult), points=[(r_mult, d_ang, "P")]),
                    "answer_svg": svg_coordinate_plane(points=[(x_val_clean, y_val_clean, f"({x_val_clean}, {y_val_clean})", True)]),
                }
            else:
                pts_rect = [(3, 4, 5, 53), (4, 3, 5, 37), (5, 12, 13, 67), (1, 1, "sqrt(2)", 45), (0, 4, 4, 90), (4, 0, 4, 0), (-3, 3, "3 sqrt(2)", 135), (-4, 0, 4, 180), (0, -5, 5, 270)]
                rx, ry, r_ans, th_ans = rng.choice(pts_rect)
                return {
                    "prompt_text": "Convert the rectangular coordinates (x, y) to polar coordinates (r, theta) with r > 0 and 0 <= theta < 360 deg.",
                    "equation_typst": f"$ (x, y) = ({rx}, {ry}) $",
                    "answer_typst": f"$ (r, theta) = ({r_ans}, {th_ans}^circle) $",
                    "steps_typst": [
                        f"Calculate radius $r = sqrt(x^2 + y^2) = sqrt(({rx})^2 + ({ry})^2) = {r_ans}$.",
                        f"Calculate angle $theta = arctan(y / x) = arctan(({ry}) / ({rx})) ==> theta = {th_ans}^circle$.",
                        f"Result: $(r, theta) = ({r_ans}, {th_ans}^circle)$.",
                    ],
                    "distractors": [
                        f"$ (r, theta) = ({r_ans}, {(th_ans + 90) % 360}^circle) $",
                        f"$ (r, theta) = ({rx + ry}, {th_ans}^circle) $",
                        f"$ (r, theta) = ({ry}, {rx}^circle) $",
                    ],
                    "diagram_svg": svg_coordinate_plane(points=[(rx, ry, f"({rx}, {ry})", True)]),
                    "answer_svg": svg_polar_grid(),
                }

        if "graphs_of_polar_equations" in t_low or "graphs" in t_low:
            p_type = rng.choice(["rose_cos", "rose_sin", "cardioid", "circle", "lemniscate"])
            if p_type == "rose_cos":
                n_pet = rng.choice([2, 3, 4, 5, 6, 7])
                pet_count = n_pet if n_pet % 2 == 1 else 2 * n_pet
                curve = [(r_val * math.cos(math.radians(n_pet * d)), d) for d in range(0, 361, 4)]
                eq_s = f"$ r = {r_val} cos({n_pet} theta) $"
                ans_s = f"$ \"Rose curve with \" {pet_count} \" petals, max radius \" r = {r_val} $"
                step_desc = f"Equations $r = a cos(n theta)$ form a rose curve. Since $n = {n_pet}$, it has ${pet_count}$ petals with maximum radius $|a| = {r_val}$."
            elif p_type == "rose_sin":
                n_pet = rng.choice([2, 3, 4, 5, 6, 7])
                pet_count = n_pet if n_pet % 2 == 1 else 2 * n_pet
                curve = [(r_val * math.sin(math.radians(n_pet * d)), d) for d in range(0, 361, 4)]
                eq_s = f"$ r = {r_val} sin({n_pet} theta) $"
                ans_s = f"$ \"Rose curve with \" {pet_count} \" petals, max radius \" r = {r_val} $"
                step_desc = f"Equations $r = a sin(n theta)$ form a rose curve with ${pet_count}$ petals and max radius ${r_val}$."
            elif p_type == "cardioid":
                curve = [((r_val + r_val * math.cos(math.radians(d))), d) for d in range(0, 361, 4)]
                eq_s = f"$ r = {r_val} + {r_val} cos(theta) $"
                ans_s = f"$ \"Cardioid symmetric to polar axis, max r = \" {2 * r_val} $"
                step_desc = f"Equations of the form $r = a + a cos(theta)$ form a cardioid (heart-shaped limaçon) with cusp at origin and max radius ${2 * r_val}$."
            elif p_type == "lemniscate":
                curve = [(r_val * math.sqrt(max(0, math.cos(math.radians(2 * d)))), d) for d in range(0, 361, 4)]
                eq_s = f"$ r^2 = {r_val * r_val} cos(2 theta) $"
                ans_s = f"$ \"Lemniscate (figure-eight) with max length \" {r_val} $"
                step_desc = f"Equations $r^2 = a^2 cos(2 theta)$ form a lemniscate symmetric about the pole with petal reach $|a| = {r_val}$."
            else:
                curve = [(r_val * math.cos(math.radians(d)), d) for d in range(0, 361, 4)]
                eq_s = f"$ r = {r_val} cos(theta) $"
                ans_s = f"$ \"Circle centered at \" ({round(r_val/2, 1)}, 0) \" with radius \" {round(r_val/2, 1)} $"
                step_desc = f"Multiply by $r$: $r^2 = {r_val} r cos(theta) ==> x^2 + y^2 = {r_val}x$, which is a circle of diameter ${r_val}$."

            return {
                "prompt_text": "Identify the symmetry and shape of the polar equation and sketch its graph on the polar grid.",
                "equation_typst": eq_s,
                "answer_typst": ans_s,
                "steps_typst": [
                    step_desc,
                    "Analyze symmetry: replace $theta$ with $-theta$ or $pi - theta$.",
                    "Plot key points and sketch the complete polar curve.",
                ],
                "distractors": [
                    f"$ \"Circle with radius \" {r_val} $",
                    f"$ \"Limaçon with inner loop, max r = \" {2 * r_val} $",
                    f"$ \"Archimedean spiral\" $",
                ],
                "diagram_svg": svg_polar_grid(),
                "answer_svg": svg_polar_grid(curve_points=curve),
            }

        # Default polar point plotting and equivalent representations
        r = r_val
        deg = ang_deg
        alt_deg1 = (deg + 360)
        alt_deg2 = (deg + 180) % 360
        return {
            "prompt_text": "Plot the polar point (r, theta) on the polar grid and find an equivalent polar representation with r > 0 and r < 0.",
            "equation_typst": f"$ P({r}, {deg}^circle) $",
            "answer_typst": f"$ ({r}, {alt_deg1}^circle) \" and \" ({-r}, {alt_deg2}^circle) $",
            "steps_typst": [
                f"Locate angle $theta = {deg}^circle$ on the grid and measure $r = {r}$ concentric units outward.",
                f"Adding $360^circle$ preserves direction: $({r}, {deg}^circle + 360^circle) = ({r}, {alt_deg1}^circle)$.",
                f"Negating $r$ and adding $180^circle$ reflects through the pole to the same point: $({-r}, {alt_deg2}^circle)$.",
            ],
            "distractors": [
                f"$ ({-r}, {deg}^circle) $",
                f"$ ({r}, {alt_deg2}^circle) $",
                f"$ ({r * 2}, {deg}^circle) $",
            ],
            "diagram_svg": svg_polar_grid(),
            "answer_svg": svg_polar_grid(max_r=max(5, r), points=[(r, deg, "P")]),
        }

    if "cross products" in t_low:
        u1, u2, u3 = rng.randint(1, 4), rng.randint(-3, 3), rng.randint(1, 4)
        v1, v2, v3 = rng.randint(-2, 3), rng.randint(1, 4), rng.randint(-3, 2)
        cx = u2 * v3 - u3 * v2
        cy = u3 * v1 - u1 * v3
        cz = u1 * v2 - u2 * v1
        return {
            "prompt_text": "Find the cross product u x v of the two three-dimensional vectors.",
            "equation_typst": f"$ bold(u) = angle.l {u1}, {u2}, {u3} angle.r, quad bold(v) = angle.l {v1}, {v2}, {v3} angle.r $",
            "answer_typst": f"$ bold(u) times bold(v) = angle.l {cx}, {cy}, {cz} angle.r $",
            "steps_typst": [
                f"Compute the $bold(i)$-component: $({u2})({v3}) - ({u3})({v2}) = {cx}$.",
                f"Compute the $bold(j)$-component: $({u3})({v1}) - ({u1})({v3}) = {cy}$.",
                f"Compute the $bold(k)$-component: $({u1})({v2}) - ({u2})({v1}) = {cz}$, giving $angle.l {cx}, {cy}, {cz} angle.r$.",
            ],
            "distractors": [
                f"$ angle.l {cx}, {-cy}, {cz} angle.r $",
                f"$ angle.l {-cx}, {-cy}, {-cz} angle.r $",
                f"$ angle.l {u1 * v1}, {u2 * v2}, {u3 * v3} angle.r $",
            ],
        }

    if c_low == "vectors" and "diagram" in t_low:
        ux, uy = rng.choice([3, 4, 5]), rng.choice([1, 2, 3])
        vx, vy = rng.choice([-2, 2, 3]), rng.choice([2, 3, 4])
        rx, ry = ux + vx, uy + vy
        return {
            "prompt_text": "Use the vector diagram on the coordinate plane to find the resultant vector u + v.",
            "equation_typst": f"$ bold(u) = angle.l {ux}, {uy} angle.r, quad bold(v) = angle.l {vx}, {vy} angle.r $",
            "answer_typst": f"$ bold(u) + bold(v) = angle.l {rx}, {ry} angle.r $",
            "steps_typst": [
                f"Place the tail of $bold(v)$ at the head of $bold(u)$ at $({ux}, {uy})$.",
                f"Add horizontal components: ${ux} + ({vx}) = {rx}$.",
                f"Add vertical components: ${uy} + ({vy}) = {ry}$, giving $angle.l {rx}, {ry} angle.r$.",
            ],
            "distractors": [
                f"$ angle.l {ux - vx}, {uy - vy} angle.r $",
                f"$ angle.l {ry}, {rx} angle.r $",
                f"$ angle.l {ux * vx}, {uy * vy} angle.r $",
            ],
            "diagram_svg": svg_coordinate_plane(
                vectors=[
                    {"x1": 0, "y1": 0, "x2": ux, "y2": uy, "color": "#2563eb", "label": "u"},
                    {"x1": ux, "y1": uy, "x2": rx, "y2": ry, "color": "#16a34a", "label": "v"},
                ]
            ),
            "answer_svg": svg_coordinate_plane(
                vectors=[
                    {"x1": 0, "y1": 0, "x2": ux, "y2": uy, "color": "#2563eb", "label": "u"},
                    {"x1": ux, "y1": uy, "x2": rx, "y2": ry, "color": "#16a34a", "label": "v"},
                    {"x1": 0, "y1": 0, "x2": rx, "y2": ry, "color": "#dc2626", "label": f"u+v=<{rx},{ry}>"},
                ]
            ),
        }

    # ------------------------------------------------------------------
    # 6. LOGARITHM GRAPHING, TRIG GRAPHING, LAW OF SINES/COSINES, PROBABILITY
    # ------------------------------------------------------------------
    if "graphing logarithmic" in t_low:
        h = rng.choice([-3, -2, 1, 2, 3])
        k = rng.choice([-2, 0, 2])
        h_str = f"- {h}" if h > 0 else f"+ {abs(h)}"
        k_str = f" + {k}" if k > 0 else (f" - {abs(k)}" if k < 0 else "")

        def _fn_log(x, _h=h, _k=k):
            return (math.log2(x - _h) + _k) if x > _h + 0.08 else float("nan")
        return {
            "prompt_text": "Identify the vertical asymptote, domain, and range, and sketch the logarithmic function.",
            "equation_typst": f"$ f(x) = log_2(x {h_str}){k_str} $",
            "answer_typst": f"$ \"VA\": x = {h}, quad \"Domain\": ({h}, infinity), quad \"Range\": (-infinity, infinity) $",
            "steps_typst": [
                f"The argument of the logarithm must be strictly positive: $x - ({h}) > 0 arrow.r.double x > {h}$.",
                f"The vertical asymptote is $x = {h}$ and the graph passes through $({h + 1}, {k})$.",
                f"Domain: $({h}, infinity)$, Range: $(-infinity, infinity)$.",
            ],
            "distractors": [
                f"$ \"VA\": x = {-h}, quad \"Domain\": ({-h}, infinity), quad \"Range\": (0, infinity) $",
                f"$ \"VA\": y = {k}, quad \"Domain\": (-infinity, infinity), quad \"Range\": ({k}, infinity) $",
                f"$ \"VA\": x = {h}, quad \"Domain\": [{h}, infinity), quad \"Range\": [{k}, infinity) $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                functions=[{"fn": _fn_log, "color": "#2563eb", "x_start": h + 0.1, "x_end": 10}],
                vertical_lines=[{"x": h, "color": "#dc2626", "dashed": True}],
                points=[(h + 1, k, f"({h+1},{k})", True)],
            ),
        }

    if "graphing trig" in t_low:
        amp = rng.choice([2, 3, 4])
        b = rng.choice([1, 2])
        d = rng.choice([-2, 0, 2])
        is_cos = rng.choice([True, False])
        fn_name = "cos" if is_cos else "sin"
        d_str = f" + {d}" if d > 0 else (f" - {abs(d)}" if d < 0 else "")
        per_str = "2 pi" if b == 1 else "pi"

        def _fn_trig(x, _a=amp, _b=b, _d=d, _c=is_cos):
            return _a * (math.cos(_b * x) if _c else math.sin(_b * x)) + _d
        return {
            "prompt_text": "Find the amplitude, period, and midline of the trigonometric function and sketch its graph.",
            "equation_typst": f"$ y = {amp} {fn_name}({'' if b == 1 else b}x){d_str} $",
            "answer_typst": f"$ \"Amplitude\" = {amp}, quad \"Period\" = {per_str}, quad \"Midline\": y = {d} $",
            "steps_typst": [
                f"The amplitude is $|A| = {amp}$.",
                f"The period is $(2 pi)/B = (2 pi)/{b} = {per_str}$.",
                f"The vertical shift gives the midline $y = {d}$.",
            ],
            "distractors": [
                f"$ \"Amplitude\" = {b}, quad \"Period\" = {amp} pi, quad \"Midline\": y = {d} $",
                f"$ \"Amplitude\" = {amp}, quad \"Period\" = 4 pi, quad \"Midline\": y = {-d} $",
                f"$ \"Amplitude\" = {2 * amp}, quad \"Period\" = {per_str}, quad \"Midline\": y = 0 $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                functions=[{"fn": _fn_trig, "color": "#2563eb"}],
                asymptotes=[{"y": d, "color": "#94a3b8"}],
            ),
        }

    if "radians and degrees" in t_low:
        is_deg_to_rad = rng.choice([True, False])
        if is_deg_to_rad:
            deg = rng.choice([15 * k for k in range(-48, 49) if k != 0] + [rng.randint(-360, 360)])
            g = math.gcd(abs(deg), 180)
            num = deg // g
            den = 180 // g
            num_str = "-" if num == -1 else ("" if num == 1 else str(num))
            rad_str = f"({num_str}pi)/({den})" if den != 1 else f"{num_str}pi"
            return {
                "prompt_text": "Convert the angle measure from degrees to radians in exact simplified form.",
                "equation_typst": f"$ {deg}^circle $",
                "answer_typst": f"$ {rad_str} $",
                "steps_typst": [
                    f"Multiply by the conversion factor $(pi \" rad\") / (180^circle)$: ${deg}^circle times pi / 180^circle$.",
                    f"Simplify fraction $({deg})/(180)$ by dividing by GCF ${g}$.",
                    f"Exact radian measure: ${rad_str}$.",
                ],
                "distractors": [f"$ ({den}pi)/({abs(num)}) $", f"$ ({num + 1}pi)/({den}) $", f"$ {deg}pi $"],
            }
        else:
            num = rng.choice([k for k in range(-12, 13) if k != 0])
            den = rng.choice([2, 3, 4, 6])
            deg = (num * 180) // den
            num_str = "-" if num == -1 else ("" if num == 1 else str(num))
            rad_expr = f"({num_str}pi)/({den})"
            return {
                "prompt_text": "Convert the angle measure from radians to degrees.",
                "equation_typst": f"$ {rad_expr} $",
                "answer_typst": f"$ {deg}^circle $",
                "steps_typst": [
                    f"Multiply by the conversion factor $180^circle / pi$: ${rad_expr} times (180^circle) / pi$.",
                    f"Cancel $pi$ and simplify: $({num} times 180^circle) / {den}$.",
                    f"Result: ${deg}^circle$.",
                ],
                "distractors": [f"$ {deg + 30}^circle $", f"$ {180 - deg}^circle $", f"$ {deg * 2}^circle $"],
            }

    if "coterminal angles" in t_low:
        ang = rng.randint(25, 330)
        pos_cot = ang + 360
        neg_cot = ang - 360
        return {
            "prompt_text": "Find one positive angle and one negative angle that are coterminal with the given angle.",
            "equation_typst": f"$ {ang}^circle $",
            "answer_typst": f"$ {pos_cot}^circle \" and \" {neg_cot}^circle $",
            "steps_typst": [
                f"Add $360^circle$ for a positive coterminal angle: ${ang}^circle + 360^circle = {pos_cot}^circle$.",
                f"Subtract $360^circle$ for a negative coterminal angle: ${ang}^circle - 360^circle = {neg_cot}^circle$.",
                f"Coterminal angles: ${pos_cot}^circle$ and ${neg_cot}^circle$.",
            ],
            "distractors": [
                f"$ {ang + 180}^circle \" and \" {ang - 180}^circle $",
                f"$ {360 - ang}^circle \" and \" {-ang}^circle $",
                f"$ {ang + 90}^circle \" and \" {ang - 90}^circle $",
            ],
        }

    if "mutually exclusive" in t_low:
        den = rng.choice([6, 8, 10, 12, 15, 16, 20, 24, 25, 30, 36, 40, 50, 52])
        num_a = rng.randint(1, den // 2)
        num_b = rng.randint(1, den - num_a - 1)
        pa = Fraction(num_a, den)
        pb = Fraction(num_b, den)
        p_union = pa + pb
        context_prompt = (
            "A card is randomly drawn from a standard deck." if den == 52 else
            (f"A fair {den}-sided die is rolled." if den in (6, 8, 12, 20) else "Events A and B are mutually exclusive.")
        )
        return {
            "prompt_text": f"{context_prompt} Find P(A or B).",
            "equation_typst": f"$ P(A) = {pa.numerator}/{pa.denominator}, quad P(B) = {pb.numerator}/{pb.denominator} $",
            "answer_typst": f"$ P(A union B) = {p_union.numerator}/{p_union.denominator} $",
            "steps_typst": [
                "Since events $A$ and $B$ are mutually exclusive, they cannot happen simultaneously ($P(A inter B) = 0$).",
                f"Apply the addition rule: $P(A union B) = P(A) + P(B) = {pa.numerator}/{pa.denominator} + {pb.numerator}/{pb.denominator}$.",
                f"Find common denominator and simplify: $P(A union B) = {p_union.numerator}/{p_union.denominator}$.",
            ],
            "distractors": [
                f"$ P(A union B) = {(pa * pb).numerator}/{(pa * pb).denominator} $",
                f"$ P(A union B) = {abs(pa - pb).numerator}/{abs(pa - pb).denominator if pa != pb else den} $",
                "$ P(A union B) = 1 $",
            ],
            "diagram_svg": svg_venn_diagram(only_a=f"{pa}", only_b=f"{pb}", both="0"),
            "answer_svg": svg_venn_diagram(only_a=f"{pa}", only_b=f"{pb}", both=f"Sum={p_union}"),
        }

    if "permutations" in t_low or "combinations" in t_low:
        is_perm = "permutation" in t_low and "combination" not in t_low
        n = rng.randint(5, 20)
        r = rng.randint(2, min(5, n - 1))
        p_val = math.perm(n, r)
        c_val = math.comb(n, r)
        if "word" in t_low or "wp" in t_low or "probability" in t_low or rng.random() < 0.4:
            if is_perm:
                scenarios = [
                    (f"How many ways can {r} officers (president, VP, secretary) be chosen from {n} members?", "order matters (different titles)"),
                    (f"In a race with {n} runners, how many ways can top {r} places be awarded?", "order matters (1st, 2nd, etc.)"),
                    (f"How many {r}-letter codes can be formed from {n} distinct letters without repetition?", "order matters in a code"),
                ]
                q_text, reason = rng.choice(scenarios)
                return {
                    "prompt_text": q_text,
                    "equation_typst": f"$ P({n}, {r}) = ({n}!)/({n - r}!) $",
                    "answer_typst": f"$ {p_val} \" ways\" $",
                    "steps_typst": [
                        f"Identify whether order matters: {reason}, so use permutations.",
                        f"Apply permutation formula: $P({n}, {r}) = {n}! / ({n} - {r})! = {n}! / {n - r}!$.",
                        f"Compute product of ${r}$ descending factors: ${p_val}$.",
                    ],
                    "distractors": [f"$ {c_val} \" ways\" $", f"$ {n * r} \" ways\" $", f"$ {p_val + n} \" ways\" $"],
                }
            else:
                scenarios = [
                    (f"A committee of {r} members is to be chosen from a group of {n} people. How many distinct committees are possible?", "order does not matter"),
                    (f"How many ways can a student select {r} books to read from a list of {n} books?", "order does not matter"),
                    (f"A pizza parlor offers {n} toppings. How many different {r}-topping pizzas can be made?", "order of toppings does not matter"),
                ]
                q_text, reason = rng.choice(scenarios)
                return {
                    "prompt_text": q_text,
                    "equation_typst": f"$ C({n}, {r}) = binom({n}, {r}) $",
                    "answer_typst": f"$ {c_val} \" ways\" $",
                    "steps_typst": [
                        f"Identify whether order matters: {reason}, so use combinations.",
                        f"Apply combination formula: $C({n}, {r}) = {n}! / ({r}!({n - r})!)$.",
                        f"Calculate: $({p_val}) / ({math.factorial(r)}) = {c_val}$.",
                    ],
                    "distractors": [f"$ {p_val} \" ways\" $", f"$ {n * r} \" ways\" $", f"$ {c_val + r} \" ways\" $"],
                }

        if is_perm:
            return {
                "prompt_text": "Evaluate the permutation P(n, r).",
                "equation_typst": f"$ P({n}, {r}) $",
                "answer_typst": f"$ {p_val} $",
                "steps_typst": [
                    f"Use the permutation formula $P(n, r) = n! / (n - r)! = {n}! / {n - r}!$.",
                    f"Multiply the first ${r}$ descending factors: ${p_val}$.",
                    f"Result: ${p_val}$.",
                ],
                "distractors": [f"$ {c_val} $", f"$ {n * r} $", f"$ {p_val + n} $"],
            }
        return {
            "prompt_text": "Evaluate the combination C(n, r).",
            "equation_typst": f"$ C({n}, {r}) = binom({n}, {r}) $",
            "answer_typst": f"$ {c_val} $",
            "steps_typst": [
                f"Use the combination formula $C(n, r) = n! / (r!(n - r)!) = {n}! / ({r}! dot {n - r}!)$.",
                f"Compute $P({n}, {r}) / {r}! = {p_val} / {math.factorial(r)}$.",
                f"Result: ${c_val}$.",
            ],
            "distractors": [f"$ {p_val} $", f"$ {n * r} $", f"$ {c_val + r} $"],
        }

    if "mathematical induction" in t_low:
        family = rng.choice(["linear", "odd", "squares", "powers2"])
        k = rng.randint(2, 8)
        if family == "linear":
            s_k = k * (k + 1) // 2
            eq_t = f"$ 1 + 2 + 3 + dots.c + n = (n(n + 1))/(2); quad \"verify at \" n = {k} \" and state \" S_(k+1) $"
            ans_t = f"$ S_({k}) = {s_k}, quad S_(k+1) = ((k + 1)(k + 2))/(2) $"
            steps_t = [
                "Base case $n = 1$: $1 = 1(2)/2 = 1$ holds true.",
                f"At $n = {k}$, the sum is ${k}({k + 1})/2 = {s_k}$.",
                "Inductive step: add $(k + 1)$ to $k(k + 1)/2$ to obtain $((k + 1)(k + 2))/2$.",
            ]
            dist_t = [
                f"$ S_({k}) = {k * k}, quad S_(k+1) = (k(k + 2))/(2) $",
                f"$ S_({k}) = {k * (k - 1) // 2}, quad S_(k+1) = ((k + 1)^2)/(2) $",
                f"$ S_({k}) = {k + 1}, quad S_(k+1) = k + 2 $",
            ]
        elif family == "odd":
            s_k = k * k
            eq_t = f"$ 1 + 3 + 5 + dots.c + (2n - 1) = n^2; quad \"verify at \" n = {k} \" and state \" S_(k+1) $"
            ans_t = f"$ S_({k}) = {s_k}, quad S_(k+1) = (k + 1)^2 $"
            steps_t = [
                "Base case $n = 1$: $2(1) - 1 = 1 = 1^2$ holds true.",
                f"At $n = {k}$, the sum is ${k}^2 = {s_k}$.",
                "Inductive step: add $2(k + 1) - 1 = 2k + 1$ to $k^2$ to obtain $(k + 1)^2$.",
            ]
            dist_t = [
                f"$ S_({k}) = {2 * k}, quad S_(k+1) = k^2 + 1 $",
                f"$ S_({k}) = {s_k - 1}, quad S_(k+1) = (k + 2)^2 $",
                f"$ S_({k}) = {k * (k + 1)}, quad S_(k+1) = 2(k + 1) $",
            ]
        elif family == "squares":
            s_k = k * (k + 1) * (2 * k + 1) // 6
            eq_t = f"$ 1^2 + 2^2 + 3^2 + dots.c + n^2 = (n(n + 1)(2n + 1))/(6); quad \"verify at \" n = {k} \" and state \" S_(k+1) $"
            ans_t = f"$ S_({k}) = {s_k}, quad S_(k+1) = ((k + 1)(k + 2)(2k + 3))/(6) $"
            steps_t = [
                "Base case $n = 1$: $1^2 = (1)(2)(3)/6 = 1$ holds true.",
                f"At $n = {k}$, the sum is ${k}({k + 1})({2 * k + 1})/6 = {s_k}$.",
                "Inductive step: add $(k + 1)^2$ to $S_k$ to obtain $((k + 1)(k + 2)(2k + 3))/6$.",
            ]
            dist_t = [
                f"$ S_({k}) = {k ** 3}, quad S_(k+1) = ((k + 1)^3)/(3) $",
                f"$ S_({k}) = {s_k + k}, quad S_(k+1) = ((k + 1)(k + 2)(2k + 1))/(6) $",
                f"$ S_({k}) = {k * (k + 1)}, quad S_(k+1) = (k + 1)^2 $",
            ]
        else:
            s_k = (2 ** k) - 1
            eq_t = f"$ 1 + 2 + 4 + dots.c + 2^(n - 1) = 2^n - 1; quad \"verify at \" n = {k} \" and state \" S_(k+1) $"
            ans_t = f"$ S_({k}) = {s_k}, quad S_(k+1) = 2^(k + 1) - 1 $"
            steps_t = [
                "Base case $n = 1$: $2^0 = 1 = 2^1 - 1$ holds true.",
                f"At $n = {k}$, the sum is $2^{k} - 1 = {s_k}$.",
                "Inductive step: add $2^k$ to $(2^k - 1)$ to obtain $2 dot 2^k - 1 = 2^(k + 1) - 1$.",
            ]
            dist_t = [
                f"$ S_({k}) = {2 * k}, quad S_(k+1) = 2^(k + 2) - 1 $",
                f"$ S_({k}) = {s_k + 1}, quad S_(k+1) = 2^k $",
                f"$ S_({k}) = {2 ** (k - 1)}, quad S_(k+1) = 2^(k + 1) $",
            ]
        return {
            "prompt_text": "State the base case (n = 1) and the inductive step target for the mathematical induction proof.",
            "equation_typst": eq_t,
            "answer_typst": ans_t,
            "steps_typst": steps_t,
            "distractors": dist_t,
        }

    # ------------------------------------------------------------------
    # 7. CALCULUS: LIMITS, DERIVATIVES, TABLES, APPLICATIONS, INTEGRALS, SLOPE FIELDS
    # ------------------------------------------------------------------
    if "rules, using tables" in t_low:
        a = rng.randint(1, 5)
        fa = rng.randint(2, 6)
        fpa = rng.choice([-4, -3, -2, -1, 2, 3, 4, 5])
        ga = rng.randint(2, 6)
        gpa = rng.choice([-4, -3, -2, -1, 2, 3, 4, 5])
        table_hdr = f"\"Given: \" f({a}) = {fa}, quad f'({a}) = {fpa}, quad g({a}) = {ga}, quad g'({a}) = {gpa}"
        if difficulty == ProblemDifficulty.MILD:
            ans_v = fpa * ga + fa * gpa
            eq = f"{table_hdr}. quad \"Find \" (d)/(d x)[f(x) g(x)] \" at \" x = {a}"
            steps = [
                f"Apply the Product Rule: $(f g)'({a}) = f'({a}) g({a}) + f({a}) g'({a})$.",
                f"Read values from the table: $({fpa})({ga}) + ({fa})({gpa})$.",
                f"Compute: ${fpa * ga} + {fa * gpa} = {ans_v}$.",
            ]
            dists = [f"$ {fpa * gpa} $", f"$ {fa * ga} $", f"$ {fpa * ga - fa * gpa} $"]
        elif difficulty == ProblemDifficulty.MEDIUM:
            num = fpa * ga - fa * gpa
            den = ga * ga
            ans_v = f"({num})/({den})"
            eq = f"{table_hdr}. quad \"Find \" (d)/(d x)[f(x) / g(x)] \" at \" x = {a}"
            steps = [
                f"Apply the Quotient Rule: $(f/g)'({a}) = (f'({a})g({a}) - f({a})g'({a})) / (g({a}))^2$.",
                f"Substitute table values: $(({fpa})({ga}) - ({fa})({gpa})) / ({ga})^2$.",
                f"Result: $({num})/({den})$.",
            ]
            dists = [f"$ ({fpa * ga + fa * gpa})/({den}) $", f"$ ({fpa})/({gpa}) $", f"$ ({fa * gpa - fpa * ga})/({den}) $"]
        else:
            ans_v = 2 * fa * fpa
            eq = f"{table_hdr}. quad \"Find \" (d)/(d x)[(f(x))^2] \" at \" x = {a}"
            steps = [
                f"Apply the Chain Rule: $[(f(x))^2]' = 2 f({a}) f'({a})$.",
                f"Substitute table values: $2({fa})({fpa}) = {ans_v}$.",
                f"Result: ${ans_v}$.",
            ]
            dists = [f"$ {fpa * fpa} $", f"$ {2 * fa} $", f"$ {fa * fpa} $"]
        tbl = svg_data_table(
            ["x", "f(x)", "f'(x)", "g(x)", "g'(x)"],
            [[str(a), str(fa), str(fpa), str(ga), str(gpa)]],
        )
        return {
            "prompt_text": "Use the given table of function and derivative values to evaluate the derivative.",
            "equation_typst": f"$ {eq} $",
            "answer_typst": f"$ {ans_v} $",
            "steps_typst": steps,
            "distractors": dists,
            "diagram_svg": tbl,
            "answer_svg": tbl,
        }

    if "jump" in t_low and "limit" in c_low or "kinks and jumps" in t_low:
        c = rng.randint(-2, 3)
        l_val = rng.randint(-4, 1)
        r_val = rng.randint(2, 6)
        return {
            "prompt_text": "Evaluate the left-hand limit, right-hand limit, and two-sided limit at the jump discontinuity.",
            "equation_typst": f"$ f(x) = cases(x + {l_val - c} & \"if \" x < {c}, -x + {r_val + c} & \"if \" x >= {c}); quad lim_(x arrow.r {c}) f(x) $",
            "answer_typst": f"$ lim_(x arrow.r {c}^-) f(x) = {l_val}, quad lim_(x arrow.r {c}^+) f(x) = {r_val}, quad \"Limit DNE\" $",
            "steps_typst": [
                f"Left-hand limit: $lim_(x arrow.r {c}^-) (x + {l_val - c}) = {l_val}$.",
                f"Right-hand limit: $lim_(x arrow.r {c}^+) (-x + {r_val + c}) = {r_val}$.",
                f"Since ${l_val} != {r_val}$, the two-sided limit does not exist (DNE).",
            ],
            "distractors": [
                f"$ lim_(x arrow.r {c}) f(x) = {l_val} $",
                f"$ lim_(x arrow.r {c}) f(x) = {r_val} $",
                f"$ lim_(x arrow.r {c}) f(x) = {(l_val + r_val) / 2:g} $",
            ],
            "diagram_svg": svg_coordinate_plane(
                functions=[
                    {"fn": lambda x, _c=c, _l=l_val: x + _l - _c, "x_start": -10, "x_end": c, "color": "#2563eb"},
                    {"fn": lambda x, _c=c, _r=r_val: -x + _r + _c, "x_start": c, "x_end": 10, "color": "#dc2626"},
                ],
                points=[(c, l_val, "", False), (c, r_val, "", True)],
            ),
            "answer_svg": svg_coordinate_plane(
                functions=[
                    {"fn": lambda x, _c=c, _l=l_val: x + _l - _c, "x_start": -10, "x_end": c, "color": "#2563eb"},
                    {"fn": lambda x, _c=c, _r=r_val: -x + _r + _c, "x_start": c, "x_end": 10, "color": "#dc2626"},
                ],
                points=[(c, l_val, f"L={l_val}", False), (c, r_val, f"R={r_val}", True)],
            ),
        }

    if "rolle's theorem" in t_low or ("mean value theorem" in t_low and "integration" not in c_low):
        r1 = rng.randint(-4, 0)
        r2 = r1 + rng.choice([2, 4, 6])
        c_val = (r1 + r2) // 2
        b = -(r1 + r2)
        c_const = r1 * r2
        b_str = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
        c_str = f"+ {c_const}" if c_const > 0 else (f"- {abs(c_const)}" if c_const < 0 else "")
        b_deriv = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
        return {
            "prompt_text": "Find the value c in the open interval (a, b) that satisfies Rolle's Theorem / the Mean Value Theorem.",
            "equation_typst": f"$ f(x) = x^2 {b_str} {c_str} quad \"on\" [{r1}, {r2}] $",
            "answer_typst": f"$ c = {c_val} $",
            "steps_typst": [
                f"Compute the average rate of change on $[{r1}, {r2}]$: $(f({r2}) - f({r1}))/({r2} - ({r1})) = 0$.",
                f"Differentiate: $f'(x) = 2x {b_deriv}$.",
                f"Solve $f'(c) = 0$: $2c = {-b} ==> c = {c_val}$.",
            ],
            "distractors": [f"$ c = {-c_val} $", f"$ c = {r2} $", f"$ c = {c_val + 1} $"],
        }

    if "related rates" in t_low:
        r_val = rng.randint(3, 8)
        dr_dt = rng.randint(2, 5)
        da_dt = 2 * r_val * dr_dt
        return {
            "prompt_text": "Solve the related rates problem by differentiating implicitly with respect to time t.",
            "equation_typst": f"\"The radius of a circle increases at \" (d r)/(d t) = {dr_dt} \" cm/s. Find \" (d A)/(d t) \" when \" r = {r_val} \" cm.\"",
            "answer_typst": f"$ (d A)/(d t) = {da_dt} pi \" cm\"^2\"/s\" $",
            "steps_typst": [
                "Start with the area of a circle: $A = pi r^2$.",
                "Differentiate both sides with respect to $t$: $(d A)/(d t) = 2 pi r (d r)/(d t)$.",
                f"Substitute $r = {r_val}$ and $(d r)/(d t) = {dr_dt}$: $(d A)/(d t) = 2 pi ({r_val})({dr_dt}) = {da_dt} pi$.",
            ],
            "distractors": [
                f"$ (d A)/(d t) = {r_val * r_val * dr_dt} pi \" cm\"^2\"/s\" $",
                f"$ (d A)/(d t) = {2 * r_val} pi \" cm\"^2\"/s\" $",
                f"$ (d A)/(d t) = {da_dt // 2} pi \" cm\"^2\"/s\" $",
            ],
        }

    if "newton's method" in t_low:
        x0 = rng.randint(2, 12)
        diff_n = rng.choice([-3, -2, -1, 1, 2, 3, 5])
        n = x0 * x0 + diff_n
        fx0 = x0 * x0 - n
        fpx0 = 2 * x0
        x1_f = Fraction(x0) - Fraction(fx0, fpx0)
        return {
            "prompt_text": "Perform one iteration of Newton's Method to approximate a zero of f(x) starting from x_0.",
            "equation_typst": f"$ f(x) = x^2 - {n}, quad x_0 = {x0} $",
            "answer_typst": f"$ x_1 = {x1_f.numerator}/{x1_f.denominator} approx {float(x1_f):.4f} $",
            "steps_typst": [
                f"Compute $f(x_0) = ({x0})^2 - {n} = {fx0}$ and $f'(x_0) = 2({x0}) = {fpx0}$.",
                f"Apply Newton's Method formula: $x_1 = x_0 - f(x_0)/f'(x_0) = {x0} - ({fx0})/({fpx0})$.",
                f"Simplify: $x_1 = {x1_f.numerator}/{x1_f.denominator}$.",
            ],
            "distractors": [
                f"$ x_1 = {(Fraction(x0) + Fraction(fx0, fpx0)).numerator}/{(Fraction(x0) + Fraction(fx0, fpx0)).denominator} $",
                f"$ x_1 = {x0 - fx0} $",
                f"$ x_1 = {fpx0}/{fx0} $",
            ],
        }

    if "curve sketching" in t_low or "graphical comparison of f" in t_low:
        a = rng.choice([-3, -2, -1, 1, 2, 3])
        k = rng.randint(1, 12)
        c_shift = rng.randint(-15, 15)
        k2 = k * k
        c3 = 3 * k2
        f_expr = f"{'' if a == 1 else ('-' if a == -1 else a)}(x^3 - {c3}x)" + (f" {'+' if c_shift > 0 else '-'} {abs(c_shift)}" if c_shift != 0 else "")

        def fn_f(x, _a=a, _k=k, _c=c_shift):
            return _a * (0.15 * (x ** 3) - 0.45 * (_k ** 2) * x) + _c * 0.1

        def fn_fp(x, _a=a, _k=k):
            return _a * (0.45 * (x ** 2) - 0.45 * (_k ** 2))

        return {
            "prompt_text": "Find the critical points, inflection point, and sketch f(x) and f'(x).",
            "equation_typst": f"$ f(x) = {f_expr} $",
            "answer_typst": f"$ \"Critical points\": x = plus.minus {k}, quad \"Inflection point\": (0, {c_shift}) $",
            "steps_typst": [
                f"Compute $f'(x) = {3 * a}(x^2 - {k2}) = 0 ==> x = plus.minus {k}$.",
                f"Compute $f''(x) = {6 * a}x = 0 ==> x = 0$, giving inflection point at $(0, {c_shift})$.",
                f"Evaluate local extrema at $x = -{k}$ and $x = {k}$.",
            ],
            "distractors": [
                f"$ \"Critical points\": x = 0, plus.minus {k}, quad \"Inflection point\": (1, {c_shift}) $",
                f"$ \"Critical points\": x = plus.minus {k + 1}, quad \"Inflection point\": (0, 0) $",
                f"$ \"Critical points\": x = 0, quad \"Inflection point\": (plus.minus {k}, 0) $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                functions=[
                    {"fn": fn_f, "color": "#2563eb"},
                    {"fn": fn_fp, "color": "#dc2626", "dashed": True},
                ],
                points=[(-k, fn_f(-k), f"x=-{k}", True), (k, fn_f(k), f"x={k}", True), (0, c_shift * 0.1, "IP", True)],
            ),
        }

    if "integration by parts" in t_low:
        ibp_type = rng.choice(["x_exp", "x_sin", "x_cos", "x_n_ln", "x_sec2"])
        c_mult = rng.choice([1, 2, 3, 4, 5])
        k = rng.choice([k for k in range(-8, 9) if k != 0])
        kx = "x" if k == 1 else (f"-x" if k == -1 else f"{k}x")
        if ibp_type == "x_sec2":
            return {
                "prompt_text": "Evaluate the indefinite integral using integration by parts.",
                "equation_typst": f"$ integral {c_mult}x sec^2({kx}) d x $",
                "answer_typst": f"$ ({c_mult}x)/({k}) tan({kx}) - ({c_mult})/({k * k}) ln|sec({kx})| + C $",
                "steps_typst": [
                    f"Choose $u = {c_mult}x$ ($d u = {c_mult} d x$) and $d v = sec^2({kx}) d x$ ($v = (1/{k}) tan({kx})$).",
                    f"Apply formula: $({c_mult}x/{k}) tan({kx}) - integral ({c_mult}/{k}) tan({kx}) d x$.",
                    f"Integrate: $({c_mult}x/{k}) tan({kx}) - ({c_mult}/{k * k}) ln|sec({kx})| + C$.",
                ],
                "distractors": [
                    f"$ ({c_mult}x)/({k}) tan({kx}) + ({c_mult})/({k * k}) ln|sec({kx})| + C $",
                    f"$ ({c_mult}x^2)/2 sec^2({kx}) + C $",
                    f"$ {c_mult} tan({kx}) + C $",
                ],
            }
        elif ibp_type == "x_n_ln":
            n_pow = rng.randint(1, 6)
            return {
                "prompt_text": "Evaluate the indefinite integral using integration by parts.",
                "equation_typst": f"$ integral x^{n_pow} ln(x) d x $" if n_pow > 1 else "$ integral x ln(x) d x $",
                "answer_typst": f"$ (x^({n_pow + 1}))/({n_pow + 1}) ln(x) - (x^({n_pow + 1}))/({(n_pow + 1) ** 2}) + C $",
                "steps_typst": [
                    f"Choose $u = ln(x)$ ($d u = (1/x) d x$) and $d v = x^{n_pow} d x$ ($v = (x^{n_pow + 1})/({n_pow + 1})$).",
                    f"Apply $integral u d v = u v - integral v d u$: $(x^{n_pow + 1}/{n_pow + 1}) ln(x) - integral (x^{n_pow})/({n_pow + 1}) d x$.",
                    f"Evaluate: $(x^({n_pow + 1}))/({n_pow + 1}) ln(x) - (x^({n_pow + 1}))/({(n_pow + 1) ** 2}) + C$.",
                ],
                "distractors": [
                    f"$ (x^({n_pow + 1}))/({n_pow + 1}) ln(x) + C $",
                    f"$ (x^({n_pow}))/({n_pow}) ln(x) - x + C $",
                    f"$ (ln(x))^2 / 2 + C $",
                ],
            }
        elif ibp_type == "x_sin":
            return {
                "prompt_text": "Evaluate the indefinite integral using integration by parts.",
                "equation_typst": f"$ integral {c_mult}x sin({kx}) d x $",
                "answer_typst": f"$ -({c_mult}x)/({k}) cos({kx}) + ({c_mult})/({k * k}) sin({kx}) + C $",
                "steps_typst": [
                    f"Choose $u = {c_mult}x$ ($d u = {c_mult} d x$) and $d v = sin({kx}) d x$ ($v = -(1/{k}) cos({kx})$).",
                    f"Apply formula: $-({c_mult}x/{k}) cos({kx}) - integral -({c_mult}/{k}) cos({kx}) d x$.",
                    f"Evaluate: $-({c_mult}x/{k}) cos({kx}) + ({c_mult}/{k * k}) sin({kx}) + C$.",
                ],
                "distractors": [
                    f"$ ({c_mult}x)/({k}) cos({kx}) - ({c_mult})/({k * k}) sin({kx}) + C $",
                    f"$ -({c_mult}x^2)/2 cos({kx}) + C $",
                    f"$ -{c_mult}x sin({kx}) + cos({kx}) + C $",
                ],
            }
        elif ibp_type == "x_cos":
            return {
                "prompt_text": "Evaluate the indefinite integral using integration by parts.",
                "equation_typst": f"$ integral {c_mult}x cos({kx}) d x $",
                "answer_typst": f"$ ({c_mult}x)/({k}) sin({kx}) + ({c_mult})/({k * k}) cos({kx}) + C $",
                "steps_typst": [
                    f"Choose $u = {c_mult}x$ ($d u = {c_mult} d x$) and $d v = cos({kx}) d x$ ($v = (1/{k}) sin({kx})$).",
                    f"Apply formula: $({c_mult}x/{k}) sin({kx}) - integral ({c_mult}/{k}) sin({kx}) d x$.",
                    f"Evaluate: $({c_mult}x/{k}) sin({kx}) + ({c_mult}/{k * k}) cos({kx}) + C$.",
                ],
                "distractors": [
                    f"$ -({c_mult}x)/({k}) sin({kx}) + ({c_mult})/({k * k}) cos({kx}) + C $",
                    f"$ ({c_mult}x^2)/2 sin({kx}) + C $",
                    f"$ {c_mult}x cos({kx}) - sin({kx}) + C $",
                ],
            }
        else:
            return {
                "prompt_text": "Evaluate the indefinite integral using integration by parts.",
                "equation_typst": f"$ integral {c_mult}x e^({kx}) d x $",
                "answer_typst": f"$ ({c_mult}x)/({k}) e^({kx}) - ({c_mult})/({k * k}) e^({kx}) + C $",
                "steps_typst": [
                    f"Choose $u = {c_mult}x$ ($d u = {c_mult} d x$) and $d v = e^({kx}) d x$ ($v = (1/{k}) e^({kx})$).",
                    f"Apply $integral u d v = u v - integral v d u$: $({c_mult}x/{k})e^({kx}) - integral ({c_mult}/{k})e^({kx}) d x$.",
                    f"Integrate: $({c_mult}x/{k})e^({kx}) - ({c_mult}/{k * k})e^({kx}) + C$.",
                ],
                "distractors": [
                    f"$ ({c_mult}x)/({k}) e^({kx}) + ({c_mult})/({k * k}) e^({kx}) + C $",
                    f"$ ({c_mult}x^2)/(2) e^({kx}) + C $",
                    f"$ {k} x e^({kx}) - e^({kx}) + C $",
                ],
            }

    if "area between curves" in t_low or "area under a curve" in t_low:
        variant = rng.choice(["parabola_axis", "line_parabola", "shifted_line_parabola", "cubic_axis", "parabola_const"])
        if variant == "parabola_axis":
            b = rng.randint(2, 6)
            a = rng.choice([1, 2])
            b2 = b * b
            c = a * b2
            area_f = Fraction(4 * a * (b ** 3), 3)
            quad_s = f"{c} - x^2" if a == 1 else f"{c} - {a}x^2"

            def fn_top_math(x, _c=c, _a=a):
                return (_c - _a * x * x) * (6.0 / max(c, 1))

            def fn_bot_math(x):
                return 0.0

            x_a, x_b = -b, b
            eq_s = f"$ y = {quad_s} \" and \" y = 0 \" on \" [-{b}, {b}] $"
            steps = [
                f"Set up the integral: $A = integral_(-{b})^{b} ({quad_s}) d x$.",
                f"Find the antiderivative: $[{c}x - ({a}x^3)/3]_(-{b})^{b}$.",
                f"Evaluate: $2({c * b} - ({a * (b ** 3)})/3) = {area_f.numerator}/{area_f.denominator}$.",
            ]
        elif variant == "line_parabola":
            m = rng.randint(2, 7)
            area_f = Fraction(m ** 3, 6)

            def fn_top_math(x, _m=m):
                return _m * x * (6.0 / (_m * _m))

            def fn_bot_math(x, _m=m):
                return (x * x) * (6.0 / (_m * _m))

            x_a, x_b = 0, m
            eq_s = f"$ y = {m}x \" and \" y = x^2 \" on \" [0, {m}] $"
            steps = [
                f"Set up the integral: $A = integral_0^{m} ({m}x - x^2) d x$.",
                f"Find the antiderivative: $[({m}x^2)/2 - x^3/3]_0^{m}$.",
                f"Evaluate: $({m ** 3})/2 - ({m ** 3})/3 = {area_f.numerator}/{area_f.denominator}$.",
            ]
        elif variant == "shifted_line_parabola":
            r1 = rng.choice([-3, -2, -1])
            diff = rng.randint(2, 5)
            r2 = r1 + diff
            area_f = Fraction(diff ** 3, 6)
            m_l = r1 + r2
            c_l = - (r1 * r2)
            m_str = f"{m_l}x" if m_l != 0 else ""
            c_str = f"+ {c_l}" if c_l > 0 else (f"- {abs(c_l)}" if c_l < 0 else "")
            line_expr = f"{m_str} {c_str}".strip() or "0"

            def fn_top_math(x, _m=m_l, _c=c_l):
                return _m * x + _c

            def fn_bot_math(x):
                return x * x

            x_a, x_b = r1, r2
            eq_s = f"$ y = {line_expr} \" and \" y = x^2 \" on \" [{r1}, {r2}] $"
            steps = [
                f"Find intersection points: $x^2 = {line_expr} ==> x = {r1}, x = {r2}$.",
                f"Set up integral: $A = integral_({r1})^{r2} [({line_expr}) - x^2] d x$.",
                f"Evaluate between limits: $A = {area_f.numerator}/{area_f.denominator}$.",
            ]
        elif variant == "cubic_axis":
            k = rng.randint(2, 5)
            k2 = k * k
            area_f = Fraction(k ** 4, 4)

            def fn_top_math(x, _k2=k2):
                return (_k2 * x - x ** 3) * (6.0 / (_k2 * 1.5))

            def fn_bot_math(x):
                return 0.0

            x_a, x_b = 0, k
            eq_s = f"$ y = {k2}x - x^3 \" and \" y = 0 \" on \" [0, {k}] $"
            steps = [
                f"Set up the integral: $A = integral_0^{k} ({k2}x - x^3) d x$.",
                f"Find the antiderivative: $[({k2}x^2)/2 - x^4/4]_0^{k}$.",
                f"Evaluate: $({k ** 4})/2 - ({k ** 4})/4 = {area_f.numerator}/{area_f.denominator}$.",
            ]
        else:  # parabola_const
            k = rng.randint(2, 5)
            c = rng.randint(-3, 3)
            c_top = c + k * k
            area_f = Fraction(4 * (k ** 3), 3)

            def fn_top_math(x, _ct=c_top):
                return (_ct - x * x)

            def fn_bot_math(x, _c=c):
                return float(_c)

            x_a, x_b = -k, k
            eq_s = f"$ y = {c_top} - x^2 \" and \" y = {c} \" on \" [-{k}, {k}] $"
            steps = [
                f"Set up integral: $A = integral_(-{k})^{k} [({c_top} - x^2) - ({c})] d x = integral_(-{k})^{k} ({k * k} - x^2) d x$.",
                f"Find the antiderivative: $[{k * k}x - x^3/3]_(-{k})^{k}$.",
                f"Evaluate: $2({k ** 3} - ({k ** 3})/3) = {area_f.numerator}/{area_f.denominator}$.",
            ]

        d1 = f"$ A = {area_f.numerator + 2}/{area_f.denominator} $"
        d2 = f"$ A = {(area_f * 2).numerator}/{(area_f * 2).denominator} $"
        d3 = f"$ A = {(area_f / 2).numerator}/{(area_f / 2).denominator} $"
        ans_s = f"$ A = {area_f.numerator}/{area_f.denominator} $" if area_f.denominator != 1 else f"$ A = {area_f.numerator} $"

        return {
            "prompt_text": "Set up and evaluate the definite integral for the shaded area under/between the curves.",
            "equation_typst": eq_s,
            "answer_typst": ans_s,
            "steps_typst": steps,
            "distractors": [d1, d2, d3],
            "diagram_svg": svg_coordinate_plane(
                shaded_between={"fn_top": fn_top_math, "fn_bot": fn_bot_math, "a": x_a, "b": x_b, "color": "#3b82f6"},
                functions=[{"fn": fn_top_math, "color": "#1d4ed8"}, {"fn": fn_bot_math, "color": "#64748b"}],
            ),
            "answer_svg": svg_coordinate_plane(
                shaded_between={"fn_top": fn_top_math, "fn_bot": fn_bot_math, "a": x_a, "b": x_b, "color": "#22c55e"},
                functions=[{"fn": fn_top_math, "color": "#15803d"}, {"fn": fn_bot_math, "color": "#64748b"}],
            ),
        }

    if "volume by" in t_low or "volume of solids" in t_low:
        v_type = rng.choice(["disk_linear", "disk_sqrt", "disk_quad", "shell_quad", "cross_square"])
        if v_type == "disk_linear":
            m = rng.randint(1, 3)
            b = rng.randint(2, 6)
            vol = Fraction(m * m * (b ** 3), 3)
            line_s = f"{m}x" if m > 1 else "x"
            eq_s = f"$ y = {line_s}, quad y = 0, quad x = {b} quad (\"about the \" x\"-axis\") $"
            steps = [
                f"Use the Disk Method: $V = pi integral_0^{b} [R(x)]^2 d x = pi integral_0^{b} ({m * m}x^2) d x$.",
                f"Find the antiderivative: $pi [({m * m}x^3) / 3]_0^{b}$.",
                f"Evaluate at the limits: $V = ({m * m * (b ** 3)})/(3) pi = {vol.numerator}/{vol.denominator} pi$.",
            ]
        elif v_type == "disk_sqrt":
            k = rng.choice([1, 2, 3])
            b = rng.randint(2, 8)
            vol = Fraction(k * (b ** 2), 2)
            rad_s = f"sqrt({k}x)" if k > 1 else "sqrt(x)"
            eq_s = f"$ y = {rad_s}, quad y = 0, quad x = {b} quad (\"about the \" x\"-axis\") $"
            steps = [
                f"Use the Disk Method: $V = pi integral_0^{b} [sqrt({k}x)]^2 d x = pi integral_0^{b} ({k}x) d x$.",
                f"Find the antiderivative: $pi [({k}x^2)/2]_0^{b}$.",
                f"Evaluate: $V = ({k * (b ** 2)})/(2) pi = {vol.numerator}/{vol.denominator} pi$.",
            ]
        elif v_type == "disk_quad":
            b = rng.randint(1, 3)
            vol = Fraction(b ** 5, 5)
            eq_s = f"$ y = x^2, quad y = 0, quad x = {b} quad (\"about the \" x\"-axis\") $"
            steps = [
                f"Use the Disk Method: $V = pi integral_0^{b} [x^2]^2 d x = pi integral_0^{b} x^4 d x$.",
                f"Find the antiderivative: $pi [x^5 / 5]_0^{b}$.",
                f"Evaluate: $V = ({b ** 5})/(5) pi$.",
            ]
        elif v_type == "shell_quad":
            b = rng.randint(2, 5)
            vol = Fraction(b ** 4, 2)
            eq_s = f"$ y = x^2, quad y = 0, quad x = {b} quad (\"about the \" y\"-axis using cylindrical shells\") $"
            steps = [
                f"Use Cylindrical Shells: $V = 2 pi integral_0^{b} x(x^2) d x = 2 pi integral_0^{b} x^3 d x$.",
                f"Find antiderivative: $2 pi [x^4 / 4]_0^{b} = pi [x^4 / 2]_0^{b}$.",
                f"Evaluate: $V = ({b ** 4})/(2) pi$.",
            ]
        else:  # cross_square
            b = rng.randint(2, 5)
            b2 = b * b
            vol = Fraction(16 * (b ** 5), 15)
            eq_s = f"$ \"Base: \" y = {b2} - x^2, y = 0; quad \"Cross-sections: squares \" perp x\"-axis\" $"
            steps = [
                f"Cross-section area at $x$ is $A(x) = [s(x)]^2 = ({b2} - x^2)^2 = {b2 * b2} - {2 * b2}x^2 + x^4$.",
                f"Integrate from $-{b}$ to ${b}$: $V = integral_(-{b})^{b} ({b2 * b2} - {2 * b2}x^2 + x^4) d x$.",
                f"Evaluate: $V = {vol.numerator}/{vol.denominator}$.",
            ]

        v_ans = f"$ V = ({vol.numerator})/({vol.denominator}) pi $" if vol.denominator != 1 and "squares" not in eq_s else (
            f"$ V = {vol.numerator} pi $" if "squares" not in eq_s else f"$ V = {vol.numerator}/{vol.denominator} $"
        )
        return {
            "prompt_text": "Find the volume of the solid generated by revolving the region or by known cross-sections.",
            "equation_typst": eq_s,
            "answer_typst": v_ans,
            "steps_typst": steps,
            "distractors": [
                f"$ V = {vol.numerator + 4} pi $" if "pi" in v_ans else f"$ V = {vol.numerator + 4} $",
                f"$ V = {(vol / 2).numerator}/{(vol / 2).denominator} pi $" if "pi" in v_ans else f"$ V = {(vol / 2).numerator} $",
                f"$ V = {2 * vol.numerator} pi $" if "pi" in v_ans else f"$ V = {2 * vol.numerator} $",
            ],
        }

    if "slope fields" in t_low:
        a = rng.choice([-3, -2, -1, 1, 2, 3])
        b = rng.choice([-3, -2, -1, 1, 2, 3])
        sf_case = rng.choice(["linear_x", "linear_y", "sum_xy", "circle_field"])
        if sf_case == "linear_x":
            eq_typst = f"$ (d y)/(d x) = {'' if a == 1 else ('-' if a == -1 else a)}x $"
            ans_typst = f"$ y = ({a})/(2) x^2 + C; quad \"Slopes depend only on \" x $"
            steps = [
                f"At each grid point $(x, y)$, slope segment $m = {a}x$.",
                "Slopes are zero along $x = 0$ (the y-axis) and invariant under vertical translations.",
                f"Antiderivative family of parabolas: $y = ({a})/2 x^2 + C$.",
            ]
            fn_sf = lambda x, y, _a=a: (_a * x) / 3.0
            fn_sol = lambda x, _a=a: (_a * x * x) / 6.0
        elif sf_case == "linear_y":
            eq_typst = f"$ (d y)/(d x) = {'' if b == 1 else ('-' if b == -1 else b)}y $"
            ans_typst = f"$ y = C e^({b}x); quad \"Slopes depend only on \" y $"
            steps = [
                f"At each grid point $(x, y)$, slope $m = {b}y$.",
                "Slopes are zero along $y = 0$ (the x-axis) and invariant under horizontal translations.",
                f"General solution is exponential: $y = C e^({b}x)$.",
            ]
            fn_sf = lambda x, y, _b=b: (_b * y) / 3.0
            fn_sol = lambda x, _b=b: 0.5 * math.exp(_b * x * 0.4) if abs(_b * x * 0.4) < 4 else float('nan')
        elif sf_case == "circle_field":
            eq_typst = "$ (d y)/(d x) = -x / y $"
            ans_typst = "$ x^2 + y^2 = C; quad \"Concentric circular trajectories\" $"
            steps = [
                "At each $(x, y)$, the slope $m = -x/y$ is orthogonal to the radius vector.",
                "Separating variables: $y d y = -x d x ==> x^2 + y^2 = C$.",
                "Field forms concentric circles centered at origin.",
            ]
            fn_sf = lambda x, y: -x / y if abs(y) > 0.3 else 10.0
            fn_sol = lambda x: math.sqrt(max(0.0, 16.0 - x * x))
        else:
            eq_typst = f"$ (d y)/(d x) = {a}x {'+' if b >= 0 else '-'} {abs(b)}y $"
            ans_typst = f"$ \"Slopes depend on both \" x \" and \" y $"
            steps = [
                f"Evaluate slope at sample coordinates: $m = {a}x {'+' if b >= 0 else '-'} {abs(b)}y$.",
                f"Isoclines occur along straight lines where ${a}x {'+' if b >= 0 else '-'} {abs(b)}y = c$.",
                "Sketch directional field segments at each lattice point.",
            ]
            fn_sf = lambda x, y, _a=a, _b=b: (_a * x + _b * y) / 4.0
            fn_sol = lambda x, _a=a: _a * x * 0.3

        return {
            "prompt_text": "Match the differential equation with its slope field and identify key solution curve features.",
            "equation_typst": eq_typst,
            "answer_typst": ans_typst,
            "steps_typst": steps,
            "distractors": [
                "$ (d y)/(d x) = x^2 + y^2 $",
                "$ y = sin(x) + C $",
                "$ (d y)/(d x) = 0 $",
            ],
            "diagram_svg": svg_coordinate_plane(slope_field=fn_sf),
            "answer_svg": svg_coordinate_plane(slope_field=fn_sf, functions=[{"fn": fn_sol, "color": "#dc2626"}]),
        }
