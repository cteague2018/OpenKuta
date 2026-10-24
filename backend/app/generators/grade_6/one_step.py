from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6OneStepGenerator(BaseGenerator):
    generator_id = "grade_6.one_step"
    name = "One-Step Equations and Inequalities"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.EE.B.7", "CCSS.MATH.CONTENT.6.EE.B.8"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        op = rng.choice(["add", "sub", "mul", "div"])
        x_val = rng.choice([3, 4, 5, 6, 7, 8, 9, 12])
        k = rng.choice([2, 3, 4, 5, 6, 7])

        if op == "add":
            eq_typst = f"x + {k} = {x_val + k}"
            ans_typst = f"x = {x_val}"
            steps = [
                f"Identify the operation performed on x: addition of {k}.",
                f"Apply inverse operation: subtract {k} from both sides: $ x = ({x_val + k}) - {k} $",
                f"Calculate difference: $ x = {x_val} $",
                f"Result: $ {ans_typst} $"
            ]
        elif op == "sub":
            eq_typst = f"x - {k} = {x_val}"
            ans_typst = f"x = {x_val + k}"
            steps = [
                f"Identify the operation performed on x: subtraction of {k}.",
                f"Apply inverse operation: add {k} to both sides: $ x = {x_val} + {k} $",
                f"Calculate sum: $ x = {x_val + k} $",
                f"Result: $ {ans_typst} $"
            ]
        elif op == "mul":
            eq_typst = f"{k} x = {k * x_val}"
            ans_typst = f"x = {x_val}"
            steps = [
                f"Identify the operation performed on x: multiplication by {k}.",
                f"Apply inverse operation: divide both sides by {k}: $ x = ({k * x_val}) / {k} $",
                f"Calculate quotient: $ x = {x_val} $",
                f"Result: $ {ans_typst} $"
            ]
        else:
            eq_typst = f"x / {k} = {x_val}"
            ans_typst = f"x = {k * x_val}"
            steps = [
                f"Identify the operation performed on x: division by {k}.",
                f"Apply inverse operation: multiply both sides by {k}: $ x = {x_val} dot {k} $",
                f"Calculate product: $ x = {k * x_val} $",
                f"Result: $ {ans_typst} $"
            ]

        return BaseProblem(
            id=f"g6_onestep_{problem_idx}",
            prompt_text="Solve each one-step equation.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"x = {x_val + 1}", f"x = {x_val - 2}"],
            difficulty=difficulty,
            standards=self.standards
        )
