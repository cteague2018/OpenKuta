from __future__ import annotations

import math
import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class PythagoreanTheoremGenerator(BaseGenerator):
    generator_id = "geometry.pythagorean"
    name = "The Pythagorean Theorem & Right Triangles"
    category = "Geometry"
    standards = [
        "CCSS.MATH.CONTENT.8.G.B.7",
        "CCSS.MATH.CONTENT.HSG.SRT.C.8",
        "TEKS.MATH.8.7.C",
        "TEKS.MATH.G.9.B"
    ]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            return self._generate_pythagorean_triple(rng, problem_idx)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_find_leg(rng, problem_idx)
        else:
            return self._generate_radical_hypotenuse(rng, problem_idx)

    def _generate_pythagorean_triple(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Find the missing hypotenuse with exact integer triple (3-4-5, 5-12-13, 8-15-17)."""
        base_triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10)]
        a_base, b_base, c_base = rng.choice(base_triples)
        k = rng.choice([1, 2])
        a, b, c = a_base * k, b_base * k, c_base * k

        eq_typst = f"a = {a}, quad b = {b}, quad c = ?"
        ans_typst = f"c = {c}"

        d1 = f"c = {a + b}"  # added legs directly
        d2 = f"c = {c + 2}"
        d3 = f"c = {int(math.sqrt(abs(b**2 - a**2)))}" if b != a else f"c = {c + 1}"

        steps = [
            "Pythagorean Theorem: $ a^2 + b^2 = c^2 $",
            f"Substitute known legs: $ ({a})^2 + ({b})^2 = c^2 $",
            f"Calculate squares: $ {a*a} + {b*b} = {c*c} = c^2 $",
            f"Take the square root: $ c = sqrt({c*c}) = {c} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"pyth_mild_{problem_idx}",
            prompt_text="Find the missing side of each triangle. Round your answer to the nearest tenth if necessary.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"a": a, "b": b, "c": c}
        )

    def _generate_find_leg(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Given leg and hypotenuse, solve for the other leg."""
        base_triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15)]
        a_base, b_base, c_base = rng.choice(base_triples)
        k = rng.choice([1, 2])
        a, b, c = a_base * k, b_base * k, c_base * k

        eq_typst = f"a = {a}, quad c = {c}, quad b = ?"
        ans_typst = f"b = {b}"

        d1 = f"b = {c - a}"  # Subtracted without squaring
        d2 = f"b = {int(math.sqrt(c**2 + a**2))}"  # Added instead of subtracted
        d3 = f"b = {b + 1}"

        steps = [
            "Pythagorean Theorem: $ a^2 + b^2 = c^2 $",
            f"Substitute known side and hypotenuse: $ ({a})^2 + b^2 = ({c})^2 $",
            f"Isolate $ b^2 $: $ b^2 = {c*c} - {a*a} = {b*b} $",
            f"Take square root: $ b = sqrt({b*b}) = {b} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"pyth_med_{problem_idx}",
            prompt_text="Find the missing side of each right triangle.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"a": a, "b": b, "c": c}
        )

    def _generate_radical_hypotenuse(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Non-integer hypotenuse with radical simplification or decimal approximation."""
        a = rng.randint(3, 9)
        b = rng.randint(4, 11)
        c_sq = a * a + b * b

        # Exact radical simplification
        sq = 1
        for i in range(2, int(math.isqrt(c_sq)) + 1):
            if c_sq % (i * i) == 0:
                sq = i
        rad_rem = c_sq // (sq * sq)

        if sq > 1 and rad_rem > 1:
            exact_str = f"{sq} sqrt({rad_rem})"
        elif rad_rem == 1:
            exact_str = str(sq)
        else:
            exact_str = f"sqrt({c_sq})"

        dec_val = round(math.sqrt(c_sq), 1)

        eq_typst = f"a = {a}, quad b = {b}, quad c = ?"
        ans_typst = f"c = {exact_str} approx {dec_val}"

        d1 = f"c = {a + b}"
        d2 = f"c = approx {round(math.sqrt(abs(b**2 - a**2)), 1)}"
        d3 = f"c = approx {dec_val + 1.2}"

        steps = [
            f"Apply theorem: $ c^2 = a^2 + b^2 = ({a})^2 + ({b})^2 = {a*a} + {b*b} = {c_sq} $",
            f"Take square root: $ c = sqrt({c_sq}) $",
            f"Simplify radical: $ c = {exact_str} approx {dec_val} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"pyth_spicy_{problem_idx}",
            prompt_text="Find the missing side of each right triangle. Give exact simplified radical and decimal to nearest tenth.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"a": a, "b": b, "c_sq": c_sq}
        )

