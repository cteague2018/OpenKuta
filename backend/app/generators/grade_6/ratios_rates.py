from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class Grade6RatiosRatesGenerator(BaseGenerator):
    generator_id = "grade_6.ratios_rates"
    name = "Ratios, Rates & Unit Rates"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.RP.A.1", "CCSS.MATH.CONTENT.6.RP.A.2", "CCSS.MATH.CONTENT.6.RP.A.3"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Unit rate: $cost for n items
            n = rng.choice([3, 4, 5, 6])
            rate = rng.choice([2, 3, 4, 5, 7, 8])
            total = n * rate

            eq_typst = f"Cost: \\${total} for {n} items"
            ans_typst = f"\\${rate} per item"

            steps = [
                "Recall unit rate formula: $ \"Unit Rate\" = (\"Total Cost\") / (\"Total Items\") $",
                f"Divide cost by number of items: $ ({total}) / ({n}) $",
                f"Calculate quotient: $ {rate} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"g6_ratio_mild_{problem_idx}",
                prompt_text="Find the unit rate.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"\\${rate + 1} per item", f"\\${int(total / 2)} per item"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Equivalent ratios: a / b = x / d
            a = rng.choice([2, 3, 4, 5])
            b = rng.choice([3, 5, 7, 8])
            k = rng.choice([2, 3, 4, 5])
            c = a * k
            d = b * k

            eq_typst = f"{a} / {b} = x / {d}"
            ans_typst = f"x = {c}"

            steps = [
                f"Identify the multiplier between denominators: $ {d} / {b} = {k} $",
                f"Multiply numerator by the same scale factor: $ x = {a} dot {k} $",
                f"Calculate product: $ {a} dot {k} = {c} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"g6_ratio_med_{problem_idx}",
                prompt_text="Find the missing value to make an equivalent ratio.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"x = {c + 1}", f"x = {d - b}", f"x = {c * 2}"],
                difficulty=difficulty,
                standards=self.standards
            )
        else:
            # Spicy: Cross-multiplication or rate prediction over larger quantity
            a = rng.choice([3, 4, 5, 7, 9])
            b = rng.choice([4, 5, 6, 8, 10])
            while a == b:
                b += 1
            k = rng.choice([6, 7, 8, 9, 11])
            c = a * k
            d = b * k

            eq_typst = f"{c} / x = {a} / {b}"
            ans_typst = f"x = {d}"

            steps = [
                f"Cross-multiply to solve the proportion: $ {a} x = {c} dot {b} = {c * b} $",
                f"Divide both sides by {a}: $ x = {c * b} / {a} = {d} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"g6_ratio_spicy_{problem_idx}",
                prompt_text="Solve the proportion for x.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"x = {d + b}", f"x = {c}", f"x = {d - a}"],
                difficulty=difficulty,
                standards=self.standards
            )
