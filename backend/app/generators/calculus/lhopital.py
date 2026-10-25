from __future__ import annotations

import math
import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


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


class LhopitalGenerator(BaseGenerator):
    generator_id = "calculus.lhopital"
    name = "L'Hôpital's Rule & Indeterminate Limits"
    category = "Calculus"
    standards = ["AP.CALC.LIM.3", "AP.CALC.LIM.4"]

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
            return self._generate_medium(rng, problem_idx)
        else:
            return self._generate_spicy(rng, problem_idx)

    def _generate_mild(self, rng: random.Random, problem_idx: int, allow_negatives: bool) -> BaseProblem:
        """Mild: Indeterminate 0/0 limits of rational functions resolved with one application of L'Hôpital's Rule."""
        flavor = rng.choice(["diff_of_squares", "factored_quadratic"])

        if flavor == "diff_of_squares":
            c = rng.choice([-4, -3, -2, 2, 3, 4, 5]) if allow_negatives else rng.choice([2, 3, 4, 5])
            c_sq = c * c
            a = rng.choice([1, 2, 3])

            num_str = f"x^2 - {c_sq}" if a == 1 else f"{a} x^2 - {a * c_sq}"
            den_str = f"x - {c}" if c > 0 else f"x + {-c}"

            eq_typst = f"$ lim_(x -> {c}) ({num_str}) / ({den_str}) $"
            ans_val = 2 * a * c
            ans_typst = f"$ {ans_val} $"

            d_num = "2 x" if a == 1 else f"{2 * a} x"
            d_den = "1"

            steps = [
                f"Evaluate by direct substitution: $ ({num_str.replace('x', str(c))}) / ({den_str.replace('x', str(c))}) = 0/0 $ (indeterminate form).",
                "Since both numerator and denominator are differentiable and form $ 0/0 $, apply L'Hôpital's Rule:",
                f"$ lim_(x -> {c}) (f(x))/(g(x)) = lim_(x -> {c}) (f'(x))/(g'(x)) $",
                f"Differentiate the numerator: $ (d)/(d x)[{num_str}] = {d_num} $",
                f"Differentiate the denominator: $ (d)/(d x)[{den_str}] = {d_den} $",
                f"Evaluate the new limit: $ lim_(x -> {c}) ({d_num}) / ({d_den}) = ({2 * a}({c})) / 1 = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            distractors = ensure_distractors(
                [f"$ {a * c} $", f"$ {-ans_val} $", f"$ {ans_val + 2} $", "$ 0 $"],
                ans_typst,
                ["$ 1 $", "$ text(\"Does not exist\") $", f"$ {ans_val - 1} $", f"$ {c} $"]
            )

        else:
            # Numerator: (x - c)(x - r) = x^2 - (c + r)x + c*r
            c = rng.choice([-3, -2, 1, 2, 3, 4]) if allow_negatives else rng.choice([1, 2, 3, 4])
            r = rng.choice([-4, -1, 3, 5])
            while r == c:
                r += 1

            b = -(c + r)
            d = c * r
            b_sign = f"- {-b}" if b < 0 else f"+ {b}"
            d_sign = f"- {-d}" if d < 0 else f"+ {d}"
            num_str = f"x^2 {b_sign} x {d_sign}"
            den_str = f"x - {c}" if c > 0 else f"x + {-c}"

            eq_typst = f"$ lim_(x -> {c}) ({num_str}) / ({den_str}) $"
            ans_val = 2 * c + b  # = c - r
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Evaluate by direct substitution: $ 0/0 $ (indeterminate form).",
                f"Apply L'Hôpital's Rule: $ lim_(x -> {c}) (f'(x))/(g'(x)) $",
                f"Differentiate the numerator: $ (d)/(d x)[{num_str}] = 2 x {b_sign} $",
                f"Differentiate the denominator: $ (d)/(d x)[{den_str}] = 1 $",
                f"Evaluate at $ x = {c} $: $ 2({c}) {b_sign} = {2 * c} {b_sign} = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            distractors = ensure_distractors(
                [f"$ {c + r} $", "$ 0 $", f"$ {-ans_val} $", f"$ {ans_val + 1} $"],
                ans_typst,
                ["$ 1 $", "$ text(\"Does not exist\") $", f"$ {d} $", f"$ {c} $"]
            )

        return BaseProblem(
            id=f"calc_lhopital_mild_{problem_idx}",
            prompt_text="Evaluate each indeterminate limit using L'Hôpital's Rule.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Indeterminate 0/0 with trigonometric or exponential expressions."""
        flavor = rng.choice(["sin_kx", "exp_kx", "tan_kx", "ln_1kx"])

        if flavor == "sin_kx":
            a = rng.choice([2, 3, 4, 5, 6, 7])
            b = rng.choice([2, 3, 4, 5])
            while a == b:
                b = rng.choice([2, 3, 4, 5, 7])

            eq_typst = f"$ lim_(x -> 0) (sin({a} x)) / ({b} x) $"
            ans_val = format_fraction_typst(a, b)
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Evaluate by direct substitution: $ (sin(0)) / (0) = 0/0 $ (indeterminate form).",
                "Apply L'Hôpital's Rule: differentiate numerator and denominator with respect to $ x $:",
                f"$ (d)/(d x)[sin({a} x)] = {a} cos({a} x) $",
                f"$ (d)/(d x)[{b} x] = {b} $",
                f"Evaluate the limit: $ lim_(x -> 0) ({a} cos({a} x)) / ({b}) = ({a} cos(0)) / ({b}) = ({a} dot 1) / ({b}) = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            d1 = f"$ {format_fraction_typst(b, a)} $"
            d2 = "$ 0 $"
            d3 = "$ 1 $"
            d4 = f"$ {a * b} $"

            distractors = ensure_distractors([d1, d2, d3, d4], ans_typst, ["$ text(\"Does not exist\") $", "$ 1/2 $", "$ 2 $"])

        elif flavor == "exp_kx":
            k = rng.choice([2, 3, 4, 5])
            m = rng.choice([1, 2, 3])

            num_str = f"e^({k} x) - 1"
            den_str = f"{m} x" if m > 1 else "x"
            eq_typst = f"$ lim_(x -> 0) ({num_str}) / ({den_str}) $"
            ans_val = format_fraction_typst(k, m)
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Direct substitution gives: $ (e^0 - 1) / (0) = 0/0 $ (indeterminate form).",
                "Apply L'Hôpital's Rule by taking derivatives of numerator and denominator:",
                f"$ (d)/(d x)[e^({k} x) - 1] = {k} e^({k} x) $",
                f"$ (d)/(d x)[{den_str}] = {m} $",
                f"Evaluate limit: $ lim_(x -> 0) ({k} e^({k} x)) / ({m}) = ({k} e^0) / ({m}) = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            d1 = f"$ {format_fraction_typst(m, k)} $"
            d2 = "$ 0 $"
            d3 = "$ 1 $"
            d4 = f"$ {k * m} $"

            distractors = ensure_distractors([d1, d2, d3, d4], ans_typst, ["$ e $", "$ text(\"Does not exist\") $", "$ 1/2 $"])

        elif flavor == "tan_kx":
            a = rng.choice([2, 3, 4, 5])
            b = rng.choice([1, 2, 3])

            den_str = f"{b} x" if b > 1 else "x"
            eq_typst = f"$ lim_(x -> 0) (tan({a} x)) / ({den_str}) $"
            ans_val = format_fraction_typst(a, b)
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Direct substitution: $ (tan(0)) / (0) = 0/0 $ (indeterminate form).",
                "Apply L'Hôpital's Rule:",
                f"$ (d)/(d x)[tan({a} x)] = {a} sec^2({a} x) $",
                f"$ (d)/(d x)[{den_str}] = {b} $",
                f"Evaluate limit: $ lim_(x -> 0) ({a} sec^2({a} x)) / ({b}) = ({a} sec^2(0)) / ({b}) = ({a} dot 1) / ({b}) = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            d1 = f"$ {format_fraction_typst(b, a)} $"
            d2 = "$ 0 $"
            d3 = "$ 1 $"
            d4 = f"$ {a + b} $"

            distractors = ensure_distractors([d1, d2, d3, d4], ans_typst, ["$ text(\"Does not exist\") $", "$ 2 $", "$ 1/4 $"])

        else:
            # ln(1 + a x) / (b x)
            a = rng.choice([2, 3, 4, 5])
            b = rng.choice([1, 2, 3])

            den_str = f"{b} x" if b > 1 else "x"
            eq_typst = f"$ lim_(x -> 0) (ln(1 + {a} x)) / ({den_str}) $"
            ans_val = format_fraction_typst(a, b)
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Direct substitution: $ (ln(1)) / (0) = 0/0 $ (indeterminate form).",
                "Apply L'Hôpital's Rule:",
                f"$ (d)/(d x)[ln(1 + {a} x)] = ({a}) / (1 + {a} x) $",
                f"$ (d)/(d x)[{den_str}] = {b} $",
                f"Evaluate limit: $ lim_(x -> 0) (({a}) / (1 + {a} x)) / ({b}) = ({a} / 1) / ({b}) = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            d1 = f"$ {format_fraction_typst(b, a)} $"
            d2 = "$ 0 $"
            d3 = "$ 1 $"
            d4 = f"$ {a} $"

            distractors = ensure_distractors([d1, d2, d3, d4], ans_typst, ["$ text(\"Does not exist\") $", "$ 1/2 $", "$ 3 $"])

        return BaseProblem(
            id=f"calc_lhopital_med_{problem_idx}",
            prompt_text="Evaluate each trigonometric or exponential indeterminate limit using L'Hôpital's Rule.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Indeterminate infinity/infinity or requiring two applications of L'Hôpital's Rule."""
        flavor = rng.choice(["two_steps_zero", "two_steps_finite", "two_steps_trig", "two_steps_rational_infinity"])

        if flavor == "two_steps_zero":
            # lim_{x -> oo} (a x^2) / e^(k x) -> 0
            a = rng.choice([1, 2, 3, 4])
            k = rng.choice([1, 2, 3])
            num_str = f"{a} x^2" if a > 1 else "x^2"
            exp_str = f"e^({k} x)" if k > 1 else "e^x"

            eq_typst = f"$ lim_(x -> infinity) ({num_str}) / ({exp_str}) $"
            ans_typst = "$ 0 $"

            d1_num = f"{2 * a} x"
            d1_den = f"{k} {exp_str}" if k > 1 else exp_str

            d2_num = f"{2 * a}"
            d2_den = f"{k**2} {exp_str}" if k > 1 else exp_str

            steps = [
                "Direct substitution gives indeterminate form: $ (infinity) / (infinity) $",
                "Apply L'Hôpital's Rule (1st application):",
                f"$ lim_(x -> infinity) (f'(x))/(g'(x)) = lim_(x -> infinity) ({d1_num}) / ({d1_den}) $",
                f"Checking direct substitution again: $ ({d1_num}) / ({d1_den}) = (infinity) / (infinity) $ (still indeterminate).",
                "Apply L'Hôpital's Rule a second time (2nd application):",
                f"$ lim_(x -> infinity) (f''(x))/(g''(x)) = lim_(x -> infinity) ({d2_num}) / ({d2_den}) $",
                f"As $ x -> infinity $, the denominator grows without bound while numerator is constant: $ {d2_num} / (infinity) = 0 $",
                f"Result: {ans_typst}"
            ]

            distractors = ensure_distractors(
                ["$ infinity $", "$ 1 $", f"$ {2 * a} $", f"$ {format_fraction_typst(2 * a, k**2)} $"],
                ans_typst,
                ["$ text(\"Does not exist\") $", "$ -1 $", "$ 1/2 $"]
            )

        elif flavor == "two_steps_finite":
            # lim_{x -> 0} (e^(k x) - k x - 1) / (x^2) -> k^2 / 2
            k = rng.choice([2, 3, 4, 5])
            eq_typst = f"$ lim_(x -> 0) (e^({k} x) - {k} x - 1) / (x^2) $"
            ans_val = format_fraction_typst(k**2, 2)
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Direct substitution: $ (e^0 - 0 - 1) / (0) = 0/0 $ (indeterminate form).",
                "Apply L'Hôpital's Rule (1st application):",
                f"$ lim_(x -> 0) ({k} e^({k} x) - {k}) / (2 x) $",
                f"Evaluate again: $ ({k} - {k}) / (0) = 0/0 $ (still indeterminate).",
                "Apply L'Hôpital's Rule a second time (2nd application):",
                f"$ lim_(x -> 0) ({k**2} e^({k} x)) / (2) $",
                f"Evaluate by substitution: $ ({k**2} e^0) / 2 = ({k**2} dot 1) / 2 = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            d1 = f"$ {k**2} $"  # forgot factor of 2 from x^2 derivative
            d2 = f"$ {k} $"
            d3 = "$ 0 $"
            d4 = f"$ {format_fraction_typst(k, 2)} $"

            distractors = ensure_distractors([d1, d2, d3, d4], ans_typst, ["$ 1 $", "$ infinity $", "$ text(\"Does not exist\") $"])

        elif flavor == "two_steps_trig":
            # lim_{x -> 0} (1 - cos(k x)) / (a x^2) -> k^2 / (2 a)
            k = rng.choice([2, 3, 4, 6])
            a = rng.choice([1, 2, 3])
            den_str = f"{a} x^2" if a > 1 else "x^2"
            eq_typst = f"$ lim_(x -> 0) (1 - cos({k} x)) / ({den_str}) $"
            ans_val = format_fraction_typst(k**2, 2 * a)
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Direct substitution: $ (1 - cos(0)) / (0) = (1 - 1) / 0 = 0/0 $ (indeterminate form).",
                "Apply L'Hôpital's Rule (1st application):",
                f"$ lim_(x -> 0) ({k} sin({k} x)) / ({2 * a} x) $",
                f"Evaluate again: $ ({k} sin(0)) / (0) = 0/0 $ (still indeterminate).",
                "Apply L'Hôpital's Rule a second time (2nd application):",
                f"$ lim_(x -> 0) ({k**2} cos({k} x)) / ({2 * a}) $",
                f"Evaluate limit: $ ({k**2} cos(0)) / ({2 * a}) = ({k**2} dot 1) / ({2 * a}) = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            d1 = f"$ {format_fraction_typst(k, 2 * a)} $"
            d2 = f"$ {format_fraction_typst(k**2, a)} $"
            d3 = "$ 0 $"
            d4 = "$ 1 $"

            distractors = ensure_distractors([d1, d2, d3, d4], ans_typst, ["$ text(\"Does not exist\") $", "$ 1/2 $", "$ 2 $"])

        else:
            # lim_{x -> oo} (a x^2 + b x) / (c x^2 + d) -> a / c via two L'Hopital applications
            a = rng.choice([2, 3, 4, 6, 8])
            c = rng.choice([2, 3, 5, 6])
            while a == c:
                c = rng.choice([2, 3, 5, 7])
            b = rng.choice([1, 3, 5, -2, -4])
            d = rng.choice([1, 2, 4, 7])

            b_sign = f"- {-b}" if b < 0 else f"+ {b}"
            num_str = f"{a} x^2 {b_sign} x"
            den_str = f"{c} x^2 + {d}"

            eq_typst = f"$ lim_(x -> infinity) ({num_str}) / ({den_str}) $"
            ans_val = format_fraction_typst(a, c)
            ans_typst = f"$ {ans_val} $"

            steps = [
                "Direct substitution gives indeterminate form: $ (infinity) / (infinity) $",
                "Apply L'Hôpital's Rule (1st application):",
                f"$ lim_(x -> infinity) ({2 * a} x {b_sign}) / ({2 * c} x) $",
                "Direct substitution still yields: $ (infinity) / (infinity) $",
                "Apply L'Hôpital's Rule a second time (2nd application):",
                f"$ lim_(x -> infinity) ({2 * a}) / ({2 * c}) = ({a}) / ({c}) = {ans_val} $",
                f"Result: {ans_typst}"
            ]

            d1 = f"$ {format_fraction_typst(c, a)} $"
            d2 = "$ infinity $"
            d3 = "$ 0 $"
            d4 = f"$ {a} $"

            distractors = ensure_distractors([d1, d2, d3, d4], ans_typst, ["$ 1 $", "$ text(\"Does not exist\") $", "$ 2 $"])

        return BaseProblem(
            id=f"calc_lhopital_spicy_{problem_idx}",
            prompt_text="Evaluate each indeterminate limit using L'Hôpital's Rule (multiple applications or infinity form).",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
