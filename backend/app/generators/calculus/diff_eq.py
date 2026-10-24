from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class CalculusDiffEqGenerator(BaseGenerator):
    generator_id = "calculus.diff_eq"
    name = "Differential Equations (Separable & Growth)"
    category = "Calculus"
    standards = ["AP.CALC.FUN-7.D", "AP.CALC.FUN-7.E"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        k = rng.choice([2, 3, 4, 5])
        c = rng.choice([1, 2, 3, 5])

        if difficulty == ProblemDifficulty.MILD:
            # dy/dx = k y
            eq_typst = f"(d y)/(d x) = {k} y"
            ans_typst = f"y = C e^({k} x)"

            steps = [
                f"Separate variables: $ (1/y) dif y = {k} dif x $",
                f"Integrate both sides: $ integral (1/y) dif y = integral {k} dif x $",
                f"Evaluate integrals: $ ln|y| = {k} x + C_1 $",
                f"Exponentiate both sides: $ |y| = e^({k} x + C_1) = e^(C_1) dot e^({k} x) $",
                f"General solution: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_de_mild_{problem_idx}",
                prompt_text="Find the general solution of each differential equation.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"y = {k} x + C", f"y = C e^(-{k} x)"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        else:
            # dy/dx = x / y
            eq_typst = "(d y)/(d x) = x / y"
            ans_typst = "y^2 - x^2 = C"

            steps = [
                f"Separate variables: multiply by y and dif x: $ y dif y = x dif x $",
                f"Integrate both sides: $ integral y dif y = integral x dif x $",
                f"Evaluate integrals: $ (y^2)/2 = (x^2)/2 + C_1 $",
                f"Multiply by 2 and rearrange: $ y^2 - x^2 = 2 C_1 = C $",
                f"Implicit general solution: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_de_med_{problem_idx}",
                prompt_text="Find the general solution of each differential equation.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=["y = x + C", "y^2 + x^2 = C"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
