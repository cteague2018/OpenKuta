from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class AbsoluteValueEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.absolute_value"
    name = "Absolute Value Equations"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.3", "CCSS.MATH.CONTENT.HSA.CED.A.1"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        var = "x"

        if difficulty == ProblemDifficulty.MILD:
            # |x + b| = c or |x - b| = c
            b = rng.randint(1, 9)
            sign = rng.choice(["+", "-"])
            c = rng.randint(3, 15)
            if sign == "+":
                eq_str = f"|{var} + {b}| = {c}"
                ans1 = c - b
                ans2 = -c - b
                step_pos = f"{var} + {b} = {c} ==> {var} = {ans1}"
                step_neg = f"{var} + {b} = -{c} ==> {var} = {ans2}"
            else:
                eq_str = f"|{var} - {b}| = {c}"
                ans1 = c + b
                ans2 = -c + b
                step_pos = f"{var} - {b} = {c} ==> {var} = {ans1}"
                step_neg = f"{var} - {b} = -{c} ==> {var} = {ans2}"

            roots = sorted([ans1, ans2])
            ans_str = f"{var} = {roots[0]}, {roots[1]}"
            distractors = [
                f"{var} = {roots[1]}",
                f"{var} = {-roots[0]}, {-roots[1]}",
                f"{var} = {roots[0] + 2}, {roots[1] - 2}",
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # |a x + b| = c
            a = rng.choice([2, 3, 4, 5])
            r1 = rng.randint(-6, 6)
            b = rng.randint(1, 9)
            c = abs(a * r1 + b)
            if c == 0:
                c = a * 2 + b

            r_pos = (c - b) // a if (c - b) % a == 0 else f"{(c - b)}/{a}"
            r_neg = (-c - b) // a if (-c - b) % a == 0 else f"{(-c - b)}/{a}"

            eq_str = f"|{a}{var} + {b}| = {c}"
            ans_str = f"{var} = {r_pos}, {r_neg}"
            step_pos = f"{a}{var} + {b} = {c} ==> {a}{var} = {c - b} ==> {var} = {r_pos}"
            step_neg = f"{a}{var} + {b} = -{c} ==> {a}{var} = {-c - b} ==> {var} = {r_neg}"
            distractors = [
                f"{var} = {r_pos}",
                f"{var} = {-r1 if isinstance(r1, int) else 2}",
                f"{var} = {c}, {-c}",
            ]

        else: # SPICY
            # Multi-step: d * |a x + b| - k = c
            d = rng.choice([2, 3])
            k = rng.randint(2, 8)
            inner_val = rng.randint(3, 9)
            target = d * inner_val - k
            b = rng.randint(1, 6)
            a = rng.choice([2, 3])

            c = inner_val
            r_pos = (c - b) // a if (c - b) % a == 0 else f"{(c - b)}/{a}"
            r_neg = (-c - b) // a if (-c - b) % a == 0 else f"{(-c - b)}/{a}"

            eq_str = f"{d}|{a}{var} + {b}| - {k} = {target}"
            ans_str = f"{var} = {r_pos}, {r_neg}"
            step_pos = f"Isolate absolute value: |{a}{var} + {b}| = ({target} + {k}) / {d} = {inner_val}"
            step_neg = f"Case 1: {a}{var} + {b} = {inner_val} ==> {var} = {r_pos}; Case 2: {a}{var} + {b} = -{inner_val} ==> {var} = {r_neg}"
            distractors = [
                f"{var} = {r_pos}",
                f"{var} = {inner_val}, {-inner_val}",
                f"{var} = {target // d}",
            ]

        steps = [
            f"$ {eq_str} $",
            f"Set up two linear cases: positive and negative.",
            f"Case 1: $ {step_pos} $",
            f"Case 2: $ {step_neg} $",
            f"Solution set: $ {ans_str} $"
        ]

        return BaseProblem(
            id=f"abs_val_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each absolute value equation.",
            equation_typst=f"$ {eq_str} $",
            answer_typst=f"$ {ans_str} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": eq_str}
        )
