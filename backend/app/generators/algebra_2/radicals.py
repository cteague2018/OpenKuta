from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Algebra2RadicalsGenerator(BaseGenerator):
    generator_id = "algebra_2.radicals"
    name = "Radicals & Rational Exponents"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSN.RN.A.2"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        # Simplify sqrt(k^2 * p) = k sqrt(p)
        k = rng.choice([2, 3, 4, 5, 6])
        p = rng.choice([2, 3, 5, 7])
        num = (k * k) * p

        eq_typst = f"sqrt({num})"
        ans_typst = f"{k} sqrt({p})"

        steps = [
            f"Find the largest perfect square factor of {num}: $ {k*k} dot {p} = {num} $",
            f"Rewrite using product property of square roots: $ sqrt({k*k}) dot sqrt({p}) $",
            f"Evaluate the square root of the perfect square: $ sqrt({k*k}) = {k} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"a2_rad_{problem_idx}",
            prompt_text="Simplify each radical expression completely.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"{k*k} sqrt({p})", f"{p} sqrt({k})", f"{k + p}"],
            difficulty=difficulty,
            standards=self.standards
        )
