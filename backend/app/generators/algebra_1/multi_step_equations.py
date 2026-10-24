from __future__ import annotations

import random
from typing import List
import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class MultiStepEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.multi_step"
    name = "Multi-Step Linear Equations"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.HSA.REI.B.3",
        "CCSS.MATH.CONTENT.8.EE.C.7",
        "CCSS.MATH.CONTENT.8.EE.C.7.B",
        "TEKS.MATH.A1.5.A",
    ]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True,
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            return self._generate_mild(rng, problem_idx, allow_negatives)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_medium(rng, problem_idx, allow_negatives)
        else:
            return self._generate_spicy(rng, problem_idx, allow_negatives)

    def _generate_mild(self, rng: random.Random, idx: int, allow_negatives: bool) -> BaseProblem:
        """Mild: Distributive property a(x + b) = c or like terms ax + b + cx = d."""
        mode = rng.choice(["distribute", "like_terms"])

        if mode == "distribute":
            a = rng.choice([2, 3, 4, 5, -2, -3])
            r = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)
            b = rng.choice([-7, -5, -3, -2, 2, 3, 5, 7])
            c = a * (r + b)

            b_str = f"+ {b}" if b > 0 else f"- {abs(b)}"
            eq_typst = f"{a}(x {b_str}) = {c}"
            ans_typst = f"x = {r}"

            steps = [
                f"$ {eq_typst} $",
                f"Distribute {a}: $ {a}x {'+ ' if a*b >= 0 else '- '}{abs(a*b)} = {c} $",
                f"{'Subtract' if a*b > 0 else 'Add'} {abs(a*b)}: $ {a}x = {c - a*b} $",
                f"Divide by {a}: $ x = {r} $",
            ]
        else:
            # Combining like terms: a1*x + b + a2*x = c
            r = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)
            a1 = rng.choice([2, 3, 4, 5])
            a2 = rng.choice([2, 3, -1, -2])
            if a1 + a2 == 0:
                a2 = 1
            b = rng.choice([-8, -4, 3, 5, 9])
            c = (a1 + a2) * r + b

            a2_str = f"+ {a2}x" if a2 > 0 else f"- {abs(a2)}x"
            b_str = f"+ {b}" if b > 0 else f"- {abs(b)}"
            eq_typst = f"{a1}x {b_str} {a2_str} = {c}"
            ans_typst = f"x = {r}"

            steps = [
                f"$ {eq_typst} $",
                f"Combine like terms ({a1}x and {a2_str}): $ {a1+a2}x {b_str} = {c} $",
                f"{'Subtract' if b > 0 else 'Add'} {abs(b)}: $ {a1+a2}x = {c - b} $",
                f"Divide by {a1+a2}: $ x = {r} $",
            ]

        d1 = f"x = {-r}"
        d2 = f"x = {r + 2}"
        d3 = f"x = {r - 2}"

        return BaseProblem(
            id=f"multistep_mild_{idx}",
            prompt_text="Solve each multi-step equation.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
        )

    def _generate_medium(self, rng: random.Random, idx: int, allow_negatives: bool) -> BaseProblem:
        """Medium: Variables on both sides: a*x + b = c*x + d."""
        r = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)
        a = rng.choice([3, 4, 5, 6, 7])
        c = rng.choice([1, 2, -1, -2, -3])
        if a == c:
            c = 2
        b = rng.choice([-10, -6, -2, 4, 8, 12])
        d = (a - c) * r + b

        b_str = f"+ {b}" if b > 0 else f"- {abs(b)}"
        d_str = f"+ {d}" if d > 0 else f"- {abs(d)}"
        eq_typst = f"{a}x {b_str} = {c}x {d_str}"
        ans_typst = f"x = {r}"

        diff_a = a - c
        diff_d = d - b

        steps = [
            f"$ {eq_typst} $",
            f"Subtract {c}x from both sides: $ {diff_a}x {b_str} = {d} $",
            f"{'Subtract' if b > 0 else 'Add'} {abs(b)} from both sides: $ {diff_a}x = {diff_d} $",
            f"Divide by {diff_a}: $ x = {r} $",
        ]

        d1 = f"x = {-r}"
        d2 = f"x = {(d + b) // diff_a if (d + b) % diff_a == 0 else -r}"
        d3 = f"x = {r + 1}"

        return BaseProblem(
            id=f"multistep_med_{idx}",
            prompt_text="Solve each multi-step equation.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
        )

    def _generate_spicy(self, rng: random.Random, idx: int, allow_negatives: bool) -> BaseProblem:
        """Spicy: Distribute and variables on both sides: a(x + b) = c(x + d) + e."""
        r = rng.randint(-6, 6) if allow_negatives else rng.randint(1, 6)
        a = rng.choice([2, 3, 4])
        b = rng.choice([-4, -2, 1, 3, 5])
        c = rng.choice([1, -1, -2, 5])
        if a == c:
            c = -1

        lhs = a * (r + b)
        d_val = rng.choice([-3, -1, 2, 4])
        e = lhs - c * (r + d_val)

        b_str = f"+ {b}" if b > 0 else f"- {abs(b)}"
        d_str = f"+ {d_val}" if d_val > 0 else f"- {abs(d_val)}"
        e_str = f"+ {e}" if e > 0 else (f"- {abs(e)}" if e < 0 else "")

        eq_typst = f"{a}(x {b_str}) = {c}(x {d_str}) {e_str}".strip()
        ans_typst = f"x = {r}"

        c_exp = c * d_val + e
        c_exp_str = f"+ {c_exp}" if c_exp > 0 else f"- {abs(c_exp)}"
        a_b = a * b
        a_b_str = f"+ {a_b}" if a_b > 0 else f"- {abs(a_b)}"

        steps = [
            f"$ {eq_typst} $",
            f"Expand parentheses on both sides: $ {a}x {a_b_str} = {c}x {c_exp_str} $",
            f"Subtract {c}x from both sides: $ {a - c}x {a_b_str} = {c_exp} $",
            f"{'Subtract' if a_b > 0 else 'Add'} {abs(a_b)}: $ {a - c}x = {c_exp - a_b} $",
            f"Divide by {a - c}: $ x = {r} $",
        ]

        d1 = f"x = {-r}"
        d2 = f"x = {r + 2}"
        d3 = f"x = {r - 1}"

        return BaseProblem(
            id=f"multistep_spicy_{idx}",
            prompt_text="Solve each multi-step equation.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
        )
