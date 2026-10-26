from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class SpecialRightTrianglesGenerator(BaseGenerator):
    generator_id = "geometry.special_right_triangles"
    name = "Special Right Triangles (30-60-90 and 45-45-90)"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.SRT.C.8"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # 45-45-90 Triangle: legs = x, hypotenuse = x * sqrt(2)
            # Given leg, find hypotenuse
            x = rng.choice([3, 4, 5, 6, 7, 8, 9, 10])
            eq_typst = f"\"45-45-90 triangle with leg = \" {x}, quad \"hypotenuse \" c = ?"
            ans_typst = f"c = {x} sqrt(2)"

            steps = [
                "Recall properties of a 45-45-90 right triangle (isosceles right triangle):",
                "Side ratios are $ 1 : 1 : sqrt(2) $",
                "Hypotenuse formula: $ c = \"leg\" dot sqrt(2) $",
                f"Substitute known leg: $ c = {x} sqrt(2) $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [f"c = {x * 2}", f"c = {x} sqrt(3)", f"c = {x}"]

            return BaseProblem(
                id=f"geom_srt_mild_{problem_idx}",
                prompt_text="Find the missing side of each 45-45-90 special right triangle.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

        elif difficulty == ProblemDifficulty.MEDIUM:
            # 30-60-90 Triangle: short leg = x, long leg = x*sqrt(3), hypotenuse = 2x
            x = rng.choice([2, 3, 4, 5, 6, 7, 8])
            flavor = rng.choice(["given_short_find_all", "given_hyp_find_legs"])

            if flavor == "given_short_find_all":
                eq_typst = f"\"30-60-90 triangle with shorter leg (opposite 30^\\circle) = \" {x}"
                long_leg = f"{x} sqrt(3)"
                hyp = f"{2 * x}"
                ans_typst = f"\"longer leg = \" {long_leg}, quad \"hypotenuse = \" {hyp}"

                steps = [
                    "Recall 30-60-90 triangle side ratios: $ 1 : sqrt(3) : 2 $",
                    rf"Shorter leg (opposite 30^\circle) is $ x = {x} $",
                    rf"Longer leg (opposite 60^\circle) is $ x sqrt(3) = {long_leg} $",
                    rf"Hypotenuse (opposite 90^\circle) is $ 2x = 2({x}) = {hyp} $",
                    f"Result: $ {ans_typst} $"
                ]
                d1 = f"longer leg = {2*x}, hypotenuse = {x} sqrt(3)"
                d2 = f"longer leg = {x} sqrt(2), hypotenuse = {2*x}"
            else:
                h = 2 * x
                eq_typst = f"\"30-60-90 triangle with hypotenuse = \" {h}"
                short_leg = f"{x}"
                long_leg = f"{x} sqrt(3)"
                ans_typst = f"\"shorter leg = \" {short_leg}, quad \"longer leg = \" {long_leg}"

                steps = [
                    "Recall 30-60-90 triangle ratios: $ \"hypotenuse\" = 2 dot (\"shorter leg\") $",
                    f"Divide hypotenuse by 2: $ \"shorter leg\" = {h} / 2 = {x} $",
                    f"Multiply shorter leg by $ sqrt(3) $: $ \"longer leg\" = {long_leg} $",
                    f"Result: $ {ans_typst} $"
                ]
                d1 = f"shorter leg = {x} sqrt(3), longer leg = {x}"
                d2 = f"shorter leg = {h - 2}, longer leg = {h - 1}"

            return BaseProblem(
                id=f"geom_srt_med_{problem_idx}",
                prompt_text="Find the missing sides of each 30-60-90 special right triangle.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=[d1, d2],
                difficulty=ProblemDifficulty.MEDIUM,
                standards=self.standards
            )
        else:
            # Spicy: Given longer leg (which might be an integer or radical) or rationalizing denominator
            # e.g., 45-45-90 with hypotenuse = integer H => leg = H / sqrt(2) = H*sqrt(2)/2
            h = rng.choice([6, 8, 10, 12, 14, 16])
            half_h = h // 2
            eq_typst = f"\"45-45-90 triangle with hypotenuse = \" {h}, quad \"leg \" x = ?"
            ans_typst = f"x = {half_h} sqrt(2)"

            steps = [
                "Recall 45-45-90 ratio: $ \"hypotenuse\" = \"leg\" dot sqrt(2) $",
                f"Divide hypotenuse by $ sqrt(2) $: $ x = {h} / sqrt(2) $",
                "Rationalize the denominator by multiplying by $ sqrt(2) / sqrt(2) $:",
                f"$ x = ({h} dot sqrt(2)) / (sqrt(2) dot sqrt(2)) = ({h} sqrt(2)) / 2 $",
                f"Simplify fraction: $ x = {half_h} sqrt(2) $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [f"x = {h} sqrt(2)", f"x = {half_h}", f"x = {h - 2}"]

            return BaseProblem(
                id=f"geom_srt_spicy_{problem_idx}",
                prompt_text="Find the exact leg length of each special right triangle. Rationalize the denominator.",
                equation_typst=eq_typst,
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )
