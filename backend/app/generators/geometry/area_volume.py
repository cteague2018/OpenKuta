from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeometryAreaVolumeGenerator(BaseGenerator):
    generator_id = "geometry.area_volume"
    name = "Surface Area and Volume of Solids"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.GMD.A.3"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        l = rng.choice([3, 4, 5, 6, 8])
        w = rng.choice([2, 3, 4, 5])
        h = rng.choice([4, 6, 7, 9, 10])

        vol = l * w * h
        sa = 2 * (l * w + l * h + w * h)

        eq_typst = f"\"Rectangular prism: length = \" {l}, quad \"width = \" {w}, quad \"height = \" {h}"
        ans_typst = f"V = {vol}, quad \"SA\" = {sa}"

        steps = [
            f"Recall volume formula for a rectangular prism: $ V = l dot w dot h $",
            f"Calculate volume: $ V = ({l}) dot ({w}) dot ({h}) = {vol} $",
            f"Recall surface area formula: $ \"SA\" = 2(l w + l h + w h) $",
            f"Calculate face areas: $ l w = {l*w}, l h = {l*h}, w h = {w*h} $",
            f"Sum and double: $ 2({l*w} + {l*h} + {w*h}) = 2({l*w + l*h + w*h}) = {sa} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"geom_vol_{problem_idx}",
            prompt_text="Find the volume and surface area of each solid.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"V = {vol}, SA = {vol / 2}", f"V = {l*w + h}, SA = {sa}"],
            difficulty=difficulty,
            standards=self.standards
        )
