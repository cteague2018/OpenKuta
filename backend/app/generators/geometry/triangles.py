from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeometryTrianglesGenerator(BaseGenerator):
    generator_id = "geometry.triangles"
    name = "Triangles (Angle Sum, Exterior Angle, Congruence)"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.CO.C.10"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        a = rng.choice([35, 42, 50, 58, 65, 72])
        b = rng.choice([30, 45, 55, 60, 68])
        c = 180 - (a + b)

        eq_typst = f"m angle A = {a}^circle, quad m angle B = {b}^circle, quad m angle C = ?"
        ans_typst = f"m angle C = {c}^circle"

        steps = [
            f"Apply Triangle Angle Sum Theorem: The interior angles of any triangle sum to $ 180^circle $.",
            f"Equation: $ m angle A + m angle B + m angle C = 180^circle $",
            f"Substitute given angles: $ {a}^circle + {b}^circle + m angle C = 180^circle $",
            f"Combine known angles: $ {a + b}^circle + m angle C = 180^circle $",
            f"Subtract {a + b}^circle from 180: $ m angle C = 180^circle - {a + b}^circle = {c}^circle $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"geom_tri_{problem_idx}",
            prompt_text="Find the measure of angle C indicated in the triangle.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"m angle C = {c + 10}^circle", f"m angle C = {180 - c}^circle"],
            difficulty=difficulty,
            standards=self.standards
        )
