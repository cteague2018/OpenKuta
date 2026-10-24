from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeometryCirclesGenerator(BaseGenerator):
    generator_id = "geometry.circles"
    name = "Circles (Circumference, Area, Arcs & Chords)"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.C.A.2", "CCSS.MATH.CONTENT.HSG.C.B.5"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        r = rng.choice([3, 4, 5, 6, 7, 8, 9, 10])

        if difficulty == ProblemDifficulty.MILD:
            # Circumference & Area
            eq_typst = f"\"radius \" r = {r}"
            c_val = 2 * r
            a_val = r * r
            ans_typst = f"C = {c_val} pi, quad A = {a_val} pi"

            steps = [
                f"Recall circle formulas: $ C = 2 pi r $ and $ A = pi r^2 $",
                f"Calculate circumference: $ C = 2 pi ({r}) = {c_val} pi $",
                f"Calculate area: $ A = pi ({r})^2 = {a_val} pi $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"geom_circ_mild_{problem_idx}",
                prompt_text="Find the exact circumference and area of each circle in terms of pi.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"C = {r} pi, A = {a_val} pi", f"C = {c_val} pi, A = {c_val} pi"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        else:
            # Arc Length: s = 2 pi r * (theta / 360)
            theta = rng.choice([60, 90, 120, 180, 270])
            eq_typst = f"\"radius \" r = {r}, quad \"central angle \" theta = {theta}^circle"
            # s = (2 * r * theta) / 360 * pi
            # reduce fraction
            import math
            num = 2 * r * theta
            den = 360
            g = math.gcd(num, den)
            num //= g
            den //= g
            arc_str = f"({num} pi)/{den}" if den != 1 else f"{num} pi"
            ans_typst = f"s = {arc_str}"

            steps = [
                f"Recall arc length formula: $ s = 2 pi r dot (theta / 360^circle) $",
                f"Substitute given values: $ s = 2 pi ({r}) dot ({theta}^circle / 360^circle) $",
                f"Multiply: $ s = ({2*r*theta} pi) / 360 $",
                f"Reduce fraction: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"geom_circ_med_{problem_idx}",
                prompt_text="Find the length of each arc in terms of pi.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"s = {r} pi", f"s = ({theta} pi)/360"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
