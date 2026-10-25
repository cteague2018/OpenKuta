from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class LinearInequalitiesGenerator(BaseGenerator):
    generator_id = "algebra_1.inequalities"
    name = "Linear Inequalities (One-Step, Multi-Step & Compound)"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.3", "TEKS.MATH.A1.5.B"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        symbols = ["<", "<=", ">", ">="]
        opp_symbols = {"<": ">", "<=": ">=", ">": "<", ">=": "<="}

        if difficulty == ProblemDifficulty.MILD:
            # Two-step inequality: ax + b < c
            sym = rng.choice(symbols)
            a = rng.choice([2, 3, 4, 5, -2, -3, -4])
            x_boundary = rng.randint(-8, 8)
            b = rng.randint(-12, 12)
            c = a * x_boundary + b

            b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
            eq_typst = f"{a} x {b_str} {sym} {c}"

            # If dividing by negative, flip inequality sign
            res_sym = opp_symbols[sym] if a < 0 else sym
            ans_typst = f"x {res_sym} {x_boundary}"

            flip_note = "Dividing by a NEGATIVE number FLIPS the inequality sign!" if a < 0 else "Dividing by a positive number preserves the inequality sign."
            op_b = "Subtract" if b >= 0 else "Add"
            steps = [
                f"Given inequality: $ {eq_typst} $",
                f"{op_b} {abs(b)} on both sides: $ {a} x {sym} {c - b} $",
                f"Divide both sides by {a}. {flip_note}",
                f"$ x {res_sym} ({c - b}) / ({a}) $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"x {sym} {x_boundary}"  # Forgot to flip
            d2 = f"x {res_sym} {-x_boundary}"
            d3 = f"x {res_sym} {x_boundary + 2}"

            return BaseProblem(
                id=f"alg1_ineq_mild_{problem_idx}",
                prompt_text="Solve each inequality.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[d1, d2, d3],
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Multi-step with variables on both sides: ax + b <= cx + d
            a = rng.choice([3, 4, 5, 6])
            c_coef = rng.choice([1, 2, -1, -2])
            sym = rng.choice(symbols)
            x_bound = rng.randint(-6, 6)
            b = rng.randint(-10, 10)
            d = (a - c_coef) * x_bound + b

            b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
            d_str = f"+ {d}" if d >= 0 else f"- {abs(d)}"
            c_str = f"{c_coef} x" if c_coef != 1 else "x"
            eq_typst = f"{a} x {b_str} {sym} {c_str} {d_str}"

            net_a = a - c_coef
            res_sym = opp_symbols[sym] if net_a < 0 else sym
            ans_typst = f"x {res_sym} {x_bound}"

            steps = [
                f"Given: $ {eq_typst} $",
                f"Subtract {c_str} from both sides: $ {net_a} x {b_str} {sym} {d} $",
                f"Subtract {b} from both sides: $ {net_a} x {sym} {d - b} $",
                f"Divide both sides by {net_a}: $ x {res_sym} {x_bound} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [f"x {opp_symbols[res_sym]} {x_bound}", f"x {res_sym} {-x_bound}"]

            return BaseProblem(
                id=f"alg1_ineq_med_{problem_idx}",
                prompt_text="Solve each multi-step inequality.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # Spicy: Compound inequality (AND / OR): e.g. a <= 2x + b < c
            x_low = rng.randint(-5, 0)
            x_high = x_low + rng.choice([3, 4, 5, 6])
            k = rng.choice([2, 3])
            b = rng.choice([1, 3, 5, -2, -4])

            low_val = k * x_low + b
            high_val = k * x_high + b

            b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
            eq_typst = f"{low_val} <= {k} x {b_str} < {high_val}"
            ans_typst = f"{x_low} <= x < {x_high}"

            steps = [
                f"Compound inequality: $ {eq_typst} $",
                f"Subtract {b} from all three parts: $ {low_val - b} <= {k} x < {high_val - b} $",
                f"Divide all three parts by {k}: $ ({low_val - b})/{k} <= x < ({high_val - b})/{k} $",
                f"Simplify boundaries: $ {ans_typst} $"
            ]

            distractors = [
                f"{x_low} < x <= {x_high}",
                f"{-x_high} <= x < {-x_low}",
                f"{x_low - 1} <= x < {x_high + 1}"
            ]

            return BaseProblem(
                id=f"alg1_ineq_spicy_{problem_idx}",
                prompt_text="Solve each compound inequality.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )

