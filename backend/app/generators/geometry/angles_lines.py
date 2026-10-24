from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeometryAnglesLinesGenerator(BaseGenerator):
    generator_id = "geometry.angles_lines"
    name = "Angles, Lines & Transversals"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.CO.C.9"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        if difficulty == ProblemDifficulty.MILD:
            # Complementary or supplementary angles
            is_supp = rng.choice([True, False])
            total = 180 if is_supp else 90
            angle_name = "supplementary" if is_supp else "complementary"
            given = rng.choice([25, 35, 45, 55, 65, 75, 110, 125] if is_supp else [20, 32, 45, 54, 68])
            if given >= total:
                given = total - 30

            missing = total - given
            eq_typst = f"\"angle 1 and angle 2 are \" {angle_name}, quad m angle 1 = {given}^circle, quad m angle 2 = ?"
            ans_typst = f"m angle 2 = {missing}^circle"

            steps = [
                f"Recall that {angle_name} angles sum to $ {total}^circle $.",
                f"Equation: $ m angle 1 + m angle 2 = {total}^circle $",
                f"Substitute known angle: $ {given}^circle + m angle 2 = {total}^circle $",
                f"Subtract {given}^circle from both sides: $ m angle 2 = {total}^circle - {given}^circle = {missing}^circle $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"geom_ang_mild_{problem_idx}",
                prompt_text="Find the measure of angle 2.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"m angle 2 = {missing + 10}^circle", f"m angle 2 = {given}^circle"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        else:
            # Segment Addition Postulate: B is between A and C. AB = 2x + 3, BC = x + 5, AC = total
            x_val = rng.choice([3, 4, 5, 6, 7])
            c1 = rng.choice([2, 3])
            c2 = rng.choice([1, 4])
            ab = c1 * x_val + c2
            bc = x_val + 3
            ac = ab + bc

            eq_typst = f"B \" is between \" A \" and \" C. quad A B = {c1} x + {c2}, quad B C = x + 3, quad A C = {ac}"
            ans_typst = f"x = {x_val}"

            steps = [
                f"Apply Segment Addition Postulate: $ A B + B C = A C $",
                f"Substitute algebraic expressions: $ ({c1} x + {c2}) + (x + 3) = {ac} $",
                f"Combine like terms: $ {c1 + 1} x + {c2 + 3} = {ac} $",
                f"Subtract {c2 + 3} from both sides: $ {c1 + 1} x = {ac - (c2 + 3)} $",
                f"Divide by {c1 + 1}: $ x = {x_val} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"geom_ang_med_{problem_idx}",
                prompt_text="Solve for x using the Segment Addition Postulate.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"x = {x_val + 2}", f"x = {x_val - 1}"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
