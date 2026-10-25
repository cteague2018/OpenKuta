from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Algebra2LogarithmsGenerator(BaseGenerator):
    generator_id = "algebra_2.logarithms"
    name = "Exponential & Logarithmic Equations"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSF.LE.A.4"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        base = rng.choice([2, 3, 4, 5, 10])
        exponent = rng.choice([2, 3, 4])
        arg = base ** exponent

        if difficulty == ProblemDifficulty.MILD:
            # Evaluate log_b(x)
            eq_typst = f"log_{base}({arg})"
            ans_typst = f"{exponent}"

            steps = [
                "Recall definition of logarithm: $ log_b(x) = y <==> b^y = x $",
                f"Set equal to y: $ log_{base}({arg}) = y <==> {base}^y = {arg} $",
                f"Express {arg} as a power of {base}: $ {base}^{exponent} = {arg} $",
                f"Equate exponents: $ y = {exponent} $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"a2_log_mild_{problem_idx}",
                prompt_text="Evaluate each logarithmic expression.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{exponent + 1}", f"{base}", f"{exponent - 1}"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        else:
            # Solve log_b(2x - c) = exponent
            c = rng.choice([1, 3, 5])
            arg + c
            # let 2x = val ==> if val is odd, use x + c
            eq_typst = f"log_{base}(x - {c}) = {exponent}"
            x_val = arg + c
            ans_typst = f"x = {x_val}"

            steps = [
                f"Convert logarithmic equation to exponential form: $ x - {c} = {base}^{exponent} $",
                f"Evaluate power: $ {base}^{exponent} = {arg} $",
                f"Equation becomes: $ x - {c} = {arg} $",
                f"Add {c} to both sides: $ x = {arg} + {c} = {x_val} $",
                f"Check extraneous solutions: $ {x_val} - {c} = {arg} > 0 $ (valid).",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"a2_log_{difficulty.value}_{problem_idx}",
                prompt_text="Solve each logarithmic equation.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"x = {arg}", f"x = {arg - c}", f"x = {x_val + 2}"],
                difficulty=difficulty,
                standards=self.standards
            )
