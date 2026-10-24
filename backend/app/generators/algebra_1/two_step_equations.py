from __future__ import annotations

import random
from typing import List
import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class TwoStepEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.two_step"
    name = "Two-Step Linear Equations"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.7.EE.B.4",
        "CCSS.MATH.CONTENT.7.EE.B.4.A",
        "CCSS.MATH.CONTENT.HSA.REI.B.3",
        "TEKS.MATH.7.11.A",
        "TEKS.MATH.8.8.C"
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
            return self._generate_mild(rng, problem_idx, allow_negatives)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_medium(rng, problem_idx, allow_negatives)
        else:
            return self._generate_spicy(rng, problem_idx, allow_negatives)

    def _generate_mild(self, rng: random.Random, problem_idx: int, allow_negatives: bool) -> BaseProblem:
        """Standard two-step: a*x + b = c with positive integers and integer solution."""
        r = rng.randint(2, 9)
        a = rng.randint(2, 7)
        b = rng.randint(1, 15)
        c = a * r + b

        eq_typst = f"{a}x + {b} = {c}"
        ans_typst = f"x = {r}"

        # Distractors targeting specific student misconceptions:
        # Misconception 1: Added b instead of subtracting b: (c + b) / a
        d1 = f"x = {(c + b) // a}" if (c + b) % a == 0 else f"x = {c + b}/{a}"
        # Misconception 2: Multiplied instead of divided by a: a * (c - b)
        d2 = f"x = {a * (c - b)}"
        # Misconception 3: Divided c by a before subtracting b
        d3 = f"x = {c - b}"

        steps = [
            f"$ {eq_typst} $",
            f"Subtract {b} from both sides: $ {a}x = {c} - {b} = {c - b} $",
            f"Divide both sides by {a}: $ x = ({c - b}) / {a} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"twostep_mild_{problem_idx}",
            prompt_text="Solve each two-step equation.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"a": a, "b": b, "c": c, "root": r}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int, allow_negatives: bool) -> BaseProblem:
        """Two-step with negatives and division: x/a + b = c or -a*x + b = c."""
        flavor = rng.choice(["fraction", "negative_coeff"])

        if flavor == "fraction":
            a = rng.choice([2, 3, 4, 5, 6])
            r = rng.randint(-8, 8) if allow_negatives else rng.randint(2, 9)
            if r == 0:
                r = 4
            b = rng.randint(-12, 12) if allow_negatives else rng.randint(2, 12)
            if b == 0:
                b = 3
            c = (r // a) + b if r % a == 0 else (r * a) + b  # ensure clean
            # Let's ensure r is divisible by a:
            k = rng.randint(-6, 6) if allow_negatives else rng.randint(1, 6)
            if k == 0:
                k = 2
            r = k * a
            c = k + b

            b_str = f"+ {b}" if b > 0 else f"- {abs(b)}"
            eq_typst = f"x/{a} {b_str} = {c}"
            ans_typst = f"x = {r}"

            # Misconceptions:
            # Did not multiply by a, or divided instead:
            d1 = f"x = {(c - b) // a if (c - b) % a == 0 else (c - b)}"
            # Added b instead:
            d2 = f"x = {a * (c + b)}"
            d3 = f"x = {-r}"

            steps = [
                f"$ {eq_typst} $",
                f"Isolate the fraction by {'subtracting' if b > 0 else 'adding'} {abs(b)}: $ x/{a} = {c - b} $",
                f"Multiply both sides by {a}: $ x = ({c - b}) dot {a} = {(c - b) * a} $",
                f"Result: $ {ans_typst} $"
            ]
        else:
            # -a*x + b = c
            a = rng.choice([-5, -4, -3, -2])
            r = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)
            b = rng.randint(1, 15)
            c = a * r + b

            eq_typst = f"{a}x + {b} = {c}"
            ans_typst = f"x = {r}"

            d1 = f"x = {-r}"  # Forgot negative when dividing by a
            d2 = f"x = {(c + b) // a if (c + b) % a == 0 else (c + b)}"
            d3 = f"x = {r + 2}"

            steps = [
                f"$ {eq_typst} $",
                f"Subtract {b} from both sides: $ {a}x = {c - b} $",
                f"Divide both sides by {a} (remember sign rule): $ x = ({c - b}) / ({a}) $",
                f"Result: $ {ans_typst} $"
            ]

        return BaseProblem(
            id=f"twostep_med_{problem_idx}",
            prompt_text="Solve each equation.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"flavor": flavor, "root": r}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int, allow_negatives: bool) -> BaseProblem:
        """Variables on both sides: a*x + b = c*x + d or distributive a(x + b) = c."""
        # Distributive form: a(x + b) = c
        a = rng.choice([3, 4, 5, -2, -3])
        r = rng.randint(-7, 7) if allow_negatives else rng.randint(1, 8)
        if r == 0:
            r = 3
        b = rng.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
        c = a * (r + b)

        b_sign = f"+ {b}" if b > 0 else f"- {abs(b)}"
        eq_typst = f"{a}(x {b_sign}) = {c}"
        ans_typst = f"x = {r}"

        # Distractor misconceptions:
        # 1. Distribute error: distributed only to x and not to b: a*x + b = c => x = (c - b)/a
        d1 = f"x = {(c - b) // a if (c - b) % a == 0 else (c - b)}"
        # 2. Subtract b before divide without expanding: x = c - b
        d2 = f"x = {c - b}"
        # 3. Sign confusion on b
        d3 = f"x = {r - 2 * b}"

        steps = [
            f"$ {eq_typst} $",
            f"Divide both sides by {a}: $ x {b_sign} = {c} / {a} = {c // a} $",
            f"{'Subtract' if b > 0 else 'Add'} {abs(b)} from both sides: $ x = {c // a} {'-' if b > 0 else '+'} {abs(b)} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"twostep_spicy_{problem_idx}",
            prompt_text="Solve each multi-step equation.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"a": a, "b": b, "c": c, "root": r}
        )
