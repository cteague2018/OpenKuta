from __future__ import annotations

import math
import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeometryTrigonometryGenerator(BaseGenerator):
    generator_id = "geometry.trigonometry"
    name = "Right Triangle Trigonometry"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.SRT.C.6", "CCSS.MATH.CONTENT.HSG.SRT.C.8"]

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
        """Mild: Evaluating sin(theta), cos(theta), tan(theta) given all 3 sides (SOH CAH TOA)."""
        triples = [
            (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
            (9, 40, 41), (12, 35, 37), (6, 8, 10), (10, 24, 26)
        ]
        opp, adj, hyp = rng.choice(triples)
        func_name = rng.choice(["sin", "cos", "tan"])

        if func_name == "sin":
            num, den = opp, hyp
            desc = "opposite / hypotenuse"
        elif func_name == "cos":
            num, den = adj, hyp
            desc = "adjacent / hypotenuse"
        else:
            num, den = opp, adj
            desc = "opposite / adjacent"

        g = math.gcd(num, den)
        s_num, s_den = num // g, den // g
        ratio_str = f"{s_num}/{s_den}" if s_den != 1 else f"{s_num}"

        eq_typst = f"\"opposite = \" {opp}, quad \"adjacent = \" {adj}, quad \"hypotenuse = \" {hyp}"
        ans_typst = f"{func_name}(theta) = {ratio_str}"

        steps = [
            "Recall the trigonometric ratios for right triangles using SOH CAH TOA:",
            f"$ {func_name}(theta) = text(\"{desc}\") $",
            f"Substitute given side lengths: $ {func_name}(theta) = {num} / {den} $",
        ]
        if g > 1:
            steps.append(f"Simplify the fraction by dividing numerator and denominator by {g}: $ {ans_typst} $")
        else:
            steps.append(f"Result: $ {ans_typst} $")

        # Distractor 1: reciprocal ratio
        d1 = f"{func_name}(theta) = {den}/{num}" if den != num else f"{func_name}(theta) = {num + 1}/{den}"
        # Distractor 2: wrong ratio (adjacent instead of opposite or vice-versa)
        if func_name == "sin":
            d2 = f"{func_name}(theta) = {adj}/{hyp}"
        elif func_name == "cos":
            d2 = f"{func_name}(theta) = {opp}/{hyp}"
        else:
            d2 = f"{func_name}(theta) = {adj}/{opp}"
        # Distractor 3: hypotenuse involved in tangent or opp/adj swapped
        d3 = f"{func_name}(theta) = {opp}/{hyp + adj}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"{func_name}(theta) = 1/2")

        return BaseProblem(
            id=f"geom_trig_mild_{problem_idx}",
            prompt_text=f"Find the value of {func_name}(theta) for the given right triangle in simplest form.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"func": func_name, "opp": opp, "adj": adj, "hyp": hyp}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Finding a missing side in a right triangle given an angle and one side length."""
        use_special = rng.choice([True, False])

        if use_special:
            # 30, 45, or 60 degrees with exact / clean calculations
            angle_type = rng.choice(["sin30", "cos60", "tan45"])
            if angle_type == "sin30":
                theta = 30
                hyp = rng.choice([8, 10, 12, 14, 16, 20])
                ans_val = hyp // 2
                eq_typst = f"theta = 30^circle, quad \"hypotenuse = \" {hyp}, quad \"opposite (x) = ?\""
                ans_typst = f"x = {ans_val}"
                steps = [
                    "Identify sides relative to angle $ theta $: opposite is $ x $, hypotenuse is $ {hyp} $.",
                    "Use the sine ratio: $ sin(theta) = text(\"opposite\") / text(\"hypotenuse\") $",
                    f"Substitute known values: $ sin(30^circle) = x / {hyp} $",
                    "Recall that $ sin(30^circle) = 1/2 = 0.5 $.",
                    f"Solve for $ x $: $ x = {hyp} dot sin(30^circle) = {hyp} dot 0.5 = {ans_val} $",
                    f"Result: $ {ans_typst} $"
                ]
                d1 = f"x = {hyp}"
                d2 = f"x = {hyp * 2}"
                d3 = f"x = {round(hyp * math.cos(math.radians(30)), 1)}"
            elif angle_type == "cos60":
                theta = 60
                hyp = rng.choice([8, 10, 12, 14, 16, 20])
                ans_val = hyp // 2
                eq_typst = f"theta = 60^circle, quad \"hypotenuse = \" {hyp}, quad \"adjacent (x) = ?\""
                ans_typst = f"x = {ans_val}"
                steps = [
                    "Identify sides relative to angle $ theta $: adjacent is $ x $, hypotenuse is $ {hyp} $.",
                    "Use the cosine ratio: $ cos(theta) = text(\"adjacent\") / text(\"hypotenuse\") $",
                    f"Substitute known values: $ cos(60^circle) = x / {hyp} $",
                    "Recall that $ cos(60^circle) = 1/2 = 0.5 $.",
                    f"Solve for $ x $: $ x = {hyp} dot cos(60^circle) = {hyp} dot 0.5 = {ans_val} $",
                    f"Result: $ {ans_typst} $"
                ]
                d1 = f"x = {hyp}"
                d2 = f"x = {hyp * 2}"
                d3 = f"x = {round(hyp * math.sin(math.radians(60)), 1)}"
            else:  # tan45
                theta = 45
                adj = rng.choice([5, 6, 7, 8, 9, 10, 12])
                ans_val = adj
                eq_typst = f"theta = 45^circle, quad \"adjacent = \" {adj}, quad \"opposite (x) = ?\""
                ans_typst = f"x = {ans_val}"
                steps = [
                    "Identify sides relative to angle $ theta $: opposite is $ x $, adjacent is $ {adj} $.",
                    "Use the tangent ratio: $ tan(theta) = text(\"opposite\") / text(\"adjacent\") $",
                    f"Substitute known values: $ tan(45^circle) = x / {adj} $",
                    "Recall that $ tan(45^circle) = 1 $.",
                    f"Solve for $ x $: $ x = {adj} dot tan(45^circle) = {adj} dot 1 = {ans_val} $",
                    f"Result: $ {ans_typst} $"
                ]
                d1 = f"x = {round(adj * math.sqrt(2), 1)}"
                d2 = f"x = {adj + 2}"
                d3 = f"x = {adj // 2}"
        else:
            # General angle rounded to nearest tenth
            theta = rng.choice([25, 35, 40, 50, 55, 65, 70])
            hyp = rng.choice([10, 12, 14, 15, 18, 20])
            sin_val = math.sin(math.radians(theta))
            ans_num = round(hyp * sin_val, 1)
            eq_typst = f"theta = {theta}^circle, quad \"hypotenuse = \" {hyp}, quad \"opposite (x) = ?\""
            ans_typst = f"x approx {ans_num:.1f}"

            steps = [
                "Identify sides relative to angle $ theta $: opposite side is $ x $, hypotenuse is $ {hyp} $.",
                "Select sine ratio: $ sin(theta) = text(\"opposite\") / text(\"hypotenuse\") $",
                f"Substitute given values: $ sin({theta}^circle) = x / {hyp} $",
                f"Solve for $ x $: $ x = {hyp} dot sin({theta}^circle) $",
                f"Compute: $ {hyp} dot {sin_val:.4f} approx {ans_num:.1f} $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"x approx {round(hyp * math.cos(math.radians(theta)), 1):.1f}"
            d2 = f"x approx {round(hyp / sin_val, 1):.1f}"
            d3 = f"x approx {round(ans_num + 3.2, 1):.1f}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append("x = 10.0")

        return BaseProblem(
            id=f"geom_trig_med_{problem_idx}",
            prompt_text="Find the missing side x in the right triangle. Round your answer to the nearest tenth if necessary.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"theta": theta}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Finding a missing acute angle in a right triangle given two sides using inverse trig."""
        # Setup: opp & adj (arctan), opp & hyp (arcsin), or adj & hyp (arccos)
        case = rng.choice(["arctan", "arcsin", "arccos"])

        if case == "arctan":
            opp = rng.choice([3, 5, 7, 8, 9, 11, 14])
            adj = rng.choice([4, 6, 8, 10, 12, 15])
            while opp == adj:
                adj = rng.choice([4, 6, 8, 10, 12, 15])
            ratio = opp / adj
            angle_deg = round(math.degrees(math.atan(ratio)), 1)

            eq_typst = f"\"opposite = \" {opp}, quad \"adjacent = \" {adj}, quad theta = ?"
            ans_typst = f"theta approx {angle_deg:.1f}^circle"

            steps = [
                "Identify given sides relative to angle $ theta $: opposite is $ {opp} $, adjacent is $ {adj} $.",
                "Select tangent ratio: $ tan(theta) = text(\"opposite\") / text(\"adjacent\") = {opp} / {adj} $",
                f"Calculate ratio: $ tan(theta) = {ratio:.4f} $",
                f"Apply inverse tangent: $ theta = arctan({ratio:.4f}) $",
                f"Compute angle measure: $ theta approx {angle_deg:.1f}^circle $",
                f"Result: $ {ans_typst} $"
            ]

            comp_angle = round(90.0 - angle_deg, 1)
            inv_ratio_angle = round(math.degrees(math.atan(adj / opp)), 1)
            d1 = f"theta approx {comp_angle:.1f}^circle"
            d2 = f"theta approx {inv_ratio_angle:.1f}^circle"
            d3 = f"theta approx {round(angle_deg + 4.5, 1):.1f}^circle"

        elif case == "arcsin":
            hyp = rng.choice([10, 13, 15, 17, 20, 25])
            opp = rng.choice([5, 7, 8, 9, 12, 15])
            while opp >= hyp:
                opp = hyp - rng.choice([2, 3, 5])
            ratio = opp / hyp
            angle_deg = round(math.degrees(math.asin(ratio)), 1)

            eq_typst = f"\"opposite = \" {opp}, quad \"hypotenuse = \" {hyp}, quad theta = ?"
            ans_typst = f"theta approx {angle_deg:.1f}^circle"

            steps = [
                "Identify given sides relative to angle $ theta $: opposite is $ {opp} $, hypotenuse is $ {hyp} $.",
                "Select sine ratio: $ sin(theta) = text(\"opposite\") / text(\"hypotenuse\") = {opp} / {hyp} $",
                f"Calculate ratio: $ sin(theta) = {ratio:.4f} $",
                f"Apply inverse sine: $ theta = arcsin({ratio:.4f}) $",
                f"Compute angle measure: $ theta approx {angle_deg:.1f}^circle $",
                f"Result: $ {ans_typst} $"
            ]

            comp_angle = round(90.0 - angle_deg, 1)
            d1 = f"theta approx {comp_angle:.1f}^circle"
            d2 = f"theta approx {round(math.degrees(math.acos(ratio)), 1):.1f}^circle"
            d3 = f"theta approx {round(angle_deg + 5.0, 1):.1f}^circle"

        else:  # arccos
            hyp = rng.choice([10, 13, 15, 17, 20, 25])
            adj = rng.choice([5, 6, 8, 9, 12, 14])
            while adj >= hyp:
                adj = hyp - rng.choice([2, 3, 4])
            ratio = adj / hyp
            angle_deg = round(math.degrees(math.acos(ratio)), 1)

            eq_typst = f"\"adjacent = \" {adj}, quad \"hypotenuse = \" {hyp}, quad theta = ?"
            ans_typst = f"theta approx {angle_deg:.1f}^circle"

            steps = [
                "Identify given sides relative to angle $ theta $: adjacent is $ {adj} $, hypotenuse is $ {hyp} $.",
                "Select cosine ratio: $ cos(theta) = text(\"adjacent\") / text(\"hypotenuse\") = {adj} / {hyp} $",
                f"Calculate ratio: $ cos(theta) = {ratio:.4f} $",
                f"Apply inverse cosine: $ theta = arccos({ratio:.4f}) $",
                f"Compute angle measure: $ theta approx {angle_deg:.1f}^circle $",
                f"Result: $ {ans_typst} $"
            ]

            comp_angle = round(90.0 - angle_deg, 1)
            d1 = f"theta approx {comp_angle:.1f}^circle"
            d2 = f"theta approx {round(math.degrees(math.asin(ratio)), 1):.1f}^circle"
            d3 = f"theta approx {round(angle_deg + 4.8, 1):.1f}^circle"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append("theta approx 45.0^circle")

        return BaseProblem(
            id=f"geom_trig_spicy_{problem_idx}",
            prompt_text="Find the measure of the indicated acute angle theta. Round your answer to the nearest tenth of a degree.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"case": case, "angle_deg": angle_deg}
        )
