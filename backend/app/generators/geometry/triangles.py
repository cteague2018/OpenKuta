from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_general_triangle
from backend.app.generators.verification_gate import verify_mathematical_truth


class GeometryTrianglesGenerator(BaseGenerator):
    generator_id = "geometry.triangles"
    name = "Triangles (Angle Sum, Exterior Angle, Congruence)"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.CO.C.10"]

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
        """Mild: Triangle angle sum theorem (A + B + C = 180 degrees) with clean steps."""
        a = rng.choice([35, 40, 45, 50, 55, 60, 65, 70, 75])
        b = rng.choice([30, 35, 40, 45, 50, 55, 60, 65])
        while a + b >= 170:
            b = rng.choice([30, 35, 40, 45, 50])
        c = 180 - (a + b)

        eq_typst = f"m angle A = {a}°, quad m angle B = {b}°, quad m angle C = ?"
        ans_typst = f"m angle C = {c}°"

        steps = [
            "Apply the Triangle Angle Sum Theorem: The sum of the measures of the interior angles of a triangle is $ 180° $.",
            "$ m angle A + m angle B + m angle C = 180° $",
            f"Substitute given angles: $ {a}° + {b}° + m angle C = 180° $",
            f"Combine known angle measures: $ {a + b}° + m angle C = 180° $",
            f"Subtract $ {a + b}° $ from $ 180° $: $ m angle C = 180° - {a + b}° = {c}° $",
            f"Result: $ {ans_typst} $"
        ]

        # Misconceptions:
        # 1. Summing to 90 or 360
        d1 = f"m angle C = {abs(90 - (a + b))}°" if a + b != 90 else f"m angle C = {c + 15}°"
        # 2. Subtracting only one angle from 180
        d2 = f"m angle C = {180 - a}°"
        # 3. Off by 10 arithmetic error
        d3 = f"m angle C = {c + 10}°"
        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"m angle C = {c + 20}°")

        return BaseProblem(
            id=f"geom_tri_mild_{problem_idx}",
            prompt_text="Find the measure of angle C indicated in the triangle.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            diagram_svg=svg_general_triangle(ang_a=f"{a}°", ang_b=f"{b}°", ang_c="?"),
            answer_svg=svg_general_triangle(ang_a=f"{a}°", ang_b=f"{b}°", ang_c=f"{c}°"),
            metadata={"angle_A": a, "angle_B": b, "angle_C": c}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Exterior angle theorem (measure of exterior angle equals sum of two remote interior angles)."""
        # Variation 1: find exterior angle D given remote interiors A and B
        # Variation 2: find remote interior B given exterior D and remote interior A
        find_exterior = rng.choice([True, False])
        a = rng.choice([32, 42, 48, 54, 63, 71])
        b = rng.choice([28, 36, 45, 52, 58, 67])
        ext = a + b

        if find_exterior:
            eq_typst = f"m angle A = {a}°, quad m angle B = {b}°, quad m angle D \" (exterior)\" = ?"
            ans_typst = f"m angle D = {ext}°"

            steps = [
                "Apply the Exterior Angle Theorem: The measure of an exterior angle of a triangle is equal to the sum of the measures of its two remote interior angles.",
                "$ m angle D = m angle A + m angle B $",
                f"Substitute known remote interior angles: $ m angle D = {a}° + {b}° $",
                f"Calculate the sum: $ m angle D = {ext}° $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"m angle D = {180 - ext}°"  # interior angle adjacent to D
            d2 = f"m angle D = {ext + 10}°"
            d3 = f"m angle D = {abs(a - b)}°"
        else:
            eq_typst = f"m angle D = {ext}° \" (exterior)\", quad m angle A = {a}°, quad m angle B = ?"
            ans_typst = f"m angle B = {b}°"

            steps = [
                "Apply the Exterior Angle Theorem: An exterior angle equals the sum of the two remote interior angles.",
                "$ m angle D = m angle A + m angle B $",
                f"Substitute given values: $ {ext}° = {a}° + m angle B $",
                f"Subtract $ {a}° $ from both sides: $ m angle B = {ext}° - {a}° = {b}° $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"m angle B = {ext + a}°"  # added instead of subtracted
            d2 = f"m angle B = {180 - ext}°"
            d3 = f"m angle B = {b + 12}°"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"m angle = {ext + 5}°")

        return BaseProblem(
            id=f"geom_tri_med_{problem_idx}",
            prompt_text="Find the missing angle measure using the Exterior Angle Theorem.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            diagram_svg=svg_general_triangle(ang_a=f"{a}°", ang_b=f"{b}°" if find_exterior else "?", ext_c="?" if find_exterior else f"{ext}°"),
            answer_svg=svg_general_triangle(ang_a=f"{a}°", ang_b=f"{b}°", ext_c=f"{ext}°"),
            metadata={"angle_A": a, "angle_B": b, "exterior_D": ext}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Isosceles and equilateral triangles with algebraic expressions for angles."""
        is_equilateral = rng.choice([False, True, False])  # 1/3 chance equilateral, 2/3 isosceles

        if is_equilateral:
            # Equilateral triangle: all angles = 60 degrees. One angle is a*x + b = 60
            a = rng.choice([2, 3, 4, 5])
            x = rng.choice([5, 8, 10, 12, 15])
            b = 60 - a * x
            sign_b = f"- {abs(b)}" if b < 0 else f"+ {b}"

            eq_typst = f"\"Equilateral triangle:\" quad m angle A = ({a}x {sign_b})°"
            ans_typst = f"x = {x}, quad m angle A = 60°"

            steps = [
                "In an equilateral triangle, all three interior angles are congruent and each measures $ 60° $.",
                f"Set the algebraic angle expression equal to $ 60° $: $ {a}x {sign_b} = 60 $",
                f"Isolate the $ x $-term: $ {a}x = 60 {'+' if b < 0 else '-'} {abs(b)} = {60 - b} $",
                f"Divide both sides by $ {a} $: $ x = {60 - b} / {a} = {x} $",
                f"Verify: $ m angle A = {a}({x}) {sign_b} = 60° $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"x = {x + 2}, quad m angle A = 60°"
            d2 = f"x = {x - 2}, quad m angle A = 60°"
            d3 = f"x = {x}, quad m angle A = 180°"
        else:
            # Isosceles triangle: two base angles congruent (a*x + b), vertex angle C
            # 2*(a*x + b) + C = 180 => 2*base + C = 180
            a = rng.choice([2, 3, 4])
            x = rng.choice([4, 5, 6, 7, 8, 9, 10])
            base_target = rng.choice([40, 50, 55, 65, 70])
            b = base_target - a * x
            sign_b = f"- {abs(b)}" if b < 0 else f"+ {b}"
            vertex = 180 - 2 * base_target

            eq_typst = f"\"Isosceles triangle (base angles \" A, B \"):\" quad m angle A = ({a}x {sign_b})°, quad m angle C = {vertex}°"
            ans_typst = f"x = {x}, quad m angle A = {base_target}°"

            # 2*(ax + b) + vertex = 180 => 2*ax + 2*b + vertex = 180
            two_b = 2 * b
            sign_2b = f"- {abs(two_b)}" if two_b < 0 else f"+ {two_b}"
            const_term = two_b + vertex

            steps = [
                f"In an isosceles triangle, the base angles are congruent: $ m angle A = m angle B = ({a}x {sign_b})° $.",
                "Apply the Triangle Angle Sum Theorem: $ m angle A + m angle B + m angle C = 180° $.",
                f"Substitute expressions: $ 2({a}x {sign_b}) + {vertex} = 180 $",
                f"Distribute and simplify: $ {2*a}x {sign_2b} + {vertex} = 180 ==> {2*a}x + {const_term} = 180 $",
                f"Subtract $ {const_term} $ from both sides: $ {2*a}x = {180 - const_term} $",
                f"Divide by $ {2*a} $: $ x = {180 - const_term} / {2*a} = {x} $",
                f"Find the base angle measure: $ m angle A = {a}({x}) {sign_b} = {base_target}° $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"x = {x + 3}, quad m angle A = {base_target + 3 * a}°"
            d2 = f"x = {x}, quad m angle A = {vertex}°"
            d3 = f"x = {(180 - vertex) // a}, quad m angle A = {base_target}°"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"x = {x + 1}, quad m angle A = 50°")

        return BaseProblem(
            id=f"geom_tri_spicy_{problem_idx}",
            prompt_text="Solve for x and find the indicated angle measure in the triangle.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            diagram_svg=svg_general_triangle(ang_a=f"{a}x{sign_b}", ang_b="60°" if is_equilateral else f"{vertex}°"),
            answer_svg=svg_general_triangle(ang_a="60°" if is_equilateral else f"{base_target}°", ang_b="60°" if is_equilateral else f"{vertex}°", ang_c="60°" if is_equilateral else f"{base_target}°"),
            metadata={"x": x}
        )
