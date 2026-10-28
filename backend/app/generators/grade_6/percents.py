from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class Grade6PercentsGenerator(BaseGenerator):
    generator_id = "grade_6.percents"
    name = "Percents & Conversions"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.RP.A.3.C"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            pct = rng.choice([10, 20, 25, 50, 75])
            base = rng.choice([20, 40, 60, 80, 100, 120, 200])
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
            distractors = [f"{val + 5}", f"{val * 2}", f"{abs(base - pct)}"]
        elif difficulty == ProblemDifficulty.MEDIUM:
            pct = rng.choice([15, 30, 35, 45, 65, 85])
            base = rng.choice([40, 60, 80, 140, 160, 240])
            val_calc = (pct * base) / 100
            val = int(val_calc) if val_calc.is_integer() else round(val_calc, 2)
            eq_typst = f"Find {pct}% of {base}."
            ans_typst = f"$ {val} $"
            steps = [
                f"Write {pct}% as a decimal: $ {pct / 100} $",
                f"Multiply by {base}: $ {pct / 100} dot {base} = {val} $",
                f"Result: $ {ans_typst} $"
            ]
            distractors = [f"{val + 6}", f"{round(val / 2, 1)}", f"{base - pct}"]
        else:
            # Find the whole given part and percent
            pct = rng.choice([20, 25, 40, 50, 75, 80])
            whole = rng.choice([40, 60, 80, 120, 160, 200])
            part = (pct * whole) // 100
            eq_typst = f"{part} is {pct}% of what number?"
            ans_typst = f"$ {whole} $"
            steps = [
                f"Set up percent equation: $ ({pct}/100) dot w = {part} $",
                f"Divide {part} by {pct/100}: $ w = {part} / {pct/100} = {whole} $",
                f"Result: $ {ans_typst} $"
            ]
            distractors = [f"{part * pct // 100}", f"{whole + 20}", f"{whole - 15}"]

        return BaseProblem(
            id=f"g6_pct_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each percent problem.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=difficulty,
            standards=self.standards
        )
