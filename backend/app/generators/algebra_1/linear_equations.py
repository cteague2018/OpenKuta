from __future__ import annotations

import random
from typing import Any

import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_coordinate_plane, svg_coordinate_plane_pair


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
        self, rng: random.Random, problem_idx: int, allow_negatives: bool
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
            "Use slope formula: $ m = (y_2 - y_1) / (x_2 - x_1) $",
            f"Substitute coordinates: $ m = ({y2} - ({y1})) / ({x2} - ({x1})) = {dy} / {dx} $",
            f"Simplify fraction: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"slope_mild_{problem_idx}",
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
        self, rng: random.Random, problem_idx: int, allow_negatives: bool
    ) -> BaseProblem:
        """Write the slope-intercept equation given a point and slope."""
        m_num = rng.choice([-3, -2, -1, 1, 2, 3])
        m_den = rng.choice([1, 2, 3, 4]) if rng.random() < 0.4 else 1
        m: Any = sp.Rational(m_num, m_den)

        # Choose point (x1, y1)
        x1 = rng.randint(-6, 6) if allow_negatives else rng.randint(0, 8)
        # Ensure b is clean integer or simple fraction
        b = rng.randint(-8, 8) if allow_negatives else rng.randint(1, 8)
        y1: Any = m * x1 + b

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
            "Point-slope form: $ y - y_1 = m(x - x_1) $",
            f"Substitute $ m = {m_str} $ and $ ({x1}, {y1}) $: $ y - ({y1}) = {m_str}(x - ({x1})) $",
            f"Distribute and isolate $y$: $ y = {m_str_disp}x {b_sign} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"slope_med_{problem_idx}",
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
        self, rng: random.Random, problem_idx: int, allow_negatives: bool
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
            id=f"slope_spicy_{problem_idx}",
            prompt_text="Convert each standard form equation into slope-intercept form.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"A": A, "B": B, "C": C}
        )


class SlopeGenerator(BaseGenerator):
    generator_id = "algebra_1.slope"
    name = "Slope of a Line"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.8.EE.B.6", "TEKS.MATH.A1.3.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x1 = rng.randint(-8, 8) if allow_negatives else rng.randint(0, 8)
        y1 = rng.randint(-8, 8) if allow_negatives else rng.randint(0, 8)

        if difficulty == ProblemDifficulty.MILD:
            dx = rng.choice([-3, -2, -1, 1, 2, 3])
            dy = rng.choice([-6, -4, -3, -2, -1, 1, 2, 3, 4, 6])
        elif difficulty == ProblemDifficulty.MEDIUM:
            dx = rng.choice([-7, -5, -4, 4, 5, 7])
            dy = rng.randint(-9, 9)
        else:  # SPICY
            if rng.random() < 0.35:
                dx = 0
                dy = rng.choice([-5, -3, 3, 5])
            elif rng.random() < 0.7:
                dx = rng.choice([-6, -4, 4, 6])
                dy = 0
            else:
                dx = rng.choice([-9, -8, 8, 9])
                dy = rng.choice([-7, -5, 5, 7])

        x2 = x1 + dx
        y2 = y1 + dy
        eq_typst = f"({x1}, {y1}) quad \"and\" quad ({x2}, {y2})"

        if dx == 0:
            ans_typst = "Undefined"
            steps = [
                f"Given coordinates: $ ({x1}, {y1}) $ and $ ({x2}, {y2}) $",
                "Slope formula: $ m = (y_2 - y_1) / (x_2 - x_1) $",
                f"Calculate: $ m = ({y2} - ({y1})) / ({x2} - ({x1})) = {dy} / 0 $",
                "Division by zero is undefined.",
                "Result: Undefined"
            ]
            distractors = ["m = 0", f"m = {dy}", "m = 1"]
        elif dy == 0:
            ans_typst = "m = 0"
            steps = [
                f"Given coordinates: $ ({x1}, {y1}) $ and $ ({x2}, {y2}) $",
                "Slope formula: $ m = (y_2 - y_1) / (x_2 - x_1) $",
                f"Calculate: $ m = ({y2} - ({y1})) / ({x2} - ({x1})) = 0 / {dx} = 0 $",
                "Result: $ m = 0 $"
            ]
            distractors = ["Undefined", f"m = {dx}", "m = 1"]
        else:
            rat = sp.Rational(dy, dx)
            slope_s = str(rat.p) if rat.q == 1 else f"{rat.p}/{rat.q}"
            ans_typst = f"m = {slope_s}"
            steps = [
                f"Given coordinates: $ ({x1}, {y1}) $ and $ ({x2}, {y2}) $",
                "Slope formula: $ m = (y_2 - y_1) / (x_2 - x_1) $",
                f"Calculate: $ m = ({y2} - ({y1})) / ({x2} - ({x1})) = {dy} / {dx} $",
                f"Simplify fraction: $ m = {slope_s} $"
            ]
            inv_rat = sp.Rational(dx, dy) if dy != 0 else sp.Integer(0)
            d1 = f"m = {inv_rat.p}/{inv_rat.q}" if inv_rat.q != 1 else f"m = {inv_rat.p}"
            d2 = f"m = -{slope_s}" if not slope_s.startswith("-") else f"m = {slope_s[1:]}"
            d3 = "m = 0" if rat != 0 else "m = 1"
            distractors = [d1, d2, d3]

        if dx == 0:
            diag_svg = svg_coordinate_plane(
                lines=[{"x_vert": float(x1), "color": "#2563eb"}],
                points=[
                    {"x": x1, "y": y1, "color": "#dc2626", "label": f"({x1},{y1})"},
                    {"x": x2, "y": y2, "color": "#dc2626", "label": f"({x2},{y2})"},
                ],
            )
        else:
            m_fl = dy / dx
            b_fl = y1 - m_fl * x1
            diag_svg = svg_coordinate_plane(
                lines=[{"m": m_fl, "b": b_fl, "color": "#2563eb"}],
                points=[
                    {"x": x1, "y": y1, "color": "#dc2626", "label": f"({x1},{y1})"},
                    {"x": x2, "y": y2, "color": "#dc2626", "label": f"({x2},{y2})"},
                ],
            )

        return BaseProblem(
            id=f"slope_{difficulty.value}_{problem_idx}",
            prompt_text="Find the slope of the line through each pair of points.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $" if "m =" in ans_typst else ans_typst,
            steps_typst=steps,
            distractors=[f"$ {d} $" if "m =" in d else d for d in distractors],
            difficulty=difficulty,
            standards=self.standards,
            diagram_svg=None,
            answer_svg=diag_svg,
            metadata={"m": ans_typst, "p1": (x1, y1), "p2": (x2, y2)}
        )


class GraphingLinesGenerator(BaseGenerator):
    generator_id = "algebra_1.graphing_lines"
    name = "Graphing Linear Equations"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.CED.A.2", "CCSS.MATH.CONTENT.8.EE.B.6", "TEKS.MATH.A1.3.C"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            m = rng.choice([-3, -2, -1, 1, 2, 3])
            b = rng.randint(-5, 5)
            m_s = "" if m == 1 else ("-" if m == -1 else str(m))
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            eq = f"y = {m_s}x {b_s}".strip()
            ans_str = f"$ \"Line through \" (0, {b}) \" and \" (1, {b + m}), quad m = {m} $"
            distractors = [
                f"$ \"Line through \" (0, {-b}) \" with \" m = {m} $",
                f"$ \"Line through \" (0, {b}) \" with \" m = {-m} $",
                f"$ \"Line through \" ({b}, 0) \" with \" m = {m} $",
            ]
            diagram_svg, ans_svg = svg_coordinate_plane_pair(
                lines=[{"m": float(m), "b": float(b), "color": "#dc2626"}],
                points=[
                    {"x": 0, "y": b, "color": "#2563eb", "label": f"(0,{b})"},
                    {"x": 1, "y": b + m, "color": "#2563eb", "label": f"(1,{b+m})"},
                ],
                show_numbers=False,
            )
            steps = [
                f"Given linear equation: $ {eq} $",
                f"Identify the slope: $ m = {m} $",
                f"Identify the y-intercept: $ (0, {b}) $",
                f"Plot the y-intercept $ (0, {b}) $ and use the slope $ {m}/1 $ (rise {m}, run 1) to plot a second point: $ (1, {b + m}) $.",
                "Draw a straight line through the points."
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            if rng.random() < 0.2:
                val = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5])
                var = rng.choice(["x", "y"])
                eq = f"{var} = {val}"
                kind = "Vertical" if var == "x" else "Horizontal"
                other_kind = "Horizontal" if var == "x" else "Vertical"
                pt_lbl = f"({val}, 0)" if var == "x" else f"(0, {val})"
                ans_str = f"$ \"{kind} line through \" {pt_lbl} $"
                distractors = [
                    f"$ \"{other_kind} line through \" {pt_lbl} $",
                    f"$ \"{kind} line through \" ({-val}, 0) $" if var == "x" else f"$ \"{kind} line through \" (0, {-val}) $",
                    f"$ \"Line through origin with slope \" {val} $",
                ]
                if var == "x":
                    diagram_svg, ans_svg = svg_coordinate_plane_pair(
                        lines=[{"x_vert": float(val), "color": "#dc2626"}],
                        points=[{"x": val, "y": 0, "color": "#2563eb", "label": f"({val},0)"}],
                        show_numbers=False,
                    )
                else:
                    diagram_svg, ans_svg = svg_coordinate_plane_pair(
                        lines=[{"m": 0.0, "b": float(val), "color": "#dc2626"}],
                        points=[{"x": 0, "y": val, "color": "#2563eb", "label": f"(0,{val})"}],
                        show_numbers=False,
                    )
                steps = [
                    f"Given equation: $ {eq} $",
                    f"This is a {kind.lower()} line passing through {var} = {val}.",
                    f"Plot points where {var} is always {val} and draw the line."
                ]
            else:
                num = rng.choice([-3, -2, -1, 1, 2, 3])
                den = rng.choice([2, 3, 4, 5])
                b = rng.randint(-4, 4)
                sign = "-" if (num * den) < 0 else ""
                num_abs, den_abs = abs(num), abs(den)
                b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
                eq = f"y = {sign}{num_abs}/{den_abs} x {b_s}".strip()
                ans_str = f"$ \"Line through \" (0, {b}) \" and \" ({den}, {b + num}), quad m = {sign}{num_abs}/{den_abs} $"
                distractors = [
                    f"$ \"Line through \" (0, {b}) \" with \" m = {'' if sign else '-'}{num_abs}/{den_abs} $",
                    f"$ \"Line through \" (0, {-b}) \" with \" m = {sign}{num_abs}/{den_abs} $",
                    f"$ \"Line through \" (0, {b}) \" with \" m = {sign}{den_abs}/{num_abs} $",
                ]
                diagram_svg, ans_svg = svg_coordinate_plane_pair(
                    lines=[{"m": num / den, "b": float(b), "color": "#dc2626"}],
                    points=[
                        {"x": 0, "y": b, "color": "#2563eb", "label": f"(0,{b})"},
                        {"x": den, "y": b + num, "color": "#2563eb", "label": f"({den},{b+num})"},
                    ],
                    show_numbers=False,
                )
                steps = [
                    f"Given linear equation: $ {eq} $",
                    f"Slope: $ m = {sign}{num_abs}/{den_abs} $, y-intercept: $ (0, {b}) $",
                    f"From $ (0, {b}) $, rise {num} and run {den} to reach second point $ ({den}, {b + num}) $.",
                    "Draw the line connecting these points."
                ]
        else:  # SPICY
            A = rng.choice([-3, -2, -1, 1, 2, 3])
            B = rng.choice([2, 3, 4, -2, -3])
            C = rng.choice([6, 12, -6, -12, 8, -8])
            a_s = f"{A}x" if A not in (1, -1) else ("x" if A == 1 else "-x")
            b_s = f"+ {B}y" if B > 0 else f"- {abs(B)}y"
            eq = f"{a_s} {b_s} = {C}".replace("+ -", "- ")
            m_val = sp.Rational(-A, B)
            b_val = sp.Rational(C, B)
            ans_str = f"$ \"Line with slope \" m = {m_val} \" and y-int \" (0, {b_val}) $"
            distractors = [
                f"$ \"Line with slope \" m = {-m_val} \" and y-int \" (0, {b_val}) $",
                f"$ \"Line with slope \" m = {m_val} \" and y-int \" (0, {-b_val}) $",
                f"$ \"Line with slope \" m = {A} \" and y-int \" (0, {C}) $",
            ]
            diagram_svg, ans_svg = svg_coordinate_plane_pair(
                lines=[{"m": float(m_val), "b": float(b_val), "color": "#dc2626"}],
                points=[{"x": 0, "y": float(b_val), "color": "#2563eb", "label": f"(0,{b_val})"}],
                show_numbers=False,
            )
            steps = [
                f"Given equation in standard form: $ {eq} $",
                f"Convert to slope-intercept form by isolating $y$: $ y = {m_val}x {'+ ' if b_val >= 0 else '- '}{abs(b_val)} $",
                "Plot the y-intercept and use the slope to sketch the line."
            ]

        return BaseProblem(
            id=f"graph_line_{difficulty.value}_{problem_idx}",
            prompt_text="Sketch the graph of each line.",
            equation_typst=f"$ {eq} $",
            answer_typst=ans_str,
            steps_typst=steps,
            distractors=distractors,
            difficulty=difficulty,
            standards=self.standards,
            diagram_svg=diagram_svg,
            answer_svg=ans_svg,
            metadata={"equation": eq}
        )


class WritingLinearEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.writing_linear_equations"
    name = "Writing Linear Equations"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSF.LE.A.2", "TEKS.MATH.A1.2.B"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            m = rng.choice([-3, -2, -1, 1, 2, 3])
            x1 = rng.randint(-6, 6)
            b = rng.randint(-6, 6)
            y1: Any = m * x1 + b
            eq_typst = f"\"through: \" ({x1}, {y1}), quad \"slope = \" {m}"
            m_s = "" if m == 1 else ("-" if m == -1 else str(m))
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            ans_typst = f"y = {m_s}x {b_s}".strip()

            steps = [
                f"Given point $ ({x1}, {y1}) $ and slope $ m = {m} $",
                "Point-slope formula: $ y - y_1 = m(x - x_1) $",
                f"Substitute: $ y - ({y1}) = {m}(x - ({x1})) $",
                f"Solve for $y$: $ y = {m_s}x {b_s} $",
                f"Result: $ {ans_typst} $"
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            m_num = rng.choice([-3, -2, -1, 1, 2, 3])
            m_den = rng.choice([1, 2, 3])
            m_rat: Any = sp.Rational(m_num, m_den)
            x1 = rng.randint(-5, 5)
            b = rng.randint(-6, 6)
            y1_rat: Any = m_rat * x1 + b
            dx = m_den * rng.choice([-2, -1, 1, 2])
            x2 = x1 + dx
            y2_rat: Any = y1_rat + m_rat * dx
            x1_i, y1_i = int(x1), int(y1_rat)
            x2_i, y2_i = int(x2), int(y2_rat)

            eq_typst = f"\"through: \" ({x1_i}, {y1_i}) quad \"and\" quad ({x2_i}, {y2_i})"
            m_str = str(m_rat.p) if m_rat.q == 1 else f"{m_rat.p}/{m_rat.q}"
            m_s = "" if m_str == "1" else ("-" if m_str == "-1" else m_str)
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            ans_typst = f"y = {m_s}x {b_s}".strip()

            steps = [
                f"Find the slope through $ ({x1_i}, {y1_i}) $ and $ ({x2_i}, {y2_i}) $: $ m = ({y2_i} - ({y1_i})) / ({x2_i} - ({x1_i})) = {m_str} $",
                f"Use point-slope form with $ ({x1_i}, {y1_i}) $: $ y - ({y1_i}) = {m_str}(x - ({x1_i})) $",
                f"Isolate $y$: $ y = {m_s}x {b_s} $",
                f"Result: $ {ans_typst} $"
            ]
        else:  # SPICY
            is_perp = rng.choice([True, False])
            m_orig = rng.choice([-3, -2, 2, 3])
            b_orig = rng.randint(-5, 5)
            x1 = rng.randint(-5, 5)
            b_target = rng.randint(-6, 6)

            if is_perp:
                m_target: Any = sp.Rational(-1, m_orig)
                rel = "perpendicular to"
            else:
                m_target = sp.Rational(m_orig, 1)
                rel = "parallel to"

            y1_sp: Any = m_target * x1 + b_target
            if not y1_sp.is_integer:
                x1 = int(m_orig * rng.choice([1, 2, -1, -2]))
                y1_sp = m_target * x1 + b_target

            x1_i = int(x1)
            y1_i = int(y1_sp)
            orig_s = f"y = {m_orig}x {'+ ' if b_orig > 0 else '- '}{abs(b_orig)}"
            eq_typst = f"\"through: \" ({x1_i}, {y1_i}), quad \"{rel} \" {orig_s}"
            m_str = str(m_target.p) if m_target.q == 1 else f"{m_target.p}/{m_target.q}"
            m_s = "" if m_str == "1" else ("-" if m_str == "-1" else m_str)
            b_s = f"+ {b_target}" if b_target > 0 else (f"- {abs(b_target)}" if b_target < 0 else "")
            ans_typst = f"y = {m_s}x {b_s}".strip()

            steps = [
                f"Given line: $ {orig_s} $ has slope $ m = {m_orig} $.",
                f"The line is {rel} the given line, so its slope is $ m = {m_str} $.",
                f"Use point-slope form with $ ({x1_i}, {y1_i}) $: $ y - ({y1_i}) = {m_str}(x - ({x1_i})) $",
                f"Solve for $y$: $ y = {m_s}x {b_s} $",
                f"Result: $ {ans_typst} $"
            ]

        d1 = f"y = -{ans_typst.split('=')[1].strip()}"
        d2 = f"y = {ans_typst.split('=')[1].strip().replace('+', '-')}"
        d3 = "y = 2x + 1"
        return BaseProblem(
            id=f"write_line_{difficulty.value}_{problem_idx}",
            prompt_text="Write the slope-intercept form of the equation of each line.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": ans_typst}
        )


class GraphingLinearInequalitiesGenerator(BaseGenerator):
    generator_id = "algebra_1.graphing_linear_inequalities"
    name = "Graphing Linear Inequalities"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.D.12", "TEKS.MATH.A1.3.D"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        sym = rng.choice(["<", "<=", ">", ">="])
        is_solid = "<=" in sym or ">=" in sym

        if difficulty == ProblemDifficulty.MILD:
            m = rng.choice([-3, -2, -1, 1, 2, 3])
            b = rng.randint(-5, 5)
            m_s = "" if m == 1 else ("-" if m == -1 else str(m))
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            eq = f"y {sym} {m_s}x {b_s}".strip()
            m_fl, b_fl, eff_op = float(m), float(b), sym
            shade_dir = "above" if ">" in sym else "below"
            steps = [
                f"Given inequality: $ {eq} $",
                f"Boundary line: $ y = {m_s}x {b_s} $ (slope $ m = {m} $, y-intercept $ (0, {b}) $).",
                f"Draw a {'solid' if is_solid else 'dashed'} line because the inequality symbol is $ {sym} $.",
                f"Test point $ (0, 0) $ to determine shading: shade {shade_dir} the boundary line."
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            num = rng.choice([-3, -2, -1, 1, 2, 3])
            den = rng.choice([2, 3, 4])
            b = rng.randint(-4, 4)
            sign = "-" if (num * den) < 0 else ""
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            eq = f"y {sym} {sign}{abs(num)}/{abs(den)} x {b_s}".strip()
            m_fl, b_fl, eff_op = num / den, float(b), sym
            shade_dir = "above" if ">" in sym else "below"
            steps = [
                f"Given inequality: $ {eq} $",
                f"Boundary line has slope $ m = {sign}{abs(num)}/{abs(den)} $ and y-intercept $ (0, {b}) $.",
                f"Draw a {'solid' if is_solid else 'dashed'} line.",
                f"Shade {shade_dir} the boundary line."
            ]
        else:  # SPICY
            A = rng.choice([-3, -2, 1, 2, 3])
            B = rng.choice([-3, -2, -1])
            C = rng.choice([-6, 6, -12, 12])
            a_s = f"{A}x" if A not in (1, -1) else ("x" if A == 1 else "-x")
            b_s = f"- {abs(B)}y"
            eq = f"{a_s} {b_s} {sym} {C}"

            opp = {"<": ">", "<=": ">=", ">": "<", ">=": "<="}[sym]
            m_fl, b_fl, eff_op = -A / B, C / B, opp
            shade_dir = "above" if ">" in opp else "below"
            steps = [
                f"Given inequality in standard form: $ {eq} $",
                f"Subtract $ {a_s} $ from both sides: $ {B}y {sym} -{A}x + {C} $",
                f"Divide by negative {abs(B)} (remembering to FLIP the inequality sign): $ y {opp} {-A}/{B} x + {C}/{B} $",
                f"Draw a {'solid' if is_solid else 'dashed'} line and shade {shade_dir}."
            ]

        style_word = "Solid" if is_solid else "Dashed"
        opp_style = "Dashed" if is_solid else "Solid"
        opp_dir = "below" if shade_dir == "above" else "above"
        ans_str = f"$ \"{style_word} boundary, shaded {shade_dir} (y-int \" (0, {round(b_fl, 2)}) \")\" $"
        distractors = [
            f"$ \"{style_word} boundary, shaded {opp_dir}\" $",
            f"$ \"{opp_style} boundary, shaded {shade_dir}\" $",
            f"$ \"{opp_style} boundary, shaded {opp_dir}\" $",
        ]
        diagram_svg, ans_svg = svg_coordinate_plane_pair(
            lines=[{"m": m_fl, "b": b_fl, "dashed": not is_solid, "color": "#dc2626"}],
            shaded_half_planes=[{"m": m_fl, "b": b_fl, "op": eff_op, "color": "#3b82f6"}],
            show_numbers=False,
        )

        return BaseProblem(
            id=f"graph_ineq_{difficulty.value}_{problem_idx}",
            prompt_text="Sketch the graph of each linear inequality.",
            equation_typst=f"$ {eq} $",
            answer_typst=ans_str,
            steps_typst=steps,
            distractors=distractors,
            difficulty=difficulty,
            standards=self.standards,
            diagram_svg=diagram_svg,
            answer_svg=ans_svg,
            metadata={"inequality": eq}
        )
