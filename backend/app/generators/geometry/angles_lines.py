from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_angle_diagram, svg_parallel_transversal


class GeometryAnglesLinesGenerator(BaseGenerator):
    generator_id = "geometry.angles_lines"
    name = "Angles, Lines & Transversals"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.CO.C.9"]

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
        """Mild: Complementary (sum to 90) and supplementary (sum to 180) angle pairs."""
        is_supp = rng.choice([True, False])
        total = 180 if is_supp else 90
        type_name = "supplementary" if is_supp else "complementary"

        if is_supp:
            given = rng.choice([25, 35, 45, 55, 65, 75, 105, 115, 125, 135, 145])
        else:
            given = rng.choice([18, 25, 32, 41, 48, 54, 63, 72])

        missing = total - given
        eq_typst = f"\"angle 1 and angle 2 are \" {type_name}, quad m angle 1 = {given}^circle, quad m angle 2 = ?"
        ans_typst = f"m angle 2 = {missing}^circle"

        steps = [
            f"Recall that {type_name} angles sum to $ {total}^circle $.",
            f"Equation: $ m angle 1 + m angle 2 = {total}^circle $",
            f"Substitute the given angle: $ {given}^circle + m angle 2 = {total}^circle $",
            f"Subtract $ {given}^circle $ from both sides: $ m angle 2 = {total}^circle - {given}^circle = {missing}^circle $",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: used wrong total (90 vs 180)
        wrong_total = 90 if is_supp else 180
        d1 = f"m angle 2 = {abs(wrong_total - given)}^circle"
        # Distractor 2: added instead of subtracted
        d2 = f"m angle 2 = {missing + 10}^circle"
        # Distractor 3: repeated given
        d3 = f"m angle 2 = {given}^circle"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"m angle 2 = {missing + 5}^circle")

        if is_supp:
            diag_mild = svg_angle_diagram(angle_degrees=float(given), mode="linear_pair", angle_label=f"{given}&#176;", interior_angle_label="?")
            ans_mild = svg_angle_diagram(angle_degrees=float(given), mode="linear_pair", angle_label=f"{given}&#176;", interior_angle_label=f"{missing}&#176;", shade=True, bottom_label=f"m∠2 = {missing}&#176;")
        else:
            diag_mild = svg_angle_diagram(angle_degrees=float(missing), interior_angle=float(given), mode="interior_ray", angle_label="?", interior_angle_label=f"{given}&#176;")
            ans_mild = svg_angle_diagram(angle_degrees=float(missing), interior_angle=float(given), mode="interior_ray", angle_label=f"{missing}&#176;", interior_angle_label=f"{given}&#176;", shade=True, bottom_label=f"m∠2 = {missing}&#176;")

        return BaseProblem(
            id=f"geom_ang_mild_{problem_idx}",
            prompt_text=f"Find the measure of angle 2 given that angle 1 and angle 2 are {type_name}.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            diagram_svg=diag_mild,
            answer_svg=ans_mild,
            metadata={"type": type_name, "angle1": given, "angle2": missing}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Segment Addition Postulate (B between A and C, AB = ax + b, BC = cx + d, AC = total)."""
        x_val = rng.choice([3, 4, 5, 6, 7, 8])
        a = rng.choice([2, 3, 4])
        b = rng.choice([1, 2, 3, 4, 5])
        c = rng.choice([1, 2, 3])
        d = rng.choice([2, 3, 4, 6])

        ab = a * x_val + b
        bc = c * x_val + d
        ac = ab + bc

        eq_typst = f"B \" is between \" A \" and \" C. quad A B = {a}x + {b}, quad B C = {c}x + {d}, quad A C = {ac}"
        ans_typst = f"x = {x_val}"

        sum_coef = a + c
        sum_const = b + d
        rem = ac - sum_const

        steps = [
            "Apply the Segment Addition Postulate: $ A B + B C = A C $",
            f"Substitute the algebraic expressions: $ ({a}x + {b}) + ({c}x + {d}) = {ac} $",
            f"Combine like terms: $ {sum_coef}x + {sum_const} = {ac} $",
            f"Subtract $ {sum_const} $ from both sides: $ {sum_coef}x = {ac} - {sum_const} = {rem} $",
            f"Divide both sides by $ {sum_coef} $: $ x = {rem} / {sum_coef} = {x_val} $",
            f"Verify: $ A B = {a}({x_val}) + {b} = {ab} $, $ B C = {c}({x_val}) + {d} = {bc} $, and $ {ab} + {bc} = {ac} $.",
            f"Result: $ {ans_typst} $"
        ]

        d1 = f"x = {x_val + 2}"
        d2 = f"x = {x_val - 1 if x_val > 1 else x_val + 3}"
        d3 = f"x = {ac // sum_coef}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"x = {x_val + 4}")

        return BaseProblem(
            id=f"geom_ang_med_{problem_idx}",
            prompt_text="Solve for x using the Segment Addition Postulate.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"x": x_val, "AB": ab, "BC": bc, "AC": ac}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Parallel lines cut by a transversal: alternate interior angles or consecutive interior angles."""
        is_consecutive = rng.choice([True, False])

        if not is_consecutive:
            # Alternate interior angles (congruent: ax + b = cx + d)
            x_val = rng.choice([4, 5, 6, 7, 8, 9, 10])
            c = rng.choice([2, 3])
            k = rng.choice([1, 2])
            a = c + k

            target_angle = rng.choice([45, 55, 65, 75, 110, 120, 130])
            b = target_angle - a * x_val
            d = target_angle - c * x_val

            sign_b = f"- {abs(b)}" if b < 0 else f"+ {b}"
            sign_d = f"- {abs(d)}" if d < 0 else f"+ {d}"

            eq_typst = f"l_1 parallel l_2 \" cut by transversal.\" quad angle 1 \" and \" angle 2 \" are alternate interior:\" quad m angle 1 = ({a}x {sign_b})^circle, quad m angle 2 = ({c}x {sign_d})^circle"
            ans_typst = f"x = {x_val}, quad m angle 1 = {target_angle}^circle"

            steps = [
                "Alternate Interior Angles Theorem: When two parallel lines are cut by a transversal, alternate interior angles are congruent: $ m angle 1 = m angle 2 $.",
                f"Set up equation: $ {a}x {sign_b} = {c}x {sign_d} $",
                f"Subtract $ {c}x $ from both sides: $ {a - c}x {sign_b} = {d} $",
                f"Isolate the $ x $-term: $ {a - c}x = {d - b} $",
                f"Divide by $ {a - c} $: $ x = {d - b} / {a - c} = {x_val} $",
                f"Find the angle measure: $ m angle 1 = {a}({x_val}) {sign_b} = {target_angle}^circle $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"x = {x_val + 2}, quad m angle 1 = {target_angle + 2 * a}^circle"
            d2 = f"x = {x_val}, quad m angle 1 = {180 - target_angle}^circle"
            d3 = f"x = {x_val - 2 if x_val > 3 else x_val + 3}, quad m angle 1 = {target_angle}^circle"

        else:
            # Consecutive interior angles (supplementary: (ax + b) + (cx + d) = 180)
            x_val = rng.choice([4, 5, 6, 7, 8])
            a = rng.choice([2, 3])
            c = rng.choice([1, 2])
            sum_coef = a + c

            # sum_coef * x_val + (b + d) = 180 => b + d = 180 - sum_coef * x_val
            total_const = 180 - sum_coef * x_val
            b = rng.choice([10, 15, 20, 25])
            d = total_const - b

            ang1 = a * x_val + b
            ang2 = c * x_val + d

            sign_b = f"- {abs(b)}" if b < 0 else f"+ {b}"
            sign_d = f"- {abs(d)}" if d < 0 else f"+ {d}"

            eq_typst = f"l_1 parallel l_2 \" cut by transversal.\" quad angle 1 \" and \" angle 2 \" are consecutive interior:\" quad m angle 1 = ({a}x {sign_b})^circle, quad m angle 2 = ({c}x {sign_d})^circle"
            ans_typst = f"x = {x_val}, quad m angle 1 = {ang1}^circle, quad m angle 2 = {ang2}^circle"

            steps = [
                "Consecutive Interior Angles Theorem: When two parallel lines are cut by a transversal, consecutive interior angles are supplementary: $ m angle 1 + m angle 2 = 180^circle $.",
                f"Set up equation: $ ({a}x {sign_b}) + ({c}x {sign_d}) = 180 $",
                f"Combine like terms: $ {sum_coef}x + {total_const} = 180 $",
                f"Subtract $ {total_const} $ from both sides: $ {sum_coef}x = {180 - total_const} $",
                f"Divide by $ {sum_coef} $: $ x = {180 - total_const} / {sum_coef} = {x_val} $",
                f"Calculate angles: $ m angle 1 = {a}({x_val}) {sign_b} = {ang1}^circle $ and $ m angle 2 = {c}({x_val}) {sign_d} = {ang2}^circle $.",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"x = {x_val + 2}, quad m angle 1 = {ang1 + 2 * a}^circle, quad m angle 2 = {ang2 + 2 * c}^circle"
            d2 = f"x = {x_val}, quad m angle 1 = {ang2}^circle, quad m angle 2 = {ang1}^circle"
            d3 = f"x = {x_val - 1}, quad m angle 1 = {ang1 - a}^circle, quad m angle 2 = {ang2 - c}^circle"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"x = {x_val + 1}, quad m angle 1 = 60^circle")

        return BaseProblem(
            id=f"geom_ang_spicy_{problem_idx}",
            prompt_text="Solve for x and find the indicated angle measures.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            diagram_svg=svg_parallel_transversal("∠1", "∠2", "consecutive_interior" if is_consecutive else "alt_interior"),
            answer_svg=svg_parallel_transversal("∠1", "∠2", "consecutive_interior" if is_consecutive else "alt_interior"),
            metadata={"x": x_val}
        )
