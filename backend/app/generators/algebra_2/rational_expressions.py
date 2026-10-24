from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Algebra2RationalExpressionsGenerator(BaseGenerator):
    generator_id = "algebra_2.rational_expressions"
    name = "Rational Expressions & Equations"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSA.APR.D.6", "CCSS.MATH.CONTENT.HSA.REI.A.2"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        a = rng.choice([2, 3, 4, 5])
        a_sq = a * a
        # Simplify (x^2 - a^2) / (x + a) = x - a
        eq_typst = f"(x^2 - {a_sq}) / (x + {a})"
        ans_typst = f"x - {a}"

        steps = [
            f"Factor the numerator as a difference of squares: $ x^2 - {a_sq} = (x - {a})(x + {a}) $",
            f"Write with factored numerator: $ ((x - {a})(x + {a})) / (x + {a}) $",
            f"Cancel common factor $ (x + {a}) $ for $ x != -{a} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"a2_rat_{problem_idx}",
            prompt_text="Simplify each rational expression. State any excluded values.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"x + {a}", f"x - {a_sq}", f"1 / (x - {a})"],
            difficulty=difficulty,
            standards=self.standards
        )
