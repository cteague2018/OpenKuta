from __future__ import annotations

import math
import random
from typing import List, Tuple

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


def simplify_radical(n: int) -> Tuple[int, int]:
    """Simplify sqrt(n) -> outside * sqrt(inside) where inside is square-free."""
    if n <= 0:
        return 0, 0
    outside = 1
    d = 2
    temp = n
    while d * d <= temp:
        while temp % (d * d) == 0:
            outside *= d
            temp //= (d * d)
        d += 1
    inside = temp
    return outside, inside


def format_radical_typst(outside: int, inside: int) -> str:
    """Format simplified radical for Typst math syntax."""
    if inside == 1:
        return str(outside)
    if outside == 1:
        return f"sqrt({inside})"
    return f"{outside} sqrt({inside})"


def format_fraction_typst(num: int, den: int) -> str:
    """Format fraction cleanly for Typst math."""
    if den == 0:
        return "undefined"
    if den < 0:
        num = -num
        den = -den
    g = math.gcd(abs(num), den)
    num //= g
    den //= g
    if den == 1:
        return str(num)
    if num < 0:
        return f"-{abs(num)}/{den}"
    return f"{num}/{den}"


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


class CoordinateGeometryGenerator(BaseGenerator):
    generator_id = "geometry.coordinate_geometry"
    name = "Coordinate Geometry (Distance, Midpoint & Slope)"
    category = "Geometry"
    standards = ["CCSS.MATH.CONTENT.HSG.GPE.B.7", "CCSS.MATH.CONTENT.HSG.GPE.B.5"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            return self._generate_mild(rng, problem_idx, allow_negatives)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_medium(rng, problem_idx, allow_negatives)
        else:
            return self._generate_spicy(rng, problem_idx, allow_negatives)

    def _generate_mild(self, rng: random.Random, problem_idx: int, allow_negatives: bool) -> BaseProblem:
        """Mild: Midpoint or slope between two integer coordinate points."""
        subflavor = rng.choice(["midpoint", "slope"])

        coord_range = list(range(-8, 9)) if allow_negatives else list(range(0, 11))

        if subflavor == "midpoint":
            x1 = rng.choice(coord_range)
            y1 = rng.choice(coord_range)
            x2 = rng.choice(coord_range)
            y2 = rng.choice(coord_range)

            # Ensure distinct points
            while x1 == x2 and y1 == y2:
                x2 = rng.choice(coord_range)
                y2 = rng.choice(coord_range)

            xm_str = format_fraction_typst(x1 + x2, 2)
            ym_str = format_fraction_typst(y1 + y2, 2)
            ans_typst = f"$ ({xm_str}, {ym_str}) $"

            # Step-by-step
            steps = [
                "Use the midpoint formula: $ M = ((x_1 + x_2)/2, (y_1 + y_2)/2) $",
                f"Substitute the coordinates $ ({x1}, {y1}) $ and $ ({x2}, {y2}) $:",
                f"$ M = (({x1} + ({x2}))/2, ({y1} + ({y2}))/2) $",
                f"Simplify x-coordinate: $ ({x1 + x2})/2 = {xm_str} $",
                f"Simplify y-coordinate: $ ({y1 + y2})/2 = {ym_str} $",
                f"Result: $ M = ({xm_str}, {ym_str}) $"
            ]

            d1 = f"$ ({format_fraction_typst(x2 - x1, 2)}, {format_fraction_typst(y2 - y1, 2)}) $"
            d2 = f"$ ({x1 + x2}, {y1 + y2}) $"
            d3 = f"$ ({ym_str}, {xm_str}) $"
            d4 = f"$ ({format_fraction_typst(-(x1 + x2), 2)}, {format_fraction_typst(-(y1 + y2), 2)}) $"
            d5 = f"$ ({format_fraction_typst(x1 + x2 + 2, 2)}, {format_fraction_typst(y1 + y2 - 2, 2)}) $"

            distractors = ensure_distractors(
                [d1, d2, d3, d4],
                ans_typst,
                [d5, "$ (0, 0) $", "$ (1, 1) $", "$ (-1, -1) $"]
            )

            return BaseProblem(
                id=f"coord_geom_mild_{problem_idx}",
                prompt_text="Find the midpoint of the line segment joining the two points.",
                equation_typst=f"$ ({x1}, {y1}) \" and \" ({x2}, {y2}) $",
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

        else:
            # Slope: m = (y2 - y1) / (x2 - x1)
            x1 = rng.choice(coord_range)
            y1 = rng.choice(coord_range)
            x2 = rng.choice(coord_range)
            while x2 == x1:
                x2 = rng.choice(coord_range)
            y2 = rng.choice(coord_range)

            dy = y2 - y1
            dx = x2 - x1
            m_str = format_fraction_typst(dy, dx)
            ans_typst = f"$ m = {m_str} $"

            steps = [
                "Use the slope formula: $ m = (y_2 - y_1) / (x_2 - x_1) $",
                f"Substitute the coordinates $ ({x1}, {y1}) $ and $ ({x2}, {y2}) $:",
                f"$ m = ({y2} - ({y1})) / ({x2} - ({x1})) $",
                f"Calculate differences: $ m = {dy} / {dx} $",
                f"Simplify the fraction: $ m = {m_str} $"
            ]

            d1 = f"$ m = {format_fraction_typst(dx, dy)} $" if dy != 0 else "$ m = 1 $"
            d2 = f"$ m = {format_fraction_typst(-dy, dx)} $"
            d3 = f"$ m = {format_fraction_typst(y2 + y1, x2 + x1)} $" if (x2 + x1) != 0 else "$ m = 0 $"
            d4 = f"$ m = {format_fraction_typst(dy + 1, dx)} $"
            d5 = f"$ m = {format_fraction_typst(dy - 1, dx)} $"

            distractors = ensure_distractors(
                [d1, d2, d3, d4],
                ans_typst,
                [d5, "$ m = 0 $", "$ m = 1 $", "$ m = -1 $", "$ m = 2 $"]
            )

            return BaseProblem(
                id=f"coord_geom_mild_{problem_idx}",
                prompt_text="Find the slope of the line passing through the two points.",
                equation_typst=f"$ ({x1}, {y1}) \" and \" ({x2}, {y2}) $",
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.MILD,
                standards=self.standards
            )

    def _generate_medium(self, rng: random.Random, problem_idx: int, allow_negatives: bool) -> BaseProblem:
        """Medium: Exact distance formula simplifying square roots into exact radical form or clean integers."""
        coord_range = list(range(-10, 11)) if allow_negatives else list(range(1, 15))

        flavor = rng.choice(["integer", "simplifying_radical", "prime_radical"])

        if flavor == "integer":
            triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
            dx, dy, d_val = rng.choice(triples)
            if rng.choice([True, False]):
                dx, dy = dy, dx
        elif flavor == "simplifying_radical":
            pairs = [(1, 7), (2, 4), (2, 6), (3, 6), (4, 4), (5, 5), (3, 9), (2, 8), (4, 8), (6, 8)]
            dx, dy = rng.choice(pairs)
        else:
            pairs = [(2, 3), (2, 5), (3, 4), (1, 4), (1, 6), (3, 5), (4, 5), (2, 7)]
            dx, dy = rng.choice(pairs)

        x1 = rng.choice(coord_range)
        y1 = rng.choice(coord_range)
        x2 = x1 + (dx if rng.choice([True, False]) else -dx)
        y2 = y1 + (dy if rng.choice([True, False]) else -dy)

        diff_x = x2 - x1
        diff_y = y2 - y1
        d_sq = diff_x**2 + diff_y**2
        outside, inside = simplify_radical(d_sq)
        rad_str = format_radical_typst(outside, inside)
        ans_typst = f"$ d = {rad_str} $"

        steps = [
            "Use the distance formula: $ d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2) $",
            f"Substitute the coordinates $ ({x1}, {y1}) $ and $ ({x2}, {y2}) $:",
            f"$ d = sqrt(({x2} - ({x1}))^2 + ({y2} - ({y1}))^2) $",
            f"Calculate the differences: $ d = sqrt(({diff_x})^2 + ({diff_y})^2) $",
            f"Square each term: $ d = sqrt({diff_x**2} + {diff_y**2}) = sqrt({d_sq}) $"
        ]

        if inside == 1:
            steps.append(f"Evaluate the square root: $ d = {outside} $")
        elif outside > 1:
            steps.append(f"Factor out perfect square $ {outside}^2 = {outside**2} $: $ d = sqrt({outside**2} dot {inside}) = {rad_str} $")
        else:
            steps.append(f"$ {d_sq} $ has no square factors, so the radical is already simplified.")
        steps.append(f"Result: {ans_typst}")

        # Distractors
        d1 = f"$ d = {abs(diff_x) + abs(diff_y)} $"
        d2 = f"$ d = sqrt({d_sq}) $" if outside > 1 else f"$ d = {d_sq} $"
        d3 = f"$ d = {inside} sqrt({outside}) $" if (outside > 1 and inside > 1) else f"$ d = {outside + 2} $"
        d4 = f"$ d = {format_radical_typst(outside + 1, inside)} $"
        d5 = f"$ d = {format_radical_typst(outside, inside + 2)} $"

        distractors = ensure_distractors(
            [d1, d2, d3, d4],
            ans_typst,
            [d5, f"$ d = {outside + 1} $", f"$ d = {outside * 2} $", "$ d = sqrt(2) $"]
        )

        return BaseProblem(
            id=f"coord_geom_med_{problem_idx}",
            prompt_text="Find the distance between the two points. Express your answer in simplest radical form.",
            equation_typst=f"$ ({x1}, {y1}) \" and \" ({x2}, {y2}) $",
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int, allow_negatives: bool) -> BaseProblem:
        """Spicy: Missing endpoint given midpoint and one endpoint, or distance with larger coordinates."""
        subflavor = rng.choice(["missing_endpoint", "large_distance"])

        if subflavor == "missing_endpoint":
            span = list(range(-15, 16)) if allow_negatives else list(range(0, 20))
            x1 = rng.choice(span)
            y1 = rng.choice(span)
            x2 = rng.choice(span)
            y2 = rng.choice(span)
            while x1 == x2 and y1 == y2:
                x2 = rng.choice(span)
                y2 = rng.choice(span)

            if (x1 + x2) % 2 != 0:
                x2 += 1
            if (y1 + y2) % 2 != 0:
                y2 += 1

            xm = (x1 + x2) // 2
            ym = (y1 + y2) // 2

            ans_typst = f"$ ({x2}, {y2}) $"

            steps = [
                "Let the unknown endpoint be $ B(x_2, y_2) $.",
                "Recall the midpoint formula: $ M = ((x_1 + x_2)/2, (y_1 + y_2)/2) $",
                f"Set up equation for x: $ ({x1} + x_2)/2 = {xm} implies {x1} + x_2 = {2 * xm} implies x_2 = {x2} $",
                f"Set up equation for y: $ ({y1} + y_2)/2 = {ym} implies {y1} + y_2 = {2 * ym} implies y_2 = {y2} $",
                f"Result: The coordinates of endpoint B are {ans_typst}"
            ]

            d1 = f"$ ({format_fraction_typst(x1 + xm, 2)}, {format_fraction_typst(y1 + ym, 2)}) $"
            d2 = f"$ ({2 * xm + x1}, {2 * ym + y1}) $"
            d3 = f"$ ({y2}, {x2}) $"
            d4 = f"$ ({xm - x1}, {ym - y1}) $"
            d5 = f"$ ({x2 + 2}, {y2 - 2}) $"

            distractors = ensure_distractors(
                [d1, d2, d3, d4],
                ans_typst,
                [d5, f"$ ({-x2}, {-y2}) $", f"$ ({x1}, {y1}) $", "$ (0, 0) $"]
            )

            return BaseProblem(
                id=f"coord_geom_spicy_{problem_idx}",
                prompt_text="Given endpoint A and midpoint M of line segment AB, find the coordinates of endpoint B.",
                equation_typst=f"$ A({x1}, {y1}), quad M({xm}, {ym}) $",
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )

        else:
            k = rng.choice([2, 3, 4, 5, 6, 7])
            base_dx, base_dy = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (2, 5), (3, 4)])
            dx = base_dx * k
            dy = base_dy * k

            x1 = rng.randint(-30, 20)
            y1 = rng.randint(-30, 20)
            x2 = x1 + (dx if rng.choice([True, False]) else -dx)
            y2 = y1 + (dy if rng.choice([True, False]) else -dy)

            diff_x = x2 - x1
            diff_y = y2 - y1
            d_sq = diff_x**2 + diff_y**2
            outside, inside = simplify_radical(d_sq)
            rad_str = format_radical_typst(outside, inside)
            ans_typst = f"$ d = {rad_str} $"

            steps = [
                "Use the distance formula: $ d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2) $",
                f"Substitute the coordinates $ ({x1}, {y1}) $ and $ ({x2}, {y2}) $:",
                f"$ d = sqrt(({x2} - ({x1}))^2 + ({y2} - ({y1}))^2) $",
                f"Calculate the differences: $ d = sqrt(({diff_x})^2 + ({diff_y})^2) $",
                f"Square and sum: $ d = sqrt({diff_x**2} + {diff_y**2}) = sqrt({d_sq}) $"
            ]

            if inside == 1:
                steps.append(f"Evaluate the square root: $ d = {outside} $")
            elif outside > 1:
                steps.append(f"Simplify by factoring out perfect square $ {outside}^2 = {outside**2} $: $ d = sqrt({outside**2} dot {inside}) = {rad_str} $")
            else:
                steps.append(f"$ {d_sq} $ is square-free, so the radical cannot be simplified further.")
            steps.append(f"Result: {ans_typst}")

            d1 = f"$ d = {abs(diff_x) + abs(diff_y)} $"
            d2 = f"$ d = sqrt({d_sq}) $" if outside > 1 else f"$ d = {outside * 2} $"
            d3 = f"$ d = {format_radical_typst(outside + 1, inside)} $"
            d4 = f"$ d = {format_radical_typst(max(1, outside - 1), inside)} $"
            d5 = f"$ d = {inside} sqrt({outside}) $" if (outside > 1 and inside > 1) else f"$ d = {outside * 3} $"

            distractors = ensure_distractors(
                [d1, d2, d3, d4],
                ans_typst,
                [d5, f"$ d = {outside + 3} $", f"$ d = {d_sq} $", "$ d = 10 sqrt(2) $"]
            )

            return BaseProblem(
                id=f"coord_geom_spicy_{problem_idx}",
                prompt_text="Find the distance between the two points. Express your answer in simplest radical form.",
                equation_typst=f"$ ({x1}, {y1}) \" and \" ({x2}, {y2}) $",
                answer_typst=ans_typst,
                steps_typst=steps,
                distractors=distractors,
                difficulty=ProblemDifficulty.SPICY,
                standards=self.standards
            )
