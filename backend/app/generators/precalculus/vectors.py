from __future__ import annotations

import math
import random
from typing import Tuple

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


def simplify_radical(n: int) -> Tuple[int, int]:
    """Given positive integer n, return (k, p) such that sqrt(n) = k * sqrt(p) with square-free p."""
    k = 1
    p = n
    d = 2
    while d * d <= p:
        while p % (d * d) == 0:
            k *= d
            p //= (d * d)
        d += 1
    return k, p


def format_radical(k: int, p: int) -> str:
    """Format k * sqrt(p) into Typst syntax."""
    if p == 1:
        return f"{k}"
    if k == 1:
        return f"sqrt({p})"
    return f"{k} sqrt({p})"


class PrecalcVectorsGenerator(BaseGenerator):
    generator_id = "precalculus.vectors"
    name = "Vectors (Magnitude, Operations, Dot Product)"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSN.VM.B.4", "CCSS.MATH.CONTENT.HSN.VM.B.5"]

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
        """Mild: Vector magnitude ||v|| with EXACT simplified radical form."""
        # Pick components that yield interesting simplified radicals or perfect squares
        pairs = [
            (3, 3), (4, 4), (3, 6), (2, 4), (4, 8), (2, 6), (3, 9),
            (3, 4), (5, 12), (6, 8), (8, 15), (7, 24),
            (1, 5), (2, 5), (4, 7), (5, 5), (6, 7), (4, 6)
        ]
        a, b = rng.choice(pairs)
        if rng.choice([True, False]):
            a = -a
        if rng.choice([True, False]):
            b = -b

        eq_typst = f"bold(v) = chevron.l {a}, {b} chevron.r"
        mag_sq = a * a + b * b
        k, p = simplify_radical(mag_sq)
        ans_val = format_radical(k, p)
        ans_typst = f"norm(bold(v)) = {ans_val}"

        steps = [
            "Recall vector magnitude formula: $ norm(bold(v)) = sqrt(v_1^2 + v_2^2) $",
            f"Substitute components: $ norm(bold(v)) = sqrt(({a})^2 + ({b})^2) = sqrt({a*a} + {b*b}) = sqrt({mag_sq}) $"
        ]

        if p == 1:
            steps.append(f"Evaluate exact integer square root: $ sqrt({mag_sq}) = {k} $")
        elif k > 1:
            steps.append(f"Factor out largest perfect square: $ sqrt({mag_sq}) = sqrt({k*k} dot {p}) = {k} sqrt({p}) $")
        else:
            steps.append(f"Radicand {mag_sq} has no square factors greater than 1: $ sqrt({mag_sq}) $")

        steps.append(f"Simplified magnitude: $ {ans_typst} $")

        if k > 1 and p > 1:
            distractors = [
                f"norm(bold(v)) = sqrt({mag_sq})",
                f"norm(bold(v)) = {p} sqrt({k})",
                f"norm(bold(v)) = {abs(a) + abs(b)}"
            ]
        elif p == 1:
            distractors = [
                f"norm(bold(v)) = sqrt({mag_sq})",
                f"norm(bold(v)) = {k + 2}",
                f"norm(bold(v)) = {abs(a) + abs(b)}"
            ]
        else:
            distractors = [
                f"norm(bold(v)) = {mag_sq}",
                f"norm(bold(v)) = {abs(a) + abs(b)}",
                f"norm(bold(v)) = sqrt({mag_sq + 2})"
            ]

        return BaseProblem(
            id=f"pcalc_vec_mild_{problem_idx}",
            prompt_text="Find the magnitude of the vector. Write your answer in exact simplified radical form.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Dot product u . v and angle theta between vectors using cos(theta) = (u . v) / (||u|| ||v||)."""
        # Select nice vector pairs with known angles or clean coordinates
        special_pairs = [
            ((1, 0), (0, 1), 0, "90 degree"),
            ((2, 0), (0, -3), 0, "90 degree"),
            ((3, 4), (-4, 3), 0, "90 degree"),
            ((1, 1), (0, 1), 1, "45 degree"),
            ((1, 1), (1, 0), 1, "45 degree"),
            ((1, math.sqrt(3)), (1, 0), 1, "60 degree"),
            ((2, 2), (-2, -2), -8, "180 degree"),
            ((3, 1), (2, 4), 10, "approx 37.9 degree"),
            ((2, 3), (4, -1), 5, "approx 67.4 degree"),
            ((1, 3), (-2, 4), 10, "approx 36.9 degree"),
            ((4, 2), (1, -2), 0, "90 degree"),
            ((3, -1), (2, 6), 0, "90 degree"),
        ]

        choice = rng.choice(special_pairs)
        (u1, u2_val), (v1, v2_val), dot_val, angle_str = choice

        # Format components to integer if int
        u2 = int(round(u2_val)) if abs(round(u2_val) - u2_val) < 1e-6 else u2_val
        v2 = int(round(v2_val)) if abs(round(v2_val) - v2_val) < 1e-6 else v2_val

        u_sq = u1 * u1 + u2 * u2
        v_sq = v1 * v1 + v2 * v2
        ku, pu = simplify_radical(int(u_sq))
        kv, pv = simplify_radical(int(v_sq))
        mag_u_str = format_radical(ku, pu)
        mag_v_str = format_radical(kv, pv)

        eq_typst = f"bold(u) = chevron.l {u1}, {u2} chevron.r, quad bold(v) = chevron.l {v1}, {v2} chevron.r"
        ans_typst = f"bold(u) dot bold(v) = {dot_val}, quad theta = {angle_str}"

        steps = [
            f"Compute dot product: $ bold(u) dot bold(v) = ({u1})({v1}) + ({u2})({v2}) = {u1*v1} + {u2*v2} = {dot_val} $",
            f"Compute magnitudes: $ norm(bold(u)) = sqrt(({u1})^2 + ({u2})^2) = {mag_u_str} $, quad $ norm(bold(v)) = sqrt(({v1})^2 + ({v2})^2) = {mag_v_str} $",
            "Apply formula: $ cos(theta) = (bold(u) dot bold(v)) / (norm(bold(u)) norm(bold(v))) $",
            f"Substitute values: $ cos(theta) = ({dot_val}) / ({mag_u_str} dot {mag_v_str}) $",
            f"Find angle: $ theta = {angle_str} $"
        ]

        distractors = [
            f"bold(u) dot bold(v) = {dot_val}, quad theta = 45 degree" if "45" not in angle_str else f"bold(u) dot bold(v) = {dot_val}, quad theta = 90 degree",
            f"bold(u) dot bold(v) = {dot_val + 2}, quad theta = {angle_str}",
            f"bold(u) dot bold(v) = {u1*v1 - u2*v2}, quad theta = 60 degree"
        ]

        return BaseProblem(
            id=f"pcalc_vec_med_{problem_idx}",
            prompt_text="Find the dot product bold(u) dot bold(v) and the angle theta between the two vectors.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Unit vector in direction of v (v / ||v||) and linear combinations a*u + b*v."""
        subtype = rng.choice(["unit_vector", "linear_comb"])

        if subtype == "unit_vector":
            # Unit vector v / ||v||
            pairs = [(3, 4), (5, 12), (1, 1), (1, 2), (2, 3), (1, 3), (6, 8)]
            vx, vy = rng.choice(pairs)
            if rng.choice([True, False]):
                vx = -vx
            if rng.choice([True, False]):
                vy = -vy

            sq = vx * vx + vy * vy
            k, p = simplify_radical(sq)
            mag_str = format_radical(k, p)

            eq_typst = f"bold(v) = chevron.l {vx}, {vy} chevron.r"
            ans_typst = f"bold(u) = 1/({mag_str}) chevron.l {vx}, {vy} chevron.r"

            steps = [
                "Recall unit vector formula: $ bold(u) = bold(v) / (norm(bold(v))) $",
                f"Calculate magnitude: $ norm(bold(v)) = sqrt(({vx})^2 + ({vy})^2) = sqrt({sq}) = {mag_str} $",
                f"Divide each component by magnitude: $ bold(u) = 1/({mag_str}) chevron.l {vx}, {vy} chevron.r $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"bold(u) = 1/({sq}) chevron.l {vx}, {vy} chevron.r",
                f"bold(u) = chevron.l {vx}, {vy} chevron.r",
                f"bold(u) = 1/({mag_str}) chevron.l {-vx}, {vy} chevron.r"
            ]

            prompt = "Find a unit vector bold(u) in the direction of the given vector bold(v)."
        else:
            # Linear combination: c*u + d*v
            u1, u2 = rng.choice([-4, -3, -2, 2, 3, 4]), rng.choice([-3, -2, 1, 2, 3, 5])
            v1, v2 = rng.choice([-3, -2, 1, 2, 3, 4]), rng.choice([-4, -2, 2, 3, 4])
            c = rng.choice([2, 3, -2, -3])
            d = rng.choice([2, 3, 4, -2])

            ans_x = c * u1 + d * v1
            ans_y = c * u2 + d * v2

            eq_typst = f"bold(u) = chevron.l {u1}, {u2} chevron.r, quad bold(v) = chevron.l {v1}, {v2} chevron.r; quad \"Find \" {c} bold(u) + ({d}) bold(v)" if d < 0 else f"bold(u) = chevron.l {u1}, {u2} chevron.r, quad bold(v) = chevron.l {v1}, {v2} chevron.r; quad \"Find \" {c} bold(u) + {d} bold(v)"
            ans_typst = f"chevron.l {ans_x}, {ans_y} chevron.r"

            steps = [
                f"Write out the linear combination: $ {c} chevron.l {u1}, {u2} chevron.r + ({d}) chevron.l {v1}, {v2} chevron.r $" if d < 0 else f"Write out the linear combination: $ {c} chevron.l {u1}, {u2} chevron.r + {d} chevron.l {v1}, {v2} chevron.r $",
                f"Multiply each vector by its scalar: $ chevron.l {c*u1}, {c*u2} chevron.r + chevron.l {d*v1}, {d*v2} chevron.r $",
                f"Add corresponding components: $ chevron.l ({c*u1}) + ({d*v1}), ({c*u2}) + ({d*v2}) chevron.r $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"chevron.l {c*u1 + v1}, {c*u2 + v2} chevron.r",
                f"chevron.l {ans_x + 2}, {ans_y - 2} chevron.r",
                f"chevron.l {c*u1 - d*v1}, {c*u2 - d*v2} chevron.r"
            ]

            prompt = "Find the specified linear combination of vectors."

        return BaseProblem(
            id=f"pcalc_vec_spicy_{problem_idx}",
            prompt_text=prompt,
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
