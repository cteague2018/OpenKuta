from __future__ import annotations

import random
from typing import List

import sympy as sp

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.core.typst_utils import format_polynomial_typst


def _poly_from_coeffs(coeffs: List[int], var: sp.Symbol = sp.Symbol('x')) -> sp.Expr:
    """Build a SymPy polynomial expression from a list of descending coefficients."""
    deg = len(coeffs) - 1
    expr = sp.Integer(0)
    for i, c in enumerate(coeffs):
        p = deg - i
        expr += c * (var ** p)
    return expr


def _format_division_ans(
    q_expr: sp.Expr,
    r_val: int | sp.Expr,
    d_expr: sp.Expr,
    var: sp.Symbol = sp.Symbol('x')
) -> str:
    """Format quotient and remainder cleanly in Typst math."""
    q_str = format_polynomial_typst(q_expr, var)
    if r_val == 0:
        return q_str

    d_str = format_polynomial_typst(d_expr, var)
    r_int = int(r_val) if isinstance(r_val, (int, sp.Integer)) else r_val

    if isinstance(r_int, int) and r_int < 0:
        rem_part = f"- ({abs(r_int)}) / ({d_str})"
    else:
        rem_part = f"+ ({r_int}) / ({d_str})"

    if q_str == "0":
        return f"({r_int}) / ({d_str})" if not (isinstance(r_int, int) and r_int < 0) else f"-({abs(r_int)}) / ({d_str})"
    return f"{q_str} {rem_part}"


class PolynomialDivisionGenerator(BaseGenerator):
    generator_id = "algebra_2.polynomial_division"
    name = "Polynomial Long Division & Synthetic Division"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSA.APR.B.2", "CCSS.MATH.CONTENT.HSA.APR.D.6"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        x = sp.Symbol('x')
        if difficulty == ProblemDifficulty.MILD:
            return self._generate_mild(rng, problem_idx, x)
        elif difficulty == ProblemDifficulty.MEDIUM:
            return self._generate_medium(rng, problem_idx, x)
        else:
            return self._generate_spicy(rng, problem_idx, x)

    def _generate_mild(self, rng: random.Random, problem_idx: int, x: sp.Symbol) -> BaseProblem:
        """Mild: Division of quadratic or cubic by (x - c) with remainder 0."""
        is_cubic = rng.choice([False, True])
        roots_pool = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]

        if not is_cubic:
            # (x^2 + bx + c) / (x - r) = x - s
            r = rng.choice(roots_pool)
            s = rng.choice([v for v in roots_pool if v != r])

            d_expr = x - r
            q_expr = x - s
            p_expr = sp.expand(q_expr * d_expr)

            p_str = format_polynomial_typst(p_expr, x)
            d_str = format_polynomial_typst(d_expr, x)
            q_str = format_polynomial_typst(q_expr, x)
            eq_typst = f"({p_str}) / ({d_str})"
            ans_typst = q_str

            b_coeff = -(r + s)
            c_const = r * s

            steps = [
                f"Identify the divisor root: $ {d_str} = 0 ==> x = {r} $",
                f"Dividend coefficients: $ [{1}, {b_coeff}, {c_const}] $",
                f"Synthetic division by $x = {r}$:",
                "  1. Bring down the leading coefficient: $ 1 $",
                f"  2. Multiply $ {r} dot 1 = {r} $, add to $ {b_coeff} $: $ {b_coeff} + ({r}) = {-s} $",
                f"  3. Multiply $ {r} dot ({-s}) = {-r * s} $, add to $ {c_const} $: $ {c_const} + ({-r * s}) = 0 $ (remainder)",
                f"Quotient: $ {ans_typst} $ with remainder $ 0 $",
                f"Final answer: $ {ans_typst} $"
            ]

            # Distractors: sign errors or root misconception
            d1 = format_polynomial_typst(x + s, x)
            d2 = format_polynomial_typst(x - r, x)
            d3 = format_polynomial_typst(x + (s if s != 0 else 1) + 1, x)

        else:
            # Cubic / linear: (x - r)(x - s)(x - t) / (x - r) = (x - s)(x - t)
            r = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            s = rng.choice([-3, -2, -1, 1, 2, 3])
            t = rng.choice([-3, -2, -1, 1, 2, 3])

            d_expr = x - r
            q_expr = sp.expand((x - s) * (x - t))
            p_expr = sp.expand(q_expr * d_expr)

            p_str = format_polynomial_typst(p_expr, x)
            d_str = format_polynomial_typst(d_expr, x)
            q_str = format_polynomial_typst(q_expr, x)
            eq_typst = f"({p_str}) / ({d_str})"
            ans_typst = q_str

            poly_p = sp.Poly(p_expr, x)
            p_coeffs = poly_p.all_coeffs()

            # Synthetic division trace
            c0, c1, c2, c3 = [int(v) for v in p_coeffs]
            q0 = c0
            m1 = r * q0
            q1 = c1 + m1
            m2 = r * q1
            q2 = c2 + m2
            m3 = r * q2
            c3 + m3

            steps = [
                f"Identify divisor root: $ {d_str} = 0 ==> x = {r} $",
                f"Coefficients of dividend: $ [{', '.join(str(c) for c in p_coeffs)}] $",
                "Perform synthetic division:",
                f"  - Bring down $ {q0} $",
                f"  - Multiply $ {r} dot {q0} = {m1} $, add: $ {c1} + ({m1}) = {q1} $",
                f"  - Multiply $ {r} dot {q1} = {m2} $, add: $ {c2} + ({m2}) = {q2} $",
                f"  - Multiply $ {r} dot {q2} = {m3} $, add: $ {c3} + ({m3}) = 0 $ (remainder)",
                f"Quotient polynomial: $ {ans_typst} $",
                f"Final answer: $ {ans_typst} $"
            ]

            # Distractors: sign error on linear or constant term, or wrong root
            q_poly = sp.Poly(q_expr, x)
            qc = [int(c) for c in q_poly.all_coeffs()]  # [1, q1, q2]
            d1 = format_polynomial_typst(_poly_from_coeffs([qc[0], -qc[1], qc[2]], x), x)
            d2 = format_polynomial_typst(_poly_from_coeffs([qc[0], qc[1], -qc[2]], x), x)
            d3 = format_polynomial_typst(_poly_from_coeffs([qc[0], -qc[1], -qc[2]], x), x)

        valid_distractors = [d for d in dict.fromkeys([d1, d2, d3]) if d != ans_typst][:3]
        while len(valid_distractors) < 3:
            cand = format_polynomial_typst(x**2 + (len(valid_distractors) + 1) * x - 2, x)
            if cand not in valid_distractors and cand != ans_typst:
                valid_distractors.append(cand)

        return BaseProblem(
            id=f"alg2_polydiv_mild_{problem_idx}",
            prompt_text="Divide each polynomial using long division or synthetic division.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=valid_distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int, x: sp.Symbol) -> BaseProblem:
        """Medium: Division of cubic by (x - c) with non-zero remainder."""
        a = rng.choice([1, 1, 2])
        q1 = rng.randint(-4, 4)
        q0 = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        r = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        rem = rng.choice([-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8])

        q_expr = a * (x**2) + q1 * x + q0
        d_expr = x - r
        p_expr = sp.expand(q_expr * d_expr + rem)

        p_str = format_polynomial_typst(p_expr, x)
        d_str = format_polynomial_typst(d_expr, x)
        eq_typst = f"({p_str}) / ({d_str})"
        ans_typst = _format_division_ans(q_expr, rem, d_expr, x)

        poly_p = sp.Poly(p_expr, x)
        p_coeffs = [int(c) for c in poly_p.all_coeffs()]
        c0, c1, c2, c3 = p_coeffs

        # Step by step calculation
        step_q0 = c0
        step_m1 = r * step_q0
        step_q1 = c1 + step_m1
        step_m2 = r * step_q1
        step_q2 = c2 + step_m2
        step_m3 = r * step_q2
        step_rem = c3 + step_m3

        steps = [
            f"Divisor is $ {d_str} $. Root: $ x = {r} $",
            f"Dividend coefficients: $ [{', '.join(str(c) for c in p_coeffs)}] $",
            "Synthetic Division table:",
            f"  - Bring down leading coefficient: $ {step_q0} $",
            f"  - Multiply $ {r} dot {step_q0} = {step_m1} $, add: $ {c1} + ({step_m1}) = {step_q1} $",
            f"  - Multiply $ {r} dot {step_q1} = {step_m2} $, add: $ {c2} + ({step_m2}) = {step_q2} $",
            f"  - Multiply $ {r} dot {step_q2} = {step_m3} $, add: $ {c3} + ({step_m3}) = {step_rem} $ (Remainder)",
            f"Quotient: $ Q(x) = {format_polynomial_typst(q_expr, x)} $, Remainder: $ R = {rem} $",
            f"Express result as $ Q(x) + R / ({d_str}) $:",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: Remainder sign mistake: -rem instead of rem
        d1 = _format_division_ans(q_expr, -rem, d_expr, x)

        # Distractor 2: Synthetic division using opposite root -r
        wrong_r = -r
        wq0 = c0
        wq1 = c1 + wrong_r * wq0
        wq2 = c2 + wrong_r * wq1
        w_rem = c3 + wrong_r * wq2
        wrong_q_expr = wq0 * (x**2) + wq1 * x + wq2
        d2 = _format_division_ans(wrong_q_expr, w_rem, d_expr, x)

        # Distractor 3: Off-by-one in constant term of quotient
        off_q_expr = a * (x**2) + q1 * x + (q0 + 1 if q0 > 0 else q0 - 1)
        d3 = _format_division_ans(off_q_expr, rem, d_expr, x)

        # Distractor 4: Forgot to divide remainder: Q(x) + R
        d4 = f"{format_polynomial_typst(q_expr, x)} + {rem}" if rem > 0 else f"{format_polynomial_typst(q_expr, x)} - {abs(rem)}"

        distractors = [d for d in [d1, d2, d3, d4] if d != ans_typst]
        valid_distractors = list(dict.fromkeys(distractors))[:3]
        while len(valid_distractors) < 3:
            fake_r = rem + len(valid_distractors) + 2
            cand = _format_division_ans(q_expr, fake_r, d_expr, x)
            if cand not in valid_distractors and cand != ans_typst:
                valid_distractors.append(cand)

        return BaseProblem(
            id=f"alg2_polydiv_med_{problem_idx}",
            prompt_text="Divide each polynomial using long division or synthetic division.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=valid_distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int, x: sp.Symbol) -> BaseProblem:
        """Spicy: Division by linear binomial with leading coefficient (ax - c) or missing term."""
        sub_type = rng.choice(["missing_term", "leading_coeff"])

        if sub_type == "missing_term":
            # Missing x^2 term in cubic dividend: (x^3 + 0*x^2 + b*x + c) / (x - r)
            r = rng.choice([-3, -2, 2, 3])
            q1 = r  # guarantees q1 - r = 0, so coefficient of x^2 in P(x) is exactly 0
            q0 = rng.choice([-6, -5, -4, 4, 5, 6])
            rem = rng.choice([-7, -5, -3, 3, 5, 7])

            q_expr = x**2 + q1 * x + q0
            d_expr = x - r
            p_expr = sp.expand(q_expr * d_expr + rem)

            p_str = format_polynomial_typst(p_expr, x)
            d_str = format_polynomial_typst(d_expr, x)
            eq_typst = f"({p_str}) / ({d_str})"
            ans_typst = _format_division_ans(q_expr, rem, d_expr, x)

            p_poly = sp.Poly(p_expr, x)
            [int(c) for c in p_poly.all_coeffs()]
            # With degree 3 and missing x^2: coefficients are [1, 0, p_coeffs[1], p_coeffs[2]]
            # Let's verify p_coeffs has 4 terms including 0
            dense_coeffs = [int(p_poly.coeff_monomial(x**3)), int(p_poly.coeff_monomial(x**2)), int(p_poly.coeff_monomial(x**1)), int(p_poly.coeff_monomial(x**0))]

            steps = [
                f"Dividend: $ {p_str} $",
                f"Divisor: $ {d_str} ==> x = {r} $",
                "IMPORTANT: The dividend is missing the $x^2$ term. Insert placeholder $ 0 x^2 $:",
                f"  $ x^3 + 0 x^2 + ({dense_coeffs[2]}) x + ({dense_coeffs[3]}) $",
                f"Set up synthetic division using coefficients $ [{', '.join(str(c) for c in dense_coeffs)}] $:",
                "  - Bring down $ 1 $",
                f"  - Multiply $ {r} dot 1 = {r} $, add to 0: $ 0 + ({r}) = {q1} $",
                f"  - Multiply $ {r} dot {q1} = {r * q1} $, add to $ {dense_coeffs[2]} $: $ {dense_coeffs[2]} + ({r * q1}) = {q0} $",
                f"  - Multiply $ {r} dot {q0} = {r * q0} $, add to $ {dense_coeffs[3]} $: $ {dense_coeffs[3]} + ({r * q0}) = {rem} $",
                f"Quotient: $ Q(x) = {format_polynomial_typst(q_expr, x)} $, Remainder: $ R = {rem} $",
                f"Final answer: $ {ans_typst} $"
            ]

            # Distractor 1: Student omits the 0 placeholder (classic misconception)
            omitted_coeffs = [dense_coeffs[0], dense_coeffs[2], dense_coeffs[3]]
            w0 = omitted_coeffs[0]
            w1 = omitted_coeffs[1] + r * w0
            w_rem = omitted_coeffs[2] + r * w1
            w_q_expr = w0 * x + w1
            d1 = _format_division_ans(w_q_expr, w_rem, d_expr, x)

            # Distractor 2: Remainder sign flipped
            d2 = _format_division_ans(q_expr, -rem, d_expr, x)

            # Distractor 3: Root sign flipped
            d3 = _format_division_ans(x**2 - q1 * x + q0, rem, d_expr, x)

        else:
            # Division by linear binomial with leading coefficient: (ax - c) where a in [2, 3]
            a = rng.choice([2, 3])
            c_val = rng.choice([-3, -1, 1, 3])
            while sp.gcd(a, abs(c_val)) != 1:
                c_val = rng.choice([-3, -1, 1, 3])

            d_expr = a * x - c_val
            # Construct integer quotient Q(x) = q2*x^2 + q1*x + q0
            q2 = rng.choice([1, 2, 3])
            q1 = rng.randint(-3, 3)
            q0 = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            rem = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

            q_expr = q2 * (x**2) + q1 * x + q0
            p_expr = sp.expand(q_expr * d_expr + rem)

            p_str = format_polynomial_typst(p_expr, x)
            d_str = format_polynomial_typst(d_expr, x)
            eq_typst = f"({p_str}) / ({d_str})"
            ans_typst = _format_division_ans(q_expr, rem, d_expr, x)

            lead_p_coeff = a * q2
            f"+ {abs(c_val)}" if c_val < 0 else f"- {c_val}"

            sub1 = sp.expand(q2 * (x**2) * d_expr)
            diff1 = sp.expand(p_expr - sub1)
            diff1_str = format_polynomial_typst(diff1, x)

            sub2 = sp.expand(q1 * x * d_expr)
            diff2 = sp.expand(diff1 - sub2)
            diff2_str = format_polynomial_typst(diff2, x)

            sub3 = sp.expand(q0 * d_expr)

            steps = [
                f"Set up Polynomial Long Division: $ ({p_str}) / ({d_str}) $",
                f"Step 1: Divide leading terms: $ ({lead_p_coeff} x^3) / ({a} x) = {q2} x^2 $",
                f"  Multiply and subtract from dividend: $ ({p_str}) - ({format_polynomial_typst(sub1, x)}) = {diff1_str} $",
                f"Step 2: Divide leading term: $ ({format_polynomial_typst(sp.LT(diff1), x)}) / ({a} x) = {format_polynomial_typst(q1 * x, x) if q1 != 0 else '0'} $",
                f"  Multiply and subtract: $ ({diff1_str}) - ({format_polynomial_typst(sub2, x)}) = {diff2_str} $",
                f"Step 3: Divide leading term: $ ({format_polynomial_typst(sp.LT(diff2), x)}) / ({a} x) = {q0} $",
                f"  Multiply and subtract to find remainder: $ ({diff2_str}) - ({format_polynomial_typst(sub3, x)}) = {rem} $",
                f"Quotient: $ Q(x) = {format_polynomial_typst(q_expr, x)} $, Remainder: $ R = {rem} $",
                f"Result: $ {ans_typst} $"
            ]

            # Distractor 1: Forgot to divide synthetic division row by leading coefficient 'a'
            unscaled_q = (a * q2) * (x**2) + (a * q1) * x + (a * q0)
            d1 = _format_division_ans(unscaled_q, rem, d_expr, x)

            # Distractor 2: Remainder sign flipped
            d2 = _format_division_ans(q_expr, -rem, d_expr, x)

            # Distractor 3: Sign error on middle term of quotient
            mod_q = q2 * (x**2) + (-q1 if q1 != 0 else 1) * x + q0
            d3 = _format_division_ans(mod_q, rem, d_expr, x)

        distractors = [d for d in [d1, d2, d3] if d != ans_typst]
        valid_distractors = list(dict.fromkeys(distractors))[:3]
        while len(valid_distractors) < 3:
            fake_r = rem + len(valid_distractors) + 2
            cand = _format_division_ans(q_expr, fake_r, d_expr, x)
            if cand not in valid_distractors and cand != ans_typst:
                valid_distractors.append(cand)

        return BaseProblem(
            id=f"alg2_polydiv_spicy_{problem_idx}",
            prompt_text="Divide each polynomial using long division or synthetic division.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=valid_distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
