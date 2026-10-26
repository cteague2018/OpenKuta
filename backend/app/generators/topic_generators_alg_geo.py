from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any, Dict, Optional

from backend.app.core.base import ProblemDifficulty
from backend.app.core.svg_utils import (
    svg_area_model,
    svg_box_plot,
    svg_circle_diagram,
    svg_coordinate_plane,
    svg_data_table,
    svg_dot_plot,
    svg_general_triangle,
    svg_histogram,
    svg_number_line,
    svg_parallel_transversal,
    svg_polygon_diagram,
    svg_solid_3d,
    svg_tape_or_hanger,
)


def _fmt_frac(f_in: Any) -> str:
    f = f_in if isinstance(f_in, Fraction) else Fraction(f_in).limit_denominator()
    if f.denominator == 1:
        return str(f.numerator)
    if f.numerator < 0:
        return f"-({abs(f.numerator)})/({f.denominator})"
    return f"({f.numerator})/({f.denominator})"


def gen_alg_geo_problem(
    topic_id: str,
    topic_name: str,
    category_name: str,
    course_key: str,
    difficulty: ProblemDifficulty,
    rng: random.Random,
) -> Optional[Dict[str, Any]]:
    """Generate a topic-specific problem for Grade 6, Pre-Algebra, Algebra 1, or Geometry topics."""
    t_low = topic_name.lower()
    c_low = category_name.lower()
    a: Any
    b: Any
    c: Any
    d: Any
    d1: Any
    d2: Any
    f: Any
    f1: Any
    f2: Any
    f3: Any
    f4: Any
    h: Any
    k: Any
    m: Any
    n: Any
    p: Any
    r: Any
    s: Any
    t: Any
    v: Any
    w: Any
    x: Any
    y: Any
    xs: Any
    ys: Any
    pts: Any
    ans: Any
    val: Any
    area: Any
    vol: Any
    tot: Any
    bins: Any

    # ------------------------------------------------------------------
    # 1. SETS OF NUMBERS
    # ------------------------------------------------------------------
    if "sets of numbers" in t_low:
        if difficulty == ProblemDifficulty.MILD:
            val = rng.choice([-12, -7, -3, 0, 5, 14, 29])
            if val > 0:
                ans = "Natural, Whole, Integer, Rational, Real"
                d1 = "Integer, Rational, Real only"
                d2 = "Irrational, Real"
                d3 = "Whole, Irrational, Real"
            elif val == 0:
                ans = "Whole, Integer, Rational, Real"
                d1 = "Natural, Whole, Integer, Rational, Real"
                d2 = "Irrational, Real"
                d3 = "Integer, Real only"
            else:
                ans = "Integer, Rational, Real"
                d1 = "Whole, Integer, Rational, Real"
                d2 = "Irrational, Real"
                d3 = "Natural, Integer, Real"
            eq = f"$ {val} $"
            steps = [
                f"Examine whether ${val}$ is a counting number, zero, negative integer, or fraction.",
                f"Every integer can be written with denominator $1$, so ${val}$ is also Rational and Real.",
                f"Classification: {ans}",
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            num = rng.choice([-7, -5, -3, 3, 5, 9, 11])
            den = rng.choice([2, 4, 8, 5])
            eq = f"$ ({num})/({den}) $" if rng.random() < 0.5 else f"$ {num / den:.3g} $"
            ans = "Rational, Real"
            d1 = "Integer, Rational, Real"
            d2 = "Irrational, Real"
            d3 = "Whole, Rational, Real"
            steps = [
                "A number that can be written as a ratio of two integers $p/q$ ($q != 0$) is rational.",
                "Because it has a non-integer fractional part, it is not an Integer, Whole, or Natural number.",
                f"Classification: {ans}",
            ]
        else:
            rad = rng.choice([2, 3, 5, 6, 7, 10, 11, 13, 15])
            eq = f"$ sqrt({rad}) $" if rng.random() < 0.7 else f"$ -sqrt({rad}) $"
            ans = "Irrational, Real"
            d1 = "Rational, Real"
            d2 = "Integer, Rational, Real"
            d3 = "Imaginary"
            steps = [
                f"Notice that ${rad}$ is not a perfect square.",
                "The square root of a non-perfect square has a non-terminating, non-repeating decimal expansion.",
                f"Classification: {ans}",
            ]
        return {
            "prompt_text": "Name the set or sets of numbers to which each real number belongs.",
            "equation_typst": eq,
            "answer_typst": f"$ \"{ans}\" $",
            "steps_typst": steps,
            "distractors": [f"$ \"{d1}\" $", f"$ \"{d2}\" $", f"$ \"{d3}\" $"],
        }

    # ------------------------------------------------------------------
    # 2. MULTIPLYING & DIVIDING RATIONAL NUMBERS (NUMERICAL)
    # ------------------------------------------------------------------
    if "multiplying rational numbers" in t_low or "dividing rational numbers" in t_low:
        is_div = "dividing" in t_low
        op_sym = "div" if is_div else "times"
        if difficulty == ProblemDifficulty.MILD:
            f1 = Fraction(rng.choice([1, 2, 3, 4]), rng.choice([5, 7]))
            f2 = Fraction(rng.choice([2, 3, 5]), rng.choice([4, 8]))
        elif difficulty == ProblemDifficulty.MEDIUM:
            f1 = Fraction(rng.choice([-5, -3, -2, 3, 5]), rng.choice([4, 6, 8]))
            f2 = Fraction(rng.choice([-7, -4, -3, 2, 7]), rng.choice([3, 5, 9]))
        else:
            f1 = Fraction(rng.choice([-11, -9, -7, 7, 11]), rng.choice([6, 8, 10]))
            f2 = Fraction(rng.choice([-8, -5, 5, 9]), rng.choice([4, 9, 12]))
        res = f1 / f2 if is_div else f1 * f2
        ans = f"$ {_fmt_frac(res)} $"
        steps = [
            f"Write both rational numbers as fractions: ${_fmt_frac(f1)} {op_sym} {_fmt_frac(f2)}$.",
            (
                f"Multiply by the reciprocal of the divisor: ${_fmt_frac(f1)} times {_fmt_frac(Fraction(f2.denominator, f2.numerator))}$."
                if is_div
                else "Multiply the numerators together and the denominators together."
            ),
            f"Reduce to lowest terms: ${ans.strip('$ ')}$.",
        ]
        return {
            "prompt_text": f"Find each {'quotient' if is_div else 'product'}. Write your answer in simplest form.",
            "equation_typst": f"$ {_fmt_frac(f1)} {op_sym} ({_fmt_frac(f2)}) $",
            "answer_typst": ans,
            "steps_typst": steps,
            "distractors": [
                f"$ {_fmt_frac(-res)} $",
                f"$ {_fmt_frac(res + Fraction(1, 2))} $",
                f"$ {_fmt_frac(Fraction(res.denominator, res.numerator if res.numerator != 0 else 1))} $",
            ],
        }

    # ------------------------------------------------------------------
    # 3. NUMBER LINES, OPPOSITES, ABSOLUTE VALUE, COMPARING & ORDERING
    # ------------------------------------------------------------------
    if c_low == "negative numbers and absolute value" or "opposites" in t_low or "numbers on a number line" in t_low or "number line word" in t_low:
        if "opposites" in t_low:
            v = rng.randint(2, 15) * rng.choice([-1, 1])
            if difficulty == ProblemDifficulty.MEDIUM:
                v = -abs(v)
            elif difficulty == ProblemDifficulty.SPICY:
                # Opposite of the opposite
                ans = f"$ {v} $"
                return {
                    "prompt_text": "Find the value of the expression and locate it on the number line.",
                    "equation_typst": f"$ -(-({v})) $",
                    "answer_typst": ans,
                    "steps_typst": [
                        f"The opposite of ${v}$ is ${-v}$.",
                        f"The opposite of ${-v}$ returns to ${v}$.",
                        f"Answer: ${v}$",
                    ],
                    "distractors": [f"$ {-v} $", f"$ {abs(v) + 1} $", "$ 0 $"],
                    "diagram_svg": svg_number_line(),
                    "answer_svg": svg_number_line(points=[(v, str(v)), (-v, str(-v))]),
                }
            return {
                "prompt_text": "Find the opposite of the given number and plot both on the number line.",
                "equation_typst": f"$ {v} $",
                "answer_typst": f"$ {-v} $",
                "steps_typst": [
                    "Two numbers are opposites if they are the same distance from $0$ on opposite sides.",
                    f"The opposite of ${v}$ is ${-v}$.",
                    f"Answer: ${-v}$",
                ],
                "distractors": [f"$ {v} $", f"$ 1/{abs(v)} $", "$ 0 $"],
                "diagram_svg": svg_number_line(),
                "answer_svg": svg_number_line(points=[(v, str(v)), (-v, f"opp={-v}")]),
            }
        if "comparing" in t_low:
            use_abs = "absolute" in t_low
            a = rng.randint(-9, 9)
            b = rng.choice([x for x in range(-9, 10) if x != a])
            if difficulty == ProblemDifficulty.SPICY:
                a, b = -abs(a) - 2, abs(a) + 1
            va = abs(a) if use_abs else a
            vb = abs(b) if use_abs and difficulty != ProblemDifficulty.MILD else b
            cmp_sym = "<" if va < vb else (">" if va > vb else "=")
            lhs = f"|{a}|" if use_abs else str(a)
            rhs = f"|{b}|" if (use_abs and difficulty != ProblemDifficulty.MILD) else str(b)
            return {
                "prompt_text": "Compare the two values using <, >, or =.",
                "equation_typst": f"$ {lhs} quad square quad {rhs} $",
                "answer_typst": f"$ {lhs} {cmp_sym} {rhs} $",
                "steps_typst": [
                    f"Evaluate each side: ${lhs} = {va}$ and ${rhs} = {vb}$.",
                    f"On a horizontal number line, ${min(va, vb)}$ lies to the left of ${max(va, vb)}$.",
                    f"Therefore, ${lhs} {cmp_sym} {rhs}$.",
                ],
                "distractors": [
                    f"$ {lhs} {'>' if cmp_sym == '<' else '<'} {rhs} $",
                    f"$ {lhs} = {rhs} $",
                    f"$ {lhs} <= {rhs} $",
                ],
                "diagram_svg": svg_number_line(),
                "answer_svg": svg_number_line(points=[(va, lhs), (vb, rhs)]),
            }
        if "ordering" in t_low:
            use_abs = "absolute" in t_low
            vals = rng.sample(range(-9, 10), 4 if difficulty != ProblemDifficulty.SPICY else 5)
            items = [(abs(v) if (use_abs and i % 2 == 0) else v, f"|{v}|" if (use_abs and i % 2 == 0) else str(v)) for i, v in enumerate(vals)]
            sorted_items = sorted(items, key=lambda x: x[0])
            rev_items = list(reversed(sorted_items))
            ans_str = ", ".join(x[1] for x in sorted_items)
            return {
                "prompt_text": "Order the given numbers from least to greatest.",
                "equation_typst": f"$ {', '.join(x[1] for x in items)} $",
                "answer_typst": f"$ {ans_str} $",
                "steps_typst": [
                    "Evaluate any absolute value bars before comparing.",
                    "Numbers further to the left on the number line are smaller.",
                    f"Ordered from least to greatest: ${ans_str}$.",
                ],
                "distractors": [
                    f"$ {', '.join(x[1] for x in rev_items)} $",
                    f"$ {', '.join(x[1] for x in items)} $",
                    f"$ {', '.join(x[1] for x in sorted_items[1:] + sorted_items[:1])} $",
                ],
                "diagram_svg": svg_number_line(),
                "answer_svg": svg_number_line(points=[(x[0], x[1]) for x in sorted_items]),
            }
        if "absolute values" in t_low:
            v = rng.randint(-18, -2) if difficulty == ProblemDifficulty.MILD else rng.randint(-35, 35)
            if difficulty == ProblemDifficulty.SPICY:
                w = rng.randint(3, 12)
                res = abs(v) - abs(-w)
                return {
                    "prompt_text": "Evaluate the absolute value expression.",
                    "equation_typst": f"$ |{v}| - |{-w}| $",
                    "answer_typst": f"$ {res} $",
                    "steps_typst": [
                        f"Evaluate each absolute value: $|{v}| = {abs(v)}$ and $|{-w}| = {w}$.",
                        f"Subtract the results: ${abs(v)} - {w} = {res}$.",
                        f"Answer: ${res}$",
                    ],
                    "distractors": [f"$ {abs(v) + w} $", f"$ {-res} $", f"$ {v - w} $"],
                    "diagram_svg": svg_number_line(),
                    "answer_svg": svg_number_line(points=[(res, str(res))]),
                }
            return {
                "prompt_text": "Find the absolute value of the given number.",
                "equation_typst": f"$ |{v}| $",
                "answer_typst": f"$ {abs(v)} $",
                "steps_typst": [
                    "Absolute value represents the distance from $0$ on a number line.",
                    f"Since distance is always non-negative, $|{v}| = {abs(v)}$.",
                    f"Answer: ${abs(v)}$",
                ],
                "distractors": [f"$ {-abs(v)} $", "$ 0 $", f"$ {abs(v) + 1} $"],
                "diagram_svg": svg_number_line(),
                "answer_svg": svg_number_line(points=[(0, "0"), (v, f"dist={abs(v)}")]),
            }
        # Numbers on a number line / word problems
        v = rng.randint(-8, 8) if difficulty != ProblemDifficulty.SPICY else rng.randint(-9, 9)
        delta = rng.randint(2, 6) * rng.choice([-1, 1])
        end_v = v + delta
        if "word" in t_low:
            eq = f"\"A submarine starts at \" ${v}$ \" m and changes depth by \" ${delta}$ \" m. Find its final position.\""
        else:
            eq = f"$ \"Start at \" {v} \" and move \" {abs(delta)} \" units to the {'right' if delta > 0 else 'left'}.\" $"
        return {
            "prompt_text": "Use the number line to find the final position.",
            "equation_typst": eq,
            "answer_typst": f"$ {end_v} $",
            "steps_typst": [
                f"Locate the starting value ${v}$ on the number line.",
                f"Move ${abs(delta)}$ units to the {'right (add)' if delta > 0 else 'left (subtract)'}: ${v} + ({delta}) = {end_v}$.",
                f"Final position: ${end_v}$.",
            ],
            "distractors": [f"$ {v - delta} $", f"$ {-end_v} $", f"$ {abs(v) + abs(delta)} $"],
            "diagram_svg": svg_number_line(points=[(v, "Start")]),
            "answer_svg": svg_number_line(points=[(v, "Start"), (end_v, f"End={end_v}")]),
        }

    # ------------------------------------------------------------------
    # 4. GRADE 6 RATIOS, RATES, PERCENTS, DECIMALS, FRACTIONS, DIAGRAMS
    # ------------------------------------------------------------------
    if c_low in ("ratios", "proportions and percents") and ("ratio" in t_low or "proportion" in t_low):
        a = rng.randint(2, 7)
        b = rng.choice([x for x in range(2, 9) if math.gcd(a, x) == 1])
        k = rng.randint(2, 5) if difficulty == ProblemDifficulty.MILD else rng.randint(4, 9)
        if "part-part-whole" in t_low:
            total = (a + b) * k
            part_a = a * k
            labels = ["a"] * a + ["b"] * b
            return {
                "prompt_text": "Use the part-part-whole tape diagram and ratio to find the requested quantity.",
                "equation_typst": f"\"The ratio of red to blue marbles is \" ${a}:{b}$ \". If there are \" ${total}$ \" marbles in all, how many are red?\"",
                "answer_typst": f"$ {part_a} $",
                "steps_typst": [
                    f"Add the parts of the ratio to find the total number of equal parts: ${a} + {b} = {a + b}$ parts.",
                    f"Divide the total marbles by ${a + b}$: ${total} div {a + b} = {k}$ marbles per part.",
                    f"Multiply the red parts by ${k}$: ${a} times {k} = {part_a}$.",
                ],
                "distractors": [f"$ {b * k} $", f"$ {total - a} $", f"$ {(a + b) * (k + 1)} $"],
                "diagram_svg": svg_tape_or_hanger(mode="tape", parts_labels=labels[:6], total_label=str(total)),
                "answer_svg": svg_tape_or_hanger(mode="tape", parts_labels=[str(k)] * min(a + b, 6), total_label=f"Red = {part_a}"),
            }
        if "comparing ratios" in t_low:
            c = a + rng.choice([1, 2])
            d = b + rng.choice([1, 3])
            cmp_sym = ">" if a * d > b * c else ("<" if a * d < b * c else "=")
            return {
                "prompt_text": "Compare the two ratios using <, >, or =.",
                "equation_typst": f"$ {a}:{b} quad square quad {c}:{d} $",
                "answer_typst": f"$ {a}:{b} {cmp_sym} {c}:{d} $",
                "steps_typst": [
                    f"Write both ratios as fractions: $({a})/({b})$ and $({c})/({d})$.",
                    f"Use a common denominator of ${b * d}$: $({a * d})/({b * d})$ vs $({b * c})/({b * d})$.",
                    f"Compare numerators: ${a}:{b} {cmp_sym} {c}:{d}$.",
                ],
                "distractors": [
                    f"$ {a}:{b} {'<' if cmp_sym == '>' else '>'} {c}:{d} $",
                    f"$ {a}:{b} = {c}:{d} $",
                    f"$ {a + b} = {c + d} $",
                ],
                "diagram_svg": svg_data_table(["Ratio A", "Ratio B"], [[f"{a} : {b}", f"{c} : {d}"]]),
                "answer_svg": svg_data_table(["Ratio A", "Ratio B"], [[f"{a*d}/{b*d}", f"{b*c}/{b*d}"]]),
            }
        # Equivalent ratios / introduction / solving proportions
        missing = b * k
        return {
            "prompt_text": "Find the missing value in the equivalent ratio table or proportion.",
            "equation_typst": f"$ ({a})/({b}) = ({a * k})/(x) $",
            "answer_typst": f"$ x = {missing} $",
            "steps_typst": [
                f"Notice the numerator scales by a factor of ${k}$ since ${a} times {k} = {a * k}$.",
                f"Multiply the denominator ${b}$ by the same scale factor ${k}$: ${b} times {k} = {missing}$.",
                f"Therefore, $x = {missing}$.",
            ],
            "distractors": [f"$ x = {b + k} $", f"$ x = {a * k} $", f"$ x = {missing + b} $"],
            "diagram_svg": svg_data_table(["Part 1", "Part 2"], [[str(a), str(b)], [str(a * k), "x"]]),
            "answer_svg": svg_data_table(["Part 1", "Part 2"], [[str(a), str(b)], [str(a * k), str(missing)]]),
        }

    if c_low == "rates" or "constant rate" in t_low:
        rate = rng.randint(4, 15) if difficulty == ProblemDifficulty.MILD else rng.randint(12, 45)
        t = rng.randint(3, 8)
        dist = rate * t
        if "converting units" in t_low:
            ft = rng.randint(3, 18)
            inches = ft * 12
            return {
                "prompt_text": "Convert the measurement to the indicated unit.",
                "equation_typst": f"$ {ft} \" feet\" = x \" inches\" quad (1 \" ft\" = 12 \" in\") $",
                "answer_typst": f"$ x = {inches} \" inches\" $",
                "steps_typst": [
                    "Multiply by the unit conversion factor $(12 \" in\")/(1 \" ft\")$.",
                    f"Compute ${ft} times 12 = {inches}$.",
                    f"Answer: ${inches}$ inches.",
                ],
                "distractors": [f"$ x = {ft + 12} \" inches\" $", f"$ x = {ft * 10} \" inches\" $", f"$ x = {inches + 12} \" inches\" $"],
            }
        if "constant rate" in t_low:
            return {
                "prompt_text": "Write the two-variable constant rate equation and find y for the given x.",
                "equation_typst": f"\"Rate\" k = {rate}; \" find \" y \" when \" x = {t}",
                "answer_typst": f"$ y = {rate}x; quad y = {dist} $",
                "steps_typst": [
                    f"A constant rate relationship has the form $y = k x$ with $k = {rate}$.",
                    f"Substitute $x = {t}$ into $y = {rate}x$: $y = {rate}({t}) = {dist}$.",
                    f"Answer: $y = {rate}x$, $y = {dist}$.",
                ],
                "distractors": [f"$ y = x + {rate}; quad y = {t + rate} $", f"$ y = {dist}x $", f"$ y = {rate}x; quad y = {dist + rate} $"],
                "diagram_svg": svg_data_table(["x", "y"], [["1", str(rate)], [str(t), "?"]]),
                "answer_svg": svg_data_table(["x", "y"], [["1", str(rate)], [str(t), str(dist)]]),
            }
        return {
            "prompt_text": "Find the unit rate.",
            "equation_typst": f"\"$\"{dist} \" for \" {t} \" items\"",
            "answer_typst": f"$ \"$\"{rate} \" per item\" $",
            "steps_typst": [
                f"Divide total cost by the number of items: $({dist})/({t})$.",
                f"Simplify the quotient: ${dist} div {t} = {rate}$.",
                f"Unit rate: $\\${rate}$ per item.",
            ],
            "distractors": [f"$ \"$\"{rate + 2} \" per item\" $", f"$ \"$\"{dist - t} \" per item\" $", f"$ \"$\"{t} \" per item\" $"],
        }

    if "percent of change" in t_low:
        old_v = rng.choice([20, 25, 40, 50, 80, 100, 200])
        pct = rng.choice([10, 15, 20, 25, 30, 40, 50])
        inc = rng.choice([True, False])
        delta = (old_v * pct) // 100
        new_v = old_v + delta if inc else old_v - delta
        kind = "increase" if inc else "decrease"
        return {
            "prompt_text": "Find each percent change. State if it is an increase or a decrease.",
            "equation_typst": f"\"From \" {old_v} \" to \" {new_v}",
            "answer_typst": f"$ {pct}% \" {kind}\" $",
            "steps_typst": [
                f"Find the amount of change: $|{new_v} - {old_v}| = {delta}$.",
                f"Divide by the original amount: $({delta})/({old_v}) = {pct / 100:.2f} = {pct}%$.",
                f"Since ${new_v}$ is {'greater' if inc else 'less'} than ${old_v}$, it is a ${pct}%$ {kind}.",
            ],
            "distractors": [
                f"$ {pct}% \" {'decrease' if inc else 'increase'}\" $",
                f"$ {delta}% \" {kind}\" $",
                f"$ {pct + 5}% \" {kind}\" $",
            ],
        }

    if c_low == "percents" and ("diagram" in t_low or "relating" in t_low or "equivalent" in t_low or "introduction" in t_low):
        pct = rng.choice([20, 25, 40, 50, 75, 80])
        whole = rng.choice([40, 60, 80, 120, 200])
        part = (whole * pct) // 100
        if "relating" in t_low:
            f = Fraction(pct, 100)
            return {
                "prompt_text": "Write the given percent as both a simplified fraction and a decimal.",
                "equation_typst": f"$ {pct}% $",
                "answer_typst": f"$ {_fmt_frac(f)} = {pct / 100:g} $",
                "steps_typst": [
                    f"Percent means per hundred: ${pct}% = ({pct})/(100)$.",
                    f"Reduce the fraction by dividing numerator and denominator by ${math.gcd(pct, 100)}$: ${_fmt_frac(f)}$.",
                    f"Divide by $100$ for the decimal form: ${pct / 100:g}$.",
                ],
                "distractors": [
                    f"$ ({pct})/(10) = {pct / 10:g} $",
                    f"$ {_fmt_frac(f)} = {pct:g} $",
                    f"$ ({100})/({pct}) = {100 / pct:.2f} $",
                ],
            }
        return {
            "prompt_text": "Use a percent tape diagram or equivalent ratio to solve the percent problem.",
            "equation_typst": f"\"Find \" {pct}% \" of \" {whole}",
            "answer_typst": f"$ {part} $",
            "steps_typst": [
                f"Write ${pct}%$ as the fraction $({pct})/(100)$.",
                f"Set up the equivalent fraction with whole ${whole}$: $({pct})/(100) = (x)/({whole})$.",
                f"Solve for $x$: $x = ({pct} times {whole})/(100) = {part}$.",
            ],
            "distractors": [f"$ {whole - part} $", f"$ {pct} $", f"$ {part + 10} $"],
            "diagram_svg": svg_tape_or_hanger(mode="tape", parts_labels=[f"{pct}% = ?", f"{100 - pct}%"], total_label=str(whole)),
            "answer_svg": svg_tape_or_hanger(mode="tape", parts_labels=[f"{pct}% = {part}", f"{whole - part}"], total_label=str(whole)),
        }

    # ------------------------------------------------------------------
    # 5. DECIMAL ARITHMETIC & AREA DIAGRAMS & LONG DIVISION
    # ------------------------------------------------------------------
    if c_low == "decimal arithmetic":
        a_int = rng.randint(12, 48)
        b_int = rng.randint(4, 15)
        a_dec = a_int / 10.0
        b_dec = b_int / 10.0
        if "addition" in t_low:
            res = round(a_dec + b_dec, 2)
            svg_d = svg_area_model([f"{a_dec:.1f}", f"{b_dec:.1f}"], "Sum", ["?", "?"], title="Decimal Addition Diagram") if "diagram" in t_low else None
            svg_a = svg_area_model([f"{a_dec:.1f}", f"{b_dec:.1f}"], f"= {res:.1f}", [f"{a_dec:.1f}", f"{b_dec:.1f}"], title="Decimal Addition Diagram") if "diagram" in t_low else None
            return {
                "prompt_text": "Find the sum of the decimals.",
                "equation_typst": f"$ {a_dec:.1f} + {b_dec:.1f} $",
                "answer_typst": f"$ {res:.1f} $",
                "steps_typst": [
                    "Line up the decimal points vertically.",
                    f"Add the tenths and ones columns: ${a_dec:.1f} + {b_dec:.1f} = {res:.1f}$.",
                    f"Answer: ${res:.1f}$",
                ],
                "distractors": [f"$ {abs(a_dec - b_dec):.1f} $", f"$ {res + 1:.1f} $", f"$ {res / 10:.2f} $"],
                "diagram_svg": svg_d,
                "answer_svg": svg_a,
            }
        if "subtraction" in t_low:
            if a_dec < b_dec:
                a_dec, b_dec = b_dec + 1.5, a_dec
            res = round(a_dec - b_dec, 2)
            svg_d = svg_area_model([f"Total: {a_dec:.1f}"], "-", [f"Subtract {b_dec:.1f}"], title="Decimal Subtraction Diagram") if "diagram" in t_low else None
            svg_a = svg_area_model([f"{b_dec:.1f}", f"{res:.1f}"], f"= {res:.1f}", [f"{b_dec:.1f}", f"{res:.1f}"], title="Decimal Subtraction Diagram") if "diagram" in t_low else None
            return {
                "prompt_text": "Find the difference of the decimals.",
                "equation_typst": f"$ {a_dec:.1f} - {b_dec:.1f} $",
                "answer_typst": f"$ {res:.1f} $",
                "steps_typst": [
                    "Align the decimal points vertically.",
                    f"Subtract tenths and ones: ${a_dec:.1f} - {b_dec:.1f} = {res:.1f}$.",
                    f"Answer: ${res:.1f}$",
                ],
                "distractors": [f"$ {a_dec + b_dec:.1f} $", f"$ {res + 0.2:.1f} $", f"$ {res + 1.0:.1f} $"],
                "diagram_svg": svg_d,
                "answer_svg": svg_a,
            }
        if "multiplication" in t_low:
            res = round(a_dec * b_dec, 2)
            w_part = int(a_dec)
            t_part = round(a_dec - w_part, 1)
            svg_d = svg_area_model([str(w_part), f"{t_part:.1f}"], f"{b_dec:.1f}", ["?", "?"], title="Decimal Area Model") if "area" in t_low else None
            svg_a = svg_area_model([str(w_part), f"{t_part:.1f}"], f"{b_dec:.1f}", [f"{w_part * b_dec:.2f}", f"{t_part * b_dec:.2f}"], title=f"Product = {res:.2f}") if "area" in t_low else None
            return {
                "prompt_text": "Find the decimal product.",
                "equation_typst": f"$ {a_dec:.1f} times {b_dec:.1f} $",
                "answer_typst": f"$ {res:.2f} $",
                "steps_typst": [
                    f"Write as tenths fractions: $({a_int})/(10) times ({b_int})/(10) = ({a_int * b_int})/(100)$.",
                    f"Place the decimal point two places from the right: ${res:.2f}$.",
                    f"Answer: ${res:.2f}$",
                ],
                "distractors": [f"$ {res * 10:.1f} $", f"$ {res / 10:.3f} $", f"$ {a_dec + b_dec:.2f} $"],
                "diagram_svg": svg_d,
                "answer_svg": svg_a,
            }
        if "remainders" in t_low:
            divisor = rng.randint(4, 9)
            quot = rng.randint(12, 35)
            rem = rng.randint(1, divisor - 1)
            dividend = divisor * quot + rem
            return {
                "prompt_text": "Divide using long division and state the quotient and remainder.",
                "equation_typst": f"$ {dividend} div {divisor} $",
                "answer_typst": f"$ {quot} \" R \" {rem} $",
                "steps_typst": [
                    f"Find the largest multiple of ${divisor}$ less than or equal to ${dividend}$: ${divisor} times {quot} = {divisor * quot}$.",
                    f"Subtract to find the remainder: ${dividend} - {divisor * quot} = {rem}$.",
                    f"Quotient: ${quot} \" R \" {rem}$.",
                ],
                "distractors": [f"$ {quot + 1} \" R \" {rem} $", f"$ {quot} \" R \" {divisor - rem} $", f"$ {rem} \" R \" {quot} $"],
            }
        # Decimal division
        quot_dec = round(rng.randint(12, 45) / 10.0, 1)
        div_val = rng.choice([2, 4, 5, 8]) if "whole" in t_low else round(rng.choice([2, 4, 5]) / 10.0, 1)
        dividend_val = round(quot_dec * div_val, 2)
        return {
            "prompt_text": "Find the quotient.",
            "equation_typst": f"$ {dividend_val:g} div {div_val:g} $",
            "answer_typst": f"$ {quot_dec:g} $",
            "steps_typst": [
                "Shift the decimal point in both dividend and divisor so the divisor is a whole number.",
                f"Divide as with whole numbers and align the decimal point: ${dividend_val:g} div {div_val:g} = {quot_dec:g}$.",
                f"Answer: ${quot_dec:g}$",
            ],
            "distractors": [f"$ {quot_dec * 10:g} $", f"$ {quot_dec / 10:g} $", f"$ {quot_dec + 1:g} $"],
        }

    # ------------------------------------------------------------------
    # 6. EXPRESSIONS, TAPE DIAGRAMS, HANGER DIAGRAMS, DISTRIBUTIVE AREA
    # ------------------------------------------------------------------
    if "tape diagram" in t_low or "hanger diagram" in t_low:
        is_hanger = "hanger" in t_low
        is_ineq = c_low == "inequalities"
        n = rng.choice([2, 3, 4])
        x_val = rng.randint(3, 9)
        b_val = rng.randint(2, 11)
        total = n * x_val + b_val
        labels = ["x"] * n + [str(b_val)]
        op = "<" if is_ineq else "="
        return {
            "prompt_text": f"Use the {'hanger' if is_hanger else 'tape'} diagram to write and solve the {'inequality' if is_ineq else 'equation'} for x.",
            "equation_typst": f"$ {n}x + {b_val} {op} {total} $",
            "answer_typst": f"$ x {op} {x_val} $",
            "steps_typst": [
                f"The diagram shows ${n}$ groups of $x$ plus ${b_val}$ balancing a total of ${total}$: ${n}x + {b_val} {op} {total}$.",
                f"Subtract ${b_val}$ from both sides: ${n}x {op} {total - b_val}$.",
                f"Divide by ${n}$: $x {op} {x_val}$.",
            ],
            "distractors": [
                f"$ x {op} {total - b_val} $",
                f"$ x {op} {x_val + 2} $",
                f"$ x {op} {(total + b_val) / n:g} $",
            ],
            "diagram_svg": svg_tape_or_hanger(mode="hanger" if is_hanger else "tape", parts_labels=labels, total_label=str(total)),
            "answer_svg": svg_tape_or_hanger(mode="hanger" if is_hanger else "tape", parts_labels=[str(x_val)] * n + [str(b_val)], total_label=f"x {op} {x_val}"),
        }

    if "area diagram" in t_low and "distributive" in t_low:
        is_num = "numeric" in t_low
        a = rng.randint(3, 8)
        b = rng.randint(4, 9)
        c = rng.randint(2, 7)
        if is_num:
            tot = a * (b + c)
            return {
                "prompt_text": "Use the area diagram and the Distributive Property to evaluate the numeric expression.",
                "equation_typst": f"$ {a}({b} + {c}) $",
                "answer_typst": f"$ {a * b} + {a * c} = {tot} $",
                "steps_typst": [
                    f"Multiply the height ${a}$ by the first width ${b}$: ${a} times {b} = {a * b}$.",
                    f"Multiply the height ${a}$ by the second width ${c}$: ${a} times {c} = {a * c}$.",
                    f"Add the partial areas: ${a * b} + {a * c} = {tot}$.",
                ],
                "distractors": [f"$ {a * b + c} $", f"$ {a + b + c} $", f"$ {tot + a} $"],
                "diagram_svg": svg_area_model([str(b), str(c)], str(a), ["?", "?"], title="Distributive Area Diagram"),
                "answer_svg": svg_area_model([str(b), str(c)], str(a), [str(a * b), str(a * c)], title=f"Total Area = {tot}"),
            }
        else:
            return {
                "prompt_text": "Use the area diagram and the Distributive Property to write an equivalent algebraic expression.",
                "equation_typst": f"$ {a}({b}x + {c}) $",
                "answer_typst": f"$ {a * b}x + {a * c} $",
                "steps_typst": [
                    f"Find the area of the first box: ${a} times {b}x = {a * b}x$.",
                    f"Find the area of the second box: ${a} times {c} = {a * c}$.",
                    f"Combine the partial areas: ${a * b}x + {a * c}$.",
                ],
                "distractors": [f"$ {a * b}x + {c} $", f"$ {b}x + {a * c} $", f"$ {a * b + a * c}x $"],
                "diagram_svg": svg_area_model([f"{b}x", str(c)], str(a), ["?", "?"], title="Algebraic Area Diagram"),
                "answer_svg": svg_area_model([f"{b}x", str(c)], str(a), [f"{a * b}x", str(a * c)], title=f"{a*b}x + {a*c}"),
            }

    if "evaluating" in t_low and "expression" in t_low:
        a = rng.randint(2, 6)
        b = rng.randint(3, 8)
        xv = rng.randint(2, 5)
        yv = rng.randint(2, 6)
        if difficulty == ProblemDifficulty.MILD:
            val = a * xv + b
            eq = f"$ {a}x + {b} quad \"for\" x = {xv} $"
            steps = [f"Substitute $x = {xv}$: ${a}({xv}) + {b}$.", f"Multiply: ${a * xv} + {b}$.", f"Add: ${val}$."]
        elif difficulty == ProblemDifficulty.MEDIUM:
            val = a * xv * xv - b * yv
            eq = f"$ {a}x^2 - {b}y quad \"for\" x = {xv}, y = {yv} $"
            steps = [f"Substitute $x = {xv}, y = {yv}$: ${a}({xv})^2 - {b}({yv})$.", f"Evaluate powers and products: ${a * xv * xv} - {b * yv}$.", f"Result: ${val}$."]
        else:
            val = (a * xv + yv) * (xv - 1)
            eq = f"$ ({a}x + y)(x - 1) quad \"for\" x = {xv}, y = {yv} $"
            steps = [f"Substitute $x = {xv}, y = {yv}$: $({a}({xv}) + {yv})({xv} - 1)$.", f"Simplify inside parentheses: $({a * xv + yv})({xv - 1})$.", f"Multiply: ${val}$."]
        return {
            "prompt_text": "Evaluate each algebraic expression for the given values of the variables.",
            "equation_typst": eq,
            "answer_typst": f"$ {val} $",
            "steps_typst": steps,
            "distractors": [f"$ {val + a} $", f"$ {val - b} $", f"$ {val * 2} $"],
        }

    if "combining like terms" in t_low or "simplifying algebraic expressions" in t_low:
        a = rng.randint(3, 9)
        b = rng.randint(2, 8)
        c = rng.randint(2, 7) * rng.choice([-1, 1])
        d = rng.randint(1, 9)
        coef = a + c
        const = b + d
        c_str = f"+ {c}x" if c > 0 else f"- {abs(c)}x"
        ans = f"$ {coef}x + {const} $"
        return {
            "prompt_text": "Simplify each expression by combining like terms.",
            "equation_typst": f"$ {a}x + {b} {c_str} + {d} $",
            "answer_typst": ans,
            "steps_typst": [
                f"Group the variable terms and constant terms: $({a}x {c_str}) + ({b} + {d})$.",
                f"Combine coefficients of $x$: ${a} + ({c}) = {coef}$.",
                f"Combine constants: ${b} + {d} = {const}$, giving ${coef}x + {const}$.",
            ],
            "distractors": [f"$ {a - c}x + {const} $", f"$ {coef + const}x $", f"$ {coef}x^2 + {const} $"],
        }

    # ------------------------------------------------------------------
    # 7. DEDICATED WORD PROBLEMS (MIXTURE, D=RT, WORK, SYSTEMS)
    # ------------------------------------------------------------------
    if "mixture word problems" in t_low:
        v1 = rng.choice([4, 6, 8, 10])
        c1 = rng.choice([10, 15, 20])
        c2 = rng.choice([40, 50, 60])
        v2 = rng.choice([2, 4, 6, 10])
        total_solute = v1 * c1 + v2 * c2
        if (total_solute) % (v1 + v2) != 0:
            v2 = v1
            total_solute = v1 * (c1 + c2)
        c_mix = total_solute // (v1 + v2)
        return {
            "prompt_text": "Set up an algebraic equation and solve the mixture word problem.",
            "equation_typst": f"\"How many liters of a \" {c2}% \" acid solution must be mixed with \" {v1} \" L of a \" {c1}% \" solution to obtain a \" {c_mix}% \" solution?\"",
            "answer_typst": f"$ {v2} \" liters\" $",
            "steps_typst": [
                f"Let $x$ be the liters of ${c2}%$ solution: $0.{c1:02d}({v1}) + 0.{c2:02d}x = 0.{c_mix:02d}({v1} + x)$.",
                f"Multiply by $100$: ${c1 * v1} + {c2}x = {c_mix * v1} + {c_mix}x$.",
                f"Solve for $x$: $({c2 - c_mix})x = {(c_mix - c1) * v1} arrow.r.double x = {v2}$ liters.",
            ],
            "distractors": [f"$ {v1 + 2} \" liters\" $", f"$ {v2 + 3} \" liters\" $", f"$ {max(1, v2 - 2)} \" liters\" $"],
        }

    if "distance, rate, time" in t_low:
        r1 = rng.choice([40, 45, 50, 55, 60])
        r2 = rng.choice([50, 55, 60, 65, 70])
        t = rng.randint(2, 5)
        dist = (r1 + r2) * t
        return {
            "prompt_text": "Use the distance-rate-time relationship d = rt to solve the word problem.",
            "equation_typst": f"\"Two trains leave a station traveling in opposite directions at \" {r1} \" mph and \" {r2} \" mph. After how many hours are they \" {dist} \" miles apart?\"",
            "answer_typst": f"$ t = {t} \" hours\" $",
            "steps_typst": [
                f"Since the trains travel in opposite directions, their combined rate of separation is ${r1} + {r2} = {r1 + r2}$ mph.",
                f"Write the distance equation: $({r1 + r2})t = {dist}$.",
                f"Divide by ${r1 + r2}$: $t = {t}$ hours.",
            ],
            "distractors": [f"$ t = {t + 1} \" hours\" $", f"$ t = {t + 2} \" hours\" $", f"$ t = {max(1, t - 1)} \" hours\" $"],
        }

    if "work word problems" in t_low:
        pairs = [(3, 6, 2), (4, 12, 3), (6, 12, 4), (5, 20, 4), (6, 30, 5)]
        t1, t2, both = rng.choice(pairs)
        if difficulty != ProblemDifficulty.MILD:
            k = rng.choice([2, 3])
            t1, t2, both = t1 * k, t2 * k, both * k
        return {
            "prompt_text": "Set up a rational work-rate equation and solve for the combined time.",
            "equation_typst": f"\"Pump A can fill a tank in \" {t1} \" hours and Pump B can fill it in \" {t2} \" hours. How long will it take both pumps working together?\"",
            "answer_typst": f"$ t = {both} \" hours\" $",
            "steps_typst": [
                f"Combine hourly work rates: $1/({t1}) + 1/({t2}) = 1/t$.",
                f"Find a common denominator of ${t2}$: $({t2 // t1 + 1})/({t2}) = 1/t$.",
                f"Solve for $t$: $t = {both}$ hours.",
            ],
            "distractors": [f"$ t = {(t1 + t2) // 2} \" hours\" $", f"$ t = {t1 + t2} \" hours\" $", f"$ t = {both + 2} \" hours\" $"],
        }

    if "systems" in c_low and "word problems" in t_low:
        adults = rng.randint(5, 15)
        kids = rng.randint(6, 18)
        pa, pk = rng.choice([(8, 5), (10, 6), (12, 7), (9, 4)])
        tot_tickets = adults + kids
        tot_rev = adults * pa + kids * pk
        return {
            "prompt_text": "Write and solve a system of two linear equations to answer the word problem.",
            "equation_typst": f"\"A theater sold \" {tot_tickets} \" tickets for a total of $\"{tot_rev}\". Adult tickets cost $\"{pa}\" and child tickets cost $\"{pk}\". How many of each were sold?\"",
            "answer_typst": f"$ \"Adults\" = {adults}, \" Children\" = {kids} $",
            "steps_typst": [
                f"Let $a$ be adult tickets and $c$ be child tickets: $a + c = {tot_tickets}$ and ${pa}a + {pk}c = {tot_rev}$.",
                f"Substitute $c = {tot_tickets} - a$: ${pa}a + {pk}({tot_tickets} - a) = {tot_rev}$.",
                f"Solve: $({pa - pk})a = {tot_rev - pk * tot_tickets} arrow.r.double a = {adults}$ and $c = {kids}$.",
            ],
            "distractors": [
                f"$ \"Adults\" = {kids}, \" Children\" = {adults} $",
                f"$ \"Adults\" = {adults + 2}, \" Children\" = {kids - 2} $",
                f"$ \"Adults\" = {adults - 1}, \" Children\" = {kids + 1} $",
            ],
        }

    # ------------------------------------------------------------------
    # 8. INEQUALITIES (COMPOUND, ABSOLUTE VALUE, ONE-STEP, TWO-STEP, MULTI-STEP)
    # ------------------------------------------------------------------
    if "compound inequalities" in t_low:
        a = rng.randint(2, 5)
        b = rng.randint(-5, 5)
        x1 = rng.randint(-6, -1)
        x2 = rng.randint(2, 7)
        if difficulty == ProblemDifficulty.SPICY:
            # Disjunction OR
            left_v = a * x1 + b
            right_v = a * x2 + b
            b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
            return {
                "prompt_text": "Solve the compound inequality and graph its solution set on the number line.",
                "equation_typst": f"$ {a}x {b_str} <= {left_v} quad \"or\" quad {a}x {b_str} > {right_v} $",
                "answer_typst": f"$ x <= {x1} \" or \" x > {x2} $",
                "steps_typst": [
                    f"Solve the first inequality: ${a}x <= {left_v - b} arrow.r.double x <= {x1}$.",
                    f"Solve the second inequality: ${a}x > {right_v - b} arrow.r.double x > {x2}$.",
                    f"Combine the disjunction: $x <= {x1}$ or $x > {x2}$.",
                ],
                "distractors": [
                    f"$ {x1} <= x < {x2} $",
                    f"$ x < {x1} \" or \" x >= {x2} $",
                    f"$ x <= {x1 - 1} \" or \" x > {x2 + 1} $",
                ],
                "diagram_svg": svg_number_line(),
                "answer_svg": svg_number_line(rays=[(x1, "left", True), (x2, "right", False)]),
            }
        # Conjunction AND: low < a*x + b <= high
        low = a * x1 + b
        high = a * x2 + b
        b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        return {
            "prompt_text": "Solve the compound inequality and graph its solution set on the number line.",
            "equation_typst": f"$ {low} < {a}x {b_str} <= {high} $",
            "answer_typst": f"$ {x1} < x <= {x2} $",
            "steps_typst": [
                f"Isolate the $x$-term in the middle by subtracting ${b}$ from all three parts: ${low - b} < {a}x <= {high - b}$.",
                f"Divide all three parts by ${a}$: ${x1} < x <= {x2}$.",
                f"Graph an open circle at ${x1}$, a closed circle at ${x2}$, and shade between them.",
            ],
            "distractors": [
                f"$ {x1} <= x < {x2} $",
                f"$ x < {x1} \" or \" x >= {x2} $",
                f"$ {x1 - 1} < x <= {x2 + 1} $",
            ],
            "diagram_svg": svg_number_line(),
            "answer_svg": svg_number_line(segments=[(x1, x2, False, True)]),
        }

    if "absolute value inequalit" in t_low:
        c = rng.randint(-4, 4)
        r = rng.randint(2, 6)
        x1, x2 = c - r, c + r
        c_str = f"- {c}" if c >= 0 else f"+ {abs(c)}"
        if difficulty == ProblemDifficulty.SPICY:
            return {
                "prompt_text": "Solve the absolute value inequality and graph its solution set on the number line.",
                "equation_typst": f"$ |x {c_str}| >= {r} $",
                "answer_typst": f"$ x <= {x1} \" or \" x >= {x2} $",
                "steps_typst": [
                    f"Rewrite $|x {c_str}| >= {r}$ as a compound 'or' inequality: $x {c_str} <= {-r}$ or $x {c_str} >= {r}$.",
                    f"Add ${c}$ to both sides of each inequality: $x <= {x1}$ or $x >= {x2}$.",
                    "Graph closed circles with rays pointing outward.",
                ],
                "distractors": [f"$ {x1} <= x <= {x2} $", f"$ x < {x1} \" or \" x > {x2} $", f"$ x >= {x2} $"],
                "diagram_svg": svg_number_line(),
                "answer_svg": svg_number_line(rays=[(x1, "left", True), (x2, "right", True)]),
            }
        return {
            "prompt_text": "Solve the absolute value inequality and graph its solution set on the number line.",
            "equation_typst": f"$ |x {c_str}| < {r} $",
            "answer_typst": f"$ {x1} < x < {x2} $",
            "steps_typst": [
                f"Rewrite $|x {c_str}| < {r}$ as a three-part inequality: ${-r} < x {c_str} < {r}$.",
                f"Add ${c}$ to all three parts: ${x1} < x < {x2}$.",
                f"Graph open circles at ${x1}$ and ${x2}$ and shade the interval between them.",
            ],
            "distractors": [f"$ x < {x1} \" or \" x > {x2} $", f"$ {x1} <= x <= {x2} $", f"$ {-r} < x < {r} $"],
            "diagram_svg": svg_number_line(),
            "answer_svg": svg_number_line(segments=[(x1, x2, False, False)]),
        }

    # ------------------------------------------------------------------
    # 9. RELATIONS, FUNCTIONS, VARIATION, SCIENTIFIC NOTATION
    # ------------------------------------------------------------------
    if "discrete relations" in t_low:
        xs = rng.sample(range(-5, 6), 4)
        ys = [rng.randint(-5, 5) for _ in range(4)]
        is_func = True
        if difficulty == ProblemDifficulty.SPICY:
            xs[3] = xs[0]
            ys[3] = ys[0] + 2 if ys[0] <= 3 else ys[0] - 2
            is_func = False
        dom = sorted(set(xs))
        ran = sorted(set(ys))
        pts = list(zip(xs, ys, strict=False))
        fn_str = "Function" if is_func else "Not a function"
        return {
            "prompt_text": "State the domain and range of the discrete relation, plot the points, and determine whether it is a function.",
            "equation_typst": f"$ \\{{ {', '.join(f'({x}, {y})' for x, y in pts)} \\}} $",
            "answer_typst": f"$ \"D\" = \\{{{', '.join(map(str, dom))}\\}}, \" R\" = \\{{{', '.join(map(str, ran))}\\}}, \" {fn_str}\" $",
            "steps_typst": [
                f"The domain is the set of all input $x$-coordinates: $\\{{{', '.join(map(str, dom))}\\}}$.",
                f"The range is the set of all output $y$-coordinates: $\\{{{', '.join(map(str, ran))}\\}}$.",
                f"Check if each input $x$ has exactly one output $y$: {fn_str}.",
            ],
            "distractors": [
                f"$ \"D\" = \\{{{', '.join(map(str, ran))}\\}}, \" R\" = \\{{{', '.join(map(str, dom))}\\}}, \" {fn_str}\" $",
                f"$ \"D\" = \\{{{', '.join(map(str, dom))}\\}}, \" R\" = \\{{{', '.join(map(str, ran))}\\}}, \" {'Not a function' if is_func else 'Function'}\" $",
                f"$ \"D\" = [-5, 5], \" R\" = [-5, 5], \" {fn_str}\" $",
            ],
            "diagram_svg": svg_data_table(["x", "y"], [[str(x), str(y)] for x, y in pts]),
            "answer_svg": svg_coordinate_plane(points=[(x, y, "", True) for x, y in pts]),
        }

    if "continuous relations" in t_low:
        x1, x2 = rng.randint(-6, -2), rng.randint(2, 6)
        y1, y2 = rng.randint(-5, -1), rng.randint(1, 6)
        return {
            "prompt_text": "Find the domain and range of the continuous relation shown on the coordinate plane and state whether it is a function.",
            "equation_typst": "\"Determine the domain and range of the graphed relation\"",
            "answer_typst": f"$ \"Domain\": [{x1}, {x2}], quad \"Range\": [{y1}, {y2}], quad \"Function\" $",
            "steps_typst": [
                f"Read the horizontal extent from left to right for the domain: ${x1} <= x <= {x2}$, or $[{x1}, {x2}]$.",
                f"Read the vertical extent from bottom to top for the range: ${y1} <= y <= {y2}$, or $[{y1}, {y2}]$.",
                "Every vertical line intersects the graph at most once (Vertical Line Test), so it is a Function.",
            ],
            "distractors": [
                f"$ \"Domain\": [{y1}, {y2}], quad \"Range\": [{x1}, {x2}], quad \"Function\" $",
                f"$ \"Domain\": ({x1}, {x2}), quad \"Range\": ({y1}, {y2}), quad \"Not a function\" $",
                f"$ \"Domain\": [{x1}, {y2}], quad \"Range\": [{y1}, {x2}], quad \"Function\" $",
            ],
            "diagram_svg": svg_coordinate_plane(polygons=[{"points": [(x1, y1), (x2, y2)], "stroke": "#2563eb", "fill": "none"}], points=[(x1, y1, "", True), (x2, y2, "", True)]),
            "answer_svg": svg_coordinate_plane(polygons=[{"points": [(x1, y1), (x2, y2)], "stroke": "#2563eb", "fill": "none"}], points=[(x1, y1, f"({x1},{y1})", True), (x2, y2, f"({x2},{y2})", True)]),
        }

    if "direct and inverse variation" in t_low:
        is_inv = difficulty == ProblemDifficulty.SPICY or (difficulty == ProblemDifficulty.MEDIUM and rng.random() < 0.5)
        x1 = rng.randint(2, 6)
        k = rng.randint(3, 8)
        x2 = rng.choice([x for x in [2, 3, 4, 6, 8] if x != x1])
        if is_inv:
            prod = x1 * x2 * rng.randint(1, 3)
            y1 = prod // x1
            y2 = prod // x2
            return {
                "prompt_text": "Write an inverse variation equation relating x and y, then find y for the given x.",
                "equation_typst": f"\"Suppose \" y \" varies inversely with \" x \", and \" y = {y1} \" when \" x = {x1} \". Find \" y \" when \" x = {x2} \".\"",
                "answer_typst": f"$ y = ({prod})/(x); quad y = {y2} $",
                "steps_typst": [
                    f"Inverse variation has the form $y = k/x$, where $k = x y = {x1}({y1}) = {prod}$.",
                    f"Write the model: $y = ({prod})/(x)$.",
                    f"Substitute $x = {x2}$: $y = ({prod})/({x2}) = {y2}$.",
                ],
                "distractors": [
                    f"$ y = {prod}x; quad y = {prod * x2} $",
                    f"$ y = ({prod})/(x); quad y = {y1} $",
                    f"$ y = ({y1})/(x); quad y = {y2 + 2} $",
                ],
            }
        y1 = k * x1
        y2 = k * x2
        return {
            "prompt_text": "Write a direct variation equation relating x and y, then find y for the given x.",
            "equation_typst": f"\"Suppose \" y \" varies directly with \" x \", and \" y = {y1} \" when \" x = {x1} \". Find \" y \" when \" x = {x2} \".\"",
            "answer_typst": f"$ y = {k}x; quad y = {y2} $",
            "steps_typst": [
                f"Direct variation has the form $y = k x$. Solve for $k = y/x = ({y1})/({x1}) = {k}$.",
                f"Write the direct variation equation: $y = {k}x$.",
                f"Substitute $x = {x2}$: $y = {k}({x2}) = {y2}$.",
            ],
            "distractors": [
                f"$ y = ({k})/(x); quad y = {k / x2:g} $",
                f"$ y = {k}x; quad y = {y2 + k} $",
                f"$ y = x + {y1 - x1}; quad y = {x2 + y1 - x1} $",
            ],
        }

    # ------------------------------------------------------------------
    # 10. POLYNOMIALS (NAMING, SPECIAL CASES, FACTORING TECHNIQUES)
    # ------------------------------------------------------------------
    if "polynomial" in c_low and "naming" in t_low:
        deg = rng.choice([0, 1, 2, 3, 4])
        nterms = 1 if deg == 0 else rng.choice([1, 2, 3][: deg + 1])
        deg_names = {0: "constant", 1: "linear", 2: "quadratic", 3: "cubic", 4: "quartic"}
        term_names = {1: "monomial", 2: "binomial", 3: "trinomial"}
        lead = rng.randint(2, 9) * rng.choice([-1, 1])
        if deg == 0:
            expr = f"{lead}"
        else:
            parts = [f"{lead}x^{deg}" if deg > 1 else f"{lead}x"]
            if nterms >= 2:
                c2 = rng.randint(2, 8)
                parts.append(f"+ {c2}x" if deg > 1 else f"+ {c2}")
            if nterms >= 3:
                c3 = rng.randint(1, 9)
                parts.append(f"- {c3}")
            expr = " ".join(parts)
        ans_name = f"{deg_names[deg]} {term_names[nterms]}"
        return {
            "prompt_text": "Name each polynomial by degree and number of terms.",
            "equation_typst": f"$ {expr} $",
            "answer_typst": f"$ \"{ans_name}\" $",
            "steps_typst": [
                f"The highest exponent of $x$ is ${deg}$, so the degree is {deg_names[deg]}.",
                f"There {'is' if nterms == 1 else 'are'} ${nterms}$ term{'s' if nterms > 1 else ''}, making it a {term_names[nterms]}.",
                f"Classification: {ans_name}.",
            ],
            "distractors": [
                f"$ \"{deg_names[(deg + 1) % 5]} {term_names[nterms]}\" $",
                f"$ \"{deg_names[deg]} {term_names[(nterms % 3) + 1]}\" $",
                f"$ \"{deg_names[(deg + 2) % 5]} {term_names[(nterms % 3) + 1]}\" $",
            ],
        }

    if "multiplying special cases" in t_low:
        a = 1 if difficulty == ProblemDifficulty.MILD else rng.randint(2, 5)
        b = rng.randint(2, 8)
        ax = "x" if a == 1 else f"{a}x"
        if difficulty == ProblemDifficulty.MEDIUM:
            # Difference of squares (ax + b)(ax - b)
            return {
                "prompt_text": "Find each special product.",
                "equation_typst": f"$ ({ax} + {b})({ax} - {b}) $",
                "answer_typst": f"$ {'' if a == 1 else a * a}x^2 - {b * b} $",
                "steps_typst": [
                    "Apply the sum and difference pattern $(A + B)(A - B) = A^2 - B^2$.",
                    f"Square the first term $({ax})^2 = {'' if a == 1 else a * a}x^2$ and the second term ${b}^2 = {b * b}$.",
                    f"Result: ${'' if a == 1 else a * a}x^2 - {b * b}$.",
                ],
                "distractors": [
                    f"$ {'' if a == 1 else a * a}x^2 + {b * b} $",
                    f"$ {'' if a == 1 else a * a}x^2 - {2 * a * b}x + {b * b} $",
                    f"$ {'' if a == 1 else a * a}x^2 + {2 * a * b}x - {b * b} $",
                ],
            }
        sgn = "+" if rng.random() < 0.5 else "-"
        mid = 2 * a * b
        return {
            "prompt_text": "Find each special product.",
            "equation_typst": f"$ ({ax} {sgn} {b})^2 $",
            "answer_typst": f"$ {'' if a == 1 else a * a}x^2 {sgn} {mid}x + {b * b} $",
            "steps_typst": [
                f"Apply the square of a binomial pattern $(A {sgn} B)^2 = A^2 {sgn} 2AB + B^2$.",
                f"Compute $A^2 = {'' if a == 1 else a * a}x^2$, $2AB = {mid}x$, and $B^2 = {b * b}$.",
                f"Combine terms: ${'' if a == 1 else a * a}x^2 {sgn} {mid}x + {b * b}$.",
            ],
            "distractors": [
                f"$ {'' if a == 1 else a * a}x^2 + {b * b} $",
                f"$ {'' if a == 1 else a * a}x^2 {sgn} {a * b}x + {b * b} $",
                f"$ {'' if a == 1 else a * a}x^2 {'-' if sgn == '+' else '+'} {mid}x + {b * b} $",
            ],
        }

    if "common factor only" in t_low:
        k = rng.randint(2, 7)
        a = rng.randint(2, 5)
        b = rng.choice([x for x in range(1, 8) if math.gcd(a, x) == 1])
        p = 1 if difficulty == ProblemDifficulty.MILD else rng.choice([2, 3])
        xp = "x" if p == 1 else f"x^{p}"
        xp1 = f"x^{p + 1}"
        return {
            "prompt_text": "Factor the greatest common factor (GCF) out of the polynomial.",
            "equation_typst": f"$ {k * a}{xp1} + {k * b}{xp} $",
            "answer_typst": f"$ {k}{xp}({a}x + {b}) $",
            "steps_typst": [
                f"Find the GCF of the coefficients ${k * a}$ and ${k * b}$, which is ${k}$.",
                f"Find the highest shared power of $x$, which is ${xp}$.",
                f"Factor out ${k}{xp}$: ${k}{xp}({a}x + {b})$.",
            ],
            "distractors": [
                f"$ {k}({a}{xp1} + {b}{xp}) $",
                f"$ {xp}({k * a}x + {k * b}) $",
                f"$ {k}{xp}({a}x + {k * b}) $",
            ],
        }

    if "by grouping" in t_low:
        a = rng.randint(1, 3)
        b = rng.randint(2, 5)
        c = rng.randint(2, 6)
        ax2 = "x^2" if a == 1 else f"{a}x^2"
        # (ax^2 + b)(x + c) = a x^3 + a*c x^2 + b x + b*c
        return {
            "prompt_text": "Factor each four-term polynomial by grouping.",
            "equation_typst": f"$ {'' if a == 1 else a}x^3 + {a * c}x^2 + {b}x + {b * c} $",
            "answer_typst": f"$ ({ax2} + {b})(x + {c}) $",
            "steps_typst": [
                f"Group the first two terms and last two terms: $({'' if a == 1 else a}x^3 + {a * c}x^2) + ({b}x + {b * c})$.",
                f"Factor out the GCF from each pair: ${ax2}(x + {c}) + {b}(x + {c})$.",
                f"Factor out the common binomial $(x + {c})$: $({ax2} + {b})(x + {c})$.",
            ],
            "distractors": [
                f"$ ({ax2} - {b})(x - {c}) $",
                f"$ ({ax2} + {c})(x + {b}) $",
                f"$ ({ax2} + {b})(x - {c}) $",
            ],
        }

    if "graphing quadratic inequalities" in t_low:
        h = rng.randint(-3, 3)
        k = rng.randint(-4, 4)
        a = rng.choice([1, -1]) if difficulty != ProblemDifficulty.SPICY else rng.choice([2, -2])
        op = rng.choice(["<", "<=", ">", ">="])
        dashed = op in ("<", ">")
        shade_above = op in (">", ">=")
        h_part = f"(x - {h})^2" if h > 0 else (f"(x + {abs(h)})^2" if h < 0 else "x^2")
        a_str = "" if a == 1 else ("-" if a == -1 else str(a))
        k_str = f" + {k}" if k > 0 else (f" - {abs(k)}" if k < 0 else "")

        def _fn_quad(x, _a=a, _h=h, _k=k):
            return _a * ((x - _h) ** 2) + _k
        # Build shaded region polygon along parabola
        xs = [x / 2.0 for x in range(-14, 15)]
        poly_pts = [(x, max(-10.0, min(10.0, _fn_quad(x)))) for x in xs]
        cap_y = 10.0 if shade_above else -10.0
        poly_pts.extend([(7.0, cap_y), (-7.0, cap_y)])
        return {
            "prompt_text": "Sketch the graph of each quadratic inequality.",
            "equation_typst": f"$ y {op} {a_str}{h_part}{k_str} $",
            "answer_typst": f"$ \"Vertex\": ({h}, {k}), \" {'Dashed' if dashed else 'Solid'} parabola, shade {'above' if shade_above else 'below'}\" $",
            "steps_typst": [
                f"Identify the vertex at $({h}, {k})$ and axis of symmetry $x = {h}$.",
                f"Draw a {'dashed' if dashed else 'solid'} parabola opening {'upward' if a > 0 else 'downward'}.",
                f"Since the inequality is $y {op} ...$, shade the region {'above' if shade_above else 'below'} the parabola.",
            ],
            "distractors": [
                f"$ \"Vertex\": ({h}, {k}), \" {'Solid' if dashed else 'Dashed'} parabola, shade {'below' if shade_above else 'above'}\" $",
                f"$ \"Vertex\": ({-h}, {k}), \" {'Dashed' if dashed else 'Solid'} parabola, shade {'above' if shade_above else 'below'}\" $",
                f"$ \"Vertex\": ({h}, {-k}), \" {'Dashed' if dashed else 'Solid'} parabola, shade {'below' if shade_above else 'above'}\" $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(
                polygons=[{"points": poly_pts, "fill": "#3b82f6", "stroke": "none"}],
                functions=[{"fn": _fn_quad, "color": "#1d4ed8", "dashed": dashed}],
                points=[(h, k, f"V({h},{k})", True)],
            ),
        }

    # ------------------------------------------------------------------
    # 11. COORDINATE PLANE, DISTANCE, MIDPOINT, TRANSFORMATIONS
    # ------------------------------------------------------------------
    if "points on the coordinate" in t_low or "points of the coordinate" in t_low:
        x = rng.choice([-7, -5, -3, -2, 2, 4, 6, 7])
        y = rng.choice([-7, -4, -2, 3, 5, 7])
        quad = "Quadrant I" if (x > 0 and y > 0) else ("Quadrant II" if (x < 0 and y > 0) else ("Quadrant III" if (x < 0 and y < 0) else "Quadrant IV"))
        return {
            "prompt_text": "Plot point P on the coordinate plane and identify its quadrant.",
            "equation_typst": f"$ P({x}, {y}) $",
            "answer_typst": f"$ P({x}, {y}), quad \"{quad}\" $",
            "steps_typst": [
                f"Move horizontally along the $x$-axis to $x = {x}$.",
                f"Move vertically parallel to the $y$-axis to $y = {y}$.",
                f"The point is $P({x}, {y})$ in {quad}.",
            ],
            "distractors": [
                f"$ P({y}, {x}), quad \"{quad}\" $",
                f"$ P({-x}, {y}), quad \"Quadrant {'II' if quad == 'Quadrant I' else 'I'}\" $",
                f"$ P({x}, {-y}), quad \"Quadrant {'IV' if quad == 'Quadrant I' else 'III'}\" $",
            ],
            "diagram_svg": svg_coordinate_plane(),
            "answer_svg": svg_coordinate_plane(points=[(x, y, f"P({x},{y})", True)]),
        }

    if "midpoint formula" in t_low:
        x1, y1 = rng.randint(-6, 2) * 2, rng.randint(-6, 2) * 2
        x2, y2 = rng.randint(-2, 6) * 2, rng.randint(-2, 6) * 2
        if (x1, y1) == (x2, y2):
            x2 += 4
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        return {
            "prompt_text": "Find the midpoint of the line segment with the given endpoints.",
            "equation_typst": f"$ ({x1}, {y1}) \" and \" ({x2}, {y2}) $",
            "answer_typst": f"$ M({mx}, {my}) $",
            "steps_typst": [
                "Use the Midpoint Formula: $M = ((x_1 + x_2)/2, (y_1 + y_2)/2)$.",
                f"Average the coordinates: $M = (({x1} + {x2})/2, ({y1} + {y2})/2)$.",
                f"Midpoint: $M({mx}, {my})$.",
            ],
            "distractors": [
                f"$ M({x2 - x1}, {y2 - y1}) $",
                f"$ M({(x2 - x1) // 2}, {(y2 - y1) // 2}) $",
                f"$ M({mx + 1}, {my - 1}) $",
            ],
            "diagram_svg": svg_coordinate_plane(
                polygons=[{"points": [(x1 / 2, y1 / 2), (x2 / 2, y2 / 2)], "stroke": "#2563eb", "fill": "none"}],
                points=[(x1 / 2, y1 / 2, "A", True), (x2 / 2, y2 / 2, "B", True)],
            ),
            "answer_svg": svg_coordinate_plane(
                polygons=[{"points": [(x1 / 2, y1 / 2), (x2 / 2, y2 / 2)], "stroke": "#2563eb", "fill": "none"}],
                points=[(x1 / 2, y1 / 2, "A", True), (x2 / 2, y2 / 2, "B", True), (mx / 2, my / 2, f"M({mx},{my})", True)],
            ),
        }

    if "distance formula" in t_low or "distances on the coordinate" in t_low or "distances, word" in t_low:
        triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13)]
        dx, dy, d = rng.choice(triples)
        x1, y1 = rng.randint(-5, 1), rng.randint(-5, 1)
        x2, y2 = x1 + dx, y1 + dy
        return {
            "prompt_text": "Find the distance between the two points on the coordinate plane.",
            "equation_typst": f"$ ({x1}, {y1}) \" and \" ({x2}, {y2}) $",
            "answer_typst": f"$ d = {d} $",
            "steps_typst": [
                "Use the Distance Formula: $d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2)$.",
                f"Substitute the coordinates: $d = sqrt(({x2} - ({x1}))^2 + ({y2} - ({y1}))^2) = sqrt({dx}^2 + {dy}^2)$.",
                f"Simplify: $d = sqrt({dx*dx + dy*dy}) = {d}$.",
            ],
            "distractors": [f"$ d = {dx + dy} $", f"$ d = sqrt({dx + dy}) $", f"$ d = {d + 2} $"],
            "diagram_svg": svg_coordinate_plane(
                polygons=[{"points": [(x1, y1), (x2, y2)], "stroke": "#2563eb", "fill": "none"}],
                points=[(x1, y1, "A", True), (x2, y2, "B", True)],
            ),
            "answer_svg": svg_coordinate_plane(
                polygons=[{"points": [(x1, y1), (x2, y2)], "stroke": "#dc2626", "fill": "none"}],
                points=[(x1, y1, f"({x1},{y1})", True), (x2, y2, f"d={d}", True)],
            ),
        }

    if "shapes and perimeter" in t_low or "polygons on a grid" in t_low:
        w = rng.randint(4, 8)
        h = rng.randint(3, 7)
        x0, y0 = -w // 2, -h // 2
        pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
        perim = 2 * (w + h)
        area = w * h
        return {
            "prompt_text": "Find the perimeter and area of the rectangle plotted on the coordinate plane.",
            "equation_typst": f"\"Vertices: \" ({x0}, {y0}), ({x0+w}, {y0}), ({x0+w}, {y0+h}), ({x0}, {y0+h})",
            "answer_typst": f"$ P = {perim}, quad A = {area} $",
            "steps_typst": [
                f"Find the horizontal width: $|{x0 + w} - ({x0})| = {w}$ units.",
                f"Find the vertical height: $|{y0 + h} - ({y0})| = {h}$ units.",
                f"Compute Perimeter $P = 2({w} + {h}) = {perim}$ and Area $A = {w} times {h} = {area}$.",
            ],
            "distractors": [
                f"$ P = {w + h}, quad A = {area} $",
                f"$ P = {area}, quad A = {perim} $",
                f"$ P = {perim + 4}, quad A = {area + w} $",
            ],
            "diagram_svg": svg_coordinate_plane(polygons=[{"points": pts, "fill": "#3b82f6", "stroke": "#1d4ed8"}]),
            "answer_svg": svg_coordinate_plane(polygons=[{"points": pts, "fill": "#22c55e", "stroke": "#15803d"}], points=[(x0, y0, f"w={w}, h={h}", True)]),
        }

    if "translations, rotations, reflections" in t_low:
        pts = [(1, 2), (5, 2), (2, 6)]
        dx = rng.choice([-6, -5, -4])
        dy = rng.choice([-6, -5, -4])
        img_pts = [(x + dx, y + dy) for x, y in pts]
        return {
            "prompt_text": "Find the coordinates of the image of triangle ABC under the given transformation and sketch both on the coordinate plane.",
            "equation_typst": f"\"Translate \" triangle A(1, 2), B(5, 2), C(2, 6) \" by \" (x, y) arrow.r (x - {abs(dx)}, y - {abs(dy)})",
            "answer_typst": f"$ A'({img_pts[0][0]}, {img_pts[0][1]}), B'({img_pts[1][0]}, {img_pts[1][1]}), C'({img_pts[2][0]}, {img_pts[2][1]}) $",
            "steps_typst": [
                f"Apply the translation rule $(x, y) arrow.r (x - {abs(dx)}, y - {abs(dy)})$ to each vertex.",
                f"$A(1, 2) arrow.r A'({img_pts[0][0]}, {img_pts[0][1]})$ and $B(5, 2) arrow.r B'({img_pts[1][0]}, {img_pts[1][1]})$.",
                f"$C(2, 6) arrow.r C'({img_pts[2][0]}, {img_pts[2][1]})$.",
            ],
            "distractors": [
                f"$ A'({1 + abs(dx)}, {2 + abs(dy)}), B'({5 + abs(dx)}, {2 + abs(dy)}), C'({2 + abs(dx)}, {6 + abs(dy)}) $",
                "$ A'(-1, -2), B'(-5, -2), C'(-2, -6) $",
                f"$ A'({img_pts[0][1]}, {img_pts[0][0]}), B'({img_pts[1][1]}, {img_pts[1][0]}), C'({img_pts[2][1]}, {img_pts[2][0]}) $",
            ],
            "diagram_svg": svg_coordinate_plane(polygons=[{"points": pts, "fill": "#3b82f6", "stroke": "#1d4ed8"}]),
            "answer_svg": svg_coordinate_plane(
                polygons=[
                    {"points": pts, "fill": "#3b82f6", "stroke": "#1d4ed8"},
                    {"points": img_pts, "fill": "#ef4444", "stroke": "#dc2626"},
                ]
            ),
        }

    # ------------------------------------------------------------------
    # 12. GEOMETRY: SEGMENTS, ANGLES, PARALLEL LINES, TRIANGLES, POLYGONS, SOLIDS, CIRCLES
    # ------------------------------------------------------------------
    if "segment" in t_low and ("addition" in t_low or "measures" in t_low or "construction" in c_low):
        ab = rng.randint(5, 16)
        bc = rng.randint(6, 18)
        ac = ab + bc
        if difficulty != ProblemDifficulty.MILD:
            xv = rng.randint(3, 9)
            a_coef = rng.randint(2, 4)
            ab = a_coef * xv
            ac = ab + bc
            return {
                "prompt_text": "Point B is between A and C. Use the Segment Addition Postulate to solve for x.",
                "equation_typst": f"$ A B = {a_coef}x, quad B C = {bc}, quad A C = {ac} $",
                "answer_typst": f"$ x = {xv} $",
                "steps_typst": [
                    "By the Segment Addition Postulate, $A B + B C = A C$.",
                    f"Substitute the given lengths: ${a_coef}x + {bc} = {ac}$.",
                    f"Solve for $x$: ${a_coef}x = {ab} arrow.r.double x = {xv}$.",
                ],
                "distractors": [f"$ x = {ac} $", f"$ x = {xv + 2} $", f"$ x = {ab} $"],
                "diagram_svg": svg_number_line(min_val=0, max_val=20, points=[(2, "A"), (10, "B"), (18, "C")], segments=[(2, 18, True, True)]),
                "answer_svg": svg_number_line(min_val=0, max_val=20, points=[(2, "A"), (10, f"AB={ab}"), (18, f"AC={ac}")], segments=[(2, 18, True, True)]),
            }
        return {
            "prompt_text": "Point B is between A and C. Find the length of segment AC.",
            "equation_typst": f"$ A B = {ab}, quad B C = {bc} $",
            "answer_typst": f"$ A C = {ac} $",
            "steps_typst": [
                "By the Segment Addition Postulate, $A B + B C = A C$.",
                f"Add the lengths: ${ab} + {bc} = {ac}$.",
                f"Answer: $A C = {ac}$.",
            ],
            "distractors": [f"$ A C = {abs(ab - bc)} $", f"$ A C = {ac + 2} $", f"$ A C = {ab * bc} $"],
            "diagram_svg": svg_number_line(min_val=0, max_val=20, points=[(2, "A"), (10, "B"), (18, "C")], segments=[(2, 18, True, True)]),
            "answer_svg": svg_number_line(min_val=0, max_val=20, points=[(2, "A"), (10, "B"), (18, f"AC={ac}")], segments=[(2, 18, True, True)]),
        }

    if "classifying angles" in t_low or "basic angle terminology" in t_low:
        deg = rng.choice([35, 62, 90, 118, 145, 180])
        kind = "Acute" if deg < 90 else ("Right" if deg == 90 else ("Obtuse" if deg < 180 else "Straight"))
        return {
            "prompt_text": "Classify the angle as acute, right, obtuse, or straight.",
            "equation_typst": f"$ m angle A B C = {deg}^circle $",
            "answer_typst": f"$ \"{kind} angle\" $",
            "steps_typst": [
                "Recall: Acute ($0^circle < theta < 90^circle$), Right ($90^circle$), Obtuse ($90^circle < theta < 180^circle$), Straight ($180^circle$).",
                f"Compare ${deg}^circle$ to $90^circle$ and $180^circle$.",
                f"Classification: {kind} angle.",
            ],
            "distractors": [
                f"$ \"{'Obtuse' if kind != 'Obtuse' else 'Acute'} angle\" $",
                f"$ \"{'Right' if kind != 'Right' else 'Straight'} angle\" $",
                "$ \"Reflex angle\" $",
            ],
            "diagram_svg": svg_parallel_transversal(mode="linear_pair", angle1_label=f"{deg} deg", angle2_label=""),
            "answer_svg": svg_parallel_transversal(mode="linear_pair", angle1_label=f"{deg} deg ({kind})", angle2_label=""),
        }

    if "parallel lines and transversals" in t_low:
        xv = rng.randint(8, 22)
        a1 = 3 * xv + 10
        while a1 >= 165:
            xv -= 2
            a1 = 3 * xv + 10
        return {
            "prompt_text": "Lines l and m are parallel and cut by transversal t. Find the value of x and the angle measure.",
            "equation_typst": f"$ \"Alternate interior angles: \" (3x + 10)^circle \" and \" {a1}^circle $",
            "answer_typst": f"$ x = {xv}, quad m angle = {a1}^circle $",
            "steps_typst": [
                "By the Alternate Interior Angles Theorem, alternate interior angles are congruent.",
                f"Set up the equation: $3x + 10 = {a1} arrow.r.double 3x = {a1 - 10}$.",
                f"Divide by $3$: $x = {xv}$.",
            ],
            "distractors": [
                f"$ x = {(180 - a1 - 10) // 3}, quad m angle = {180 - a1}^circle $",
                f"$ x = {xv + 3}, quad m angle = {a1}^circle $",
                f"$ x = {xv - 2}, quad m angle = {a1}^circle $",
            ],
            "diagram_svg": svg_parallel_transversal(mode="parallel", angle1_label="3x + 10", angle2_label=f"{a1} deg"),
            "answer_svg": svg_parallel_transversal(mode="parallel", angle1_label=f"x = {xv}", angle2_label=f"{a1} deg"),
        }

    if c_low == "properties of triangles" or c_low == "congruent triangles" or c_low == "similarity":
        if "midsegment" in t_low:
            ms = rng.randint(7, 24)
            base = 2 * ms
            return {
                "prompt_text": "DE is a midsegment of triangle ABC parallel to side AC. Find the length of side AC.",
                "equation_typst": f"$ D E = {ms} $",
                "answer_typst": f"$ A C = {base} $",
                "steps_typst": [
                    "By the Triangle Midsegment Theorem, the midsegment is half the length of the parallel third side.",
                    f"Set up $D E = 1/2 A C arrow.r.double {ms} = 1/2 A C$.",
                    f"Multiply by $2$: $A C = {base}$.",
                ],
                "distractors": [f"$ A C = {ms / 2:g} $", f"$ A C = {ms + 2} $", f"$ A C = {base + 4} $"],
                "diagram_svg": svg_general_triangle(side_c=f"Midsegment = {ms}", side_a="?", side_b=""),
                "answer_svg": svg_general_triangle(side_c=f"DE = {ms}", side_a=f"AC = {base}", side_b=""),
            }
        if "centroid" in t_low or "median" in t_low:
            gm = rng.randint(4, 15)
            ag = 2 * gm
            am = 3 * gm
            return {
                "prompt_text": "Point G is the centroid of triangle ABC on median AM. Given GM, find AG and the full median AM.",
                "equation_typst": f"$ G M = {gm} $",
                "answer_typst": f"$ A G = {ag}, quad A M = {am} $",
                "steps_typst": [
                    "By the Centroid Theorem, the centroid divides each median in a $2:1$ ratio from vertex to midpoint ($A G = 2 G M$).",
                    f"Compute $A G = 2({gm}) = {ag}$.",
                    f"Full median length: $A M = A G + G M = {ag} + {gm} = {am}$.",
                ],
                "distractors": [
                    f"$ A G = {gm}, quad A M = {2 * gm} $",
                    f"$ A G = {am}, quad A M = {4 * gm} $",
                    f"$ A G = {ag + 2}, quad A M = {am + 2} $",
                ],
                "diagram_svg": svg_general_triangle(side_c=f"GM = {gm}", side_a="AG = ?", side_b="AM = ?"),
                "answer_svg": svg_general_triangle(side_c=f"GM = {gm}", side_a=f"AG = {ag}", side_b=f"AM = {am}"),
            }
        if "triangle inequality" in t_low or "inequalities in one triangle" in t_low:
            s1 = rng.randint(5, 14)
            s2 = rng.randint(s1 + 2, s1 + 12)
            low, high = s2 - s1, s1 + s2
            return {
                "prompt_text": "Two sides of a triangle have the given measures. Find the range of possible measures for the third side x.",
                "equation_typst": f"$ {s1}, quad {s2} $",
                "answer_typst": f"$ {low} < x < {high} $",
                "steps_typst": [
                    "By the Triangle Inequality Theorem, the third side $x$ must satisfy $|a - b| < x < a + b$.",
                    f"Compute the difference: ${s2} - {s1} = {low}$.",
                    f"Compute the sum: ${s1} + {s2} = {high}$, giving ${low} < x < {high}$.",
                ],
                "distractors": [
                    f"$ {low} <= x <= {high} $",
                    f"$ 0 < x < {high} $",
                    f"$ {s1} < x < {s2} $",
                ],
                "diagram_svg": svg_general_triangle(side_a=str(s1), side_b=str(s2), side_c="x"),
                "answer_svg": svg_general_triangle(side_a=str(s1), side_b=str(s2), side_c=f"{low} < x < {high}"),
            }
        if "similar" in t_low or "proportional parts" in t_low:
            a, b = rng.randint(4, 10), rng.randint(6, 12)
            k = rng.randint(2, 4)
            ans_v = b * k
            return {
                "prompt_text": "The two polygons/triangles are similar. Set up a proportion to find the missing length x.",
                "equation_typst": f"$ triangle A B C tilde.op triangle D E F: quad ({a})/({a * k}) = ({b})/(x) $",
                "answer_typst": f"$ x = {ans_v} $",
                "steps_typst": [
                    f"Corresponding sides of similar figures are proportional: $({a})/({a * k}) = ({b})/(x)$.",
                    f"The scale factor from the first figure to the second is $k = {k}$.",
                    f"Multiply ${b} times {k} = {ans_v}$, so $x = {ans_v}$.",
                ],
                "distractors": [f"$ x = {b + k} $", f"$ x = {a * k} $", f"$ x = {ans_v + a} $"],
                "diagram_svg": svg_general_triangle(side_a=str(a), side_b=str(b), side_c=f"Scale x{k} -> x=?"),
                "answer_svg": svg_general_triangle(side_a=str(a * k), side_b=f"x = {ans_v}", side_c=f"k = {k}"),
            }
        if "congruence" in t_low or "proving triangles congruent" in t_low:
            thm = rng.choice(["SSS", "SAS", "ASA", "AAS", "HL"])
            desc = {
                "SSS": "Three pairs of corresponding sides are congruent",
                "SAS": "Two pairs of sides and the included angle are congruent",
                "ASA": "Two pairs of angles and the included side are congruent",
                "AAS": "Two pairs of angles and a non-included side are congruent",
                "HL": "The hypotenuse and a leg of two right triangles are congruent",
            }[thm]
            others = [t for t in ["SSS", "SAS", "ASA", "AAS", "SSA"] if t != thm][:3]
            return {
                "prompt_text": "State the triangle congruence theorem that proves the two triangles are congruent.",
                "equation_typst": f"\"{desc} in \" triangle A B C \" and \" triangle D E F",
                "answer_typst": f"$ \"{thm} Congruence Theorem\" $",
                "steps_typst": [
                    f"Identify the marked congruent parts: {desc.lower()}.",
                    "Match the configuration of sides (S) and angles (A) to the valid congruence postulates.",
                    f"Conclusion: {thm} Congruence Theorem.",
                ],
                "distractors": [f"$ \"{o} Congruence Theorem\" $" for o in others],
                "diagram_svg": svg_general_triangle(angle_a="A", angle_b="B", angle_c="C", side_a="cong", side_b="cong"),
                "answer_svg": svg_general_triangle(angle_a="A", angle_b="B", angle_c="C", side_c=thm),
            }
        if "isosceles and equilateral" in t_low:
            vertex_ang = rng.choice([40, 50, 64, 70, 80, 100])
            base_ang = (180 - vertex_ang) // 2
            return {
                "prompt_text": "In isosceles triangle ABC with AB = BC, find the measure of each base angle.",
                "equation_typst": f"$ m angle B = {vertex_ang}^circle, quad A B = B C $",
                "answer_typst": f"$ m angle A = m angle C = {base_ang}^circle $",
                "steps_typst": [
                    "By the Base Angles Theorem, the angles opposite congruent sides are congruent ($m angle A = m angle C = x$).",
                    f"Use the Triangle Angle-Sum Theorem: $x + x + {vertex_ang} = 180$.",
                    f"Solve $2x = {180 - vertex_ang} arrow.r.double x = {base_ang}^circle$.",
                ],
                "distractors": [
                    f"$ m angle A = {180 - vertex_ang}^circle $",
                    f"$ m angle A = {vertex_ang}^circle $",
                    f"$ m angle A = {base_ang + 10}^circle $",
                ],
                "diagram_svg": svg_general_triangle(angle_b=f"{vertex_ang} deg", angle_a="x", angle_c="x", side_c="AB=BC"),
                "answer_svg": svg_general_triangle(angle_b=f"{vertex_ang} deg", angle_a=f"{base_ang} deg", angle_c=f"{base_ang} deg"),
            }

    if c_low in ("quadrilaterals and polygons", "polygons") or "parallelogram" in t_low or "trapezoid" in t_low or "rhombus" in t_low or "kite" in t_low or "regular polygon" in t_low:
        if "trapezoid" in t_low:
            b1 = rng.randint(6, 14)
            b2 = b1 + rng.choice([4, 6, 8, 10])
            h = rng.randint(4, 10)
            area = ((b1 + b2) * h) // 2
            return {
                "prompt_text": "Find the area (and midsegment length) of the trapezoid.",
                "equation_typst": f"$ b_1 = {b1}, quad b_2 = {b2}, quad h = {h} $",
                "answer_typst": f"$ A = {area}, quad \"Midsegment\" = {(b1 + b2) // 2} $",
                "steps_typst": [
                    f"Find the average of the two bases (the midsegment): $(b_1 + b_2)/2 = ({b1} + {b2})/2 = {(b1 + b2) // 2}$.",
                    f"Multiply by the height $h = {h}$: $A = {(b1 + b2) // 2} times {h} = {area}$.",
                    f"Area = ${area}$, Midsegment = ${(b1 + b2) // 2}$.",
                ],
                "distractors": [
                    f"$ A = {(b1 + b2) * h}, quad \"Midsegment\" = {b1 + b2} $",
                    f"$ A = {b1 * h}, quad \"Midsegment\" = {b1} $",
                    f"$ A = {area + h}, quad \"Midsegment\" = {(b1 + b2) // 2} $",
                ],
                "diagram_svg": svg_polygon_diagram("trapezoid", dim1=f"b1 = {b1}", dim2=f"b2 = {b2}", dim3=f"h = {h}"),
                "answer_svg": svg_polygon_diagram("trapezoid", dim1=f"b1 = {b1}", dim2=f"A = {area}", dim3=f"h = {h}"),
            }
        if "rhombus" in t_low or "kite" in t_low:
            d1 = rng.randint(3, 9) * 2
            d2 = rng.randint(4, 10) * 2
            area = (d1 * d2) // 2
            shape_name = "rhombus" if "rhombus" in t_low else "kite"
            return {
                "prompt_text": f"Find the area of the {shape_name} given the lengths of its diagonals.",
                "equation_typst": f"$ d_1 = {d1}, quad d_2 = {d2} $",
                "answer_typst": f"$ A = {area} $",
                "steps_typst": [
                    f"The diagonals of a {shape_name} are perpendicular, so $A = 1/2 d_1 d_2$.",
                    f"Substitute $d_1 = {d1}$ and $d_2 = {d2}$: $A = 1/2({d1})({d2})$.",
                    f"Simplify: $A = {area}$.",
                ],
                "distractors": [f"$ A = {d1 * d2} $", f"$ A = {d1 + d2} $", f"$ A = {area + d1} $"],
                "diagram_svg": svg_polygon_diagram(shape_name, dim1=f"d1 = {d1}", dim2=f"d2 = {d2}"),
                "answer_svg": svg_polygon_diagram(shape_name, dim1=f"d1 = {d1}", dim2=f"A = {area}"),
            }
        if "regular polygon" in t_low or "polygon basics" in t_low or ("angles" in t_low and "quadrilateral" in c_low):
            n = rng.choice([5, 6, 8, 10, 12])
            s = rng.randint(6, 14)
            a = rng.randint(4, 10)
            if "area" in t_low:
                perim = n * s
                area = (perim * a) // 2
                return {
                    "prompt_text": "Find the perimeter and area of the regular polygon with given side length s and apothem a.",
                    "equation_typst": f"$ n = {n} \" sides\", quad s = {s}, quad a = {a} $",
                    "answer_typst": f"$ P = {perim}, quad A = {area} $",
                    "steps_typst": [
                        f"Find the perimeter: $P = n s = {n}({s}) = {perim}$.",
                        f"Use the regular polygon area formula $A = 1/2 a P$: $A = 1/2({a})({perim}) = {area}$.",
                        f"Answer: $P = {perim}, A = {area}$.",
                    ],
                    "distractors": [f"$ P = {perim}, quad A = {perim * a} $", f"$ P = {s * a}, quad A = {area} $", f"$ P = {perim}, quad A = {area + s} $"],
                    "diagram_svg": svg_polygon_diagram("regular", dim1=f"a = {a}", dim2=f"s = {s} (n={n})"),
                    "answer_svg": svg_polygon_diagram("regular", dim1=f"a = {a}", dim2=f"A = {area}"),
                }
            sum_int = (n - 2) * 180
            each_int = sum_int // n
            return {
                "prompt_text": "Find the sum of the interior angles and each interior angle of the regular polygon.",
                "equation_typst": f"$ \"Regular \" {n}\"-gon\" $",
                "answer_typst": f"$ \"Sum\" = {sum_int}^circle, quad \"Each angle\" = {each_int}^circle $",
                "steps_typst": [
                    f"Use the Polygon Interior Angles Theorem: $\"Sum\" = (n - 2) times 180^circle = ({n} - 2) times 180^circle = {sum_int}^circle$.",
                    f"Divide by $n = {n}$ for a regular polygon: ${sum_int}^circle div {n} = {each_int}^circle$.",
                    f"Sum = ${sum_int}^circle$, Each angle = ${each_int}^circle$.",
                ],
                "distractors": [
                    f"$ \"Sum\" = {n * 180}^circle, quad \"Each angle\" = 180^circle $",
                    f"$ \"Sum\" = {sum_int}^circle, quad \"Each angle\" = {360 // n}^circle $",
                    f"$ \"Sum\" = {(n - 1) * 180}^circle, quad \"Each angle\" = {each_int + 15}^circle $",
                ],
                "diagram_svg": svg_polygon_diagram("regular", dim1=f"n = {n}", dim2="Interior angles = ?"),
                "answer_svg": svg_polygon_diagram("regular", dim1=f"Sum = {sum_int}", dim2=f"Each = {each_int} deg"),
            }
        # Parallelogram / triangle area
        b = rng.randint(6, 16)
        h = rng.randint(4, 12)
        side = h + rng.randint(2, 4)
        is_tri = "triangle" in t_low
        area = (b * h) / 2 if is_tri else b * h
        return {
            "prompt_text": f"Find the area of the {'triangle' if is_tri else 'parallelogram'}.",
            "equation_typst": f"$ b = {b}, quad h = {h} $",
            "answer_typst": f"$ A = {area:g} $",
            "steps_typst": [
                f"Identify the base $b = {b}$ and perpendicular height $h = {h}$.",
                f"Use the area formula $A = {'1/2 b h' if is_tri else 'b h'}$: $A = {'1/2 ' if is_tri else ''}({b})({h}) = {area:g}$.",
                f"Answer: $A = {area:g}$.",
            ],
            "distractors": [f"$ A = {b * side} $", f"$ A = {2 * (b + side)} $", f"$ A = {(b * h) if is_tri else (b * h) / 2:g} $"],
            "diagram_svg": svg_general_triangle(side_c=f"b = {b}", side_a=f"h = {h}") if is_tri else svg_polygon_diagram("parallelogram", dim1=f"b = {b}", dim2=f"h = {h}", dim3=f"s = {side}"),
            "answer_svg": svg_general_triangle(side_c=f"b = {b}", side_a=f"A = {area:g}") if is_tri else svg_polygon_diagram("parallelogram", dim1=f"A = {area:g}", dim2=f"h = {h}", dim3=f"b = {b}"),
        }

    # ------------------------------------------------------------------
    # 13. POLYHEDRA, 3D SOLIDS, NETS, AND FRACTION SIDE LENGTHS
    # ------------------------------------------------------------------
    if c_low == "polyhedra" or "nets" in t_low or "similar solids" in t_low:
        ln, w, h = rng.randint(3, 8), rng.randint(3, 7), rng.randint(4, 9)
        sa = 2 * (ln * w + ln * h + w * h)
        vol = ln * w * h
        if "net" in t_low:
            return {
                "prompt_text": "Use the 2D net of the rectangular prism to find its total surface area.",
                "equation_typst": f"$ l = {ln}, quad w = {w}, quad h = {h} $",
                "answer_typst": f"$ \"SA\" = {sa} $",
                "steps_typst": [
                    f"The net consists of 3 pairs of congruent rectangles: $2({ln} times {w}) + 2({ln} times {h}) + 2({w} times {h})$.",
                    f"Compute the face areas: $2({ln * w} + {ln * h} + {w * h})$.",
                    f"Total Surface Area = ${sa}$.",
                ],
                "distractors": [f"$ \"SA\" = {vol} $", f"$ \"SA\" = {sa // 2} $", f"$ \"SA\" = {sa + 2 * ln} $"],
                "diagram_svg": svg_polygon_diagram("net", dim1=f"{ln}x{w}x{h}", dim2="SA = ?"),
                "answer_svg": svg_polygon_diagram("net", dim1=f"{ln}x{w}x{h}", dim2=f"SA = {sa}"),
            }
        if "similar solids" in t_low:
            k = rng.choice([2, 3, 4])
            return {
                "prompt_text": "Two solids are similar with the given scale factor. Find the ratio of their surface areas and the ratio of their volumes.",
                "equation_typst": f"$ \"Scale factor\" = 1 : {k} $",
                "answer_typst": f"$ \"SA Ratio\" = 1 : {k * k}, quad \"Volume Ratio\" = 1 : {k ** 3} $",
                "steps_typst": [
                    f"If the linear scale factor is $a:b = 1:{k}$, the surface area ratio is $a^2:b^2 = 1:{k * k}$.",
                    f"The volume ratio is $a^3:b^3 = 1:{k ** 3}$.",
                    f"SA Ratio = $1:{k * k}$, Volume Ratio = $1:{k ** 3}$.",
                ],
                "distractors": [
                    f"$ \"SA Ratio\" = 1 : {k}, quad \"Volume Ratio\" = 1 : {k * k} $",
                    f"$ \"SA Ratio\" = 1 : {2 * k}, quad \"Volume Ratio\" = 1 : {3 * k} $",
                    f"$ \"SA Ratio\" = 1 : {k ** 3}, quad \"Volume Ratio\" = 1 : {k * k} $",
                ],
                "diagram_svg": svg_solid_3d("prism", dim1="1", dim2="1", dim3=f"k = 1:{k}"),
                "answer_svg": svg_solid_3d("prism", dim1=f"SA 1:{k*k}", dim2=f"V 1:{k**3}", dim3=""),
            }
        return {
            "prompt_text": "Find the surface area and volume of the polyhedron.",
            "equation_typst": f"$ \"Rectangular Prism: \" l = {ln}, w = {w}, h = {h} $",
            "answer_typst": f"$ \"SA\" = {sa}, quad V = {vol} $",
            "steps_typst": [
                f"Surface area: $\"SA\" = 2({ln}({w}) + {ln}({h}) + {w}({h})) = {sa}$.",
                f"Volume: $V = l w h = {ln} times {w} times {h} = {vol}$.",
                f"Answer: $\"SA\" = {sa}, V = {vol}$.",
            ],
            "distractors": [f"$ \"SA\" = {vol}, quad V = {sa} $", f"$ \"SA\" = {sa // 2}, quad V = {vol} $", f"$ \"SA\" = {sa}, quad V = {ln + w + h} $"],
            "diagram_svg": svg_solid_3d("prism", dim1=str(ln), dim2=str(w), dim3=str(h)),
            "answer_svg": svg_solid_3d("prism", dim1=f"V={vol}", dim2=f"SA={sa}", dim3=""),
        }

    if c_low == "area and volume with fractions":
        f1 = Fraction(rng.choice([3, 5, 7]), rng.choice([2, 4]))
        f2 = Fraction(rng.choice([3, 5]), rng.choice([2, 3]))
        if "prism" in t_low:
            f3 = Fraction(rng.choice([2, 5]), 3)
            vol = f1 * f2 * f3
            return {
                "prompt_text": "Find the volume of the right rectangular prism with fractional edge lengths.",
                "equation_typst": f"$ l = {_fmt_frac(f1)}, quad w = {_fmt_frac(f2)}, quad h = {_fmt_frac(f3)} $",
                "answer_typst": f"$ V = {_fmt_frac(vol)} $",
                "steps_typst": [
                    "Use the volume formula $V = l times w times h$.",
                    f"Multiply the fractions: ${_fmt_frac(f1)} times {_fmt_frac(f2)} times {_fmt_frac(f3)}$.",
                    f"Simplify to lowest terms: $V = {_fmt_frac(vol)}$.",
                ],
                "distractors": [f"$ V = {_fmt_frac(f1 + f2 + f3)} $", f"$ V = {_fmt_frac(vol * 2)} $", f"$ V = {_fmt_frac(f1 * f2)} $"],
                "diagram_svg": svg_solid_3d("prism", dim1=f"{f1.numerator}/{f1.denominator}", dim2=f"{f2.numerator}/{f2.denominator}", dim3=f"{f3.numerator}/{f3.denominator}"),
                "answer_svg": svg_solid_3d("prism", dim1=f"V = {vol.numerator}/{vol.denominator}", dim2="", dim3=""),
            }
        is_tri = "triangle" in t_low
        area = (f1 * f2) / 2 if is_tri else f1 * f2
        return {
            "prompt_text": f"Find the area of the {'triangle' if is_tri else 'rectangle'} with fractional side lengths.",
            "equation_typst": f"$ b = {_fmt_frac(f1)}, quad h = {_fmt_frac(f2)} $",
            "answer_typst": f"$ A = {_fmt_frac(area)} $",
            "steps_typst": [
                f"Use the area formula $A = {'1/2 b h' if is_tri else 'b h'}$.",
                f"Multiply the fractions: ${'1/2 times ' if is_tri else ''}{_fmt_frac(f1)} times {_fmt_frac(f2)}$.",
                f"Simplify: $A = {_fmt_frac(area)}$.",
            ],
            "distractors": [f"$ A = {_fmt_frac(f1 + f2)} $", f"$ A = {_fmt_frac(area * 2)} $", f"$ A = {_fmt_frac(area / 2)} $"],
            "diagram_svg": svg_general_triangle(side_c=f"{f1}", side_a=f"{f2}") if is_tri else svg_polygon_diagram("parallelogram", dim1=f"{f1}", dim2=f"{f2}"),
            "answer_svg": svg_general_triangle(side_c=f"A = {area}", side_a="") if is_tri else svg_polygon_diagram("parallelogram", dim1=f"A = {area}", dim2=""),
        }

    # ------------------------------------------------------------------
    # 14. CIRCLES (ARCS, CHORDS, INSCRIBED ANGLES, TANGENTS, SECANTS, EQUATIONS)
    # ------------------------------------------------------------------
    if c_low == "circles":
        if "inscribed angles" in t_low:
            ins = rng.randint(24, 72)
            arc = 2 * ins
            return {
                "prompt_text": "Find the measure of the intercepted arc (or inscribed angle) in the circle.",
                "equation_typst": f"$ \"Inscribed angle\" = {ins}^circle $",
                "answer_typst": f"$ \"Intercepted arc\" = {arc}^circle $",
                "steps_typst": [
                    "By the Inscribed Angle Theorem, the measure of an inscribed angle is half the measure of its intercepted arc.",
                    f"Multiply the inscribed angle by $2$: $2 times {ins}^circle = {arc}^circle$.",
                    f"Intercepted arc = ${arc}^circle$.",
                ],
                "distractors": [f"$ \"Intercepted arc\" = {ins // 2}^circle $", f"$ \"Intercepted arc\" = {ins}^circle $", f"$ \"Intercepted arc\" = {180 - ins}^circle $"],
                "diagram_svg": svg_circle_diagram(angle_label=f"Inscribed = {ins} deg"),
                "answer_svg": svg_circle_diagram(angle_label=f"Arc = {arc} deg"),
            }
        if "tangent" in t_low or "secant" in t_low:
            arc_big = rng.randint(110, 170)
            arc_small = rng.randrange(30, 80, 2)
            if (arc_big - arc_small) % 2 != 0:
                arc_big += 1
            ext_ang = (arc_big - arc_small) // 2
            return {
                "prompt_text": "Find the measure of the exterior angle formed by the secant/tangent lines intersecting outside the circle.",
                "equation_typst": f"$ \"Far arc\" = {arc_big}^circle, quad \"Near arc\" = {arc_small}^circle $",
                "answer_typst": f"$ m angle = {ext_ang}^circle $",
                "steps_typst": [
                    "The angle formed outside a circle by two secants/tangents equals half the difference of the intercepted arcs.",
                    f"Compute $1/2({arc_big}^circle - {arc_small}^circle) = 1/2({arc_big - arc_small}^circle)$.",
                    f"Simplify: $m angle = {ext_ang}^circle$.",
                ],
                "distractors": [f"$ m angle = {(arc_big + arc_small) // 2}^circle $", f"$ m angle = {arc_big - arc_small}^circle $", f"$ m angle = {ext_ang + 10}^circle $"],
                "diagram_svg": svg_circle_diagram(angle_label=f"Arcs: {arc_big}, {arc_small}"),
                "answer_svg": svg_circle_diagram(angle_label=f"Angle = {ext_ang} deg"),
            }
        if "segment measures" in t_low or "chords" in t_low:
            a, b = rng.choice([(4, 9), (6, 8), (3, 12), (6, 10), (8, 9)])
            prod = a * b
            c = rng.choice([x for x in range(2, 15) if prod % x == 0 and x != a])
            d = prod // c
            return {
                "prompt_text": "Two chords intersect inside the circle. Find the missing segment length x.",
                "equation_typst": f"$ {a} dot {b} = {c} dot x $",
                "answer_typst": f"$ x = {d} $",
                "steps_typst": [
                    "By the Intersecting Chords (Segments of Chords) Theorem, the products of the chord segments are equal.",
                    f"Set up ${a} times {b} = {c} x arrow.r.double {prod} = {c} x$.",
                    f"Divide by ${c}$: $x = {d}$.",
                ],
                "distractors": [f"$ x = {a + b - c} $", f"$ x = {prod} $", f"$ x = {d + 2} $"],
                "diagram_svg": svg_circle_diagram(chord_label=f"{a} * {b} = {c} * x"),
                "answer_svg": svg_circle_diagram(chord_label=f"x = {d}"),
            }
        if "equations of circles" in t_low:
            h, k = rng.randint(-4, 4), rng.randint(-4, 4)
            r = rng.randint(2, 5)
            hx = f"(x - {h})^2" if h > 0 else (f"(x + {abs(h)})^2" if h < 0 else "x^2")
            ky = f"(y - {k})^2" if k > 0 else (f"(y + {abs(k)})^2" if k < 0 else "y^2")
            return {
                "prompt_text": "Write the standard equation of the circle and sketch its graph on the coordinate plane.",
                "equation_typst": f"$ \"Center\": ({h}, {k}), quad \"Radius\": r = {r} $",
                "answer_typst": f"$ {hx} + {ky} = {r * r} $",
                "steps_typst": [
                    "Use standard circle form: $(x - h)^2 + (y - k)^2 = r^2$.",
                    f"Substitute $(h, k) = ({h}, {k})$ and $r^2 = {r}^2 = {r * r}$.",
                    f"Equation: ${hx} + {ky} = {r * r}$.",
                ],
                "distractors": [
                    f"$ {hx} + {ky} = {r} $",
                    f"$ (x + {h})^2 + (y + {k})^2 = {r * r} $",
                    f"$ {hx} - {ky} = {r * r} $",
                ],
                "diagram_svg": svg_coordinate_plane(),
                "answer_svg": svg_coordinate_plane(circles=[{"h": h, "k": k, "r": r, "color": "#2563eb"}], points=[(h, k, f"C({h},{k})", True)]),
            }

    # ------------------------------------------------------------------
    # 15. DATA SETS, DOT PLOTS, HISTOGRAMS, BOX PLOTS, SCATTER PLOTS
    # ------------------------------------------------------------------
    if c_low in ("data sets and distributions", "statistics"):
        if "dot plot" in t_low or "visualizing data" in t_low:
            base = rng.randint(2, 6)
            counts = {base: 2, base + 1: 4, base + 2: 3, base + 3: 1, base + 4: 2}
            total_n = sum(counts.values())
            mode_v = base + 1
            return {
                "prompt_text": "Use the dot plot to find the total number of observations and the mode of the distribution.",
                "equation_typst": f"\"Dot plot over values \" {base} \" to \" {base + 4}",
                "answer_typst": f"$ n = {total_n}, quad \"Mode\" = {mode_v} $",
                "steps_typst": [
                    f"Count all dots above the number line: $2 + 4 + 3 + 1 + 2 = {total_n}$ observations.",
                    f"Find the value with the tallest stack of dots ($4$ dots at ${mode_v}$).",
                    f"Total $n = {total_n}$, Mode = ${mode_v}$.",
                ],
                "distractors": [
                    f"$ n = {total_n + 2}, quad \"Mode\" = {base + 2} $",
                    "$ n = 5, quad \"Mode\" = 4 $",
                    f"$ n = {total_n}, quad \"Mode\" = {base} $",
                ],
                "diagram_svg": svg_dot_plot(counts),
                "answer_svg": svg_dot_plot(counts, title=f"n = {total_n}, Mode = {mode_v}"),
            }
        if "histogram" in t_low:
            f1, f2, f3, f4 = rng.randint(2, 5), rng.randint(6, 9), rng.randint(4, 7), rng.randint(1, 4)
            bins = [("0-9", f1), ("10-19", f2), ("20-29", f3), ("30-39", f4)]
            tot = f1 + f2 + f3 + f4
            return {
                "prompt_text": "Use the histogram to determine the total frequency and the modal interval.",
                "equation_typst": "\"Analyze the frequency distribution in the histogram below\"",
                "answer_typst": f"$ \"Total\" = {tot}, quad \"Modal interval\" = 10\"-\"19 $",
                "steps_typst": [
                    f"Add the bar heights: ${f1} + {f2} + {f3} + {f4} = {tot}$.",
                    f"The tallest bar is over interval $10\"-\"19$ with frequency ${f2}$.",
                    f"Total = ${tot}$, Modal interval = $10\"-\"19$.",
                ],
                "distractors": [
                    f"$ \"Total\" = {tot}, quad \"Modal interval\" = 20\"-\"29 $",
                    f"$ \"Total\" = {f2}, quad \"Modal interval\" = 10\"-\"19 $",
                    f"$ \"Total\" = {tot + 4}, quad \"Modal interval\" = 0\"-\"9 $",
                ],
                "diagram_svg": svg_histogram(bins),
                "answer_svg": svg_histogram(bins, title=f"Total = {tot}, Peak = 10-19"),
            }
        if "box plot" in t_low:
            mn = rng.randint(10, 20)
            q1 = mn + rng.randint(5, 10)
            med = q1 + rng.randint(6, 12)
            q3 = med + rng.randint(6, 12)
            mx = q3 + rng.randint(5, 10)
            iqr = q3 - q1
            rng_v = mx - mn
            return {
                "prompt_text": "Read the five-number summary from the box-and-whisker plot and compute the median and interquartile range (IQR).",
                "equation_typst": "\"Read the five-number summary from the box-and-whisker plot below\"",
                "answer_typst": f"$ \"Median\" = {med}, quad \"IQR\" = {iqr}, quad \"Range\" = {rng_v} $",
                "steps_typst": [
                    f"The vertical line inside the box marks the median: ${med}$.",
                    f"The box spans from $Q_1 = {q1}$ to $Q_3 = {q3}$, so $\"IQR\" = Q_3 - Q_1 = {q3} - {q1} = {iqr}$.",
                    f"The overall range is $\"Max\" - \"Min\" = {mx} - {mn} = {rng_v}$.",
                ],
                "distractors": [
                    f"$ \"Median\" = {q1}, quad \"IQR\" = {rng_v}, quad \"Range\" = {iqr} $",
                    f"$ \"Median\" = {med}, quad \"IQR\" = {q3 - med}, quad \"Range\" = {rng_v} $",
                    f"$ \"Median\" = {q3}, quad \"IQR\" = {iqr}, quad \"Range\" = {mx} $",
                ],
                "diagram_svg": svg_box_plot(mn, q1, med, q3, mx),
                "answer_svg": svg_box_plot(mn, q1, med, q3, mx, title=f"Median = {med}, IQR = {iqr}"),
            }
        if "scatter plot" in t_low or "statistical model" in t_low:
            m = rng.choice([2, -2, 1, -1])
            b = rng.randint(-2, 3)
            pts = [(x, m * x + b + (1 if x % 2 == 0 else -1), "", True) for x in range(-4, 5, 2)]
            corr = "Positive correlation" if m > 0 else "Negative correlation"
            x_pred = 6
            y_pred = m * x_pred + b
            return {
                "prompt_text": "Identify the correlation in the scatter plot and use the line of best fit to predict y when x = 6.",
                "equation_typst": f"\"Line of best fit: \" y = {m}x {'+ ' + str(b) if b >= 0 else '- ' + str(abs(b))}",
                "answer_typst": f"$ \"{corr}\", quad y(6) = {y_pred} $",
                "steps_typst": [
                    f"The slope $m = {m}$ is {'positive' if m > 0 else 'negative'}, indicating a {corr.lower()}.",
                    f"Substitute $x = 6$ into the line of best fit: $y = {m}(6) + ({b}) = {y_pred}$.",
                    f"Answer: {corr}, $y(6) = {y_pred}$.",
                ],
                "distractors": [
                    f"$ \"{'Negative' if m > 0 else 'Positive'} correlation\", quad y(6) = {y_pred} $",
                    f"$ \"{corr}\", quad y(6) = {m * 6 - b} $",
                    f"$ \"No correlation\", quad y(6) = {b} $",
                ],
                "diagram_svg": svg_coordinate_plane(points=pts),
                "answer_svg": svg_coordinate_plane(lines=[{"m": m, "b": b, "color": "#dc2626"}], points=pts),
            }

    return None
