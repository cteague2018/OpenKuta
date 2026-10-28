from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_number_line
from backend.app.generators.verification_gate import verify_mathematical_truth


class LinearInequalitiesGenerator(BaseGenerator):
    generator_id = "algebra_1.inequalities"
    name = "Linear Inequalities (One-Step, Multi-Step & Compound)"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.3", "TEKS.MATH.A1.5.B"]

    @verify_mathematical_truth()
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


class GraphingInequalitiesGenerator(BaseGenerator):
    generator_id = "algebra_1.graphing_inequalities"
    name = "Graphing Single-Variable Inequalities"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.3", "TEKS.MATH.A1.5.B"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        var = rng.choice(["x", "n", "k", "m", "p", "v"])
        val = rng.randint(-8, 8) if allow_negatives else rng.randint(0, 8)
        sym = rng.choice(["<", "<=", ">", ">="])

        if difficulty == ProblemDifficulty.MILD:
            eq = f"{var} {sym} {val}"
            ans = f"{var} {sym} {val}"
            is_closed = "<=" in sym or ">=" in sym
            dir_s = "left" if "<" in sym else "right"
            ans_svg = svg_number_line(intervals=[{"type": "ray", "val": val, "dir": dir_s, "closed": is_closed}])
            steps = [
                f"Given inequality: $ {eq} $",
                f"Place an {'closed (solid)' if is_closed else 'open'} circle at $ {val} $ on the number line.",
                f"Draw an arrow pointing to the {dir_s} since the inequality represents values {'less than' if '<' in sym else 'greater than'} {val}."
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            a = rng.choice([2, 3, -2, -3])
            b = rng.randint(-6, 6)
            c = a * val + b
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            eq = f"{a} {var} {b_s} {sym} {c}".replace("+ -", "- ")
            res_sym = (">" if sym == "<" else (">=" if sym == "<=" else ("<" if sym == ">" else "<="))) if a < 0 else sym
            ans = f"{var} {res_sym} {val}"
            is_closed = "<=" in res_sym or ">=" in res_sym
            dir_s = "left" if "<" in res_sym else "right"
            ans_svg = svg_number_line(intervals=[{"type": "ray", "val": val, "dir": dir_s, "closed": is_closed}])
            steps = [
                f"Given inequality: $ {eq} $",
                f"Subtract constant and divide by {a} (remembering to {'FLIP the inequality sign because dividing by negative' if a < 0 else 'preserve the sign'}): $ {ans} $",
                f"Graph: {'closed' if is_closed else 'open'} circle at $ {val} $, arrow pointing {dir_s}."
            ]
        else:  # SPICY
            v1 = rng.randint(-6, 0)
            v2 = rng.randint(1, 7)
            eq = f"{v1} < {var} <= {v2}"
            ans = f"{v1} < {var} <= {v2}"
            ans_svg = svg_number_line(intervals=[{"type": "segment", "a": v1, "b": v2, "closed_a": False, "closed_b": True}])
            steps = [
                f"Given compound inequality: $ {eq} $",
                f"Place an open circle at $ {v1} $ and a closed (solid) circle at $ {v2} $.",
                f"Shade the segment connecting $ {v1} $ and $ {v2} $ on the number line."
            ]

        d1 = f"{var} {'<' if sym == '>' else '>'} {val}"
        d2 = f"{var} {sym} {-val}"
        d3 = f"{var} {sym} {val + 1}"

        return BaseProblem(
            id=f"graph_ineq_num_{difficulty.value}_{problem_idx}",
            prompt_text="Draw a graph for each inequality on a number line.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            diagram_svg=svg_number_line(),
            answer_svg=ans_svg,
            metadata={"inequality": eq}
        )
