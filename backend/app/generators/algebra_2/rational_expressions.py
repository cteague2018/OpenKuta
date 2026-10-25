from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


def format_lin(var: str, root: int) -> str:
    """Returns (var - root) e.g. root=3 -> (var - 3), root=-2 -> (var + 2)."""
    if root > 0:
        return f"({var} - {root})"
    elif root < 0:
        return f"({var} + {-root})"
    else:
        return var


def format_poly_lin(var: str, root: int) -> str:
    """Returns var - root without parens, e.g. x - 3 or x + 2."""
    if root > 0:
        return f"{var} - {root}"
    elif root < 0:
        return f"{var} + {-root}"
    else:
        return var


class Algebra2RationalExpressionsGenerator(BaseGenerator):
    generator_id = "algebra_2.rational_expressions"
    name = "Rational Expressions & Equations"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSA.APR.D.6", "CCSS.MATH.CONTENT.HSA.REI.A.2"]

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
        """Mild: Simplifying rational expressions with explicit statement of excluded values (e.g. x - 3, quad x != -3)."""
        # (x - r)(x - s) / (x - r) = x - s, excluded value x != r
        roots = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
        r = rng.choice(roots)
        s = rng.choice([x for x in roots if x != r])

        # (x - r)(x - s) = x^2 - (r + s)x + r*s
        b_coeff = -(r + s)
        c_const = r * s

        num_str = "x^2"
        if b_coeff > 0:
            num_str += f" + {b_coeff} x" if b_coeff != 1 else " + x"
        elif b_coeff < 0:
            num_str += f" - {abs(b_coeff)} x" if b_coeff != -1 else " - x"

        if c_const > 0:
            num_str += f" + {c_const}"
        elif c_const < 0:
            num_str += f" - {abs(c_const)}"

        den_str = format_poly_lin("x", r)
        res_str = format_poly_lin("x", s)

        eq_typst = f"({num_str}) / ({den_str})"
        ans_typst = f"{res_str}, quad x != {r}"

        lin_r = format_lin("x", r)
        lin_s = format_lin("x", s)

        steps = [
            f"Factor the numerator: $ {num_str} = {lin_r} {lin_s} $",
            f"Set denominator to zero to identify excluded values: $ {den_str} = 0 ==> x = {r} $",
            f"Write expression in factored form: $ ({lin_r} {lin_s}) / ({lin_r}) $",
            f"Cancel common factor ${lin_r}$ for $x != {r}$: $ {ans_typst} $"
        ]

        distractors = [
            f"{res_str}",
            f"{format_poly_lin('x', r)}, quad x != {s}",
            f"{res_str}, quad x != {-r}"
        ]

        return BaseProblem(
            id=f"a2_rat_mild_{problem_idx}",
            prompt_text="Simplify each rational expression. State any excluded values.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Multiplying and dividing rational expressions with excluded values."""
        op = rng.choice(["multiply", "divide"])

        # Construct: (x - a) / (x - b) * (x - b)(x - c) / (x - a)(x - d)
        # Result: (x - c) / (x - d)
        # Excluded values from all denominators
        # Distinct roots for factors
        a, b, c, d = rng.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6], 4)

        la = format_lin("x", a)
        lb = format_lin("x", b)
        lc = format_lin("x", c)
        ld = format_lin("x", d)

        if op == "multiply":
            # (x - a)/(x - b) * ((x - b)(x - c)) / ((x - a)(x - d))
            # = (x - c) / (x - d), x != b, a, d
            eq_typst = f"({la}) / ({lb}) dot ({lb} {lc}) / ({la} {ld})"
            ans_typst = f"({lc}) / ({ld}), quad x != {b}, {a}, {d}"

            steps = [
                f"Identify excluded values where denominators are zero: $ {lb} = 0 ==> x = {b} $, $ {la} = 0 ==> x = {a} $, $ {ld} = 0 ==> x = {d} $",
                f"Multiply numerators and denominators: $ ({la} dot {lb} {lc}) / ({lb} dot {la} {ld}) $",
                f"Cancel common factors ${la}$ and ${lb}$",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"({lc}) / ({ld})",
                f"({lc}) / ({ld}), quad x != {b}",
                f"({la}) / ({ld}), quad x != {b}, {a}"
            ]

            prompt = "Multiply and simplify each rational expression. State all excluded values."
        else:
            # Division: ((x - a)(x - c)) / (x - b) / ((x - a)(x - d)) / (x - b)
            # = (x - c) / (x - d), excluded values: b, a, d
            eq_typst = f"({la} {lc}) / ({lb}) div ({la} {ld}) / ({lb})"
            ans_typst = f"({lc}) / ({ld}), quad x != {b}, {a}, {d}"

            steps = [
                f"Convert division to multiplication by the reciprocal: $ ({la} {lc}) / ({lb}) dot ({lb}) / ({la} {ld}) $",
                f"Determine excluded values from all denominators and divisor numerator: $ x != {b}, {a}, {d} $",
                f"Multiply and cancel common factors ${la}$ and ${lb}$: $ ({la} {lc} dot {lb}) / ({lb} dot {la} {ld}) $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"({lc}) / ({ld})",
                f"({lc}) / ({ld}), quad x != {b}",
                f"({ld}) / ({lc}), quad x != {b}, {a}, {d}"
            ]

            prompt = "Divide and simplify each rational expression. State all excluded values."

        return BaseProblem(
            id=f"a2_rat_med_{problem_idx}",
            prompt_text=prompt,
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Adding and subtracting rational expressions with unlike denominators."""
        op = rng.choice(["+", "-"])
        r = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        s = rng.choice([x for x in [-4, -3, -2, -1, 1, 2, 3, 4] if x != r])

        A = rng.choice([2, 3, 4, 5])
        B = rng.choice([1, 2, 3, 4])

        lr = format_lin("x", r)
        ls = format_lin("x", s)

        eq_typst = f"{A} / {lr} {op} {B} / {ls}"

        # A/(x - r) +/- B/(x - s) = [A(x - s) +/- B(x - r)] / [(x - r)(x - s)]
        # Numerator:
        # If +: (A + B)x - (A*s + B*r)
        # If -: (A - B)x - (A*s - B*r)
        if op == "+":
            nx = A + B
            nc = -(A * s + B * r)
        else:
            nx = A - B
            nc = -(A * s - B * r)

        num_parts = []
        if nx == 1:
            num_parts.append("x")
        elif nx == -1:
            num_parts.append("-x")
        elif nx != 0:
            num_parts.append(f"{nx} x")

        if nc > 0:
            num_parts.append(f"+ {nc}")
        elif nc < 0:
            num_parts.append(f"- {abs(nc)}")
        elif not num_parts:
            num_parts.append("0")

        num_str = " ".join(num_parts)
        ans_typst = f"({num_str}) / ({lr} {ls}), quad x != {r}, {s}"

        steps = [
            f"Find the least common denominator (LCD): $ {lr} {ls} $",
            f"State excluded values where denominators vanish: $ x != {r}, {s} $",
            f"Rewrite each term with the LCD: $ ({A} {ls}) / ({lr} {ls}) {op} ({B} {lr}) / ({lr} {ls}) $",
            f"Expand numerators: $ {A}(x {'-' if s >= 0 else '+'} {abs(s)}) = {A} x {'-' if A*s >= 0 else '+'} {abs(A*s)} $ and $ {B}(x {'-' if r >= 0 else '+'} {abs(r)}) = {B} x {'-' if B*r >= 0 else '+'} {abs(B*r)} $",
            f"Combine like terms in the numerator: $ ({num_str}) / ({lr} {ls}) $",
            f"Result: $ {ans_typst} $"
        ]

        distractors = [
            f"({num_str}) / ({lr} {ls})",
            f"({A + B if op == '+' else A - B}) / ({lr} {ls}), quad x != {r}, {s}",
            f"({num_str}) / ({lr}), quad x != {r}"
        ]

        return BaseProblem(
            id=f"a2_rat_spicy_{problem_idx}",
            prompt_text="Perform the operation and simplify. State any excluded values.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
