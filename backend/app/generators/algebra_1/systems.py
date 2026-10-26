from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class SystemsGraphingGenerator(BaseGenerator):
    generator_id = "algebra_1.systems_graphing"
    name = "Systems of Equations: Solving by Graphing"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.C.6", "CCSS.MATH.CONTENT.8.EE.C.8.A", "TEKS.MATH.A1.3.F"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x_sol = rng.randint(-4, 4) if allow_negatives else rng.randint(1, 4)
        y_sol = rng.randint(-4, 4) if allow_negatives else rng.randint(1, 4)

        if difficulty == ProblemDifficulty.MILD:
            # Both in slope-intercept form y = m1*x + b1, y = m2*x + b2 with small integer slopes
            slopes = [-2, -1, 1, 2, 3]
            m1 = rng.choice(slopes)
            m2 = rng.choice([s for s in slopes if s != m1])
            b1 = y_sol - m1 * x_sol
            b2 = y_sol - m2 * x_sol

            b1_str = f"+ {b1}" if b1 > 0 else (f"- {abs(b1)}" if b1 < 0 else "")
            b2_str = f"+ {b2}" if b2 > 0 else (f"- {abs(b2)}" if b2 < 0 else "")
            m1_str = "" if m1 == 1 else ("-" if m1 == -1 else str(m1))
            m2_str = "" if m2 == 1 else ("-" if m2 == -1 else str(m2))

            eq1 = f"y = {m1_str}x {b1_str}".strip()
            eq2 = f"y = {m2_str}x {b2_str}".strip()
            system_typst = f"cases({eq1}, {eq2})"
            ans_typst = f"({x_sol}, {y_sol})"

            steps = [
                f"Given system: $ {system_typst} $",
                f"Line 1: $ {eq1} $ has slope $ m_1 = {m1} $ and y-intercept $ (0, {b1}) $.",
                f"Line 2: $ {eq2} $ has slope $ m_2 = {m2} $ and y-intercept $ (0, {b2}) $.",
                "Graph both lines on the coordinate plane.",
                f"Locate the intersection point: $ ({x_sol}, {y_sol}) $.",
                f"Solution: $ {ans_typst} $"
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # One in slope-intercept, one in standard form Ax + By = C
            m1 = rng.choice([-2, -1, 1, 2])
            b1 = y_sol - m1 * x_sol
            m1_str = "" if m1 == 1 else ("-" if m1 == -1 else str(m1))
            b1_str = f"+ {b1}" if b1 > 0 else (f"- {abs(b1)}" if b1 < 0 else "")
            eq1 = f"y = {m1_str}x {b1_str}".strip()

            A = rng.choice([1, 2, -1, -2])
            B = rng.choice([1, 2, -1])
            if -A / B == m1:
                A = -A
            C = A * x_sol + B * y_sol
            b_sign = f"+ {B}y" if B > 0 else f"- {abs(B)}y"
            a_str = f"{A}x" if A not in (1, -1) else ("x" if A == 1 else "-x")
            eq2 = f"{a_str} {b_sign} = {C}".replace("+ -", "- ")

            system_typst = f"cases({eq1}, {eq2})"
            ans_typst = f"({x_sol}, {y_sol})"
            m2 = -A / B
            b2 = C / B
            m2_disp = int(m2) if m2.is_integer() else f"{-A}/{B}"
            b2_disp = int(b2) if b2.is_integer() else f"{C}/{B}"

            steps = [
                f"Given system: $ {system_typst} $",
                f"First line is in slope-intercept form: $ {eq1} $ (slope $ m = {m1} $, y-intercept $ (0, {b1}) $).",
                f"Rewrite second equation into slope-intercept form: $ y = {m2_disp}x {'+ ' if b2 >= 0 else '- '}{abs(b2_disp) if isinstance(b2_disp, int) else b2_disp} $.",
                "Graph both lines and locate the intersection.",
                f"Intersection point: $ ({x_sol}, {y_sol}) $.",
                f"Solution: $ {ans_typst} $"
            ]

        else: # SPICY
            # Both in standard form Ax + By = C
            A1, B1 = rng.choice([(1, 1), (2, -1), (1, -2), (3, 1)])
            A2, B2 = rng.choice([(1, -1), (1, 2), (2, 1), (-1, 2)])
            if A1 * B2 == A2 * B1:
                B2 += 1
            C1 = A1 * x_sol + B1 * y_sol
            C2 = A2 * x_sol + B2 * y_sol

            a1_s = f"{A1}x" if A1 not in (1, -1) else ("x" if A1 == 1 else "-x")
            b1_s = f"+ {B1}y" if B1 > 0 else f"- {abs(B1)}y"
            a2_s = f"{A2}x" if A2 not in (1, -1) else ("x" if A2 == 1 else "-x")
            b2_s = f"+ {B2}y" if B2 > 0 else f"- {abs(B2)}y"

            eq1 = f"{a1_s} {b1_s} = {C1}".replace("+ -", "- ")
            eq2 = f"{a2_s} {b2_s} = {C2}".replace("+ -", "- ")
            system_typst = f"cases({eq1}, {eq2})"
            ans_typst = f"({x_sol}, {y_sol})"

            steps = [
                f"Given system: $ {system_typst} $",
                "Convert both equations to slope-intercept form $ y = mx + b $ or find the intercepts.",
                "Graph both lines carefully on the coordinate plane.",
                f"Determine coordinates of the intersection: $ ({x_sol}, {y_sol}) $.",
                f"Solution: $ {ans_typst} $"
            ]

        d1 = f"({y_sol}, {x_sol})"
        d2 = f"({-x_sol}, {y_sol})"
        d3 = f"({x_sol + 1}, {y_sol - 1})"

        return BaseProblem(
            id=f"sys_graph_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each system of equations by graphing.",
            equation_typst=f"$ {system_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"solution": (x_sol, y_sol)}
        )


class SystemsSubstitutionGenerator(BaseGenerator):
    generator_id = "algebra_1.systems_substitution"
    name = "Systems of Equations: Solving by Substitution"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.C.6", "CCSS.MATH.CONTENT.8.EE.C.8.B", "TEKS.MATH.A1.5.C"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x_sol = rng.randint(-5, 5) if allow_negatives else rng.randint(1, 5)
        y_sol = rng.randint(-5, 5) if allow_negatives else rng.randint(1, 5)

        if difficulty == ProblemDifficulty.MILD:
            m = rng.choice([-3, -2, -1, 1, 2, 3])
            b = y_sol - m * x_sol
            m_s = "" if m == 1 else ("-" if m == -1 else str(m))
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            eq1 = f"y = {m_s}x {b_s}".strip()

            A = rng.choice([2, 3, 4])
            B = rng.choice([1, -1, 2, -2])
            C = A * x_sol + B * y_sol
            b_sign = f"+ {B}y" if B > 0 else f"- {abs(B)}y"
            eq2 = f"{A}x {b_sign} = {C}".replace("+ -", "- ")

            sub_expr = f"{m_s}x {b_s}".strip()
            steps = [
                f"Given system: $ cases({eq1}, {eq2}) $",
                f"Substitute $ y = {sub_expr} $ into the second equation: $ {A}x {'+ ' if B > 0 else '- '}{abs(B)}({sub_expr}) = {C} $",
                f"Expand and solve for $x$: $ x = {x_sol} $",
                f"Substitute $ x = {x_sol} $ back into the first equation: $ y = {m}({x_sol}) {b_s} = {y_sol} $",
                f"Solution: $ ({x_sol}, {y_sol}) $"
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            isolate_x = rng.choice([True, False])
            if isolate_x:
                k = rng.choice([-3, -2, 2, 3])
                C1 = x_sol + k * y_sol
                k_sign = f"+ {k}y" if k > 0 else f"- {abs(k)}y"
                eq1 = f"x {k_sign} = {C1}"

                A2 = rng.choice([2, 3, 4])
                B2 = rng.choice([-2, -1, 1, 2])
                C2 = A2 * x_sol + B2 * y_sol
                b2_sign = f"+ {B2}y" if B2 > 0 else f"- {abs(B2)}y"
                eq2 = f"{A2}x {b2_sign} = {C2}".replace("+ -", "- ")

                iso_s = f"{C1} {'- ' if k > 0 else '+ '}{abs(k)}y"
                steps = [
                    f"Given system: $ cases({eq1}, {eq2}) $",
                    f"Isolate $x$ in the first equation: $ x = {iso_s} $",
                    f"Substitute into the second equation: $ {A2}({iso_s}) {b2_sign} = {C2} $",
                    f"Solve for $y$: $ y = {y_sol} $",
                    f"Back-substitute to find $x$: $ x = {x_sol} $",
                    f"Solution: $ ({x_sol}, {y_sol}) $"
                ]
            else:
                k = rng.choice([-3, -2, 2, 3])
                C1 = k * x_sol + y_sol
                k_sign = f"{k}x" if k != 1 else "x"
                eq1 = f"{k_sign} + y = {C1}"

                A2 = rng.choice([2, 3, 5])
                B2 = rng.choice([-3, -2, 2])
                C2 = A2 * x_sol + B2 * y_sol
                b2_sign = f"+ {B2}y" if B2 > 0 else f"- {abs(B2)}y"
                eq2 = f"{A2}x {b2_sign} = {C2}".replace("+ -", "- ")

                iso_s = f"{C1} - {k}x"
                steps = [
                    f"Given system: $ cases({eq1}, {eq2}) $",
                    f"Isolate $y$ in the first equation: $ y = {iso_s} $",
                    f"Substitute into the second equation: $ {A2}x {'+ ' if B2 > 0 else '- '}{abs(B2)}({iso_s}) = {C2} $",
                    f"Solve for $x$: $ x = {x_sol} $",
                    f"Back-substitute to find $y$: $ y = {y_sol} $",
                    f"Solution: $ ({x_sol}, {y_sol}) $"
                ]

        else: # SPICY
            m1 = rng.choice([-3, -2, 2, 3])
            m2 = rng.choice([-1, 1, 4])
            b1 = y_sol - m1 * x_sol
            b2 = y_sol - m2 * x_sol
            m1_s = "" if m1 == 1 else ("-" if m1 == -1 else str(m1))
            m2_s = "" if m2 == 1 else ("-" if m2 == -1 else str(m2))
            b1_s = f"+ {b1}" if b1 > 0 else (f"- {abs(b1)}" if b1 < 0 else "")
            b2_s = f"+ {b2}" if b2 > 0 else (f"- {abs(b2)}" if b2 < 0 else "")
            eq1 = f"y = {m1_s}x {b1_s}".strip()
            eq2 = f"y = {m2_s}x {b2_s}".strip()

            steps = [
                f"Given system: $ cases({eq1}, {eq2}) $",
                f"Set the expressions for $y$ equal: $ {eq1.split('=')[1].strip()} = {eq2.split('=')[1].strip()} $",
                f"Solve for $x$: $ ({m1} - ({m2}))x = {b2} - ({b1}) ==> x = {x_sol} $",
                f"Substitute $ x = {x_sol} $ into first equation to find $y$: $ y = {y_sol} $",
                f"Solution: $ ({x_sol}, {y_sol}) $"
            ]

        d1 = f"({-x_sol}, {-y_sol})"
        d2 = f"({y_sol}, {x_sol})"
        d3 = f"({x_sol}, {-y_sol})"
        system_typst = f"cases({eq1}, {eq2})"

        return BaseProblem(
            id=f"sys_sub_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each system of equations by substitution.",
            equation_typst=f"$ {system_typst} $",
            answer_typst=f"$ ({x_sol}, {y_sol}) $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"solution": (x_sol, y_sol)}
        )


class SystemsEliminationGenerator(BaseGenerator):
    generator_id = "algebra_1.systems_elimination"
    name = "Systems of Equations: Solving by Elimination"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.C.6", "CCSS.MATH.CONTENT.8.EE.C.8.B", "TEKS.MATH.A1.5.C"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x_sol = rng.randint(-5, 5) if allow_negatives else rng.randint(1, 5)
        y_sol = rng.randint(-5, 5) if allow_negatives else rng.randint(1, 5)

        if difficulty == ProblemDifficulty.MILD:
            a1 = rng.choice([2, 3, 4, 5])
            a2 = rng.choice([1, 2, 3])
            b_val = rng.choice([1, 2, 3])
            b1 = b_val
            b2 = -b_val

            c1 = a1 * x_sol + b1 * y_sol
            c2 = a2 * x_sol + b2 * y_sol
            eq1 = f"{a1}x + {b1}y = {c1}"
            eq2 = f"{a2}x - {abs(b2)}y = {c2}"
            system_typst = f"cases({eq1}, {eq2})"

            sum_a = a1 + a2
            sum_c = c1 + c2
            steps = [
                f"Given system: $ {system_typst} $",
                f"Add both equations directly to eliminate $y$: $ ({a1} + {a2})x = {c1} + ({c2}) $",
                f"Solve for $x$: $ {sum_a}x = {sum_c} ==> x = {x_sol} $",
                f"Substitute $ x = {x_sol} $ into first equation: $ {a1}({x_sol}) + {b1}y = {c1} $",
                f"Solve for $y$: $ y = {y_sol} $",
                f"Solution: $ ({x_sol}, {y_sol}) $"
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            mult = rng.choice([2, 3, -2])
            b2 = rng.choice([1, 2, -1])
            b1 = -b2 * mult
            a1 = rng.choice([3, 4, 5])
            a2 = rng.choice([1, 2])

            c1 = a1 * x_sol + b1 * y_sol
            c2 = a2 * x_sol + b2 * y_sol
            b1_s = f"+ {b1}y" if b1 > 0 else f"- {abs(b1)}y"
            b2_s = f"+ {b2}y" if b2 > 0 else f"- {abs(b2)}y"
            eq1 = f"{a1}x {b1_s} = {c1}"
            eq2 = f"{a2}x {b2_s} = {c2}"
            system_typst = f"cases({eq1}, {eq2})"

            steps = [
                f"Given system: $ {system_typst} $",
                f"Multiply second equation by {mult} to align coefficients of $y$: $ {a2 * mult}x {'+ ' if b2 * mult > 0 else '- '}{abs(b2 * mult)}y = {c2 * mult} $",
                f"Add to first equation to eliminate $y$ and solve for $x$: $ x = {x_sol} $",
                f"Substitute $ x = {x_sol} $ into second equation to find $y$: $ y = {y_sol} $",
                f"Solution: $ ({x_sol}, {y_sol}) $"
            ]

        else: # SPICY
            a1, b1 = rng.choice([(2, 3), (3, 2), (4, 3), (5, 2)])
            a2, b2 = rng.choice([(3, -2), (2, -5), (3, 4), (-2, 5)])
            if a1 * b2 == a2 * b1:
                b2 += 1
            c1 = a1 * x_sol + b1 * y_sol
            c2 = a2 * x_sol + b2 * y_sol

            b1_s = f"+ {b1}y" if b1 > 0 else f"- {abs(b1)}y"
            b2_s = f"+ {b2}y" if b2 > 0 else f"- {abs(b2)}y"
            eq1 = f"{a1}x {b1_s} = {c1}"
            eq2 = f"{a2}x {b2_s} = {c2}"
            system_typst = f"cases({eq1}, {eq2})"

            steps = [
                f"Given system: $ {system_typst} $",
                f"Multiply first equation by {abs(b2)} and second equation by {abs(b1)} to eliminate $y$.",
                f"Add or subtract aligned equations to find $x$: $ x = {x_sol} $",
                f"Substitute $ x = {x_sol} $ into first equation to solve for $y$: $ y = {y_sol} $",
                f"Solution: $ ({x_sol}, {y_sol}) $"
            ]

        d1 = f"({x_sol + 1}, {y_sol - 1})"
        d2 = f"({-x_sol}, {y_sol})"
        d3 = f"({y_sol}, {x_sol})"
        return BaseProblem(
            id=f"sys_elim_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each system of equations by elimination.",
            equation_typst=f"$ {system_typst} $",
            answer_typst=f"$ ({x_sol}, {y_sol}) $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"solution": (x_sol, y_sol)}
        )


class SystemsInequalitiesGenerator(BaseGenerator):
    generator_id = "algebra_1.systems_inequalities"
    name = "Systems of Inequalities: Graphing"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.D.12", "TEKS.MATH.A1.3.H"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        m1 = rng.choice([-2, -1, 1, 2])
        m2 = rng.choice([s for s in [-3, -2, -1, 1, 2, 3] if s != m1])
        b1 = rng.randint(-4, 4)
        b2 = rng.randint(-4, 4)

        sym1 = rng.choice(["<", "<=", ">", ">="])
        sym2 = rng.choice(["<", "<=", ">", ">="])

        m1_s = "" if m1 == 1 else ("-" if m1 == -1 else str(m1))
        m2_s = "" if m2 == 1 else ("-" if m2 == -1 else str(m2))
        b1_s = f"+ {b1}" if b1 > 0 else (f"- {abs(b1)}" if b1 < 0 else "")
        b2_s = f"+ {b2}" if b2 > 0 else (f"- {abs(b2)}" if b2 < 0 else "")

        if difficulty == ProblemDifficulty.MILD:
            ineq1 = f"y {sym1} {m1_s}x {b1_s}".strip()
            ineq2 = f"y {sym2} {m2_s}x {b2_s}".strip()
        elif difficulty == ProblemDifficulty.MEDIUM:
            ineq1 = f"y {sym1} {m1_s}x {b1_s}".strip()
            A = rng.choice([1, 2, -1])
            B = rng.choice([1, 2])
            C = rng.randint(-6, 6)
            ineq2 = f"{A}x {'+ ' if B > 0 else '- '}{abs(B)}y {sym2} {C}".replace("+ -", "- ")
        else:
            A1, B1 = rng.choice([(1, 1), (2, -1), (1, -2)])
            A2, B2 = rng.choice([(1, -1), (2, 1), (-1, 2)])
            C1 = rng.randint(-6, 6)
            C2 = rng.randint(-6, 6)
            ineq1 = f"{A1}x {'+ ' if B1 > 0 else '- '}{abs(B1)}y {sym1} {C1}".replace("+ -", "- ")
            ineq2 = f"{A2}x {'+ ' if B2 > 0 else '- '}{abs(B2)}y {sym2} {C2}".replace("+ -", "- ")

        system_typst = f"cases({ineq1}, {ineq2})"
        b1_style = "solid" if "<=" in sym1 or ">=" in sym1 else "dashed"
        b2_style = "solid" if "<=" in sym2 or ">=" in sym2 else "dashed"

        steps = [
            f"Given system of inequalities: $ {system_typst} $",
            f"Boundary line 1 is {b1_style} line. Shade region satisfying $ {ineq1} $.",
            f"Boundary line 2 is {b2_style} line. Shade region satisfying $ {ineq2} $.",
            "The final solution is the intersection (overlapping region) of both shaded half-planes."
        ]

        return BaseProblem(
            id=f"sys_ineq_{difficulty.value}_{problem_idx}",
            prompt_text="Sketch the solution to each system of inequalities.",
            equation_typst=f"$ {system_typst} $",
            answer_typst="Shaded intersection region",
            steps_typst=steps,
            distractors=["Region above line 1 only", "Region below line 2 only", "Unbounded disjoint region"],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"ineq1": ineq1, "ineq2": ineq2}
        )


class SystemsOfEquationsGenerator(BaseGenerator):
    """General generator supporting all methods (elimination, substitution, graphing)
    for backwards compatibility."""
    generator_id = "algebra_1.systems"
    name = "Systems of Two Linear Equations (Elimination & Substitution)"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.HSA.REI.C.6",
        "CCSS.MATH.CONTENT.8.EE.C.8.B",
        "TEKS.MATH.A1.5.C"
    ]

    def __init__(self) -> None:
        super().__init__()
        self._graphing_gen = SystemsGraphingGenerator()
        self._sub_gen = SystemsSubstitutionGenerator()
        self._elim_gen = SystemsEliminationGenerator()

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            return self._elim_gen.generate_single(rng, difficulty, problem_idx, allow_negatives)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._sub_gen.generate_single(rng, difficulty, problem_idx, allow_negatives)
        else:
            return self._elim_gen.generate_single(rng, difficulty, problem_idx, allow_negatives)
