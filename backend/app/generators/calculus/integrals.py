from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class CalculusIntegralsGenerator(BaseGenerator):
    generator_id = "calculus.integrals"
    name = "Indefinite & Definite Integration"
    category = "Calculus"
    standards = ["AP.CALC.FUN-6.A", "AP.CALC.FUN-6.B"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        if difficulty == ProblemDifficulty.MILD:
            # Indefinite integral: int (a x^n + b x + c) dx
            n = rng.choice([2, 3])
            a = rng.choice([3, 4, 6]) * (n + 1)
            b = rng.choice([2, 4, 6]) * 2
            c = rng.choice([1, 2, 5, -3])

            eq_typst = f"integral ({a} x^{n} + {b} x + {c}) dif x"
            c1 = a // (n + 1)
            c2 = b // 2
            ans_typst = f"{c1} x^{n+1} + {c2} x^2 + {c} x + C"

            steps = [
                f"Apply the reverse power rule: $ integral x^k dif x = (x^{{k+1}}) / (k + 1) $",
                f"Integrate first term: $ integral {a} x^{n} dif x = {a} dot (x^{{n+1}})/({n+1}) = {c1} x^{{n+1}} $",
                f"Integrate second term: $ integral {b} x dif x = {b} dot (x^2)/2 = {c2} x^2 $",
                f"Integrate constant term: $ integral {c} dif x = {c} x $",
                f"Add constant of integration: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_int_mild_{problem_idx}",
                prompt_text="Evaluate each indefinite integral.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{c1} x^{n} + {c2} x + C", f"{a} x^{n+1} + {b} x^2 + C"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Definite integral: int_0^b (3 x^2 + 2x) dx
            b = rng.choice([2, 3, 4])
            eq_typst = f"integral_0^{b} (3 x^2 + 2 x) dif x"
            val = (b**3) + (b**2)
            ans_typst = f"{val}"

            steps = [
                f"Find the antiderivative: $ F(x) = x^3 + x^2 $",
                f"Apply First Fundamental Theorem of Calculus: $ [F(x)]_0^{b} = F({b}) - F(0) $",
                f"Evaluate at upper limit: $ F({b}) = ({b})^3 + ({b})^2 = {b**3} + {b**2} = {val} $",
                f"Evaluate at lower limit: $ F(0) = 0 $",
                f"Subtract: $ {val} - 0 = {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_int_med_{problem_idx}",
                prompt_text="Evaluate each definite integral.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{val - 2}", f"{val + 4}", f"{b**3}"],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # U-substitution: int 2x (x^2 + a)^n dx
            a = rng.choice([1, 2, 3, 4])
            n = rng.choice([3, 4])
            eq_typst = f"integral 2 x (x^2 + {a})^{n} dif x"
            ans_typst = f"((x^2 + {a})^{n+1}) / ({n+1}) + C"

            steps = [
                f"Use u-substitution: let $ u = x^2 + {a} $",
                f"Compute differential: $ dif u = 2 x dif x $",
                f"Substitute into integral: $ integral u^{n} dif u $",
                f"Evaluate integral in terms of u: $ (u^{{n+1}}) / ({n+1}) + C $",
                f"Substitute back $ u = x^2 + {a} $: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"calc_int_spicy_{problem_idx}",
                prompt_text="Evaluate each indefinite integral using substitution.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"((x^2 + {a})^{n}) / {n} + C", f"2 (x^2 + {a})^{n+1} + C"],
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )
