from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class VerbalExpressionsGenerator(BaseGenerator):
    generator_id = "algebra_1.verbal_expressions"
    name = "Verbal Expressions"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.SSE.A.1", "CCSS.MATH.CONTENT.6.EE.A.2"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        var = rng.choice(["x", "n", "y", "a", "k", "m"])
        num1 = rng.randint(2, 12)
        num2 = rng.randint(2, 9)

        if difficulty == ProblemDifficulty.MILD:
            patterns = [
                (
                    f"The sum of {num1} and a number {var}",
                    f"{var} + {num1}",
                    [f"{var} - {num1}", f"{num1} * {var}", f"{var} / {num1}"]
                ),
                (
                    f"{num1} less than a number {var}",
                    f"{var} - {num1}",
                    [f"{num1} - {var}", f"{var} + {num1}", f"{num1} * {var}"]
                ),
                (
                    f"The product of {num2} and a number {var}",
                    f"{num2}{var}",
                    [f"{var} + {num2}", f"{var} / {num2}", f"{var}^{num2}"]
                ),
                (
                    f"The quotient of a number {var} and {num1}",
                    f"{var} / {num1}",
                    [f"{num1} / {var}", f"{num1}{var}", f"{var} - {num1}"]
                ),
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            patterns = [
                (
                    f"{num1} more than twice a number {var}",
                    f"2{var} + {num1}",
                    [f"2({var} + {num1})", f"{var} + 2*{num1}", f"2{var} - {num1}"]
                ),
                (
                    f"{num1} less than {num2} times a number {var}",
                    f"{num2}{var} - {num1}",
                    [f"{num1} - {num2}{var}", f"{num2}({var} - {num1})", f"{num2}{var} + {num1}"]
                ),
                (
                    f"The sum of {num2} times a number {var} and {num1}",
                    f"{num2}{var} + {num1}",
                    [f"{num2}({var} + {num1})", f"{var} + {num2}*{num1}", f"{num2}{var} - {num1}"]
                ),
                (
                    f"The quotient of {num1} more than {var}, and {num2}",
                    f"({var} + {num1}) / {num2}",
                    [f"{var} + {num1} / {num2}", f"{num2} / ({var} + {num1})", f"{var}/{num2} + {num1}"]
                ),
            ]
        else: # SPICY
            patterns = [
                (
                    f"Twice the difference of {num2} times a number {var} and {num1}",
                    f"2({num2}{var} - {num1})",
                    [f"2*{num2}{var} - {num1}", f"2({num1} - {num2}{var})", f"{num2}{var} - 2*{num1}"]
                ),
                (
                    f"The square of the sum of a number {var} and {num1}",
                    f"({var} + {num1})^2",
                    [f"{var}^2 + {num1}^2", f"{var}^2 + {num1}", f"2({var} + {num1})"]
                ),
                (
                    f"{num1} less than the quotient of {num2} and the square of {var}",
                    f"{num2} / {var}^2 - {num1}",
                    [f"{var}^2 / {num2} - {num1}", f"{num1} - {num2} / {var}^2", f"({num2} - {num1}) / {var}^2"]
                ),
            ]

        phrase, ans_expr, distractors = rng.choice(patterns)
        steps = [
            f"Identify the mathematical operations in the verbal phrase: '{phrase}'.",
            f"Translate the unknown quantity as variable: $ {var} $.",
            f"Formulate the algebraic expression: $ {ans_expr} $."
        ]

        return BaseProblem(
            id=f"verbal_expr_{difficulty.value}_{problem_idx}",
            prompt_text="Write each as an algebraic expression.",
            equation_typst=phrase,
            answer_typst=f"$ {ans_expr} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"phrase": phrase, "variable": var}
        )

