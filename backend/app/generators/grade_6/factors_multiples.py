from __future__ import annotations

import math
import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6FactorsMultiplesGenerator(BaseGenerator):
    generator_id = "grade_6.factors_multiples"
    name = "Greatest Common Factor & Least Common Multiple"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.NS.B.4"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        is_gcf = rng.choice([True, False])
        n1 = rng.choice([12, 18, 24, 30, 36, 42, 48])
        n2 = rng.choice([16, 20, 28, 32, 40, 54, 60])

        if is_gcf:
            ans = math.gcd(n1, n2)
            eq_typst = f"\"GCF of \" {n1} \" and \" {n2}"
            ans_typst = f"{ans}"
            steps = [
                f"List prime factors of {n1} and {n2}.",
                f"Identify all common prime factors.",
                f"Multiply common prime factors: $ {ans} $",
                f"Result: $ {ans_typst} $"
            ]
            prompt = "Find the greatest common factor (GCF) of each pair of numbers."
        else:
            ans = (n1 * n2) // math.gcd(n1, n2)
            eq_typst = f"\"LCM of \" {n1} \" and \" {n2}"
            ans_typst = f"{ans}"
            steps = [
                f"Find the greatest common factor: $ gcd({n1}, {n2}) = {math.gcd(n1, n2)} $",
                f"Calculate LCM using formula: $ \"LCM\"(a, b) = (a dot b) / (\"GCF\"(a, b)) $",
                f"Compute: $ ({n1} dot {n2}) / ({math.gcd(n1, n2)}) = {ans} $",
                f"Result: $ {ans_typst} $"
            ]
            prompt = "Find the least common multiple (LCM) of each pair of numbers."

        return BaseProblem(
            id=f"g6_fac_{problem_idx}",
            prompt_text=prompt,
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"{ans + 2}", f"{ans * 2}" if is_gcf else f"{ans // 2}"],
            difficulty=difficulty,
            standards=self.standards
        )
