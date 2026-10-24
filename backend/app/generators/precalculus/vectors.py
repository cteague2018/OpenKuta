from __future__ import annotations

import math
import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class PrecalcVectorsGenerator(BaseGenerator):
    generator_id = "precalculus.vectors"
    name = "Vectors (Magnitude, Operations, Dot Product)"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSN.VM.B.4", "CCSS.MATH.CONTENT.HSN.VM.B.5"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        if difficulty == ProblemDifficulty.MILD:
            # Finding magnitude: u = <a, b>
            a = rng.choice([3, 4, 5, 6, 8, 12])
            b = rng.choice([3, 4, 5, 8, 9, 12])
            eq_typst = f"bold(v) = angle.l {a}, {b} angle.r"
            mag_sq = a * a + b * b
            root = int(round(math.sqrt(mag_sq)))
            if root * root == mag_sq:
                ans_typst = f"norm(bold(v)) = {root}"
            else:
                ans_typst = f"norm(bold(v)) = sqrt({mag_sq})"

            steps = [
                f"Recall vector magnitude formula: $ norm(bold(v)) = sqrt(x^2 + y^2) $",
                f"Substitute components: $ norm(bold(v)) = sqrt(({a})^2 + ({b})^2) $",
                f"Calculate squares: $ sqrt({a*a} + {b*b}) = sqrt({mag_sq}) $",
                f"Simplify: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"pcalc_vec_mild_{problem_idx}",
                prompt_text="Find the magnitude of each vector.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"norm(bold(v)) = {a + b}", f"norm(bold(v)) = {mag_sq}"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        else:
            # Dot Product: u = <a1, a2>, v = <b1, b2>
            a1, a2 = rng.choice([2, 3, 4, -2, -3]), rng.choice([1, 2, 5, -4])
            b1, b2 = rng.choice([3, 4, 5, -1, -3]), rng.choice([2, 3, -2, 4])
            eq_typst = f"bold(u) = angle.l {a1}, {a2} angle.r, quad bold(v) = angle.l {b1}, {b2} angle.r"
            dot = a1 * b1 + a2 * b2
            ans_typst = f"bold(u) dot bold(v) = {dot}"

            steps = [
                f"Recall dot product definition: $ bold(u) dot bold(v) = u_1 v_1 + u_2 v_2 $",
                f"Multiply corresponding components: $ ({a1})({b1}) + ({a2})({b2}) $",
                f"Calculate products: $ ({a1*b1}) + ({a2*b2}) $",
                f"Sum: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"pcalc_vec_med_{problem_idx}",
                prompt_text="Find the dot product of the given vectors.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"bold(u) dot bold(v) = {a1*b1 - a2*b2}", f"bold(u) dot bold(v) = {dot + 5}"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
