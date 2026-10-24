from __future__ import annotations

import random
from typing import List
import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.typst_utils import format_polynomial_typst


class PolynomialFactoringGenerator(BaseGenerator):
    generator_id = "algebra_1.factoring"
    name = "Factoring Polynomials (GCF, Trinomials, Difference of Squares)"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.HSA.SSE.A.2",
        "CCSS.MATH.CONTENT.HSA.SSE.B.3.A",
        "TEKS.MATH.A1.10.E",
        "TEKS.MATH.A1.10.F"
    ]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x = sp.Symbol('x')

        if difficulty == ProblemDifficulty.MILD:
            return self._generate_difference_of_squares_or_gcf(rng, problem_idx, allow_negatives, x)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_trinomial_monic(rng, problem_idx, allow_negatives, x)
        else:
            return self._generate_trinomial_non_monic(rng, problem_idx, allow_negatives, x)

    def _generate_difference_of_squares_or_gcf(
        self, rng: random.Random, idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Difference of two squares: a^2 x^2 - b^2."""
        b = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        a = rng.choice([1, 1, 1, 2, 3])  # mostly 1

        poly_expr = (a * x)**2 - b**2
        eq_typst = format_polynomial_typst(poly_expr, x)

        ax_str = f"{a}x" if a != 1 else "x"
        ans_typst = f"({ax_str} - {b})({ax_str} + {b})"

        d1 = f"({ax_str} - {b})^2"
        d2 = f"({ax_str} + {b})^2"
        d3 = f"({ax_str} - {b // 2 if b % 2 == 0 else b})({ax_str} + {b // 2 if b % 2 == 0 else b})"

        steps = [
            f"Recognize difference of two squares: $ A^2 - B^2 = (A - B)(A + B) $",
            f"Identify $ A = {ax_str} $ and $ B = {b} $",
            f"Factor: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"factor_mild_{idx}",
            prompt_text="Factor each completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"type": "diff_of_squares", "a": a, "b": b}
        )

    def _generate_trinomial_monic(
        self, rng: random.Random, idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Monic trinomial: x^2 + bx + c = (x + p)(x + q)."""
        pool = list(range(1, 10))
        if allow_negatives:
            pool += list(range(-9, 0))

        p = rng.choice(pool)
        q = rng.choice(pool)
        while p == 0 or q == 0:
            p = rng.choice(pool)

        poly_expr = sp.expand((x + p) * (x + q))
        eq_typst = format_polynomial_typst(poly_expr, x)

        p_sign = f"+ {p}" if p > 0 else f"- {abs(p)}"
        q_sign = f"+ {q}" if q > 0 else f"- {abs(q)}"
        ans_typst = f"(x {p_sign})(x {q_sign})"

        # Distractors
        d1 = f"(x {'- ' if p > 0 else '+ '}{abs(p)})(x {'- ' if q > 0 else '+ '}{abs(q)})"
        d2 = f"(x {'- ' if p > 0 else '+ '}{abs(p)})(x {q_sign})"
        d3 = f"(x + {p * q})(x + 1)"

        steps = [
            f"Given trinomial: $ {eq_typst} $",
            f"Find two numbers that multiply to $ {p * q} $ and add to $ {p + q} $",
            f"The two numbers are $ {p} $ and $ {q} $",
            f"Factored form: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"factor_med_{idx}",
            prompt_text="Factor each completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"p": p, "q": q}
        )

    def _generate_trinomial_non_monic(
        self, rng: random.Random, idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Non-monic trinomial: (ax + p)(bx + q)."""
        a = rng.choice([2, 3, 5])
        b = 1
        p = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

        poly_expr = sp.expand((a * x + p) * (b * x + q))
        eq_typst = format_polynomial_typst(poly_expr, x)

        p_sign = f"+ {p}" if p > 0 else f"- {abs(p)}"
        q_sign = f"+ {q}" if q > 0 else f"- {abs(q)}"
        ans_typst = f"({a}x {p_sign})(x {q_sign})"

        d1 = f"(x {p_sign})({a}x {q_sign})"
        d2 = f"({a}x {'- ' if p > 0 else '+ '}{abs(p)})(x {q_sign})"
        d3 = f"({a}x {p_sign})(x {'- ' if q > 0 else '+ '}{abs(q)})"

        steps = [
            f"Given non-monic trinomial: $ {eq_typst} $",
            f"Use grouping / ac method: find factors of $ a c = {a * (p * q)} $ summing to middle coefficient",
            f"Split middle term and factor by grouping",
            f"Factored form: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"factor_spicy_{idx}",
            prompt_text="Factor each completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"a": a, "p": p, "q": q}
        )

