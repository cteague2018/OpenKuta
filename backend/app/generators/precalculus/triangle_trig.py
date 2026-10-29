from __future__ import annotations

import math
import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


def ensure_distractors(distractors: List[str], correct: str, fallbacks: List[str]) -> List[str]:
    """Guarantee at least 3 distinct distractors that do not match the correct answer."""
    unique: List[str] = []
    for d in distractors:
        if d != correct and d not in unique:
            unique.append(d)
    for fb in fallbacks:
        if len(unique) >= 3:
            break
        if fb != correct and fb not in unique:
            unique.append(fb)
    return unique[:3]


class TriangleTrigGenerator(BaseGenerator):
    generator_id = "precalculus.triangle_trig"
    name = "Law of Sines and Law of Cosines"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSG.SRT.D.10", "CCSS.MATH.CONTENT.HSG.SRT.D.11"]

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
        """Mild: Law of Sines AAS / ASA - Given two angles and one side, find a missing side to 1 decimal place."""
        A = rng.randint(28, 75)
        B = rng.randint(30, 80)
        while A + B >= 165:
            B = rng.randint(25, 70)

        a = rng.randint(8, 30)

        rad_A = math.radians(A)
        rad_B = math.radians(B)
        sin_A = math.sin(rad_A)
        sin_B = math.sin(rad_B)

        b_raw = (a * sin_B) / sin_A
        b_rounded = round(b_raw, 1)

        eq_typst = f"$ \"In \" triangle A B C: A = {A}°, quad B = {B}°, quad a = {a} $"
        ans_typst = f"$ b = {b_rounded:.1f} $"

        steps = [
            "State the Law of Sines: $ a / sin(A) = b / sin(B) $",
            f"Substitute the given values: $ {a} / sin({A}°) = b / sin({B}°) $",
            f"Solve for $b$: $ b = ({a} dot sin({B}°)) / sin({A}°) $",
            f"Calculate the sine values: $ sin({A}°) approx {sin_A:.4f}, quad sin({B}°) approx {sin_B:.4f} $",
            f"Compute the side length: $ b approx ({a} dot {sin_B:.4f}) / {sin_A:.4f} approx {b_raw:.3f} $",
            f"Round to the nearest tenth: {ans_typst}"
        ]

        d1_val = round((a * sin_A) / sin_B, 1)
        d1 = f"$ b = {d1_val:.1f} $"

        try:
            d2_val = round(abs((a * math.sin(B)) / math.sin(A)), 1)
            d2 = f"$ b = {d2_val:.1f} $"
        except Exception:
            d2 = f"$ b = {round(b_rounded + 3.2, 1):.1f} $"

        d3 = f"$ b = {round(b_rounded + 2.5, 1):.1f} $"
        d4 = f"$ b = {round(max(1.0, b_rounded - 2.8), 1):.1f} $"
        d5 = f"$ b = {round(b_rounded + 5.0, 1):.1f} $"

        distractors = ensure_distractors(
            [d1, d2, d3, d4],
            ans_typst,
            [d5, f"$ b = {a} $", f"$ b = {round(b_rounded * 1.5, 1):.1f} $", "$ b = 10.0 $"]
        )

        return BaseProblem(
            id=f"precalc_trig_mild_{problem_idx}",
            prompt_text="Use the Law of Sines to find the missing side length b to the nearest tenth.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Law of Cosines SAS - Given two sides and included angle, find third side."""
        a = rng.randint(6, 24)
        b = rng.randint(6, 24)
        cand_angles = [32, 40, 48, 55, 62, 70, 80, 105, 115, 125, 135]
        C = rng.choice(cand_angles)

        rad_C = math.radians(C)
        cos_C = math.cos(rad_C)

        c_sq = a**2 + b**2 - 2 * a * b * cos_C
        c_raw = math.sqrt(max(0.01, c_sq))
        c_rounded = round(c_raw, 1)

        eq_typst = f"$ \"In \" triangle A B C: a = {a}, quad b = {b}, quad C = {C}° $"
        ans_typst = f"$ c = {c_rounded:.1f} $"

        steps = [
            "State the Law of Cosines: $ c^2 = a^2 + b^2 - 2 a b cos(C) $",
            f"Substitute the given values: $ c^2 = {a}^2 + {b}^2 - 2({a})({b}) cos({C}°) $",
            f"Calculate the squares and product: $ c^2 = {a**2} + {b**2} - {2 * a * b} dot cos({C}°) $",
            f"Evaluate the cosine: $ cos({C}°) approx {cos_C:.4f} $",
            f"Compute $ c^2 $: $ c^2 = {a**2 + b**2} - {2 * a * b}({cos_C:.4f}) approx {c_sq:.3f} $",
            f"Take the principal square root: $ c = sqrt({c_sq:.3f}) approx {c_raw:.3f} $",
            f"Round to the nearest tenth: {ans_typst}"
        ]

        d1_val = round(math.sqrt(max(1.0, a**2 + b**2 + 2 * a * b * cos_C)), 1)
        d1 = f"$ c = {d1_val:.1f} $"

        d2_val = round(math.sqrt(a**2 + b**2), 1)
        d2 = f"$ c = {d2_val:.1f} $"

        d3 = f"$ c = {round(c_rounded + 3.1, 1):.1f} $"
        d4 = f"$ c = {round(max(1.0, c_rounded - 2.6), 1):.1f} $"
        d5 = f"$ c = {round(c_rounded + 6.0, 1):.1f} $"

        distractors = ensure_distractors(
            [d1, d2, d3, d4],
            ans_typst,
            [d5, f"$ c = {a + b} $", f"$ c = {abs(a - b)} $", "$ c = 15.0 $"]
        )

        return BaseProblem(
            id=f"precalc_trig_med_{problem_idx}",
            prompt_text="Use the Law of Cosines to find the missing side length c to the nearest tenth.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Law of Cosines SSS (find angle given 3 sides) or Law of Sines SSA ambiguous case."""
        subflavor = rng.choice(["sss_angle", "ssa_ambiguous"])

        if subflavor == "sss_angle":
            a = rng.randint(7, 22)
            b = rng.randint(7, 22)
            target_C = rng.randint(35, 130)
            c_val = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(math.radians(target_C)))
            c = round(c_val, 1)
            cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
            cos_C = max(-1.0, min(1.0, cos_C))
            C_deg = math.degrees(math.acos(cos_C))
            C_rounded = round(C_deg, 1)

            eq_typst = f"$ \"In \" triangle A B C: a = {a}, quad b = {b}, quad c = {c} $"
            ans_typst = f"$ C = {C_rounded:.1f}° $"

            num = a**2 + b**2 - c**2
            den = 2 * a * b

            steps = [
                "Recall the Law of Cosines arranged for $cos(C)$: $ cos(C) = (a^2 + b^2 - c^2) / (2 a b) $",
                f"Substitute the side lengths: $ cos(C) = ({a}^2 + {b}^2 - {c}^2) / (2 dot {a} dot {b}) $",
                f"Calculate squares and products: $ cos(C) = ({a**2} + {b**2} - {round(c**2, 2)}) / {den} $",
                f"Simplify the fraction: $ cos(C) = {num:.2f} / {den} approx {cos_C:.4f} $",
                f"Take the inverse cosine: $ C = arccos({cos_C:.4f}) approx {C_deg:.3f}° $",
                f"Round to the nearest tenth: {ans_typst}"
            ]

            d1 = f"$ C = {round(180.0 - C_rounded, 1):.1f}° $"
            try:
                inv_cos = max(-1.0, min(1.0, -cos_C))
                d2 = f"$ C = {round(math.degrees(math.acos(inv_cos)), 1):.1f}° $"
            except Exception:
                d2 = f"$ C = {round(C_rounded + 15.0, 1):.1f}° $"
            d3 = f"$ C = {round(C_rounded + 12.4, 1):.1f}° $"
            d4 = f"$ C = {round(max(10.0, C_rounded - 14.2), 1):.1f}° $"
            d5 = f"$ C = {round(C_rounded + 25.0, 1):.1f}° $"

            distractors = ensure_distractors(
                [d1, d2, d3, d4],
                ans_typst,
                [d5, "$ C = 90.0° $", "$ C = 45.0° $", "$ C = 60.0° $"]
            )

            return BaseProblem(
                id=f"precalc_trig_spicy_{problem_idx}",
                prompt_text="Use the Law of Cosines to find the measure of angle C to the nearest tenth of a degree.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )

        else:
            scenario = rng.choice(["0_triangles", "1_triangle", "2_triangles"])
            A = rng.randint(30, 65)
            rad_A = math.radians(A)
            sin_A = math.sin(rad_A)
            b = rng.randint(12, 28)
            h = b * sin_A

            if scenario == "0_triangles":
                a = max(1, int(h - rng.randint(2, 5)))
                ans_typst = "$ \"0 triangles\" $"
                case_explanation = f"Since $ a = {a} < h approx {h:.2f} $, the side $a$ is too short to reach side $c$."
            elif scenario == "2_triangles":
                lower = int(math.ceil(h + 0.5))
                upper = b - 1
                if lower >= upper:
                    upper = lower + 3
                    b = upper + 1
                    h = b * sin_A
                a = rng.randint(lower, upper)
                ans_typst = "$ \"2 triangles\" $"
                case_explanation = f"Since $ h approx {h:.2f} < a = {a} < b = {b} $, two distinct triangles can be formed (ambiguous case)."
            else:
                a = b + rng.randint(1, 8)
                ans_typst = "$ \"1 triangle\" $"
                case_explanation = f"Since $ a = {a} >= b = {b} $, exactly one triangle can be formed."

            eq_typst = f"$ A = {A}°, quad a = {a}, quad b = {b} $"

            steps = [
                "For the SSA case with acute angle $ A $, compare side $ a $ to altitude $ h = b sin(A) $ and side $ b $.",
                f"Calculate the altitude: $ h = {b} dot sin({A}°) approx {b} dot ({sin_A:.4f}) approx {h:.2f} $",
                f"Compare side lengths: $ a = {a}, quad b = {b}, quad h approx {h:.2f} $",
                case_explanation,
                f"Result: {ans_typst}"
            ]

            fallbacks = ["$ \"0 triangles\" $", "$ \"1 triangle\" $", "$ \"2 triangles\" $", "$ \"3 triangles\" $", "$ \"Infinitely many triangles\" $"]
            distractors = ensure_distractors(
                [fb for fb in fallbacks if fb != ans_typst],
                ans_typst,
                fallbacks
            )

            return BaseProblem(
                id=f"precalc_trig_spicy_{problem_idx}",
                prompt_text="Determine the number of distinct triangles that can be formed with the given measurements (SSA ambiguous case).",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )
