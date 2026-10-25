from __future__ import annotations

import math
import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6FractionsDecimalsGenerator(BaseGenerator):
    generator_id = "grade_6.fractions_decimals"
    name = "Dividing Fractions & Decimal Arithmetic"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.NS.A.1", "CCSS.MATH.CONTENT.6.NS.B.3"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            return self._generate_mild(rng, problem_idx)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_medium(rng, problem_idx)
        else:
            return self._generate_spicy(rng, problem_idx)

    def _generate_mild(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Mild: Dividing fractions (a/b) div (c/d) = (a/b) * (d/c) with full cross-cancellation and reduced answer."""
        # Pick simplified fractions a/b and c/d
        fraction_pairs = [
            ((2, 3), (4, 9)),
            ((3, 4), (9, 8)),
            ((5, 6), (2, 3)),
            ((3, 5), (6, 25)),
            ((7, 8), (14, 16)),
            ((4, 5), (8, 15)),
            ((5, 8), (15, 16)),
            ((2, 7), (4, 21)),
            ((3, 10), (9, 20)),
            ((5, 12), (10, 3)),
            ((1, 4), (3, 8)),
            ((7, 10), (14, 15))
        ]
        (a, b), (c, d) = rng.choice(fraction_pairs)

        # Division: (a/b) / (c/d) = (a*d)/(b*c)
        num = a * d
        den = b * c
        g = math.gcd(num, den)
        s_num = num // g
        s_den = den // g

        ans_str = f"{s_num}/{s_den}" if s_den != 1 else f"{s_num}"
        eq_typst = f"({a}/{b}) div ({c}/{d})"
        ans_typst = f"{ans_str}"

        # Cross-cancellations between a & c, and d & b
        g1 = math.gcd(a, c)
        g2 = math.gcd(d, b)

        steps = [
            "Recall the rule for fraction division: multiply by the reciprocal of the divisor $ (a/b) div (c/d) = (a/b) dot (d/c) $.",
            f"Invert the second fraction and multiply: $ ({a}/{b}) dot ({d}/{c}) $",
        ]

        if g1 > 1 or g2 > 1:
            steps.append(
                f"Identify cross-cancellation opportunities: $ gcd({a}, {c}) = {g1} $ and $ gcd({b}, {d}) = {g2} $."
            )
            steps.append(
                f"Cross-cancel factors: $ ({a // g1}/{b // g2}) dot ({d // g2}/{c // g1}) $"
            )

        steps.append(f"Multiply across numerators and denominators: $ ({a} dot {d}) / ({b} dot {c}) = {num} / {den} $")

        if g > 1 and not (g1 * g2 == g):
            steps.append(f"Reduce to simplest form by dividing by $ gcd({num}, {den}) = {g} $: $ {ans_typst} $")
        else:
            steps.append(f"Result: $ {ans_typst} $")

        # Distractor 1: multiplied without reciprocating: (a*c)/(b*d)
        w_num = a * c
        w_den = b * d
        w_g = math.gcd(w_num, w_den)
        d1 = f"{w_num // w_g}/{w_den // w_g}" if w_den // w_g != 1 else f"{w_num // w_g}"

        # Distractor 2: inverted result
        d2 = f"{s_den}/{s_num}" if s_num != 1 else f"{s_den}"

        # Distractor 3: arithmetic variation
        d3 = f"{s_num + 1}/{s_den}" if s_den != 1 else f"{s_num + 1}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"{s_num + 2}/{s_den}")

        return BaseProblem(
            id=f"g6_frac_mild_{problem_idx}",
            prompt_text="Divide the fractions and simplify your answer completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"a": a, "b": b, "c": c, "d": d, "answer": ans_str}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Decimal addition/subtraction and multiplication with full intermediate steps."""
        op_type = rng.choice(["multiply", "add", "subtract"])

        if op_type == "multiply":
            n1 = rng.choice([1.2, 1.5, 2.4, 3.5, 0.8, 2.5, 0.75])
            n2 = rng.choice([0.4, 0.6, 1.2, 1.4, 2.2, 0.5])
            # Count decimal digits
            s1 = str(n1).split(".")
            s2 = str(n2).split(".")
            d1 = len(s1[1]) if len(s1) > 1 else 0
            d2 = len(s2[1]) if len(s2) > 1 else 0
            total_d = d1 + d2

            int1 = int(round(n1 * (10 ** d1)))
            int2 = int(round(n2 * (10 ** d2)))
            int_prod = int1 * int2
            prod_val = round(n1 * n2, total_d)

            eq_typst = f"{n1} times {n2}"
            ans_typst = f"{prod_val}"

            steps = [
                f"Ignore the decimal points and multiply as whole numbers: $ {int1} times {int2} = {int_prod} $",
                f"Count decimal places in the factors: $ {n1} $ has {d1} decimal place(s), and $ {n2} $ has {d2} decimal place(s).",
                f"Total decimal places: $ {d1} + {d2} = {total_d} $.",
                f"Place the decimal point {total_d} places from the right in $ {int_prod} $: $ {prod_val} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Multiply the decimals."
            d1_dist = f"{round(prod_val * 10, 4)}"
            d2_dist = f"{round(prod_val / 10, 4)}"
            d3_dist = f"{round(prod_val + 0.1, 4)}"

        elif op_type == "add":
            n1 = rng.choice([14.38, 12.65, 8.45, 23.7, 19.82])
            n2 = rng.choice([9.7, 7.82, 15.6, 4.28, 6.55])
            ans_val = round(n1 + n2, 2)

            eq_typst = f"{n1} + {n2}"
            ans_typst = f"{ans_val}"

            steps = [
                "Line up the numbers by their decimal points vertically.",
                f"Pad with trailing zeros if necessary: $ {n1:.2f} + {n2:.2f} $",
                "Add column by column starting from the rightmost place.",
                f"Bring down the decimal point into the answer: $ {ans_val} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Add the decimals."
            d1_dist = f"{round(ans_val + 1.0, 2)}"
            d2_dist = f"{round(ans_val - 0.1, 2)}"
            d3_dist = f"{round(n1 + n2 * 10, 2)}"

        else:  # subtract
            n1 = rng.choice([25.4, 31.2, 18.65, 42.1, 20.05])
            n2 = rng.choice([8.65, 14.7, 9.38, 15.45, 7.8])
            while n2 >= n1:
                n1 += 10.0
            ans_val = round(n1 - n2, 2)

            eq_typst = f"{n1} - {n2}"
            ans_typst = f"{ans_val}"

            steps = [
                "Line up the numbers by their decimal points vertically.",
                f"Pad with trailing zeros if necessary: $ {n1:.2f} - {n2:.2f} $",
                "Subtract column by column from right to left, regrouping (borrowing) as necessary.",
                f"Bring down the decimal point into the answer: $ {ans_val} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Subtract the decimals."
            d1_dist = f"{round(ans_val + 1.0, 2)}"
            d2_dist = f"{round(ans_val - 0.1, 2)}"
            d3_dist = f"{round(n1 - n2 / 10, 2)}"

        distractors = list(dict.fromkeys([d1_dist, d2_dist, d3_dist]))
        while len(distractors) < 2:
            distractors.append(f"{round(float(ans_typst) + 2.0, 2)}")

        return BaseProblem(
            id=f"g6_dec_med_{problem_idx}",
            prompt_text=prompt,
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"op": op_type, "answer": ans_typst}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Dividing decimals (e.g. 4.8 div 0.6 = 8, moving the decimal point in divisor and dividend)."""
        # Pick divisor with 1 or 2 decimal places, and a clean quotient
        cases = [
            (0.6, 8, 4.8),
            (0.4, 15, 6.0),
            (0.8, 12, 9.6),
            (0.5, 14, 7.0),
            (0.9, 8.4, 7.56),
            (1.2, 7.5, 9.0),
            (1.5, 6, 9.0),
            (0.25, 15, 3.75),
            (0.12, 45, 5.4),
            (0.3, 42, 12.6),
            (0.05, 36, 1.8),
            (0.15, 24, 3.6),
            (0.7, 13, 9.1)
        ]
        divisor, quotient, dividend = rng.choice(cases)

        # Count decimal places in divisor
        s_div = str(divisor).split(".")
        d_places = len(s_div[1]) if len(s_div) > 1 else 0
        multiplier = 10 ** d_places

        shifted_divisor = int(round(divisor * multiplier))
        shifted_dividend_num = round(dividend * multiplier, 4)
        shifted_dividend = int(shifted_dividend_num) if shifted_dividend_num.is_integer() else shifted_dividend_num

        quotient_str = f"{int(quotient)}" if float(quotient).is_integer() else f"{quotient}"
        dividend_str = f"{int(dividend)}" if float(dividend).is_integer() else f"{dividend}"

        eq_typst = f"{dividend_str} div {divisor}"
        ans_typst = f"{quotient_str}"

        steps = [
            f"Identify the decimal places in the divisor: $ {divisor} $ has {d_places} decimal place(s).",
            f"Multiply both dividend and divisor by $ {multiplier} $ (move the decimal point {d_places} place(s) to the right):",
            f"$ ({dividend_str} times {multiplier}) div ({divisor} times {multiplier}) = {shifted_dividend} div {shifted_divisor} $",
            f"Divide the resulting numbers: $ {shifted_dividend} div {shifted_divisor} = {quotient_str} $",
            f"Verify by multiplication: $ {quotient_str} times {divisor} = {dividend_str} $",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: forgot to shift dividend (dividend / shifted_divisor)
        d1_val = round(dividend / shifted_divisor, 3)
        d1 = f"{d1_val}"
        # Distractor 2: off by power of 10
        d2 = f"{round(float(quotient) * 10, 2)}"
        # Distractor 3: arithmetic variation
        d3 = f"{round(float(quotient) + 2.0, 2)}" if not float(quotient).is_integer() else f"{int(quotient) + 2}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"{float(quotient) + 1.0}")

        return BaseProblem(
            id=f"g6_dec_spicy_{problem_idx}",
            prompt_text="Divide the decimals.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"dividend": dividend, "divisor": divisor, "quotient": quotient}
        )
