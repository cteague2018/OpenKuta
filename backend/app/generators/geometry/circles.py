from __future__ import annotations

import math
import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_circle_diagram
from backend.app.generators.verification_gate import verify_mathematical_truth


class GeometryCirclesGenerator(BaseGenerator):
    generator_id = "geometry.circles"
    name = "Circles (Circumference, Area, Arcs & Chords)"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.C.A.2", "CCSS.MATH.CONTENT.HSG.C.B.5"]

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
        """Mild: Circumference C = 2 pi r and Area A = pi r^2 in terms of pi."""
        r = rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        c_val = 2 * r
        a_val = r * r

        eq_typst = f"\"Circle with radius \" r = {r}"
        ans_typst = f"C = {c_val} pi, quad A = {a_val} pi"

        steps = [
            "Recall circle metric formulas: Circumference $ C = 2 pi r $ and Area $ A = pi r^2 $.",
            f"Calculate circumference: $ C = 2 pi ({r}) = {c_val} pi $",
            f"Calculate area: $ A = pi ({r})^2 = {a_val} pi $",
            f"Result: $ {ans_typst} $"
        ]

        d1 = f"C = {r} pi, quad A = {a_val} pi"  # forgot factor of 2 in C
        d2 = f"C = {c_val} pi, quad A = {c_val} pi"  # did not square r for area
        d3 = f"C = {a_val} pi, quad A = {c_val} pi"  # swapped C and A

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"C = {c_val + 2} pi, quad A = {a_val + 2} pi")

        return BaseProblem(
            id=f"geom_circ_mild_{problem_idx}",
            prompt_text="Find the exact circumference and area of the circle in terms of pi.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            diagram_svg=svg_circle_diagram(radius_label=f"r = {r}"),
            answer_svg=svg_circle_diagram(radius_label=f"r = {r}"),
            metadata={"radius": r, "circumference_pi": c_val, "area_pi": a_val}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Arc length s = 2 pi r * (theta / 360) in terms of pi with fully reduced fractions."""
        r = rng.choice([3, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18])
        theta = rng.choice([30, 45, 60, 75, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315])

        raw_num = 2 * r * theta
        raw_den = 360
        g = math.gcd(raw_num, raw_den)
        num = raw_num // g
        den = raw_den // g

        if den == 1:
            arc_str = f"{num} pi"
        elif num == 1:
            arc_str = f"pi/{den}"
        else:
            arc_str = f"({num} pi)/{den}"

        eq_typst = f"\"radius \" r = {r}, quad \"central angle \" theta = {theta}°"
        ans_typst = f"s = {arc_str}"

        steps = [
            "Recall the arc length formula: $ s = 2 pi r dot (theta / 360°) $",
            f"Substitute known values: $ s = 2 pi ({r}) dot ({theta}° / 360°) $",
            f"Multiply the terms: $ s = ({raw_num} pi) / 360 $",
            f"Divide numerator and denominator by $ gcd({raw_num}, 360) = {g} $ to simplify completely.",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: used sector area formula
        g_sec = math.gcd(r * r * theta, 360)
        n_sec = (r * r * theta) // g_sec
        d_sec = 360 // g_sec
        sec_str = f"{n_sec} pi" if d_sec == 1 else f"({n_sec} pi)/{d_sec}"
        d1 = f"s = {sec_str}"

        # Distractor 2: forgot factor of 2 (pi * r * theta / 360)
        raw_num2 = r * theta
        g2 = math.gcd(raw_num2, 360)
        n2, d2 = raw_num2 // g2, 360 // g2
        half_str = f"{n2} pi" if d2 == 1 else f"({n2} pi)/{d2}"
        d2_str = f"s = {half_str}"

        # Distractor 3: inverted fraction
        d3_str = f"s = ({den} pi)/{num}" if num != 1 else f"s = {den} pi"

        distractors = list(dict.fromkeys([d1, d2_str, d3_str]))
        while len(distractors) < 2:
            distractors.append(f"s = {r} pi")

        return BaseProblem(
            id=f"geom_circ_med_{problem_idx}",
            prompt_text="Find the exact length of the arc in terms of pi. Simplify your answer completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            diagram_svg=svg_circle_diagram(radius_label=f"r = {r}", angle_label=f"{theta}°", show_sector=True),
            answer_svg=svg_circle_diagram(radius_label=f"r = {r}", angle_label=f"{theta}°", show_sector=True),
            metadata={"radius": r, "theta": theta}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Area of a sector A = pi r^2 * (theta / 360) in terms of pi with fully reduced fractions."""
        r = rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 15])
        theta = rng.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315])

        r2 = r * r
        raw_num = r2 * theta
        raw_den = 360
        g = math.gcd(raw_num, raw_den)
        num = raw_num // g
        den = raw_den // g

        if den == 1:
            sector_str = f"{num} pi"
        elif num == 1:
            sector_str = f"pi/{den}"
        else:
            sector_str = f"({num} pi)/{den}"

        eq_typst = f"\"radius \" r = {r}, quad \"central angle \" theta = {theta}°"
        ans_typst = f"A = {sector_str}"

        steps = [
            "Recall the sector area formula: $ A = pi r^2 dot (theta / 360°) $",
            f"Substitute known values: $ A = pi ({r})^2 dot ({theta}° / 360°) $",
            f"Square the radius: $ ({r})^2 = {r2} $, yielding $ A = ({r2} dot {theta} pi) / 360 = ({raw_num} pi) / 360 $",
            f"Simplify fraction by dividing numerator and denominator by $ gcd({raw_num}, 360) = {g} $.",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: used arc length formula
        g_arc = math.gcd(2 * r * theta, 360)
        n_arc = (2 * r * theta) // g_arc
        d_arc = 360 // g_arc
        arc_str = f"{n_arc} pi" if d_arc == 1 else f"({n_arc} pi)/{d_arc}"
        d1 = f"A = {arc_str}"

        # Distractor 2: forgot to square radius: (r * theta) / 360 * pi
        g_r = math.gcd(r * theta, 360)
        n_r = (r * theta) // g_r
        d_r = 360 // g_r
        r_str = f"{n_r} pi" if d_r == 1 else f"({n_r} pi)/{d_r}"
        d2 = f"A = {r_str}"

        # Distractor 3: arithmetic variation
        d3 = f"A = ({num + 1} pi)/{den}" if den != 1 else f"A = {num + 2} pi"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"A = {r2} pi")

        return BaseProblem(
            id=f"geom_circ_spicy_{problem_idx}",
            prompt_text="Find the exact area of the sector in terms of pi. Simplify your answer completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            diagram_svg=svg_circle_diagram(radius_label=f"r = {r}", angle_label=f"{theta}°", show_sector=True),
            answer_svg=svg_circle_diagram(radius_label=f"r = {r}", angle_label=f"{theta}°", show_sector=True),
            metadata={"radius": r, "theta": theta}
        )
