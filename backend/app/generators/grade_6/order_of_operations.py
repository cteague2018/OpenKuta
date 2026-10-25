from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6OrderOfOperationsGenerator(BaseGenerator):
    generator_id = "grade_6.order_of_operations"
    name = "Order of Operations (PEMDAS / GEMDAS)"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.EE.A.1", "CCSS.MATH.CONTENT.6.EE.A.2"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # 2 operations: a + b * c or a * b - c / d
            a = rng.choice([2, 3, 4, 5, 6])
            b = rng.choice([3, 4, 5, 6])
            c = rng.choice([2, 3, 4])
            flavor = rng.choice(["add_mul", "sub_mul"])

            if flavor == "add_mul":
                prod = b * c
                total = a + prod
                eq_typst = f"{a} + {b} times {c}"
                ans_typst = f"{total}"
                steps = [
                    "Identify order of operations (PEMDAS): Multiplications before Additions.",
                    f"First multiply: $ {b} times {c} = {prod} $",
                    f"Then add: $ {a} + {prod} = {total} $",
                    f"Result: $ {ans_typst} $"
                ]
                d1 = f"{(a + b) * c}"  # added first
            else:
                prod = a * b
                total = prod - c
                eq_typst = f"{a} times {b} - {c}"
                ans_typst = f"{total}"
                steps = [
                    "Identify order of operations (PEMDAS): Multiplications before Subtractions.",
                    f"First multiply: $ {a} times {b} = {prod} $",
                    f"Then subtract: $ {prod} - {c} = {total} $",
                    f"Result: $ {ans_typst} $"
                ]
                d1 = f"{a * (b - c)}"  # subtracted first

            d2 = f"{total + 2}"
            d3 = f"{total - 1}"

            return BaseProblem(
                id=f"g6_pemdas_mild_{problem_idx}",
                prompt_text="Evaluate each expression using the order of operations.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[d1, d2, d3],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Parentheses and powers: a * (b + c) - d^2
            a = rng.choice([2, 3, 4])
            b = rng.choice([3, 5, 7])
            c = rng.choice([2, 4, 6])
            d = rng.choice([2, 3, 4])

            paren_sum = b + c
            mult_val = a * paren_sum
            exp_val = d ** 2
            total = mult_val - exp_val

            eq_typst = f"{a} times ({b} + {c}) - {d}^2"
            ans_typst = f"{total}"

            steps = [
                f"Evaluate inside Parentheses first: $ {b} + {c} = {paren_sum} $",
                f"Expression becomes: $ {a} times {paren_sum} - {d}^2 $",
                f"Evaluate Exponents: $ {d}^2 = {exp_val} $",
                f"Perform Multiplication: $ {a} times {paren_sum} = {mult_val} $",
                f"Perform Subtraction: $ {mult_val} - {exp_val} = {total} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"{a * paren_sum - d * 2}",  # multiplied exponent instead of power
                f"{(a * b + c) - exp_val}",
                f"{total + 4}"
            ]

            return BaseProblem(
                id=f"g6_pemdas_med_{problem_idx}",
                prompt_text="Evaluate each expression using the order of operations.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # Spicy: Nested operations [a + b * (c - d)] / e + f^2
            d = rng.choice([2, 3, 4])
            diff_cd = rng.choice([2, 3, 4])
            c = d + diff_cd
            b = rng.choice([2, 3, 4])
            prod_b = b * diff_cd
            e = rng.choice([2, 4])
            a = e * rng.choice([3, 4, 5]) - prod_b
            if a < 1:
                a = 2
                e = 2
            inner_bracket = a + prod_b
            div_val = inner_bracket // e
            f_base = rng.choice([2, 3])
            f_sq = f_base ** 2
            total = div_val + f_sq

            eq_typst = f"({a} + {b} times ({c} - {d})) / {e} + {f_base}^2"
            ans_typst = f"{total}"

            steps = [
                f"Evaluate innermost parentheses: $ {c} - {d} = {diff_cd} $",
                f"Multiply inside outer bracket: $ {b} times {diff_cd} = {prod_b} $",
                f"Add inside outer bracket: $ {a} + {prod_b} = {inner_bracket} $",
                f"Evaluate exponent: $ {f_base}^2 = {f_sq} $",
                f"Perform division: $ {inner_bracket} / {e} = {div_val} $",
                f"Perform final addition: $ {div_val} + {f_sq} = {total} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"{div_val + f_base * 2}",
                f"{(a + b) * diff_cd // e + f_sq}",
                f"{total - 3}"
            ]

            return BaseProblem(
                id=f"g6_pemdas_spicy_{problem_idx}",
                prompt_text="Evaluate each multi-step expression completely.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )

