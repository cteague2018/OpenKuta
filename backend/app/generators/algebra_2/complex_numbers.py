from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class Algebra2ComplexNumbersGenerator(BaseGenerator):
    generator_id = "algebra_2.complex_numbers"
    name = "Complex Numbers Operations"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSN.CN.A.1", "CCSS.MATH.CONTENT.HSN.CN.A.2"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        a = rng.choice([2, 3, 4, 5, -2, -3])
        b = rng.choice([2, 3, 4, 6, -3, -5])
        c = rng.choice([1, 2, 3, 4, -1, -4])
        d = rng.choice([2, 3, 5, -2, -4])

        b_sign = "+" if b >= 0 else "-"
        d_sign = "+" if d >= 0 else "-"

        if difficulty == ProblemDifficulty.MILD:
            # Addition / subtraction: (a + bi) + (c + di)
            eq_typst = f"({a} {b_sign} {abs(b)} i) + ({c} {d_sign} {abs(d)} i)"
            real_part = a + c
            imag_part = b + d
            ans_sign = "+" if imag_part >= 0 else "-"
            ans_typst = f"{real_part} {ans_sign} {abs(imag_part)} i"

            steps = [
                f"Combine real parts: $ ({a}) + ({c}) = {real_part} $",
                f"Combine imaginary parts: $ ({b} i) + ({d} i) = ({b + d}) i $",
                f"Write in standard form a + bi: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"a2_cplx_mild_{problem_idx}",
                prompt_text="Simplify each expression into standard a + bi form.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{real_part + 2} {ans_sign} {abs(imag_part)} i", f"{a - c} + {b - d} i"],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Multiplication: (a + bi)(c + di) = (ac - bd) + (ad + bc)i
            eq_typst = f"({a} {b_sign} {abs(b)} i)({c} {d_sign} {abs(d)} i)"
            real_part = a * c - b * d
            imag_part = a * d + b * c
            ans_sign = "+" if imag_part >= 0 else "-"
            ans_typst = f"{real_part} {ans_sign} {abs(imag_part)} i"

            steps = [
                f"Use FOIL to expand terms: $ ({a})({c}) + ({a})({d} i) + ({b} i)({c}) + ({b} i)({d} i) $",
                f"Calculate products: $ {a*c} + ({a*d}) i + ({b*c}) i + ({b*d}) i^2 $",
                f"Substitute $ i^2 = -1 $: $ ({b*d})(-1) = {-b*d} $",
                f"Combine real parts: $ {a*c} - ({b*d}) = {real_part} $",
                f"Combine imaginary parts: $ ({a*d} + {b*c}) i = {imag_part} i $",
                f"Result: $ {ans_typst} $"
            ]

            return BaseProblem(
                id=f"a2_cplx_med_{problem_idx}",
                prompt_text="Simplify each expression into standard a + bi form.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{a*c + b*d} {ans_sign} {abs(imag_part)} i", f"{real_part} - {abs(imag_part)} i", f"{real_part + 2} + {abs(imag_part)} i"],
                difficulty=difficulty,
                standards=self.standards
            )
        else:
            # Spicy: Complex division or squaring with conjugate: (r + q*i)*(c + d*i) / (c + d*i) = r + q*i
            r_ans = rng.choice([-4, -3, -2, 2, 3, 4])
            q_ans = rng.choice([-5, -3, -2, 2, 3, 5])
            c_den = rng.choice([1, 2, 3])
            d_den = rng.choice([1, 2, -1, -2])
            num_r = r_ans * c_den - q_ans * d_den
            num_i = r_ans * d_den + q_ans * c_den
            den_norm = c_den * c_den + d_den * d_den
            nr_sign = "+" if num_i >= 0 else "-"
            dd_sign = "+" if d_den >= 0 else "-"
            ans_sign = "+" if q_ans >= 0 else "-"
            eq_typst = f"({num_r} {nr_sign} {abs(num_i)} i) / ({c_den} {dd_sign} {abs(d_den)} i)"
            ans_typst = f"{r_ans} {ans_sign} {abs(q_ans)} i"
            conj_sign = "-" if d_den >= 0 else "+"
            steps = [
                f"Multiply numerator and denominator by the complex conjugate $ ({c_den} {conj_sign} {abs(d_den)} i) $.",
                f"Denominator becomes $ ({c_den})^2 + ({abs(d_den)})^2 = {den_norm} $.",
                f"Expand numerator: $ {r_ans * den_norm} + ({q_ans * den_norm}) i $.",
                f"Divide real and imaginary parts by {den_norm}: $ {ans_typst} $"
            ]
            return BaseProblem(
                id=f"a2_cplx_spicy_{problem_idx}",
                prompt_text="Divide and simplify into standard a + bi form.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[f"{-r_ans} {ans_sign} {abs(q_ans)} i", f"{r_ans} {'-' if q_ans >= 0 else '+'} {abs(q_ans)} i", f"{r_ans + 1} {ans_sign} {abs(q_ans)} i"],
                difficulty=difficulty,
                standards=self.standards
            )
