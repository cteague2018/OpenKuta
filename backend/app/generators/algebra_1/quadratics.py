from __future__ import annotations

import math
import random

import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.svg_utils import svg_coordinate_plane
from backend.app.core.typst_utils import format_polynomial_typst


class QuadraticEquationsGenerator(BaseGenerator):
    generator_id = "algebra_1.quadratics"
    name = "Quadratic Equations (Factoring, Completing Square, Formula)"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.HSA.REI.B.4",
        "CCSS.MATH.CONTENT.HSA.REI.B.4.B",
        "CCSS.MATH.CONTENT.HSA.SSE.B.3.A",
        "TEKS.MATH.A1.8.A"
    ]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x = sp.Symbol('x')

        if difficulty == ProblemDifficulty.MILD:
            return self._generate_factoring_mild(rng, problem_idx, allow_negatives, x)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_completing_square_medium(rng, problem_idx, allow_negatives, x)
        else:
            return self._generate_quadratic_formula_spicy(rng, problem_idx, allow_negatives, x)

    def _generate_factoring_mild(
        self, rng: random.Random, problem_idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Monic quadratics with integer roots: x^2 + bx + c = 0."""
        # Pick integer roots r1, r2
        cand_roots = list(range(1, 9))
        if allow_negatives:
            cand_roots += list(range(-8, 0))

        r1 = rng.choice(cand_roots)
        r2 = rng.choice(cand_roots)

        # Ensure not always equal
        if rng.random() < 0.8:
            while r2 == r1:
                r2 = rng.choice(cand_roots)

        poly_expr = sp.expand((x - r1) * (x - r2))
        eq_typst = f"{format_polynomial_typst(poly_expr, x)} = 0"

        # Steps
        f1_sign = f"- {r1}" if r1 > 0 else f"+ {-r1}"
        f2_sign = f"- {r2}" if r2 > 0 else f"+ {-r2}"
        factored_typst = f"(x {f1_sign})(x {f2_sign}) = 0"

        if r1 == r2:
            ans_typst = f"x = {r1}"
            distractors = [
                f"x = {-r1}",
                f"x = {r1 + 1}, x = {r1 - 1}",
                f"x = 0, x = {r1}"
            ]
        else:
            # Sorted roots
            roots_sorted = sorted([r1, r2])
            ans_typst = f"x = {roots_sorted[0]}, quad x = {roots_sorted[1]}"
            # Misconceptions:
            # 1. Sign error: forgetting that (x - r) = 0 => x = r
            d1 = f"x = {-roots_sorted[0]}, quad x = {-roots_sorted[1]}"
            # 2. Mixed signs
            d2 = f"x = {roots_sorted[0]}, quad x = {-roots_sorted[1]}"
            # 3. Sum / product confusion
            d3 = f"x = {r1 + r2}, quad x = {r1 * r2}"
            distractors = [d1, d2, d3]

        steps = [
            f"$ {eq_typst} $",
            f"Factor the quadratic: $ {factored_typst} $",
            f"Set each factor to zero: $ x {f1_sign} = 0 $ or $ x {f2_sign} = 0 $",
            f"Solve for $x$: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"quad_mild_{problem_idx}",
            prompt_text="Solve each quadratic equation by factoring.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"method": "factoring", "roots": [r1, r2]}
        )

    def _generate_completing_square_medium(
        self, rng: random.Random, problem_idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Completing the square: x^2 + 2kx = d - k^2."""
        # Pick even linear coefficient 2*k
        k_pool = [1, 2, 3, 4, 5]
        if allow_negatives:
            k_pool += [-1, -2, -3, -4, -5]
        k = rng.choice(k_pool)

        # Target (x + k)^2 = d
        # Choose d > 0, preferably square-free or with a clean radical
        d_candidates = [2, 3, 5, 6, 7, 10, 11, 13, 15, 17, 19]
        d = rng.choice(d_candidates)

        c = k * k - d  # x^2 + 2kx + c = 0
        poly_expr = x**2 + 2 * k * x + c
        eq_typst = f"{format_polynomial_typst(poly_expr, x)} = 0"

        # Solution: x = -k +/- sqrt(d)
        ans_typst = f"x = {-k} plus.minus sqrt({d})"

        # Misconceptions:
        # 1. Forgot plus.minus
        d1 = f"x = {-k} + sqrt({d})"
        # 2. Sign error on -k
        d2 = f"x = {k} plus.minus sqrt({d})"
        # 3. Added k instead of k^2 to RHS: (x+k)^2 = -c + k = d - k^2 + k
        wrong_rhs = -c + k
        d3 = f"x = {-k} plus.minus sqrt({max(1, wrong_rhs)})"
        distractors = [d1, d2, d3]

        steps = [
            f"$ {eq_typst} $",
            f"Move constant to the right: $ x^2 {'+ ' if k >= 0 else '- '}{abs(2*k)}x = {-c} $",
            f"Complete the square by adding $ ({k})^2 = {k*k} $ to both sides:",
            f"$ (x {'+ ' if k >= 0 else '- '}{abs(k)})^2 = {-c + k*k} = {d} $",
            f"Take the square root of both sides: $ x {'+ ' if k >= 0 else '- '}{abs(k)} = plus.minus sqrt({d}) $",
            f"Solve for $x$: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"quad_med_{problem_idx}",
            prompt_text="Solve each equation by completing the square.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"method": "completing_the_square", "k": k, "d": d}
        )

    def _generate_quadratic_formula_spicy(
        self, rng: random.Random, problem_idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Quadratic formula: ax^2 + bx + c = 0 with a > 1 and radical simplification."""
        a = rng.choice([2, 3, 4, 5])
        b_cands = [1, 3, 5, 7]
        if allow_negatives:
            b_cands += [-1, -3, -5, -7]
        b = rng.choice(b_cands)

        # Choose c such that D = b^2 - 4ac > 0 and not a perfect square
        c_cands = [-1, -2, -3, -4, 1, 2]
        valid_triples = []
        for c in c_cands:
            D = b * b - 4 * a * c
            if D > 0 and math.isqrt(D)**2 != D:
                valid_triples.append(c)

        c = rng.choice(valid_triples) if valid_triples else -2
        D = b * b - 4 * a * c

        poly_expr = a * x**2 + b * x + c
        eq_typst = f"{format_polynomial_typst(poly_expr, x)} = 0"

        # Simplify sqrt(D)
        # Find largest square dividing D
        sq = 1
        for i in range(2, int(math.isqrt(D)) + 1):
            if D % (i * i) == 0:
                sq = i

        rad_rem = D // (sq * sq)
        two_a = 2 * a

        # Simplify gcd(-b, sq, 2a)
        g = math.gcd(abs(b), math.gcd(sq, two_a))
        num_b = -b // g
        num_sq = sq // g
        den = two_a // g

        rad_part = f"sqrt({rad_rem})" if num_sq == 1 else f"{num_sq} sqrt({rad_rem})"
        if den == 1:
            ans_typst = f"x = {num_b} plus.minus {rad_part}"
        else:
            ans_typst = f"x = ({num_b} plus.minus {rad_part}) / {den}"

        # Distractors
        # 1. Forgot -b sign: +b
        d1 = f"x = ({-num_b} plus.minus {rad_part}) / {den}" if den != 1 else f"x = ({-num_b} plus.minus {rad_part})"
        # 2. Forgot 2a in denominator (used just a)
        wrong_den = max(1, a // g)
        d2 = f"x = ({num_b} plus.minus {rad_part}) / {wrong_den}"
        # 3. Discarded radical part
        d3 = f"x = {num_b} / {den}"
        distractors = [d1, d2, d3]

        steps = [
            f"$ {eq_typst} $",
            f"Identify coefficients: $ a = {a}, quad b = {b}, quad c = {c} $",
            f"Calculate discriminant: $ Delta = b^2 - 4a c = ({b})^2 - 4({a})({c}) = {D} $",
            f"Apply quadratic formula: $ x = (-({b}) plus.minus sqrt({D})) / (2({a})) = ({-b} plus.minus sqrt({D})) / {two_a} $",
            f"Simplify radical and common factors: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"quad_spicy_{problem_idx}",
            prompt_text="Solve each equation using the quadratic formula.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"method": "quadratic_formula", "a": a, "b": b, "c": c, "D": D}
        )


class QuadraticsFactoringGenerator(BaseGenerator):
    generator_id = "algebra_1.quadratics_factoring"
    name = "Solving Quadratics by Factoring"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.4.B", "TEKS.MATH.A1.8.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x = sp.Symbol('x')
        roots = list(range(1, 9))
        if allow_negatives:
            roots += list(range(-8, 0))
        r1 = rng.choice(roots)
        r2 = rng.choice(roots)

        if difficulty == ProblemDifficulty.MILD:
            poly = (x - r1) * (x - r2)
            expanded = sp.expand(poly)
            b = expanded.coeff(x, 1)
            c = expanded.coeff(x, 0)
            b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
            c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
            eq = f"x^2 {b_s} {c_s} = 0".replace("+ -", "- ")

            f1 = f"(x {'- ' if r1 >= 0 else '+ '}{abs(r1)})"
            f2 = f"(x {'- ' if r2 >= 0 else '+ '}{abs(r2)})"
            steps = [
                f"Given quadratic equation: $ {eq} $",
                f"Factor the quadratic expression: $ {f1}{f2} = 0 $",
                f"Apply Zero Product Property: $ x {'- ' if r1 >= 0 else '+ '}{abs(r1)} = 0 $ or $ x {'- ' if r2 >= 0 else '+ '}{abs(r2)} = 0 $",
                f"Solve for $x$: $ x = {r1}, {r2} $",
                f"Result: $ x = {r1}, {r2} $"
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            a = rng.choice([2, 3, 5])
            r1 = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            r2 = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            poly = (a * x - r1) * (x - r2)
            expanded = sp.expand(poly)
            b = expanded.coeff(x, 1)
            c = expanded.coeff(x, 0)
            b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
            c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
            eq = f"{a}x^2 {b_s} {c_s} = 0".replace("+ -", "- ")

            r1_sol = f"{r1}/{a}" if r1 % a != 0 else str(r1 // a)
            f1 = f"({a}x {'- ' if r1 >= 0 else '+ '}{abs(r1)})"
            f2 = f"(x {'- ' if r2 >= 0 else '+ '}{abs(r2)})"
            steps = [
                f"Given quadratic equation: $ {eq} $",
                f"Factor using decomposition: $ {f1}{f2} = 0 $",
                f"Set each factor to zero to solve for $x$: $ x = {r1_sol}, {r2} $",
                f"Result: $ x = {r1_sol}, {r2} $"
            ]
        else:  # SPICY
            r1 = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            r2 = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            poly = (x - r1) * (x - r2)
            expanded = sp.expand(poly)
            b = expanded.coeff(x, 1)
            c = expanded.coeff(x, 0)
            b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
            eq = f"x^2 {b_s} = {-c}".replace("+ -", "- ")

            f1 = f"(x {'- ' if r1 >= 0 else '+ '}{abs(r1)})"
            f2 = f"(x {'- ' if r2 >= 0 else '+ '}{abs(r2)})"
            steps = [
                f"Given quadratic equation: $ {eq} $",
                f"Rewrite in standard form $ ax^2 + bx + c = 0 $: $ x^2 {b_s} {'+ ' if c >= 0 else '- '}{abs(c)} = 0 $",
                f"Factor: $ {f1}{f2} = 0 $",
                f"Solve for $x$: $ x = {r1}, {r2} $",
                f"Result: $ x = {r1}, {r2} $"
            ]

        ans = f"x = {r1}, {r2}"
        d1 = f"x = {-r1}, {-r2}"
        d2 = f"x = {r1 + 1}, {r2 - 1}"
        d3 = f"x = {r1}, {-r2}"

        return BaseProblem(
            id=f"quad_fact_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each equation by factoring.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"roots": (r1, r2)}
        )


class QuadraticsSquareRootsGenerator(BaseGenerator):
    generator_id = "algebra_1.quadratics_square_roots"
    name = "Solving Quadratics by Taking Square Roots"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.4.B", "TEKS.MATH.A1.8.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            k = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
            c = k * k
            if rng.choice([True, False]):
                eq = f"x^2 = {c}"
            else:
                eq = f"x^2 - {c} = 0"
            ans = f"x = plus.minus {k}"
            steps = [
                f"Given quadratic equation: $ {eq} $",
                f"Isolate $x^2$: $ x^2 = {c} $",
                f"Take the square root of both sides: $ x = plus.minus sqrt({c}) $",
                f"Result: $ {ans} $"
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            a = rng.choice([2, 3, 4, 5])
            k = rng.choice([2, 3, 4, 5, 6])
            b = rng.randint(-15, 15)
            c = a * (k * k) + b
            b_s = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
            eq = f"{a}x^2 {b_s} = {c}".replace("+ -", "- ")
            ans = f"x = plus.minus {k}"
            steps = [
                f"Given equation: $ {eq} $",
                f"Isolate variable term: $ {a}x^2 = {c - b} $",
                f"Divide by {a}: $ x^2 = {k * k} $",
                f"Take the square root of both sides: $ x = plus.minus sqrt({k * k}) $",
                f"Result: $ {ans} $"
            ]
        else:  # SPICY
            h = rng.randint(-6, 6)
            k = rng.choice([2, 3, 4, 5, 6, 7])
            c = k * k
            h_s = f"- {h}" if h > 0 else f"+ {abs(h)}"
            eq = f"(x {h_s})^2 = {c}"
            r1 = h + k
            r2 = h - k
            ans = f"x = {r1}, {r2}"
            steps = [
                f"Given equation: $ {eq} $",
                f"Take square root of both sides: $ x {h_s} = plus.minus {k} $",
                f"Solve for $x$: $ x = {h} plus.minus {k} $",
                f"Result: $ {ans} $"
            ]

        d1 = f"x = {k}"
        d2 = f"x = plus.minus {k + 1}"
        d3 = f"x = plus.minus {k * 2}"
        return BaseProblem(
            id=f"quad_sqrt_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each equation by taking square roots.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": eq}
        )


class QuadraticsFormulaGenerator(BaseGenerator):
    generator_id = "algebra_1.quadratics_formula"
    name = "The Quadratic Formula"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.4.B", "TEKS.MATH.A1.8.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            a = 1
            r1 = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            r2 = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            b = -(r1 + r2)
            c = r1 * r2
            ans = f"x = {r1}, {r2}"
        elif difficulty == ProblemDifficulty.MEDIUM:
            a = rng.choice([2, 3])
            r1 = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            r2 = rng.choice([-5, -3, -1, 1, 3, 5])
            b = -(r1 + a * r2)
            c = r1 * r2
            r1_s = f"{r1}/{a}" if r1 % a != 0 else str(r1 // a)
            ans = f"x = {r1_s}, {r2}"
        else:  # SPICY
            a = rng.choice([1, 2, 3])
            b = rng.choice([-5, -3, -1, 1, 3, 5])
            c = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            disc = b * b - 4 * a * c
            if disc < 0:
                c = -abs(c)
                disc = b * b - 4 * a * c
            ans = f"x = ({-b} plus.minus sqrt({disc})) / {2 * a}"

        disc = b * b - 4 * a * c
        a_lead = f"{a}x^2" if a != 1 else "x^2"
        b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
        c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
        eq = f"{a_lead} {b_s} {c_s} = 0".replace("+ -", "- ")

        steps = [
            f"Given equation: $ {eq} $",
            f"Identify coefficients: $ a = {a}, b = {b}, c = {c} $",
            "Quadratic Formula: $ x = (-b plus.minus sqrt(b^2 - 4 a c)) / (2 a) $",
            f"Substitute values: $ x = ({-b} plus.minus sqrt(({b})^2 - 4({a})({c}))) / (2({a})) $",
            f"Simplify under radical: $ x = ({-b} plus.minus sqrt({disc})) / {2 * a} $",
            f"Result: $ {ans} $"
        ]

        d1 = f"x = ({-b} plus.minus sqrt({disc + 4})) / {2 * a}"
        d2 = f"x = ({b} plus.minus sqrt({disc})) / {2 * a}"
        d3 = f"x = ({-b} plus.minus {int(math.isqrt(disc))}) / {2 * a}" if disc > 0 else "x = 1, -1"

        return BaseProblem(
            id=f"quad_form_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each equation with the quadratic formula.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": eq}
        )


class QuadraticsDiscriminantGenerator(BaseGenerator):
    generator_id = "algebra_1.quadratics_discriminant"
    name = "The Discriminant of Quadratic Equations"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.4.B", "TEKS.MATH.A1.8.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            a = 1
            case = rng.choice(["two_real", "one_real"])
            if case == "one_real":
                k = rng.choice([-4, -3, -2, 2, 3, 4])
                b = 2 * k
                c = k * k
            else:
                b = rng.choice([-6, -5, -4, 4, 5, 6])
                c = rng.choice([-5, -4, -3, -2, -1])
        elif difficulty == ProblemDifficulty.MEDIUM:
            a = rng.choice([2, 3, -1, -2])
            case = rng.choice(["two_real", "one_real", "two_imaginary"])
            if case == "one_real":
                k = rng.choice([-3, -2, 2, 3])
                b = 2 * a * k
                c = a * (k * k)
            elif case == "two_real":
                b = rng.randint(-6, 6)
                c = -rng.randint(1, 6) if a > 0 else rng.randint(1, 6)
            else:
                b = rng.choice([-2, -1, 1, 2])
                c = rng.randint(4, 9) if a > 0 else -rng.randint(4, 9)
        else:
            a = rng.choice([3, 4, 5, -3, -4])
            b = rng.choice([-9, -7, -5, 5, 7, 9])
            c = rng.choice([-8, -6, 6, 8, 10])

        disc = b * b - 4 * a * c
        if disc > 0:
            sol_type = "two real solutions"
        elif disc == 0:
            sol_type = "one real solution"
        else:
            sol_type = "two imaginary solutions"

        a_s = f"{a}x^2" if a not in (1, -1) else ("x^2" if a == 1 else "-x^2")
        b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
        c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
        if difficulty == ProblemDifficulty.SPICY:
            eq = f"{a_s} {b_s} = {-c}".replace("+ -", "- ")
        else:
            eq = f"{a_s} {b_s} {c_s} = 0".replace("+ -", "- ")

        ans = f"{disc}; {sol_type}"
        steps = [
            f"Given quadratic equation: $ {eq} $",
            f"Identify coefficients: $ a = {a}, b = {b}, c = {c} $",
            "Use discriminant formula: $ D = b^2 - 4 a c $",
            f"Calculate: $ D = ({b})^2 - 4({a})({c}) = {b*b} - ({4*a*c}) = {disc} $",
            f"Since $ D {' > 0' if disc > 0 else (' = 0' if disc == 0 else ' < 0')} $, there are {sol_type}.",
            f"Result: $ {ans} $"
        ]

        d1 = f"{disc + 4}; {sol_type}"
        d2 = f"{-disc}; {'two imaginary solutions' if disc > 0 else 'two real solutions'}"
        d3 = f"{b*b}; one real solution"

        return BaseProblem(
            id=f"quad_disc_{difficulty.value}_{problem_idx}",
            prompt_text="Find the discriminant of each quadratic equation then state the number and type of solutions.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"discriminant": disc, "type": sol_type}
        )


class QuadraticsCompletingSquareGenerator(BaseGenerator):
    generator_id = "algebra_1.quadratics_completing_square"
    name = "Solving Quadratics by Completing the Square"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.REI.B.4.B", "TEKS.MATH.A1.8.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        k = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = 2 * k
        if difficulty == ProblemDifficulty.MILD:
            d_val = rng.choice([1, 2, 3, 4, 5, 6])
            d_sq = d_val * d_val
            c = k * k - d_sq
            r1 = -k + d_val
            r2 = -k - d_val
            ans = f"x = {r1}, {r2}"
        elif difficulty == ProblemDifficulty.MEDIUM:
            d_sq = rng.choice([2, 3, 5, 6, 7, 10, 11, 13, 14, 15])
            c = k * k - d_sq
            k_s = str(-k) if -k != 0 else ""
            ans = f"x = {k_s} plus.minus sqrt({d_sq})"
        else:
            a = rng.choice([2, 3])
            d_val = rng.choice([1, 2, 3, 4])
            d_sq = d_val * d_val
            c = k * k - d_sq
            r1 = -k + d_val
            r2 = -k - d_val
            ans = f"x = {r1}, {r2}"
            b = b * a
            c = c * a

        a_lead = f"{a}x^2" if difficulty == ProblemDifficulty.SPICY else "x^2"
        b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
        c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
        eq = f"{a_lead} {b_s} {c_s} = 0".replace("+ -", "- ")

        steps = [
            f"Given quadratic equation: $ {eq} $",
            f"Isolate variable terms on left: $ {a_lead} {b_s} = {-c} $",
            f"Add $ (b/2)^2 = ({k})^2 = {k*k} $ to both sides: $ (x {'+ ' if k >= 0 else '- '}{abs(k)})^2 = {d_sq} $",
            f"Take the square root of both sides: $ x {'+ ' if k >= 0 else '- '}{abs(k)} = plus.minus sqrt({d_sq}) $",
            f"Result: $ {ans} $"
        ]

        d1 = f"x = {k} plus.minus sqrt({d_sq})"
        d2 = f"x = {-k}"
        d3 = f"x = plus.minus {d_sq}"
        return BaseProblem(
            id=f"quad_cts_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each equation by completing the square.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            metadata={"equation": eq}
        )


class GraphingQuadraticsGenerator(BaseGenerator):
    generator_id = "algebra_1.graphing_quadratics"
    name = "Graphing Quadratic Functions"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSF.IF.C.7.A", "TEKS.MATH.A1.7.A"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        h = rng.randint(-4, 4) if allow_negatives else rng.randint(0, 4)
        k = rng.randint(-4, 4) if allow_negatives else rng.randint(0, 4)
        a = rng.choice([-1, 1, 2, -2])

        if difficulty == ProblemDifficulty.MILD:
            h_s = f"- {h}" if h > 0 else (f"+ {abs(h)}" if h < 0 else "")
            k_s = f"+ {k}" if k > 0 else (f"- {abs(k)}" if k < 0 else "")
            a_s = "" if a == 1 else ("-" if a == -1 else str(a))
            inner = f"(x {h_s})" if h != 0 else "x"
            eq = f"y = {a_s}{inner}^2 {k_s}".strip()
            y_int = a * (h * h) + k
            steps = [
                f"Given quadratic function: $ {eq} $",
                f"Identify vertex $ (h, k) $: $ ({h}, {k}) $",
                f"Axis of symmetry: $ x = {h} $",
                f"The parabola opens {'upward' if a > 0 else 'downward'} because $ a = {a} $.",
                f"Plot vertex $ ({h}, {k}) $ and y-intercept $ (0, {y_int}) $, then sketch curve."
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            b = -2 * a * h
            c = a * (h * h) + k
            a_s = "" if a == 1 else ("-" if a == -1 else str(a))
            b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
            c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
            eq = f"y = {a_s}x^2 {b_s} {c_s}".strip().replace("+ -", "- ")
            steps = [
                f"Given quadratic function: $ {eq} $",
                f"Vertex x-coordinate using $ x = -b / (2a) $: $ x = -({b}) / (2({a})) = {h} $",
                f"Vertex y-coordinate: $ y = f({h}) = {k} $",
                f"Vertex: $ ({h}, {k}) $, Axis of symmetry: $ x = {h} $",
                f"Plot vertex and y-intercept $ (0, {c}) $, then sketch parabola."
            ]
        else:  # SPICY
            b = -2 * a * h
            c = a * (h * h) + k
            sym = rng.choice(["<", "<=", ">", ">="])
            is_solid = "<=" in sym or ">=" in sym
            a_s = "" if a == 1 else ("-" if a == -1 else str(a))
            b_s = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
            c_s = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
            eq = f"y {sym} {a_s}x^2 {b_s} {c_s}".strip().replace("+ -", "- ")
            steps = [
                f"Given quadratic inequality: $ {eq} $",
                f"Graph the boundary parabola with a {'solid' if is_solid else 'dashed'} curve.",
                f"Vertex is at $ ({h}, {k}) $.",
                "Test point $ (0, 0) $ to shade region."
            ]

        ans = f"Vertex: ({h}, {k}); Axis: x = {h}"
        d1 = f"Vertex: ({-h}, {k}); Axis: x = {-h}"
        d2 = f"Vertex: ({k}, {h}); Axis: x = {k}"
        d3 = f"Vertex: ({h}, {-k}); Axis: x = {h}"

        ans_svg = svg_coordinate_plane(
            functions=[{"fn": lambda xv, _a=a, _h=h, _k=k: _a * ((xv - _h) ** 2) + _k, "color": "#dc2626"}],
            asymptotes=[{"x": float(h), "color": "#64748b"}],
            points=[{"x": h, "y": k, "color": "#2563eb", "label": f"({h},{k})"}],
        )

        return BaseProblem(
            id=f"graph_quad_{difficulty.value}_{problem_idx}",
            prompt_text="Sketch the graph of each quadratic function. Identify the vertex and axis of symmetry.",
            equation_typst=f"$ {eq} $",
            answer_typst=f"$ {ans} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3]],
            difficulty=difficulty,
            standards=self.standards,
            diagram_svg=svg_coordinate_plane(),
            answer_svg=ans_svg,
            metadata={"vertex": (h, k)}
        )
