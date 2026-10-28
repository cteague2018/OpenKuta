from __future__ import annotations

import random

import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.typst_utils import format_polynomial_typst
from backend.app.generators.verification_gate import verify_mathematical_truth


class PolynomialFactoringGenerator(BaseGenerator):
    generator_id = "algebra_1.factoring"
    name = "Factoring Polynomials (GCF, Trinomials, Difference of Squares)"
    category = "Algebra 1"
    standards = [
        "CCSS.MATH.CONTENT.HSA.SSE.A.2",
        "CCSS.MATH.CONTENT.HSA.SSE.B.3.A",
        "TEKS.MATH.A1.10.E",
        "TEKS.MATH.A1.10.F"
    ]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x = sp.Symbol('x')

        if difficulty == ProblemDifficulty.MILD:
            return self._generate_difference_of_squares_or_gcf(rng, problem_idx, allow_negatives, x)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_trinomial_monic(rng, problem_idx, allow_negatives, x)
        else:
            return self._generate_trinomial_non_monic(rng, problem_idx, allow_negatives, x)

    def _generate_difference_of_squares_or_gcf(
        self, rng: random.Random, problem_idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Difference of two squares: a^2 x^2 - b^2."""
        b = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        a = rng.choice([1, 1, 1, 2, 3])  # mostly 1

        poly_expr = (a * x)**2 - b**2
        eq_typst = format_polynomial_typst(poly_expr, x)

        ax_str = f"{a}x" if a != 1 else "x"
        ans_typst = f"({ax_str} - {b})({ax_str} + {b})"

        d1 = f"({ax_str} - {b})^2"
        d2 = f"({ax_str} + {b})^2"
        d3 = f"({ax_str} - {b // 2 if b % 2 == 0 else b})({ax_str} + {b // 2 if b % 2 == 0 else b})"

        steps = [
            "Recognize difference of two squares: $ A^2 - B^2 = (A - B)(A + B) $",
            f"Identify $ A = {ax_str} $ and $ B = {b} $",
            f"Factor: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"factor_mild_{problem_idx}",
            prompt_text="Factor each completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"type": "diff_of_squares", "a": a, "b": b}
        )

    def _generate_trinomial_monic(
        self, rng: random.Random, problem_idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Monic trinomial: x^2 + bx + c = (x + p)(x + q)."""
        pool = list(range(1, 10))
        if allow_negatives:
            pool += list(range(-9, 0))

        p = rng.choice(pool)
        q = rng.choice(pool)
        while p == 0 or q == 0:
            p = rng.choice(pool)

        poly_expr = sp.expand((x + p) * (x + q))
        eq_typst = format_polynomial_typst(poly_expr, x)

        p_sign = f"+ {p}" if p > 0 else f"- {abs(p)}"
        q_sign = f"+ {q}" if q > 0 else f"- {abs(q)}"
        ans_typst = f"(x {p_sign})(x {q_sign})"

        # Distractors
        d1 = f"(x {'- ' if p > 0 else '+ '}{abs(p)})(x {'- ' if q > 0 else '+ '}{abs(q)})"
        d2 = f"(x {'- ' if p > 0 else '+ '}{abs(p)})(x {q_sign})"
        d3 = f"(x + {p * q})(x + 1)"

        steps = [
            f"Given trinomial: $ {eq_typst} $",
            f"Find two numbers that multiply to $ {p * q} $ and add to $ {p + q} $",
            f"The two numbers are $ {p} $ and $ {q} $",
            f"Factored form: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"factor_med_{problem_idx}",
            prompt_text="Factor each completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"p": p, "q": q}
        )

    def _generate_trinomial_non_monic(
        self, rng: random.Random, problem_idx: int, allow_negatives: bool, x: sp.Symbol
    ) -> BaseProblem:
        """Non-monic trinomial: (ax + p)(bx + q)."""
        a = rng.choice([2, 3, 5])
        b = 1
        p = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

        poly_expr = sp.expand((a * x + p) * (b * x + q))
        eq_typst = format_polynomial_typst(poly_expr, x)

        p_sign = f"+ {p}" if p > 0 else f"- {abs(p)}"
        q_sign = f"+ {q}" if q > 0 else f"- {abs(q)}"
        ans_typst = f"({a}x {p_sign})(x {q_sign})"

        d1 = f"(x {p_sign})({a}x {q_sign})"
        d2 = f"({a}x {'- ' if p > 0 else '+ '}{abs(p)})(x {q_sign})"
        d3 = f"({a}x {p_sign})(x {'- ' if q > 0 else '+ '}{abs(q)})"

        m1 = a * q
        m2 = p
        m1_s = f"+ {m1}x" if m1 >= 0 else f"- {abs(m1)}x"
        m2_s = f"+ {m2}x" if m2 >= 0 else f"- {abs(m2)}x"
        c_val = p * q
        c_s = f"+ {c_val}" if c_val >= 0 else f"- {abs(c_val)}"
        b_sum = a * q + p
        ac_val = a * c_val

        steps = [
            f"Given trinomial: $ {eq_typst} $",
            f"Find two factors of $a c = {ac_val}$ that sum to $b = {b_sum}$: factors are ${m1}$ and ${m2}$.",
            f"Split middle term: $ {a}x^2 {m1_s} {m2_s} {c_s} $",
            f"Factor by grouping: $ ({a}x^2 {m1_s}) + ({m2_s} {c_s}) = {a}x(x {q_sign}) {p_sign}(x {q_sign}) $",
            f"Factored form: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"factor_spicy_{problem_idx}",
            prompt_text="Factor each completely.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[d1, d2, d3],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"a": a, "p": p, "q": q}
        )


class PolynomialAddSubGenerator(BaseGenerator):
    generator_id = "algebra_1.polynomials_add_sub"
    name = "Adding and Subtracting Polynomials"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.APR.A.1", "TEKS.MATH.A1.10.A"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x = sp.Symbol('x')
        op = rng.choice(["+", "-"])

        if difficulty == ProblemDifficulty.MILD:
            # Linear polynomials: (ax + b) +/- (cx + d)
            a = rng.randint(1, 6)
            b = rng.randint(-8, 8)
            c = rng.randint(1, 6)
            d = rng.randint(-8, 8)
            p1 = a * x + b
            p2 = c * x + d
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Quadratics: (ax^2 + bx + c) +/- (dx^2 + ex + f)
            a = rng.choice([-3, -2, -1, 1, 2, 3])
            b = rng.randint(-6, 6)
            c = rng.randint(-8, 8)
            d = rng.choice([-3, -2, -1, 1, 2, 3])
            e = rng.randint(-6, 6)
            f_const = rng.randint(-8, 8)
            p1 = a * x**2 + b * x + c
            p2 = d * x**2 + e * x + f_const
        else:  # SPICY: Cubics / dissimilar powers
            a = rng.choice([1, 2, 3])
            b = rng.randint(-5, 5)
            c = rng.randint(-7, 7)
            d = rng.choice([1, 2])
            e = rng.randint(-5, 5)
            p1 = a * x**3 + b * x**2 + c
            p2 = d * x**3 + e * x + rng.randint(-6, 6)

        p2_dist = p2 if op == "+" else -p2
        ans_expr = sp.simplify(p1 + p2_dist)

        poly1 = sp.Poly(p1, x)
        poly2_dist = sp.Poly(p2_dist, x)

        eq_typst = f"({format_polynomial_typst(p1, x)}) {op} ({format_polynomial_typst(p2, x)})"

        # 1. Unparenthesized expression
        p1_str = format_polynomial_typst(p1, x)
        terms2 = []
        for deg in sorted(poly2_dist.as_dict().keys(), reverse=True):
            c = int(poly2_dist.as_dict()[deg])
            d = deg[0]
            sign_str = "+" if c >= 0 else "-"
            val = abs(c)
            var_p = f"x^{d}" if d > 1 else ("x" if d == 1 else "")
            if val == 1 and var_p:
                t = f"{sign_str} {var_p}"
            elif var_p:
                t = f"{sign_str} {val}{var_p}"
            else:
                t = f"{sign_str} {val}"
            terms2.append(t)
        unparenthesized = f"{p1_str} " + " ".join(terms2)

        # 2. Grouped by degree
        all_degs = sorted(set(list(poly1.as_dict().keys()) + list(poly2_dist.as_dict().keys())), reverse=True)
        grouped = []
        for deg in all_degs:
            d = deg[0]
            c1 = int(poly1.as_dict().get(deg, 0))
            c2 = int(poly2_dist.as_dict().get(deg, 0))
            var_part = f"x^{d}" if d > 1 else ("x" if d == 1 else "")
            if c1 != 0 and c2 != 0:
                c1_val = abs(c1)
                c1_pre = "-" if c1 < 0 else ""
                c1_str = f"{c1_pre}{var_part}" if (c1_val == 1 and var_part) else (f"{c1}{var_part}" if var_part else str(c1))

                sign2 = "+" if c2 >= 0 else "-"
                c2_val = abs(c2)
                c2_str = f"{sign2} {var_part}" if (c2_val == 1 and var_part) else (f"{sign2} {c2_val}{var_part}" if var_part else f"{sign2} {c2_val}")
                grouped.append(f"({c1_str} {c2_str})")
            elif c1 != 0:
                c1_val = abs(c1)
                c1_pre = "-" if c1 < 0 else ""
                c1_str = f"{c1_pre}{var_part}" if (c1_val == 1 and var_part) else (f"{c1}{var_part}" if var_part else str(c1))
                grouped.append(c1_str)
            elif c2 != 0:
                c2_val = abs(c2)
                c2_pre = "-" if c2 < 0 else ""
                c2_str = f"{c2_pre}{var_part}" if (c2_val == 1 and var_part) else (f"{c2}{var_part}" if var_part else str(c2))
                grouped.append(c2_str)

        grouped_str = " + ".join(grouped).replace("+ -", "- ")
        ans_typst = format_polynomial_typst(ans_expr, x)

        step2_phrase = "Distribute negative sign to second polynomial" if op == "-" else "Remove parentheses"
        steps = [
            f"Given expression: $ {eq_typst} $",
            f"{step2_phrase}: $ {unparenthesized} $",
            f"Group like terms by degree: $ {grouped_str} $",
            f"Combine like terms to simplify: $ {ans_typst} $",
        ]

        # Distractors
        # 1: sign error in subtraction or addition
        wrong_op = sp.simplify(p1 + p2) if op == "-" else sp.simplify(p1 - p2)
        d1 = format_polynomial_typst(wrong_op, x)
        d2 = format_polynomial_typst(ans_expr + 2 * x, x)
        d3 = format_polynomial_typst(ans_expr - 3, x)

        return BaseProblem(
            id=f"poly_addsub_{difficulty.value}_{problem_idx}",
            prompt_text="Simplify each expression by adding or subtracting the polynomials.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3] if d != ans_typst][:3],
            difficulty=difficulty,
            standards=self.standards
        )


class PolynomialMultiplyGenerator(BaseGenerator):
    generator_id = "algebra_1.polynomials_multiply"
    name = "Multiplying Polynomials"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.APR.A.1", "TEKS.MATH.A1.10.B"]

    @verify_mathematical_truth()
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x = sp.Symbol('x')

        if difficulty == ProblemDifficulty.MILD:
            # Monomial x Polynomial: a*x * (bx + c) or a * (bx^2 + cx + d)
            a = rng.choice([2, 3, 4, -2, -3])
            b = rng.randint(1, 5)
            c = rng.randint(-6, 6)
            eq_typst = f"{a}x({b}x {'+' if c >= 0 else '-'} {abs(c)})"
            ans_expr = sp.expand(a * x * (b * x + c))
            steps = [
                f"Distribute monomial ${a}x$ to each term inside the parentheses:",
                f"$ ({a}x) dot ({b}x) + ({a}x) dot ({c}) $",
                f"Multiply coefficients and add exponents: $ {format_polynomial_typst(ans_expr, x)} $"
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Binomial x Binomial (FOIL): (ax + b)(cx + d)
            a = rng.choice([1, 1, 2, 3])
            b = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            c = rng.choice([1, 1, 2, 3])
            d = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b_s = f"+ {b}" if b > 0 else f"- {abs(b)}"
            d_s = f"+ {d}" if d > 0 else f"- {abs(d)}"
            a_s = f"{a}x" if a != 1 else "x"
            c_s = f"{c}x" if c != 1 else "x"
            eq_typst = f"({a_s} {b_s})({c_s} {d_s})"
            ans_expr = sp.expand((a * x + b) * (c * x + d))
            ad = a * d
            bc = b * c
            bd = b * d
            s_ad = f"+ {ad}x" if ad >= 0 else f"- {abs(ad)}x"
            s_bc = f"+ {bc}x" if bc >= 0 else f"- {abs(bc)}x"
            s_bd = f"+ {bd}" if bd >= 0 else f"- {abs(bd)}"
            steps = [
                f"Given expression: $ {eq_typst} $",
                f"Apply FOIL: First $({a_s})({c_s}) = {a*c}x^2$, Outside $({a_s})({d}) = {ad}x$, Inside $({b})({c_s}) = {bc}x$, Last $({b})({d}) = {bd}$.",
                f"Write assembled expansion: $ {a*c}x^2 {s_ad} {s_bc} {s_bd} $",
                f"Combine middle like terms: $ {format_polynomial_typst(ans_expr, x)} $"
            ]
        else:  # SPICY: Special products or Binomial x Trinomial
            # Special case: (ax +/- b)^2 or (ax + b)(cx^2 + dx + e)
            subtype = rng.choice(["square", "trinomial"])
            if subtype == "square":
                a = rng.choice([2, 3, 4, 5])
                b = rng.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
                b_s = f"+ {b}" if b > 0 else f"- {abs(b)}"
                eq_typst = f"({a}x {b_s})^2"
                ans_expr = sp.expand((a * x + b)**2)
                steps = [
                    "Use the binomial square pattern: $ (A + B)^2 = A^2 + 2AB + B^2 $",
                    f"$ ({a}x)^2 + 2({a}x)({b}) + ({b})^2 $",
                    f"Result: $ {format_polynomial_typst(ans_expr, x)} $"
                ]
            else:
                a = 1
                b = rng.choice([-3, -2, 2, 3])
                b_s = f"+ {b}" if b > 0 else f"- {abs(b)}"
                c = 1
                d = rng.randint(-3, 3)
                e = rng.randint(-4, 4)
                p2 = c * x**2 + d * x + e
                eq_typst = f"(x {b_s})({format_polynomial_typst(p2, x)})"
                ans_expr = sp.expand((x + b) * p2)
                steps = [
                    "Distribute each term in the binomial across the trinomial:",
                    f"$ x dot ({format_polynomial_typst(p2, x)}) + ({b}) dot ({format_polynomial_typst(p2, x)}) $",
                    f"Combine like terms: $ {format_polynomial_typst(ans_expr, x)} $"
                ]

        ans_typst = format_polynomial_typst(ans_expr, x)
        d1 = format_polynomial_typst(ans_expr - 2 * x, x)
        d2 = format_polynomial_typst(ans_expr + 4, x)
        d3 = format_polynomial_typst(sp.simplify(ans_expr * -1), x)

        return BaseProblem(
            id=f"poly_mult_{difficulty.value}_{problem_idx}",
            prompt_text="Find each product.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in [d1, d2, d3] if d != ans_typst][:3],
            difficulty=difficulty,
            standards=self.standards
        )
