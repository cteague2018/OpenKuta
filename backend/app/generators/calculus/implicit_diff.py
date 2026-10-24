from __future__ import annotations

import random
from typing import List
import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class ImplicitDifferentiationGenerator(BaseGenerator):
    generator_id = "calculus.implicit_diff"
    name = "Implicit Differentiation"
    category = "Calculus"
    standards = [
        "AP.CALC.FUN-3.D",
        "AP.CALC.FUN-3.E"
    ]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        if difficulty == ProblemDifficulty.MILD:
            return self._generate_mild(rng, problem_idx)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_medium(rng, problem_idx)
        else:
            return self._generate_spicy(rng, problem_idx)

    def _generate_mild(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Circles/Ellipses: a x^2 + b y^2 = C.
        Derivative: 2a x + 2b y (dy/dx) = 0 ==> dy/dx = - (a x) / (b y).
        """
        a = rng.choice([1, 2, 3, 4, 5])
        b = rng.choice([1, 2, 3, 4, 5])
        c = rng.choice([9, 16, 25, 36, 49, 100])

        x_term = f"{a} x^2" if a > 1 else "x^2"
        y_term = f"{b} y^2" if b > 1 else "y^2"
        eq_typst = f"{x_term} + {y_term} = {c}"

        # d/dx(a x^2 + b y^2) = 2a x + 2b y dy/dx = 0
        ans_num = f"-{a} x" if a > 1 else "-x"
        ans_den = f"{b} y" if b > 1 else "y"
        ans_typst = f"(d y)/(d x) = ({ans_num}) / ({ans_den})"

        steps = [
            f"Differentiate both sides with respect to x: $ (d)/(d x) [{x_term} + {y_term}] = (d)/(d x) [{c}] $",
            f"Apply chain rule to y: $ {2*a} x + {2*b} y dot (d y)/(d x) = 0 $",
            f"Isolate dy/dx term: $ {2*b} y dot (d y)/(d x) = -{2*a} x $",
            f"Divide both sides by {2*b} y: $ (d y)/(d x) = (-{2*a} x) / ({2*b} y) $",
            f"Simplify: $ {ans_typst} $"
        ]

        distractors = [
            f"(d y)/(d x) = ({a} x) / ({b} y)",
            f"(d y)/(d x) = (-{b} y) / ({a} x)",
            f"(d y)/(d x) = -{a} x - {b} y"
        ]

        return BaseProblem(
            id=f"calc_implicit_mild_{problem_idx}",
            prompt_text="For each problem, use implicit differentiation to find dy/dx in terms of x and y.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Cubic or mixed polynomial: a x^3 - b y^2 = c x.
        Derivative: 3a x^2 - 2b y (dy/dx) = c ==> dy/dx = (c - 3a x^2) / (-2b y).
        """
        a = rng.choice([1, 2, 3])
        b = rng.choice([2, 3, 4])
        c = rng.choice([2, 4, 6, 8])

        eq_typst = f"{a} x^3 - {b} y^2 = {c} x"
        ans_typst = f"(d y)/(d x) = ({c} - {3*a} x^2) / (-{2*b} y)"

        steps = [
            f"Differentiate both sides with respect to x: $ (d)/(d x) [{a} x^3 - {b} y^2] = (d)/(d x) [{c} x] $",
            f"Apply power rule and chain rule: $ {3*a} x^2 - {2*b} y dot (d y)/(d x) = {c} $",
            f"Subtract {3*a} x^2 from both sides: $ -{2*b} y dot (d y)/(d x) = {c} - {3*a} x^2 $",
            f"Solve for dy/dx: $ {ans_typst} $"
        ]

        distractors = [
            f"(d y)/(d x) = ({3*a} x^2 - {c}) / ({2*b} y)",
            f"(d y)/(d x) = ({c}) / (-{2*b} y)",
            f"(d y)/(d x) = {3*a} x^2 / ({2*b} y)"
        ]

        return BaseProblem(
            id=f"calc_implicit_med_{problem_idx}",
            prompt_text="For each problem, use implicit differentiation to find dy/dx in terms of x and y.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Product rule terms: x y + y^2 = k.
        Derivative: (y + x dy/dx) + 2y dy/dx = 0 ==> (x + 2y) dy/dx = -y ==> dy/dx = -y / (x + 2y).
        """
        k = rng.choice([4, 6, 10, 12, 15])
        eq_typst = f"x y + y^2 = {k}"
        ans_typst = "(d y)/(d x) = (-y) / (x + 2 y)"

        steps = [
            f"Differentiate both sides with respect to x: $ (d)/(d x) [x y + y^2] = (d)/(d x) [{k}] $",
            f"Apply the product rule to x y and chain rule to y^2: $ (1 dot y + x dot (d y)/(d x)) + 2 y dot (d y)/(d x) = 0 $",
            f"Group terms with dy/dx: $ (x + 2 y) dot (d y)/(d x) + y = 0 $",
            f"Subtract y from both sides: $ (x + 2 y) dot (d y)/(d x) = -y $",
            f"Divide by (x + 2 y): $ {ans_typst} $"
        ]

        distractors = [
            "(d y)/(d x) = y / (x + 2 y)",
            "(d y)/(d x) = (-y) / (x + y)",
            "(d y)/(d x) = -1 / (2 y)"
        ]

        return BaseProblem(
            id=f"calc_implicit_spicy_{problem_idx}",
            prompt_text="For each problem, use implicit differentiation to find dy/dx in terms of x and y.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
