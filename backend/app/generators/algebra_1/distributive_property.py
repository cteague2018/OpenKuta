from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class DistributivePropertyGenerator(BaseGenerator):
    generator_id = "algebra_1.distributive_property"
    name = "The Distributive Property"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.SSE.A.2", "CCSS.MATH.CONTENT.6.EE.A.3"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        var = "x"

        if difficulty == ProblemDifficulty.MILD:
            # a(b x + c)
            a = rng.randint(2, 6)
            b = rng.choice([1, 2, 3])
            c = rng.randint(2, 8)
            sign = rng.choice(["+", "-"])

            b_str = f"{b}{var}" if b > 1 else var
            eq_str = f"{a}({b_str} {sign} {c})"
            coeff1 = a * b
            coeff2 = a * c
            ans_str = f"{coeff1}{var} {sign} {coeff2}"

            distractors = [
                f"{coeff1}{var} {sign} {c}",  # Forgot to distribute to constant
                f"{b}{var} {sign} {coeff2}",  # Distributed only to constant
                f"{coeff1}{var} {'-' if sign == '+' else '+'} {coeff2}",
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # -a(b x - c) or a x(b x + c)
            flavor = rng.choice(["negative_multiplier", "variable_multiplier"])
            if flavor == "negative_multiplier":
                a = rng.randint(2, 5)
                b = rng.randint(2, 5)
                c = rng.randint(2, 7)
                sign = rng.choice(["+", "-"])

                eq_str = f"-{a}({b}{var} {sign} {c})"
                c1 = -a * b
                c2 = -a * c if sign == "+" else a * c
                s_c2 = f"+ {c2}" if c2 > 0 else f"- {abs(c2)}"
                ans_str = f"{c1}{var} {s_c2}"
                distractors = [
                    f"{c1}{var} {sign} {a * c}",
                    f"{a * b}{var} {sign} {a * c}",
                    f"{c1}{var} {sign} {c}",
                ]
            else:
                a = rng.randint(2, 4)
                b = rng.randint(2, 4)
                c = rng.randint(2, 6)
                sign = rng.choice(["+", "-"])

                eq_str = f"{a}{var}({b}{var} {sign} {c})"
                c1 = a * b
                c2 = a * c
                ans_str = f"{c1}{var}^2 {sign} {c2}{var}"
                distractors = [
                    f"{c1}{var}^2 {sign} {c2}",  # Forgot variable on second term
                    f"{c1}{var} {sign} {c2}{var}",
                    f"{a + b}{var}^2 {sign} {a + c}{var}",
                ]

        else:  # SPICY
            # a(b x + c) - d(e x - f)
            a = rng.randint(2, 4)
            b = rng.randint(2, 3)
            c = rng.randint(1, 5)
            d = rng.randint(2, 3)
            e = rng.choice([1, 2])
            f_val = rng.randint(1, 4)

            eq_str = f"{a}({b}{var} + {c}) - {d}({e}{var} - {f_val})"
            term1_x = a * b
            term1_c = a * c
            term2_x = -d * e
            term2_c = d * f_val

            tot_x = term1_x + term2_x
            tot_c = term1_c + term2_c
            s_c = f"+ {tot_c}" if tot_c >= 0 else f"- {abs(tot_c)}"
            ans_str = f"{tot_x}{var} {s_c}"

            distractors = [
                f"{tot_x}{var} + {term1_c - term2_c}",  # Sign error on second constant
                f"{term1_x + d * e}{var} {s_c}",
                f"{tot_x}{var} + {c + f_val}",
            ]

        if difficulty == ProblemDifficulty.MILD:
            steps = [
                f"Given expression: $ {eq_str} $",
                f"Distribute ${a}$ to each term inside parentheses: $ ({a}) dot ({b_str}) {sign} ({a}) dot ({c}) $",
                f"Multiply coefficients: $ {ans_str} $"
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            if flavor == "negative_multiplier":
                steps = [
                    f"Given expression: $ {eq_str} $",
                    f"Distribute ${-a}$ to each term inside parentheses: $ ({-a}) dot ({b}{var}) + ({-a}) dot ({c if sign == '+' else -c}) $",
                    f"Multiply and simplify signs: $ {ans_str} $"
                ]
            else:
                steps = [
                    f"Given expression: $ {eq_str} $",
                    f"Distribute monomial ${a}{var}$ to each term: $ ({a}{var}) dot ({b}{var}) {sign} ({a}{var}) dot ({c}) $",
                    f"Multiply coefficients and add exponents: $ {ans_str} $"
                ]
        else:  # SPICY
            s_t2x = f"- {abs(term2_x)}{var}" if term2_x < 0 else f"+ {term2_x}{var}"
            s_t2c = f"+ {term2_c}" if term2_c >= 0 else f"- {abs(term2_c)}"
            steps = [
                f"Given expression: $ {eq_str} $",
                f"Apply distributive property to clear parentheses: $ ({term1_x}{var} + {term1_c}) - ({d * e}{var} - {d * f_val}) $",
                f"Distribute negative sign: $ {term1_x}{var} + {term1_c} {s_t2x} {s_t2c} $",
                f"Group like terms: $ ({term1_x}{var} {s_t2x}) + ({term1_c} {s_t2c}) $",
                f"Combine like terms to simplify: $ {ans_str} $"
            ]

        return BaseProblem(
            id=f"distrib_{difficulty.value}_{problem_idx}",
            prompt_text="Simplify each expression using the distributive property.",
            equation_typst=f"$ {eq_str} $",
            answer_typst=f"$ {ans_str} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"expression": eq_str}
        )
