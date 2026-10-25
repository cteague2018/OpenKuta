from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class CalculusRiemannSumsGenerator(BaseGenerator):
    generator_id = "calculus.riemann_sums"
    name = "Riemann Sums & Definite Integrals (LRAM, RRAM, MRAM, Trapezoid)"
    category = "Calculus"
    standards = ["AP.CALC.LIM-2.A", "AP.CALC.LIM-2.B", "AP.CALC.FUN-6.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        # Subintervals n
        n = 4
        a = 0
        b = rng.choice([4, 8])
        dx = (b - a) // n

        # Function f(x) = k * x^2 or f(x) = x^2 + c
        k = rng.choice([1, 2])
        c = rng.choice([1, 2, 3])

        def f(val: float) -> float:
            return k * (val ** 2) + c

        # Grid points x_0, x_1, x_2, x_3, x_4
        grid = [a + i * dx for i in range(n + 1)]
        f_vals = [f(x) for x in grid]

        func_str = f"{k} x^2 + {c}" if k > 1 else f"x^2 + {c}"

        if difficulty == ProblemDifficulty.MILD:
            # Left Riemann Sum (LRAM)
            sample_pts = grid[:-1]
            sample_vals = [f(x) for x in sample_pts]
            total_sum = dx * sum(sample_vals)

            eq_typst = f"\"Function \" f(x) = {func_str}, quad \"Interval: \" [{a}, {b}], quad n = {n} \" subintervals\""
            ans_typst = f"\"LRAM\" = {int(total_sum)}"

            terms_str = " + ".join(f"f({x})" for x in sample_pts)
            num_terms = " + ".join(str(int(v)) for v in sample_vals)

            steps = [
                f"Calculate subinterval width: $ Delta x = (b - a) / n = ({b} - {a}) / {n} = {dx} $",
                f"Grid points: $ {grid} $",
                f"Evaluate at left endpoints {sample_pts}: $ {terms_str} $",
                f"Function values: $ {num_terms} $",
                f"Compute sum: $ Delta x dot ({num_terms}) = {dx} dot ({int(sum(sample_vals))}) = {int(total_sum)} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [f"LRAM = {int(total_sum + 2 * dx)}", f"LRAM = {int(total_sum - 2 * dx)}"]

            return BaseProblem(
                id=f"calc_riemann_mild_{problem_idx}",
                prompt_text="Approximate the area under the curve using a Left Riemann Sum.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Right Riemann Sum (RRAM)
            sample_pts = grid[1:]
            sample_vals = [f(x) for x in sample_pts]
            total_sum = dx * sum(sample_vals)

            eq_typst = f"\"Function \" f(x) = {func_str}, quad \"Interval: \" [{a}, {b}], quad n = {n} \" subintervals\""
            ans_typst = f"\"RRAM\" = {int(total_sum)}"

            terms_str = " + ".join(f"f({x})" for x in sample_pts)
            num_terms = " + ".join(str(int(v)) for v in sample_vals)

            steps = [
                f"Calculate subinterval width: $ Delta x = (b - a) / n = ({b} - {a}) / {n} = {dx} $",
                f"Grid points: $ {grid} $",
                f"Evaluate at right endpoints {sample_pts}: $ {terms_str} $",
                f"Function values: $ {num_terms} $",
                f"Compute sum: $ Delta x dot ({num_terms}) = {dx} dot ({int(sum(sample_vals))}) = {int(total_sum)} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [f"RRAM = {int(total_sum + 4)}", f"RRAM = {int(total_sum - 8)}"]

            return BaseProblem(
                id=f"calc_riemann_med_{problem_idx}",
                prompt_text="Approximate the area under the curve using a Right Riemann Sum.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # Trapezoidal Rule (TRAM): (dx / 2) * [f(x0) + 2f(x1) + 2f(x2) + 2f(x3) + f(x4)]
            trap_sum = (dx / 2.0) * (f_vals[0] + 2 * sum(f_vals[1:-1]) + f_vals[-1])
            ans_val = int(trap_sum) if trap_sum.is_integer() else trap_sum

            eq_typst = f"\"Function \" f(x) = {func_str}, quad \"Interval: \" [{a}, {b}], quad n = {n} \" subintervals\""
            ans_typst = f"\"Trapezoid Rule\" = {ans_val}"

            inner_str = f"f({grid[0]}) + 2f({grid[1]}) + 2f({grid[2]}) + 2f({grid[3]}) + f({grid[4]})"
            inner_nums = f"{int(f_vals[0])} + 2({int(f_vals[1])}) + 2({int(f_vals[2])}) + 2({int(f_vals[3])}) + {int(f_vals[4])}"

            steps = [
                "Recall Trapezoidal Rule: $ T = (Delta x) / 2 [f(x_0) + 2 f(x_1) + 2 f(x_2) + ... + f(x_n)] $",
                f"Compute $ (Delta x)/2 = {dx} / 2 = {dx/2} $",
                f"Substitute endpoints: $ {dx/2} dot [{inner_str}] $",
                f"Evaluate terms: $ {dx/2} dot [{inner_nums}] $",
                f"Calculate total: $ {ans_typst} $"
            ]

            distractors = [f"Trapezoid Rule = {int(ans_val + 3)}", f"Trapezoid Rule = {int(ans_val - 3)}"]

            return BaseProblem(
                id=f"calc_riemann_spicy_{problem_idx}",
                prompt_text="Approximate the definite integral using the Trapezoidal Rule.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )

