from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6PercentsGenerator(BaseGenerator):
    generator_id = "grade_6.percents"
    name = "Percents & Conversions"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.RP.A.3.C"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        pct = rng.choice([10, 15, 20, 25, 30, 40, 50, 75])
        base = rng.choice([20, 40, 50, 60, 80, 100, 120, 200])

        val_calc = (pct * base) / 100
        val = int(val_calc) if val_calc.is_integer() else round(val_calc, 2)
        eq_typst = f"What is {pct}% of {base}?"
        ans_typst = f"$ {val} $"

        steps = [
            f"Convert percentage to a decimal or fraction: $ {pct}% = {pct}/100 = {pct/100} $",
            f"Multiply by the whole: $ ({pct/100}) dot ({base}) $",
            f"Calculate product: $ {val} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"g6_pct_{problem_idx}",
            prompt_text="Solve each percent problem.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"{val + 5}", f"{val * 2}", f"{base - pct}"],
            difficulty=difficulty,
            standards=self.standards
        )
