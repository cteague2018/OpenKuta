from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_coordinate_plane_pair


class ExponentialFunctionsGenerator(BaseGenerator):
    generator_id = "algebra_1.exponential_functions"
    name = "Exponential Functions & Growth"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSF.LE.A.1", "CCSS.MATH.CONTENT.HSF.LE.A.2"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Evaluating y = a * b^x at x = k
            a = rng.choice([2, 3, 4, 5])
            b = rng.choice([2, 3])
            x_val = rng.randint(1, 4)
            y_val = a * (b ** x_val)

            eq_str = f"y = {a} * {b}^x"
            q_text = f"Evaluate $ {eq_str} $ for $ x = {x_val} $."
            ans_str = f"y = {y_val}"
            distractors = [
                f"y = {(a * b) ** x_val}",  # Multiplied base by a before exponent
                f"y = {a * b * x_val}",
                f"y = {y_val + 4}",
            ]
            steps = [
                f"Substitute $ x = {x_val} $: $ y = {a} * {b}^{x_val} $.",
                f"Evaluate the exponent first: $ {b}^{x_val} = {b ** x_val} $.",
                f"Multiply by coefficient $ {a} $: $ y = {a} * {b ** x_val} = {y_val} $."
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Identifying initial value and growth/decay factor
            a = rng.randint(10, 50) * 10
            is_growth = rng.choice([True, False])
            if is_growth:
                rate_pct = rng.choice([5, 8, 12, 15])
                b_val = round(1 + rate_pct / 100, 2)
                nature = "Exponential Growth"
            else:
                rate_pct = rng.choice([5, 10, 15, 20])
                b_val = round(1 - rate_pct / 100, 2)
                nature = "Exponential Decay"

            eq_str = f"f(t) = {a}({b_val})^t"
            q_text = f"Determine whether $ {eq_str} $ represents exponential growth or decay, and identify the initial amount."
            ans_str = f"{nature}, Initial: {a}"
            wrong_nature = "Exponential Decay" if is_growth else "Exponential Growth"
            distractors = [
                f"{wrong_nature}, Initial: {a}",
                f"{nature}, Initial: {b_val}",
                f"{wrong_nature}, Initial: {b_val}",
            ]
            steps = [
                f"In $ f(t) = a * b^t $, the initial amount is $ a = {a} $.",
                f"Since the base $ b = {b_val} {' > 1' if is_growth else ' < 1'} $, this represents {nature}."
            ]

        else:  # SPICY
            # Word problem: population or depreciation
            init_pop = rng.choice([500, 1200, 2500, 5000])
            growth_pct = rng.choice([4, 6, 8, 10])
            years = rng.randint(2, 4)
            # A = P (1 + r)^t
            final_val = round(init_pop * ((1 + growth_pct / 100) ** years))

            q_text = (
                f"A town with an initial population of {init_pop:,} is growing at a continuous annual rate of {growth_pct}%. "
                f"What is the estimated population after {years} years? (Round to nearest whole number)"
            )
            ans_str = f"{final_val:,} people"
            distractors = [
                f"{init_pop + init_pop * growth_pct * years // 100:,} people",  # Linear interest mistake
                f"{final_val + 250:,} people",
                f"{final_val - 180:,} people",
            ]
            steps = [
                "Use exponential growth model: $ A = P(1 + r)^t $.",
                f"Substitute $ P = {init_pop} $, $ r = {growth_pct / 100} $, $ t = {years} $.",
                f"Calculate: $ {init_pop} * (1 + {growth_pct / 100})^{years} approx {final_val:,} $ people."
            ]

        return BaseProblem(
            id=f"exp_func_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each exponential function problem.",
            equation_typst=q_text,
            answer_typst=ans_str,
            steps_typst=steps,
            distractors=distractors,
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": q_text}
        )


class GraphingExponentialGenerator(BaseGenerator):
    generator_id = "algebra_1.graphing_exponential"
    name = "Graphing Exponential Functions"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSF.IF.C.7.E", "TEKS.MATH.A1.9.D"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            base, base_s = rng.choice([(2.0, "2"), (3.0, "3"), (4.0, "4"), (0.5, "(1/2)")])
            c = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            a = rng.choice([1, -1])
        elif difficulty == ProblemDifficulty.MEDIUM:
            base, base_s = rng.choice([(2.0, "2"), (3.0, "3"), (4.0, "4"), (5.0, "5"), (0.5, "(1/2)"), (1/3, "(1/3)"), (0.25, "(1/4)")])
            c = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            a = rng.choice([-3, -2, -1, 2, 3])
        else:
            base, base_s = rng.choice([(2.0, "2"), (3.0, "3"), (4.0, "4"), (5.0, "5"), (0.5, "(1/2)"), (1/3, "(1/3)"), (0.25, "(1/4)")])
            c = rng.choice([-7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7])
            a = rng.choice([-4, -3, -2, 2, 3, 4])
        a_s = "" if a == 1 else ("-" if a == -1 else f"{a} dot ")
        c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
        eq = f"y = {a_s}{base_s}^x {c_s}".strip()

        is_growth = (base > 1 and a > 0) or (base < 1 and a < 0)
        asymptote = f"y = {c}"
        y_int = a + c
        steps = [
            f"Given exponential function: $ {eq} $",
            f"Horizontal asymptote: $ {asymptote} $",
            f"y-intercept (when $ x = 0 $): $ (0, {y_int}) $",
            f"This represents exponential {'growth' if is_growth else 'decay'}.",
            f"Plot points and draw a smooth curve approaching asymptote $ {asymptote} $."
        ]

        ans = f"Asymptote: {asymptote}; y-int: (0, {y_int})"
        d1 = f"Asymptote: y = {c + 1}; y-int: (0, {y_int})"
        d2 = f"Asymptote: x = {c}; y-int: ({y_int}, 0)"
        d3 = f"Asymptote: {asymptote}; y-int: (0, {y_int - 1})"

        diagram_svg, ans_svg = svg_coordinate_plane_pair(
            functions=[{"fn": lambda xv, _a=a, _b=base, _c=c: _a * (_b ** xv) + _c, "color": "#dc2626"}],
            asymptotes=[{"y": float(c), "color": "#64748b"}],
            points=[{"x": 0, "y": y_int, "color": "#2563eb", "label": f"(0,{y_int})"}],
            show_numbers=False,
        )

        return BaseProblem(
            id=f"graph_exp_{difficulty.value}_{problem_idx}",
            prompt_text="Sketch the graph of each exponential function. State the horizontal asymptote and y-intercept.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            diagram_svg=diagram_svg,
            answer_svg=ans_svg,
            metadata={"asymptote": asymptote, "y_intercept": y_int}
        )
