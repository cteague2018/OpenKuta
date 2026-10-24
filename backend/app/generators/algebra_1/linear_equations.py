from __future__ import annotations

import random
from typing import List, Tuple
import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class LinearEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.linear_equations"
    name = "Slope & Linear Equations (y = mx + b)"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.HSA.CED.A.2",
        "CCSS.MATH.CONTENT.8.EE.B.6",
        "CCSS.MATH.CONTENT.HSF.LE.A.2",
        "TEKS.MATH.A1.2.B",
        "TEKS.MATH.A1.3.A"
    ]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            return self._generate_slope_from_points(rng, problem_idx, allow_negatives)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_slope_intercept(rng, problem_idx, allow_negatives)
        else:
            return self._generate_standard_to_slope_intercept(rng, problem_idx, allow_negatives)

    def _generate_slope_from_points(
        self, rng: random.Random, idx: int, allow_negatives: bool
    ) -> BaseProblem:
        """Find the slope of the line through each pair of points."""
        x1 = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)
        y1 = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)

        # Ensure x2 != x1 for non-infinite slope, or occasionally undefined
        dx = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        dy = rng.randint(-6, 6) if allow_negatives else rng.randint(1, 6)

        x2 = x1 + dx
        y2 = y1 + dy

        slope_rat = sp.Rational(dy, dx)
        if slope_rat.q == 1:
            slope_str = str(slope_rat.p)
        else:
            slope_str = f"{slope_rat.p}/{slope_rat.q}"

        eq_typst = f"({x1}, {y1}) quad \"and\" quad ({x2}, {y2})"
        ans_typst = f"m = {slope_str}"

        # Distractor misconceptions:
        # 1. Inverted slope dx / dy
        inv_rat = sp.Rational(dx, dy) if dy != 0 else sp.Integer(0)
        d1 = f"m = {inv_rat.p}/{inv_rat.q}" if inv_rat.q != 1 else f"m = {inv_rat.p}"
        # 2. Subtracted backward in one coordinate (sign flip)
        d2 = f"m = -{slope_str}" if not slope_str.startswith("-") else f"m = {slope_str[1:]}"
        # 3. Added instead of subtracted (x1+x2)/(y1+y2)
        d3 = f"m = {y1 + y2}/{x1 + x2}" if (x1 + x2) != 0 else "m = 1"

        steps = [
            f"Given points: $ (x_1, y_1) = ({x1}, {y1}) $ and $ (x_2, y_2) = ({x2}, {y2}) $",
            f"Use slope formula: $ m = (y_2 - y_1) / (x_2 - x_1) $",
            f"Substitute coordinates: $ m = ({y2} - ({y1})) / ({x2} - ({x1})) = {dy} / {dx} $",
            f"Simplify fraction: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"slope_mild_{idx}",
            prompt_text="Find the slope of the line through each pair of points.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"m": slope_str, "p1": (x1, y1), "p2": (x2, y2)}
        )

    def _generate_slope_intercept(
        self, rng: random.Random, idx: int, allow_negatives: bool
    ) -> BaseProblem:
        """Write the slope-intercept equation given a point and slope."""
        m_num = rng.choice([-3, -2, -1, 1, 2, 3])
        m_den = rng.choice([1, 2, 3, 4]) if rng.random() < 0.4 else 1
        m = sp.Rational(m_num, m_den)

        # Choose point (x1, y1)
        x1 = rng.randint(-6, 6) if allow_negatives else rng.randint(0, 8)
        # Ensure b is clean integer or simple fraction
        b = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)
        y1 = m * x1 + b

        m_str = f"{m.p}/{m.q}" if m.q != 1 else str(m.p)
        if m_str == "1":
            m_str_disp = ""
        elif m_str == "-1":
            m_str_disp = "-"
        else:
            m_str_disp = m_str

        b_sign = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
        ans_typst = f"y = {m_str_disp}x {b_sign}".strip()

        eq_typst = f"\"through:\" ({x1}, {y1}), quad \"slope =\" {m_str}"

        # Distractor misconceptions:
        # 1. Swapped x and y in point-slope: y - x1 = m(x - y1)
        wrong_b = x1 - m * y1
        d1 = f"y = {m_str_disp}x {'+ ' if wrong_b >= 0 else '- '}{abs(int(wrong_b))}"
        # 2. Subtracted m*x1 instead of adding
        d2 = f"y = {m_str_disp}x {'- ' if b >= 0 else '+ '}{abs(b)}"
        # 3. Flipped slope
        d3 = f"y = -{m_str_disp}x {b_sign}".strip()

        steps = [
            f"Point-slope form: $ y - y_1 = m(x - x_1) $",
            f"Substitute $ m = {m_str} $ and $ ({x1}, {y1}) $: $ y - ({y1}) = {m_str}(x - ({x1})) $",
            f"Distribute and isolate $y$: $ y = {m_str_disp}x {b_sign} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"slope_med_{idx}",
            prompt_text="Write the slope-intercept form of the equation of each line.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"m": m_str, "b": b}
        )

    def _generate_standard_to_slope_intercept(
        self, rng: random.Random, idx: int, allow_negatives: bool
    ) -> BaseProblem:
        """Convert standard form Ax + By = C to slope-intercept form y = mx + b."""
        B = rng.choice([2, 3, 4, 5, -2, -3])
        A = rng.choice([1, 2, 3, 4, 6, -1, -2, -3])
        # Choose C so C/B is integer or clean rational
        k = rng.randint(-6, 6)
        C = B * k

        m = sp.Rational(-A, B)
        b = sp.Rational(C, B)

        a_sign = f"{A}x" if A != 1 else "x"
        if A == -1:
            a_sign = "-x"
        b_term = f"+ {B}y" if B > 0 else f"- {abs(B)}y"
        eq_typst = f"{a_sign} {b_term} = {C}"

        m_str = f"{m.p}/{m.q}" if m.q != 1 else str(m.p)
        m_disp = "" if m_str == "1" else ("-" if m_str == "-1" else m_str)
        b_sign = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
        ans_typst = f"y = {m_disp}x {b_sign}".strip()

        # Distractor misconceptions:
        # 1. Forgot negative sign when moving Ax: m = A/B instead of -A/B
        wrong_m = sp.Rational(A, B)
        wm_str = f"{wrong_m.p}/{wrong_m.q}" if wrong_m.q != 1 else str(wrong_m.p)
        d1 = f"y = {wm_str}x {b_sign}".strip()
        # 2. Forgot to divide C by B: y = mx + C
        d2 = f"y = {m_disp}x {'+ ' if C > 0 else '- '}{abs(C)}".strip()
        # 3. Inverted fraction B/A
        d3 = f"y = {-B}/{A}x {b_sign}".strip()

        steps = [
            f"Given standard form: $ {eq_typst} $",
            f"Subtract $ {a_sign} $ from both sides: $ {B}y = -{A}x + {C} $",
            f"Divide all terms by $ {B} $: $ y = ({-A} / {B})x + ({C} / {B}) $",
            f"Slope-intercept form: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"slope_spicy_{idx}",
            prompt_text="Convert each standard form equation into slope-intercept form.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"A": A, "B": B, "C": C}
        )

