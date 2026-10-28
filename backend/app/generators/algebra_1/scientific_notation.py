from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class ScientificNotationGenerator(BaseGenerator):
    generator_id = "algebra_1.scientific_notation"
    name = "Scientific Notation & Number Sets"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.8.EE.A.3", "CCSS.MATH.CONTENT.8.EE.A.4", "CCSS.MATH.CONTENT.HSN.RN.B.3"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            flavor = rng.choice(["to_scientific", "to_standard", "number_set"])
            if flavor == "to_scientific":
                lead = rng.randint(1, 9)
                dec = rng.randint(1, 9)
                power = rng.randint(3, 7)
                num = lead * (10 ** power) + dec * (10 ** (power - 1))
                q_text = f"Write {num:,} in scientific notation."
                ans_str = f"{lead}.{dec} * 10^{power}"
                distractors = [
                    f"{lead}{dec} * 10^{power - 1}",
                    f"{lead}.{dec} * 10^{power + 1}",
                    f"0.{lead}{dec} * 10^{power + 2}"
                ]
                steps = [
                    f"Place the decimal point after the first non-zero digit: $ {lead}.{dec} $.",
                    f"Count the number of places the decimal moved to the left: $ {power} $ places.",
                    f"Result: $ {ans_str} $."
                ]
            elif flavor == "to_standard":
                lead = rng.randint(2, 8)
                dec = rng.randint(1, 9)
                power = rng.randint(3, 5)
                val = lead * (10 ** power) + dec * (10 ** (power - 1))
                q_text = f"Write $ {lead}.{dec} * 10^{power} $ in standard notation."
                ans_str = f"{val:,}"
                distractors = [f"{val * 10:,}", f"{val // 10:,}", f"{val + 100:,}"]
                steps = [
                    f"The exponent is positive $ {power} $, move the decimal point $ {power} $ places to the right.",
                    f"Fill in zeros: $ {ans_str} $."
                ]
            else:
                num_type_map = [
                    ("-7", "Integer, Rational, Real", ["Natural, Whole, Real", "Irrational, Real", "Whole, Integer"]),
                    ("sqrt(2)", "Irrational, Real", ["Rational, Real", "Integer, Real", "Whole, Rational"]),
                    ("5", "Natural, Whole, Integer, Rational, Real", ["Integer, Real", "Irrational, Real", "Rational only"]),
                    ("3/4", "Rational, Real", ["Integer, Rational, Real", "Irrational, Real", "Whole, Real"]),
                ]
                n_str, correct_set, wrong_sets = rng.choice(num_type_map)
                q_text = f"Name the sets of numbers to which $ {n_str} $ belongs."
                ans_str = correct_set
                distractors = wrong_sets
                steps = [
                    f"Analyze $ {n_str} $.",
                    f"Classify into standard number sets: $ {ans_str} $."
                ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Negative exponents & small numbers
            lead = rng.randint(1, 9)
            dec = rng.randint(1, 9)
            neg_power = rng.randint(2, 5)
            q_text = f"Write $ {lead}.{dec} * 10^(-{neg_power}) $ in standard decimal notation."
            val_dec = f"0.{'0' * (neg_power - 1)}{lead}{dec}"
            ans_str = val_dec
            distractors = [
                f"0.{'0' * neg_power}{lead}{dec}",
                f"0.{'0' * max(0, neg_power - 2)}{lead}{dec}",
                f"-{lead}.{dec * 10}",
            ]
            steps = [
                f"Negative exponent $ -{neg_power} $ means moving the decimal point $ {neg_power} $ places to the left.",
                f"Standard form: $ {ans_str} $."
            ]

        else:  # SPICY
            # Multiplication & Division in scientific notation
            op = rng.choice(["multiply", "divide"])
            if op == "multiply":
                a = rng.choice([2.0, 3.0, 4.0])
                b = rng.choice([1.5, 2.0, 2.5])
                p1 = rng.randint(3, 7)
                p2 = rng.randint(2, 5)
                prod = round(a * b, 2)
                tot_p = p1 + p2
                q_text = f"Simplify: $ ({a} * 10^{p1}) * ({b} * 10^{p2}) $. Express your answer in scientific notation."
                ans_str = f"{prod} * 10^{tot_p}"
                distractors = [
                    f"{prod} * 10^{p1 * p2}",
                    f"{prod * 10} * 10^{tot_p - 1}",
                    f"{round(a + b, 1)} * 10^{tot_p}",
                ]
                steps = [
                    f"Multiply coefficients: $ {a} * {b} = {prod} $.",
                    f"Add exponents: $ 10^{p1} * 10^{p2} = 10^{p1 + p2} = 10^{tot_p} $.",
                    f"Combined scientific notation: $ {ans_str} $."
                ]
            else:
                prod = rng.choice([6.0, 8.0, 9.0])
                b = rng.choice([2.0, 3.0])
                a = round(prod / b, 1)
                p1 = rng.randint(6, 9)
                p2 = rng.randint(2, 4)
                tot_p = p1 - p2
                q_text = f"Simplify: $ ({prod} * 10^{p1}) / ({b} * 10^{p2}) $. Express your answer in scientific notation."
                ans_str = f"{a} * 10^{tot_p}"
                distractors = [
                    f"{a} * 10^{p1 + p2}",
                    f"{prod - b} * 10^{tot_p}",
                    f"{a * 10} * 10^{tot_p - 1}",
                ]
                steps = [
                    f"Divide coefficients: $ {prod} / {b} = {a} $.",
                    f"Subtract exponents: $ 10^{p1} / 10^{p2} = 10^{p1 - p2} = 10^{tot_p} $.",
                    f"Combined scientific notation: $ {ans_str} $."
                ]

        return BaseProblem(
            id=f"sci_not_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each problem involving scientific notation or number sets.",
            equation_typst=q_text,
            answer_typst=ans_str,
            steps_typst=steps,
            distractors=distractors,
            difficulty=difficulty,
            standards=self.standards,
            metadata={"problem": q_text}
        )
