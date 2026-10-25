from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class LogPropertiesGenerator(BaseGenerator):
    generator_id = "algebra_2.log_properties"
    name = "Properties of Logarithms (Expanding & Condensing)"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSF.BF.B.5", "CCSS.MATH.CONTENT.HSF.LE.A.4"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        b = rng.choice([2, 3, 5, ""])
        base_sub = f"_{b}" if b != "" else ""

        if difficulty == ProblemDifficulty.MILD:
            # Expanding product or quotient: log(x * y) or log(x / y)
            is_prod = rng.choice([True, False])
            if is_prod:
                eq_typst = f"log{base_sub}(x y)"
                ans_typst = f"log{base_sub}(x) + log{base_sub}(y)"
                rule_name = "Product Property: $ log_b(u v) = log_b(u) + log_b(v) $"
            else:
                eq_typst = f"log{base_sub}(x / y)"
                ans_typst = f"log{base_sub}(x) - log{base_sub}(y)"
                rule_name = "Quotient Property: $ log_b(u / v) = log_b(u) - log_b(v) $"

            steps = [
                f"Recall logarithmic property: {rule_name}",
                f"Apply property: $ {ans_typst} $"
            ]

            distractors = [
                f"log{base_sub}(x) dot log{base_sub}(y)",
                f"log{base_sub}(x + y)",
                f"log{base_sub}(x) - log{base_sub}(y)" if is_prod else f"log{base_sub}(x) + log{base_sub}(y)"
            ]

            return BaseProblem(
                id=f"a2_logprop_mild_{problem_idx}",
                prompt_text="Expand each expression completely.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Expand with power and quotient: log(x^p / y^q) = p log(x) - q log(y)
            p = rng.choice([2, 3, 4])
            q = rng.choice([2, 3, 5])
            eq_typst = f"log{base_sub}((x^{p}) / (y^{q}))"
            ans_typst = f"{p} log{base_sub}(x) - {q} log{base_sub}(y)"

            steps = [
                f"Apply Quotient Property: $ log{base_sub}(x^{p}) - log{base_sub}(y^{q}) $",
                "Apply Power Property: $ log_b(u^k) = k dot log_b(u) $",
                f"Bring powers in front: $ {p} log{base_sub}(x) - {q} log{base_sub}(y) $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"{p} log{base_sub}(x) + {q} log{base_sub}(y)",
                f"log{base_sub}(x^{p} - y^{q})",
                f"{p*q} log{base_sub}(x / y)"
            ]

            return BaseProblem(
                id=f"a2_logprop_med_{problem_idx}",
                prompt_text="Expand each expression using logarithmic properties.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # Spicy: Condensing multi-term logarithmic expression: a log(x) + b log(y) - c log(z) => log((x^a y^b)/z^c)
            a = rng.choice([2, 3])
            b_pow = rng.choice([2, 4])
            c = rng.choice([2, 3])

            eq_typst = f"{a} log{base_sub}(x) + {b_pow} log{base_sub}(y) - {c} log{base_sub}(z)"
            ans_typst = f"log{base_sub}((x^{a} y^{b_pow}) / (z^{c}))"

            steps = [
                f"Apply Power Property in reverse to exponents: $ log{base_sub}(x^{a}) + log{base_sub}(y^{b_pow}) - log{base_sub}(z^{c}) $",
                f"Combine addition using Product Property: $ log{base_sub}(x^{a} y^{b_pow}) - log{base_sub}(z^{c}) $",
                f"Combine subtraction using Quotient Property: $ log{base_sub}((x^{a} y^{b_pow}) / (z^{c})) $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"log{base_sub}(x^{a} + y^{b_pow} - z^{c})",
                f"log{base_sub}((x^{a}) / (y^{b_pow} z^{c}))",
                f"{a + b_pow - c} log{base_sub}((x y) / z)"
            ]

            return BaseProblem(
                id=f"a2_logprop_spicy_{problem_idx}",
                prompt_text="Condense each logarithmic expression into a single quantity.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )

