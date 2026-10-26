from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeneralFunctionsGenerator(BaseGenerator):
    generator_id = "algebra_2.general_functions"
    name = "General Functions"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSF.BF.A.1", "CCSS.MATH.CONTENT.HSF.BF.B.4"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Evaluating a function f(x) = a x^2 + b x - c at x = k
            a = rng.choice([1, 2, 3])
            b = rng.randint(-4, 4)
            c = rng.randint(1, 8)
            k = rng.randint(-3, 4)
            val = a * (k ** 2) + b * k - c

            b_str = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
            f_str = f"f(x) = {a}x^2 {b_str} - {c}"
            q_str = f"Given $ {f_str} $, find $ f({k}) $."
            ans_str = f"f({k}) = {val}"
            distractors = [f"f({k}) = {val + 4}", f"f({k}) = {val - 6}", f"f({k}) = {-val}"]

            steps = [
                f"Substitute $ x = {k} $ into the function definition.",
                f"$ f({k}) = {a}({k})^2 {b_str.replace('x', f'({k})')} - {c} $.",
                f"Compute exponents and operations: $ {ans_str} $."
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Inverses of linear and rational functions: f(x) = a x + b ==> f^-1(x) = (x - b)/a
            a = rng.choice([2, 3, 4, 5])
            b = rng.randint(1, 9)
            sign = rng.choice(["+", "-"])

            f_str = f"f(x) = {a}x {sign} {b}"
            inv_sign = "-" if sign == "+" else "+"
            ans_str = f"f^(-1)(x) = (x {inv_sign} {b}) / {a}"
            q_str = f"Find the inverse of $ {f_str} $."
            distractors = [
                f"f^(-1)(x) = (x {sign} {b}) / {a}",
                f"f^(-1)(x) = {a}x {inv_sign} {b}",
                f"f^(-1)(x) = {b} - {a}x",
            ]

            steps = [
                f"Replace $ f(x) $ with $ y $: $ y = {a}x {sign} {b} $.",
                f"Swap $ x $ and $ y $: $ x = {a}y {sign} {b} $.",
                f"Solve for $ y $: $ y = (x {inv_sign} {b}) / {a} $.",
                f"Result: $ {ans_str} $."
            ]

        else: # SPICY
            # Function composition (f o g)(x)
            a = rng.choice([2, 3])
            b = rng.randint(1, 5)
            c = rng.choice([2, 4])
            q_str = f"If $ f(x) = {a}x + {b} $ and $ g(x) = x^2 - {c} $, find $ (f compose g)(x) $."
            # f(g(x)) = a(x^2 - c) + b = a x^2 - a*c + b
            const_term = -a * c + b
            s_const = f"+ {const_term}" if const_term >= 0 else f"- {abs(const_term)}"
            ans_str = f"{a}x^2 {s_const}"
            distractors = [
                f"{a}x^2 - {c + b}",
                f"({a}x + {b})^2 - {c}",
                f"{a}x^2 - {a * c - b}",
            ]

            steps = [
                f"By definition, $ (f compose g)(x) = f(g(x)) $.",
                f"Substitute $ g(x) = x^2 - {c} $ into $ f $: $ f(x^2 - {c}) = {a}(x^2 - {c}) + {b} $.",
                f"Distribute and simplify: $ {a}x^2 - {a * c} + {b} = {ans_str} $."
            ]

        return BaseProblem(
            id=f"func_{difficulty.value}_{problem_idx}",
            prompt_text="Perform the indicated function operation or find the inverse.",
            equation_typst=q_str,
            answer_typst=f"$ {ans_str} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"problem": q_str}
        )

