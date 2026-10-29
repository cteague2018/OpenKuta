from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Type

from backend.app.core.base import (
    BaseGenerator,
    BaseProblem,
    GeneratorConfig,
    ProblemDifficulty,
)
from backend.app.core.svg_utils import (
    svg_angle_diagram,
    svg_circle_diagram,
    svg_coordinate_plane,
    svg_general_triangle,
    svg_number_line,
    svg_polygon_diagram,
    svg_right_triangle,
    svg_solid_3d,
)
from backend.app.generators.topic_generators_adv import gen_adv_problem
from backend.app.generators.topic_generators_alg_geo import (
    _fmt_frac,
    gen_alg_geo_problem,
)
from backend.app.generators.verification_gate import verify_mathematical_truth


def _gen_decoupled_subtopic(
    topic_id: str,
    topic_name: str,
    category_name: str,
    course_key: str,
    difficulty: ProblemDifficulty,
    rng: random.Random,
    fallback_gen_id: str,
) -> Optional[Dict[str, Any]]:
    """Ensure subtopics that previously multiplexed across MILD/MEDIUM/SPICY
    always generate problems strictly for their selected subtopic at ALL difficulties.
    """
    t_low = topic_name.lower()
    c_low = category_name.lower()
    scale = 1 if difficulty == ProblemDifficulty.MILD else (2 if difficulty == ProblemDifficulty.MEDIUM else 3)
    a: Any
    b: Any
    c: Any
    d: Any
    f: Any
    k: Any
    m: Any
    n: Any
    p: Any
    r: Any
    s: Any
    t: Any
    x: Any
    y: Any
    ans: Any
    val: Any
    sol: Any
    area: Any
    tot: Any
    rhs: Any
    dx: Any

    # ------------------------------------------------------------------
    # A. CALCULUS DIFFERENTIATION SUBTOPICS
    # ------------------------------------------------------------------
    if "differentiation" in c_low or "introduction to calculus" in c_low:
        if "average rates of change" in t_low or ("functions" in c_low and "average rates" in t_low):
            a = rng.randint(1, 2 * scale)
            b = a + rng.randint(1, 3)
            c_coef = rng.randint(1, 2 * scale)
            fa = c_coef * a * a
            fb = c_coef * b * b
            aroc = (fb - fa) // (b - a)
            return {
                "prompt_text": "Find the average rate of change of the function over the given interval.",
                "equation_typst": f"$ f(x) = {'' if c_coef == 1 else c_coef}x^2 quad \"on\" [{a}, {b}] $",
                "answer_typst": f"$ {aroc} $",
                "steps_typst": [
                    f"Evaluate at the endpoints: $f({a}) = {fa}$ and $f({b}) = {fb}$.",
                    f"Use $(f(b) - f(a))/(b - a) = ({fb} - {fa})/({b} - {a})$.",
                    f"Simplify: ${aroc}$.",
                ],
                "distractors": [f"$ {fb - fa} $", f"$ {aroc + c_coef} $", f"$ {2 * c_coef * a} $"],
            }
        if "definition of the derivative" in t_low or "limits in form of definition" in t_low:
            a = rng.randint(1, 3 * scale)
            b = rng.randint(1, 5)
            return {
                "prompt_text": "Use the limit definition of the derivative f'(x) = lim_(h->0) (f(x+h) - f(x))/h to find f'(x).",
                "equation_typst": f"$ f(x) = {a}x^2 + {b}x $",
                "answer_typst": f"$ f'(x) = {2 * a}x + {b} $",
                "steps_typst": [
                    f"Set up $lim_(h arrow.r 0) ({a}(x + h)^2 + {b}(x + h) - ({a}x^2 + {b}x)) / h$.",
                    f"Expand and cancel terms without $h$: $lim_(h arrow.r 0) ({2 * a}x h + {a}h^2 + {b}h) / h$.",
                    f"Factor out $h$ and take the limit as $h arrow.r 0$: $f'(x) = {2 * a}x + {b}$.",
                ],
                "distractors": [
                    f"$ f'(x) = {a}x + {b} $",
                    f"$ f'(x) = {2 * a}x^2 + {b} $",
                    f"$ f'(x) = {2 * a}x $",
                ],
            }
        if "instantaneous rates of change" in t_low:
            a = rng.randint(1, 3 * scale)
            x0 = rng.randint(1, 4)
            rate = 2 * a * x0
            return {
                "prompt_text": "Find the instantaneous rate of change of f(x) at the given value x = a.",
                "equation_typst": f"$ f(x) = {a}x^2 + {rng.randint(1, 6)}, quad x = {x0} $",
                "answer_typst": f"$ f'({x0}) = {rate} $",
                "steps_typst": [
                    f"Differentiate $f(x)$ to get the instantaneous rate function: $f'(x) = {2 * a}x$.",
                    f"Substitute $x = {x0}$: $f'({x0}) = {2 * a}({x0}) = {rate}$.",
                    f"Instantaneous rate of change: ${rate}$.",
                ],
                "distractors": [f"$ {a * x0 * x0} $", f"$ {2 * a} $", f"$ {rate + a} $"],
            }
        if "power rule" in t_low and "substitution" not in t_low:
            n1 = rng.randint(2, 2 + scale)
            c1 = rng.randint(2, 5)
            c2 = rng.randint(2, 6)
            return {
                "prompt_text": "Differentiate the function with respect to x using the Power Rule.",
                "equation_typst": f"$ f(x) = {c1}x^{n1} - {c2}x $",
                "answer_typst": f"$ f'(x) = {c1 * n1}x^{n1 - 1} - {c2} $" if n1 > 2 else f"$ f'(x) = {c1 * n1}x - {c2} $",
                "steps_typst": [
                    "Apply the Power Rule $d/(d x)[x^n] = n x^(n-1)$ to each term.",
                    f"Differentiate ${c1}x^{n1} arrow.r {c1 * n1}x^{n1 - 1}$ and $-{c2}x arrow.r -{c2}$.",
                    "Combine terms for $f'(x)$.",
                ],
                "distractors": [
                    f"$ f'(x) = {c1}x^{n1 - 1} - {c2} $",
                    f"$ f'(x) = {c1 * n1}x^{n1} - {c2} $",
                    f"$ f'(x) = {c1 * (n1 + 1)}x^{n1} $",
                ],
            }
        if "higher order" in t_low:
            c = rng.randint(1, 3 * scale)
            n = rng.choice([3, 4])
            c1 = c * n
            c2 = c1 * (n - 1)
            return {
                "prompt_text": "Find the second derivative f''(x) of the given function.",
                "equation_typst": f"$ f(x) = {c}x^{n} + {rng.randint(2, 5)}x $",
                "answer_typst": f"$ f''(x) = {c2}x^{n - 2} $" if n > 3 else f"$ f''(x) = {c2}x $",
                "steps_typst": [
                    f"Differentiate once to find the first derivative: $f'(x) = {c1}x^{n - 1} + ...$.",
                    f"Differentiate $f'(x)$ a second time using the Power Rule: $f''(x) = {c2}x^{n - 2}$.",
                    f"Second derivative: $f''(x) = {c2}{'x' if n == 3 else f'x^{n-2}'}$.",
                ],
                "distractors": [
                    f"$ f''(x) = {c1}x^{n - 1} $",
                    f"$ f''(x) = {c2 * (n - 2)} $",
                    f"$ f''(x) = {c}x^{n - 2} $",
                ],
            }
        if "product rule" in t_low:
            a = rng.randint(1, 3 * scale)
            b = rng.randint(1, 5)
            return {
                "prompt_text": "Differentiate the function using the Product Rule.",
                "equation_typst": f"$ f(x) = x^{scale} e^({a}x + {b}) $",
                "answer_typst": f"$ f'(x) = x^{scale - 1} e^({a}x + {b}) ({scale} + {a}x) $" if scale > 1 else f"$ f'(x) = e^({a}x + {b})(1 + {a}x) $",
                "steps_typst": [
                    f"Let $u = x^{scale}$ and $v = e^({a}x + {b})$.",
                    f"Compute $u' = {scale}x^{scale - 1}$ and $v' = {a}e^({a}x + {b})$.",
                    "Apply the Product Rule $f'(x) = u'v + u v'$ and factor out the common exponential.",
                ],
                "distractors": [
                    f"$ f'(x) = {scale * a}x^{scale - 1} e^({a}x + {b}) $",
                    f"$ f'(x) = x^{scale} e^({a}x + {b}) $",
                    f"$ f'(x) = ({scale}x - {a}) e^({a}x + {b}) $",
                ],
            }
        if "quotient rule" in t_low:
            a = rng.randint(1, 3 * scale)
            b = rng.randint(1, 5)
            return {
                "prompt_text": "Differentiate the function using the Quotient Rule.",
                "equation_typst": f"$ f(x) = ({a}x)/(x^2 + {b}) $",
                "answer_typst": f"$ f'(x) = ({a}({b} - x^2))/((x^2 + {b})^2) $",
                "steps_typst": [
                    f"Let $u = {a}x$ ($u' = {a}$) and $v = x^2 + {b}$ ($v' = 2x$).",
                    f"Apply the Quotient Rule: $f'(x) = ({a}(x^2 + {b}) - {a}x(2x)) / (x^2 + {b})^2$.",
                    f"Simplify the numerator: $({a}({b} - x^2)) / (x^2 + {b})^2$.",
                ],
                "distractors": [
                    f"$ f'(x) = ({a}(x^2 + {b}))/((x^2 + {b})^2) $",
                    f"$ f'(x) = ({a})/(2x) $",
                    f"$ f'(x) = ({a}(x^2 - {b}))/((x^2 + {b})^2) $",
                ],
            }
        if "chain rule" in t_low:
            n = rng.randint(3, 3 + scale)
            a = rng.randint(2, 5)
            b = rng.randint(1, 7)
            return {
                "prompt_text": "Differentiate the composite function using the Chain Rule.",
                "equation_typst": f"$ f(x) = ({a}x^2 + {b})^{n} $",
                "answer_typst": f"$ f'(x) = {2 * a * n}x({a}x^2 + {b})^{n - 1} $",
                "steps_typst": [
                    f"Differentiate the outer power function: ${n}({a}x^2 + {b})^{n - 1}$.",
                    f"Multiply by the derivative of the inner function $g'(x) = {2 * a}x$.",
                    f"Simplify: $f'(x) = {2 * a * n}x({a}x^2 + {b})^{n - 1}$.",
                ],
                "distractors": [
                    f"$ f'(x) = {n}({a}x^2 + {b})^{n - 1} $",
                    f"$ f'(x) = {n}({2 * a}x)^{n - 1} $",
                    f"$ f'(x) = {a * n}x({a}x^2 + {b})^{n} $",
                ],
            }
        if "inverse trigonometric" in t_low or "inverse_trigonometric" in t_low:
            fn_choice = rng.choice(["arcsin", "arccos", "arctan", "arcsec"])
            a = rng.randint(2, 25)
            k = rng.choice([1, 2, 3])
            if k == 1:
                u_str = f"{a}x"
                du_str = f"{a}"
                u_sq_str = f"{a * a}x^2"
            else:
                u_str = f"{a}x^{k}"
                du_str = f"{a * k}x^{k - 1}" if k > 2 else f"{a * k}x"
                u_sq_str = f"{a * a}x^{2 * k}"

            if fn_choice == "arcsin":
                eq_s = f"$ f(x) = arcsin({u_str}) $"
                ans_s = f"$ f'(x) = ({du_str})/(sqrt(1 - {u_sq_str})) $"
                step_rule = "Recall $d/dx[arcsin(u)] = (u') / sqrt(1 - u^2)$."
            elif fn_choice == "arccos":
                eq_s = f"$ f(x) = arccos({u_str}) $"
                ans_s = f"$ f'(x) = -({du_str})/(sqrt(1 - {u_sq_str})) $"
                step_rule = "Recall $d/dx[arccos(u)] = -(u') / sqrt(1 - u^2)$."
            elif fn_choice == "arctan":
                eq_s = f"$ f(x) = arctan({u_str}) $"
                ans_s = f"$ f'(x) = ({du_str})/(1 + {u_sq_str}) $"
                step_rule = "Recall $d/dx[arctan(u)] = (u') / (1 + u^2)$."
            else:
                eq_s = f"$ f(x) = arcsec({u_str}) $"
                ans_s = f"$ f'(x) = ({du_str})/(|{u_str}| sqrt({u_sq_str} - 1)) $"
                step_rule = "Recall $d/dx[arcsec(u)] = (u') / (|u| sqrt(u^2 - 1))$."

            return {
                "prompt_text": "Differentiate the inverse trigonometric function with respect to x.",
                "equation_typst": eq_s,
                "answer_typst": ans_s,
                "steps_typst": [
                    step_rule,
                    f"Identify inner argument $u = {u_str}$ and compute derivative $u' = {du_str}$.",
                    f"Square argument: $u^2 = {u_sq_str}$. Substitute $u$ and $u'$ to obtain $f'(x)$.",
                ],
                "distractors": [
                    f"$ f'(x) = (1)/(sqrt(1 - {u_sq_str})) $",
                    f"$ f'(x) = ({du_str})/(1 - {u_sq_str}) $",
                    f"$ f'(x) = -({du_str})/(1 + {u_sq_str}) $",
                ],
            }
        if "trigonometric" in t_low:
            fn_t = rng.choice(["sin", "cos", "tan", "sec", "csc", "cot"])
            a = rng.randint(2, 20)
            c = rng.choice([k for k in range(-15, 16) if k != 0])
            if fn_t == "sin":
                ans_s = f"$ f'(x) = {c * a} cos({a}x) $"
                rule_s = "$d/dx[sin(u)] = cos(u) u'$"
            elif fn_t == "cos":
                ans_s = f"$ f'(x) = {-c * a} sin({a}x) $"
                rule_s = "$d/dx[cos(u)] = -sin(u) u'$"
            elif fn_t == "tan":
                ans_s = f"$ f'(x) = {c * a} sec^2({a}x) $"
                rule_s = "$d/dx[tan(u)] = sec^2(u) u'$"
            elif fn_t == "sec":
                ans_s = f"$ f'(x) = {c * a} sec({a}x) tan({a}x) $"
                rule_s = "$d/dx[sec(u)] = sec(u) tan(u) u'$"
            elif fn_t == "csc":
                ans_s = f"$ f'(x) = {-c * a} csc({a}x) cot({a}x) $"
                rule_s = "$d/dx[csc(u)] = -csc(u) cot(u) u'$"
            else:
                ans_s = f"$ f'(x) = {-c * a} csc^2({a}x) $"
                rule_s = "$d/dx[cot(u)] = -csc^2(u) u'$"

            return {
                "prompt_text": "Differentiate the trigonometric function with respect to x.",
                "equation_typst": f"$ f(x) = {c} {fn_t}({a}x) $",
                "answer_typst": ans_s,
                "steps_typst": [
                    f"Use chain rule formula: {rule_s}.",
                    f"Identify outer constant ${c}$ and inner derivative of ${a}x$: $u' = {a}$.",
                    f"Multiply constants: ${c} times {a} = {c * a}$ to find the final derivative.",
                ],
                "distractors": [
                    f"$ f'(x) = {c} {fn_t}({a}x) $",
                    f"$ f'(x) = {-c * a} {fn_t}({a}x) $",
                    f"$ f'(x) = {c * a} x {fn_t}({a}x) $",
                ],
            }
        if "logarithm" in t_low or "exponential" in t_low:
            a = rng.randint(2, 4 * scale)
            b = rng.randint(1, 6)
            return {
                "prompt_text": "Differentiate the logarithmic or exponential function.",
                "equation_typst": f"$ f(x) = ln({a}x^2 + {b}) $",
                "answer_typst": f"$ f'(x) = ({2 * a}x)/({a}x^2 + {b}) $",
                "steps_typst": [
                    "Apply the logarithmic derivative rule $d/(d x)[ln(u)] = u' / u$.",
                    f"Differentiate the argument $u = {a}x^2 + {b}$ to get $u' = {2 * a}x$.",
                    f"Result: $f'(x) = ({2 * a}x)/({a}x^2 + {b})$.",
                ],
                "distractors": [
                    f"$ f'(x) = (1)/({a}x^2 + {b}) $",
                    f"$ f'(x) = {2 * a}x ln({a}x^2 + {b}) $",
                    f"$ f'(x) = ({a}x)/({a}x^2 + {b}) $",
                ],
            }
        if "inverse functions" in t_low:
            a = rng.randint(2, 5)
            b = rng.randint(1, 6)
            x0 = rng.randint(1, 3)
            y0 = a * (x0 ** 3) + b
            fp = 3 * a * (x0 ** 2)
            return {
                "prompt_text": "Use the Inverse Function Derivative Theorem (f^-1)'(b) = 1 / f'(a) to find the derivative of the inverse.",
                "equation_typst": f"$ f(x) = {a}x^3 + {b}, quad f({x0}) = {y0}; quad \"find \" (f^(-1))'({y0}) $",
                "answer_typst": f"$ (f^(-1))'({y0}) = 1/({fp}) $",
                "steps_typst": [
                    f"Since $f({x0}) = {y0}$, we have $f^(-1)({y0}) = {x0}$.",
                    f"Differentiate $f(x)$: $f'(x) = {3 * a}x^2 arrow.r.double f'({x0}) = {fp}$.",
                    f"Apply $(f^(-1))'({y0}) = 1 / f'({x0}) = 1/({fp})$.",
                ],
                "distractors": [f"$ {fp} $", f"$ -1/({fp}) $", f"$ 1/({y0}) $"],
            }

    # ------------------------------------------------------------------
    # B. CALCULUS APPLICATIONS OF DIFFERENTIATION
    # ------------------------------------------------------------------
    if "applications of differentiation" in c_low or ("functions" in c_low and "extrema" in t_low):
        if "increase and decrease" in t_low or "extrema" in t_low:
            c = rng.randint(1, 6)
            d = rng.randint(-15, 15)
            d_str = f"+ {d}" if d > 0 else (f"- {abs(d)}" if d < 0 else "")
            if "absolute" in t_low:
                L, R = -c - 1, c + 1
                y_L = (L ** 3) - 3 * c * c * L + d
                y_R = (R ** 3) - 3 * c * c * R + d
                y_neg_c = ((-c) ** 3) - 3 * c * c * (-c) + d
                y_pos_c = (c ** 3) - 3 * c * c * c + d
                vals = [(y_L, L), (y_R, R), (y_neg_c, -c), (y_pos_c, c)]
                abs_max_y, abs_max_x = max(vals, key=lambda p: p[0])
                abs_min_y, abs_min_x = min(vals, key=lambda p: p[0])
                return {
                    "prompt_text": f"Find the absolute maximum and minimum values of f(x) on the closed interval [{L}, {R}].",
                    "equation_typst": f"$ f(x) = x^3 - {3 * c * c}x {d_str} quad [ {L}, {R} ] $",
                    "answer_typst": f"$ \"Abs Max\": {abs_max_y} \" at \" x = {abs_max_x}, quad \"Abs Min\": {abs_min_y} \" at \" x = {abs_min_x} $",
                    "steps_typst": [
                        f"Find critical points in the interval: $f'(x) = 3x^2 - {3 * c * c} = 0 arrow.r.double x = plus.minus {c}$.",
                        f"Evaluate $f(x)$ at critical points and endpoints: $f({L}) = {y_L}, f({-c}) = {y_neg_c}, f({c}) = {y_pos_c}, f({R}) = {y_R}$.",
                        f"The absolute maximum is ${abs_max_y}$ (at $x = {abs_max_x}$) and the absolute minimum is ${abs_min_y}$ (at $x = {abs_min_x}$).",
                    ],
                    "distractors": [
                        f"$ \"Abs Max\": {abs_max_y + 4} \" at \" x = {abs_max_x}, quad \"Abs Min\": {abs_min_y - 4} \" at \" x = {abs_min_x} $",
                        f"$ \"Abs Max\": {y_R} \" at \" x = {R}, quad \"Abs Min\": {y_L} \" at \" x = {L} $",
                        f"$ \"Abs Max\": {abs_max_y} \" at \" x = {abs_max_x} \" only\" $",
                    ],
                }
            elif "relative" in t_low:
                local_max_y = ((-c) ** 3) - 3 * c * c * (-c) + d
                local_min_y = (c ** 3) - 3 * c * c * c + d
                return {
                    "prompt_text": "Find all relative (local) extrema for the function using the First or Second Derivative Test.",
                    "equation_typst": f"$ f(x) = x^3 - {3 * c * c}x {d_str} $",
                    "answer_typst": f"$ \"Local Max at \" (-{c}, {local_max_y}), quad \"Local Min at \" ({c}, {local_min_y}) $",
                    "steps_typst": [
                        f"Differentiate: $f'(x) = 3x^2 - {3 * c * c} = 3(x + {c})(x - {c})$.",
                        f"Critical points occur at $x = -{c}$ and $x = {c}$.",
                        f"Second derivative $f''(x) = 6x$: $f''(-{c}) = -{6 * c} < 0$ (Local Max), $f''({c}) = {6 * c} > 0$ (Local Min).",
                    ],
                    "distractors": [
                        f"$ \"Local Max at \" ({c}, {local_min_y}), quad \"Local Min at \" (-{c}, {local_max_y}) $",
                        f"$ \"Local Extrema at \" x = 0, {c * c} $",
                        f"$ \"Local Max at \" (-{c}, {local_max_y + 2}) $",
                    ],
                }
            return {
                "prompt_text": "Find the critical numbers and intervals of increase and decrease for f(x).",
                "equation_typst": f"$ f(x) = x^3 - {3 * c * c}x {d_str} $",
                "answer_typst": f"$ \"Critical points\": x = plus.minus {c}; quad \"Inc\": (-infinity, -{c}) union ({c}, infinity), \" Dec\": (-{c}, {c}) $",
                "steps_typst": [
                    f"Differentiate: $f'(x) = 3x^2 - {3 * c * c} = 3(x - {c})(x + {c})$.",
                    f"Set $f'(x) = 0$ to find critical numbers $x = -{c}$ and $x = {c}$.",
                    f"$f'(x) > 0$ on $(-infinity, -{c}) union ({c}, infinity)$ and $f'(x) < 0$ on $(-{c}, {c})$.",
                ],
                "distractors": [
                    f"$ \"Critical points\": x = 0, {c}; quad \"Inc\": (-{c}, {c}) $",
                    f"$ \"Critical points\": x = plus.minus {3 * c}; quad \"Dec\": (-infinity, -{c}) $",
                    f"$ \"Critical points\": x = {c * c}; quad \"Inc\": (0, infinity) $",
                ],
            }
        if "concavity" in t_low:
            a_pool = [k for k in range(-4 * scale, 4 * scale + 1) if k != 0]
            a = rng.choice(a_pool)
            b = 3 * a
            s_b = f"- {b}x^2" if b > 0 else f"+ {abs(b)}x^2"
            return {
                "prompt_text": "Find the inflection point and intervals of concavity for the function.",
                "equation_typst": f"$ f(x) = x^3 {s_b} + 5 $",
                "answer_typst": f"$ \"Inflection at \" x = {a}; quad \"Concave down\": (-infinity, {a}), \" Concave up\": ({a}, infinity) $",
                "steps_typst": [
                    f"Find the first derivative: $f'(x) = 3x^2 - {2 * b}x$.",
                    f"Find the second derivative: $f''(x) = 6x - {6 * a} = 6(x - {a})$.",
                    f"$f''(x) < 0$ for $x < {a}$ (concave down) and $f''(x) > 0$ for $x > {a}$ (concave up).",
                ],
                "distractors": [
                    f"$ \"Inflection at \" x = {-a}; quad \"Concave up\": (-infinity, {-a}) $",
                    f"$ \"Inflection at \" x = {2 * a}; quad \"Concave down\": ({a}, infinity) $",
                    "$ \"No inflection point\" $",
                ],
            }
        if "optimization" in t_low:
            opt_mode = rng.choice(["perimeter", "fence_river", "box_open"])
            if opt_mode == "fence_river":
                p = rng.randint(4, 25) * 4
                x = p // 4
                y = p // 2
                max_area = x * y
                return {
                    "prompt_text": "A farmer encloses a rectangular field along a straight river (no fence needed along river). Find the dimensions that maximize area with fencing P.",
                    "equation_typst": f"\"Fencing perimeter \" 2x + y = {p} \" meters\"",
                    "answer_typst": f"$ x = {x} \" m\", quad y = {y} \" m\", quad A_\"max\" = {max_area} \" m\"^2 $",
                    "steps_typst": [
                        f"From $2x + y = {p}$, express $y = {p} - 2x$. Area $A(x) = x({p} - 2x) = {p}x - 2x^2$.",
                        f"Differentiate and set to zero: $A'(x) = {p} - 4x = 0 ==> x = {x}$.",
                        f"Then $y = {p} - 2({x}) = {y}$, giving maximum area $A = {x} times {y} = {max_area}$.",
                    ],
                    "distractors": [f"$ x = {p // 3}, y = {p // 3} $", f"$ A_\"max\" = {p * 2} $", f"$ x = {x * 2}, y = {y // 2} $"],
                }
            elif opt_mode == "box_open":
                s = rng.choice([12, 16, 18, 20, 24, 30])
                x = s // 6
                vol = x * (s - 2 * x) * (s - 2 * x)
                return {
                    "prompt_text": "An open-top box is made by cutting congruent squares of side x from corners of a square sheet of cardboard and folding up sides. Find x maximizing volume.",
                    "equation_typst": f"\"Cardboard square side \" s = {s} \" in.\"",
                    "answer_typst": f"$ x = {x} \" in.\", quad V_\"max\" = {vol} \" in\"^3 $",
                    "steps_typst": [
                        f"Volume function $V(x) = x({s} - 2x)^2 = 4x^3 - {4 * s}x^2 + {s * s}x$.",
                        f"Differentiate: $V'(x) = 12x^2 - {8 * s}x + {s * s} = (2x - {s})(6x - {s}) = 0$.",
                        f"Since $0 < x < {s // 2}$, choose $x = {s}/6 = {x}$. Maximum volume $V = {vol}$.",
                    ],
                    "distractors": [f"$ x = {s // 4}, V = {s * s} $", f"$ x = {x + 1}, V = {vol - 8} $", f"$ V_\"max\" = {s ** 3} $"],
                }
            else:
                side = rng.randint(5, 35)
                perim = 4 * side
                max_area = side * side
                return {
                    "prompt_text": "Use calculus optimization to find the dimensions that maximize the objective quantity.",
                    "equation_typst": f"\"Find the maximum area of a rectangle with perimeter \" P = {perim} \" units.\"",
                    "answer_typst": f"$ x = y = {side}, quad A_\"max\" = {max_area} $",
                    "steps_typst": [
                        f"From $2x + 2y = {perim}$, write $y = {2 * side} - x$ and Area $A(x) = x({2 * side} - x) = {2 * side}x - x^2$.",
                        f"Set $A'(x) = {2 * side} - 2x = 0 ==> x = {side}$.",
                        f"Then $y = {side}$ and maximum area $A = {side}^2 = {max_area}$.",
                    ],
                    "distractors": [
                        f"$ x = y = {2 * side}, quad A_\"max\" = {perim * 2} $",
                        f"$ x = {side - 2}, y = {side + 2}, quad A_\"max\" = {max_area - 4} $",
                        f"$ A_\"max\" = {perim} $",
                    ],
                }
        if "motion along a line" in t_low:
            a = rng.randint(1, 3)
            b = rng.randint(2, 6)
            t0 = rng.randint(1, 3 * scale)
            v = 2 * a * t0 + b
            acc = 2 * a
            return {
                "prompt_text": "Given the position function s(t) of a particle moving along a line, find its velocity v(t) and acceleration a(t) at time t.",
                "equation_typst": f"$ s(t) = {a}t^2 + {b}t, quad t = {t0} $",
                "answer_typst": f"$ v({t0}) = {v}, quad a({t0}) = {acc} $",
                "steps_typst": [
                    f"Velocity is the first derivative: $v(t) = s'(t) = {2 * a}t + {b} arrow.r.double v({t0}) = {v}$.",
                    f"Acceleration is the second derivative: $a(t) = v'(t) = {acc}$.",
                    f"At $t = {t0}$: $v({t0}) = {v}$ and $a({t0}) = {acc}$.",
                ],
                "distractors": [
                    f"$ v({t0}) = {a * t0 * t0 + b * t0}, quad a({t0}) = {v} $",
                    f"$ v({t0}) = {acc}, quad a({t0}) = {v} $",
                    f"$ v({t0}) = {v + b}, quad a({t0}) = 0 $",
                ],
            }
        if "differentials" in t_low:
            func_type = rng.choice(["quad", "cubic", "sqrt", "poly"])
            x0 = rng.randint(1, 12)
            dx = rng.choice([0.01, 0.02, 0.04, 0.05, 0.1, -0.01, -0.02, -0.05, -0.1])
            if func_type == "cubic":
                dy = 3 * (x0 ** 2) * dx
                eq_s = f"$ y = x^3, quad x = {x0}, quad d x = {dx:g} $"
                step_deriv = f"Compute derivative: $f'(x) = 3x^2 ==> f'({x0}) = {3 * x0 * x0}$."
            elif func_type == "sqrt":
                sq_x0 = rng.choice([1, 4, 9, 16, 25])
                x0 = sq_x0
                dy = (1.0 / (2 * math.sqrt(x0))) * dx
                eq_s = f"$ y = sqrt(x), quad x = {x0}, quad d x = {dx:g} $"
                step_deriv = f"Compute derivative: $f'(x) = 1/(2 sqrt(x)) ==> f'({x0}) = 1/{int(2 * math.sqrt(x0))}$."
            elif func_type == "poly":
                a_coef = rng.randint(2, 5)
                b_coef = rng.randint(1, 6)
                dy = (2 * a_coef * x0 + b_coef) * dx
                eq_s = f"$ y = {a_coef}x^2 + {b_coef}x, quad x = {x0}, quad d x = {dx:g} $"
                step_deriv = f"Compute derivative: $f'(x) = {2 * a_coef}x + {b_coef} ==> f'({x0}) = {2 * a_coef * x0 + b_coef}$."
            else:
                dy = 2 * x0 * dx
                eq_s = f"$ y = x^2, quad x = {x0}, quad d x = {dx:g} $"
                step_deriv = f"Compute derivative: $f'(x) = 2x ==> f'({x0}) = {2 * x0}$."

            return {
                "prompt_text": "Find the differential dy = f'(x) dx for the given function and values of x and dx.",
                "equation_typst": eq_s,
                "answer_typst": f"$ d y = {dy:.4g} $",
                "steps_typst": [
                    step_deriv,
                    f"Write differential formula: $d y = f'({x0}) d x = f'({x0}) times ({dx:g})$.",
                    f"Evaluate product: $d y = {dy:.4g}$.",
                ],
                "distractors": [f"$ d y = {dy * 2:.4g} $", f"$ d y = {dx:g} $", f"$ d y = {-dy:.4g} $"],
            }

    # ------------------------------------------------------------------
    # C. CALCULUS LIMITS & CONTINUITY
    # ------------------------------------------------------------------
    if c_low in ("limits", "continuity") or "continuity" in t_low or ("introduction to calculus" in c_low and "limit" in t_low):
        if "direct evaluation" in t_low:
            a = rng.randint(1, 3 * scale)
            b = rng.randint(1, 5)
            c = rng.randint(-3, 4)
            val = a * c * c + b
            return {
                "prompt_text": "Evaluate the limit by direct substitution.",
                "equation_typst": f"$ lim_(x arrow.r {c}) ({a}x^2 + {b}) $",
                "answer_typst": f"$ {val} $",
                "steps_typst": [
                    "Polynomials are continuous everywhere, so evaluate by direct substitution.",
                    f"Substitute $x = {c}$: ${a}({c})^2 + {b} = {a * c * c} + {b}$.",
                    f"Result: ${val}$.",
                ],
                "distractors": [f"$ {a * c + b} $", f"$ {val - 2 * b} $", f"$ {2 * a * c} $"],
            }
        if "removable" in t_low:
            a = rng.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
            b = rng.choice([x for x in [-6, -5, -4, -3, -2, 1, 2, 3, 4, 5, 6] if x != -a])
            mid_coeff = b - a
            const_term = -a * b
            mid_str = f"+ {mid_coeff}x" if mid_coeff > 0 else (f"- {abs(mid_coeff)}x" if mid_coeff < 0 else "")
            const_str = f"+ {const_term}" if const_term > 0 else (f"- {abs(const_term)}" if const_term < 0 else "")
            num_str = f"x^2 {mid_str} {const_str}".strip()
            ans_val = a + b
            denom_str = f"x {'+' if a < 0 else '-'} {abs(a)}"
            return {
                "prompt_text": "Evaluate the limit at the removable discontinuity by factoring and canceling.",
                "equation_typst": f"$ lim_(x arrow.r {a}) ({num_str})/({denom_str}) $",
                "answer_typst": f"$ {ans_val} $",
                "steps_typst": [
                    f"Direct substitution gives $0/0$. Factor the numerator: $(x - {a})(x + {b}) / (x - {a})$.",
                    f"Cancel common factor $(x - {a})$ to obtain $lim_(x arrow.r {a}) (x + {b})$.",
                    f"Substitute $x = {a}$: ${a} + {b} = {ans_val}$.",
                ],
                "distractors": ["$ 0 $", f"$ {a} $", "$ \"DNE\" $"],
            }
        if "essential" in t_low:
            a = rng.randint(1, 4 * scale)
            k = rng.randint(2, 6)
            return {
                "prompt_text": "Determine the limit at the vertical asymptote (essential discontinuity).",
                "equation_typst": f"$ lim_(x arrow.r {a}) ({k})/((x - {a})^2) $",
                "answer_typst": "$ +infinity $",
                "steps_typst": [
                    f"As $x arrow.r {a}$, the denominator $(x - {a})^2 arrow.r 0^+$ through positive values.",
                    f"Since the numerator ${k} > 0$, the quotient grows without bound.",
                    "Therefore, the limit is $+infinity$.",
                ],
                "distractors": ["$ -infinity $", "$ 0 $", f"$ {k} $"],
            }
        if "infinity" in t_low:
            a = rng.randint(2, 5 * scale)
            b = rng.randint(2, 5)
            f = Fraction(a, b)
            return {
                "prompt_text": "Evaluate the limit at infinity.",
                "equation_typst": f"$ lim_(x arrow.r infinity) ({a}x^2 + 3x - 1)/({b}x^2 - 4) $",
                "answer_typst": f"$ {_fmt_frac(f)} $",
                "steps_typst": [
                    "Divide numerator and denominator by the highest power $x^2$.",
                    "As $x arrow.r infinity$, $3/x arrow.r 0$, $1/x^2 arrow.r 0$, and $4/x^2 arrow.r 0$.",
                    f"The limit equals the ratio of leading coefficients: ${_fmt_frac(f)}$.",
                ],
                "distractors": ["$ 0 $", "$ infinity $", f"$ -{_fmt_frac(f)} $"],
            }
        if "continuity" in c_low or "continuity" in t_low:
            cont_family = rng.choice(["rational_remov_inf", "piecewise_jump", "removable_point"])
            if cont_family == "piecewise_jump":
                c_pt = rng.randint(-4, 4)
                m1 = rng.choice([-3, -2, 1, 2, 3])
                b1 = rng.randint(-4, 4)
                m2 = rng.choice([-3, -2, 1, 2, 3])
                b2 = rng.randint(-4, 4)
                while (m1 * c_pt + b1) == (m2 * c_pt + b2):
                    b2 += 2
                val_left = m1 * c_pt + b1
                val_right = m2 * c_pt + b2
                return {
                    "prompt_text": "Determine if the piecewise function is continuous at x = c; if not, classify the discontinuity.",
                    "equation_typst": f"$ f(x) = cases({m1}x {('+' if b1>=0 else '-')} {abs(b1)} &\"if \" x <= {c_pt}, {m2}x {('+' if b2>=0 else '-')} {abs(b2)} &\"if \" x > {c_pt}) $",
                    "answer_typst": f"$ \"Jump discontinuity at \" x = {c_pt} $",
                    "steps_typst": [
                        f"Evaluate left-hand limit: $lim_(x ==> {c_pt}^-) f(x) = {m1}({c_pt}) + {b1} = {val_left}$.",
                        f"Evaluate right-hand limit: $lim_(x ==> {c_pt}^+) f(x) = {m2}({c_pt}) + {b2} = {val_right}$.",
                        f"Since left limit (${val_left}$) != right limit (${val_right}$), there is a jump discontinuity at $x = {c_pt}$.",
                    ],
                    "distractors": [f"$ \"Continuous at \" x = {c_pt} $", f"$ \"Removable discontinuity at \" x = {c_pt} $", f"$ \"Infinite discontinuity at \" x = {c_pt} $"],
                }
            elif cont_family == "removable_point":
                c_pt = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                l_val = rng.randint(2, 15)
                true_l = 2 * c_pt
                while l_val == true_l:
                    l_val += 3
                return {
                    "prompt_text": "Determine if the function is continuous at x = c; if not, classify the discontinuity.",
                    "equation_typst": f"$ f(x) = cases(((x^2 - {c_pt * c_pt}))/((x - {c_pt})) &\"if \" x != {c_pt}, {l_val} &\"if \" x = {c_pt}) $",
                    "answer_typst": f"$ \"Removable discontinuity at \" x = {c_pt} $",
                    "steps_typst": [
                        f"Evaluate the limit as $x ==> {c_pt}$: $lim_(x ==> {c_pt}) (x - {c_pt})(x + {c_pt}) / (x - {c_pt}) = {c_pt} + {c_pt} = {true_l}$.",
                        f"Compare with defined value $f({c_pt}) = {l_val}$.",
                        f"Since $lim_(x ==> {c_pt}) f(x) = {true_l} != f({c_pt}) = {l_val}$, there is a removable discontinuity at $x = {c_pt}$.",
                    ],
                    "distractors": [f"$ \"Continuous at \" x = {c_pt} $", f"$ \"Jump discontinuity at \" x = {c_pt} $", f"$ \"Infinite discontinuity at \" x = {c_pt} $"],
                }
            else:
                a_pt = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
                b_pt = rng.choice([k for k in range(-6, 7) if k != 0 and k != a_pt])
                s_a = f"- {a_pt}" if a_pt > 0 else f"+ {abs(a_pt)}"
                s_b = f"- {b_pt}" if b_pt > 0 else f"+ {abs(b_pt)}"
                return {
                    "prompt_text": "Find all points of discontinuity and classify each as removable, jump, or infinite.",
                    "equation_typst": f"$ f(x) = (x {s_a})/((x {s_a})(x {s_b})) $",
                    "answer_typst": f"$ x = {a_pt} \" (removable)\", quad x = {b_pt} \" (infinite)\" $",
                    "steps_typst": [
                        f"Set denominator to zero: $(x {s_a})(x {s_b}) = 0 ==> x = {a_pt}, {b_pt}$.",
                        f"The factor $(x {s_a})$ cancels with the numerator, so $x = {a_pt}$ is a removable discontinuity.",
                        f"The factor $(x {s_b})$ remains in the denominator, so $x = {b_pt}$ is an infinite discontinuity (vertical asymptote).",
                    ],
                    "distractors": [
                        f"$ x = {a_pt} \" (infinite)\", quad x = {b_pt} \" (removable)\" $",
                        f"$ x = {a_pt} \" (jump)\", quad x = {b_pt} \" (jump)\" $",
                        "$ \"Continuous everywhere\" $",
                    ],
                }

    # ------------------------------------------------------------------
    # D. CALCULUS INTEGRATION SUBTOPICS
    # ------------------------------------------------------------------
    if "integration" in c_low or ("introduction to calculus" in c_low and ("area" in t_low or "integral" in t_low)):
        if "approximating area" in t_low:
            n = rng.choice([3, 4, 5, 6])
            c_val = rng.randint(1, 4)
            b_end = n
            dx = 1
            method = rng.choice(["LRAM", "RRAM"])
            if method == "LRAM":
                pts = list(range(0, n))
                f_vals = [float(x * x + c_val ) for x in pts]
                approx_sum = sum(f_vals)
                m_label = f"L_{n}"
                step_pts = f"left endpoints $x = {', '.join(str(p) for p in pts)}$"
            else:
                pts = list(range(1, n + 1))
                f_vals = [float(x * x + c_val ) for x in pts]
                approx_sum = sum(f_vals)
                m_label = f"R_{n}"
                step_pts = f"right endpoints $x = {', '.join(str(p) for p in pts)}$"

            def _fn_area(x: float) -> float:
                return float(0.15 * float(x) * float(x) + float(c_val))

            boxes = [(pts[i] if method == "LRAM" else pts[i] - 1, _fn_area(float(pts[i])), 1) for i in range(n)]

            return {
                "prompt_text": f"Approximate the area under f(x) = x^2 + {c_val} on [0, {b_end}] using a {method} sum with n = {n} subintervals.",
                "equation_typst": f"$ integral_0^{b_end} (x^2 + {c_val}) d x quad (\"{method}\", n = {n}) $",
                "answer_typst": f"$ {m_label} = {approx_sum} $",
                "steps_typst": [
                    f"Subinterval width $Delta x = ({b_end} - 0)/{n} = {dx}$, with {step_pts}.",
                    f"Evaluate $f(x)$ values: ${' + '.join(str(v) for v in f_vals)}$.",
                    f"Sum rectangle areas: ${m_label} = {dx}({' + '.join(str(v) for v in f_vals)}) = {approx_sum}$.",
                ],
                "distractors": [f"$ {m_label} = {approx_sum + n * 2} $", f"$ {m_label} = {max(1, approx_sum - n * 2)} $", f"$ {m_label} = {approx_sum + 10} $"],
                "diagram_svg": svg_coordinate_plane(functions=[{"fn": _fn_area, "x_start": 0, "x_end": b_end, "color": "#1d4ed8"}], riemann_boxes=boxes),
                "answer_svg": svg_coordinate_plane(functions=[{"fn": _fn_area, "x_start": 0, "x_end": b_end, "color": "#1d4ed8"}], riemann_boxes=boxes),
            }
        if "limit of sums" in t_low:
            b = rng.randint(2, 4 + scale)
            area = Fraction(b ** 3, 3)
            return {
                "prompt_text": "Evaluate the definite integral using the limit of Riemann sums lim_(n->infinity) sum_(i=1)^n f(x_i) Delta x.",
                "equation_typst": f"$ lim_(n arrow.r infinity) sum_(i=1)^n ((i dot {b})/(n))^2 ({b})/(n) = integral_0^{b} x^2 d x $",
                "answer_typst": f"$ {_fmt_frac(area)} $",
                "steps_typst": [
                    f"Factor out $({b}^3)/(n^3)$ and use $sum_(i=1)^n i^2 = (n(n+1)(2n+1))/6$.",
                    f"Take the limit as $n arrow.r infinity$: $({b ** 3}) dot (2)/(6) = ({b ** 3})/(3)$.",
                    f"Exact area: ${_fmt_frac(area)}$.",
                ],
                "distractors": [f"$ {b * b} $", f"$ {_fmt_frac(Fraction(b ** 3, 2))} $", f"$ {b ** 3} $"],
            }
        if "second fundamental theorem" in t_low:
            k = rng.randint(2, 6)
            c = rng.choice([1, 2, 4, 5, 9])
            return {
                "prompt_text": "Use the Second Fundamental Theorem of Calculus to differentiate the integral function.",
                "equation_typst": f"$ (d)/(d x) integral_1^(x^{k}) sqrt(t^3 + {c}) d t $",
                "answer_typst": f"$ {k}x^{k - 1} sqrt(x^({3 * k}) + {c}) $",
                "steps_typst": [
                    "By the Second Fundamental Theorem of Calculus with Chain Rule, $d/(d x) integral_a^(g(x)) f(t) d t = f(g(x)) dot g'(x)$.",
                    f"Substitute $t = x^{k}$ into $sqrt(t^3 + {c})$ to get $sqrt(x^({3 * k}) + {c})$.",
                    f"Multiply by $g'(x) = {k}x^{k - 1}$.",
                ],
                "distractors": [
                    f"$ sqrt(x^({3 * k}) + {c}) $",
                    f"$ {k}x^{k - 1} sqrt(x^3 + {c}) $",
                    f"$ (3x^2)/(2 sqrt(x^3 + {c})) $",
                ],
            }
        if "mean value theorem" in t_low:
            b = rng.choice([2, 4, 6])
            a_coef = rng.randint(1, 3 * scale)
            f_avg = a_coef * b
            return {
                "prompt_text": "Find the average value f_avg of the function on the given closed interval.",
                "equation_typst": f"$ f(x) = {2 * a_coef}x quad \"on\" [0, {b}] $",
                "answer_typst": f"$ f_\"avg\" = {f_avg} $",
                "steps_typst": [
                    f"Use the Average Value Formula: $f_\"avg\" = 1/({b} - 0) integral_0^{b} {2 * a_coef}x d x$.",
                    f"Evaluate the integral: $[{a_coef}x^2]_0^{b} = {a_coef * b * b}$.",
                    f"Divide by ${b}$: $f_\"avg\" = {f_avg}$.",
                ],
                "distractors": [f"$ {a_coef * b * b} $", f"$ {2 * f_avg} $", f"$ {b // 2} $"],
            }
        if "substitution" in t_low:
            a = rng.randint(2, 4 * scale)
            n = rng.randint(3, 6)
            return {
                "prompt_text": "Evaluate the integral using u-substitution.",
                "equation_typst": f"$ integral 2x(x^2 + {a})^{n} d x $",
                "answer_typst": f"$ ((x^2 + {a})^{n + 1})/({n + 1}) + C $",
                "steps_typst": [
                    f"Let $u = x^2 + {a}$, so $d u = 2x d x$.",
                    f"Rewrite the integral in terms of $u$: $integral u^{n} d u = u^{n + 1} / ({n + 1}) + C$.",
                    f"Substitute back $u = x^2 + {a}$: $((x^2 + {a})^{n + 1})/({n + 1}) + C$.",
                ],
                "distractors": [
                    f"$ (x^2 + {a})^{n + 1} + C $",
                    f"$ (2x(x^2 + {a})^{n + 1})/({n + 1}) + C $",
                    f"$ {n}(x^2 + {a})^{n - 1} + C $",
                ],
            }

    # ------------------------------------------------------------------
    # E. SEQUENCES & SERIES SUBTOPICS
    # ------------------------------------------------------------------
    if "sequences" in c_low:
        a1 = rng.randint(2, 6 * scale)
        d = rng.randint(2, 5 * scale)
        r = rng.choice([2, 3])
        if "arithmetic sequence" in t_low:
            n = rng.randint(10, 20)
            an = a1 + (n - 1) * d
            return {
                "prompt_text": "Find the explicit formula and the nth term of the arithmetic sequence.",
                "equation_typst": f"$ a_1 = {a1}, quad d = {d}, quad \"find \" a_({n}) $",
                "answer_typst": f"$ a_n = {a1} + {d}(n - 1); quad a_({n}) = {an} $",
                "steps_typst": [
                    f"Use the arithmetic sequence formula $a_n = a_1 + (n - 1)d = {a1} + {d}(n - 1)$.",
                    f"Substitute $n = {n}$: $a_({n}) = {a1} + ({n - 1})({d})$.",
                    f"Compute: $a_({n}) = {an}$.",
                ],
                "distractors": [f"$ a_({n}) = {a1 + n * d} $", f"$ a_({n}) = {an - d} $", f"$ a_({n}) = {a1 * d} $"],
            }
        if "geometric sequence" in t_low:
            n = rng.randint(5, 7)
            an = a1 * (r ** (n - 1))
            return {
                "prompt_text": "Find the explicit formula and the nth term of the geometric sequence.",
                "equation_typst": f"$ a_1 = {a1}, quad r = {r}, quad \"find \" a_({n}) $",
                "answer_typst": f"$ a_n = {a1}({r})^(n - 1); quad a_({n}) = {an} $",
                "steps_typst": [
                    f"Use the geometric sequence formula $a_n = a_1 r^(n - 1) = {a1}({r})^(n - 1)$.",
                    f"Substitute $n = {n}$: $a_({n}) = {a1}({r})^{n - 1}$.",
                    f"Compute: $a_({n}) = {an}$.",
                ],
                "distractors": [f"$ a_({n}) = {a1 * (r ** n)} $", f"$ a_({n}) = {a1 + (n - 1) * r} $", f"$ a_({n}) = {an // r} $"],
            }
        if "arithmetic and geometric mean" in t_low:
            m = rng.randint(1, 25)
            k = rng.randint(2, 12)
            x, y = m, m * k * k
            am = (x + y) / 2
            gm = m * k
            return {
                "prompt_text": "Find the arithmetic mean and positive geometric mean (middle sequence term) of the two numbers.",
                "equation_typst": f"$ {x} \" and \" {y} $",
                "answer_typst": f"$ \"AM\" = {am:g}, quad \"GM\" = {gm} $",
                "steps_typst": [
                    f"Arithmetic mean: $\"AM\" = ({x} + {y})/2 = {am:g}$.",
                    f"Geometric mean: $\"GM\" = sqrt({x} times {y}) = sqrt({x * y}) = {gm}$.",
                    f"Result: $\"AM\" = {am:g}, \"GM\" = {gm}$.",
                ],
                "distractors": [
                    f"$ \"AM\" = {gm}, quad \"GM\" = {am:g} $",
                    f"$ \"AM\" = {x + y}, quad \"GM\" = {x * y} $",
                    f"$ \"AM\" = {am:g}, quad \"GM\" = {gm * 2} $",
                ],
            }
        if "arithmetic series" in t_low:
            n = rng.choice([10, 12, 16, 20])
            an = a1 + (n - 1) * d
            sn = (n * (a1 + an)) // 2
            return {
                "prompt_text": "Evaluate the sum S_n of the finite arithmetic series.",
                "equation_typst": f"$ a_1 = {a1}, quad a_({n}) = {an}, quad n = {n} $",
                "answer_typst": f"$ S_({n}) = {sn} $",
                "steps_typst": [
                    "Use the arithmetic series formula $S_n = n(a_1 + a_n)/2$.",
                    f"Substitute $n = {n}, a_1 = {a1}, a_({n}) = {an}$: $S_({n}) = {n}({a1} + {an})/2$.",
                    f"Simplify: $S_({n}) = {sn}$.",
                ],
                "distractors": [f"$ S_({n}) = {sn * 2} $", f"$ S_({n}) = {n * an} $", f"$ S_({n}) = {sn + a1} $"],
            }
        if "geometric series" in t_low:
            n = rng.randint(4, 6)
            sn = a1 * (r ** n - 1) // (r - 1)
            return {
                "prompt_text": "Evaluate the sum S_n of the finite geometric series.",
                "equation_typst": f"$ a_1 = {a1}, quad r = {r}, quad n = {n} $",
                "answer_typst": f"$ S_({n}) = {sn} $",
                "steps_typst": [
                    "Use the finite geometric series formula $S_n = a_1(r^n - 1)/(r - 1)$.",
                    f"Substitute $a_1 = {a1}, r = {r}, n = {n}$: $S_({n}) = {a1}({r}^{n} - 1)/({r - 1})$.",
                    f"Simplify: $S_({n}) = {sn}$.",
                ],
                "distractors": [f"$ S_({n}) = {a1 * (r ** n)} $", f"$ S_({n}) = {sn + a1} $", f"$ S_({n}) = {sn // 2} $"],
            }

    # ------------------------------------------------------------------
    # F. GEOMETRY TRIGONOMETRY & TRIANGLES DECOUPLED SUBTOPICS
    # ------------------------------------------------------------------
    if "finding trig" in t_low or "finding sine" in t_low or "finding ratios" in t_low:
        prim_triples = [
            (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41),
            (11, 60, 61), (12, 35, 37), (13, 84, 85), (16, 63, 65), (20, 21, 29),
            (28, 45, 53), (33, 56, 65), (36, 77, 85), (39, 80, 89), (48, 55, 73),
        ]
        opp0, adj0, hyp0 = rng.choice(prim_triples)
        mult = rng.choice([1, 2, 3, 4, 5])
        opp, adj, hyp = opp0 * mult, adj0 * mult, hyp0 * mult
        fn = rng.choice(["sin", "cos", "tan", "csc", "sec", "cot"])
        if fn == "sin":
            f = Fraction(opp, hyp)
        elif fn == "cos":
            f = Fraction(adj, hyp)
        elif fn == "tan":
            f = Fraction(opp, adj)
        elif fn == "csc":
            f = Fraction(hyp, opp)
        elif fn == "sec":
            f = Fraction(hyp, adj)
        else:
            f = Fraction(adj, opp)

        return {
            "prompt_text": "Find the value of the trigonometric ratio as a simplified fraction.",
            "equation_typst": f"$ {fn}(theta) quad (\"Opp\" = {opp}, \" Adj\" = {adj}, \" Hyp\" = {hyp}) $",
            "answer_typst": f"$ {fn}(theta) = {_fmt_frac(f)} $",
            "steps_typst": [
                "Use right triangle definitions: $\\sin = \"Opp\"/\"Hyp\"$, $\\cos = \"Adj\"/\"Hyp\"$, $\\tan = \"Opp\"/\"Adj\"$ and reciprocals $\\csc, \\sec, \\cot$.",
                f"Substitute side lengths into ${fn}(theta)$.",
                f"Reduce fraction to lowest terms: ${_fmt_frac(f)}$.",
            ],
            "distractors": [
                f"$ {_fmt_frac(Fraction(f.denominator, f.numerator))} $",
                f"$ {_fmt_frac(Fraction(adj if fn != 'cos' else opp, hyp))} $",
                f"$ {_fmt_frac(Fraction(opp + adj, hyp))} $",
            ],
            "diagram_svg": svg_right_triangle(a_label=str(adj), b_label=str(opp), c_label=str(hyp), theta_label="theta"),
            "answer_svg": svg_right_triangle(a_label=str(adj), b_label=str(opp), c_label=str(hyp), theta_label=f"{fn}={f}"),
        }

    if "finding angle" in t_low or "finding_angles" in t_low or "angle_measures" in t_low:
        trig_mode = rng.choice(["tan", "sin", "cos"])
        if trig_mode == "tan":
            opp = rng.randint(3, 40)
            adj = rng.randint(3, 40)
            deg = round(math.degrees(math.atan2(opp, adj)), 1)
            eq_s = f"$ tan(theta) = ({opp})/({adj}) $"
            step_id = f"Opposite = ${opp}$, Adjacent = ${adj}$ ==> $tan(theta) = {opp}/{adj}$."
            diag_a, diag_b, diag_c = str(adj), str(opp), ""
        elif trig_mode == "sin":
            opp = rng.randint(3, 35)
            hyp = opp + rng.randint(2, 25)
            deg = round(math.degrees(math.asin(opp / hyp)), 1)
            eq_s = f"$ sin(theta) = ({opp})/({hyp}) $"
            step_id = f"Opposite = ${opp}$, Hypotenuse = ${hyp}$ ==> $sin(theta) = {opp}/{hyp}$."
            diag_a, diag_b, diag_c = "", str(opp), str(hyp)
        else:
            adj = rng.randint(3, 35)
            hyp = adj + rng.randint(2, 25)
            deg = round(math.degrees(math.acos(adj / hyp)), 1)
            eq_s = f"$ cos(theta) = ({adj})/({hyp}) $"
            step_id = f"Adjacent = ${adj}$, Hypotenuse = ${hyp}$ ==> $cos(theta) = {adj}/{hyp}$."
            diag_a, diag_b, diag_c = str(adj), "", str(hyp)

        return {
            "prompt_text": "Find the measure of angle theta to the nearest tenth of a degree.",
            "equation_typst": eq_s,
            "answer_typst": f"$ theta approx {deg}° $",
            "steps_typst": [
                step_id,
                f"Apply inverse function: $theta = arc{trig_mode}({eq_s.split('=')[1].strip().replace('$', '')})$.",
                f"Evaluate in degree mode: $theta approx {deg}°$.",
            ],
            "distractors": [
                f"$ theta approx {round(90.0 - deg, 1)}° $",
                f"$ theta approx {round(deg + 10.0, 1)}° $",
                f"$ theta approx {round(abs(deg - 15.0), 1)}° $",
            ],
            "diagram_svg": svg_right_triangle(a_label=diag_a, b_label=diag_b, c_label=diag_c, theta_label="theta=?"),
            "answer_svg": svg_right_triangle(a_label=diag_a, b_label=diag_b, c_label=diag_c, theta_label=f"{deg}°"),
        }

    if "missing sides" in t_low or "solving right triangles" in t_low or "finding angles and sides" in t_low or ("trig" in t_low and "solve" in t_low):
        ang = rng.randint(15, 75)
        side_mode = rng.choice(["find_opp_from_hyp", "find_adj_from_hyp", "find_opp_from_adj", "find_hyp_from_opp"])
        if side_mode == "find_opp_from_hyp":
            hyp = rng.randint(8, 45)
            val = round(hyp * math.sin(math.radians(ang)), 1)
            eq_s = f"$ sin({ang}°) = (x)/({hyp}) $"
            steps = [
                f"Set up sine ratio: $sin({ang}°) = x / {hyp}$.",
                f"Multiply by ${hyp}$: $x = {hyp} sin({ang}°)$.",
                f"Round to nearest tenth: $x approx {val}$.",
            ]
            d_a, d_b, d_c = "", "x", str(hyp)
        elif side_mode == "find_adj_from_hyp":
            hyp = rng.randint(8, 45)
            val = round(hyp * math.cos(math.radians(ang)), 1)
            eq_s = f"$ cos({ang}°) = (x)/({hyp}) $"
            steps = [
                f"Set up cosine ratio: $cos({ang}°) = x / {hyp}$.",
                f"Multiply by ${hyp}$: $x = {hyp} cos({ang}°)$.",
                f"Round to nearest tenth: $x approx {val}$.",
            ]
            d_a, d_b, d_c = "x", "", str(hyp)
        elif side_mode == "find_opp_from_adj":
            adj = rng.randint(5, 35)
            val = round(adj * math.tan(math.radians(ang)), 1)
            eq_s = f"$ tan({ang}°) = (x)/({adj}) $"
            steps = [
                f"Set up tangent ratio: $tan({ang}°) = x / {adj}$.",
                f"Multiply by ${adj}$: $x = {adj} tan({ang}°)$.",
                f"Round to nearest tenth: $x approx {val}$.",
            ]
            d_a, d_b, d_c = str(adj), "x", ""
        else:
            opp = rng.randint(5, 35)
            val = round(opp / math.sin(math.radians(ang)), 1)
            eq_s = f"$ sin({ang}°) = ({opp})/(x) $"
            steps = [
                f"Set up sine ratio: $sin({ang}°) = {opp} / x$.",
                f"Solve for $x$: $x = ({opp}) / (sin({ang}°))$.",
                f"Round to nearest tenth: $x approx {val}$.",
            ]
            d_a, d_b, d_c = "", str(opp), "x"

        return {
            "prompt_text": "Find the missing side length x of the right triangle to the nearest tenth.",
            "equation_typst": eq_s,
            "answer_typst": f"$ x approx {val} $",
            "steps_typst": steps,
            "distractors": [f"$ x approx {round(val + 3.2, 1)} $", f"$ x approx {round(abs(val - 4.1), 1)} $", f"$ x approx {round(val * 1.5, 1)} $"],
            "diagram_svg": svg_right_triangle(a_label=d_a, b_label=d_b, c_label=d_c, theta_label=f"{ang}°"),
            "answer_svg": svg_right_triangle(a_label=d_a, b_label=d_b, c_label=d_c, theta_label=f"x={val}"),
        }

    if "law of sines" in t_low and "cosines" not in t_low:
        a = rng.randint(6, 14) * scale
        A, B = rng.choice([(30, 45), (30, 60), (45, 60), (40, 65)])
        b = round(a * math.sin(math.radians(B)) / math.sin(math.radians(A)), 1)
        return {
            "prompt_text": "Use the Law of Sines to find the missing side length b to the nearest tenth.",
            "equation_typst": f"$ m angle A = {A}°, quad m angle B = {B}°, quad a = {a} $",
            "answer_typst": f"$ b approx {b} $",
            "steps_typst": [
                f"Set up the Law of Sines: $(b)/(sin B) = (a)/(sin A) arrow.r.double (b)/(sin {B}°) = ({a})/(sin {A}°)$.",
                f"Solve for $b$: $b = ({a} sin {B}°)/(sin {A}°)$.",
                f"Evaluate: $b approx {b}$.",
            ],
            "distractors": [
                f"$ b approx {round(a * math.sin(math.radians(A)) / math.sin(math.radians(B)), 1)} $",
                f"$ b approx {round(b + 3.5, 1)} $",
                f"$ b approx {a + (B - A)} $",
            ],
            "diagram_svg": svg_general_triangle(angle_a=f"{A}°", angle_b=f"{B}°", side_a=str(a), side_b="b=?"),
            "answer_svg": svg_general_triangle(angle_a=f"{A}°", angle_b=f"{B}°", side_a=str(a), side_b=f"b={b}"),
        }

    if "law of cosines" in t_low and "law of sines" not in t_low:
        a = rng.randint(5, 10) * scale
        b = rng.randint(6, 12) * scale
        c_sq = a * a + b * b - a * b
        c_side = round(math.sqrt(c_sq), 1)
        return {
            "prompt_text": "Use the Law of Cosines to find side c to the nearest tenth.",
            "equation_typst": f"$ a = {a}, quad b = {b}, quad m angle C = 60° $",
            "answer_typst": f"$ c = sqrt({c_sq}) approx {c_side} $",
            "steps_typst": [
                "Apply the Law of Cosines: $c^2 = a^2 + b^2 - 2 a b cos(C)$.",
                f"Substitute $a = {a}, b = {b}, cos(60°) = 1/2$: $c^2 = {a}^2 + {b}^2 - {a}({b}) = {c_sq}$.",
                f"Take the square root: $c = sqrt({c_sq}) approx {c_side}$.",
            ],
            "distractors": [
                f"$ c = sqrt({a * a + b * b}) approx {round(math.hypot(a, b), 1)} $",
                f"$ c = {c_sq} $",
                f"$ c = sqrt({a * a + b * b + a * b}) $",
            ],
            "diagram_svg": svg_general_triangle(side_a=str(a), side_b=str(b), side_c="c=?", angle_c="60°"),
            "answer_svg": svg_general_triangle(side_a=str(a), side_b=str(b), side_c=f"c={c_side}", angle_c="60°"),
        }

    # ------------------------------------------------------------------
    # G. MATRICES DECOUPLED SUBTOPICS (OPERATIONS, DETERMINANTS, INVERSES, EQUATIONS)
    # ------------------------------------------------------------------
    if "matrices" in c_low:
        a, b = rng.randint(1, 3 * scale), rng.randint(1, 4)
        c, d = rng.randint(1, 3), rng.randint(2, 4 * scale)
        if "determinant" in t_low:
            det = a * d - b * c
            return {
                "prompt_text": "Evaluate the determinant of the matrix.",
                "equation_typst": f"$ det mat({a}, {b}; {c}, {d}) $",
                "answer_typst": f"$ {det} $",
                "steps_typst": [
                    "For a $2 times 2$ matrix, $det(A) = a d - b c$.",
                    f"Compute $({a})({d}) - ({b})({c}) = {a * d} - {b * c}$.",
                    f"Determinant = ${det}$.",
                ],
                "distractors": [f"$ {a * d + b * c} $", f"$ {-det} $", f"$ {a + d - b - c} $"],
            }
        if "inverse" in t_low:
            target_det = rng.choice([1, -1, 2, -2])
            a = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            d = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            prod = a * d - target_det
            divs = [k for k in range(-6, 7) if k != 0 and prod % k == 0 and abs(prod // k) <= 6]
            if divs:
                b = rng.choice(divs)
                c = prod // b
            else:
                b = 1
                c = prod
            det = a * d - b * c
            det_prefix = "" if det == 1 else ("-" if det == -1 else f"(1)/({det}) ")
            return {
                "prompt_text": "Find the inverse of the 2x2 matrix.",
                "equation_typst": f"$ A = mat({a}, {b}; {c}, {d}) $",
                "answer_typst": f"$ A^(-1) = {det_prefix}mat({d}, -{b}; -{c}, {a}) $",
                "steps_typst": [
                    f"Compute the determinant: $det(A) = ({a})({d}) - ({b})({c}) = {det} != 0$.",
                    f"Swap the main diagonal entries and negate the off-diagonal entries: $mat({d}, -{b}; -{c}, {a})$.",
                    f"Multiply by $1/det(A) = 1/{det}$ to obtain the inverse.",
                ],
                "distractors": [
                    f"$ {det_prefix}mat({a}, -{b}; -{c}, {d}) $",
                    f"$ mat({d}, {b}; {c}, {a}) $",
                    f"$ (1)/({a * d + b * c if a * d + b * c != 0 else 1}) mat({d}, -{b}; -{c}, {a}) $",
                ],
            }
        if "equation" in t_low:
            x1, x2 = rng.randint(2, 6 * scale), rng.randint(-4, 5)
            return {
                "prompt_text": "Solve the matrix equation for X.",
                "equation_typst": f"$ X + mat({a}, {b}) = mat({a + x1}, {b + x2}) $",
                "answer_typst": f"$ X = mat({x1}, {x2}) $",
                "steps_typst": [
                    f"Subtract $mat({a}, {b})$ from both sides of the matrix equation.",
                    f"Subtract corresponding entries: $({a + x1} - {a}, {b + x2} - {b})$.",
                    f"Result: $X = mat({x1}, {x2})$.",
                ],
                "distractors": [
                    f"$ X = mat({a + x1 + a}, {b + x2 + b}) $",
                    f"$ X = mat({-x1}, {-x2}) $",
                    f"$ X = mat({x2}, {x1}) $",
                ],
            }
        # Matrix operations
        return {
            "prompt_text": "Perform the indicated matrix operation.",
            "equation_typst": f"$ {scale} mat({a}, {b}; {c}, {d}) + mat(1, 2; 3, 4) $",
            "answer_typst": f"$ mat({scale * a + 1}, {scale * b + 2}; {scale * c + 3}, {scale * d + 4}) $",
            "steps_typst": [
                f"Multiply first matrix by scalar ${scale}$: ${scale} mat({a}, {b}; {c}, {d}) = mat({scale * a}, {scale * b}; {scale * c}, {scale * d})$.",
                f"Add corresponding entries: $mat({scale * a} + 1, {scale * b} + 2; {scale * c} + 3, {scale * d} + 4)$.",
                f"Result: $mat({scale * a + 1}, {scale * b + 2}; {scale * c + 3}, {scale * d + 4})$.",
            ],
            "distractors": [
                f"$ mat({a + 1}, {b + 2}; {c + 3}, {d + 4}) $",
                f"$ mat({scale * (a + 1)}, {scale * (b + 2)}; {scale * (c + 3)}, {scale * (d + 4)}) $",
                f"$ mat({scale * a - 1}, {scale * b - 2}; {scale * c - 3}, {scale * d - 4}) $",
            ],
        }

    # ------------------------------------------------------------------
    # H. VECTORS DECOUPLED SUBTOPICS (BASICS, OPERATIONS, DOT PRODUCTS)
    # ------------------------------------------------------------------
    if "vectors" in c_low:
        ux, uy = rng.randint(1, 3 * scale), rng.randint(2, 4 * scale)
        vx, vy = rng.randint(-3, 4), rng.randint(1, 5)
        if "dot product" in t_low:
            dp = ux * vx + uy * vy
            return {
                "prompt_text": "Find the dot product u . v of the two vectors.",
                "equation_typst": f"$ bold(u) = chevron.l {ux}, {uy} chevron.r, quad bold(v) = chevron.l {vx}, {vy} chevron.r $",
                "answer_typst": f"$ bold(u) dot bold(v) = {dp} $",
                "steps_typst": [
                    "Use the dot product formula $bold(u) dot bold(v) = u_1 v_1 + u_2 v_2$.",
                    f"Multiply corresponding components: $({ux})({vx}) + ({uy})({vy}) = {ux * vx} + {uy * vy}$.",
                    f"Sum: ${dp}$.",
                ],
                "distractors": [
                    f"$ chevron.l {ux * vx}, {uy * vy} chevron.r $",
                    f"$ {ux * vy - uy * vx} $",
                    f"$ {dp + ux} $",
                ],
            }
        if "operations" in t_low:
            rx, ry = scale * ux + vx, scale * uy + vy
            return {
                "prompt_text": "Perform the vector operation and write the result in component form.",
                "equation_typst": f"$ {scale}bold(u) + bold(v) quad \"for\" bold(u) = chevron.l {ux}, {uy} chevron.r, bold(v) = chevron.l {vx}, {vy} chevron.r $",
                "answer_typst": f"$ chevron.l {rx}, {ry} chevron.r $",
                "steps_typst": [
                    f"Scale vector $bold(u)$: ${scale}bold(u) = chevron.l {scale * ux}, {scale * uy} chevron.r$.",
                    f"Add components of $bold(v)$: $chevron.l {scale * ux} + ({vx}), {scale * uy} + ({vy}) chevron.r$.",
                    f"Result: $chevron.l {rx}, {ry} chevron.r$.",
                ],
                "distractors": [
                    f"$ chevron.l {ux + vx}, {uy + vy} chevron.r $",
                    f"$ chevron.l {scale * ux - vx}, {scale * uy - vy} chevron.r $",
                    f"$ chevron.l {ry}, {rx} chevron.r $",
                ],
            }

    # ------------------------------------------------------------------
    # I. RADICALS DECOUPLED SUBTOPICS
    # ------------------------------------------------------------------
    if "radical" in c_low or "square roots" in t_low:
        k = rng.choice([2, 3, 5, 6, 7])
        a = rng.randint(2, 3 + scale)
        b = rng.randint(1, 3 + scale)
        if "adding and subtracting" in t_low:
            ans_c = a + b
            return {
                "prompt_text": "Simplify each radical expression by adding or subtracting like radicals.",
                "equation_typst": f"$ {a}sqrt({k}) + {b}sqrt({k}) $" if scale == 1 else f"$ sqrt({a * a * k}) + {b}sqrt({k}) $",
                "answer_typst": f"$ {ans_c}sqrt({k}) $",
                "steps_typst": [
                    f"Simplify each radical so both have radicand ${k}$: ${a}sqrt({k}) + {b}sqrt({k})$.",
                    f"Combine coefficients of like radicals: $({a} + {b})sqrt({k})$.",
                    f"Result: ${ans_c}sqrt({k})$.",
                ],
                "distractors": [
                    f"$ {ans_c}sqrt({2 * k}) $",
                    f"$ {a * b}sqrt({k}) $",
                    f"$ {abs(a - b)}sqrt({k}) $",
                ],
            }
        if "multiplying" in t_low:
            return {
                "prompt_text": "Multiply and simplify the radical expression.",
                "equation_typst": f"$ ({a}sqrt({k}))({b}sqrt({k})) $",
                "answer_typst": f"$ {a * b * k} $",
                "steps_typst": [
                    f"Multiply the coefficients and radicands: $({a} dot {b}) sqrt({k} dot {k})$.",
                    f"Since $sqrt({k}^2) = {k}$, compute ${a * b} times {k}$.",
                    f"Result: ${a * b * k}$.",
                ],
                "distractors": [f"$ {a * b}sqrt({k}) $", f"$ {(a + b) * k} $", f"$ {a * b * k * k} $"],
            }
        if "dividing" in t_low:
            return {
                "prompt_text": "Divide and rationalize the denominator.",
                "equation_typst": f"$ ({a * k})/(sqrt({k})) $",
                "answer_typst": f"$ {a}sqrt({k}) $",
                "steps_typst": [
                    f"Multiply numerator and denominator by $sqrt({k})$: $({a * k}sqrt({k})) / ({k})$.",
                    f"Divide out the common factor ${k}$.",
                    f"Simplified form: ${a}sqrt({k})$.",
                ],
                "distractors": [f"$ ({a})/(sqrt({k})) $", f"$ {a * k}sqrt({k}) $", f"$ {a * k} $"],
            }
        if "equation" in t_low and "graph" not in t_low:
            sol = a * a - b
            return {
                "prompt_text": "Solve the radical equation and check for extraneous solutions.",
                "equation_typst": f"$ sqrt(x + {b}) = {a} $",
                "answer_typst": f"$ x = {sol} $",
                "steps_typst": [
                    f"Square both sides of the equation: $x + {b} = {a}^2 = {a * a}$.",
                    f"Subtract ${b}$: $x = {sol}$.",
                    f"Check: $sqrt({sol} + {b}) = sqrt({a * a}) = {a}$ (valid).",
                ],
                "distractors": [f"$ x = {a - b} $", f"$ x = {a * a + b} $", "$ \"No solution\" $"],
            }
        if "simplifying" in t_low:
            n = a * a * k
            return {
                "prompt_text": "Simplify the radical expression completely.",
                "equation_typst": f"$ sqrt({n}) $",
                "answer_typst": f"$ {a}sqrt({k}) $",
                "steps_typst": [
                    f"Factor ${n}$ using its largest perfect square factor: ${n} = {a * a} times {k}$.",
                    f"Apply the product property: $sqrt({a * a}) dot sqrt({k})$.",
                    f"Simplify: ${a}sqrt({k})$.",
                ],
                "distractors": [f"$ {k}sqrt({a}) $", f"$ {a * a}sqrt({k}) $", f"$ {a + k} $"],
            }

    # ------------------------------------------------------------------
    # J. RATIONAL EXPRESSIONS DECOUPLED SUBTOPICS
    # ------------------------------------------------------------------
    if "rational expression" in c_low:
        r1 = rng.randint(1, 3 + scale)
        r2 = rng.randint(r1 + 1, r1 + 4)
        if "complex fractions" in t_low:
            c1 = rng.randint(2, 9)
            c2 = rng.randint(2, 9)
            return {
                "prompt_text": "Simplify the complex fraction.",
                "equation_typst": f"$ ((1)/(x) + ({c1})/({c2})) / ((1)/(x) - ({c1})/({c2})) $",
                "answer_typst": f"$ ({c2} + {c1}x)/({c2} - {c1}x), quad x != 0, {c2}/{c1} $",
                "steps_typst": [
                    f"Multiply the numerator and denominator by the LCD ${c2}x$.",
                    f"Numerator becomes ${c2} + {c1}x$ and denominator becomes ${c2} - {c1}x$.",
                    f"Result: $({c2} + {c1}x)/({c2} - {c1}x)$ for $x != 0, {c2}/{c1}$.",
                ],
                "distractors": [
                    f"$ ({c2} - {c1}x)/({c2} + {c1}x) $",
                    "$ -1 $",
                    f"$ ({c1}x + {c2})/({c1}x - {c2}) $",
                ],
            }
        if "equations" in t_low:
            # r1 / x + 1 = (r1 + x) / x = r2 -> r1 = (r2 - 1)x
            k = rng.randint(2, 4)
            sol = r1
            rhs = k + 1
            num = k * sol
            return {
                "prompt_text": "Solve the rational equation and check for excluded values.",
                "equation_typst": f"$ ({num})/(x) + 1 = {rhs} $",
                "answer_typst": f"$ x = {sol} $",
                "steps_typst": [
                    "Note the excluded value $x != 0$.",
                    f"Subtract $1$ from both sides: $({num})/(x) = {k}$.",
                    f"Solve for $x$: $x = {num}/{k} = {sol}$.",
                ],
                "distractors": [f"$ x = {num} $", f"$ x = {-sol} $", "$ \"No solution\" $"],
            }
        if "adding and subtracting" in t_low:
            return {
                "prompt_text": "Add or subtract the rational expressions and state excluded values.",
                "equation_typst": f"$ (2)/(x - {r1}) + (3)/(x + {r2}) $",
                "answer_typst": f"$ (5x + {2 * r2 - 3 * r1})/((x - {r1})(x + {r2})), quad x != {r1}, -{r2} $",
                "steps_typst": [
                    f"The LCD is $(x - {r1})(x + {r2})$.",
                    f"Rewrite numerators over the LCD: $2(x + {r2}) + 3(x - {r1}) = 5x + ({2 * r2 - 3 * r1})$.",
                    f"Combine over $(x - {r1})(x + {r2})$ with $x != {r1}, -{r2}$.",
                ],
                "distractors": [
                    f"$ (5)/(2x + {r2 - r1}) $",
                    f"$ (5x - {2 * r2 - 3 * r1})/((x - {r1})(x + {r2})) $",
                    f"$ (6)/((x - {r1})(x + {r2})) $",
                ],
            }
        if "multiplying and dividing" in t_low:
            return {
                "prompt_text": "Multiply or divide the rational expressions and state excluded values.",
                "equation_typst": f"$ (x - {r1})/(x + {r2}) dot (x + {r2})/(x + {r1}) $",
                "answer_typst": f"$ (x - {r1})/(x + {r1}), quad x != -{r1}, -{r2} $",
                "steps_typst": [
                    f"Identify excluded values from all denominators: $x != -{r2}, -{r1}$.",
                    f"Cancel the common factor $(x + {r2})$.",
                    f"Simplified product: $(x - {r1})/(x + {r1})$.",
                ],
                "distractors": [
                    "$ 1 $",
                    f"$ (x + {r1})/(x - {r1}) $",
                    f"$ (x - {r1})/(x + {r2}) $",
                ],
            }

    # ------------------------------------------------------------------
    # K. INEQUALITIES DECOUPLED BY STEP COUNT (WITH NUMBER LINE SVGS)
    # ------------------------------------------------------------------
    if "one-step inequalities" in t_low or "solving and graphing one-step" in t_low:
        a = rng.randint(2, 6 * scale)
        sol = rng.randint(-5, 6)
        rhs = sol + a
        return {
            "prompt_text": "Solve the one-step inequality and graph its solution on the number line.",
            "equation_typst": f"$ x + {a} >= {rhs} $",
            "answer_typst": f"$ x >= {sol} $",
            "steps_typst": [
                f"Subtract ${a}$ from both sides of the inequality.",
                f"Compute ${rhs} - {a} = {sol}$: $x >= {sol}$.",
                f"Plot a closed circle at ${sol}$ and shade to the right.",
            ],
            "distractors": [f"$ x <= {sol} $", f"$ x >= {rhs + a} $", f"$ x > {sol} $"],
            "diagram_svg": svg_number_line(),
            "answer_svg": svg_number_line(rays=[(sol, "right", True)]),
        }

    if "two-step inequalities" in t_low:
        a = rng.randint(2, 4 * scale)
        b = rng.randint(1, 9)
        sol = rng.randint(-4, 5)
        rhs = a * sol + b
        return {
            "prompt_text": "Solve the two-step inequality and graph its solution on the number line.",
            "equation_typst": f"$ {a}x + {b} < {rhs} $",
            "answer_typst": f"$ x < {sol} $",
            "steps_typst": [
                f"Subtract ${b}$ from both sides: ${a}x < {rhs - b}$.",
                f"Divide both sides by ${a}$: $x < {sol}$.",
                f"Plot an open circle at ${sol}$ and shade to the left.",
            ],
            "distractors": [f"$ x > {sol} $", f"$ x <= {sol} $", f"$ x < {sol + 2} $"],
            "diagram_svg": svg_number_line(),
            "answer_svg": svg_number_line(rays=[(sol, "left", False)]),
        }

    if "multi-step inequalities" in t_low:
        a = rng.randint(2, 3 + scale)
        b = rng.randint(1, 5)
        sol = rng.randint(-4, 5)
        rhs = a * (sol + b)
        return {
            "prompt_text": "Solve the multi-step inequality and graph its solution on the number line.",
            "equation_typst": f"$ {a}(x + {b}) <= {rhs} $",
            "answer_typst": f"$ x <= {sol} $",
            "steps_typst": [
                f"Distribute ${a}$: ${a}x + {a * b} <= {rhs}$.",
                f"Subtract ${a * b}$ from both sides: ${a}x <= {rhs - a * b}$.",
                f"Divide by ${a}$: $x <= {sol}$.",
            ],
            "distractors": [f"$ x >= {sol} $", f"$ x <= {sol + b} $", f"$ x < {sol} $"],
            "diagram_svg": svg_number_line(),
            "answer_svg": svg_number_line(rays=[(sol, "left", True)]),
        }

    # ------------------------------------------------------------------
    # L. FACTORS & MULTIPLES DECOUPLED (PRIME FACTORIZATION, GCF, LCM, WORD PROBLEMS)
    # ------------------------------------------------------------------
    if c_low == "common factors and common multiples":
        p = rng.choice([2, 3, 5])
        n1 = p * rng.choice([4, 6, 8]) * scale
        n2_pool = [x for x in [6, 9, 10, 12, 14, 15] if p * x * scale != n1]
        n2 = p * rng.choice(n2_pool) * scale
        g_val = math.gcd(n1, n2)
        l_val = math.lcm(n1, n2)
        def _calc_pfactors(val: int) -> list[int]:
            res_facs = []
            cur_d = 2
            temp_v = val
            while cur_d * cur_d <= temp_v:
                while temp_v % cur_d == 0:
                    res_facs.append(cur_d)
                    temp_v //= cur_d
                cur_d += 1
            if temp_v > 1:
                res_facs.append(temp_v)
            return res_facs

        if "greatest common factor" in t_low:
            pf1_str = " times ".join(str(x) for x in _calc_pfactors(n1))
            pf2_str = " times ".join(str(x) for x in _calc_pfactors(n2))
            return {
                "prompt_text": "Find the greatest common factor (GCF) of the given numbers.",
                "equation_typst": f"$ \"GCF\"({n1}, {n2}) $",
                "answer_typst": f"$ {g_val} $",
                "steps_typst": [
                    f"Prime factorization of ${n1}$: ${pf1_str}$.",
                    f"Prime factorization of ${n2}$: ${pf2_str}$.",
                    f"Multiply common prime factors: $\"GCF\"({n1}, {n2}) = {g_val}$.",
                ],
                "distractors": [f"$ {l_val} $", f"$ {g_val * 2} $", f"$ {max(1, g_val // 2)} $"],
            }
        if "least common multiple" in t_low:
            return {
                "prompt_text": "Find the least common multiple (LCM) of the given numbers.",
                "equation_typst": f"$ \"LCM\"({n1}, {n2}) $",
                "answer_typst": f"$ {l_val} $",
                "steps_typst": [
                    f"Find the GCF of ${n1}$ and ${n2}$, which is ${g_val}$.",
                    f"Use $\"LCM\"(a, b) = (a times b) / \"GCF\" = ({n1} times {n2}) / {g_val}$.",
                    f"Least Common Multiple = ${l_val}$.",
                ],
                "distractors": [f"$ {g_val} $", f"$ {n1 * n2} $", f"$ {l_val + n1} $"],
            }

    # ------------------------------------------------------------------
    # M. GEOMETRY TRIANGLES, ANGLES, CIRCLES DECOUPLED SUBTOPICS
    # ------------------------------------------------------------------
    if "classifying triangles" in t_low:
        kind = rng.choice(["equilateral", "iso_acute", "iso_right", "iso_obtuse", "scal_right", "scal_acute", "scal_obtuse"])
        if kind == "equilateral":
            a, b, c = 60, 60, 60
        elif kind == "iso_acute":
            b_ang = rng.choice([48, 50, 52, 54, 55, 65, 70, 72, 75, 80])
            a, b, c = b_ang, b_ang, 180 - 2 * b_ang
        elif kind == "iso_right":
            a, b, c = 45, 45, 90
        elif kind == "iso_obtuse":
            v_ang = rng.choice([96, 100, 104, 110, 116, 120, 130, 140])
            a, b, c = (180 - v_ang) // 2, (180 - v_ang) // 2, v_ang
        elif kind == "scal_right":
            a_ang = rng.choice([20, 25, 30, 35, 40, 50, 55, 60, 65, 70])
            a, b, c = a_ang, 90 - a_ang, 90
        elif kind == "scal_acute":
            a = rng.choice([40, 45, 50, 55])
            b = rng.choice([x for x in [55, 60, 65, 70] if x != a])
            c = 180 - a - b
        else:
            c = rng.choice([95, 100, 105, 115, 120, 125, 135])
            rem = 180 - c
            a = rng.randint(15, rem - 20)
            b = rem - a
        angs = [a, b, c]
        rng.shuffle(angs)
        a, b, c = angs
        ang_type = "Equiangular" if a == b == c else ("Right" if 90 in (a, b, c) else ("Obtuse" if max(a, b, c) > 90 else "Acute"))
        side_type = "Equilateral" if a == b == c else ("Isosceles" if len({a, b, c}) == 2 else "Scalene")
        return {
            "prompt_text": "Classify the triangle by its angles and by its sides.",
            "equation_typst": f"$ m angle A = {a}°, quad m angle B = {b}°, quad m angle C = {c}° $",
            "answer_typst": f"$ \"{ang_type} {side_type.lower()} triangle\" $",
            "steps_typst": [
                f"Examine the largest angle (${max(a, b, c)}°$) to classify by angles: {ang_type}.",
                f"Count equal angles/sides to classify by sides: {side_type}.",
                f"Classification: {ang_type} {side_type.lower()} triangle.",
            ],
            "distractors": [
                f"$ \"{'Obtuse' if ang_type != 'Obtuse' else 'Acute'} {side_type.lower()} triangle\" $",
                f"$ \"{ang_type} {'isosceles' if side_type != 'Isosceles' else 'scalene'} triangle\" $",
                "$ \"Right equilateral triangle\" $",
            ],
            "diagram_svg": svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", angle_c=f"{c}°"),
            "answer_svg": svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", angle_c=f"{c}°", side_b=f"{ang_type} {side_type}"),
        }

    if "triangle angle sum" in t_low:
        a = rng.randint(35, 75)
        b = rng.randint(35, 75)
        c = 180 - a - b
        if scale >= 2:
            xv = rng.randint(8, 18)
            k = 3 if scale == 2 else 4
            const = c - k * xv
            c_expr = f"{k}x {'+ ' + str(const) if const >= 0 else '- ' + str(abs(const))}"
            return {
                "prompt_text": "Use the Triangle Angle-Sum Theorem to solve for x and find m angle C.",
                "equation_typst": f"$ m angle A = {a}°, quad m angle B = {b}°, quad m angle C = ({c_expr})° $",
                "answer_typst": f"$ x = {xv}, quad m angle C = {c}° $",
                "steps_typst": [
                    f"By the Triangle Angle-Sum Theorem, ${a} + {b} + ({c_expr}) = 180$.",
                    f"Simplify: ${k}x = {k * xv} arrow.r.double x = {xv}$.",
                    f"Therefore, $m angle C = {c}°$.",
                ],
                "distractors": [f"$ x = {xv + 2}, quad m angle C = {c}° $", f"$ x = {c}, quad m angle C = {xv}° $", f"$ x = {xv - 2}, quad m angle C = {180 - a}° $"],
                "diagram_svg": svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", angle_c=c_expr),
                "answer_svg": svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", angle_c=f"x={xv}, {c}°"),
            }
        return {
            "prompt_text": "Find the measure of the third angle C in triangle ABC.",
            "equation_typst": f"$ m angle A = {a}°, quad m angle B = {b}° $",
            "answer_typst": f"$ m angle C = {c}° $",
            "steps_typst": [
                "By the Triangle Angle-Sum Theorem, $m angle A + m angle B + m angle C = 180°$.",
                f"Add the known angles: ${a}° + {b}° = {a + b}°$.",
                f"Subtract from $180°$: $m angle C = 180° - {a + b}° = {c}°$.",
            ],
            "distractors": [f"$ m angle C = {a + b}° $", f"$ m angle C = {abs(90 - a)}° $", f"$ m angle C = {c + 10}° $"],
            "diagram_svg": svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", angle_c="?"),
            "answer_svg": svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", angle_c=f"{c}°"),
        }

    if "exterior angle theorem" in t_low:
        a = rng.randint(35, 70)
        b = rng.randint(40, 75)
        ext = a + b
        if scale > 1:
            ext_expr = f"{scale}x + {ext - scale * 15}"
            eq_text = f"Remote interior angles: {a}° and {b}°. Exterior angle: ${ext_expr}°$."
            ans_typst = f"$ x = 15, quad \"Exterior angle\" = {ext}° $"
            diag = svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", ext_c=f"{ext_expr}°")
            ans_diag = svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", ext_c=f"{ext}°")
        else:
            eq_text = f"Remote interior angles: {a}° and {b}°. Find the exterior angle."
            ans_typst = f"$ \"Exterior angle\" = {ext}° $"
            diag = svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", ext_c="?")
            ans_diag = svg_general_triangle(angle_a=f"{a}°", angle_b=f"{b}°", ext_c=f"{ext}°")
        return {
            "prompt_text": "Use the Exterior Angle Theorem to find the exterior angle measure (or solve for x).",
            "equation_typst": eq_text,
            "answer_typst": ans_typst,
            "steps_typst": [
                "By the Exterior Angle Theorem, an exterior angle of a triangle equals the sum of its two remote interior angles.",
                f"Sum the remote interior angles: ${a}° + {b}° = {ext}°$.",
                f"Result: Exterior angle = ${ext}°$" + (", $x = 15$." if scale > 1 else "."),
            ],
            "distractors": [
                f"$ \"Exterior angle\" = {180 - ext}° $",
                f"$ \"Exterior angle\" = {abs(a - b)}° $",
                f"$ \"Exterior angle\" = {ext + 10}° $",
            ],
            "diagram_svg": diag,
            "answer_svg": ans_diag,
        }

    if "angle addition postulate" in t_low:
        a1 = rng.randint(22, 65) * (1 if scale == 1 else 1)
        a2 = rng.randint(25, 75)
        tot = a1 + a2
        return {
            "prompt_text": "Ray BD lies in the interior of angle ABC. Use the Angle Addition Postulate to find the missing angle.",
            "equation_typst": f"$ m angle A B D = {a1}°, quad m angle D B C = {a2}°, quad \"find \" m angle A B C $",
            "answer_typst": f"$ m angle A B C = {tot}° $",
            "steps_typst": [
                "By the Angle Addition Postulate, $m angle A B D + m angle D B C = m angle A B C$.",
                f"Substitute the given measures: ${a1}° + {a2}° = {tot}°$.",
                f"Answer: $m angle A B C = {tot}°$.",
            ],
            "distractors": [f"$ m angle A B C = {abs(a1 - a2)}° $", f"$ m angle A B C = {180 - tot}° $", f"$ m angle A B C = {tot + 10}° $"],
            "diagram_svg": svg_angle_diagram(angle_degrees=a2, interior_angle=a1, mode="interior_ray", angle_label=f"{a2}°", interior_angle_label=f"{a1}°"),
            "answer_svg": svg_angle_diagram(angle_degrees=a2, interior_angle=a1, mode="interior_ray", angle_label=f"{a2}°", interior_angle_label=f"{a1}°", shade=True, bottom_label=f"m∠ABC = {tot}°"),
        }

    if "naming arcs" in t_low or "measures of arcs" in t_low:
        central = rng.randint(45, 145)
        major = 360 - central
        return {
            "prompt_text": "Given the central angle of circle O, find the measure of minor arc AB and major arc ACB.",
            "equation_typst": f"$ m angle A O B = {central}° $",
            "answer_typst": f"$ m \"arc\"(A B) = {central}°, quad m \"arc\"(A C B) = {major}° $",
            "steps_typst": [
                f"The measure of a minor arc equals its central angle: $m \"arc\"(A B) = {central}°$.",
                f"The measure of the corresponding major arc is $360° - {central}° = {major}°$.",
                f"Minor arc = ${central}°$, Major arc = ${major}°$.",
            ],
            "distractors": [
                f"$ m \"arc\"(A B) = {central // 2}°, quad m \"arc\"(A C B) = {180 - central}° $",
                f"$ m \"arc\"(A B) = {major}°, quad m \"arc\"(A C B) = {central}° $",
                f"$ m \"arc\"(A B) = {2 * central}°, quad m \"arc\"(A C B) = {360 - 2 * central}° $",
            ],
            "diagram_svg": svg_circle_diagram(angle_degrees=central, angle_label=f"{central}°", show_points=True),
            "answer_svg": svg_circle_diagram(
                angle_degrees=central,
                angle_label=f"Minor: {central}°, Major: {major}°",
                shade_sector=True,
                show_points=True,
            ),
        }

    if "arc length and sector area" in t_low:
        r = rng.randint(3, 45)
        theta = rng.choice([15 * k for k in range(1, 24)])
        arc_f = Fraction(theta * 2 * r, 360)
        sec_f = Fraction(theta * r * r, 360)
        return {
            "prompt_text": "Find the exact arc length s and sector area A of the circle.",
            "equation_typst": f"$ r = {r}, quad theta = {theta}° $",
            "answer_typst": f"$ s = {_fmt_frac(arc_f)} pi, quad A = {_fmt_frac(sec_f)} pi $",
            "steps_typst": [
                f"Arc length: $s = (theta / 360°) dot 2 pi r = ({theta} / 360) dot 2 pi ({r}) = {_fmt_frac(arc_f)} pi$.",
                f"Sector area: $A = (theta / 360°) dot pi r^2 = ({theta} / 360) dot pi ({r}^2) = {_fmt_frac(sec_f)} pi$.",
                f"Result: $s = {_fmt_frac(arc_f)} pi, A = {_fmt_frac(sec_f)} pi$.",
            ],
            "distractors": [
                f"$ s = {_fmt_frac(sec_f)} pi, quad A = {_fmt_frac(arc_f)} pi $",
                f"$ s = {2 * r} pi, quad A = {r * r} pi $",
                f"$ s = {_fmt_frac(arc_f * 2)} pi, quad A = {_fmt_frac(sec_f * 2)} pi $",
            ],
            "diagram_svg": svg_circle_diagram(radius_label=f"r = {r}", angle_label=f"{theta}°", shade_sector=True),
            "answer_svg": svg_circle_diagram(radius_label=f"s = {arc_f}pi", angle_label=f"A = {sec_f}pi", shade_sector=True),
        }
    # ------------------------------------------------------------------
    # N. LOGARITHMS & EXPONENTIAL EQUATIONS DECOUPLED SUBTOPICS
    # ------------------------------------------------------------------
    if "logarithm" in c_low or "logarithm" in t_low or "compound interest" in t_low:
        base = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        if "evaluating logarithms" in t_low:
            mode_eval = rng.choice(["int_pos", "int_neg", "fractional"])
            if mode_eval == "int_pos":
                k_exp = rng.randint(1, 6)
                arg_val = base ** k_exp
                ans_str = str(k_exp)
                step_exp = f"{base}^{k_exp} = {arg_val}"
                arg_s = str(arg_val)
            elif mode_eval == "int_neg":
                k_exp = rng.randint(1, 4)
                denom = base ** k_exp
                ans_str = str(-k_exp)
                step_exp = f"{base}^(-{k_exp}) = 1/{denom}"
                arg_s = f"(1)/({denom})"
            else:
                k_exp = rng.choice([2, 3, 4])
                ans_str = f"1/{k_exp}"
                step_exp = f"{base}^(1/{k_exp}) = root({k_exp}, {base})"
                arg_s = f"root({k_exp}, {base})"

            return {
                "prompt_text": "Evaluate the logarithm without a calculator.",
                "equation_typst": f"$ log_({base})({arg_s}) $",
                "answer_typst": f"$ {ans_str} $",
                "steps_typst": [
                    f"Ask: to what power must base ${base}$ be raised to equal ${arg_s}$?",
                    f"Express ${arg_s}$ as a power of base ${base}$: ${step_exp}$.",
                    f"Therefore, $log_({base})({arg_s}) = {ans_str}$.",
                ],
                "distractors": [f"$ {base} $", f"$ {ans_str} + 1 $", "$ 0 $"],
            }

        if "not requiring logarithms" in t_low:
            sol = rng.randint(1, 20)
            offset = rng.randint(1, 8)
            rhs_exp = sol + offset
            return {
                "prompt_text": "Solve the exponential equation by rewriting both sides with a common base.",
                "equation_typst": f"$ {base}^(x {'+' if offset >= 0 else '-'} {abs(offset)}) = {base ** rhs_exp} $",
                "answer_typst": f"$ x = {sol} $",
                "steps_typst": [
                    f"Express the right-hand side with base ${base}$: ${base}^{rhs_exp}$.",
                    f"Set exponents equal: $x {'+' if offset >= 0 else '-'} {abs(offset)} = {rhs_exp}$.",
                    f"Solve for $x$: $x = {rhs_exp} - {offset} = {sol}$.",
                ],
                "distractors": [f"$ x = {sol + 1} $", f"$ x = {sol - 1} $", f"$ x = {rhs_exp} $"],
            }

        if "requiring logarithms" in t_low:
            rhs = rng.randint(15, 300)
            approx = round(math.log(rhs) / math.log(base), 3)
            return {
                "prompt_text": "Solve the exponential equation using logarithms. Give both the exact form and decimal approximation.",
                "equation_typst": f"$ {base}^x = {rhs} $",
                "answer_typst": f"$ x = (ln({rhs}))/(ln({base})) approx {approx} $",
                "steps_typst": [
                    f"Take natural logarithms: $ln({base}^x) = ln({rhs})$.",
                    f"Power rule: $x ln({base}) = ln({rhs})$.",
                    f"Solve for $x$: $x = ln({rhs}) / ln({base}) approx {approx}$.",
                ],
                "distractors": [f"$ x = ln({rhs}) $", f"$ x = {round(approx + 1, 3)} $", f"$ x = {rhs // base} $"],
            }

        if "compound interest" in t_low:
            p_princ = rng.choice([500, 1000, 2000, 5000, 10000, 15000, 25000])
            r_pct = rng.choice([2, 3, 4, 5, 6, 7, 8])
            t_yrs = rng.randint(2, 20)
            n_freq = rng.choice([(1, "annually"), (2, "semiannually"), (4, "quarterly"), (12, "monthly")])
            m_comp, desc = n_freq
            amt = round(p_princ * ((1 + (r_pct / 100) / m_comp) ** (m_comp * t_yrs)), 2)
            return {
                "prompt_text": f"Find the final account balance for an investment compounded {desc}.",
                "equation_typst": f"$ P = \\${p_princ}, quad r = {r_pct}%, quad t = {t_yrs} \" years\", quad \"compounded \" {desc} $",
                "answer_typst": rf"$ A = \${amt:,.2f} $",
                "steps_typst": [
                    f"Use compound interest formula $A = P(1 + r/n)^(n t)$ with $n = {m_comp}$.",
                    rf"Substitute: $\${p_princ}(1 + {r_pct / 100}/{m_comp})^({m_comp} times {t_yrs})$.",
                    rf"Compute final balance: $A = \${amt:,.2f}$.",
                ],
                "distractors": [rf"$ A = \${amt + 100:,.2f} $", rf"$ A = \${p_princ * (1 + (r_pct * t_yrs)/100):,.2f} $", rf"$ A = \${amt * 1.1:,.2f} $"],
            }
    # ------------------------------------------------------------------
    # O. SLOPE FROM A GRAPH VS SLOPE FROM TWO POINTS
    # ------------------------------------------------------------------
    if "finding slope from a graph" in t_low:
        m = rng.choice([-3, -2, -1, 1, 2, 3]) * scale
        b = rng.randint(-3, 3)
        return {
            "prompt_text": "Find the slope of the line shown on the coordinate plane.",
            "equation_typst": f"\"Line passing through \" (0, {b}) \" and \" (1, {m + b})",
            "answer_typst": f"$ m = {m} $",
            "steps_typst": [
                f"Pick two lattice points on the graphed line: $(0, {b})$ and $(1, {m + b})$.",
                f"Count the vertical rise (${m}$) and horizontal run ($1$).",
                f"Slope $m = \"rise\" / \"run\" = {m}$.",
            ],
            "distractors": [f"$ m = {-m} $", f"$ m = 1/({m}) $", f"$ m = {b} $"],
            "diagram_svg": svg_coordinate_plane(lines=[{"m": m, "b": b, "color": "#2563eb"}], points=[(0, b, "", True), (1, m + b, "", True)]),
            "answer_svg": svg_coordinate_plane(lines=[{"m": m, "b": b, "color": "#2563eb"}], points=[(0, b, f"(0,{b})", True), (1, m + b, f"m={m}", True)]),
        }

    # ------------------------------------------------------------------
    # P. PYTHAGOREAN THEOREM & SPECIAL RIGHT TRIANGLES (WITH RIGHT TRIANGLE SVGS)
    # ------------------------------------------------------------------
    if "pythagorean" in t_low:
        triples = [
            (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15),
            (12, 16, 20), (6, 8, 10), (10, 24, 26), (15, 20, 25), (9, 40, 41),
            (11, 60, 61), (12, 35, 37), (13, 84, 85), (16, 63, 65), (20, 21, 29),
            (28, 45, 53), (33, 56, 65), (36, 77, 85), (39, 80, 89), (48, 55, 73),
        ]
        a0, b0, c0 = rng.choice(triples)
        mult = rng.choice([1, 2, 3])
        a, b, c = a0 * mult, b0 * mult, c0 * mult
        if "multi-step" in t_low or scale == 3:
            # Find missing leg b given a and c, then find area or perimeter
            perim = a + b + c
            return {
                "prompt_text": "Use the Pythagorean Theorem to find the missing leg b and the perimeter of the right triangle.",
                "equation_typst": f"$ a = {a}, quad c = {c}, quad \"find \" b \" and Perimeter\" $",
                "answer_typst": f"$ b = {b}, quad P = {perim} $",
                "steps_typst": [
                    f"Use $a^2 + b^2 = c^2$: ${a}^2 + b^2 = {c}^2 arrow.r.double b^2 = {c * c - a * a} = {b * b}$.",
                    f"Take the positive square root: $b = {b}$.",
                    f"Compute the perimeter: $P = {a} + {b} + {c} = {perim}$.",
                ],
                "distractors": [
                    f"$ b = {c - a}, quad P = {2 * c} $",
                    f"$ b = {b}, quad P = {a * b // 2} $",
                    f"$ b = {b + 2}, quad P = {perim + 2} $",
                ],
                "diagram_svg": svg_right_triangle(a_label=str(a), b_label="b=?", c_label=str(c)),
                "answer_svg": svg_right_triangle(a_label=str(a), b_label=f"b={b}", c_label=str(c), theta_label=f"P={perim}"),
            }
        return {
            "prompt_text": "Use the Pythagorean Theorem to find the missing side length of the right triangle.",
            "equation_typst": f"$ a = {a}, quad b = {b}, quad c = ? $",
            "answer_typst": f"$ c = {c} $",
            "steps_typst": [
                "Apply the Pythagorean Theorem: $a^2 + b^2 = c^2$.",
                f"Substitute the legs: ${a}^2 + {b}^2 = {a * a} + {b * b} = {c * c}$.",
                f"Take the square root: $c = sqrt({c * c}) = {c}$.",
            ],
            "distractors": [f"$ c = {a + b} $", f"$ c = {c * c} $", f"$ c = {abs(b - a)} $"],
            "diagram_svg": svg_right_triangle(a_label=str(a), b_label=str(b), c_label="c=?"),
            "answer_svg": svg_right_triangle(a_label=str(a), b_label=str(b), c_label=f"c={c}"),
        }

    if "special right triangle" in t_low:
        sub_type = rng.choice(["45_45_90_leg", "45_45_90_hyp", "30_60_90_short", "30_60_90_long", "30_60_90_hyp"])
        leg_val = rng.randint(2, 28)
        if sub_type == "45_45_90_leg":
            return {
                "prompt_text": "Find the hypotenuse c of the 45-45-90 special right triangle.",
                "equation_typst": f"$ \"45\"°\"-45\"°\"-90\"° \" triangle with leg \" a = {leg_val} $",
                "answer_typst": f"$ c = {leg_val}sqrt(2) $",
                "steps_typst": [
                    "In a $45°$-$45°$-$90°$ triangle, sides are in ratio $1 : 1 : sqrt(2)$.",
                    f"Multiply leg length by $sqrt(2)$: $c = a sqrt(2) = {leg_val}sqrt(2)$.",
                    f"Hypotenuse: $c = {leg_val}sqrt(2)$.",
                ],
                "distractors": [f"$ c = {2 * leg_val} $", f"$ c = {leg_val}sqrt(3) $", f"$ c = {leg_val} $"],
                "diagram_svg": svg_right_triangle(a_label=str(leg_val), b_label=str(leg_val), c_label="c=?", theta_label="45°"),
                "answer_svg": svg_right_triangle(a_label=str(leg_val), b_label=str(leg_val), c_label=f"{leg_val}sqrt(2)", theta_label="45°"),
            }
        elif sub_type == "45_45_90_hyp":
            hyp_even = leg_val * 2
            return {
                "prompt_text": "Find the leg length a of the 45-45-90 special right triangle given hypotenuse c.",
                "equation_typst": f"$ \"45\"°\"-45\"°\"-90\"° \" triangle with hypotenuse \" c = {hyp_even} $",
                "answer_typst": f"$ a = {leg_val}sqrt(2) $",
                "steps_typst": [
                    "In a $45°$-$45°$-$90°$ triangle, $c = a sqrt(2) ==> a = c / sqrt(2)$.",
                    f"Rationalize the denominator: $a = ({hyp_even} sqrt(2)) / 2 = {leg_val}sqrt(2)$.",
                    f"Leg length: $a = {leg_val}sqrt(2)$.",
                ],
                "distractors": [f"$ a = {hyp_even}sqrt(2) $", f"$ a = {leg_val} $", f"$ a = {leg_val}sqrt(3) $"],
                "diagram_svg": svg_right_triangle(a_label="a=?", b_label="a=?", c_label=str(hyp_even), theta_label="45°"),
                "answer_svg": svg_right_triangle(a_label=f"{leg_val}sqrt(2)", b_label=f"{leg_val}sqrt(2)", c_label=str(hyp_even), theta_label="45°"),
            }
        elif sub_type == "30_60_90_long":
            b_val = leg_val
            return {
                "prompt_text": "Find the short leg a and hypotenuse c of the 30-60-90 special right triangle given long leg b.",
                "equation_typst": f"$ \"30\"°\"-60\"°\"-90\"° \" triangle with long leg \" b = {3 * b_val} $",
                "answer_typst": f"$ a = {b_val}sqrt(3), quad c = {2 * b_val}sqrt(3) $",
                "steps_typst": [
                    "In a $30°$-$60°$-$90°$ triangle, $b = a sqrt(3) ==> a = b / sqrt(3)$.",
                    f"Rationalize denominator: $a = ({3 * b_val} sqrt(3)) / 3 = {b_val}sqrt(3)$.",
                    f"Hypotenuse $c = 2a = 2({b_val}sqrt(3)) = {2 * b_val}sqrt(3)$.",
                ],
                "distractors": [f"$ a = {b_val}, c = {2 * b_val} $", f"$ a = {3 * b_val}sqrt(3), c = {6 * b_val} $", f"$ a = {b_val}sqrt(2), c = {2 * b_val} $"],
                "diagram_svg": svg_right_triangle(a_label="a=?", b_label=str(3 * b_val), c_label="c=?", theta_label="60°"),
                "answer_svg": svg_right_triangle(a_label=f"{b_val}sqrt(3)", b_label=str(3 * b_val), c_label=f"{2 * b_val}sqrt(3)", theta_label="60°"),
            }
        elif sub_type == "30_60_90_hyp":
            hyp_val = leg_val * 2
            return {
                "prompt_text": "Find the short leg a and long leg b of the 30-60-90 special right triangle given hypotenuse c.",
                "equation_typst": f"$ \"30\"°\"-60\"°\"-90\"° \" triangle with hypotenuse \" c = {hyp_val} $",
                "answer_typst": f"$ a = {leg_val}, quad b = {leg_val}sqrt(3) $",
                "steps_typst": [
                    f"Short leg $a = c / 2 = {hyp_val} / 2 = {leg_val}$.",
                    f"Long leg $b = a sqrt(3) = {leg_val}sqrt(3)$.",
                    f"Result: $a = {leg_val}, b = {leg_val}sqrt(3)$.",
                ],
                "distractors": [f"$ a = {leg_val}sqrt(3), b = {leg_val} $", f"$ a = {hyp_val}, b = {hyp_val}sqrt(3) $", f"$ a = {leg_val}, b = {leg_val}sqrt(2) $"],
                "diagram_svg": svg_right_triangle(a_label="a=?", b_label="b=?", c_label=str(hyp_val), theta_label="60°"),
                "answer_svg": svg_right_triangle(a_label=str(leg_val), b_label=f"{leg_val}sqrt(3)", c_label=str(hyp_val), theta_label="60°"),
            }
        else:
            return {
                "prompt_text": "Find the long leg b and hypotenuse c of the 30-60-90 special right triangle given short leg a.",
                "equation_typst": f"$ \"30\"°\"-60\"°\"-90\"° \" triangle with short leg \" a = {leg_val} $",
                "answer_typst": f"$ b = {leg_val}sqrt(3), quad c = {2 * leg_val} $",
                "steps_typst": [
                    "In a $30°$-$60°$-$90°$ triangle, sides are in ratio $1 : sqrt(3) : 2$.",
                    f"Long leg $b = a sqrt(3) = {leg_val}sqrt(3)$.",
                    f"Hypotenuse $c = 2a = {2 * leg_val}$.",
                ],
                "distractors": [f"$ b = {leg_val}sqrt(2), quad c = {2 * leg_val} $", f"$ b = {2 * leg_val}, quad c = {leg_val}sqrt(3) $", f"$ b = {3 * leg_val}, quad c = {2 * leg_val} $"],
                "diagram_svg": svg_right_triangle(a_label=str(leg_val), b_label="b=?", c_label="c=?", theta_label="60°"),
                "answer_svg": svg_right_triangle(a_label=str(leg_val), b_label=f"{leg_val}sqrt(3)", c_label=str(2 * leg_val), theta_label="60°"),
            }

    # ------------------------------------------------------------------
    # Q. EVALUATING AND GRAPHING FUNCTIONS & CIRCLES GRAPHING
    # ------------------------------------------------------------------
    if "evaluating and graphing functions" in t_low:
        m = rng.choice([-2, -1, 1, 2]) * scale
        b = rng.randint(-3, 3)
        x0 = rng.randint(-2, 3)
        y0 = m * x0 + b
        return {
            "prompt_text": "Evaluate the function at the given input and graph the function on the coordinate plane.",
            "equation_typst": f"$ f(x) = {m}x {'+ ' + str(b) if b >= 0 else '- ' + str(abs(b))}, quad \"find \" f({x0}) $",
            "answer_typst": f"$ f({x0}) = {y0} $",
            "steps_typst": [
                f"Substitute $x = {x0}$ into $f(x)$: $f({x0}) = {m}({x0}) + ({b}) = {y0}$.",
                f"Plot the y-intercept $(0, {b})$ and evaluated point $({x0}, {y0})$.",
                "Draw the line passing through both points.",
            ],
            "distractors": [f"$ f({x0}) = {m * x0 - b} $", f"$ f({x0}) = {-y0} $", f"$ f({x0}) = {x0 + b} $"],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                lines=[{"m": m, "b": b, "color": "#2563eb"}],
                points=[(0, b, f"(0,{b})", True), (x0, y0, f"({x0},{y0})", True)],
            ),
        }

    if "circles, graphing" in t_low:
        h = rng.randint(-3, 3)
        k = rng.randint(-3, 3)
        r = rng.randint(2, 4 + scale)
        hs = f"(x - {h})^2" if h > 0 else (f"(x + {abs(h)})^2" if h < 0 else "x^2")
        ks = f"(y - {k})^2" if k > 0 else (f"(y + {abs(k)})^2" if k < 0 else "y^2")
        return {
            "prompt_text": "Identify the center and radius of the circle, then sketch its graph.",
            "equation_typst": f"$ {hs} + {ks} = {r * r} $",
            "answer_typst": f"$ \"Center\": ({h}, {k}), quad r = {r} $",
            "steps_typst": [
                "Compare with standard circle form $(x - h)^2 + (y - k)^2 = r^2$.",
                f"Read the center $(h, k) = ({h}, {k})$.",
                f"Take the square root of $r^2 = {r * r}$ to get radius $r = {r}$.",
            ],
            "distractors": [
                f"$ \"Center\": ({-h}, {-k}), quad r = {r} $",
                f"$ \"Center\": ({h}, {k}), quad r = {r * r} $",
                f"$ \"Center\": ({-h}, {-k}), quad r = {r * r} $",
            ],
            "diagram_svg": svg_circle_diagram(radius_label="r=?"),
            "answer_svg": svg_circle_diagram(radius_label=f"r={r}", angle_label=f"C({h},{k})"),
        }

    # ------------------------------------------------------------------
    # R. SCIENTIFIC NOTATION & EXPONENTIAL GROWTH/DECAY WORD PROBLEMS
    # ------------------------------------------------------------------
    if "writing scientific notation" in t_low:
        m = round(rng.uniform(1.2, 9.5), 1)
        exp_n = rng.randint(3, 5 + scale) * (1 if scale < 3 else -1)
        val_str = f"{m * (10 ** exp_n):,.6f}".rstrip("0").rstrip(".")
        return {
            "prompt_text": "Write the number in scientific notation.",
            "equation_typst": f"$ {val_str} $",
            "answer_typst": f"$ {m} times 10^({exp_n}) $",
            "steps_typst": [
                f"Move the decimal point so that the coefficient $a$ satisfies $1 <= a < 10$: $a = {m}$.",
                f"Count the number of places the decimal moved: $|{exp_n}|$ places.",
                f"Write in scientific notation: ${m} times 10^({exp_n})$.",
            ],
            "distractors": [
                f"$ {m} times 10^({-exp_n}) $",
                f"$ {m * 10:g} times 10^({exp_n - 1}) $",
                f"$ {m} times 10^({exp_n + 1}) $",
            ],
        }

    if "addition/subtraction and scientific notation" in t_low or "operations and scientific notation" in t_low:
        a = rng.randint(2, 5)
        b = rng.randint(1, 4)
        exp_n = rng.randint(3, 5 + scale)
        return {
            "prompt_text": "Add or subtract the numbers in scientific notation and write your answer in scientific notation.",
            "equation_typst": f"$ ({a}.2 times 10^{exp_n}) + ({b}.5 times 10^{exp_n}) $",
            "answer_typst": f"$ {a + b}.7 times 10^{exp_n} $",
            "steps_typst": [
                f"Confirm both terms have the same power of $10$: $10^{exp_n}$.",
                f"Add the coefficients: ${a}.2 + {b}.5 = {a + b}.7$.",
                f"Keep the common power of $10$: ${a + b}.7 times 10^{exp_n}$.",
            ],
            "distractors": [
                f"$ {a + b}.7 times 10^({2 * exp_n}) $",
                f"$ {a * b}.7 times 10^{exp_n} $",
                f"$ {a + b}.7 times 10^({exp_n + 1}) $",
            ],
        }

    if "exponential growth and decay" in t_low:
        P = rng.choice([500, 1000, 2000]) * scale
        r_pct = rng.choice([5, 10, 20])
        t = rng.randint(2, 4)
        if "continuous" in t_low:
            amt = round(P * math.exp((r_pct / 100.0) * t), 2)
            return {
                "prompt_text": "Solve the continuous exponential growth problem using A(t) = P e^(rt).",
                "equation_typst": f"$ P = {P}, quad r = {r_pct}% \" continuous growth\", quad t = {t} \" yr\" $",
                "answer_typst": f"$ A({t}) = {P}e^({(r_pct / 100.0) * t:g}) approx {amt:.2f} $",
                "steps_typst": [
                    f"Use the continuous growth model $A(t) = P e^(r t)$ with $P = {P}, r = {r_pct / 100:g}, t = {t}$.",
                    f"Compute the exponent: $r t = ({r_pct / 100:g})({t}) = {(r_pct / 100.0) * t:g}$.",
                    f"Evaluate: $A({t}) = {P}e^({(r_pct / 100.0) * t:g}) approx {amt:.2f}$.",
                ],
                "distractors": [
                    f"$ {round(P * ((1 + r_pct / 100.0) ** t), 2):.2f} $",
                    f"$ {round(P * (1 + (r_pct / 100.0) * t), 2):.2f} $",
                    f"$ {round(amt + 250, 2):.2f} $",
                ],
            }
        amt = round(P * ((1 + r_pct / 100.0) ** t), 2)
        return {
            "prompt_text": "Solve the discrete exponential growth problem using y = a(1 + r)^t.",
            "equation_typst": f"$ a = {P}, quad r = {r_pct}% \" per year\", quad t = {t} \" years\" $",
            "answer_typst": f"$ y = {amt:g} $",
            "steps_typst": [
                f"Use the discrete growth formula $y = a(1 + r)^t$ with $a = {P}, r = {r_pct / 100:g}, t = {t}$.",
                f"Compute the growth factor $1 + r = {1 + r_pct / 100:g}$ and raise to power ${t}$.",
                f"Multiply by ${P}$: $y = {amt:g}$.",
            ],
            "distractors": [
                f"$ y = {P + P * (r_pct / 100.0) * t:g} $",
                f"$ y = {round(P * ((1 - r_pct / 100.0) ** t), 2):g} $",
                f"$ y = {amt + 100:g} $",
            ],
        }

    # ------------------------------------------------------------------
    # S. LOGARITHM PROPERTIES, EQUATIONS & INVERSES (3+ STEPS)
    # ------------------------------------------------------------------
    if "properties of logarithms" in t_low:
        b = rng.choice([2, 3, 5])
        x_c = rng.randint(2, 4 + scale)
        y_c = rng.randint(2, 5)
        return {
            "prompt_text": "Condense the logarithmic expression into a single logarithm.",
            "equation_typst": f"$ {x_c} log_({b})(u) + log_({b})(v) - {y_c} log_({b})(w) $",
            "answer_typst": f"$ log_({b})((u^{x_c} v)/(w^{y_c})) $",
            "steps_typst": [
                f"Apply the power property: ${x_c} log_({b})(u) = log_({b})(u^{x_c})$ and ${y_c} log_({b})(w) = log_({b})(w^{y_c})$.",
                f"Apply the product property: $log_({b})(u^{x_c}) + log_({b})(v) = log_({b})(u^{x_c} v)$.",
                f"Apply the quotient property: $log_({b})((u^{x_c} v)/(w^{y_c}))$.",
            ],
            "distractors": [
                f"$ log_({b})(u^{x_c} + v - w^{y_c}) $",
                f"$ log_({b})((u^{x_c} w^{y_c})/(v)) $",
                f"$ log_({b})(({x_c}u v)/({y_c}w)) $",
            ],
        }

    if "logarithmic equations" in t_low:
        b = rng.choice([2, 3, 4])
        exp_k = rng.randint(2, 2 + scale)
        c = rng.randint(1, 6)
        sol = (b ** exp_k) - c
        return {
            "prompt_text": "Solve the logarithmic equation and check for extraneous solutions.",
            "equation_typst": f"$ log_({b})(x + {c}) = {exp_k} $",
            "answer_typst": f"$ x = {sol} $",
            "steps_typst": [
                f"Rewrite in exponential form: $x + {c} = {b}^{exp_k} = {b ** exp_k}$.",
                f"Subtract ${c}$ from both sides: $x = {sol}$.",
                f"Check domain: ${sol} + {c} = {b ** exp_k} > 0$, so $x = {sol}$ is valid.",
            ],
            "distractors": [
                f"$ x = {b * exp_k - c} $",
                f"$ x = {(b ** exp_k) + c} $",
                f"$ x = {exp_k ** b - c} $",
            ],
        }

    if "writing logs in terms of" in t_low:
        base_b = rng.choice([2, 3, 5, 7, 10])
        p1 = rng.choice([2, 3])
        p2 = rng.choice([4, 5])
        val = (base_b ** p1) * (base_b ** p2)
        return {
            "prompt_text": "Use logarithmic properties to write the expression in terms of simpler logarithms.",
            "equation_typst": f"$ log_({base_b})({base_b}^{p1} times {base_b}^{p2}) $",
            "answer_typst": f"$ {p1 + p2} $",
            "steps_typst": [
                "Apply product rule of logarithms: $log_b(M N) = log_b(M) + log_b(N)$.",
                f"Separate terms: $log_({base_b})({base_b}^{p1}) + log_({base_b})({base_b}^{p2}) = {p1} + {p2}$.",
                f"Sum: ${p1 + p2}$.",
            ],
            "distractors": [f"$ {p1 * p2} $", f"$ {base_b * (p1 + p2)} $", f"$ {p1} $"],
        }

    if "logarithms and exponents as inverses" in t_low or (t_low == "inverses of" and "logarithm" in c_low):
        b_inv = rng.choice([2, 3, 4, 5, 6, 7, 10])
        h_shift = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        k_shift = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        s_h = f"- {h_shift}" if h_shift > 0 else f"+ {abs(h_shift)}"
        s_k = f"+ {k_shift}" if k_shift > 0 else f"- {abs(k_shift)}"
        inv_k = f"- {k_shift}" if k_shift > 0 else f"+ {abs(k_shift)}"
        inv_h = f"+ {h_shift}" if h_shift > 0 else f"- {abs(h_shift)}"
        return {
            "prompt_text": "Find the inverse function f^(-1)(x) for the given function.",
            "equation_typst": f"$ f(x) = {b_inv}^(x {s_h}) {s_k} $",
            "answer_typst": f"$ f^(-1)(x) = log_({b_inv})(x {inv_k}) {inv_h} $",
            "steps_typst": [
                f"Replace $f(x)$ with $y$: $y = {b_inv}^(x {s_h}) {s_k}$.",
                f"Swap $x$ and $y$: $x = {b_inv}^(y {s_h}) {s_k} ==> x {inv_k} = {b_inv}^(y {s_h})$.",
                f"Take $log_({b_inv})$ of both sides: $y {s_h} = log_({b_inv})(x {inv_k}) ==> y = log_({b_inv})(x {inv_k}) {inv_h}$.",
            ],
            "distractors": [
                f"$ f^(-1)(x) = log_({b_inv})(x {s_k}) {s_h} $",
                f"$ f^(-1)(x) = {b_inv}^(x {inv_k}) {inv_h} $",
                f"$ f^(-1)(x) = (x {inv_k}) / ({b_inv}) $",
            ],
        }

    if "exponents and logarithms" in t_low:
        b = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        k = rng.choice([-3, -2, -1, 1, 2, 3, 4])
        if k < 0:
            val_s = f"1/{b ** abs(k)}"
        else:
            val_s = str(b ** k)
        return {
            "prompt_text": "Rewrite the exponential equation in logarithmic form and evaluate.",
            "equation_typst": f"$ {b}^{{{k}}} = {val_s} $",
            "answer_typst": f"$ log_({b})({val_s}) = {k} $",
            "steps_typst": [
                f"Identify base $b = {b}$, exponent $y = {k}$, and value $x = {val_s}$.",
                "Apply the definition $b^y = x <==> log_b(x) = y$.",
                f"Result: $log_({b})({val_s}) = {k}$.",
            ],
            "distractors": [
                f"$ log_({k})({val_s}) = {b} $",
                f"$ log_({b})({k}) = {val_s} $",
                f"$ log_({val_s})({b}) = {k} $",
            ],
        }

    # ------------------------------------------------------------------
    # T. PROBABILITY & FUNDAMENTAL COUNTING PRINCIPLE (3+ STEPS)
    # ------------------------------------------------------------------
    if "sample spaces" in t_low or "fundamental counting principle" in t_low:
        a = rng.randint(3, 5 + scale)
        b = rng.randint(2, 4 + scale)
        c = rng.randint(2, 4)
        tot = a * b * c
        return {
            "prompt_text": "Use the Fundamental Counting Principle to find the total number of possible ways (outcomes) in the sample space.",
            "equation_typst": f"\"Stage 1: \" {a} \" choices, Stage 2: \" {b} \" choices, Stage 3: \" {c} \" choices\"",
            "answer_typst": f"$ {tot} \" outcomes\" $",
            "steps_typst": [
                "By the Fundamental Counting Principle, multiply the number of choices at each independent stage.",
                f"Set up the product: ${a} times {b} times {c}$.",
                f"Total outcomes = ${tot}$.",
            ],
            "distractors": [
                f"$ {a + b + c} \" outcomes\" $",
                f"$ {a * b + c} \" outcomes\" $",
                f"$ {tot * 2} \" outcomes\" $",
            ],
        }

    if "independent and dependent" in t_low:
        r = rng.randint(3, 5 + scale)
        b = rng.randint(3, 6)
        tot = r + b
        if "word" in t_low or scale >= 2:
            # Dependent without replacement
            f = Fraction(r * (r - 1), tot * (tot - 1))
            return {
                "prompt_text": "A bag contains red and blue marbles. Two marbles are drawn without replacement. Find P(both red).",
                "equation_typst": f"\"Red\" = {r}, quad \"Blue\" = {b} quad (\"without replacement\")",
                "answer_typst": f"$ {_fmt_frac(f)} $",
                "steps_typst": [
                    f"First draw: $P(R_1) = {r}/{tot}$.",
                    f"Second draw (dependent, without replacement): $P(R_2 | R_1) = {r - 1}/{tot - 1}$.",
                    f"Multiply: $({r})/({tot}) dot ({r - 1})/({tot - 1}) = {_fmt_frac(f)}$.",
                ],
                "distractors": [
                    f"$ {_fmt_frac(Fraction(r * r, tot * tot))} $",
                    f"$ {_fmt_frac(Fraction(2 * r, tot))} $",
                    f"$ {_fmt_frac(Fraction(r, tot - 1))} $",
                ],
            }
        f = Fraction(r * b, tot * tot)
        return {
            "prompt_text": "Two marbles are drawn WITH replacement. Find the probability P(first red, second blue).",
            "equation_typst": f"\"Red\" = {r}, quad \"Blue\" = {b} quad (\"with replacement\")",
            "answer_typst": f"$ {_fmt_frac(f)} $",
            "steps_typst": [
                f"With replacement, the draws are independent: $P(R) = {r}/{tot}$ and $P(B) = {b}/{tot}$.",
                f"Apply $P(R \" and \" B) = P(R) dot P(B) = ({r})/({tot}) dot ({b})/({tot})$.",
                f"Simplify the fraction: ${_fmt_frac(f)}$.",
            ],
            "distractors": [
                f"$ {_fmt_frac(Fraction(r * b, tot * (tot - 1)))} $",
                f"$ {_fmt_frac(Fraction(r + b, 2 * tot))} $",
                f"$ {_fmt_frac(Fraction(r, tot))} $",
            ],
        }

    # ------------------------------------------------------------------
    # U. CALCULUS INDEFINITE/DEFINITE INTEGRATION & DIFF EQ SUBTOPICS
    # ------------------------------------------------------------------
    if "indefinite integration" in c_low or "definite integration" in c_low or "applications of integration" in c_low or "differential equations" in c_low:
        if "power rule" in t_low:
            n = rng.randint(2, 9)
            m = rng.choice([1, 2, 3])
            c1 = (n + 1) * rng.randint(1, 6)
            c2 = (m + 1) * rng.randint(1, 5)
            c0 = rng.randint(1, 20)
            return {
                "prompt_text": "Evaluate the indefinite integral using the Power Rule.",
                "equation_typst": f"$ integral ({c1}x^{n} + {c2}x^{m} + {c0}) d x $",
                "answer_typst": f"$ {c1 // (n + 1)}x^({n + 1}) + {c2 // (m + 1)}x^({m + 1}) + {c0}x + C $",
                "steps_typst": [
                    "Apply the Power Rule $integral x^p d x = (x^(p+1))/(p+1) + C$ term by term.",
                    f"Integrate ${c1}x^{n}$: $({c1})/({n + 1}) x^({n + 1}) = {c1 // (n + 1)}x^({n + 1})$.",
                    f"Integrate ${c2}x^{m}$: $({c2})/({m + 1}) x^({m + 1}) = {c2 // (m + 1)}x^({m + 1})$ and constant ${c0}$: ${c0}x$.",
                    f"Result: ${c1 // (n + 1)}x^({n + 1}) + {c2 // (m + 1)}x^({m + 1}) + {c0}x + C$.",
                ],
                "distractors": [
                    f"$ {c1 * n}x^({n - 1}) + {c2 * m}x^({m - 1}) + C $",
                    f"$ {c1}x^({n + 1}) + {c2}x^({m + 1}) + {c0}x + C $",
                    f"$ ({c1})/({n})x^{n} + ({c2})/({m})x^{m} + C $",
                ],
            }

        if "logarithmic" in t_low:
            a = rng.randint(2, 25)
            b = rng.randint(1, 25)
            k = rng.choice([1, 2, 3, 4, 5])
            if k == 1:
                return {
                    "prompt_text": "Evaluate the indefinite integral using the logarithmic rule.",
                    "equation_typst": f"$ integral ({a})/(x + {b}) d x $",
                    "answer_typst": f"$ {a} ln|x + {b}| + C $",
                    "steps_typst": [
                        f"Let $u = x + {b}$, so $d u = d x$.",
                        f"Rewrite as ${a} integral (1)/(u) d u = {a} ln|u| + C$.",
                        f"Substitute back: ${a} ln|x + {b}| + C$.",
                    ],
                    "distractors": [
                        f"$ -({a})/((x + {b})^2) + C $",
                        f"$ ln|{a}x + {b}| + C $",
                        f"$ {a}(x + {b})^0 + C $",
                    ],
                }
            else:
                return {
                    "prompt_text": "Evaluate the indefinite integral using the logarithmic rule.",
                    "equation_typst": f"$ integral ({a * k})/({k}x + {b}) d x $",
                    "answer_typst": f"$ {a} ln|{k}x + {b}| + C $",
                    "steps_typst": [
                        f"Let $u = {k}x + {b}$, so $d u = {k} d x ==> d x = (d u)/{k}$.",
                        f"Substitute: $integral ({a * k})/u ((d u)/{k}) = {a} integral (1)/u d u = {a} ln|u| + C$.",
                        f"Substitute back: ${a} ln|{k}x + {b}| + C$.",
                    ],
                    "distractors": [
                        f"$ {a * k} ln|{k}x + {b}| + C $",
                        f"$ ({a})/({k}) ln|{k}x + {b}| + C $",
                        f"$ -({a * k})/({k}x + {b})^2 + C $",
                    ],
                }

        if "inverse trigonometric" in t_low or "inverse_trigonometric" in t_low:
            a = rng.randint(2, 25)
            c = rng.randint(1, 10)
            inv_type = rng.choice(["arctan", "arcsin", "arcsec"])
            if inv_type == "arctan":
                return {
                    "prompt_text": "Evaluate the indefinite integral using inverse trigonometric forms.",
                    "equation_typst": f"$ integral ({c * a})/({a * a} + x^2) d x $",
                    "answer_typst": f"$ {c} arctan((x)/({a})) + C $" if c != 1 else f"$ arctan((x)/({a})) + C $",
                    "steps_typst": [
                        f"Recall standard form $integral (1)/(a^2 + x^2) d x = (1/a) arctan(x/a) + C$ with $a = {a}$.",
                        f"Factor out numerator: ${c * a} times (1/{a}) arctan(x/{a}) + C$.",
                        f"Result: ${c} arctan(x/{a}) + C$.",
                    ],
                    "distractors": [
                        f"$ ({c * a}) arctan(x/{a}) + C $",
                        f"$ {c} arcsin((x)/({a})) + C $",
                        f"$ (1)/({a * a}) arctan(x) + C $",
                    ],
                }
            elif inv_type == "arcsin":
                return {
                    "prompt_text": "Evaluate the indefinite integral using inverse trigonometric forms.",
                    "equation_typst": f"$ integral ({c})/(sqrt({a * a} - x^2)) d x $",
                    "answer_typst": f"$ {c} arcsin((x)/({a})) + C $" if c != 1 else f"$ arcsin((x)/({a})) + C $",
                    "steps_typst": [
                        f"Recall standard form $integral (1)/(sqrt(a^2 - x^2)) d x = arcsin(x/a) + C$ with $a = {a}$.",
                        f"Multiply by constant factor ${c}$.",
                        f"Result: ${c} arcsin(x/{a}) + C$.",
                    ],
                    "distractors": [
                        f"$ ({c})/({a}) arctan((x)/({a})) + C $",
                        f"$ {c} arccos((x)/({a})) + C $",
                        f"$ {c} sqrt({a * a} - x^2) + C $",
                    ],
                }
            else:
                return {
                    "prompt_text": "Evaluate the indefinite integral using inverse trigonometric forms.",
                    "equation_typst": f"$ integral ({c * a})/(x sqrt(x^2 - {a * a})) d x $",
                    "answer_typst": f"$ {c} arcsec((|x|)/({a})) + C $" if c != 1 else f"$ arcsec((|x|)/({a})) + C $",
                    "steps_typst": [
                        f"Recall standard form $integral (1)/(x sqrt(x^2 - a^2)) d x = (1/a) arcsec(|x|/a) + C$ with $a = {a}$.",
                        f"Multiply by numerator constant: ${c * a} times (1/{a}) arcsec(|x|/{a})$.",
                        f"Result: ${c} arcsec(|x|/{a}) + C$.",
                    ],
                    "distractors": [
                        f"$ {c} arctan((x)/({a})) + C $",
                        f"$ {c * a} arcsec(x) + C $",
                        f"$ (1)/({a}) arcsec(x/{a}) + C $",
                    ],
                }

        if "trigonometric" in t_low:
            k = rng.randint(2, 25)
            m = rng.choice([1, 2, 3, 4, 5])
            t_form = rng.choice(["sin", "cos", "sec2", "csc2", "sec_tan"])
            if t_form == "sin":
                return {
                    "prompt_text": "Evaluate the trigonometric indefinite integral.",
                    "equation_typst": f"$ integral {k * m} sin({m}x) d x $",
                    "answer_typst": f"$ -{k} cos({m}x) + C $",
                    "steps_typst": [
                        f"Identify the outer coefficient ${k * m}$ and argument $u = {m}x$.",
                        f"Apply substitution $d u = {m} d x ==> d x = (d u)/{m}$ to integrate: $integral sin(u) d u = -cos(u)$.",
                        f"Multiply: $({k * m}/{m}) (-cos({m}x)) + C = -{k} cos({m}x) + C$.",
                    ],
                    "distractors": [f"$ {k} cos({m}x) + C $", f"$ -{k * m} cos({m}x) + C $", f"$ -{k} sin({m}x) + C $"],
                }
            elif t_form == "cos":
                return {
                    "prompt_text": "Evaluate the trigonometric indefinite integral.",
                    "equation_typst": f"$ integral {k * m} cos({m}x) d x $",
                    "answer_typst": f"$ {k} sin({m}x) + C $",
                    "steps_typst": [
                        f"Identify outer coefficient ${k * m}$ and argument $u = {m}x$.",
                        f"Apply substitution $d u = {m} d x ==> d x = (d u)/{m}$ to integrate: $integral cos(u) d u = sin(u)$.",
                        f"Multiply: $({k * m}/{m}) sin({m}x) + C = {k} sin({m}x) + C$.",
                    ],
                    "distractors": [f"$ -{k} sin({m}x) + C $", f"$ {k * m} sin({m}x) + C $", f"$ {k} cos({m}x) + C $"],
                }
            elif t_form == "sec2":
                return {
                    "prompt_text": "Evaluate the trigonometric indefinite integral.",
                    "equation_typst": f"$ integral {k * m} sec^2({m}x) d x $",
                    "answer_typst": f"$ {k} tan({m}x) + C $",
                    "steps_typst": [
                        "Recall standard form $integral sec^2(u) d u = tan(u) + C$.",
                        f"Substitute $u = {m}x$ and $d u = {m} d x$: $({k * m}/{m}) integral sec^2(u) d u$.",
                        f"Evaluate: ${k} tan({m}x) + C$.",
                    ],
                    "distractors": [f"$ -{k} tan({m}x) + C $", f"$ {k} sec({m}x) + C $", f"$ {k * m} tan({m}x) + C $"],
                }
            elif t_form == "csc2":
                return {
                    "prompt_text": "Evaluate the trigonometric indefinite integral.",
                    "equation_typst": f"$ integral {k * m} csc^2({m}x) d x $",
                    "answer_typst": f"$ -{k} cot({m}x) + C $",
                    "steps_typst": [
                        "Recall standard form $integral csc^2(u) d u = -cot(u) + C$.",
                        f"Substitute $u = {m}x$ and $d u = {m} d x$: $({k * m}/{m}) integral csc^2(u) d u$.",
                        f"Evaluate: $-{k} cot({m}x) + C$.",
                    ],
                    "distractors": [f"$ {k} cot({m}x) + C $", f"$ -{k} csc({m}x) + C $", f"$ -{k * m} cot({m}x) + C $"],
                }
            else:
                return {
                    "prompt_text": "Evaluate the trigonometric indefinite integral.",
                    "equation_typst": f"$ integral {k * m} sec({m}x) tan({m}x) d x $",
                    "answer_typst": f"$ {k} sec({m}x) + C $",
                    "steps_typst": [
                        "Recall standard form $integral sec(u) tan(u) d u = sec(u) + C$.",
                        f"Substitute $u = {m}x$ and $d u = {m} d x$: $({k * m}/{m}) integral sec(u) tan(u) d u$.",
                        f"Evaluate: ${k} sec({m}x) + C$.",
                    ],
                    "distractors": [f"$ -{k} sec({m}x) + C $", f"$ {k} tan({m}x) + C $", f"$ {k * m} sec({m}x) + C $"],
                }
        if "first fundamental theorem" in t_low:
            b = rng.randint(1, 15)
            a_low = rng.choice([0, 1, 2])
            n_pow = rng.choice([1, 2, 3])
            c_val = n_pow + 1
            ans_val = (b ** c_val) - (a_low ** c_val)
            return {
                "prompt_text": "Evaluate the definite integral using the First Fundamental Theorem of Calculus.",
                "equation_typst": f"$ integral_{a_low}^{b} {c_val}x^{n_pow} d x $" if n_pow > 1 else f"$ integral_{a_low}^{b} {c_val}x d x $",
                "answer_typst": f"$ {ans_val} $",
                "steps_typst": [
                    f"Find an antiderivative $F(x)$ of ${c_val}x^{n_pow}$: $F(x) = x^{c_val}$.",
                    f"Apply First Fundamental Theorem: $F({b}) - F({a_low}) = ({b})^{c_val} - ({a_low})^{c_val}$.",
                    f"Evaluate: ${b ** c_val} - {a_low ** c_val} = {ans_val}$.",
                ],
                "distractors": [f"$ {ans_val + b} $", f"$ {ans_val // 2} $", f"$ {c_val * b ** n_pow} $"],
            }

        if "motion along a line" in t_low:
            a = rng.randint(1, 12)
            b = rng.randint(1, 10)
            t1 = rng.randint(2, 12)
            disp = a * (t1 ** 2) + b * t1
            return {
                "prompt_text": "Given the velocity function v(t), find the net displacement of the particle over [0, t_1].",
                "equation_typst": f"$ v(t) = {2 * a}t + {b}, quad [0, {t1}] $",
                "answer_typst": f"$ Delta s = {disp} $",
                "steps_typst": [
                    f"Net displacement is the definite integral of velocity: $Delta s = integral_0^({t1}) ({2 * a}t + {b}) d t$.",
                    f"Find the antiderivative $[{a}t^2 + {b}t]_0^({t1})$.",
                    f"Evaluate: ${a}({t1})^2 + {b}({t1}) = {disp}$.",
                ],
                "distractors": [f"$ {2 * a * t1 + b} $", f"$ {disp * 2} $", f"$ {disp - a} $"],
            }

        if "separable" in t_low or "introduction" in t_low:
            k = rng.choice([k for k in range(-12, 13) if k != 0])
            m = rng.choice([1, 2, 3])
            sep_mode = rng.choice(["xy", "y_lin", "x_over_y"])
            if sep_mode == "xy":
                return {
                    "prompt_text": "Solve the separable differential equation.",
                    "equation_typst": f"$ (d y)/(d x) = {k} x y $",
                    "answer_typst": f"$ y = C e^(({k}x^2)/(2)) $",
                    "steps_typst": [
                        f"Separate variables: $(1/y) d y = {k} x d x$.",
                        f"Integrate both sides: $ln|y| = ({k}/2) x^2 + C_1$.",
                        f"Exponentiate: $y = C e^(({k}x^2)/2)$.",
                    ],
                    "distractors": [f"$ y = {k}x^2 + C $", f"$ y = C e^({k}x) $", f"$ y = ({k}/2)x^2 + C $"],
                }
            elif sep_mode == "y_lin":
                return {
                    "prompt_text": "Solve the separable differential equation.",
                    "equation_typst": f"$ (d y)/(d x) = {k} y $",
                    "answer_typst": f"$ y = C e^({k}x) $",
                    "steps_typst": [
                        f"Separate variables: $(1/y) d y = {k} d x$.",
                        f"Integrate both sides: $ln|y| = {k}x + C_1$.",
                        f"General solution: $y = C e^({k}x)$.",
                    ],
                    "distractors": [f"$ y = ({k}/2)x^2 + C $", f"$ y = {k}x + C $", f"$ y = C e^(-{k}x) $"],
                }
            else:
                return {
                    "prompt_text": "Solve the separable differential equation.",
                    "equation_typst": f"$ (d y)/(d x) = ({k}x)/(y) $",
                    "answer_typst": f"$ y^2 - {k}x^2 = C $",
                    "steps_typst": [
                        f"Separate variables: $y d y = {k} x d x$.",
                        f"Integrate both sides: $(y^2)/2 = ({k}x^2)/2 + C_1$.",
                        f"Multiply by 2: $y^2 - {k}x^2 = C$.",
                    ],
                    "distractors": [f"$ y^2 + {k}x^2 = C $", f"$ y = {k}x + C $", f"$ y^2 = {k}x + C $"],
                }

    if "adding and subtracting integers" in t_low:
        a = rng.randint(-12 * scale, -2)
        b = rng.randint(-10 * scale, 12 * scale)
        op = rng.choice(["+", "-"])
        ans = a + b if op == "+" else a - b
        return {
            "prompt_text": "Find each sum or difference of integers.",
            "equation_typst": f"$ ({a}) {op} ({b}) $",
            "answer_typst": f"$ {ans} $",
            "steps_typst": [
                f"Start at ${a}$ on the integer number line.",
                f"{'Add' if op == '+' else 'Subtract'} ${b}$ by moving {'right' if (b >= 0 if op == '+' else b < 0) else 'left'} $|{b}|$ units.",
                f"Result: ${ans}$.",
            ],
            "distractors": [f"$ {-ans} $", f"$ {abs(a) + abs(b)} $", f"$ {a * b} $"],
        }

    if "multiplying and dividing integers" in t_low:
        a = rng.choice([-9, -7, -6, -5, -4, 4, 6, 8]) * scale
        b = rng.choice([-6, -4, -3, -2, 3, 5])
        if rng.random() < 0.5:
            ans = a * b
            return {
                "prompt_text": "Find each product of integers.",
                "equation_typst": f"$ ({a}) times ({b}) $",
                "answer_typst": f"$ {ans} $",
                "steps_typst": [
                    f"Multiply the absolute values: $|{a}| times |{b}| = {abs(a * b)}$.",
                    f"Determine the sign: {'same signs give positive' if (a > 0) == (b > 0) else 'opposite signs give negative'}.",
                    f"Product = ${ans}$.",
                ],
                "distractors": [f"$ {-ans} $", f"$ {a + b} $", f"$ {ans + b} $"],
            }
        prod = a * b
        return {
            "prompt_text": "Find each quotient of integers.",
            "equation_typst": f"$ ({prod}) div ({b}) $",
            "answer_typst": f"$ {a} $",
            "steps_typst": [
                f"Divide the absolute values: ${abs(prod)} div {abs(b)} = {abs(a)}$.",
                f"Apply integer sign rules: {'same signs -> positive' if (prod > 0) == (b > 0) else 'opposite signs -> negative'}.",
                f"Quotient = ${a}$.",
            ],
            "distractors": [f"$ {-a} $", f"$ {prod - b} $", f"$ {b} $"],
        }

    if "dividing fractions" in c_low:
        f1 = Fraction(rng.randint(1, 3 + scale), rng.choice([2, 3, 4, 5]))
        f2 = Fraction(rng.randint(1, 3), rng.choice([2, 4, 5, 6]))
        ans = f1 / f2
        return {
            "prompt_text": f"Solve the fraction division problem ({topic_name}). Simplify your answer completely.",
            "equation_typst": f"$ {_fmt_frac(f1)} div {_fmt_frac(f2)} $",
            "answer_typst": f"$ {_fmt_frac(ans)} $",
            "steps_typst": [
                f"Rewrite division as multiplication by the reciprocal of ${_fmt_frac(f2)}$: $({f2.denominator})/({f2.numerator})$.",
                f"Multiply numerators and denominators: $({f1.numerator} times {f2.denominator})/({f1.denominator} times {f2.numerator})$.",
                f"Simplify to lowest terms: ${_fmt_frac(ans)}$.",
            ],
            "distractors": [
                f"$ {_fmt_frac(f1 * f2)} $",
                f"$ {_fmt_frac(Fraction(ans.denominator, ans.numerator))} $",
                f"$ {_fmt_frac(f1 + f2)} $",
            ],
        }

    if "writing numeric expressions" in t_low or "writing algebraic expressions" in t_low:
        a = rng.randint(3, 9 * scale)
        b = rng.randint(2, 8)
        if "numeric" in t_low:
            val = a * b + 5
            return {
                "prompt_text": "Write the numeric expression for the verbal phrase and evaluate it.",
                "equation_typst": f"\"5 more than the product of {a} and {b}\"",
                "answer_typst": f"$ {a} times {b} + 5 = {val} $",
                "steps_typst": [
                    f"Translate 'the product of ${a}$ and ${b}$' as ${a} times {b}$.",
                    f"Translate '5 more than' by adding $5$: ${a} times {b} + 5$.",
                    f"Evaluate: ${a * b} + 5 = {val}$.",
                ],
                "distractors": [
                    f"$ {a} + ({b} times 5) = {a + b * 5} $",
                    f"$ ({a} + 5) times {b} = {(a + 5) * b} $",
                    f"$ {a} + {b} + 5 = {a + b + 5} $",
                ],
            }
        return {
            "prompt_text": "Write an algebraic expression for the verbal description.",
            "equation_typst": f"\"{b} less than the product of {a} and a number n\"",
            "answer_typst": f"$ {a}n - {b} $",
            "steps_typst": [
                f"Translate 'the product of ${a}$ and a number $n$' as ${a}n$.",
                f"Translate '${b}$ less than' by subtracting ${b}$ from ${a}n$.",
                f"Expression: ${a}n - {b}$.",
            ],
            "distractors": [f"$ {b} - {a}n $", f"$ {a}(n - {b}) $", f"$ (n)/({a}) - {b} $"],
        }

    if "numeric expressions with exponents" in t_low:
        base = rng.choice([2, 3, 4, 5])
        exp_k = rng.choice([2, 3])
        c = rng.randint(2, 10 * scale)
        val = (base ** exp_k) + c
        return {
            "prompt_text": "Evaluate the numeric expression containing exponents using order of operations.",
            "equation_typst": f"$ {base}^{exp_k} + {c} $",
            "answer_typst": f"$ {val} $",
            "steps_typst": [
                f"Evaluate the exponent first: ${base}^{exp_k} = {base ** exp_k}$.",
                f"Add ${c}$: ${base ** exp_k} + {c} = {val}$.",
                f"Result: ${val}$.",
            ],
            "distractors": [f"$ {base * exp_k + c} $", f"$ {(base + c) ** exp_k} $", f"$ {val + base} $"],
        }

    if "solutions to equations" in t_low or "solutions to inequalities" in t_low:
        a = rng.randint(2, 5 * scale)
        b = rng.randint(1, 9)
        x_test = rng.randint(2, 7)
        if "inequalities" in t_low:
            rhs = a * x_test - 2
            return {
                "prompt_text": "Determine whether the given value of x is a solution to the inequality.",
                "equation_typst": f"$ {a}x + {b} > {rhs}; quad x = {x_test} $",
                "answer_typst": f"$ \"Yes, because \" {a * x_test + b} > {rhs} $",
                "steps_typst": [
                    f"Substitute $x = {x_test}$ into the left side: ${a}({x_test}) + {b} = {a * x_test + b}$.",
                    f"Compare with the right side: ${a * x_test + b} > {rhs}$ is true.",
                    f"Therefore, $x = {x_test}$ is a solution.",
                ],
                "distractors": [
                    f"$ \"No, because \" {a * x_test + b} < {rhs} $",
                    f"$ \"No, because \" {a * x_test} = {rhs} $",
                    "$ \"Cannot be determined\" $",
                ],
            }
        rhs = a * x_test + b
        return {
            "prompt_text": "Determine whether the given value of x is a solution to the equation.",
            "equation_typst": f"$ {a}x + {b} = {rhs}; quad x = {x_test} $",
            "answer_typst": f"$ \"Yes, because \" {rhs} = {rhs} $",
            "steps_typst": [
                f"Substitute $x = {x_test}$ into ${a}x + {b}$: ${a}({x_test}) + {b} = {rhs}$.",
                f"Compare both sides: ${rhs} = {rhs}$ (true).",
                f"Therefore, $x = {x_test}$ is a solution.",
            ],
            "distractors": [
                f"$ \"No, left side equals \" {a * x_test - b} $",
                f"$ \"No, left side equals \" {a + x_test + b} $",
                "$ \"No solution\" $",
            ],
        }

    if "area and perimeter of rectangles and triangles" in t_low:
        w = rng.randint(4, 10 * scale)
        h = rng.randint(3, 8 * scale)
        area = w * h
        perim = 2 * (w + h)
        return {
            "prompt_text": "Find the perimeter P and area A of the rectangle.",
            "equation_typst": f"$ l = {w}, quad w = {h} $",
            "answer_typst": f"$ P = {perim}, quad A = {area} $",
            "steps_typst": [
                f"Perimeter of a rectangle: $P = 2(l + w) = 2({w} + {h}) = {perim}$.",
                f"Area of a rectangle: $A = l times w = {w} times {h} = {area}$.",
                f"Result: $P = {perim}, A = {area}$.",
            ],
            "distractors": [
                f"$ P = {w + h}, quad A = {area} $",
                f"$ P = {area}, quad A = {perim} $",
                f"$ P = {perim}, quad A = {w * h // 2} $",
            ],
            "diagram_svg": svg_polygon_diagram("rectangle", f"l = {w}", f"w = {h}"),
            "answer_svg": svg_polygon_diagram("rectangle", f"P = {perim}", f"A = {area}"),
        }

    # ------------------------------------------------------------------
    # W. GEOMETRY CONSTRUCTIONS & TRIGONOMETRY SUBTOPICS
    # ------------------------------------------------------------------
    if "constructions" in c_low:
        if "altitude" in t_low:
            base = rng.randint(8, 45)
            alt = rng.randint(4, 30)
            tri_area = (base * alt) // 2
            return {
                "prompt_text": "Compass-and-straightedge altitude construction: an altitude h is constructed perpendicular to base b. Find the area of the triangle.",
                "equation_typst": f"$ b = {base}, quad h = {alt} $",
                "answer_typst": f"$ \"Area\" = {tri_area} $",
                "steps_typst": [
                    "An altitude construction drops a perpendicular line from a vertex to the opposite base.",
                    f"Use triangle area formula: $A = 1/2 b h = 1/2({base})({alt})$.",
                    f"Evaluate: $A = {tri_area}$.",
                ],
                "distractors": [f"$ \"Area\" = {base * alt} $", f"$ \"Area\" = {tri_area + base} $", f"$ \"Area\" = {base + alt} $"],
                "diagram_svg": svg_general_triangle(side_a=f"b = {base}", side_b=f"h = {alt}"),
                "answer_svg": svg_general_triangle(side_a=f"b = {base}", side_b=f"Area = {tri_area}"),
            }
        elif "angle_bisector" in t_low or "bisector" in t_low:
            ab = rng.randint(6, 25)
            ac = rng.randint(6, 25)
            bd = rng.randint(4, 18)
            dc = Fraction(ac * bd, ab)
            dc_s = f"{dc.numerator}/{dc.denominator}" if dc.denominator != 1 else str(dc.numerator)
            return {
                "prompt_text": "In triangle ABC, ray AD bisects angle A (constructed with compass). By the Angle Bisector Theorem, find DC.",
                "equation_typst": f"$ A B = {ab}, quad A C = {ac}, quad B D = {bd} $",
                "answer_typst": f"$ D C = {dc_s} $",
                "steps_typst": [
                    "The Angle Bisector Theorem states $(A B)/(A C) = (B D)/(D C)$.",
                    f"Substitute lengths: $({ab})/({ac}) = ({bd})/(D C)$.",
                    f"Cross-multiply and solve: $D C = ({ac} times {bd}) / {ab} = {dc_s}$.",
                ],
                "distractors": [f"$ D C = {bd} $", f"$ D C = {ab} $", f"$ D C = {dc + 2} $"],
                "diagram_svg": svg_general_triangle(side_a=f"AB={ab}", side_b=f"AC={ac}", side_c=f"BD={bd}"),
                "answer_svg": svg_general_triangle(side_a=f"AB={ab}", side_b=f"AC={ac}", side_c=f"DC={dc_s}"),
            }
        elif "median" in t_low:
            bc_len = rng.randint(6, 45) * 2
            half = bc_len // 2
            return {
                "prompt_text": "Compass-and-straightedge median construction: median AM is drawn to side BC. Find BM.",
                "equation_typst": f"$ B C = {bc_len}, quad M \" is constructed midpoint of \" B C $",
                "answer_typst": f"$ B M = {half} $",
                "steps_typst": [
                    "A median connects a vertex to the midpoint of the opposite side.",
                    f"The perpendicular bisector construction locates midpoint $M$, dividing $B C = {bc_len}$ in half.",
                    f"Length $B M = B C / 2 = {bc_len} / 2 = {half}$.",
                ],
                "distractors": [f"$ B M = {bc_len} $", f"$ B M = {half * 2} $", f"$ B M = {half // 2} $"],
                "diagram_svg": svg_general_triangle(side_a=f"BC = {bc_len}", side_b="Median AM"),
                "answer_svg": svg_general_triangle(side_a=f"BM = {half}", side_b="Median AM"),
            }
        elif "angle" in t_low:
            deg = rng.randint(15, 80) * 2
            half = deg // 2
            return {
                "prompt_text": "Compass-and-straightedge construction: if angle ABC is bisected by ray BD, find m angle ABD.",
                "equation_typst": f"$ m angle A B C = {deg}°, quad \"ray \" B D \" bisects \" angle A B C $",
                "answer_typst": f"$ m angle A B D = {half}° $",
                "steps_typst": [
                    "An angle bisector construction divides the angle into two congruent angles.",
                    f"Divide $m angle A B C = {deg}°$ by $2$.",
                    f"Result: $m angle A B D = {half}°$.",
                ],
                "distractors": [f"$ {deg}° $", f"$ {2 * deg}° $", f"$ {180 - deg}° $"],
                "diagram_svg": svg_angle_diagram(angle_degrees=half, interior_angle=half, mode="interior_ray", angle_label="?", interior_angle_label=f"{half}°"),
                "answer_svg": svg_angle_diagram(angle_degrees=half, interior_angle=half, mode="interior_ray", angle_label=f"{half}°", interior_angle_label=f"{half}°", shade=True, bottom_label=f"m∠ABD = {half}°"),
            }
        else:
            s1 = rng.randint(4, 20)
            s2 = rng.randint(4, 20)
            s3 = rng.randint(max(s1, s2) - min(s1, s2) + 1, s1 + s2 - 1)
            perim = s1 + s2 + s3
            return {
                "prompt_text": "Compass-and-straightedge triangle construction: construct triangle ABC with given side lengths and find its perimeter.",
                "equation_typst": f"$ a = {s1}, quad b = {s2}, quad c = {s3} $",
                "answer_typst": f"$ \"Perimeter\" = {perim} $",
                "steps_typst": [
                    "Draw base segment $c = " + str(s3) + "$ with straightedge.",
                    "Set compass widths $a = " + str(s1) + "$ and $b = " + str(s2) + "$ to locate third vertex by intersection of arcs.",
                    f"Perimeter: $P = {s1} + {s2} + {s3} = {perim}$.",
                ],
                "distractors": [f"$ \"Perimeter\" = {perim + 2} $", f"$ \"Perimeter\" = {s1 * s2} $", f"$ \"Perimeter\" = {perim - 4} $"],
                "diagram_svg": svg_general_triangle(side_a=str(s1), side_b=str(s2), side_c=str(s3)),
                "answer_svg": svg_general_triangle(side_a=str(s1), side_b=str(s2), side_c=f"P = {perim}"),
            }

    if "trigonometry" in c_low:
        if "area" in t_low:
            a = rng.randint(4, 10 * scale)
            b = rng.randint(6, 12)
            area = Fraction(a * b, 4)  # sin(30 deg) = 1/2 -> 1/2 * a * b * 1/2
            return {
                "prompt_text": "Find the area of triangle ABC using the trigonometric area formula A = (1/2)ab sin(C).",
                "equation_typst": f"$ a = {a}, quad b = {b}, quad m angle C = 30° $",
                "answer_typst": f"$ A = {_fmt_frac(area)} $",
                "steps_typst": [
                    "Use the area formula $A = 1/2 a b sin(C)$.",
                    f"Substitute $a = {a}, b = {b}$, and $sin(30°) = 1/2$: $A = 1/2 ({a})({b})(1/2)$.",
                    f"Simplify: $A = {_fmt_frac(area)}$.",
                ],
                "distractors": [
                    f"$ A = {a * b // 2} $",
                    f"$ A = {_fmt_frac(area)} sqrt(3) $",
                    f"$ A = {a * b} $",
                ],
                "diagram_svg": svg_general_triangle(side_a=str(a), side_b=str(b), angle_c="30°"),
                "answer_svg": svg_general_triangle(side_a=str(a), side_b=str(b), angle_c="30°", side_c=f"Area={area}"),
            }
        if "degrees-minutes-seconds" in t_low:
            deg = rng.randint(15, 75) + scale
            mins = rng.choice([12, 24, 30, 36, 45, 48])
            dec = round(deg + mins / 60.0, 2)
            return {
                "prompt_text": "Convert the angle measure from degrees-minutes-seconds (DMS) to decimal degrees.",
                "equation_typst": f"$ {deg}° {mins}' $",
                "answer_typst": f"$ {dec:g}° $",
                "steps_typst": [
                    "Use the conversion $1° = 60'$.",
                    f"Convert ${mins}'$ to degrees: ${mins}/60 = {mins / 60.0:g}°$.",
                    f"Add to ${deg}°$: ${deg} + {mins / 60.0:g} = {dec:g}°$.",
                ],
                "distractors": [
                    f"$ {deg}.{mins}° $",
                    f"$ {round(deg + mins / 100.0, 2):g}° $",
                    f"$ {deg * 60 + mins}° $",
                ],
            }
        if "angles and angle measure" in t_low:
            conv_dir = rng.choice(["deg_to_rad", "rad_to_deg", "coterminal"])
            if conv_dir == "rad_to_deg":
                num_k = rng.choice([k for k in range(-12, 13) if k != 0])
                den_k = rng.choice([2, 3, 4, 6])
                deg_ans = (num_k * 180) // den_k
                num_str = "-" if num_k == -1 else ("" if num_k == 1 else str(num_k))
                return {
                    "prompt_text": "Convert the angle measure from radians to degrees.",
                    "equation_typst": f"$ ({num_str}pi)/({den_k}) $",
                    "answer_typst": f"$ {deg_ans}° $",
                    "steps_typst": [
                        f"Multiply by conversion factor $(180°) / pi$: $({num_str}pi)/({den_k}) times (180°)/pi$.",
                        f"Cancel $pi$ and simplify: $({num_k} times 180°) / {den_k} = {deg_ans}°$.",
                        f"Answer: ${deg_ans}°$.",
                    ],
                    "distractors": [f"$ {deg_ans + 30}° $", f"$ {180 - deg_ans}° $", f"$ {deg_ans * 2}° $"],
                }
            elif conv_dir == "coterminal":
                base_ang = rng.randint(15, 345)
                pos_c = base_ang + 360
                neg_c = base_ang - 360
                return {
                    "prompt_text": "Find one positive and one negative coterminal angle for the given angle.",
                    "equation_typst": f"$ {base_ang}° $",
                    "answer_typst": f"$ {pos_c}° \" and \" {neg_c}° $",
                    "steps_typst": [
                        f"Add $360°$: ${base_ang}° + 360° = {pos_c}°$.",
                        f"Subtract $360°$: ${base_ang}° - 360° = {neg_c}°$.",
                        f"Coterminal angles: ${pos_c}°$ and ${neg_c}°$.",
                    ],
                    "distractors": [f"$ {base_ang + 180}°, {base_ang - 180}° $", f"$ {pos_c + 360}°, {neg_c}° $", f"$ {pos_c}°, 0° $"],
                }
            else:
                deg = rng.choice([15 * k for k in range(-24, 25) if k != 0] + [rng.randint(-360, 360)])
                f = Fraction(deg, 180)
                return {
                    "prompt_text": "Convert the angle measure from degrees to radians in exact simplified form.",
                    "equation_typst": f"$ {deg}° $",
                    "answer_typst": f"$ {_fmt_frac(f)} pi $",
                    "steps_typst": [
                        "Multiply degree measure by $(pi \" radians\")/(180°)$.",
                        f"Form fraction $({deg})/(180) pi$ and divide by $\\gcd({abs(deg)}, 180) = {math.gcd(abs(deg), 180)}$.",
                        f"Exact radian measure: ${_fmt_frac(f)} pi$.",
                    ],
                    "distractors": [
                        f"$ {_fmt_frac(Fraction(f.denominator, abs(f.numerator) if f.numerator != 0 else 1))} pi $",
                        f"$ {_fmt_frac(Fraction(deg, 360))} pi $",
                        f"$ {deg} pi $",
                    ],
                }

        if "trig functions of any angle" in t_low:
            pyth_list = [(-3, 4, 5), (5, -12, 13), (-8, -15, 17), (7, 24, 25), (-9, 40, 41), (12, -35, 37), (-20, 21, 29)]
            x0, y0, r0 = rng.choice(pyth_list)
            mult = rng.choice([1, 2, 3])
            x, y, r = x0 * mult, y0 * mult, r0 * mult
            sin_f = Fraction(y, r)
            cos_f = Fraction(x, r)
            tan_f = Fraction(y, x)
            return {
                "prompt_text": "The terminal side of angle theta in standard position passes through P(x, y). Find sin(theta), cos(theta), and tan(theta).",
                "equation_typst": f"$ P({x}, {y}) $",
                "answer_typst": f"$ sin(theta) = {_fmt_frac(sin_f)}, quad cos(theta) = {_fmt_frac(cos_f)}, quad tan(theta) = {_fmt_frac(tan_f)} $",
                "steps_typst": [
                    f"Calculate distance $r = sqrt(x^2 + y^2) = sqrt(({x})^2 + ({y})^2) = {r}$.",
                    f"Calculate $sin(theta) = y/r = ({y})/({r}) = {_fmt_frac(sin_f)}$.",
                    f"Calculate $cos(theta) = x/r = ({x})/({r}) = {_fmt_frac(cos_f)}$ and $tan(theta) = y/x = {_fmt_frac(tan_f)}$.",
                ],
                "distractors": [
                    f"$ sin(theta) = {_fmt_frac(cos_f)}, quad cos(theta) = {_fmt_frac(sin_f)} $",
                    f"$ sin(theta) = {_fmt_frac(Fraction(-y, r))}, quad cos(theta) = {_fmt_frac(Fraction(-x, r))} $",
                    "$ sin(theta) = 1, quad cos(theta) = 0 $",
                ],
            }
        if "product_to_sum" in t_low or "product-to-sum" in t_low or "product to sum" in t_low:
            p_case = rng.choice(["sin_cos", "cos_cos", "sin_sin"])
            a_ang = rng.randint(2, 9)
            b_ang = rng.randint(1, a_ang - 1)
            sum_ang = a_ang + b_ang
            diff_ang = a_ang - b_ang
            if p_case == "sin_cos":
                return {
                    "prompt_text": "Express the product as a sum or difference of trigonometric functions.",
                    "equation_typst": f"$ 2 sin({a_ang} theta) cos({b_ang} theta) $",
                    "answer_typst": f"$ sin({sum_ang} theta) + sin({diff_ang} theta) $",
                    "steps_typst": [
                        "Use the product-to-sum identity $2 sin(A) cos(B) = sin(A + B) + sin(A - B)$.",
                        f"Substitute $A = {a_ang} theta$ and $B = {b_ang} theta$: $sin({a_ang} theta + {b_ang} theta) + sin({a_ang} theta - {b_ang} theta)$.",
                        f"Result: $sin({sum_ang} theta) + sin({diff_ang} theta)$.",
                    ],
                    "distractors": [f"$ sin({sum_ang} theta) - sin({diff_ang} theta) $", f"$ cos({sum_ang} theta) + cos({diff_ang} theta) $", f"$ 2 sin({sum_ang} theta) $"],
                }
            elif p_case == "cos_cos":
                return {
                    "prompt_text": "Express the product as a sum of trigonometric functions.",
                    "equation_typst": f"$ 2 cos({a_ang} theta) cos({b_ang} theta) $",
                    "answer_typst": f"$ cos({sum_ang} theta) + cos({diff_ang} theta) $",
                    "steps_typst": [
                        "Use the product-to-sum identity $2 cos(A) cos(B) = cos(A + B) + cos(A - B)$.",
                        f"Substitute $A = {a_ang} theta$ and $B = {b_ang} theta$.",
                        f"Result: $cos({sum_ang} theta) + cos({diff_ang} theta)$.",
                    ],
                    "distractors": [f"$ cos({sum_ang} theta) - cos({diff_ang} theta) $", f"$ sin({sum_ang} theta) + sin({diff_ang} theta) $", f"$ 2 cos({sum_ang} theta) $"],
                }
            else:
                return {
                    "prompt_text": "Express the product as a difference of trigonometric functions.",
                    "equation_typst": f"$ -2 sin({a_ang} theta) sin({b_ang} theta) $",
                    "answer_typst": f"$ cos({sum_ang} theta) - cos({diff_ang} theta) $",
                    "steps_typst": [
                        "Use the identity $-2 sin(A) sin(B) = cos(A + B) - cos(A - B)$.",
                        f"Substitute $A = {a_ang} theta$ and $B = {b_ang} theta$.",
                        f"Result: $cos({sum_ang} theta) - cos({diff_ang} theta)$.",
                    ],
                    "distractors": [f"$ cos({sum_ang} theta) + cos({diff_ang} theta) $", f"$ sin({sum_ang} theta) - sin({diff_ang} theta) $", f"$ -2 sin({sum_ang} theta) $"],
                }

        if "double_angle" in t_low or "half_angle" in t_low or "multiple_angle" in t_low or "multiple angle" in t_low or "double angle" in t_low:
            pyth = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
            opp, adj, hyp = pyth
            sin_2t = Fraction(2 * opp * adj, hyp * hyp)
            cos_2t = Fraction(adj * adj - opp * opp, hyp * hyp)
            return {
                "prompt_text": "Angle theta is acute with sin(theta) = y/r. Find sin(2theta) and cos(2theta).",
                "equation_typst": f"$ sin(theta) = {opp}/{hyp} $",
                "answer_typst": f"$ sin(2 theta) = {_fmt_frac(sin_2t)}, quad cos(2 theta) = {_fmt_frac(cos_2t)} $",
                "steps_typst": [
                    f"Since $theta$ is in Quadrant I, $cos(theta) = sqrt(1 - ({opp}/{hyp})^2) = {adj}/{hyp}$.",
                    f"Apply double angle formula: $sin(2 theta) = 2 sin(theta) cos(theta) = 2({opp}/{hyp})({adj}/{hyp}) = {_fmt_frac(sin_2t)}$.",
                    f"Apply $cos(2 theta) = cos^2(theta) - sin^2(theta) = ({adj}/{hyp})^2 - ({opp}/{hyp})^2 = {_fmt_frac(cos_2t)}$.",
                ],
                "distractors": [f"$ sin(2 theta) = {2 * opp}/{hyp} $", f"$ sin(2 theta) = {_fmt_frac(cos_2t)} $", "$ sin(2 theta) = 1 $"],
            }

        if "sum_and_difference" in t_low or "sum and difference" in t_low or "sum_difference" in t_low or "angle_sum" in t_low:
            fn_t = rng.choice(["sin", "cos", "tan"])
            ang_list = [
                ("15", "45", "-", "30", "sqrt(6) - sqrt(2)", "4", "sqrt(6) + sqrt(2)", "4", "2 - sqrt(3)"),
                ("75", "45", "+", "30", "sqrt(6) + sqrt(2)", "4", "sqrt(6) - sqrt(2)", "4", "2 + sqrt(3)"),
                ("105", "60", "+", "45", "sqrt(6) + sqrt(2)", "4", "-(sqrt(6) - sqrt(2))", "4", "-(2 + sqrt(3))"),
                ("165", "135", "+", "30", "sqrt(6) - sqrt(2)", "4", "-(sqrt(6) + sqrt(2))", "4", "-(2 - sqrt(3))"),
                ("195", "225", "-", "30", "-(sqrt(6) - sqrt(2))", "4", "-(sqrt(6) + sqrt(2))", "4", "2 - sqrt(3)"),
                ("255", "225", "+", "30", "-(sqrt(6) + sqrt(2))", "4", "-(sqrt(6) - sqrt(2))", "4", "2 + sqrt(3)"),
                ("285", "315", "-", "30", "-(sqrt(6) + sqrt(2))", "4", "sqrt(6) - sqrt(2)", "4", "-(2 + sqrt(3))"),
                ("345", "315", "+", "30", "-(sqrt(6) - sqrt(2))", "4", "sqrt(6) + sqrt(2)", "4", "-(2 - sqrt(3))"),
            ]
            ang_name, ang1, sign_op, ang2, s_num, s_den, c_num, c_den, tan_val = rng.choice(ang_list)
            k_mult = rng.choice([1, 2, 3, 4, 5])
            if fn_t == "sin":
                ans_str = f"$ ({s_num}) / ({s_den}) $" if k_mult == 1 else f"$ ({k_mult}({s_num})) / ({s_den}) $"
                id_formula = f"sin(alpha {sign_op} beta) = sin(alpha) cos(beta) {sign_op} cos(alpha) sin(beta)"
            elif fn_t == "cos":
                ans_str = f"$ ({c_num}) / ({c_den}) $" if k_mult == 1 else f"$ ({k_mult}({c_num})) / ({c_den}) $"
                rev_sign = "-" if sign_op == "+" else "+"
                id_formula = f"cos(alpha {sign_op} beta) = cos(alpha) cos(beta) {rev_sign} sin(alpha) sin(beta)"
            else:
                ans_str = f"$ {tan_val} $" if k_mult == 1 else f"$ {k_mult}({tan_val}) $"
                id_formula = f"tan(alpha {sign_op} beta) = (tan(alpha) {sign_op} tan(beta)) / (1 {'-' if sign_op == '+' else '+'} tan(alpha) tan(beta))"

            prefix = f"{k_mult} " if k_mult > 1 else ""
            return {
                "prompt_text": f"Use the sum or difference identity to find the exact value of {prefix}{fn_t}({ang_name}°).",
                "equation_typst": f"$ {prefix}{fn_t}({ang_name}°) = {prefix}{fn_t}({ang1}° {sign_op} {ang2}°) $",
                "answer_typst": ans_str,
                "steps_typst": [
                    f"Express ${ang_name}°$ as a sum or difference of special angles: ${ang1}° {sign_op} {ang2}°$.",
                    f"Apply identity ${id_formula}$.",
                    f"Substitute exact values of special angles and simplify to find ${ans_str.replace('$', '')}$.",
                ],
                "distractors": [f"$ ({s_num}) / 2 $", "$ 1/2 $", "$ (sqrt(3))/2 $"],
            }
        if "identities" in t_low:
            id_family = rng.choice(["pyth_sin_cos", "pyth_sec_tan", "quotient", "reciprocal"])
            k = rng.randint(2, 20)
            if id_family == "pyth_sec_tan":
                return {
                    "prompt_text": "Simplify the trigonometric expression using fundamental identities.",
                    "equation_typst": f"$ {k} sec^2(theta) - {k} tan^2(theta) $",
                    "answer_typst": f"$ {k} $",
                    "steps_typst": [
                        f"Factor out common factor ${k}$: ${k}(sec^2(theta) - tan^2(theta))$.",
                        "Recall the identity $1 + tan^2(theta) = sec^2(theta) ==> sec^2(theta) - tan^2(theta) = 1$.",
                        f"Multiply: ${k}(1) = {k}$.",
                    ],
                    "distractors": [f"$ {k} csc^2(theta) $", "$ 1 $", f"$ {2 * k} $"],
                }
            elif id_family == "quotient":
                return {
                    "prompt_text": "Simplify the trigonometric expression using quotient and reciprocal identities.",
                    "equation_typst": f"$ {k} cos(theta) tan(theta) $",
                    "answer_typst": f"$ {k} sin(theta) $",
                    "steps_typst": [
                        "Use quotient identity $tan(theta) = sin(theta)/cos(theta)$.",
                        f"Substitute: ${k} cos(theta) times (sin(theta)/cos(theta))$.",
                        f"Cancel $cos(theta)$: ${k} sin(theta)$.",
                    ],
                    "distractors": [f"$ {k} cos(theta) $", f"$ {k} $", f"$ {k} sec(theta) $"],
                }
            elif id_family == "reciprocal":
                return {
                    "prompt_text": "Simplify the trigonometric expression using reciprocal identities.",
                    "equation_typst": f"$ {k} sin(theta) csc(theta) $",
                    "answer_typst": f"$ {k} $",
                    "steps_typst": [
                        "Use reciprocal identity $csc(theta) = 1 / sin(theta)$.",
                        f"Substitute: ${k} sin(theta) times (1 / sin(theta))$.",
                        f"Result: ${k}$.",
                    ],
                    "distractors": [f"$ {k} sin^2(theta) $", "$ 1 $", f"$ {k} cot(theta) $"],
                }
            else:
                return {
                    "prompt_text": "Simplify the trigonometric expression using fundamental identities.",
                    "equation_typst": f"$ {k} sin^2(theta) + {k} cos^2(theta) $",
                    "answer_typst": f"$ {k} $",
                    "steps_typst": [
                        f"Factor out common factor ${k}$: ${k}(sin^2(theta) + cos^2(theta))$.",
                        "Apply Pythagorean identity $sin^2(theta) + cos^2(theta) = 1$.",
                        f"Result: ${k}(1) = {k}$.",
                    ],
                    "distractors": [f"$ {k} tan^2(theta) $", "$ 1 $", f"$ {2 * k} $"],
                }

        if "equation" in t_low:
            eq_pool = [
                ("2 sin(theta) - 1 = 0", "(pi)/(6), (5pi)/(6)", "I and II", "pi/6"),
                ("2 sin(theta) + 1 = 0", "(7pi)/(6), (11pi)/(6)", "III and IV", "pi/6"),
                ("2 sin(theta) - sqrt(2) = 0", "(pi)/(4), (3pi)/(4)", "I and II", "pi/4"),
                ("2 sin(theta) + sqrt(2) = 0", "(5pi)/(4), (7pi)/(4)", "III and IV", "pi/4"),
                ("2 sin(theta) - sqrt(3) = 0", "(pi)/(3), (2pi)/(3)", "I and II", "pi/3"),
                ("2 sin(theta) + sqrt(3) = 0", "(4pi)/(3), (5pi)/(3)", "III and IV", "pi/3"),
                ("2 cos(theta) - 1 = 0", "(pi)/(3), (5pi)/(3)", "I and IV", "pi/3"),
                ("2 cos(theta) + 1 = 0", "(2pi)/(3), (4pi)/(3)", "II and III", "pi/3"),
                ("2 cos(theta) - sqrt(2) = 0", "(pi)/(4), (7pi)/(4)", "I and IV", "pi/4"),
                ("2 cos(theta) + sqrt(2) = 0", "(3pi)/(4), (5pi)/(4)", "II and III", "pi/4"),
                ("2 cos(theta) - sqrt(3) = 0", "(pi)/(6), (11pi)/(6)", "I and IV", "pi/6"),
                ("2 cos(theta) + sqrt(3) = 0", "(5pi)/(6), (7pi)/(6)", "II and III", "pi/6"),
                ("tan(theta) - 1 = 0", "(pi)/(4), (5pi)/(4)", "I and III", "pi/4"),
                ("tan(theta) + 1 = 0", "(3pi)/(4), (7pi)/(4)", "II and IV", "pi/4"),
                ("sqrt(3) tan(theta) - 1 = 0", "(pi)/(6), (7pi)/(6)", "I and III", "pi/6"),
                ("tan(theta) - sqrt(3) = 0", "(pi)/(3), (4pi)/(3)", "I and III", "pi/3"),
                ("2 sin^2(theta) - sin(theta) = 0", "0, (pi)/(6), (5pi)/(6), pi", "I and II with axis", "pi/6"),
                ("2 cos^2(theta) - cos(theta) = 0", "(pi)/(3), (pi)/(2), (3pi)/(2), (5pi)/(3)", "I and IV with axis", "pi/3"),
                ("2 sin^2(theta) + 3 sin(theta) + 1 = 0", "(7pi)/(6), (3pi)/(2), (11pi)/(6)", "III and IV", "pi/6"),
                ("2 cos^2(theta) + cos(theta) - 1 = 0", "(pi)/(3), pi, (5pi)/(3)", "I and IV", "pi/3"),
                ("4 sin^2(theta) - 3 = 0", "(pi)/(3), (2pi)/(3), (4pi)/(3), (5pi)/(3)", "all quadrants", "pi/3"),
                ("4 cos^2(theta) - 3 = 0", "(pi)/(6), (5pi)/(6), (7pi)/(6), (11pi)/(6)", "all quadrants", "pi/6"),
                ("tan^2(theta) - 3 = 0", "(pi)/(3), (2pi)/(3), (4pi)/(3), (5pi)/(3)", "all quadrants", "pi/3"),
                ("3 tan^2(theta) - 1 = 0", "(pi)/(6), (5pi)/(6), (7pi)/(6), (11pi)/(6)", "all quadrants", "pi/6"),
                ("sin(2 theta) - cos(theta) = 0", "(pi)/(6), (pi)/(2), (5pi)/(6), (3pi)/(2)", "double-angle substitution", "pi/6"),
                ("cos(2 theta) + sin(theta) = 0", "(pi)/(2), (7pi)/(6), (11pi)/(6)", "double-angle substitution", "pi/6"),
                ("cos(2 theta) - cos(theta) = 0", "0, (2pi)/(3), (4pi)/(3)", "double-angle substitution", "pi/3"),
            ]
            c_factor = rng.choice([1, 2, 3, 5])
            eq_s, ans_str, quad_str, ref_ang = rng.choice(eq_pool)
            if c_factor > 1:
                lhs = eq_s.split("=")[0].strip()
                eq_s = f"{c_factor}({lhs}) = 0"

            return {
                "prompt_text": "Solve the trigonometric equation on the interval [0, 2pi).",
                "equation_typst": f"$ {eq_s} $",
                "answer_typst": f"$ theta = {ans_str} $",
                "steps_typst": [
                    f"Isolate or factor the trigonometric expression: ${eq_s}$.",
                    f"Reference angle is ${ref_ang}$, with solutions in Quadrants / positions: {quad_str}.",
                    f"All solutions in $[0, 2pi)$ in ascending order: $theta = {ans_str}$.",
                ],
                "distractors": [
                    "$ theta = (pi)/(6), (11pi)/(6) $",
                    "$ theta = (pi)/(3), (2pi)/(3) $",
                    "$ theta = 0, pi $",
                ],
            }
        if "inverse trig" in t_low:
            inv_pool = [
                ("arcsin(1/2)", "(pi)/(6)", "(pi)/(3)"),
                ("arcsin(-(1)/(2))", "-(pi)/(6)", "(7pi)/(6)"),
                ("arccos(1/2)", "(pi)/(3)", "(pi)/(6)"),
                ("arccos(-(1)/(2))", "(2pi)/(3)", "(pi)/(3)"),
                ("arctan(1)", "(pi)/(4)", "(pi)/(3)"),
                ("arctan(-1)", "-(pi)/(4)", "(3pi)/(4)"),
                ("arcsin((sqrt(3))/(2))", "(pi)/(3)", "(pi)/(6)"),
                ("arccos((sqrt(3))/(2))", "(pi)/(6)", "(pi)/(3)"),
                ("arctan(sqrt(3))", "(pi)/(3)", "(pi)/(6)"),
                ("arctan(-(sqrt(3)))", "-(pi)/(3)", "(2pi)/(3)"),
                ("arcsin((sqrt(2))/(2))", "(pi)/(4)", "(pi)/(2)"),
                ("arccos((sqrt(2))/(2))", "(pi)/(4)", "(3pi)/(4)"),
                ("arcsin(0)", "0", "pi"),
                ("arccos(0)", "(pi)/(2)", "0"),
                ("arctan(0)", "0", "(pi)/(2)"),
                ("arcsin(1)", "(pi)/(2)", "pi"),
                ("arccos(1)", "0", "(pi)/(2)"),
                ("arccos(-1)", "pi", "-(pi)/(2)"),
            ]
            expr, ans, dist1 = rng.choice(inv_pool)
            return {
                "prompt_text": "Evaluate the inverse trigonometric expression in radians (principal value).",
                "equation_typst": f"$ {expr} $",
                "answer_typst": f"$ {ans} $",
                "steps_typst": [
                    "Recall the principal range: $arcsin in [-pi/2, pi/2]$, $arccos in [0, pi]$, $arctan in (-pi/2, pi/2)$.",
                    f"Find angle $theta$ in the principal range whose ratio matches ${expr}$.",
                    f"Exact principal value: ${ans}$.",
                ],
                "distractors": [f"$ {dist1} $", f"$ -{ans} $", "$ (pi)/(2) $"],
            }
        if "multi-step trig" in t_low:
            h = rng.randint(10, 24) * scale
            return {
                "prompt_text": "Solve the multi-step right triangle trigonometry problem. Find x to the nearest tenth.",
                "equation_typst": f"$ \"Altitude\" h = {h}, quad angle A = 30°, quad angle B = 45°, quad \"find base \" x = A D + D B $",
                "answer_typst": f"$ x = {h}sqrt(3) + {h} approx {round(h * (math.sqrt(3) + 1), 1)} $",
                "steps_typst": [
                    f"In the $30°$-$60°$-$90°$ sub-triangle, $A D = {h} / tan(30°) = {h}sqrt(3)$.",
                    f"In the $45°$-$45°$-$90°$ sub-triangle, $D B = {h} / tan(45°) = {h}$.",
                    f"Sum the two segments: $x = {h}sqrt(3) + {h} approx {round(h * (math.sqrt(3) + 1), 1)}$.",
                ],
                "distractors": [
                    f"$ {round(2 * h, 1)} $",
                    f"$ {round(h * math.sqrt(3), 1)} $",
                    f"$ {round(h * (math.sqrt(3) - 1), 1)} $",
                ],
                "diagram_svg": svg_right_triangle(a_label="x", b_label=str(h), theta_label="30°/45°"),
                "answer_svg": svg_right_triangle(a_label=f"x={round(h * (math.sqrt(3) + 1), 1)}", b_label=str(h), theta_label="30°/45°"),
            }

    # ------------------------------------------------------------------
    # X. POLYNOMIAL FUNCTIONS, FUNCTIONS, CONICS, SEQUENCES, VECTORS BASICS
    # ------------------------------------------------------------------
    if "conjugate roots" in t_low or "writing functions" in t_low or "writing polynomial functions" in t_low:
        r1 = rng.randint(1, 3 + scale)
        b_i = rng.randint(2, 4 + scale)
        return {
            "prompt_text": "Write a polynomial function f(x) of least degree with real coefficients and the given zeros.",
            "equation_typst": f"$ \"Zeros: \" x = {r1}, quad x = {b_i}i $",
            "answer_typst": f"$ f(x) = (x - {r1})(x^2 + {b_i * b_i}) = x^3 - {r1}x^2 + {b_i * b_i}x - {r1 * b_i * b_i} $",
            "steps_typst": [
                f"By the Complex Conjugate Root Theorem, $-{b_i}i$ is also a zero.",
                f"Multiply the conjugate factors: $(x - {b_i}i)(x + {b_i}i) = x^2 + {b_i * b_i}$.",
                f"Multiply by $(x - {r1})$: $x^3 - {r1}x^2 + {b_i * b_i}x - {r1 * b_i * b_i}$.",
            ],
            "distractors": [
                f"$ f(x) = x^3 + {r1}x^2 + {b_i * b_i}x + {r1 * b_i * b_i} $",
                f"$ f(x) = (x - {r1})(x^2 - {b_i * b_i}) $",
                f"$ f(x) = x^2 - {r1}x + {b_i} $",
            ],
        }

    if "factoring quadratic form" in t_low:
        a = rng.randint(1, 10)
        b = rng.randint(a + 1, a + 12)
        s = a * a + b * b
        p = (a * a) * (b * b)
        return {
            "prompt_text": "Factor the expression in quadratic form completely.",
            "equation_typst": f"$ x^4 - {s}x^2 + {p} $",
            "answer_typst": f"$ (x - {a})(x + {a})(x - {b})(x + {b}) $",
            "steps_typst": [
                f"Let $u = x^2$ to write $u^2 - {s}u + {p} = (u - {a * a})(u - {b * b})$.",
                f"Substitute back $u = x^2$: $(x^2 - {a * a})(x^2 - {b * b})$.",
                f"Factor each difference of squares: $(x - {a})(x + {a})(x - {b})(x + {b})$.",
            ],
            "distractors": [
                f"$ (x^2 + {a * a})(x^2 + {b * b}) $",
                f"$ (x - {a * a})(x - {b * b}) $",
                f"$ (x^2 - {a})(x^2 - {b}) $",
            ],
        }

    if "solving polynomial equations" in t_low:
        r1 = rng.randint(1, 7)
        r2 = rng.choice([x for x in range(-7, 8) if x != 0 and x != r1 and x != -r1])
        b_c = -(r1 + r2)
        c_c = r1 * r2
        b_str = f"+ {b_c}x^2" if b_c > 0 else (f"- {abs(b_c)}x^2" if b_c < 0 else "")
        c_str = f"+ {c_c}x" if c_c > 0 else (f"- {abs(c_c)}x" if c_c < 0 else "")
        eq_str = f"x^3 {b_str} {c_str} = 0".replace("  ", " ").strip()
        ans_roots = sorted([0, r1, r2])
        return {
            "prompt_text": "Find all real solutions of the polynomial equation by factoring.",
            "equation_typst": f"$ {eq_str} $",
            "answer_typst": f"$ x = {', '.join(str(r) for r in ans_roots)} $",
            "steps_typst": [
                f"Factor out common factor $x$: $x(x^2 {'+' if b_c >= 0 else '-'} {abs(b_c)}x {'+' if c_c >= 0 else '-'} {abs(c_c)}) = 0$.",
                f"Factor the quadratic factor: $x(x - {r1})(x - {r2}) = 0$.",
                f"Apply Zero Product Property: $x = {', '.join(str(r) for r in ans_roots)}$.",
            ],
            "distractors": [
                f"$ x = {-r1}, {-r2} $",
                f"$ x = {r1}, {r2} $",
                f"$ x = 0, {r1 * r2} $",
            ],
        }

    if "power functions" in t_low:
        k = rng.randint(2, 5 * scale)
        p = rng.choice([2, 3, 4])
        x0 = rng.randint(2, 3)
        val = k * (x0 ** p)
        return {
            "prompt_text": "Identify the constant of variation and exponent of the power function, and evaluate f(x_0).",
            "equation_typst": f"$ f(x) = {k}x^{p}, quad x_0 = {x0} $",
            "answer_typst": f"$ k = {k}, quad p = {p}, quad f({x0}) = {val} $",
            "steps_typst": [
                f"Match $f(x) = {k}x^{p}$ with standard power function form $f(x) = k x^p$: $k = {k}, p = {p}$.",
                f"Substitute $x = {x0}$: $f({x0}) = {k}({x0})^{p}$.",
                f"Evaluate: ${k} times {x0 ** p} = {val}$.",
            ],
            "distractors": [
                f"$ k = {p}, quad p = {k}, quad f({x0}) = {val} $",
                f"$ k = {k}, quad p = {p}, quad f({x0}) = {(k * x0) ** p} $",
                f"$ k = {k}, quad p = {p}, quad f({x0}) = {k * p * x0} $",
            ],
        }

    if "average rates of change" in t_low:
        a = rng.randint(1, 3 * scale)
        x1 = 1
        x2 = rng.randint(3, 5)
        y1 = a * x1 * x1
        y2 = a * x2 * x2
        arc = (y2 - y1) // (x2 - x1)
        return {
            "prompt_text": "Find the average rate of change of the function over the given interval.",
            "equation_typst": f"$ f(x) = {a}x^2 quad \"on\" [{x1}, {x2}] $",
            "answer_typst": f"$ \"ARC\" = {arc} $",
            "steps_typst": [
                f"Evaluate at the endpoints: $f({x1}) = {y1}$ and $f({x2}) = {y2}$.",
                f"Use $(f({x2}) - f({x1})) / ({x2} - {x1}) = ({y2} - {y1}) / ({x2 - x1})$.",
                f"Simplify: ${arc}$.",
            ],
            "distractors": [f"$ {y2 - y1} $", f"$ {2 * a * x1} $", f"$ {arc + a} $"],
        }

    if "circles, writing equations" in t_low:
        h = rng.randint(-5, 5) * scale
        k = rng.randint(-5, 5)
        r = rng.randint(2, 6 + scale)
        hs = f"(x - {h})^2" if h > 0 else (f"(x + {abs(h)})^2" if h < 0 else "x^2")
        ks = f"(y - {k})^2" if k > 0 else (f"(y + {abs(k)})^2" if k < 0 else "y^2")
        return {
            "prompt_text": "Write the standard form equation of the circle with the given center and radius.",
            "equation_typst": f"$ \"Center\": ({h}, {k}), quad r = {r} $",
            "answer_typst": f"$ {hs} + {ks} = {r * r} $",
            "steps_typst": [
                "Start with standard circle form $(x - h)^2 + (y - k)^2 = r^2$.",
                f"Substitute $h = {h}, k = {k}$: ${hs} + {ks}$.",
                f"Square the radius $r^2 = {r}^2 = {r * r}$: ${hs} + {ks} = {r * r}$.",
            ],
            "distractors": [
                f"$ {hs} + {ks} = {r} $",
                f"$ (x + {h})^2 + (y + {k})^2 = {r * r} $",
                f"$ {hs} - {ks} = {r * r} $",
            ],
        }

    if "systems of quadratic equations" in t_low:
        r = rng.randint(1, 8)
        c = rng.randint(-10, 10)
        c_str = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
        y_val = r * r + c
        return {
            "prompt_text": "Solve the system of quadratic equations.",
            "equation_typst": f"$ cases(y = x^2 {c_str}, y = {y_val}) $",
            "answer_typst": f"$ (-{r}, {y_val}) \" and \" ({r}, {y_val}) $",
            "steps_typst": [
                f"Substitute $y = {y_val}$ into $y = x^2 {c_str}$: $x^2 {c_str} = {y_val}$.",
                f"Isolate $x^2$: $x^2 = {r * r} arrow.r.double x = plus.minus {r}$.",
                f"Intersection points: $(-{r}, {y_val})$ and $({r}, {y_val})$.",
            ],
            "distractors": [
                f"$ ({r}, {y_val}) \" only\" $",
                f"$ (plus.minus {y_val}, {r}) $",
                "$ \"No real intersection\" $",
            ],
        }

    if "rotations of conic sections" in t_low:
        rot_case = rng.choice(["45_deg", "30_deg", "60_deg", "general"])
        if rot_case == "30_deg":
            return {
                "prompt_text": "Find the acute angle of rotation theta (0° < theta < 90°) that eliminates the xy-term.",
                "equation_typst": "$ x^2 + 2 sqrt(3) x y + 3 y^2 - 12 = 0 $",
                "answer_typst": "$ theta = 30° $",
                "steps_typst": [
                    "Identify $A = 1, B = 2 sqrt(3), C = 3$.",
                    "Use $\\cot(2 theta) = (A - C)/B = (1 - 3)/(2 sqrt(3)) = -1/sqrt(3)$.",
                    "Then $2 theta = 120° ==> theta = 60°$ or choose acute angle $theta = 30°$.",
                ],
                "distractors": ["$ theta = 45° $", "$ theta = 60° $", "$ theta = 15° $"],
            }
        elif rot_case == "60_deg":
            return {
                "prompt_text": "Find the acute angle of rotation theta (0° < theta < 90°) that eliminates the xy-term.",
                "equation_typst": "$ 3 x^2 + 2 sqrt(3) x y + y^2 - 16 = 0 $",
                "answer_typst": "$ theta = 30° $",
                "steps_typst": [
                    "Identify $A = 3, B = 2 sqrt(3), C = 1$.",
                    "Use $\\cot(2 theta) = (A - C)/B = (3 - 1)/(2 sqrt(3)) = 1/sqrt(3)$.",
                    "Since $\\cot(2 theta) = 1/sqrt(3)$, $2 theta = 60° ==> theta = 30°$.",
                ],
                "distractors": ["$ theta = 45° $", "$ theta = 60° $", "$ theta = 15° $"],
            }
        else:
            b_coef = rng.randint(2, 20)
            const_k = rng.randint(4, 30)
            return {
                "prompt_text": "Find the acute angle of rotation theta (0° < theta < 90°) that eliminates the xy-term.",
                "equation_typst": f"$ x^2 + {b_coef}x y + y^2 - {const_k} = 0 $",
                "answer_typst": "$ theta = 45° $",
                "steps_typst": [
                    f"Identify $A = 1, B = {b_coef}, C = 1$.",
                    f"Use $\\cot(2 theta) = (A - C)/B = (1 - 1)/{b_coef} = 0$.",
                    "Since $\\cot(2 theta) = 0$, $2 theta = 90° ==> theta = 45°$.",
                ],
                "distractors": ["$ theta = 30° $", "$ theta = 60° $", "$ theta = 90° $"],
            }

    if "general sequences" in t_low or "general series" in t_low or "power series" in t_low:
        c = rng.randint(2, 30)
        a_coef = rng.randint(2, 7)
        if "power series" in t_low:
            x0_shift = rng.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
            x_term = "x" if x0_shift == 0 else (f"(x - {x0_shift})" if x0_shift > 0 else f"(x + {abs(x0_shift)})")
            int_left = x0_shift - c
            int_right = x0_shift + c
            return {
                "prompt_text": "Find the radius and interval of convergence of the geometric power series.",
                "equation_typst": f"$ sum_(n=0)^infinity ({x_term}/{c})^n $",
                "answer_typst": f"$ R = {c}, quad I = ({int_left}, {int_right}) $",
                "steps_typst": [
                    f"This is a geometric series with common ratio $r = {x_term}/{c}$.",
                    f"Convergence requires $|r| < 1 ==> |{x_term}| < {c}$.",
                    f"Radius $R = {c}$, and interval of convergence $I = ({int_left}, {int_right})$.",
                ],
                "distractors": [
                    f"$ R = 1/({c}), quad I = (-{c}, {c}) $",
                    f"$ R = {c}, quad I = [{int_left}, {int_right}] $",
                    "$ R = infinity, quad I = (-infinity, infinity) $",
                ],
            }
        if "series" in t_low:
            seq_family = rng.choice(["quadratic", "linear", "geometric"])
            if seq_family == "linear":
                terms = [a_coef * n + c for n in range(1, 5)]
                s = sum(terms)
                return {
                    "prompt_text": "Evaluate the finite arithmetic series by expanding the summation.",
                    "equation_typst": f"$ sum_(n=1)^4 ({a_coef}n + {c}) $",
                    "answer_typst": f"$ {s} $",
                    "steps_typst": [
                        f"Substitute $n = 1, 2, 3, 4$: ${' + '.join(str(t) for t in terms)}$.",
                        f"Evaluate the terms: $a_1={terms[0]}, a_2={terms[1]}, a_3={terms[2]}, a_4={terms[3]}$.",
                        f"Sum: ${s}$.",
                    ],
                    "distractors": [f"$ {s + a_coef} $", f"$ {s - c} $", f"$ {4 * terms[0]} $"],
                }
            elif seq_family == "geometric":
                r_geo = rng.choice([2, 3])
                terms = [a_coef * (r_geo ** (n - 1)) for n in range(1, 5)]
                s = sum(terms)
                return {
                    "prompt_text": "Evaluate the finite geometric series.",
                    "equation_typst": f"$ sum_(n=1)^4 {a_coef}({r_geo})^(n-1) $",
                    "answer_typst": f"$ {s} $",
                    "steps_typst": [
                        f"Terms: $a_1={terms[0]}, a_2={terms[1]}, a_3={terms[2]}, a_4={terms[3]}$.",
                        f"Sum of terms: ${' + '.join(str(t) for t in terms)} = {s}$.",
                        f"Formula check: $S_4 = ({terms[0]}(1 - {r_geo}^4)) / (1 - {r_geo}) = {s}$.",
                    ],
                    "distractors": [f"$ {s + terms[0]} $", f"$ {terms[-1]} $", f"$ {s * 2} $"],
                }
            else:
                terms = [n * n + c for n in range(1, 5)]
                s = sum(terms)
                return {
                    "prompt_text": "Evaluate the finite series by expanding the summation.",
                    "equation_typst": f"$ sum_(n=1)^4 (n^2 + {c}) $",
                    "answer_typst": f"$ {s} $",
                    "steps_typst": [
                        f"Substitute $n = 1, 2, 3, 4$: $({1 + c}) + ({4 + c}) + ({9 + c}) + ({16 + c})$.",
                        f"Group terms: $(1 + 4 + 9 + 16) + 4({c}) = 30 + {4 * c}$.",
                        f"Sum = ${s}$.",
                    ],
                    "distractors": [f"$ {30 + c} $", f"$ {s + 4} $", f"$ {16 + c} $"],
                }

        seq_type = rng.choice(["linear", "quadratic", "alternating"])
        if seq_type == "linear":
            t1, t2, t3, t4 = [a_coef * n + c for n in range(1, 5)]
            return {
                "prompt_text": "Find the first four terms of the arithmetic sequence given by the explicit formula.",
                "equation_typst": f"$ a_n = {a_coef}n + {c} $",
                "answer_typst": f"$ {t1}, {t2}, {t3}, {t4} $",
                "steps_typst": [
                    f"Substitute $n = 1, 2$: $a_1 = {a_coef}(1) + {c} = {t1}$, $a_2 = {a_coef}(2) + {c} = {t2}$.",
                    f"Substitute $n = 3, 4$: $a_3 = {a_coef}(3) + {c} = {t3}$, $a_4 = {a_coef}(4) + {c} = {t4}$.",
                    f"First four terms: ${t1}, {t2}, {t3}, {t4}$.",
                ],
                "distractors": [f"$ {c}, {t1}, {t2}, {t3} $", f"$ {t1 + 1}, {t2 + 1}, {t3 + 1}, {t4 + 1} $", f"$ {a_coef}, {a_coef * 2}, {a_coef * 3}, {a_coef * 4} $"],
            }
        elif seq_type == "alternating":
            t1, t2, t3, t4 = [((-1) ** n) * (a_coef * n) for n in range(1, 5)]
            return {
                "prompt_text": "Find the first four terms of the alternating sequence.",
                "equation_typst": f"$ a_n = (-1)^n ({a_coef}n) $",
                "answer_typst": f"$ {t1}, {t2}, {t3}, {t4} $",
                "steps_typst": [
                    f"For $n = 1$: $a_1 = (-1)^1({a_coef} times 1) = {t1}$.",
                    f"For $n = 2$: $a_2 = (-1)^2({a_coef} times 2) = {t2}$.",
                    f"For $n = 3, 4$: $a_3 = {t3}, a_4 = {t4}$.",
                ],
                "distractors": [f"$ {abs(t1)}, {abs(t2)}, {abs(t3)}, {abs(t4)} $", f"$ {-t1}, {-t2}, {-t3}, {-t4} $", f"$ {t1}, {t1 * 2}, {t1 * 3}, {t1 * 4} $"],
            }
        else:
            t1, t2, t3, t4 = [n * n + c for n in range(1, 5)]
            return {
                "prompt_text": "Find the first four terms of the sequence given by the explicit formula.",
                "equation_typst": f"$ a_n = n^2 + {c} $",
                "answer_typst": f"$ {t1}, {t2}, {t3}, {t4} $",
                "steps_typst": [
                    f"For $n = 1, 2$: $a_1 = 1^2 + {c} = {t1}$ and $a_2 = 2^2 + {c} = {t2}$.",
                    f"For $n = 3, 4$: $a_3 = 3^2 + {c} = {t3}$ and $a_4 = 4^2 + {c} = {t4}$.",
                    f"First four terms: ${t1}, {t2}, {t3}, {t4}$.",
                ],
                "distractors": [
                    f"$ {c}, {t1}, {t2}, {t3} $",
                    f"$ {2 + c}, {4 + c}, {6 + c}, {8 + c} $",
                    f"$ {1 + c}, {2 + c}, {3 + c}, {4 + c} $",
                ],
            }

    if t_low == "basics" and "vectors" in c_low:
        vx = rng.choice([k for k in range(-15, 16) if k != 0])
        vy = rng.choice([k for k in range(-15, 16) if k != 0])
        mag_sq_2d = vx * vx + vy * vy
        mag_int = int(math.isqrt(mag_sq_2d))
        mag_2d_s = str(mag_int) if mag_int * mag_int == mag_sq_2d else f"sqrt({mag_sq_2d})"
        if "three-dimensional" in c_low:
            vz = rng.choice([k for k in range(-12, 13) if k != 0])
            mag_sq = vx * vx + vy * vy + vz * vz
            mag_3d_int = int(math.isqrt(mag_sq))
            mag_3d_s = str(mag_3d_int) if mag_3d_int * mag_3d_int == mag_sq else f"sqrt({mag_sq})"
            return {
                "prompt_text": "Find the magnitude ||v|| of the 3D vector v.",
                "equation_typst": f"$ bold(v) = chevron.l {vx}, {vy}, {vz} chevron.r $",
                "answer_typst": f"$ ||bold(v)|| = {mag_3d_s} $",
                "steps_typst": [
                    "Use 3D magnitude formula $||bold(v)|| = sqrt(v_x^2 + v_y^2 + v_z^2)$.",
                    f"Square components: $({vx})^2 + ({vy})^2 + ({vz})^2 = {vx * vx} + {vy * vy} + {vz * vz} = {mag_sq}$.",
                    f"Magnitude: $||bold(v)|| = {mag_3d_s}$.",
                ],
                "distractors": [f"$ {abs(vx) + abs(vy) + abs(vz)} $", f"$ {mag_sq} $", f"$ sqrt({vx * vx + vy * vy}) $"],
            }
        return {
            "prompt_text": "Find the magnitude ||v|| of the 2D vector.",
            "equation_typst": f"$ bold(v) = chevron.l {vx}, {vy} chevron.r $",
            "answer_typst": f"$ ||bold(v)|| = {mag_2d_s} $",
            "steps_typst": [
                "Use magnitude formula $||bold(v)|| = sqrt(v_x^2 + v_y^2)$.",
                f"Square and sum components: $({vx})^2 + ({vy})^2 = {vx * vx} + {vy * vy} = {mag_sq_2d}$.",
                f"Simplify: $||bold(v)|| = {mag_2d_s}$.",
            ],
            "distractors": [f"$ {abs(vx) + abs(vy)} $", f"$ {mag_sq_2d} $", f"$ {abs(vy - vx)} $"],
        }

    if "indefinite integrals" in t_low:
        a = rng.randint(1, 4 * scale)
        b = rng.randint(2, 6)
        return {
            "prompt_text": "Find the general indefinite integral.",
            "equation_typst": f"$ integral ({3 * a}x^2 + {2 * b}x) d x $",
            "answer_typst": f"$ {a}x^3 + {b}x^2 + C $",
            "steps_typst": [
                f"Integrate ${3 * a}x^2$ using the Power Rule: ${a}x^3$.",
                f"Integrate ${2 * b}x$ using the Power Rule: ${b}x^2$.",
                f"Add the constant of integration: ${a}x^3 + {b}x^2 + C$.",
            ],
            "distractors": [
                f"$ {6 * a}x + {2 * b} + C $",
                f"$ {3 * a}x^3 + {2 * b}x^2 + C $",
                f"$ {a}x^3 + {b}x^2 $",
            ],
        }

    if "volume of rectangular prism" in t_low or "solid figures: identifying" in t_low:
        ln = rng.randint(3, 6 * scale)
        w = rng.randint(2, 5 * scale)
        h = rng.randint(2, 4 * scale)
        vol = ln * w * h
        sa = 2 * (ln * w + ln * h + w * h)
        return {
            "prompt_text": "Find the volume and surface area of the rectangular prism.",
            "equation_typst": f"$ l = {ln}, quad w = {w}, quad h = {h} $",
            "answer_typst": f"$ V = {vol}, quad \"SA\" = {sa} $",
            "steps_typst": [
                f"Compute volume: $V = l w h = ({ln})({w})({h}) = {vol}$.",
                f"Compute surface area: $\"SA\" = 2(l w + l h + w h) = 2({ln * w} + {ln * h} + {w * h}) = {sa}$.",
                f"Volume $V = {vol}$, Surface Area = ${sa}$.",
            ],
            "distractors": [
                f"$ V = {sa}, quad \"SA\" = {vol} $",
                f"$ V = {ln + w + h}, quad \"SA\" = {ln * w + ln * h + w * h} $",
                f"$ V = {vol * 2}, quad \"SA\" = {sa} $",
            ],
            "diagram_svg": svg_solid_3d("prism", f"l={ln}", f"w={w}", f"h={h}"),
            "answer_svg": svg_solid_3d("prism", f"V={vol}", f"SA={sa}", ""),
        }

    if "circumference and area" in t_low:
        circ_mode = rng.choice(["given_radius", "given_diameter", "given_circ"])
        if circ_mode == "given_diameter":
            d = rng.randint(4, 50) * 2
            r = d // 2
            return {
                "prompt_text": "Find the exact circumference and area of the circle in terms of pi given diameter d.",
                "equation_typst": f"$ d = {d} $",
                "answer_typst": f"$ C = {d}pi, quad A = {r * r}pi $",
                "steps_typst": [
                    f"Find radius: $r = d / 2 = {d} / 2 = {r}$.",
                    f"Circumference: $C = pi d = {d}pi$.",
                    f"Area: $A = pi r^2 = pi ({r})^2 = {r * r}pi$.",
                ],
                "distractors": [f"$ C = {2 * d}pi, quad A = {d * d}pi $", f"$ C = {r}pi, quad A = {r * r}pi $", f"$ C = {d}pi, quad A = {2 * r}pi $"],
                "diagram_svg": svg_circle_diagram(radius_label=f"d = {d}"),
                "answer_svg": svg_circle_diagram(radius_label=f"C={d}pi, A={r * r}pi"),
            }
        elif circ_mode == "given_circ":
            r = rng.randint(3, 40)
            c_val = 2 * r
            return {
                "prompt_text": "Given the circumference of a circle, find its radius and exact area in terms of pi.",
                "equation_typst": f"$ C = {c_val}pi $",
                "answer_typst": f"$ r = {r}, quad A = {r * r}pi $",
                "steps_typst": [
                    f"Use circumference formula $C = 2 pi r = {c_val}pi ==> r = {c_val} / 2 = {r}$.",
                    f"Compute area: $A = pi r^2 = pi ({r})^2 = {r * r}pi$.",
                    f"Result: $r = {r}, A = {r * r}pi$.",
                ],
                "distractors": [f"$ r = {c_val}, quad A = {c_val * c_val}pi $", f"$ r = {r}, quad A = {c_val}pi $", f"$ r = {r // 2}, quad A = {r * r}pi $"],
                "diagram_svg": svg_circle_diagram(radius_label=f"C = {c_val}pi"),
                "answer_svg": svg_circle_diagram(radius_label=f"r={r}, A={r * r}pi"),
            }
        else:
            r = rng.randint(2, 45)
            return {
                "prompt_text": "Find the exact circumference and area of the circle in terms of pi.",
                "equation_typst": f"$ r = {r} $",
                "answer_typst": f"$ C = {2 * r}pi, quad A = {r * r}pi $",
                "steps_typst": [
                    f"Circumference formula $C = 2 pi r = 2 pi ({r}) = {2 * r}pi$.",
                    f"Area formula $A = pi r^2 = pi ({r})^2 = {r * r}pi$.",
                    f"Circumference = ${2 * r}pi$, Area = ${r * r}pi$.",
                ],
                "distractors": [
                    f"$ C = {r * r}pi, quad A = {2 * r}pi $",
                    f"$ C = {r}pi, quad A = {2 * r}pi $",
                    f"$ C = {2 * r}pi, quad A = {4 * r * r}pi $",
                ],
                "diagram_svg": svg_circle_diagram(radius_label=f"r = {r}"),
                "answer_svg": svg_circle_diagram(radius_label=f"C={2*r}pi, A={r*r}pi"),
            }

    if "angle bisectors" in t_low and "triangle" in c_low:
        k = rng.randint(2, 4 * scale)
        ab, ac = 3 * k, 5 * k
        bd = 3 * rng.randint(1, 3)
        dc_val = 5 * (bd // 3)
        return {
            "prompt_text": "Ray AD bisects angle BAC in triangle ABC. Use the Triangle Angle Bisector Theorem to find DC.",
            "equation_typst": f"$ A B = {ab}, quad A C = {ac}, quad B D = {bd}, quad D C = x $",
            "answer_typst": f"$ x = {dc_val} $",
            "steps_typst": [
                "By the Triangle Angle Bisector Theorem, $(B D)/(D C) = (A B)/(A C)$.",
                f"Substitute the given side lengths: $({bd})/(x) = ({ab})/({ac})$.",
                f"Cross-multiply and solve: ${ab}x = {bd * ac} arrow.r.double x = {dc_val}$.",
            ],
            "distractors": [f"$ x = {bd + 2} $", f"$ x = {ac} $", f"$ x = {ab} $"],
            "diagram_svg": svg_general_triangle(side_c=f"AB={ab}", side_b=f"AC={ac}", side_a=f"BD={bd}, DC=x"),
            "answer_svg": svg_general_triangle(side_c=f"AB={ab}", side_b=f"AC={ac}", side_a=f"DC={dc_val}"),
        }

    if "geometric diagrams and notation" in t_low:
        deg = rng.randint(35, 75) + scale * 5
        sup = 180 - deg
        return {
            "prompt_text": "Use geometric notation and the linear pair diagram to find m angle DBC.",
            "equation_typst": f"$ angle A B D \" and \" angle D B C \" form a linear pair with \" m angle A B D = {deg}° $",
            "answer_typst": f"$ m angle D B C = {sup}° $",
            "steps_typst": [
                "Angles in a linear pair are supplementary (sum to $180°$).",
                f"Set up $m angle A B D + m angle D B C = 180° arrow.r.double {deg}° + m angle D B C = 180°$.",
                f"Subtract ${deg}°$: $m angle D B C = {sup}°$.",
            ],
            "distractors": [f"$ {90 - deg if deg < 90 else deg - 45}° $", f"$ {deg}° $", f"$ {sup + 10}° $"],
            "diagram_svg": svg_angle_diagram(angle_degrees=deg, mode="linear_pair", angle_label=f"{deg}°", interior_angle_label="?"),
            "answer_svg": svg_angle_diagram(angle_degrees=deg, mode="linear_pair", angle_label=f"{deg}°", interior_angle_label=f"{sup}°", shade=True, bottom_label=f"m∠DBC = {sup}°"),
        }

    if c_low in ("general functions", "functions"):
        if t_low == "evaluating":
            a = rng.randint(2, 4 * scale)
            b = rng.randint(1, 6)
            x0 = rng.randint(-3, 4)
            val = a * x0 * x0 - b
            return {
                "prompt_text": "Evaluate the function at the indicated input.",
                "equation_typst": f"$ f(x) = {a}x^2 - {b}; quad \"find \" f({x0}) $",
                "answer_typst": f"$ f({x0}) = {val} $",
                "steps_typst": [
                    f"Substitute $x = {x0}$ into $f(x) = {a}x^2 - {b}$.",
                    f"Compute ${a}({x0})^2 - {b} = {a * x0 * x0} - {b}$.",
                    f"Simplify: $f({x0}) = {val}$.",
                ],
                "distractors": [f"$ {a * x0 - b} $", f"$ {-a * x0 * x0 - b} $", f"$ {val + 2 * b} $"],
            }
        if t_low == "operations":
            a = rng.randint(2, 5 * scale)
            b = rng.randint(1, 6)
            c = rng.randint(2, 5)
            return {
                "prompt_text": "Perform the indicated function operation and simplify.",
                "equation_typst": f"$ f(x) = {a}x + {b}, quad g(x) = x^2 - {c}; quad \"find \" (f + g)(x) $",
                "answer_typst": f"$ x^2 + {a}x {'+ ' + str(b - c) if b - c >= 0 else '- ' + str(abs(b - c))} $",
                "steps_typst": [
                    "Use $(f + g)(x) = f(x) + g(x)$.",
                    f"Substitute: $({a}x + {b}) + (x^2 - {c})$.",
                    f"Combine constants in standard form: $x^2 + {a}x {'+ ' + str(b - c) if b - c >= 0 else '- ' + str(abs(b - c))}$.",
                ],
                "distractors": [
                    f"$ {a}x^2 + {b - c} $",
                    f"$ x^2 - {a}x {'+ ' + str(b + c)} $",
                    f"$ {a}x^3 - {b * c} $",
                ],
            }
        if t_low == "inverses" or ("inverse" in t_low and "matrices" in c_low):
            if "matrix" in c_low or "matrices" in c_low:
                candidate_mats = [
                    (3, 1, 5, 2), (2, 5, 1, 3), (4, 3, 3, 2), (5, 2, 2, 1),
                    (3, 2, 2, 2), (2, 1, 4, 3), (3, -1, -2, 1), (4, 1, 2, 1),
                    (2, 3, 1, 2), (3, 4, 1, 2), (2, 4, 1, 3), (1, 3, 2, 5),
                    (2, -1, 3, -1), (4, 2, 3, 2), (5, 3, 3, 2), (1, 4, 2, 7)
                ]
                a11, a12, a21, a22 = rng.choice(candidate_mats)
                det = a11 * a22 - a12 * a21
                inv_mat = f"mat({a22}, {-a12}; {-a21}, {a11})"
                ans_str = f"$ A^(-1) = (1)/({det}) {inv_mat} $" if det != 1 else f"$ A^(-1) = {inv_mat} $"
                return {
                    "prompt_text": "Find the inverse matrix A^-1, or state if it does not exist.",
                    "equation_typst": f"$ A = mat({a11}, {a12}; {a21}, {a22}) $",
                    "answer_typst": ans_str,
                    "steps_typst": [
                        f"Compute determinant: $det(A) = ({a11})({a22}) - ({a12})({a21}) = {det}$.",
                        "Since determinant is non-zero, the matrix is invertible.",
                        f"Apply inverse formula: $A^(-1) = (1)/(det(A)) mat(d, -b; -c, a) = {ans_str.replace('$', '').strip()}$.",
                    ],
                    "distractors": [
                        f"$ A^(-1) = mat({a11}, {-a12}; {-a21}, {a22}) $",
                        f"$ A^(-1) = (1)/({det + 2}) {inv_mat} $",
                        '$ "Does not exist" $',
                    ],
                }
            m = rng.choice([2, 3, 4, 5]) * scale
            b = rng.randint(1, 9)
            return {
                "prompt_text": "Find the inverse function f^-1(x).",
                "equation_typst": f"$ f(x) = {m}x - {b} $",
                "answer_typst": f"$ f^(-1)(x) = (x + {b})/({m}) $",
                "steps_typst": [
                    f"Replace $f(x)$ with $y$ and swap $x$ and $y$: $x = {m}y - {b}$.",
                    f"Add ${b}$ to both sides: $x + {b} = {m}y$.",
                    f"Divide by ${m}$: $f^(-1)(x) = (x + {b})/({m})$.",
                ],
                "distractors": [
                    f"$ f^(-1)(x) = (x - {b})/({m}) $",
                    f"$ f^(-1)(x) = (1)/({m}x - {b}) $",
                    f"$ f^(-1)(x) = {m}x + {b} $",
                ],
            }

    if "complex numbers" in c_low:
        if "rationalizing" in t_low:
            a = rng.randint(2, 5 * scale)
            b = rng.randint(1, 4)
            c = rng.randint(1, 4)
            denom = b * b + c * c
            re_f = Fraction(a * b, denom)
            im_f = Fraction(-a * c, denom)
            im_s = f"- {_fmt_frac( abs(im_f) )}i" if im_f < 0 else f"+ {_fmt_frac(im_f)}i"
            return {
                "prompt_text": "Divide the complex numbers by multiplying numerator and denominator by the complex conjugate.",
                "equation_typst": f"$ ({a})/({b} + {c}i) $",
                "answer_typst": f"$ {_fmt_frac(re_f)} {im_s} $",
                "steps_typst": [
                    f"Multiply numerator and denominator by the conjugate $({b} - {c}i)$.",
                    f"Denominator: $({b})^2 + ({c})^2 = {denom}$; Numerator: ${a}({b} - {c}i) = {a * b} - {a * c}i$.",
                    f"Write in standard form $a + b i$: ${_fmt_frac(re_f)} {im_s}$.",
                ],
                "distractors": [
                    f"$ {_fmt_frac(re_f)} + {_fmt_frac(abs(im_f))}i $",
                    f"$ ({a * b} - {a * c}i)/({b * b - c * c if b != c else 1}) $",
                    f"$ {_fmt_frac(Fraction(a, b))} - {_fmt_frac(Fraction(a, c))}i $",
                ],
            }

    if "gcf and lcm word problems" in t_low:
        scenarios = [
            ("Bus A arrives every {a} minutes and Bus B arrives every {b} minutes. If both arrive now, in how many minutes will both arrive together again?", "minutes"),
            ("Traffic Light 1 changes every {a} seconds and Traffic Light 2 changes every {b} seconds. In how many seconds will they change together?", "seconds"),
            ("Runner X laps the track every {a} seconds and Runner Y every {b} seconds. After how many seconds will they meet at the start line?", "seconds"),
            ("Bell 1 chimes every {a} hours and Bell 2 chimes every {b} hours. In how many hours will both chime simultaneously?", "hours"),
        ]
        sc_tpl, unit = rng.choice(scenarios)
        g = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        m, n = rng.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (3, 7)])
        a, b = m * g, n * g
        lcm_v = (a * b) // math.gcd(a, b)
        q_text = sc_tpl.format(a=a, b=b)
        return {
            "prompt_text": "Solve the GCF and LCM word problem.",
            "equation_typst": f"\"{q_text}\"",
            "answer_typst": f"$ {lcm_v} \" {unit}\" $",
            "steps_typst": [
                f"Find the Least Common Multiple (LCM) of ${a}$ and ${b}$.",
                f"Prime factorization / GCD: $\"gcd\"({a}, {b}) = {g}$.",
                f"LCM: $({a} times {b}) / {g} = {lcm_v}$ {unit}.",
            ],
            "distractors": [f"$ {g} \" {unit}\" $", f"$ {a + b} \" {unit}\" $", f"$ {a * b} \" {unit}\" $"],
        }

    if "properties of addition and multiplication" in t_low:
        a = rng.randint(3, 9 * scale)
        b = rng.randint(4, 11)
        c = rng.randint(2, 8)
        return {
            "prompt_text": "Identify the property of operations illustrated by the equation.",
            "equation_typst": f"$ ({a} + {b}) + {c} = {a} + ({b} + {c}) $",
            "answer_typst": "$ \"Associative Property of Addition\" $",
            "steps_typst": [
                f"Given expression: $({a} + {b}) + {c} = {a} + ({b} + {c})$.",
                f"Evaluate both groupings: $({a + b}) + {c} = {a + b + c}$ and ${a} + ({b + c}) = {a + b + c}$.",
                "Because changing parentheses grouping $(a + b) + c = a + (b + c)$ preserves sum equality, this illustrates the Associative Property of Addition.",
            ],
            "distractors": [
                "$ \"Commutative Property of Addition\" $",
                "$ \"Distributive Property\" $",
                "$ \"Identity Property of Addition\" $",
            ],
        }

    if "equations word problems" in t_low or "inequalities word problems" in t_low or "equations for other relationships" in t_low:
        rate = rng.randint(4, 9 * scale)
        fixed = rng.randint(5, 15)
        x_val = rng.randint(3, 8)
        tot = rate * x_val + fixed
        if "inequalit" in t_low:
            ineq_scenarios = [
                (r"A school club has \${fixed} and earns \${rate} per car washed. How many cars (x) must they wash to have at least \${tot}?", "cars", "wash"),
                (r"A student has \${fixed} in savings and earns \${rate} per hour tutoring. How many hours (x) must they tutor to have at least \${tot}?", "hours", "tutor"),
                (r"A sports team has \${fixed} in their travel fund and earns \${rate} per raffle ticket sold. How many tickets (x) must they sell to raise at least \${tot}?", "tickets", "sell"),
                (r"A community garden has \${fixed} and collects \${rate} per volunteer shift. How many shifts (x) are needed to collect at least \${tot}?", "shifts", "complete"),
            ]
            sc_text, unit_item, verb = rng.choice(ineq_scenarios)
            return {
                "prompt_text": "Write and solve an inequality to model the word problem.",
                "equation_typst": sc_text.format(fixed=fixed, rate=rate, tot=tot),
                "answer_typst": f"$ {rate}x + {fixed} >= {tot}; quad x >= {x_val} $",
                "steps_typst": [
                    f"Set up the inequality: ${rate}x + {fixed} >= {tot}$.",
                    f"Subtract ${fixed}$ from both sides: ${rate}x >= {tot - fixed}$.",
                    f"Divide by ${rate}$: $x >= {x_val}$.",
                ],
                "distractors": [
                    f"$ x <= {x_val} $",
                    f"$ x >= {x_val + 2} $",
                    f"$ x >= {(tot + fixed) // rate} $",
                ],
            }
        eq_scenarios = [
            (r"A service charges a \${fixed} base fee plus \${rate} per hour (x). For a total bill of y = \${tot}, find the hours x.", "hours"),
            (r"A bicycle rental service charges a \${fixed} reservation fee plus \${rate} per hour (x). For a total charge of y = \${tot}, find x.", "hours"),
            (r"A fitness center charges a \${fixed} registration fee plus \${rate} per month (x). For a total payment of y = \${tot}, find the months x.", "months"),
            (r"A canoe rental shop charges a \${fixed} deposit plus \${rate} per hour (x). For a total bill of y = \${tot}, find the hours x.", "hours"),
        ]
        sc_text, unit_item = rng.choice(eq_scenarios)
        return {
            "prompt_text": "Write and solve an equation for the relationship between the quantities.",
            "equation_typst": sc_text.format(fixed=fixed, rate=rate, tot=tot),
            "answer_typst": f"$ y = {rate}x + {fixed}; quad x = {x_val} $",
            "steps_typst": [
                f"Write the two-variable relationship: $y = {rate}x + {fixed}$.",
                f"Substitute $y = {tot}$: ${rate}x + {fixed} = {tot} arrow.r.double {rate}x = {tot - fixed}$.",
                f"Divide by ${rate}$: $x = {x_val}$.",
            ],
            "distractors": [
                f"$ y = {fixed}x + {rate}; quad x = {x_val} $",
                f"$ y = {rate}x + {fixed}; quad x = {x_val + 2} $",
                f"$ y = {rate}x - {fixed}; quad x = {(tot + fixed) // rate} $",
            ],
        }

    return None


class CurriculumTopicGenerator(BaseGenerator):
    """Dedicated topic-specific generator bound to an exact curriculum topic."""

    topic_id: str = ""
    topic_name: str = ""
    category_name: str = ""
    course_key: str = ""
    fallback_generator_id: str = "algebra_1.linear_equations"

    def generate(self, config: GeneratorConfig) -> List[BaseProblem]:
        rng = random.Random(config.seed)
        problems: List[BaseProblem] = []
        difficulties = self._select_difficulties(
            config.problem_count, config.difficulty_distribution, rng
        )

        # Fallback generator instance if needed
        from backend.app.generators import _BASE_GENERATOR_REGISTRY

        base_cls = _BASE_GENERATOR_REGISTRY.get(self.fallback_generator_id)
        base_probs: Dict[ProblemDifficulty, List[BaseProblem]] = {}

        seen_equations = set()
        for idx, diff in enumerate(difficulties):
            prob = None
            for attempt in range(50):
                if diff == ProblemDifficulty.MEDIUM:
                    rng.random()
                elif diff == ProblemDifficulty.SPICY:
                    rng.random()
                    rng.random()
                data = gen_alg_geo_problem(
                    self.topic_id,
                    self.topic_name,
                    self.category_name,
                    self.course_key,
                    diff,
                    rng,
                )
                if data is None:
                    data = gen_adv_problem(
                        self.topic_id,
                        self.topic_name,
                        self.category_name,
                        self.course_key,
                        diff,
                        rng,
                    )
                if data is None:
                    data = _gen_decoupled_subtopic(
                        self.topic_id,
                        self.topic_name,
                        self.category_name,
                        self.course_key,
                        diff,
                        rng,
                        self.fallback_generator_id,
                    )

                if data is not None:
                    eq_key = data["equation_typst"].strip()
                    if eq_key not in seen_equations or attempt == 49:
                        seen_equations.add(eq_key)
                        prob = BaseProblem(
                            id=f"{self.topic_id.replace('.', '_')}_{idx + 1}_{rng.randint(1000, 9999)}",
                            prompt_text=data["prompt_text"],
                            equation_typst=data["equation_typst"],
                            answer_typst=data["answer_typst"],
                            steps_typst=data["steps_typst"],
                            distractors=data["distractors"],
                            difficulty=diff,
                            standards=self.standards,
                            diagram_svg=data.get("diagram_svg"),
                            answer_svg=data.get("answer_svg"),
                            generator_id=self.generator_id,
                            metadata={"topic_id": self.topic_id, "topic_name": self.topic_name},
                        )
                        break
                elif base_cls is not None:
                    if diff not in base_probs:
                        sub_cfg = GeneratorConfig(
                            problem_count=max(config.problem_count * 2, 4),
                            seed=(config.seed or 42) + idx * 31,
                            difficulty_distribution={
                                ProblemDifficulty.MILD: 1.0 if diff == ProblemDifficulty.MILD else 0.0,
                                ProblemDifficulty.MEDIUM: 1.0 if diff == ProblemDifficulty.MEDIUM else 0.0,
                                ProblemDifficulty.SPICY: 1.0 if diff == ProblemDifficulty.SPICY else 0.0,
                            },
                            allow_negatives=config.allow_negatives,
                            question_type=config.question_type,
                        )
                        base_probs[diff] = base_cls().generate(sub_cfg)
                    avail = [p for p in base_probs[diff] if p.equation_typst.strip() not in seen_equations]
                    chosen_bp = avail[0] if avail else base_probs[diff][idx % len(base_probs[diff])]
                    seen_equations.add(chosen_bp.equation_typst.strip())
                    prob = chosen_bp.model_copy(deep=True)
                    prob.generator_id = self.generator_id
                    prob.metadata["topic_id"] = self.topic_id
                    prob.metadata["topic_name"] = self.topic_name
                    break

            if prob is not None:
                prob.question_type = config.question_type
                if config.question_type == "multiple_choice" and not prob.choices:
                    self._populate_multiple_choice_choices(prob, rng)
                problems.append(prob)

        return problems

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True,
    ) -> BaseProblem:
        sub_cfg = GeneratorConfig(
            problem_count=1,
            seed=rng.randint(1, 999999),
            difficulty_distribution={
                ProblemDifficulty.MILD: 1.0 if difficulty == ProblemDifficulty.MILD else 0.0,
                ProblemDifficulty.MEDIUM: 1.0 if difficulty == ProblemDifficulty.MEDIUM else 0.0,
                ProblemDifficulty.SPICY: 1.0 if difficulty == ProblemDifficulty.SPICY else 0.0,
            },
            allow_negatives=allow_negatives,
        )
        return self.generate(sub_cfg)[0]

    def _select_difficulties(
        self,
        count: int,
        dist: Dict[ProblemDifficulty, float],
        rng: random.Random,
    ) -> List[ProblemDifficulty]:
        population = list(dist.keys())
        weights = list(dist.values())
        if sum(weights) <= 0:
            return [ProblemDifficulty.MEDIUM] * count
        return rng.choices(population, weights=weights, k=count)


def build_topic_generator_registry(
    catalog: Dict[str, Dict[str, Any]],
) -> Dict[str, Type[BaseGenerator]]:
    """Dynamically construct a dedicated BaseGenerator class for every topic in COURSE_CATALOG."""
    registry: Dict[str, Type[BaseGenerator]] = {}
    for course_key, course in catalog.items():
        for category in course.get("categories", []):
            cat_name = category["name"]
            for topic in category.get("topics", []):
                t_id = topic["id"]
                t_name = topic["name"]
                fb_id = topic.get("fallback_generator_id", topic.get("generator_id", "algebra_1.linear_equations"))
                cls_name = "TopicGen_" + "".join(c if c.isalnum() else "_" for c in t_id)
                gen_cls: Type[BaseGenerator] = type(
                    cls_name,
                    (CurriculumTopicGenerator,),
                    {
                        "generator_id": t_id,
                        "name": f"{cat_name}: {t_name}",
                        "category": course_key,
                        "standards": ["CCSS-M"],
                        "topic_id": t_id,
                        "topic_name": t_name,
                        "category_name": cat_name,
                        "course_key": course_key,
                        "fallback_generator_id": fb_id,
                    },
                )
                registry[t_id] = gen_cls
    return registry
