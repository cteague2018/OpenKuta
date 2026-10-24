from __future__ import annotations

import math
import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6FractionsDecimalsGenerator(BaseGenerator):
    generator_id = "grade_6.fractions_decimals"
    name = "Dividing Fractions & Decimal Arithmetic"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.NS.A.1", "CCSS.MATH.CONTENT.6.NS.B.3"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        if difficulty == ProblemDifficulty.MILD:
            # Fraction division: (a/b) / (c/d) = (a*d)/(b*c)
            a = rng.choice([1, 2, 3, 5])
            b = rng.choice([3, 4, 5, 6])
            c = rng.choice([1, 2, 3])
            d = rng.choice([2, 5, 7])

            eq_typst = f"({a}/{b}) div ({c}/{d})"
            num = a * d
            den = b * c
            g = math.gcd(num, den)
            num //= g
            den //= g

            ans_typst = f"{num}/{den}" if den != 1 else f"{num}"

            steps = [
                f"Recall fraction division rule: multiply by the reciprocal $ (a/b) div (c/d) = (a/b) dot (d/c) $",
                f"Flip the second fraction: $ ({a}/{b}) dot ({d}/{c}) $",
                f"Multiply numerators and denominators: $ ({a} dot {d}) / ({b} dot {c}) = {a*d} / {b*c} $",
                f"Reduce to simplest form: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"g6_frac_mild_{problem_idx}",
                prompt_text="Find each quotient. Simplify your answer completely.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{a*c}/{b*d}", f"{den}/{num}", f"{(num+1)}/{den}"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        else:
            # Decimal multiplication: a.b * c.d
            n1 = rng.choice([1.2, 2.5, 3.4, 0.5, 1.8])
            n2 = rng.choice([0.4, 1.5, 2.2, 3.1])
            prod = round(n1 * n2, 3)

            eq_typst = f"{n1} times {n2}"
            ans_typst = f"{prod}"

            steps = [
                f"Multiply as whole numbers ignoring decimal points.",
                f"Count total decimal places in both factors.",
                f"Place decimal point: $ {n1} times {n2} = {prod} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"g6_dec_med_{problem_idx}",
                prompt_text="Multiply the decimals.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{round(prod * 10, 2)}", f"{round(prod / 10, 4)}"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
