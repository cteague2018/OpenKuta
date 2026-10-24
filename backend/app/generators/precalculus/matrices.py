from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class PrecalcMatricesGenerator(BaseGenerator):
    generator_id = "precalculus.matrices"
    name = "Matrices (Operations, Determinants, Inverses)"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSN.VM.C.8", "CCSS.MATH.CONTENT.HSN.VM.C.10"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        a = rng.choice([2, 3, 4, 5, -2, -3])
        b = rng.choice([1, 2, 3, 4, -1, -2])
        c = rng.choice([1, 3, 4, 2, -3, -4])
        d = rng.choice([2, 3, 5, -2, -3])

        det = a * d - b * c
        eq_typst = f"mat({a}, {b}; {c}, {d})"
        ans_typst = f"{det}"

        steps = [
            f"Recall 2x2 determinant formula: $ det mat(a, b; c, d) = a d - b c $",
            f"Identify entries: $ a = {a}, b = {b}, c = {c}, d = {d} $",
            f"Compute main diagonal product: $ ({a}) dot ({d}) = {a*d} $",
            f"Compute off-diagonal product: $ ({b}) dot ({c}) = {b*c} $",
            f"Subtract: $ ({a*d}) - ({b*c}) = {ans_typst} $"
        ]

        return BaseProblem(
            id=f"pcalc_mat_{problem_idx}",
            prompt_text="Evaluate the determinant of each 2x2 matrix.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"{a*d + b*c}", f"{det - 4}", f"{b*c - a*d}"],
            difficulty=difficulty,
            standards=self.standards
        )
