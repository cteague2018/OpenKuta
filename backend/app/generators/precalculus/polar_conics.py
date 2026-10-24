from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class PrecalcPolarConicsGenerator(BaseGenerator):
    generator_id = "precalculus.polar_conics"
    name = "Polar Coordinates & Conic Sections"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSG.GPE.A.1", "CCSS.MATH.CONTENT.HSG.GPE.A.3"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        h = rng.choice([-4, -2, 0, 1, 3, 5])
        k = rng.choice([-3, -1, 0, 2, 4])
        r = rng.choice([2, 3, 4, 5, 6])

        h_str = f"- {h}" if h > 0 else (f"+ {-h}" if h < 0 else "")
        k_str = f"- {k}" if k > 0 else (f"+ {-k}" if k < 0 else "")

        x_part = f"(x {h_str})^2" if h != 0 else "x^2"
        y_part = f"(y {k_str})^2" if k != 0 else "y^2"

        eq_typst = f"\"Center: \" ({h}, {k}), quad \"Radius: \" {r}"
        ans_typst = f"{x_part} + {y_part} = {r*r}"

        steps = [
            f"Recall standard equation of a circle: $ (x - h)^2 + (y - k)^2 = r^2 $",
            f"Substitute center coordinates $ (h, k) = ({h}, {k}) $",
            f"Calculate radius squared: $ r^2 = ({r})^2 = {r*r} $",
            f"Assemble standard form: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"pcalc_conic_{problem_idx}",
            prompt_text="Write the standard form equation of each circle given its center and radius.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"{x_part} - {y_part} = {r*r}", f"{x_part} + {y_part} = {2*r}"],
            difficulty=difficulty,
            standards=self.standards
        )
