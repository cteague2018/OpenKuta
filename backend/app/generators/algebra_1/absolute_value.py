from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_coordinate_plane_pair
from backend.app.generators.verification_gate import verify_mathematical_truth


class AbsoluteValueEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.absolute_value"
    name = "Absolute Value Equations"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.3", "CCSS.MATH.CONTENT.HSA.CED.A.1"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        var = "x"

        if difficulty == ProblemDifficulty.MILD:
            # |x + b| = c or |x - b| = c
            b = rng.randint(1, 9)
            sign = rng.choice(["+", "-"])
            c = rng.randint(3, 15)
            if sign == "+":
                eq_str = f"|{var} + {b}| = {c}"
                ans1 = c - b
                ans2 = -c - b
                step_pos = f"{var} + {b} = {c} ==> {var} = {ans1}"
                step_neg = f"{var} + {b} = -{c} ==> {var} = {ans2}"
            else:
                eq_str = f"|{var} - {b}| = {c}"
                ans1 = c + b
                ans2 = -c + b
                step_pos = f"{var} - {b} = {c} ==> {var} = {ans1}"
                step_neg = f"{var} - {b} = -{c} ==> {var} = {ans2}"

            roots = sorted([ans1, ans2])
            ans_str = f"{var} = {roots[0]}, {roots[1]}"
            distractors = [
                f"{var} = {roots[1]}",
                f"{var} = {-roots[0]}, {-roots[1]}",
                f"{var} = {roots[0] + 2}, {roots[1] - 2}",
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # |a x + b| = c
            a = rng.choice([2, 3, 4, 5])
            r1 = rng.randint(-6, 6)
            b = rng.randint(1, 9)
            c = abs(a * r1 + b)
            if c == 0:
                c = a * 2 + b

            r_pos = (c - b) // a if (c - b) % a == 0 else f"{(c - b)}/{a}"
            r_neg = (-c - b) // a if (-c - b) % a == 0 else f"{(-c - b)}/{a}"

            eq_str = f"|{a}{var} + {b}| = {c}"
            ans_str = f"{var} = {r_pos}, {r_neg}"
            step_pos = f"{a}{var} + {b} = {c} ==> {a}{var} = {c - b} ==> {var} = {r_pos}"
            step_neg = f"{a}{var} + {b} = -{c} ==> {a}{var} = {-c - b} ==> {var} = {r_neg}"
            distractors = [
                f"{var} = {r_pos}",
                f"{var} = {-r1 if isinstance(r1, int) else 2}",
                f"{var} = {c}, {-c}",
            ]

        else:  # SPICY
            # Multi-step: d * |a x + b| - k = c
            d = rng.choice([2, 3])
            k = rng.randint(2, 8)
            inner_val = rng.randint(3, 9)
            target = d * inner_val - k
            b = rng.randint(1, 6)
            a = rng.choice([2, 3])

            c = inner_val
            r_pos = (c - b) // a if (c - b) % a == 0 else f"{(c - b)}/{a}"
            r_neg = (-c - b) // a if (-c - b) % a == 0 else f"{(-c - b)}/{a}"

            eq_str = f"{d}|{a}{var} + {b}| - {k} = {target}"
            ans_str = f"{var} = {r_pos}, {r_neg}"
            step_pos = f"Isolate absolute value: |{a}{var} + {b}| = ({target} + {k}) / {d} = {inner_val}"
            step_neg = f"Case 1: {a}{var} + {b} = {inner_val} ==> {var} = {r_pos}; Case 2: {a}{var} + {b} = -{inner_val} ==> {var} = {r_neg}"
            distractors = [
                f"{var} = {r_pos}",
                f"{var} = {inner_val}, {-inner_val}",
                f"{var} = {target // d}",
            ]

        if difficulty == ProblemDifficulty.SPICY:
            steps = [
                f"Given equation: $ {eq_str} $",
                f"Isolate absolute value expression: $ |{a}{var} + {b}| = ({target} + {k}) / {d} = {inner_val} $",
                f"Set up Case 1 (positive): $ {a}{var} + {b} = {inner_val} arrow.r.double {a}{var} = {inner_val - b} arrow.r.double {var} = {r_pos} $",
                f"Set up Case 2 (negative): $ {a}{var} + {b} = -{inner_val} arrow.r.double {a}{var} = {-inner_val - b} arrow.r.double {var} = {r_neg} $",
                f"Solution set: $ {ans_str} $"
            ]
        else:
            steps = [
                f"Given equation: $ {eq_str} $",
                f"Case 1 (positive): $ {step_pos} $",
                f"Case 2 (negative): $ {step_neg} $",
                f"Solution set: $ {ans_str} $"
            ]

        return BaseProblem(
            id=f"abs_val_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each absolute value equation.",
            equation_typst=f"$ {eq_str} $",
            answer_typst=f"$ {ans_str} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": eq_str}
        )


class GraphingAbsoluteValueGenerator(BaseGenerator):
    generator_id = "algebra_1.graphing_absolute_value"
    name = "Graphing Absolute Value Equations"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSF.IF.C.7.B", "TEKS.MATH.A1.6.C"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            h = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            k = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            a = 1
        elif difficulty == ProblemDifficulty.MEDIUM:
            h = rng.randint(-4, 4)
            k = rng.randint(-4, 4)
            a = rng.choice([-2, -1, 2, 3])
        else:
            h = rng.choice([-5, -4, -3, 3, 4, 5])
            k = rng.choice([-5, -4, -3, 3, 4, 5])
            a = rng.choice([-3, -2, 2, 3])

        h_s = f"- {h}" if h > 0 else (f"+ {abs(h)}" if h < 0 else "")
        k_s = f"+ {k}" if k > 0 else (f"- {abs(k)}" if k < 0 else "")
        a_s = "" if a == 1 else ("-" if a == -1 else str(a))
        inner = f"x {h_s}".strip() if h != 0 else "x"
        eq = f"y = {a_s}|{inner}| {k_s}".strip()

        steps = [
            f"Given absolute value equation: $ {eq} $",
            f"Identify vertex $ (h, k) $: $ ({h}, {k}) $",
            f"The V-shape opens {'upward' if a > 0 else 'downward'} with branch slope $ plus.minus {abs(a)} $.",
            f"Plot vertex $ ({h}, {k}) $ and symmetric points $ ({h + 1}, {k + a}) $ and $ ({h - 1}, {k + a}) $.",
            "Draw the two straight rays forming the V-graph."
        ]

        ans = f"Vertex: ({h}, {k})"
        d1 = f"Vertex: ({-h}, {k})"
        d2 = f"Vertex: ({k}, {h})"
        d3 = f"Vertex: ({h}, {-k})"

        diagram_svg, ans_svg = svg_coordinate_plane_pair(
            functions=[{"fn": lambda xv, _a=a, _h=h, _k=k: _a * abs(xv - _h) + _k, "color": "#dc2626"}],
            points=[{"x": h, "y": k, "color": "#2563eb", "label": f"({h},{k})"}],
            show_numbers=False,
        )

        return BaseProblem(
            id=f"graph_abs_{difficulty.value}_{problem_idx}",
            prompt_text="Sketch the graph of each absolute value equation. Identify the vertex.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            diagram_svg=diagram_svg,
            answer_svg=ans_svg,
            metadata={"vertex": (h, k)}
        )
