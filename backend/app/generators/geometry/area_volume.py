from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class GeometryAreaVolumeGenerator(BaseGenerator):
    generator_id = "geometry.area_volume"
    name = "Surface Area and Volume of Solids"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.GMD.A.3"]

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
        """Mild: Volume and surface area of rectangular prisms: V = l*w*h, SA = 2(lw + lh + wh)."""
        length = rng.choice([3, 4, 5, 6, 7, 8, 9, 10])
        w = rng.choice([2, 3, 4, 5, 6])
        h = rng.choice([3, 4, 6, 7, 8, 10])

        vol = length * w * h
        lw = length * w
        lh = length * h
        wh = w * h
        sum_faces = lw + lh + wh
        sa = 2 * sum_faces

        eq_typst = f"\"Rectangular Prism:\" quad l = {length}, quad w = {w}, quad h = {h}"
        ans_typst = f"V = {vol}, quad \"SA\" = {sa}"

        steps = [
            "Recall volume formula for a rectangular prism: $ V = l dot w dot h $",
            f"Calculate volume: $ V = ({length}) dot ({w}) dot ({h}) = {vol} $",
            "Recall surface area formula: $ \"SA\" = 2(l w + l h + w h) $",
            f"Calculate the areas of the three pairs of faces: $ l w = {lw}, quad l h = {lh}, quad w h = {wh} $",
            f"Sum face areas and double: $ 2({lw} + {lh} + {wh}) = 2({sum_faces}) = {sa} $",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: forgot to multiply by 2 for SA
        d1 = f"V = {vol}, quad \"SA\" = {sum_faces}"
        # Distractor 2: added dimensions instead of multiplying for V
        d2 = f"V = {2 * (length + w + h)}, quad \"SA\" = {sa}"
        # Distractor 3: arithmetic variation
        d3 = f"V = {vol + lw}, quad \"SA\" = {sa + 4}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"V = {vol + 10}, quad \"SA\" = {sa + 10}")

        return BaseProblem(
            id=f"geom_vol_mild_{problem_idx}",
            prompt_text="Find the volume and surface area of the rectangular prism.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"length": length, "width": w, "height": h, "volume": vol, "surface_area": sa}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Cylinders: V = pi * r^2 * h, SA = 2 * pi * r * h + 2 * pi * r^2, both in terms of pi."""
        r = rng.choice([2, 3, 4, 5, 6, 7, 8])
        h = rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])

        r2 = r * r
        vol = r2 * h
        lateral_area = 2 * r * h
        bases_area = 2 * r2
        sa = lateral_area + bases_area

        eq_typst = f"\"Right Cylinder:\" quad r = {r}, quad h = {h}"
        ans_typst = f"V = {vol} pi, quad \"SA\" = {sa} pi"

        steps = [
            "Recall volume formula for a right cylinder: $ V = pi r^2 h $",
            f"Calculate base area: $ B = pi r^2 = pi ({r})^2 = {r2} pi $",
            f"Multiply by height to find volume: $ V = ({r2} pi) dot ({h}) = {vol} pi $",
            "Recall surface area formula: $ \"SA\" = 2 pi r h + 2 pi r^2 $ (lateral area + two bases)",
            f"Calculate lateral area: $ 2 pi r h = 2 pi ({r})({h}) = {lateral_area} pi $",
            f"Calculate area of both circular bases: $ 2 pi r^2 = 2 pi ({r})^2 = {bases_area} pi $",
            f"Sum lateral and base areas: $ \"SA\" = {lateral_area} pi + {bases_area} pi = {sa} pi $",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: only counted 1 base in surface area
        d1 = f"V = {vol} pi, quad \"SA\" = {lateral_area + r2} pi"
        # Distractor 2: swapped volume and lateral area
        d2 = f"V = {lateral_area} pi, quad \"SA\" = {sa} pi"
        # Distractor 3: forgot pi or squaring radius
        d3 = f"V = {2 * r * h} pi, quad \"SA\" = {sa + 2 * r} pi"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"V = {vol + 4} pi, quad \"SA\" = {sa + 4} pi")

        return BaseProblem(
            id=f"geom_vol_med_{problem_idx}",
            prompt_text="Find the exact volume and surface area of the cylinder in terms of pi.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"radius": r, "height": h, "volume_pi": vol, "surface_area_pi": sa}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Right cones or spheres with exact answers in terms of pi."""
        solid_type = rng.choice(["cone", "sphere"])

        if solid_type == "cone":
            # Cone: V = 1/3 pi r^2 h, slant height s = sqrt(r^2 + h^2), SA = pi r s + pi r^2
            # Pythagorean triples ensure integer slant height s
            triple = rng.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15)])
            r, h, s = triple

            r2 = r * r
            r2h = r2 * h
            if r2h % 3 == 0:
                v_str = f"{r2h // 3} pi"
            else:
                v_str = f"({r2h} pi)/3"

            lateral_area = r * s
            base_area = r2
            sa = lateral_area + base_area

            eq_typst = f"\"Right Cone:\" quad r = {r}, quad h = {h}"
            ans_typst = f"V = {v_str}, quad \"SA\" = {sa} pi"

            steps = [
                "Find the slant height $ s $ using the Pythagorean Theorem: $ s = sqrt(r^2 + h^2) $",
                f"$ s = sqrt(({r})^2 + ({h})^2) = sqrt({r2} + {h*h}) = sqrt({r2 + h*h}) = {s} $",
                "Recall volume formula for a right cone: $ V = 1/3 pi r^2 h $",
                f"Calculate volume: $ V = 1/3 pi ({r})^2 ({h}) = 1/3 pi ({r2h}) = {v_str} $",
                "Recall surface area formula: $ \"SA\" = pi r s + pi r^2 $ (lateral area + base)",
                f"Calculate lateral area: $ pi r s = pi ({r})({s}) = {lateral_area} pi $",
                f"Calculate base area: $ pi r^2 = pi ({r})^2 = {base_area} pi $",
                f"Sum areas: $ \"SA\" = {lateral_area} pi + {base_area} pi = {sa} pi $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"V = {r2h} pi, quad \"SA\" = {sa} pi"  # forgot 1/3 in volume
            d2 = f"V = {v_str}, quad \"SA\" = {lateral_area} pi"  # forgot base in SA
            d3 = f"V = {v_str}, quad \"SA\" = {lateral_area + 2 * base_area} pi"  # added two bases

        else:
            # Sphere: V = 4/3 pi r^3, SA = 4 pi r^2
            r = rng.choice([3, 4, 5, 6, 7, 8, 9])
            r2 = r * r
            r3 = r * r2
            four_r3 = 4 * r3
            if four_r3 % 3 == 0:
                v_str = f"{four_r3 // 3} pi"
            else:
                v_str = f"({four_r3} pi)/3"

            sa = 4 * r2

            eq_typst = f"\"Sphere:\" quad r = {r}"
            ans_typst = f"V = {v_str}, quad \"SA\" = {sa} pi"

            steps = [
                "Recall volume formula for a sphere: $ V = 4/3 pi r^3 $",
                f"Substitute radius: $ V = 4/3 pi ({r})^3 = 4/3 pi ({r3}) = {v_str} $",
                "Recall surface area formula for a sphere: $ \"SA\" = 4 pi r^2 $",
                f"Substitute radius: $ \"SA\" = 4 pi ({r})^2 = 4 pi ({r2}) = {sa} pi $",
                f"Result: $ {ans_typst} $"
            ]

            d1 = f"V = {sa} pi, quad \"SA\" = {v_str}"  # swapped V and SA
            d2 = f"V = {v_str}, quad \"SA\" = {2 * r2} pi"  # forgot factor of 4
            d3 = f"V = ({r3} pi)/3, quad \"SA\" = {sa} pi"  # forgot factor of 4 in volume

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"V = {v_str}, quad \"SA\" = 50 pi")

        return BaseProblem(
            id=f"geom_vol_spicy_{problem_idx}",
            prompt_text=f"Find the exact volume and surface area of the {solid_type} in terms of pi.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"solid_type": solid_type, "radius": r}
        )
