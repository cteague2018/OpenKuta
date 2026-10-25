from __future__ import annotations

import math
import random

import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
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
