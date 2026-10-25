from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class SystemsOfEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.systems"
    name = "Systems of Two Linear Equations (Elimination & Substitution)"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.HSA.REI.C.6",
        "CCSS.MATH.CONTENT.8.EE.C.8.B",
        "TEKS.MATH.A1.5.C"
    ]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        # Backward parameterization: choose integer solution (x_sol, y_sol)
        x_sol = rng.randint(-6, 6) if allow_negatives else rng.randint(1, 6)
        y_sol = rng.randint(-6, 6) if allow_negatives else rng.randint(1, 6)

        if difficulty == ProblemDifficulty.MILD:
            return self._generate_elimination_direct(rng, problem_idx, x_sol, y_sol)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_substitution(rng, problem_idx, x_sol, y_sol)
        else:
            return self._generate_elimination_scaling(rng, problem_idx, x_sol, y_sol)

    def _generate_elimination_direct(
        self, rng: random.Random, problem_idx: int, x_sol: int, y_sol: int
    ) -> BaseProblem:
        """Coefficients match or are opposites directly: e.g. +y and -y."""
        a1 = rng.choice([2, 3, 4, -2, -3])
        b_val = rng.choice([1, 2])
        b1 = b_val
        b2 = -b_val  # Direct elimination by adding

        a2 = rng.choice([1, 2, 5])

        c1 = a1 * x_sol + b1 * y_sol
        c2 = a2 * x_sol + b2 * y_sol

        eq1 = f"{a1}x {'+ ' if b1 > 0 else '- '}{abs(b1)}y = {c1}"
        eq2 = f"{a2}x {'+ ' if b2 > 0 else '- '}{abs(b2)}y = {c2}"
        system_typst = f"cases({eq1}, {eq2})"
        ans_typst = f"({x_sol}, {y_sol})"

        # Distractor misconceptions:
        # 1. Swapped x and y: (y_sol, x_sol)
        d1 = f"({y_sol}, {x_sol})"
        # 2. Sign error on x or y
        d2 = f"({-x_sol}, {y_sol})"
        # 3. Arithmetic error in addition
        d3 = f"({x_sol + 1}, {y_sol - 1})"

        sum_a = a1 + a2
        sum_c = c1 + c2
        steps = [
            f"Given system: $ {system_typst} $",
            f"Add both equations to eliminate $y$: $ ({a1} + {a2})x = {c1} + ({c2}) $",
            f"Solve for $x$: $ {sum_a}x = {sum_c} ==> x = {x_sol} $",
            f"Substitute $ x = {x_sol} $ into first equation: $ {a1}({x_sol}) {'+ ' if b1 > 0 else '- '}{abs(b1)}y = {c1} $",
            f"Solve for $y$: $ y = {y_sol} $",
            f"Solution: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"sys_mild_{problem_idx}",
            prompt_text="Solve each system of equations by elimination.",
            equation_typst=f"$ {system_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"solution": (x_sol, y_sol)}
        )

    def _generate_substitution(
        self, rng: random.Random, problem_idx: int, x_sol: int, y_sol: int
    ) -> BaseProblem:
        """One equation has an isolated variable: e.g. y = mx + c."""
        # y = m*x + b
        m = rng.choice([-3, -2, -1, 1, 2, 3])
        b = y_sol - m * x_sol

        # Second equation: Ax + By = C
        A = rng.choice([2, 3, 4, 5])
        B = rng.choice([-2, -1, 1, 2])
        C = A * x_sol + B * y_sol

        b_sign = f"+ {b}" if b > 0 else f"- {abs(b)}"
        eq1 = f"y = {m if m != 1 else ''}{'x' if m != -1 else '-x'} {b_sign}".strip()
        eq2 = f"{A}x {'+ ' if B > 0 else '- '}{abs(B)}y = {C}"
        system_typst = f"cases({eq1}, {eq2})"
        ans_typst = f"({x_sol}, {y_sol})"

        d1 = f"({-x_sol}, {-y_sol})"
        d2 = f"({y_sol}, {x_sol})"
        d3 = f"({x_sol}, {-y_sol})"

        steps = [
            f"Given system: $ {system_typst} $",
            f"Substitute first equation into second equation: $ {A}x {'+ ' if B > 0 else '- '}{abs(B)}({eq1.split('=')[1].strip()}) = {C} $",
            f"Expand and combine like terms to solve for $x$: $ x = {x_sol} $",
            f"Substitute $ x = {x_sol} $ back to find $y$: $ y = {y_sol} $",
            f"Solution: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"sys_med_{problem_idx}",
            prompt_text="Solve each system of equations by substitution.",
            equation_typst=f"$ {system_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"solution": (x_sol, y_sol)}
        )

    def _generate_elimination_scaling(
        self, rng: random.Random, problem_idx: int, x_sol: int, y_sol: int
    ) -> BaseProblem:
        """Requires multiplying one or both equations by scalar constants."""
        a1, b1 = rng.choice([(2, 3), (3, 2), (4, 3), (5, 2)])
        a2, b2 = rng.choice([(3, -2), (2, -5), (3, 4), (-2, 5)])

        # Ensure determinant != 0
        if a1 * b2 - a2 * b1 == 0:
            b2 += 1

        c1 = a1 * x_sol + b1 * y_sol
        c2 = a2 * x_sol + b2 * y_sol

        eq1 = f"{a1}x {'+ ' if b1 > 0 else '- '}{abs(b1)}y = {c1}"
        eq2 = f"{a2}x {'+ ' if b2 > 0 else '- '}{abs(b2)}y = {c2}"
        system_typst = f"cases({eq1}, {eq2})"
        ans_typst = f"({x_sol}, {y_sol})"

        d1 = f"({x_sol + 2}, {y_sol - 1})"
        d2 = f"({-x_sol}, {y_sol})"
        d3 = f"({y_sol}, {x_sol})"

        steps = [
            f"Given system: $ {system_typst} $",
            f"Multiply equation (1) by {abs(b2)} and equation (2) by {abs(b1)} to eliminate $y$",
            f"Add or subtract aligned equations to find $x$: $ x = {x_sol} $",
            f"Substitute $ x = {x_sol} $ into original equation to solve for $y$: $ y = {y_sol} $",
            f"Solution: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"sys_spicy_{problem_idx}",
            prompt_text="Solve each system of equations by elimination.",
            equation_typst=f"$ {system_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"solution": (x_sol, y_sol)}
        )

