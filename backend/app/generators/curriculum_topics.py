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
    svg_circle_diagram,
    svg_coordinate_plane,
    svg_data_table,
    svg_general_triangle,
    svg_number_line,
    svg_parallel_transversal,
    svg_polygon_diagram,
    svg_right_triangle,
)
from backend.app.generators.topic_generators_adv import gen_adv_problem
from backend.app.generators.topic_generators_alg_geo import (
    _fmt_frac,
    gen_alg_geo_problem,
)


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
    lram: Any

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
        if "inverse trigonometric" in t_low:
            a = rng.randint(2, 4 * scale)
            return {
                "prompt_text": "Differentiate the inverse trigonometric function.",
                "equation_typst": f"$ f(x) = arcsin({a}x) $" if scale < 3 else f"$ f(x) = arctan({a}x) $",
                "answer_typst": f"$ f'(x) = ({a})/(sqrt(1 - {a * a}x^2)) $" if scale < 3 else f"$ f'(x) = ({a})/(1 + {a * a}x^2) $",
                "steps_typst": [
                    "Recall $d/(d x)[arcsin(u)] = u' / sqrt(1 - u^2)$ and $d/(d x)[arctan(u)] = u' / (1 + u^2)$.",
                    f"Here $u = {a}x$ and $u' = {a}$, with $u^2 = {a * a}x^2$.",
                    "Substitute $u$ and $u'$ into the inverse trigonometric derivative formula.",
                ],
                "distractors": [
                    f"$ f'(x) = (1)/(sqrt(1 - {a * a}x^2)) $",
                    f"$ f'(x) = ({a})/(1 - {a * a}x^2) $",
                    f"$ f'(x) = arccos({a}x) $",
                ],
            }
        if "trigonometric" in t_low:
            a = rng.randint(2, 3 * scale)
            c = rng.randint(1, 5)
            return {
                "prompt_text": "Differentiate the trigonometric function with respect to x.",
                "equation_typst": f"$ f(x) = {c} sin({a}x) $",
                "answer_typst": f"$ f'(x) = {c * a} cos({a}x) $",
                "steps_typst": [
                    "Use $d/(d x)[sin(u)] = cos(u) dot u'$.",
                    f"Multiply the outer coefficient ${c}$ by the inner derivative ${a}$.",
                    f"Result: $f'(x) = {c * a} cos({a}x)$.",
                ],
                "distractors": [
                    f"$ f'(x) = -{c * a} cos({a}x) $",
                    f"$ f'(x) = {c} cos({a}x) $",
                    f"$ f'(x) = {c * a} sin({a}x) $",
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
            c = rng.randint(1, 3 * scale)
            return {
                "prompt_text": "Find the critical numbers and intervals of increase/decrease (or local extrema) for f(x).",
                "equation_typst": f"$ f(x) = x^3 - {3 * c * c}x $",
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
            a = rng.randint(-3 * scale, 3 * scale)
            b = 3 * a
            s_b = f"- {b}x^2" if b >= 0 else f"+ {abs(b)}x^2"
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
            perim = rng.choice([20, 24, 32, 40, 48]) * scale
            side = perim // 4
            max_area = side * side
            return {
                "prompt_text": "Use calculus optimization to find the dimensions that maximize the objective quantity.",
                "equation_typst": f"\"Find the maximum area of a rectangle with perimeter \" P = {perim} \" units.\"",
                "answer_typst": f"$ x = y = {side}, quad A_\"max\" = {max_area} $",
                "steps_typst": [
                    f"From $2x + 2y = {perim}$, write $y = {perim // 2} - x$ and Area $A(x) = x({perim // 2} - x) = {perim // 2}x - x^2$.",
                    f"Set $A'(x) = {perim // 2} - 2x = 0 arrow.r.double x = {side}$.",
                    f"Then $y = {side}$ and maximum area $A = {side}^2 = {max_area}$.",
                ],
                "distractors": [
                    f"$ x = {perim // 2}, quad A_\"max\" = {perim * 2} $",
                    f"$ x = y = {side}, quad A_\"max\" = {perim} $",
                    f"$ x = {side - 2}, y = {side + 2}, quad A_\"max\" = {(side - 2) * (side + 2)} $",
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
            x0 = rng.randint(2, 5)
            dx = Fraction(1, 10 * scale)
            dy = Fraction(2 * x0, 1) * dx
            return {
                "prompt_text": "Find the differential dy = f'(x) dx for the given values of x and dx.",
                "equation_typst": f"$ y = x^2, quad x = {x0}, quad d x = {float(dx):g} $",
                "answer_typst": f"$ d y = {float(dy):g} $",
                "steps_typst": [
                    "Compute the derivative: $f'(x) = 2x$.",
                    f"Write the differential formula: $d y = 2x d x = 2({x0})({float(dx):g})$.",
                    f"Multiply: $d y = {float(dy):g}$.",
                ],
                "distractors": [
                    f"$ d y = {float(dx):g} $",
                    f"$ d y = {float(dy * 2):g} $",
                    f"$ d y = {x0 * x0 * float(dx):g} $",
                ],
            }

    # ------------------------------------------------------------------
    # C. CALCULUS LIMITS & CONTINUITY
    # ------------------------------------------------------------------
    if c_low in ("limits", "continuity") or ("introduction to calculus" in c_low and "limit" in t_low):
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
            a = rng.randint(2, 4 + scale)
            return {
                "prompt_text": "Evaluate the limit at the removable discontinuity by factoring and canceling.",
                "equation_typst": f"$ lim_(x arrow.r {a}) (x^2 - {a * a})/(x - {a}) $",
                "answer_typst": f"$ {2 * a} $",
                "steps_typst": [
                    f"Direct substitution gives $0/0$. Factor the numerator: $(x - {a})(x + {a}) / (x - {a})$.",
                    f"Cancel $(x - {a})$ for $x != {a}$ to obtain $lim_(x arrow.r {a}) (x + {a})$.",
                    f"Substitute $x = {a}$: ${a} + {a} = {2 * a}$.",
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
            a = rng.randint(1, 5 * scale)
            return {
                "prompt_text": "Find all points of discontinuity and classify each as removable, jump, or infinite.",
                "equation_typst": f"$ f(x) = (x - {a})/((x - {a})(x + {a})) $",
                "answer_typst": f"$ x = {a} \" (removable)\", quad x = -{a} \" (infinite)\" $",
                "steps_typst": [
                    f"Set the denominator to zero: $(x - {a})(x + {a}) = 0 arrow.r.double x = {a}, -{a}$.",
                    f"The factor $(x - {a})$ cancels with the numerator, so $x = {a}$ is a removable discontinuity.",
                    f"The factor $(x + {a})$ remains in the denominator, so $x = -{a}$ is an infinite discontinuity.",
                ],
                "distractors": [
                    f"$ x = {a} \" (infinite)\", quad x = -{a} \" (removable)\" $",
                    f"$ x = {a} \" (jump)\", quad x = -{a} \" (jump)\" $",
                    "$ \"Continuous everywhere\" $",
                ],
            }

    # ------------------------------------------------------------------
    # D. CALCULUS INTEGRATION SUBTOPICS
    # ------------------------------------------------------------------
    if "integration" in c_low or ("introduction to calculus" in c_low and ("area" in t_low or "integral" in t_low)):
        if "approximating area" in t_low:
            n = 4

            def _fn_area(x: float) -> float:
                return 0.25 * x * x + 1

            boxes = [(i, _fn_area(i), 1) for i in range(n)]
            lram = sum(i * i + 1 for i in range(n))
            return {
                "prompt_text": "Approximate the area under f(x) = x^2 + 1 on [0, 4] using a Left Riemann Sum with n = 4 subintervals.",
                "equation_typst": "$ integral_0^4 (x^2 + 1) d x quad (\"LRAM\", n = 4) $",
                "answer_typst": f"$ L_4 = {lram} $",
                "steps_typst": [
                    "Subinterval width is $Delta x = (4 - 0)/4 = 1$, with left endpoints $x = 0, 1, 2, 3$.",
                    "Evaluate $f(0) = 1, f(1) = 2, f(2) = 5, f(3) = 10$.",
                    f"Sum: $L_4 = 1(1 + 2 + 5 + 10) = {lram}$.",
                ],
                "distractors": [f"$ {lram + 16} $", f"$ {lram - 4} $", "$ 24 $"],
                "diagram_svg": svg_coordinate_plane(functions=[{"fn": _fn_area, "x_start": 0, "x_end": 4, "color": "#1d4ed8"}], riemann_boxes=boxes),
                "answer_svg": svg_coordinate_plane(functions=[{"fn": _fn_area, "x_start": 0, "x_end": 4, "color": "#1d4ed8"}], riemann_boxes=boxes),
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
            k = rng.randint(2, 3 + scale)
            return {
                "prompt_text": "Use the Second Fundamental Theorem of Calculus to differentiate the integral function.",
                "equation_typst": f"$ (d)/(d x) integral_1^(x^{k}) sqrt(t^3 + 1) d t $",
                "answer_typst": f"$ {k}x^{k - 1} sqrt(x^({3 * k}) + 1) $",
                "steps_typst": [
                    "By the Second Fundamental Theorem of Calculus with Chain Rule, $d/(d x) integral_a^(g(x)) f(t) d t = f(g(x)) dot g'(x)$.",
                    f"Substitute $t = x^{k}$ into $sqrt(t^3 + 1)$ to get $sqrt(x^({3 * k}) + 1)$.",
                    f"Multiply by $g'(x) = {k}x^{k - 1}$.",
                ],
                "distractors": [
                    f"$ sqrt(x^({3 * k}) + 1) $",
                    f"$ {k}x^{k - 1} sqrt(x^3 + 1) $",
                    "$ (3x^2)/(2 sqrt(x^3 + 1)) $",
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
            m = rng.randint(2, 5)
            k = rng.choice([2, 3, 4])
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
        triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
        opp, adj, hyp = rng.choice(triples)
        opp, adj, hyp = opp * scale, adj * scale, hyp * scale
        fn = rng.choice(["sin", "cos", "tan"])
        f = Fraction(opp, hyp) if fn == "sin" else (Fraction(adj, hyp) if fn == "cos" else Fraction(opp, adj))
        return {
            "prompt_text": "Find the value of the trigonometric ratio as a simplified fraction.",
            "equation_typst": f"$ {fn}(theta) quad (\"Opp\" = {opp}, \" Adj\" = {adj}, \" Hyp\" = {hyp}) $",
            "answer_typst": f"$ {fn}(theta) = {_fmt_frac(f)} $",
            "steps_typst": [
                "Use SOH CAH TOA: $\\sin = \"Opp\"/\"Hyp\"$, $\\cos = \"Adj\"/\"Hyp\"$, $\\tan = \"Opp\"/\"Adj\"$.",
                f"Substitute the side lengths for ${fn}(theta)$.",
                f"Reduce to lowest terms: ${_fmt_frac(f)}$.",
            ],
            "distractors": [
                f"$ {_fmt_frac(Fraction(f.denominator, f.numerator))} $",
                f"$ {_fmt_frac(Fraction(adj if fn != 'cos' else opp, hyp))} $",
                f"$ {_fmt_frac(Fraction(opp + adj, hyp))} $",
            ],
            "diagram_svg": svg_right_triangle(a_label=str(adj), b_label=str(opp), c_label=str(hyp), theta_label="theta"),
            "answer_svg": svg_right_triangle(a_label=str(adj), b_label=str(opp), c_label=str(hyp), theta_label=f"{fn}={f}"),
        }

    if "finding angle" in t_low:
        opp, adj, hyp = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
        opp, adj, hyp = opp * scale, adj * scale, hyp * scale
        deg = round(math.degrees(math.atan2(opp, adj)), 1)
        return {
            "prompt_text": "Find the measure of angle theta to the nearest tenth of a degree.",
            "equation_typst": f"$ tan(theta) = ({opp})/({adj}) $",
            "answer_typst": f"$ theta approx {deg}^circle $",
            "steps_typst": [
                f"Identify the opposite side (${opp}$) and adjacent side (${adj}$): $tan(theta) = ({opp})/({adj})$.",
                f"Apply the inverse tangent function: $theta = arctan(({opp})/({adj}))$.",
                f"Evaluate in degree mode: $theta approx {deg}^circle$.",
            ],
            "distractors": [
                f"$ theta approx {round(90.0 - deg, 1)}^circle $",
                f"$ theta approx {round(deg + 10.0, 1)}^circle $",
                f"$ theta approx {round(deg / 2, 1)}^circle $",
            ],
            "diagram_svg": svg_right_triangle(a_label=str(adj), b_label=str(opp), c_label="", theta_label="theta=?"),
            "answer_svg": svg_right_triangle(a_label=str(adj), b_label=str(opp), c_label="", theta_label=f"{deg} deg"),
        }

    if "missing sides" in t_low or "solving right triangles" in t_low or "finding angles and sides" in t_low:
        ang = rng.choice([30, 45, 60, 35, 50])
        hyp = rng.randint(8, 18) * scale
        opp_v = round(hyp * math.sin(math.radians(ang)), 1)
        return {
            "prompt_text": "Find the missing side length x of the right triangle to the nearest tenth.",
            "equation_typst": f"$ sin({ang}^circle) = (x)/({hyp}) $",
            "answer_typst": f"$ x approx {opp_v} $",
            "steps_typst": [
                f"Relate the opposite side $x$ and hypotenuse ${hyp}$ using sine: $sin({ang}^circle) = x / {hyp}$.",
                f"Multiply both sides by ${hyp}$: $x = {hyp} sin({ang}^circle)$.",
                f"Round to the nearest tenth: $x approx {opp_v}$.",
            ],
            "distractors": [
                f"$ x approx {round(hyp * math.cos(math.radians(ang)), 1)} $",
                f"$ x approx {round(hyp / math.sin(math.radians(ang)), 1)} $",
                f"$ x approx {round(opp_v + 3.2, 1)} $",
            ],
            "diagram_svg": svg_right_triangle(a_label="", b_label="x", c_label=str(hyp), theta_label=f"{ang} deg"),
            "answer_svg": svg_right_triangle(a_label="", b_label=f"x={opp_v}", c_label=str(hyp), theta_label=f"{ang} deg"),
        }

    if "law of sines" in t_low and "cosines" not in t_low:
        a = rng.randint(6, 14) * scale
        A, B = rng.choice([(30, 45), (30, 60), (45, 60), (40, 65)])
        b = round(a * math.sin(math.radians(B)) / math.sin(math.radians(A)), 1)
        return {
            "prompt_text": "Use the Law of Sines to find the missing side length b to the nearest tenth.",
            "equation_typst": f"$ m angle A = {A}^circle, quad m angle B = {B}^circle, quad a = {a} $",
            "answer_typst": f"$ b approx {b} $",
            "steps_typst": [
                f"Set up the Law of Sines: $(b)/(sin B) = (a)/(sin A) arrow.r.double (b)/(sin {B}^circle) = ({a})/(sin {A}^circle)$.",
                f"Solve for $b$: $b = ({a} sin {B}^circle)/(sin {A}^circle)$.",
                f"Evaluate: $b approx {b}$.",
            ],
            "distractors": [
                f"$ b approx {round(a * math.sin(math.radians(A)) / math.sin(math.radians(B)), 1)} $",
                f"$ b approx {round(b + 3.5, 1)} $",
                f"$ b approx {a + (B - A)} $",
            ],
            "diagram_svg": svg_general_triangle(angle_a=f"{A} deg", angle_b=f"{B} deg", side_a=str(a), side_b="b=?"),
            "answer_svg": svg_general_triangle(angle_a=f"{A} deg", angle_b=f"{B} deg", side_a=str(a), side_b=f"b={b}"),
        }

    if "law of cosines" in t_low and "law of sines" not in t_low:
        a = rng.randint(5, 10) * scale
        b = rng.randint(6, 12) * scale
        c_sq = a * a + b * b - a * b
        c_val = round(math.sqrt(c_sq), 1)
        return {
            "prompt_text": "Use the Law of Cosines to find side c to the nearest tenth.",
            "equation_typst": f"$ a = {a}, quad b = {b}, quad m angle C = 60^circle $",
            "answer_typst": f"$ c = sqrt({c_sq}) approx {c_val} $",
            "steps_typst": [
                "Apply the Law of Cosines: $c^2 = a^2 + b^2 - 2 a b cos(C)$.",
                f"Substitute $a = {a}, b = {b}, cos(60^circle) = 1/2$: $c^2 = {a}^2 + {b}^2 - {a}({b}) = {c_sq}$.",
                f"Take the square root: $c = sqrt({c_sq}) approx {c_val}$.",
            ],
            "distractors": [
                f"$ c = sqrt({a * a + b * b}) approx {round(math.hypot(a, b), 1)} $",
                f"$ c = {c_sq} $",
                f"$ c = sqrt({a * a + b * b + a * b}) $",
            ],
            "diagram_svg": svg_general_triangle(side_a=str(a), side_b=str(b), side_c="c=?", angle_c="60 deg"),
            "answer_svg": svg_general_triangle(side_a=str(a), side_b=str(b), side_c=f"c={c_val}", angle_c="60 deg"),
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
            # Ensure det = 1 so inverse has clean entries
            a, b, c = 2 * scale, 1, 2 * scale - 1
            d = 1
            det = a * d - b * c
            return {
                "prompt_text": "Find the inverse of the 2x2 matrix.",
                "equation_typst": f"$ A = mat({a}, {b}; {c}, {d}) $",
                "answer_typst": f"$ A^(-1) = (1)/({det}) mat({d}, -{b}; -{c}, {a}) $",
                "steps_typst": [
                    f"Compute the determinant: $det(A) = ({a})({d}) - ({b})({c}) = {det} != 0$.",
                    f"Swap the main diagonal entries and negate the off-diagonal entries: $mat({d}, -{b}; -{c}, {a})$.",
                    f"Divide by $det(A) = {det}$.",
                ],
                "distractors": [
                    f"$ (1)/({det}) mat({a}, -{b}; -{c}, {d}) $",
                    f"$ mat({d}, {b}; {c}, {a}) $",
                    f"$ (1)/({a * d + b * c}) mat({d}, -{b}; -{c}, {a}) $",
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
                f"Multiply each entry of the first matrix by scalar ${scale}$.",
                "Add corresponding entries of the two matrices.",
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
                "equation_typst": f"$ bold(u) = angle.l {ux}, {uy} angle.r, quad bold(v) = angle.l {vx}, {vy} angle.r $",
                "answer_typst": f"$ bold(u) dot bold(v) = {dp} $",
                "steps_typst": [
                    "Use the dot product formula $bold(u) dot bold(v) = u_1 v_1 + u_2 v_2$.",
                    f"Multiply corresponding components: $({ux})({vx}) + ({uy})({vy}) = {ux * vx} + {uy * vy}$.",
                    f"Sum: ${dp}$.",
                ],
                "distractors": [
                    f"$ angle.l {ux * vx}, {uy * vy} angle.r $",
                    f"$ {ux * vy - uy * vx} $",
                    f"$ {dp + ux} $",
                ],
            }
        if "operations" in t_low:
            rx, ry = scale * ux + vx, scale * uy + vy
            return {
                "prompt_text": "Perform the vector operation and write the result in component form.",
                "equation_typst": f"$ {scale}bold(u) + bold(v) quad \"for\" bold(u) = angle.l {ux}, {uy} angle.r, bold(v) = angle.l {vx}, {vy} angle.r $",
                "answer_typst": f"$ angle.l {rx}, {ry} angle.r $",
                "steps_typst": [
                    f"Scale vector $bold(u)$: ${scale}bold(u) = angle.l {scale * ux}, {scale * uy} angle.r$.",
                    f"Add components of $bold(v)$: $angle.l {scale * ux} + ({vx}), {scale * uy} + ({vy}) angle.r$.",
                    f"Result: $angle.l {rx}, {ry} angle.r$.",
                ],
                "distractors": [
                    f"$ angle.l {ux + vx}, {uy + vy} angle.r $",
                    f"$ angle.l {scale * ux - vx}, {scale * uy - vy} angle.r $",
                    f"$ angle.l {ry}, {rx} angle.r $",
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
            return {
                "prompt_text": "Simplify the complex fraction.",
                "equation_typst": f"$ ((1)/(x) + (1)/({r1})) / ((1)/(x) - (1)/({r1})) $",
                "answer_typst": f"$ ({r1} + x)/({r1} - x), quad x != 0, {r1} $",
                "steps_typst": [
                    f"Multiply the main numerator and denominator by the LCD ${r1}x$.",
                    f"Numerator becomes ${r1} + x$ and denominator becomes ${r1} - x$.",
                    f"Result: $({r1} + x)/({r1} - x)$ for $x != 0, {r1}$.",
                ],
                "distractors": [
                    f"$ ({r1} - x)/({r1} + x) $",
                    "$ -1 $",
                    f"$ (x + {r1})/(x - {r1}) $",
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
        n2 = p * rng.choice([6, 9, 10]) * scale
        g_val = math.gcd(n1, n2)
        l_val = math.lcm(n1, n2)
        if "greatest common factor" in t_low:
            return {
                "prompt_text": "Find the greatest common factor (GCF) of the given numbers.",
                "equation_typst": f"$ \"GCF\"({n1}, {n2}) $",
                "answer_typst": f"$ {g_val} $",
                "steps_typst": [
                    f"List the prime factors of ${n1}$ and ${n2}$.",
                    "Multiply the prime factors common to both numbers.",
                    f"Greatest Common Factor = ${g_val}$.",
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
        a, b = rng.choice([(60, 60), (90, 45), (110, 35), (50, 60)])
        c = 180 - a - b
        ang_type = "Equiangular" if a == b == c else ("Right" if 90 in (a, b, c) else ("Obtuse" if max(a, b, c) > 90 else "Acute"))
        side_type = "Equilateral" if a == b == c else ("Isosceles" if len({a, b, c}) == 2 else "Scalene")
        return {
            "prompt_text": "Classify the triangle by its angles and by its sides.",
            "equation_typst": f"$ m angle A = {a}^circle, quad m angle B = {b}^circle, quad m angle C = {c}^circle $",
            "answer_typst": f"$ \"{ang_type} {side_type.lower()} triangle\" $",
            "steps_typst": [
                f"Examine the largest angle (${max(a, b, c)}^circle$) to classify by angles: {ang_type}.",
                f"Count equal angles/sides to classify by sides: {side_type}.",
                f"Classification: {ang_type} {side_type.lower()} triangle.",
            ],
            "distractors": [
                f"$ \"{'Obtuse' if ang_type != 'Obtuse' else 'Acute'} {side_type.lower()} triangle\" $",
                f"$ \"{ang_type} {'isosceles' if side_type != 'Isosceles' else 'scalene'} triangle\" $",
                "$ \"Right equilateral triangle\" $",
            ],
            "diagram_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", angle_c=f"{c} deg"),
            "answer_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", angle_c=f"{c} deg", side_c=f"{ang_type} {side_type}"),
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
                "equation_typst": f"$ m angle A = {a}^circle, quad m angle B = {b}^circle, quad m angle C = ({c_expr})^circle $",
                "answer_typst": f"$ x = {xv}, quad m angle C = {c}^circle $",
                "steps_typst": [
                    f"By the Triangle Angle-Sum Theorem, ${a} + {b} + ({c_expr}) = 180$.",
                    f"Simplify: ${k}x = {k * xv} arrow.r.double x = {xv}$.",
                    f"Therefore, $m angle C = {c}^circle$.",
                ],
                "distractors": [f"$ x = {xv + 2}, quad m angle C = {c}^circle $", f"$ x = {c}, quad m angle C = {xv}^circle $", f"$ x = {xv - 2}, quad m angle C = {180 - a}^circle $"],
                "diagram_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", angle_c=c_expr),
                "answer_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", angle_c=f"x={xv}, {c} deg"),
            }
        return {
            "prompt_text": "Find the measure of the third angle C in triangle ABC.",
            "equation_typst": f"$ m angle A = {a}^circle, quad m angle B = {b}^circle $",
            "answer_typst": f"$ m angle C = {c}^circle $",
            "steps_typst": [
                "By the Triangle Angle-Sum Theorem, $m angle A + m angle B + m angle C = 180^circle$.",
                f"Add the known angles: ${a}^circle + {b}^circle = {a + b}^circle$.",
                f"Subtract from $180^circle$: $m angle C = 180^circle - {a + b}^circle = {c}^circle$.",
            ],
            "distractors": [f"$ m angle C = {a + b}^circle $", f"$ m angle C = {abs(90 - a)}^circle $", f"$ m angle C = {c + 10}^circle $"],
            "diagram_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", angle_c="?"),
            "answer_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", angle_c=f"{c} deg"),
        }

    if "exterior angle theorem" in t_low:
        a = rng.randint(35, 70)
        b = rng.randint(40, 75)
        ext = a + b
        return {
            "prompt_text": "Use the Exterior Angle Theorem to find the exterior angle measure (or solve for x).",
            "equation_typst": f"$ \"Remote interior angles: \" {a}^circle \" and \" {b}^circle; quad \"Exterior angle\" = {scale}x + {ext - scale * 15} $" if scale > 1 else f"$ \"Remote interior angles: \" {a}^circle \" and \" {b}^circle $",
            "answer_typst": f"$ x = 15, quad \"Exterior angle\" = {ext}^circle $" if scale > 1 else f"$ \"Exterior angle\" = {ext}^circle $",
            "steps_typst": [
                "By the Exterior Angle Theorem, an exterior angle of a triangle equals the sum of its two remote interior angles.",
                f"Sum the remote interior angles: ${a}^circle + {b}^circle = {ext}^circle$.",
                f"Result: Exterior angle = ${ext}^circle$" + (", $x = 15$." if scale > 1 else "."),
            ],
            "distractors": [
                f"$ \"Exterior angle\" = {180 - ext}^circle $",
                f"$ \"Exterior angle\" = {abs(a - b)}^circle $",
                f"$ \"Exterior angle\" = {ext + 10}^circle $",
            ],
            "diagram_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", side_c="Ext = ?"),
            "answer_svg": svg_general_triangle(angle_a=f"{a} deg", angle_b=f"{b} deg", side_c=f"Ext = {ext} deg"),
        }

    if "angle addition postulate" in t_low:
        a1 = rng.randint(22, 65) * (1 if scale == 1 else 1)
        a2 = rng.randint(25, 75)
        tot = a1 + a2
        return {
            "prompt_text": "Ray BD lies in the interior of angle ABC. Use the Angle Addition Postulate to find the missing angle.",
            "equation_typst": f"$ m angle A B D = {a1}^circle, quad m angle D B C = {a2}^circle, quad \"find \" m angle A B C $",
            "answer_typst": f"$ m angle A B C = {tot}^circle $",
            "steps_typst": [
                "By the Angle Addition Postulate, $m angle A B D + m angle D B C = m angle A B C$.",
                f"Substitute the given measures: ${a1}^circle + {a2}^circle = {tot}^circle$.",
                f"Answer: $m angle A B C = {tot}^circle$.",
            ],
            "distractors": [f"$ m angle A B C = {abs(a1 - a2)}^circle $", f"$ m angle A B C = {180 - tot}^circle $", f"$ m angle A B C = {tot + 10}^circle $"],
            "diagram_svg": svg_parallel_transversal(mode="linear_pair", angle1_label=f"{a1} deg", angle2_label=f"{a2} deg"),
            "answer_svg": svg_parallel_transversal(mode="linear_pair", angle1_label=f"{a1} deg", angle2_label=f"Total = {tot} deg"),
        }

    if "naming arcs" in t_low or "measures of arcs" in t_low:
        central = rng.randint(45, 145)
        major = 360 - central
        return {
            "prompt_text": "Given the central angle of circle O, find the measure of minor arc AB and major arc ACB.",
            "equation_typst": f"$ m angle A O B = {central}^circle $",
            "answer_typst": f"$ m \"arc\"(A B) = {central}^circle, quad m \"arc\"(A C B) = {major}^circle $",
            "steps_typst": [
                f"The measure of a minor arc equals its central angle: $m \"arc\"(A B) = {central}^circle$.",
                f"The measure of the corresponding major arc is $360^circle - {central}^circle = {major}^circle$.",
                f"Minor arc = ${central}^circle$, Major arc = ${major}^circle$.",
            ],
            "distractors": [
                f"$ m \"arc\"(A B) = {central // 2}^circle, quad m \"arc\"(A C B) = {180 - central}^circle $",
                f"$ m \"arc\"(A B) = {major}^circle, quad m \"arc\"(A C B) = {central}^circle $",
                f"$ m \"arc\"(A B) = {2 * central}^circle, quad m \"arc\"(A C B) = {360 - 2 * central}^circle $",
            ],
            "diagram_svg": svg_circle_diagram(angle_label=f"{central} deg"),
            "answer_svg": svg_circle_diagram(angle_label=f"Minor={central}, Major={major}"),
        }

    if "arc length and sector area" in t_low:
        r = rng.choice([6, 8, 10, 12])
        theta = rng.choice([60, 90, 120, 180])
        arc_f = Fraction(theta * 2 * r, 360)
        sec_f = Fraction(theta * r * r, 360)
        return {
            "prompt_text": "Find the exact arc length s and sector area A of the circle.",
            "equation_typst": f"$ r = {r}, quad theta = {theta}^circle $",
            "answer_typst": f"$ s = {_fmt_frac(arc_f)} pi, quad A = {_fmt_frac(sec_f)} pi $",
            "steps_typst": [
                f"Arc length: $s = (theta / 360^circle) dot 2 pi r = ({theta} / 360) dot 2 pi ({r}) = {_fmt_frac(arc_f)} pi$.",
                f"Sector area: $A = (theta / 360^circle) dot pi r^2 = ({theta} / 360) dot pi ({r}^2) = {_fmt_frac(sec_f)} pi$.",
                f"Result: $s = {_fmt_frac(arc_f)} pi, A = {_fmt_frac(sec_f)} pi$.",
            ],
            "distractors": [
                f"$ s = {_fmt_frac(sec_f)} pi, quad A = {_fmt_frac(arc_f)} pi $",
                f"$ s = {2 * r} pi, quad A = {r * r} pi $",
                f"$ s = {_fmt_frac(arc_f * 2)} pi, quad A = {_fmt_frac(sec_f * 2)} pi $",
            ],
            "diagram_svg": svg_circle_diagram(radius_label=f"r = {r}", angle_label=f"{theta} deg", shade_sector=True),
            "answer_svg": svg_circle_diagram(radius_label=f"s = {arc_f}pi", angle_label=f"A = {sec_f}pi", shade_sector=True),
        }

    # ------------------------------------------------------------------
    # N. LOGARITHMS & EXPONENTIAL EQUATIONS DECOUPLED SUBTOPICS
    # ------------------------------------------------------------------
    if "logarithm" in c_low or "logarithm" in t_low or "compound interest" in t_low:
        base = rng.choice([2, 3, 4, 5])
        exp_k = rng.randint(2, 3 + scale)
        val = base ** exp_k
        if "evaluating logarithms" in t_low:
            return {
                "prompt_text": "Evaluate the logarithm without a calculator.",
                "equation_typst": f"$ log_({base})({val}) $",
                "answer_typst": f"$ {exp_k} $",
                "steps_typst": [
                    f"Ask: to what power must ${base}$ be raised to equal ${val}$?",
                    f"Rewrite ${val}$ as a power of ${base}$: ${base}^{exp_k} = {val}$.",
                    f"Therefore, $log_({base})({val}) = {exp_k}$.",
                ],
                "distractors": [f"$ {val // base} $", f"$ {exp_k + 1} $", f"$ 1/({exp_k}) $"],
            }
        if "not requiring logarithms" in t_low:
            sol = rng.randint(1, 4 * scale)
            return {
                "prompt_text": "Solve the exponential equation by rewriting both sides with a common base.",
                "equation_typst": f"$ {base}^(x + 1) = {base ** (sol + 1)} $",
                "answer_typst": f"$ x = {sol} $",
                "steps_typst": [
                    f"Write ${base ** (sol + 1)}$ as a power of ${base}$: ${base}^{sol + 1}$.",
                    f"Equate the exponents: $x + 1 = {sol + 1}$.",
                    f"Solve for $x$: $x = {sol}$.",
                ],
                "distractors": [f"$ x = {sol + 1} $", f"$ x = {sol - 1} $", f"$ x = {base * sol} $"],
            }
        if "requiring logarithms" in t_low:
            rhs = rng.choice([7, 10, 12, 15, 20]) * scale
            approx = round(math.log(rhs) / math.log(base), 3)
            return {
                "prompt_text": "Solve the exponential equation using logarithms. Give both the exact form and decimal approximation.",
                "equation_typst": f"$ {base}^x = {rhs} $",
                "answer_typst": f"$ x = (ln({rhs}))/(ln({base})) approx {approx} $",
                "steps_typst": [
                    f"Take the natural logarithm of both sides: $ln({base}^x) = ln({rhs})$.",
                    f"Apply the power property: $x ln({base}) = ln({rhs})$.",
                    f"Divide by $ln({base})$: $x = ln({rhs})/ln({base}) approx {approx}$.",
                ],
                "distractors": [
                    f"$ x = (ln({base}))/(ln({rhs})) $",
                    f"$ x = ln({rhs} - {base}) $",
                    f"$ x = ({rhs})/({base}) $",
                ],
            }
        if "compound interest" in t_low:
            P = rng.choice([1000, 2000, 5000])
            r_pct = rng.choice([4, 5, 6, 8])
            t = rng.randint(3, 6 * scale)
            amt = round(P * ((1 + r_pct / 100.0) ** t), 2)
            return {
                "prompt_text": "Find the account balance A using the compound interest formula A = P(1 + r/n)^(nt).",
                "equation_typst": f"$ P = \"$\"{P}, quad r = {r_pct}% \" compounded annually\", quad t = {t} \" years\" $",
                "answer_typst": f"$ A = \"$\"{amt:.2f} $",
                "steps_typst": [
                    f"Substitute $P = {P}, r = {r_pct / 100:.2f}, n = 1, t = {t}$ into $A = P(1 + r)^t$.",
                    f"Write $A = {P}(1.{r_pct:02d})^{t}$.",
                    f"Evaluate and round to the nearest cent: $\\${amt:.2f}$.",
                ],
                "distractors": [
                    f"$ A = \"$\"{P + P * (r_pct / 100.0) * t:.2f} $",
                    f"$ A = \"$\"{amt + 150:.2f} $",
                    f"$ A = \"$\"{P * (1 + r_pct / 100.0) * t:.2f} $",
                ],
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
        triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
        a0, b0, c0 = rng.choice(triples)
        a, b, c = a0 * scale, b0 * scale, c0 * scale
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
        leg = rng.randint(3, 9) * scale
        if scale == 1:
            return {
                "prompt_text": "Find the hypotenuse c of the 45-45-90 special right triangle.",
                "equation_typst": f"$ \"45\"^circle\"-45\"^circle\"-90\"^circle \" triangle with leg \" a = {leg} $",
                "answer_typst": f"$ c = {leg}sqrt(2) $",
                "steps_typst": [
                    "In a $45^circle$-$45^circle$-$90^circle$ triangle, the sides are in the ratio $1 : 1 : sqrt(2)$.",
                    f"Multiply the leg length ${leg}$ by $sqrt(2)$.",
                    f"Hypotenuse $c = {leg}sqrt(2)$.",
                ],
                "distractors": [f"$ c = {2 * leg} $", f"$ c = {leg}sqrt(3) $", f"$ c = ({leg})/(sqrt(2)) $"],
                "diagram_svg": svg_right_triangle(a_label=str(leg), b_label=str(leg), c_label="c=?", theta_label="45 deg"),
                "answer_svg": svg_right_triangle(a_label=str(leg), b_label=str(leg), c_label=f"{leg}sqrt(2)", theta_label="45 deg"),
            }
        return {
            "prompt_text": "Find the long leg b and hypotenuse c of the 30-60-90 special right triangle given short leg a.",
            "equation_typst": f"$ \"30\"^circle\"-60\"^circle\"-90\"^circle \" triangle with short leg \" a = {leg} $",
            "answer_typst": f"$ b = {leg}sqrt(3), quad c = {2 * leg} $",
            "steps_typst": [
                "In a $30^circle$-$60^circle$-$90^circle$ triangle, the sides are in the ratio $1 : sqrt(3) : 2$.",
                f"Long leg $b = a sqrt(3) = {leg}sqrt(3)$.",
                f"Hypotenuse $c = 2a = {2 * leg}$.",
            ],
            "distractors": [
                f"$ b = {leg}sqrt(2), quad c = {2 * leg} $",
                f"$ b = {2 * leg}, quad c = {leg}sqrt(3) $",
                f"$ b = {3 * leg}, quad c = {2 * leg} $",
            ],
            "diagram_svg": svg_right_triangle(a_label=str(leg), b_label="b=?", c_label="c=?", theta_label="60 deg"),
            "answer_svg": svg_right_triangle(a_label=str(leg), b_label=f"{leg}sqrt(3)", c_label=str(2 * leg), theta_label="60 deg"),
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

    if "exponents and logarithms" in t_low or "logarithms and exponents as inverses" in t_low or "writing logs in terms of" in t_low or (t_low == "inverses of" and "logarithm" in c_low):
        b = rng.choice([2, 3, 5])
        k = rng.randint(2, 3 + scale)
        val = b ** k
        return {
            "prompt_text": "Rewrite the exponential equation in logarithmic form and evaluate.",
            "equation_typst": f"$ {b}^{k} = {val} $",
            "answer_typst": f"$ log_({b})({val}) = {k} $",
            "steps_typst": [
                f"Identify base $b = {b}$, exponent $y = {k}$, and result $x = {val}$.",
                "Use the equivalence $b^y = x arrow.l.r.double log_b(x) = y$.",
                f"Write $log_({b})({val}) = {k}$.",
            ],
            "distractors": [
                f"$ log_({k})({val}) = {b} $",
                f"$ log_({val})({b}) = {k} $",
                f"$ log_({b})({k}) = {val} $",
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
            n = rng.randint(2, 4 + scale)
            c = (n + 1) * rng.randint(1, 3)
            return {
                "prompt_text": "Evaluate the indefinite integral using the Power Rule.",
                "equation_typst": f"$ integral {c}x^{n} d x $",
                "answer_typst": f"$ {c // (n + 1)}x^({n + 1}) + C $",
                "steps_typst": [
                    "Apply the Power Rule for integration: $integral x^n d x = (x^(n+1))/(n+1) + C$.",
                    f"Divide coefficient ${c}$ by the new exponent ${n + 1}$: ${c}/({n + 1}) = {c // (n + 1)}$.",
                    f"Result: ${c // (n + 1)}x^({n + 1}) + C$.",
                ],
                "distractors": [
                    f"$ {c * n}x^({n - 1}) + C $",
                    f"$ {c}x^({n + 1}) + C $",
                    f"$ ({c})/({n})x^{n} + C $",
                ],
            }
        if "logarithmic" in t_low:
            a = rng.randint(2, 5 * scale)
            b = rng.randint(1, 7)
            return {
                "prompt_text": "Evaluate the indefinite integral using the logarithmic/exponential rule.",
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
        if "inverse trigonometric" in t_low:
            a = rng.randint(2, 4 + scale)
            return {
                "prompt_text": "Evaluate the indefinite integral using inverse trigonometric forms.",
                "equation_typst": f"$ integral (1)/(sqrt({a * a} - x^2)) d x $",
                "answer_typst": f"$ arcsin((x)/({a})) + C $",
                "steps_typst": [
                    f"Match the integrand with $integral (1)/(sqrt(a^2 - x^2)) d x = arcsin(x/a) + C$ where $a = {a}$.",
                    f"Substitute $a = {a}$ into the antiderivative formula.",
                    f"Result: $arcsin(x/{a}) + C$.",
                ],
                "distractors": [
                    f"$ (1)/({a}) arctan((x)/({a})) + C $",
                    f"$ arccos((x)/({a})) + C $",
                    f"$ sqrt({a * a} - x^2) + C $",
                ],
            }
        if "trigonometric" in t_low:
            k = rng.randint(2, 4 * scale)
            return {
                "prompt_text": "Evaluate the trigonometric indefinite integral.",
                "equation_typst": f"$ integral {k} cos(x) d x $",
                "answer_typst": f"$ {k} sin(x) + C $",
                "steps_typst": [
                    f"Factor out the constant ${k}$: ${k} integral cos(x) d x$.",
                    "Since $(d)/(d x)[sin(x)] = cos(x)$, the antiderivative of $cos(x)$ is $sin(x) + C$.",
                    f"Result: ${k} sin(x) + C$.",
                ],
                "distractors": [
                    f"$ -{k} sin(x) + C $",
                    f"$ {k} cos(x) + C $",
                    f"$ {k} sec(x) + C $",
                ],
            }
        if "first fundamental theorem" in t_low:
            b = rng.randint(2, 3 + scale)
            val = b ** 3
            return {
                "prompt_text": "Evaluate the definite integral using the First Fundamental Theorem of Calculus.",
                "equation_typst": f"$ integral_0^{b} 3x^2 d x $",
                "answer_typst": f"$ {val} $",
                "steps_typst": [
                    "Find an antiderivative $F(x)$ of $3x^2$: $F(x) = x^3$.",
                    f"Apply $F({b}) - F(0) = {b}^3 - 0^3$.",
                    f"Result: ${val}$.",
                ],
                "distractors": [f"$ {3 * b * b} $", f"$ {val // 3} $", f"$ {val + b} $"],
            }
        if "motion along a line" in t_low:
            a = rng.randint(1, 3 * scale)
            t1 = rng.randint(2, 4)
            disp = a * t1 * t1
            return {
                "prompt_text": "Given the velocity function v(t), find the net displacement of the particle over [0, t_1].",
                "equation_typst": f"$ v(t) = {2 * a}t, quad [0, {t1}] $",
                "answer_typst": f"$ Delta s = {disp} $",
                "steps_typst": [
                    f"Net displacement is the definite integral of velocity: $Delta s = integral_0^({t1}) {2 * a}t d t$.",
                    f"Find the antiderivative $[{a}t^2]_0^({t1})$.",
                    f"Evaluate: ${a}({t1})^2 - 0 = {disp}$.",
                ],
                "distractors": [f"$ {2 * a * t1} $", f"$ {disp * 2} $", f"$ {a * t1} $"],
            }
        if "separable" in t_low or "introduction" in t_low:
            k = rng.randint(2, 4 * scale)
            return {
                "prompt_text": "Find the general solution of the separable differential equation.",
                "equation_typst": f"$ (d y)/(d x) = {k}x y $",
                "answer_typst": f"$ y = C e^({k / 2:g}x^2) $",
                "steps_typst": [
                    f"Separate variables: $(1)/(y) d y = {k}x d x$.",
                    f"Integrate both sides: $ln|y| = ({k})/(2)x^2 + C_1$.",
                    f"Exponentiate to solve for $y$: $y = C e^({k / 2:g}x^2)$.",
                ],
                "distractors": [
                    f"$ y = C e^({k}x) $",
                    f"$ y = ({k})/(2)x^2 + C $",
                    f"$ y = ln|{k}x^2 + C| $",
                ],
            }

        if "riemann sum table" in t_low:
            dx = rng.choice([2, 3, 4])
            xs = [0, dx, 2 * dx, 3 * dx]
            ys = [rng.randint(2, 5 * scale) + 2 * i for i in range(4)]
            lram = dx * (ys[0] + ys[1] + ys[2])
            tbl = svg_data_table(
                headers=["x"] + [str(x) for x in xs],
                rows=[["f(x)"] + [str(y) for y in ys]],
                title="Values of f(x)",
            )
            return {
                "prompt_text": f"Use a Left Riemann Sum with 3 subintervals indicated by the table to approximate integral_0^{3 * dx} f(x) dx.",
                "equation_typst": f"$ integral_0^({3 * dx}) f(x) d x quad (\"LRAM\", Delta x = {dx}) $",
                "answer_typst": f"$ L_3 = {lram} $",
                "steps_typst": [
                    f"Each subinterval has width $Delta x = {dx}$ with left endpoints $x = 0, {dx}, {2 * dx}$.",
                    f"Read the left endpoint values from the table: $f(0) = {ys[0]}, f({dx}) = {ys[1]}, f({2 * dx}) = {ys[2]}$.",
                    f"Compute $L_3 = {dx}({ys[0]} + {ys[1]} + {ys[2]}) = {lram}$.",
                ],
                "distractors": [
                    f"$ {dx * (ys[1] + ys[2] + ys[3])} $",
                    f"$ {ys[0] + ys[1] + ys[2]} $",
                    f"$ {lram + dx * ys[3]} $",
                ],
                "diagram_svg": tbl,
                "answer_svg": tbl,
            }

    # ------------------------------------------------------------------
    # V. GRADE 6 & PRE-ALGEBRA SPECIFIC SUBTOPICS
    # ------------------------------------------------------------------
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
        if "angle" in t_low:
            deg = rng.choice([30, 45, 60, 75, 90, 120]) * (1 if scale == 1 else 1) + (2 * scale if scale > 1 else 0)
            if deg % 2 != 0:
                deg += 1
            half = deg // 2
            return {
                "prompt_text": "Compass-and-straightedge construction: if angle ABC is bisected by ray BD, find m angle ABD.",
                "equation_typst": f"$ m angle A B C = {deg}^circle, quad \"ray \" B D \" bisects \" angle A B C $",
                "answer_typst": f"$ m angle A B D = {half}^circle $",
                "steps_typst": [
                    "An angle bisector construction divides the angle into two congruent angles.",
                    f"Divide $m angle A B C = {deg}^circle$ by $2$.",
                    f"Result: $m angle A B D = {half}^circle$.",
                ],
                "distractors": [f"$ {deg}^circle $", f"$ {2 * deg}^circle $", f"$ {180 - deg}^circle $"],
                "diagram_svg": svg_parallel_transversal(mode="linear_pair", angle1_label=f"{deg} deg", angle2_label="Bisect"),
                "answer_svg": svg_parallel_transversal(mode="linear_pair", angle1_label=f"{half} deg", angle2_label=f"{half} deg"),
            }
        if "circle" in t_low:
            r = rng.randint(3, 8 * scale)
            return {
                "prompt_text": "Compass construction: a circle is constructed with compass width r. Find its diameter and circumference.",
                "equation_typst": f"$ \"Compass radius\" r = {r} $",
                "answer_typst": f"$ d = {2 * r}, quad C = {2 * r}pi $",
                "steps_typst": [
                    f"The compass opening sets the radius $r = {r}$.",
                    f"Diameter $d = 2r = {2 * r}$.",
                    f"Circumference $C = 2 pi r = {2 * r}pi$.",
                ],
                "distractors": [f"$ d = {r}, quad C = {r * r}pi $", f"$ d = {2 * r}, quad C = {r * r}pi $", f"$ d = {r * r}, quad C = {2 * r}pi $"],
                "diagram_svg": svg_circle_diagram(radius_label=f"r = {r}"),
                "answer_svg": svg_circle_diagram(radius_label=f"d={2 * r}, C={2 * r}pi"),
            }
        # Triangles, medians, altitudes
        a = rng.randint(6, 14 * scale) * 2
        return {
            "prompt_text": f"Triangle construction ({topic_name}): median AM is constructed to side BC of length {a}. Find BM.",
            "equation_typst": f"$ B C = {a}, quad M \" is the midpoint of \" B C $",
            "answer_typst": f"$ B M = {a // 2} $",
            "steps_typst": [
                "Construct the perpendicular bisector of side $B C$ to locate its midpoint $M$.",
                f"Since $M$ bisects $B C = {a}$, we have $B M = B C / 2$.",
                f"Result: $B M = {a // 2}$.",
            ],
            "distractors": [f"$ B M = {a} $", f"$ B M = {2 * a} $", f"$ B M = {a // 4} $"],
            "diagram_svg": svg_general_triangle(side_a=f"BC = {a}", side_b="Median AM"),
            "answer_svg": svg_general_triangle(side_a=f"BM = {a // 2}", side_b="Median AM"),
        }

    if "trigonometry" in c_low:
        if "area" in t_low:
            a = rng.randint(4, 10 * scale)
            b = rng.randint(6, 12)
            area = Fraction(a * b, 4)  # sin(30 deg) = 1/2 -> 1/2 * a * b * 1/2
            return {
                "prompt_text": "Find the area of triangle ABC using the trigonometric area formula A = (1/2)ab sin(C).",
                "equation_typst": f"$ a = {a}, quad b = {b}, quad m angle C = 30^circle $",
                "answer_typst": f"$ A = {_fmt_frac(area)} $",
                "steps_typst": [
                    "Use the area formula $A = 1/2 a b sin(C)$.",
                    f"Substitute $a = {a}, b = {b}$, and $sin(30^circle) = 1/2$: $A = 1/2 ({a})({b})(1/2)$.",
                    f"Simplify: $A = {_fmt_frac(area)}$.",
                ],
                "distractors": [
                    f"$ A = {a * b // 2} $",
                    f"$ A = {_fmt_frac(area)} sqrt(3) $",
                    f"$ A = {a * b} $",
                ],
                "diagram_svg": svg_general_triangle(side_a=str(a), side_b=str(b), angle_c="30 deg"),
                "answer_svg": svg_general_triangle(side_a=str(a), side_b=str(b), angle_c="30 deg", side_c=f"Area={area}"),
            }
        if "degrees-minutes-seconds" in t_low:
            deg = rng.randint(15, 75) + scale
            mins = rng.choice([12, 24, 30, 36, 45, 48])
            dec = round(deg + mins / 60.0, 2)
            return {
                "prompt_text": "Convert the angle measure from degrees-minutes-seconds (DMS) to decimal degrees.",
                "equation_typst": f"$ {deg}^circle {mins}' $",
                "answer_typst": f"$ {dec:g}^circle $",
                "steps_typst": [
                    "Use the conversion $1^circle = 60'$.",
                    f"Convert ${mins}'$ to degrees: ${mins}/60 = {mins / 60.0:g}^circle$.",
                    f"Add to ${deg}^circle$: ${deg} + {mins / 60.0:g} = {dec:g}^circle$.",
                ],
                "distractors": [
                    f"$ {deg}.{mins}^circle $",
                    f"$ {round(deg + mins / 100.0, 2):g}^circle $",
                    f"$ {deg * 60 + mins}^circle $",
                ],
            }
        if "angles and angle measure" in t_low:
            mult = rng.choice([2, 3, 4, 5, 7]) + scale
            deg = mult * 30
            f = Fraction(deg, 180)
            return {
                "prompt_text": "Convert the angle measure from degrees to radians in exact form.",
                "equation_typst": f"$ {deg}^circle $",
                "answer_typst": f"$ {_fmt_frac(f)} pi $",
                "steps_typst": [
                    "Multiply the degree measure by $(pi \" radians\")/(180^circle)$.",
                    f"Form the fraction $({deg})/(180) pi$.",
                    f"Reduce by $\\gcd({deg}, 180)$: ${_fmt_frac(f)} pi$.",
                ],
                "distractors": [
                    f"$ {_fmt_frac(Fraction(f.denominator, f.numerator))} pi $",
                    f"$ {_fmt_frac(Fraction(deg, 360))} pi $",
                    f"$ {deg} pi $",
                ],
            }
        if "trig functions of any angle" in t_low:
            x0, y0, r0 = rng.choice([(-3, 4, 5), (5, -12, 13), (-8, -15, 17), (7, 24, 25)])
            x, y, r = x0 * scale, y0 * scale, r0 * scale
            return {
                "prompt_text": "The terminal side of angle theta in standard position passes through P(x, y). Find sin(theta) and cos(theta).",
                "equation_typst": f"$ P({x}, {y}) $",
                "answer_typst": f"$ sin(theta) = {_fmt_frac(Fraction(y, r))}, quad cos(theta) = {_fmt_frac(Fraction(x, r))} $",
                "steps_typst": [
                    f"Find the distance $r = sqrt(x^2 + y^2) = sqrt(({x})^2 + ({y})^2) = {r}$.",
                    f"Use $sin(theta) = y/r = {_fmt_frac(Fraction(y, r))}$.",
                    f"Use $cos(theta) = x/r = {_fmt_frac(Fraction(x, r))}$.",
                ],
                "distractors": [
                    f"$ sin(theta) = {_fmt_frac(Fraction(x, r))}, quad cos(theta) = {_fmt_frac(Fraction(y, r))} $",
                    f"$ sin(theta) = {_fmt_frac(Fraction(y, x))}, quad cos(theta) = {_fmt_frac(Fraction(x, y))} $",
                    f"$ sin(theta) = {_fmt_frac(Fraction(-y, r))}, quad cos(theta) = {_fmt_frac(Fraction(-x, r))} $",
                ],
            }
        if "identities" in t_low:
            k = rng.randint(2, 5 * scale)
            return {
                "prompt_text": f"Simplify the trigonometric expression using {topic_name}.",
                "equation_typst": f"$ {k} sin^2(theta) + {k} cos^2(theta) $",
                "answer_typst": f"$ {k} $",
                "steps_typst": [
                    f"Factor out the common coefficient ${k}$: ${k}(sin^2(theta) + cos^2(theta))$.",
                    "Apply the Pythagorean identity $sin^2(theta) + cos^2(theta) = 1$.",
                    f"Multiply: ${k}(1) = {k}$.",
                ],
                "distractors": [f"$ {k} tan^2(theta) $", "$ 1 $", f"$ {2 * k} $"],
            }
        if "equation" in t_low:
            k = rng.choice([1, 2, 3]) * scale
            return {
                "prompt_text": "Solve the trigonometric equation on the interval [0, 2pi).",
                "equation_typst": f"$ 2 cos(theta) - 1 = 0 quad (\"or scale \" k = {k}) $",
                "answer_typst": "$ theta = (pi)/(3), (5pi)/(3) $",
                "steps_typst": [
                    "Isolate $cos(theta)$: $2 cos(theta) = 1 arrow.r.double cos(theta) = 1/2$.",
                    "Identify the quadrants where cosine is positive (Quadrants I and IV) with reference angle $pi/3$.",
                    "Solutions in $[0, 2pi)$: $theta = pi/3$ and $theta = 5pi/3$.",
                ],
                "distractors": [
                    "$ theta = (pi)/(6), (11pi)/(6) $",
                    "$ theta = (2pi)/(3), (4pi)/(3) $",
                    "$ theta = (pi)/(3), (2pi)/(3) $",
                ],
            }

        if "inverse trig" in t_low:
            vals = [
                ("arcsin(1/2)", "(pi)/(6)", "(pi)/(3)"),
                ("arccos(1/2)", "(pi)/(3)", "(pi)/(6)"),
                ("arctan(1)", "(pi)/(4)", "(pi)/(3)"),
                ("arcsin((sqrt(3))/(2))", "(pi)/(3)", "(pi)/(6)"),
                ("arccos(-(1)/(2))", "(2pi)/(3)", "(pi)/(3)"),
                ("arctan(sqrt(3))", "(pi)/(3)", "(pi)/(6)"),
            ]
            expr, ans, dist1 = vals[(rng.randint(0, 5) + scale) % len(vals)]
            return {
                "prompt_text": "Evaluate the inverse trigonometric expression in radians (principal value).",
                "equation_typst": f"$ {expr} $",
                "answer_typst": f"$ {ans} $",
                "steps_typst": [
                    "Recall the principal range of the inverse trigonometric function.",
                    f"Find the angle $theta$ in the principal range whose trigonometric ratio matches ${expr}$.",
                    f"Exact value: ${ans}$.",
                ],
                "distractors": [f"$ {dist1} $", f"$ -{ans} $", "$ (pi)/(2) $"],
            }
        if "multi-step trig" in t_low:
            h = rng.randint(10, 24) * scale
            return {
                "prompt_text": "Solve the multi-step right triangle trigonometry problem. Find x to the nearest tenth.",
                "equation_typst": f"$ \"Altitude\" h = {h}, quad angle A = 30^circle, quad angle B = 45^circle, quad \"find base \" x = A D + D B $",
                "answer_typst": f"$ x = {h}sqrt(3) + {h} approx {round(h * (math.sqrt(3) + 1), 1)} $",
                "steps_typst": [
                    f"In the $30^circle$-$60^circle$-$90^circle$ sub-triangle, $A D = {h} / tan(30^circle) = {h}sqrt(3)$.",
                    f"In the $45^circle$-$45^circle$-$90^circle$ sub-triangle, $D B = {h} / tan(45^circle) = {h}$.",
                    f"Sum the two segments: $x = {h}sqrt(3) + {h} approx {round(h * (math.sqrt(3) + 1), 1)}$.",
                ],
                "distractors": [
                    f"$ {round(2 * h, 1)} $",
                    f"$ {round(h * math.sqrt(3), 1)} $",
                    f"$ {round(h * (math.sqrt(3) - 1), 1)} $",
                ],
                "diagram_svg": svg_right_triangle(a_label="x", b_label=str(h), theta_label="30/45 deg"),
                "answer_svg": svg_right_triangle(a_label=f"x={round(h * (math.sqrt(3) + 1), 1)}", b_label=str(h), theta_label="30/45 deg"),
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
        a = rng.randint(1, 3) * scale
        b = rng.randint(a + 1, a + 4)
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
        a = rng.randint(2, 4 + scale)
        return {
            "prompt_text": "Find all real solutions of the polynomial equation by factoring.",
            "equation_typst": f"$ x^3 - {a * a}x = 0 $",
            "answer_typst": f"$ x = 0, -{a}, {a} $",
            "steps_typst": [
                f"Factor out the greatest common monomial factor $x$: $x(x^2 - {a * a}) = 0$.",
                f"Factor the difference of squares: $x(x - {a})(x + {a}) = 0$.",
                f"Apply the Zero Product Property: $x = 0, x = {a}, x = -{a}$.",
            ],
            "distractors": [
                f"$ x = -{a}, {a} $",
                f"$ x = 0, {a * a} $",
                f"$ x = {a} $",
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
        r = rng.randint(2, 4 + scale)
        return {
            "prompt_text": "Solve the system of quadratic equations.",
            "equation_typst": f"$ cases(y = x^2, y = {r * r}) $",
            "answer_typst": f"$ (-{r}, {r * r}) \" and \" ({r}, {r * r}) $",
            "steps_typst": [
                f"Substitute $y = {r * r}$ into $y = x^2$: $x^2 = {r * r}$.",
                f"Take square roots of both sides: $x = plus.minus {r}$.",
                f"Intersection points: $(-{r}, {r * r})$ and $({r}, {r * r})$.",
            ],
            "distractors": [
                f"$ ({r}, {r * r}) \" only\" $",
                f"$ (plus.minus {r * r}, {r}) $",
                "$ \"No real intersection\" $",
            ],
        }

    if "rotations of conic sections" in t_low:
        b = rng.randint(2, 6 * scale)
        return {
            "prompt_text": "Find the angle of rotation theta (0 < theta < 90 deg) that eliminates the xy-term.",
            "equation_typst": f"$ x^2 + {b}x y + y^2 - 8 = 0 $",
            "answer_typst": "$ theta = 45^circle $",
            "steps_typst": [
                f"Identify $A = 1, B = {b}, C = 1$ in $A x^2 + B x y + C y^2 + D x + E y + F = 0$.",
                "Use $\\cot(2 theta) = (A - C)/B = (1 - 1)/B = 0$.",
                "Since $2 theta = 90^circle$, the rotation angle is $theta = 45^circle$.",
            ],
            "distractors": ["$ theta = 30^circle $", "$ theta = 60^circle $", "$ theta = 90^circle $"],
        }

    if "general sequences" in t_low or "general series" in t_low or "power series" in t_low:
        c = rng.randint(1, 3 * scale)
        if "power series" in t_low:
            return {
                "prompt_text": "Find the radius and interval of convergence of the geometric power series.",
                "equation_typst": f"$ sum_(n=0)^infinity ((x)/({c}))^n $",
                "answer_typst": f"$ R = {c}, quad I = (-{c}, {c}) $",
                "steps_typst": [
                    f"This is a geometric series with common ratio $r = x/{c}$.",
                    f"It converges when $|x/{c}| < 1 arrow.r.double |x| < {c}$.",
                    f"Radius of convergence $R = {c}$ and interval $I = (-{c}, {c})$.",
                ],
                "distractors": [
                    f"$ R = 1/({c}), quad I = (-1/{c}, 1/{c}) $",
                    f"$ R = {c}, quad I = [-{c}, {c}] $",
                    "$ R = infinity, quad I = (-infinity, infinity) $",
                ],
            }
        if "series" in t_low:
            s = sum(n * n + c for n in range(1, 5))
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
        return {
            "prompt_text": "Find the first four terms of the sequence given by the explicit formula.",
            "equation_typst": f"$ a_n = n^2 + {c} $",
            "answer_typst": f"$ {1 + c}, {4 + c}, {9 + c}, {16 + c} $",
            "steps_typst": [
                f"For $n = 1, 2$: $a_1 = 1^2 + {c} = {1 + c}$ and $a_2 = 2^2 + {c} = {4 + c}$.",
                f"For $n = 3, 4$: $a_3 = 3^2 + {c} = {9 + c}$ and $a_4 = 4^2 + {c} = {16 + c}$.",
                f"First four terms: ${1 + c}, {4 + c}, {9 + c}, {16 + c}$.",
            ],
            "distractors": [
                f"$ {c}, {1 + c}, {4 + c}, {9 + c} $",
                f"$ {2 + c}, {4 + c}, {6 + c}, {8 + c} $",
                f"$ {1 + c}, {2 + c}, {3 + c}, {4 + c} $",
            ],
        }

    if t_low == "basics" and "vectors" in c_low:
        a0, b0, c0 = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13)])
        vx, vy, mag = a0 * scale, b0 * scale, c0 * scale
        if "three-dimensional" in c_low:
            vz = rng.randint(1, 4) * scale
            mag_sq = vx * vx + vy * vy + vz * vz
            return {
                "prompt_text": "Find the component form and magnitude of the 3D vector v.",
                "equation_typst": f"$ bold(v) = angle.l {vx}, {vy}, {vz} angle.r $",
                "answer_typst": f"$ ||bold(v)|| = sqrt({mag_sq}) $",
                "steps_typst": [
                    "Use the 3D vector magnitude formula $||bold(v)|| = sqrt(v_x^2 + v_y^2 + v_z^2)$.",
                    f"Square and add components: ${vx}^2 + {vy}^2 + {vz}^2 = {mag_sq}$.",
                    f"Magnitude: $sqrt({mag_sq})$.",
                ],
                "distractors": [f"$ {vx + vy + vz} $", f"$ {mag_sq} $", f"$ sqrt({vx * vx + vy * vy}) $"],
            }
        return {
            "prompt_text": "Find the magnitude ||v|| of the 2D vector.",
            "equation_typst": f"$ bold(v) = angle.l {vx}, {vy} angle.r $",
            "answer_typst": f"$ ||bold(v)|| = {mag} $",
            "steps_typst": [
                "Use the magnitude formula $||bold(v)|| = sqrt(v_x^2 + v_y^2)$.",
                f"Substitute components: $sqrt({vx}^2 + {vy}^2) = sqrt({vx * vx + vy * vy})$.",
                f"Simplify: $||bold(v)|| = {mag}$.",
            ],
            "distractors": [f"$ {vx + vy} $", f"$ {mag * mag} $", f"$ {abs(vy - vx)} $"],
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

        for idx, diff in enumerate(difficulties):
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
                    metadata={"topic_id": self.topic_id, "topic_name": self.topic_name},
                )
                prob.question_type = config.question_type
                if config.question_type == "multiple_choice":
                    self._populate_multiple_choice_choices(prob, rng)
                problems.append(prob)
            elif base_cls is not None:
                if diff not in base_probs:
                    sub_cfg = GeneratorConfig(
                        problem_count=max(config.problem_count, 6),
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
                bp = base_probs[diff][idx % len(base_probs[diff])]
                problems.append(bp)

        return problems

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
