from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class CalculusLimitsGenerator(BaseGenerator):
    generator_id = "calculus.limits"
    name = "Limits (Direct Evaluation, Factoring, Infinity)"
    category = "Calculus"
    standards = ["AP.CALC.LIM-1.A", "AP.CALC.LIM-1.B"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Direct substitution: lim_{x -> c} (a x^2 + b x + d)
            c = rng.choice([-3, -2, -1, 1, 2, 3, 4])
            a = rng.choice([1, 2, 3])
            b = rng.choice([-4, -2, 3, 5])
            d = rng.choice([-5, -1, 4, 7])

            eq_typst = f"$ lim_(x -> {c}) ({a} x^2 + {b} x + {d}) $"
            val = a * (c**2) + b * c + d
            ans_typst = f"{val}"

            steps = [
                "Check for continuity: Polynomials are continuous everywhere.",
                f"Use direct substitution: substitute $ x = {c} $",
                f"Evaluate terms: $ {a}({c})^2 + {b}({c}) + {d} $",
                f"Simplify: $ {a}({c**2}) + ({b*c}) + {d} = {val} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_limit_mild_{problem_idx}",
                prompt_text="Evaluate each limit.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{val + 2}", f"{val - 3}", "Does not exist"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        elif difficulty == ProblemDifficulty.MEDIUM:
            # 0/0 Indeterminate form resolved by factoring: lim_{x -> a} (x^2 - a^2) / (x - a)
            a = rng.choice([2, 3, 4, 5, -2, -3])
            a_sq = a * a
            eq_typst = f"$ lim_(x -> {a}) (x^2 - {a_sq}) / (x - {a}) $"
            ans_val = 2 * a
            ans_typst = f"{ans_val}"

            steps = [
                f"Direct substitution gives indeterminate form: $ ({a}^2 - {a_sq})/({a} - {a}) = 0/0 $",
                f"Factor the numerator as a difference of squares: $ (x - {a})(x + {a}) $",
                f"Cancel common factor $ (x - {a}) $ for $ x != {a} $: $ lim_(x -> {a}) (x + {a}) $",
                f"Substitute $ x = {a} $: $ {a} + {a} = {ans_val} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_limit_med_{problem_idx}",
                prompt_text="Evaluate each limit.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{a}", "0", "Does not exist"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # Limits at infinity: lim_{x -> oo} (a x^2 + b x) / (c x^2 + d)
            a = rng.choice([2, 3, 4, 6])
            c = rng.choice([2, 3, 4, 5])
            b = rng.choice([3, 5, -2])
            d = rng.choice([1, 7, -4])

            eq_typst = f"$ lim_(x -> oo) ({a} x^2 + {b} x) / ({c} x^2 + {d}) $"
            # Fraction simplification
            import math
            g = math.gcd(a, c)
            num = a // g
            den = c // g
            ans_typst = f"{num}/{den}" if den != 1 else f"{num}"

            steps = [
                "Both numerator and denominator have highest power of $ x^2 $.",
                f"Divide every term by $ x^2 $: $ lim_(x -> oo) ({a} + {b}/x) / ({c} + {d}/x^2) $",
                f"As $ x -> oo $, terms with $ 1/x $ approach 0: $ {b}/x -> 0 $ and $ {d}/x^2 -> 0 $",
                f"Evaluate remaining leading coefficients: $ {a} / {c} $",
                f"Reduce to lowest terms: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_limit_spicy_{problem_idx}",
                prompt_text="Evaluate each limit at infinity.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=["oo", "0", f"{a + 1}/{c}"],
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )
