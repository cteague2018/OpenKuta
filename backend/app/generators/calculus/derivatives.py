from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class CalculusDerivativesGenerator(BaseGenerator):
    generator_id = "calculus.derivatives"
    name = "Differentiation Rules (Power, Product, Quotient, Chain)"
    category = "Calculus"
    standards = ["AP.CALC.FUN-2.A", "AP.CALC.FUN-2.B"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Power rule: f(x) = a x^n + b x^m
            a = rng.choice([2, 3, 4, 5, -2, -3])
            n = rng.choice([3, 4, 5])
            b = rng.choice([2, 3, 4, 6, -4, -5])
            m = rng.choice([1, 2])
            c = rng.choice([1, 5, 7, -3])

            eq_typst = f"f(x) = {a} x^{n} + {b} x^{m} + {c}"
            # derivative: a*n x^{n-1} + b*m x^{m-1}
            d1_coef = a * n
            d2_coef = b * m
            t1 = f"{d1_coef} x^{n-1}" if n-1 > 1 else f"{d1_coef} x"
            t2 = f"{d2_coef} x" if m-1 == 1 else f"{d2_coef}"
            sign2 = "+" if d2_coef > 0 else "-"
            ans_typst = f"f'(x) = {t1} {sign2} {abs(d2_coef)} x" if m-1 == 1 else f"f'(x) = {t1} {sign2} {abs(d2_coef)}"

            steps = [
                "Apply the Power Rule: $ (d)/(d x) [c x^n] = c dot n x^{n-1} $",
                f"Differentiate each term: $ (d)/(d x) [{a} x^{n}] = {d1_coef} x^{{n-1}} $",
                f"Differentiate second term: $ (d)/(d x) [{b} x^{m}] = {t2} $",
                f"Derivative of constant {c} is 0.",
                f"Combine terms: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_deriv_mild_{problem_idx}",
                prompt_text="Differentiate each function with respect to x.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"f'(x) = {a} x^{n-1} + {b}", f"f'(x) = {d1_coef} x^{n} + {d2_coef}"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Chain rule: f(x) = (a x^2 + b)^n
            a = rng.choice([2, 3, 4])
            b = rng.choice([1, 3, 5, -2, -4])
            n = rng.choice([3, 4, 5])
            eq_typst = f"f(x) = ({a} x^2 + {b})^{n}"
            # f'(x) = n (a x^2 + b)^{n-1} * (2a x) = (2 a n x)(a x^2 + b)^{n-1}
            outer_coef = 2 * a * n
            ans_typst = f"f'(x) = {outer_coef} x ({a} x^2 + {b})^{n-1}"

            steps = [
                f"Identify inner and outer functions: $ u = {a} x^2 + {b} $, $ f(u) = u^{n} $",
                "Apply Chain Rule: $ f'(x) = f'(u) dot u' $",
                f"Outer derivative: $ {n} u^{{n-1}} = {n} ({a} x^2 + {b})^{{n-1}} $",
                f"Inner derivative: $ u' = (d)/(d x) [{a} x^2 + {b}] = {2*a} x $",
                f"Multiply: $ f'(x) = {n} ({a} x^2 + {b})^{{n-1}} dot ({2*a} x) = {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_deriv_med_{problem_idx}",
                prompt_text="Differentiate each function with respect to x.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"f'(x) = {n} ({a} x^2 + {b})^{n-1}", f"f'(x) = {2*a} x ({a} x^2 + {b})^{n}"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # Product rule: f(x) = x^2 * sin(x) or (2x + 1) e^x
            k = rng.choice([2, 3, 4])
            eq_typst = f"f(x) = x^{k} e^x"
            ans_typst = f"f'(x) = x^{k-1} e^x (x + {k})"

            steps = [
                "Apply Product Rule: $ (u v)' = u' v + u v' $",
                f"Let $ u = x^{k} $ and $ v = e^x $",
                f"Calculate derivatives: $ u' = {k} x^{{k-1}} $, $ v' = e^x $",
                f"Assemble: $ f'(x) = {k} x^{{k-1}} e^x + x^{k} e^x $",
                f"Factor out $ x^{{k-1}} e^x $: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_deriv_spicy_{problem_idx}",
                prompt_text="Differentiate each function with respect to x.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"f'(x) = {k} x^{k-1} e^x", "f'(x) = x^k e^x"],
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )
