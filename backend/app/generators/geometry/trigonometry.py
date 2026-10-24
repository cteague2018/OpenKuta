from __future__ import annotations

import math
import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeometryTrigonometryGenerator(BaseGenerator):
    generator_id = "geometry.trigonometry"
    name = "Right Triangle Trigonometry"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.SRT.C.6", "CCSS.MATH.CONTENT.HSG.SRT.C.8"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        # Triples: 3-4-5, 5-12-13, 8-15-17
        triple = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
        opp, adj, hyp = triple

        func_name = rng.choice(["sin", "cos", "tan"])
        if func_name == "sin":
            ratio_str = f"{opp}/{hyp}"
            desc = "opposite / hypotenuse"
            num, den = opp, hyp
        elif func_name == "cos":
            ratio_str = f"{adj}/{hyp}"
            desc = "adjacent / hypotenuse"
            num, den = adj, hyp
        else:
            ratio_str = f"{opp}/{adj}"
            desc = "opposite / adjacent"
            num, den = opp, adj

        eq_typst = f"\"opposite = \" {opp}, quad \"adjacent = \" {adj}, quad \"hypotenuse = \" {hyp}"
        ans_typst = f"{func_name}(theta) = {ratio_str}"

        steps = [
            f"Recall trigonometric definition for right triangles: SOH CAH TOA.",
            f"$ {func_name}(theta) = text(\"{desc}\") $",
            f"Substitute side values: $ {func_name}(theta) = {num} / {den} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"geom_trig_{problem_idx}",
            prompt_text=f"Find the value of {func_name}(theta) for the given right triangle.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"{func_name}(theta) = {den}/{num}", f"{func_name}(theta) = {opp}/{hyp}" if func_name != "sin" else f"{func_name}(theta) = {adj}/{hyp}"],
            difficulty=difficulty,
            standards=self.standards
        )
