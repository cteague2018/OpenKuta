from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6IntegersGenerator(BaseGenerator):
    generator_id = "grade_6.integers"
    name = "Operations with Integers (Adding, Subtracting, Multiplying & Dividing)"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.7.NS.A.1", "CCSS.MATH.CONTENT.7.NS.A.2", "CCSS.MATH.CONTENT.6.NS.C.5"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Adding and subtracting integers
            op = rng.choice(["add", "sub"])
            a = rng.randint(-15, 15)
            b = rng.randint(-15, 15)
            while a == 0 or b == 0:
                a = rng.randint(-12, 12)
                b = rng.randint(-12, 12)

            if op == "add":
                total = a + b
                b_str = f"({b})" if b < 0 else str(b)
                a_str = f"({a})" if a < 0 else str(a)
                eq_typst = f"{a_str} + {b_str}"
                ans_typst = f"{total}"
                if (a > 0 and b > 0) or (a < 0 and b < 0):
                    reason = "Same signs: add the absolute values and keep the common sign."
                else:
                    reason = "Different signs: find difference of absolute values and keep sign of larger magnitude."

                steps = [
                    f"Expression: $ {eq_typst} $",
                    reason,
                    f"Compute sum: $ {ans_typst} $"
                ]
            else:
                total = a - b
                b_str = f"({b})" if b < 0 else str(b)
                a_str = f"({a})" if a < 0 else str(a)
                eq_typst = f"{a_str} - {b_str}"
                ans_typst = f"{total}"
                opp_b = -b
                steps = [
                    f"Expression: $ {eq_typst} $",
                    f"Subtracting a number is the same as adding its opposite: $ {a_str} + ({opp_b}) $",
                    f"Compute difference: $ {ans_typst} $"
                ]

            distractors = [f"{-total}", f"{total + 2}", f"{total - 2}"]

            return BaseProblem(
                id=f"g6_int_mild_{problem_idx}",
                prompt_text="Evaluate each expression.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Multiplying and dividing integers
            op = rng.choice(["mul", "div"])
            if op == "mul":
                a = rng.choice([-9, -8, -7, -6, -5, -4, -3, 3, 4, 5, 6, 7, 8, 9])
                b = rng.choice([-8, -7, -6, -5, -4, -3, 3, 4, 5, 6, 7, 8])
                total = a * b
                a_str = f"({a})" if a < 0 else str(a)
                b_str = f"({b})" if b < 0 else str(b)
                eq_typst = f"{a_str} dot {b_str}"
                ans_typst = f"{total}"
                sign_rule = "The product of two negative numbers is POSITIVE." if (a < 0 and b < 0) else "The product of positive and negative is NEGATIVE." if (a * b < 0) else "Positive times positive is POSITIVE."
                steps = [
                    f"Expression: $ {eq_typst} $",
                    f"Rule of signs: {sign_rule}",
                    f"Calculate magnitude: $ |{a}| dot |{b}| = {abs(a)} dot {abs(b)} = {abs(total)} $",
                    f"Apply sign: $ {ans_typst} $"
                ]
            else:
                divisor = rng.choice([-8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8])
                quotient = rng.choice([-9, -8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9])
                dividend = divisor * quotient
                d_str = f"({divisor})" if divisor < 0 else str(divisor)
                eq_typst = f"({dividend}) / {d_str}"
                ans_typst = f"{quotient}"
                sign_rule = "Dividing two numbers with the SAME sign yields a POSITIVE result." if quotient > 0 else "Dividing two numbers with DIFFERENT signs yields a NEGATIVE result."
                steps = [
                    f"Expression: $ {eq_typst} $",
                    f"Rule of signs: {sign_rule}",
                    f"Calculate magnitude: $ |{dividend}| / |{divisor}| = {abs(dividend)} / {abs(divisor)} = {abs(quotient)} $",
                    f"Apply sign: $ {ans_typst} $"
                ]

            distractors = [f"{-total if op == 'mul' else -quotient}", f"{total + 1 if op == 'mul' else quotient + 1}"]

            return BaseProblem(
                id=f"g6_int_med_{problem_idx}",
                prompt_text="Find each product or quotient.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # 3-term combined integer evaluation: a * b - c / d + e
            b = rng.choice([-4, -3, -2, 2, 3, 4])
            a = rng.choice([-6, -5, -4, 4, 5, 6])
            ab = a * b
            d = rng.choice([-3, -2, 2, 3])
            q = rng.choice([-5, -4, -3, 3, 4, 5])
            c = d * q
            e = rng.choice([-7, -5, -3, 3, 5, 7])
            total = ab - q + e

            a_s = f"({a})" if a < 0 else str(a)
            b_s = f"({b})" if b < 0 else str(b)
            c_s = f"({c})" if c < 0 else str(c)
            d_s = f"({d})" if d < 0 else str(d)
            e_s = f"+ ({e})" if e < 0 else f"+ {e}"

            eq_typst = f"{a_s} dot {b_s} - ({c_s} / {d_s}) {e_s}"
            ans_typst = f"{total}"

            steps = [
                f"Expression: $ {eq_typst} $",
                f"Perform multiplication first: $ {a_s} dot {b_s} = {ab} $",
                f"Perform division second: $ {c_s} / {d_s} = {q} $",
                f"Expression simplifies to: $ {ab} - ({q}) + ({e}) $",
                f"Evaluate left to right: $ ({ab - q}) + ({e}) = {total} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [f"{-total}", f"{total + 4}", f"{total - 4}"]

            return BaseProblem(
                id=f"g6_int_spicy_{problem_idx}",
                prompt_text="Evaluate each multi-operation expression completely.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )
