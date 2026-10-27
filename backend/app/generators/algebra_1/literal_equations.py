from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class LiteralEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.literal_equations"
    name = "Literal Equations"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.CED.A.4", "CCSS.MATH.CONTENT.HSA.REI.B.3"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            patterns = [
                ("Solve for y", "2x + y = 10", "y = 10 - 2x", ["y = 2x - 10", "y = 10 + 2x", "y = 5 - x"]),
                ("Solve for x", "x - 4y = 8", "x = 8 + 4y", ["x = 8 - 4y", "x = 4y - 8", "x = 2 + y"]),
                ("Solve for h", "A = b h", "h = A / b", ["h = A - b", "h = b / A", "h = A b"]),
                ("Solve for r", "d = r t", "r = d / t", ["r = d - t", "r = t / d", "r = d t"]),
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            a = rng.choice([2, 3, 4, 5])
            b = rng.choice([2, 3, 5])
            c = rng.randint(6, 24)
            patterns = [
                (
                    "Solve for y",
                    f"{a}x + {b}y = {c}",
                    f"y = ({c} - {a}x) / {b}",
                    [f"y = ({c} + {a}x) / {b}", f"y = {c} - {a}x", f"y = ({a}x - {c}) / {b}"]
                ),
                (
                    "Solve for x",
                    f"{a}x - {b}y = {c}",
                    f"x = ({c} + {b}y) / {a}",
                    [f"x = ({c} - {b}y) / {a}", f"x = {c} + {b}y", f"x = ({b}y - {c}) / {a}"]
                ),
                (
                    "Solve for w",
                    "P = 2l + 2w",
                    "w = (P - 2l) / 2",
                    ["w = P - 2l", "w = (P + 2l) / 2", "w = P / 2 - l"]
                ),
            ]
        else:  # SPICY
            patterns = [
                (
                    "Solve for C",
                    "F = 9/5 C + 32",
                    "C = 5/9 (F - 32)",
                    ["C = 9/5 (F - 32)", "C = 5/9 F - 32", "C = 5/9 (F + 32)"]
                ),
                (
                    "Solve for h",
                    "V = 1/3 pi r^2 h",
                    "h = (3V) / (pi r^2)",
                    ["h = (V) / (3 pi r^2)", "h = (3V pi) / r^2", "h = 3V - pi r^2"]
                ),
                (
                    "Solve for x",
                    "a x + b = c x + d",
                    "x = (d - b) / (a - c)",
                    ["x = (d + b) / (a - c)", "x = (d - b) / (a + c)", "x = (a - c) / (d - b)"]
                ),
            ]

        pattern_tuple = rng.choice(patterns)
        if len(pattern_tuple) == 5:
            prompt_prefix, eq_typst, ans_typst, distractors, custom_steps = pattern_tuple
            steps = custom_steps
        else:
            prompt_prefix, eq_typst, ans_typst, distractors = pattern_tuple
            steps = [
                f"Given equation: $ {eq_typst} $",
                f"Goal: {prompt_prefix}.",
                "Isolate the target variable on one side of the equation.",
                f"Result: $ {ans_typst} $"
            ]

        return BaseProblem(
            id=f"literal_{difficulty.value}_{problem_idx}",
            prompt_text=f"{prompt_prefix}.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": eq_typst}
        )
