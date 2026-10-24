from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class PrecalcTrigGenerator(BaseGenerator):
    generator_id = "precalculus.trig"
    name = "Trigonometric Equations & Identities"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSF.TF.C.8", "CCSS.MATH.CONTENT.HSF.TF.C.9"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        choices = [
            ("2 sin(x) - 1 = 0", "pi/6, 5 pi/6", [
                "Isolate sin(x): $ 2 sin(x) = 1 $",
                "Divide by 2: $ sin(x) = 1/2 $",
                "Find reference angle in [0, 2 pi): $ x = pi/6 $",
                "Sine is positive in Quadrants I and II: $ x = pi/6, 5 pi/6 $"
            ]),
            ("2 cos(x) - sqrt(3) = 0", "pi/6, 11 pi/6", [
                "Isolate cos(x): $ 2 cos(x) = sqrt(3) $",
                "Divide by 2: $ cos(x) = (sqrt(3))/2 $",
                "Find reference angle in [0, 2 pi): $ x = pi/6 $",
                "Cosine is positive in Quadrants I and IV: $ x = pi/6, 11 pi/6 $"
            ]),
            ("tan(x) - 1 = 0", "pi/4, 5 pi/4", [
                "Isolate tan(x): $ tan(x) = 1 $",
                "Find reference angle in [0, 2 pi): $ x = pi/4 $",
                "Tangent is positive in Quadrants I and III: $ x = pi/4, 5 pi/4 $"
            ]),
            ("2 cos(x) + 1 = 0", "2 pi/3, 4 pi/3", [
                "Isolate cos(x): $ 2 cos(x) = -1 $",
                "Divide by 2: $ cos(x) = -1/2 $",
                "Reference angle is $ pi/3 $; Cosine is negative in Quadrants II and III",
                "Angles: $ x = 2 pi/3, 4 pi/3 $"
            ])
        ]

        eq_typst, ans_typst, steps = rng.choice(choices)

        return BaseProblem(
            id=f"pcalc_trig_{problem_idx}",
            prompt_text="Find all solutions to each equation in the interval [0, 2 pi).",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=["pi/3, 2 pi/3", "pi/2, 3 pi/2", "pi/4, 7 pi/4"],
            difficulty=difficulty,
            standards=self.standards
        )
