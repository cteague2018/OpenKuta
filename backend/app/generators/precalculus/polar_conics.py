from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


def format_sq_term(var: str, shift: int) -> str:
    if shift == 0:
        return f"{var}^2"
    elif shift > 0:
        return f"({var} - {shift})^2"
    else:
        return f"({var} + {-shift})^2"


class PrecalcPolarConicsGenerator(BaseGenerator):
    generator_id = "precalculus.polar_conics"
    name = "Polar Coordinates & Conic Sections"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSG.GPE.A.1", "CCSS.MATH.CONTENT.HSG.GPE.A.3"]

    @verify_mathematical_truth()
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
        """Mild: Circle in standard form (x - h)^2 + (y - k)^2 = r^2 given center and radius."""
        h = rng.choice([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6])
        k = rng.choice([-6, -4, -3, -1, 0, 1, 2, 4, 5])
        r = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])

        x_part = format_sq_term("x", h)
        y_part = format_sq_term("y", k)
        r_sq = r * r

        eq_typst = f"\"Center: \" ({h}, {k}), quad \"Radius: \" {r}"
        ans_typst = f"{x_part} + {y_part} = {r_sq}"

        steps = [
            "Recall standard form of a circle: $ (x - h)^2 + (y - k)^2 = r^2 $",
            f"Substitute center coordinates $ (h, k) = ({h}, {k}) $: $ {x_part} + {y_part} = r^2 $",
            f"Square the radius: $ r^2 = ({r})^2 = {r_sq} $",
            f"Write final equation in standard form: $ {ans_typst} $"
        ]

        distractors = [
            f"{x_part} - {y_part} = {r_sq}",
            f"{format_sq_term('x', -h)} + {format_sq_term('y', -k)} = {r_sq}",
            f"{x_part} + {y_part} = {2 * r}"
        ]

        return BaseProblem(
            id=f"pcalc_conic_mild_{problem_idx}",
            prompt_text="Write the standard form equation of each circle given its center and radius.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Ellipse in standard form (x - h)^2/a^2 + (y - k)^2/b^2 = 1, identifying center, vertices, and foci c = sqrt(abs(a^2 - b^2))."""
        # Pythagorean triples for clean integer focal distance c
        ellipses = [
            (5, 4, 3, "horizontal"),
            (5, 3, 4, "horizontal"),
            (13, 12, 5, "horizontal"),
            (10, 8, 6, "horizontal"),
            (10, 6, 8, "horizontal"),
            (4, 5, 3, "vertical"),
            (3, 5, 4, "vertical"),
            (12, 13, 5, "vertical"),
            (8, 10, 6, "vertical"),
            (6, 10, 8, "vertical"),
        ]

        a, b, c, orientation = rng.choice(ellipses)
        h = rng.choice([-4, -2, -1, 0, 1, 2, 3, 5])
        k = rng.choice([-3, -2, 0, 1, 2, 4])

        a2 = a * a
        b2 = b * b
        x_term = format_sq_term("x", h)
        y_term = format_sq_term("y", k)

        eq_typst = f"({x_term}) / {a2} + ({y_term}) / {b2} = 1"

        if orientation == "horizontal":
            v1_str = f"({h - a}, {k})"
            v2_str = f"({h + a}, {k})"
            f1_str = f"({h - c}, {k})"
            f2_str = f"({h + c}, {k})"
            ans_typst = f"\"Center: \" ({h}, {k}), quad \"Vertices: \" {v1_str}, {v2_str}, quad \"Foci: \" {f1_str}, {f2_str}"

            steps = [
                f"Identify center $ (h, k) $ from numerators: $ ({h}, {k}) $",
                f"Compare denominators: $ a^2 = {a2} $ (under x) is larger than $ b^2 = {b2} $ (under y), so the major axis is horizontal with $ a = {a}, b = {b} $",
                f"Calculate focal distance: $ c = sqrt(a^2 - b^2) = sqrt({a2} - {b2}) = sqrt({c*c}) = {c} $",
                f"Vertices are at $ (h plus.minus a, k) $: $ ({h} - {a}, {k}) = {v1_str} $ and $ ({h} + {a}, {k}) = {v2_str} $",
                f"Foci are at $ (h plus.minus c, k) $: $ ({h} - {c}, {k}) = {f1_str} $ and $ ({h} + {c}, {k}) = {f2_str} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"\"Center: \" ({-h}, {-k}), quad \"Vertices: \" {v1_str}, {v2_str}, quad \"Foci: \" {f1_str}, {f2_str}",
                f"\"Center: \" ({h}, {k}), quad \"Vertices: \" ({h}, {k - a}), ({h}, {k + a}), quad \"Foci: \" ({h}, {k - c}), ({h}, {k + c})",
                f"\"Center: \" ({h}, {k}), quad \"Vertices: \" {v1_str}, {v2_str}, quad \"Foci: \" ({h - b}, {k}), ({h + b}, {k})"
            ]
        else:
            v1_str = f"({h}, {k - b})"
            v2_str = f"({h}, {k + b})"
            f1_str = f"({h}, {k - c})"
            f2_str = f"({h}, {k + c})"
            ans_typst = f"\"Center: \" ({h}, {k}), quad \"Vertices: \" {v1_str}, {v2_str}, quad \"Foci: \" {f1_str}, {f2_str}"

            steps = [
                f"Identify center $ (h, k) $ from numerators: $ ({h}, {k}) $",
                f"Compare denominators: $ b^2 = {b2} $ (under y) is larger than $ a^2 = {a2} $ (under x), so the major axis is vertical with $ b = {b}, a = {a} $",
                f"Calculate focal distance: $ c = sqrt(b^2 - a^2) = sqrt({b2} - {a2}) = sqrt({c*c}) = {c} $",
                f"Vertices are at $ (h, k plus.minus b) $: $ ({h}, {k} - {b}) = {v1_str} $ and $ ({h}, {k} + {b}) = {v2_str} $",
                f"Foci are at $ (h, k plus.minus c) $: $ ({h}, {k} - {c}) = {f1_str} $ and $ ({h}, {k} + {c}) = {f2_str} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"\"Center: \" ({-h}, {-k}), quad \"Vertices: \" {v1_str}, {v2_str}, quad \"Foci: \" {f1_str}, {f2_str}",
                f"\"Center: \" ({h}, {k}), quad \"Vertices: \" ({h - b}, {k}), ({h + b}, {k}), quad \"Foci: \" ({h - c}, {k}), ({h + c}, {k})",
                f"\"Center: \" ({h}, {k}), quad \"Vertices: \" {v1_str}, {v2_str}, quad \"Foci: \" ({h}, {k - a}), ({h}, {k + a})"
            ]

        return BaseProblem(
            id=f"pcalc_conic_med_{problem_idx}",
            prompt_text="Identify the center, vertices, and foci of each ellipse.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Converting general conic equation to standard form by completing the square."""
        h = rng.choice([-3, -2, -1, 1, 2, 3])
        k = rng.choice([-3, -2, -1, 1, 2, 3])

        # Ellipse: A*(x - h)^2 + B*(y - k)^2 = M
        # with A=4, B=9, M=36 => (x-h)^2/9 + (y-k)^2/4 = 1
        # or A=9, B=4, M=36 => (x-h)^2/4 + (y-k)^2/9 = 1
        # or A=1, B=4, M=16 => (x-h)^2/16 + (y-k)^2/4 = 1
        # or A=4, B=1, M=16 => (x-h)^2/4 + (y-k)^2/16 = 1
        configs = [
            (4, 9, 36, 9, 4),
            (9, 4, 36, 4, 9),
            (1, 4, 16, 16, 4),
            (4, 1, 16, 4, 16),
            (1, 9, 36, 36, 4),
            (9, 1, 36, 4, 36)
        ]

        A, B, M, den_x, den_y = rng.choice(configs)

        # Expand: A*(x^2 - 2hx + h^2) + B*(y^2 - 2ky + k^2) - M = 0
        # A x^2 + B y^2 - 2Ah x - 2Bk y + (A*h^2 + B*k^2 - M) = 0
        coeff_x = -2 * A * h
        coeff_y = -2 * B * k
        const_term = A * (h ** 2) + B * (k ** 2) - M

        # Format equation
        parts = []
        parts.append(f"{A} x^2" if A > 1 else "x^2")
        parts.append(f"+ {B} y^2" if B > 1 else "+ y^2")
        if coeff_x > 0:
            parts.append(f"+ {coeff_x} x")
        elif coeff_x < 0:
            parts.append(f"- {abs(coeff_x)} x")

        if coeff_y > 0:
            parts.append(f"+ {coeff_y} y")
        elif coeff_y < 0:
            parts.append(f"- {abs(coeff_y)} y")

        if const_term > 0:
            parts.append(f"+ {const_term}")
        elif const_term < 0:
            parts.append(f"- {abs(const_term)}")

        eq_typst = " ".join(parts) + " = 0"

        x_sq = format_sq_term("x", h)
        y_sq = format_sq_term("y", k)
        ans_typst = f"({x_sq}) / {den_x} + ({y_sq}) / {den_y} = 1"

        steps = [
            f"Rearrange terms by grouping $x$ and $y$ variables and moving the constant to the right: $ ({A} x^2 {'+' if coeff_x >= 0 else '-'} {abs(coeff_x)} x) + ({B} y^2 {'+' if coeff_y >= 0 else '-'} {abs(coeff_y)} y) = {-const_term} $",
            f"Factor out leading coefficients from each group: $ {A} (x^2 {'+' if -2*h >= 0 else '-'} {abs(2*h)} x) + {B} (y^2 {'+' if -2*k >= 0 else '-'} {abs(2*k)} y) = {-const_term} $",
            f"Complete the square inside each set of parentheses by adding $({-h})^2 = {h*h}$ and $({-k})^2 = {k*k}$: $ {A} (x^2 {'+' if -2*h >= 0 else '-'} {abs(2*h)} x + {h*h}) + {B} (y^2 {'+' if -2*k >= 0 else '-'} {abs(2*k)} y + {k*k}) = {-const_term} + {A*h*h} + {B*k*k} $",
            f"Write as perfect squares: $ {A} {x_sq} + {B} {y_sq} = {M} $",
            f"Divide both sides by {M} to obtain standard form: $ {ans_typst} $"
        ]

        distractors = [
            f"({x_sq}) / {den_y} + ({y_sq}) / {den_x} = 1",
            f"({format_sq_term('x', -h)}) / {den_x} + ({format_sq_term('y', -k)}) / {den_y} = 1",
            f"({x_sq}) / {den_x} - ({y_sq}) / {den_y} = 1"
        ]

        return BaseProblem(
            id=f"pcalc_conic_spicy_{problem_idx}",
            prompt_text="Rewrite the general conic equation in standard form by completing the square.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
