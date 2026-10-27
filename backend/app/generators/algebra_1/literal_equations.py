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
                (
                    "Solve for y",
                    "2x + y = 10",
                    "y = 10 - 2x",
                    ["y = 2x - 10", "y = 10 + 2x", "y = 5 - x"],
                    [
                        "Given equation: $2x + y = 10$.",
                        "Subtract $2x$ from both sides to isolate $y$: $y = 10 - 2x$.",
                        "Result: $y = 10 - 2x$."
                    ]
                ),
                (
                    "Solve for x",
                    "x - 4y = 8",
                    "x = 8 + 4y",
                    ["x = 8 - 4y", "x = 4y - 8", "x = 2 + y"],
                    [
                        "Given equation: $x - 4y = 8$.",
                        "Add $4y$ to both sides to isolate $x$: $x = 8 + 4y$.",
                        "Result: $x = 8 + 4y$."
                    ]
                ),
                (
                    "Solve for h",
                    "A = b h",
                    "h = A / b",
                    ["h = A - b", "h = b / A", "h = A b"],
                    [
                        "Given area formula: $A = b h$.",
                        "Divide both sides by $b$ to isolate $h$: $h = A / b$.",
                        "Result: $h = A / b$."
                    ]
                ),
                (
                    "Solve for r",
                    "d = r t",
                    "r = d / t",
                    ["r = d - t", "r = t / d", "r = d t"],
                    [
                        "Given distance formula: $d = r t$.",
                        "Divide both sides by $t$ to isolate $r$: $r = d / t$.",
                        "Result: $r = d / t$."
                    ]
                ),
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
                    [f"y = ({c} + {a}x) / {b}", f"y = {c} - {a}x", f"y = ({a}x - {c}) / {b}"],
                    [
                        f"Given equation: ${a}x + {b}y = {c}$.",
                        f"Subtract ${a}x$ from both sides: ${b}y = {c} - {a}x$.",
                        f"Divide both sides by ${b}$: $y = ({c} - {a}x) / {b}$.",
                        f"Result: $y = ({c} - {a}x) / {b}$."
                    ]
                ),
                (
                    "Solve for x",
                    f"{a}x - {b}y = {c}",
                    f"x = ({c} + {b}y) / {a}",
                    [f"x = ({c} - {b}y) / {a}", f"x = {c} + {b}y", f"x = ({b}y - {c}) / {a}"],
                    [
                        f"Given equation: ${a}x - {b}y = {c}$.",
                        f"Add ${b}y$ to both sides: ${a}x = {c} + {b}y$.",
                        f"Divide both sides by ${a}$: $x = ({c} + {b}y) / {a}$.",
                        f"Result: $x = ({c} + {b}y) / {a}$."
                    ]
                ),
                (
                    "Solve for w",
                    "P = 2l + 2w",
                    "w = (P - 2l) / 2",
                    ["w = P - 2l", "w = (P + 2l) / 2", "w = P / 2 - l"],
                    [
                        "Given perimeter formula: $P = 2l + 2w$.",
                        "Subtract $2l$ from both sides: $2w = P - 2l$.",
                        "Divide both sides by $2$: $w = (P - 2l) / 2$.",
                        "Result: $w = (P - 2l) / 2$."
                    ]
                ),
            ]
        else:  # SPICY
            patterns = [
                (
                    "Solve for C",
                    "F = 9/5 C + 32",
                    "C = 5/9 (F - 32)",
                    ["C = 9/5 (F - 32)", "C = 5/9 F - 32", "C = 5/9 (F + 32)"],
                    [
                        "Given temperature formula: $F = 9/5 C + 32$.",
                        "Subtract $32$ from both sides: $F - 32 = 9/5 C$.",
                        "Multiply both sides by $5/9$: $C = 5/9 (F - 32)$.",
                        "Result: $C = 5/9 (F - 32)$."
                    ]
                ),
                (
                    "Solve for h",
                    "V = 1/3 pi r^2 h",
                    "h = (3V) / (pi r^2)",
                    ["h = (V) / (3 pi r^2)", "h = (3V pi) / r^2", "h = 3V - pi r^2"],
                    [
                        "Given cone volume formula: $V = 1/3 pi r^2 h$.",
                        "Multiply both sides by $3$: $3V = pi r^2 h$.",
                        "Divide both sides by $pi r^2$: $h = (3V) / (pi r^2)$.",
                        "Result: $h = (3V) / (pi r^2)$."
                    ]
                ),
                (
                    "Solve for x",
                    "a x + b = c x + d",
                    "x = (d - b) / (a - c)",
                    ["x = (d + b) / (a - c)", "x = (d - b) / (a + c)", "x = (a - c) / (d - b)"],
                    [
                        "Given linear equation: $a x + b = c x + d$.",
                        "Collect $x$ terms on one side and constants on the other: $a x - c x = d - b$.",
                        "Factor out $x$: $x(a - c) = d - b$.",
                        "Divide both sides by $(a - c)$: $x = (d - b) / (a - c)$."
                    ]
                ),
            ]

        prompt_prefix, eq_typst, ans_typst, distractors, steps = rng.choice(patterns)

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
