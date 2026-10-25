from __future__ import annotations

import math
import random
from typing import Dict

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


def _format_var_power(var: str, power: int) -> str:
    """Format variable and power in Typst: x, x^2, x^-3, etc."""
    if power == 0:
        return ""
    if power == 1:
        return var
    return f"{var}^{power}"


def _format_var_dict(var_powers: Dict[str, int]) -> str:
    """Format a dictionary of {var: power} into Typst space-separated variables."""
    parts = []
    for var, p in sorted(var_powers.items()):
        if p != 0:
            parts.append(_format_var_power(var, p))
    return " ".join(parts)


def _format_monomial(coeff: int, var_powers: Dict[str, int]) -> str:
    """Format a monomial term with coefficient and powers, e.g. 2x^3, -4x^-2 y^3, x^2, 12."""
    v_str = _format_var_dict(var_powers)
    if not v_str:
        return str(coeff)
    if coeff == 1:
        return v_str
    if coeff == -1:
        return f"-{v_str}"
    return f"{coeff}{v_str}"


def _format_positive_answer(num_coeff: int, den_coeff: int, powers: Dict[str, int]) -> str:
    """Format expression using strictly positive integer exponents in Typst syntax."""
    g = math.gcd(abs(num_coeff), abs(den_coeff))
    if g != 0:
        num_coeff //= g
        den_coeff //= g
    if den_coeff < 0:
        num_coeff = -num_coeff
        den_coeff = -den_coeff

    num_vars = {v: p for v, p in powers.items() if p > 0}
    den_vars = {v: abs(p) for v, p in powers.items() if p < 0}

    num_v_str = _format_var_dict(num_vars)
    den_v_str = _format_var_dict(den_vars)

    if num_v_str:
        if num_coeff == 1:
            top_str = num_v_str
        elif num_coeff == -1:
            top_str = f"-{num_v_str}"
        else:
            top_str = f"{num_coeff} {num_v_str}"
    else:
        top_str = str(num_coeff)

    if den_v_str:
        if den_coeff == 1:
            bot_str = den_v_str
        else:
            bot_str = f"{den_coeff} {den_v_str}"
    else:
        bot_str = str(den_coeff) if den_coeff != 1 else ""

    if not bot_str:
        return top_str
    return f"({top_str}) / ({bot_str})"


class ExponentRulesGenerator(BaseGenerator):
    generator_id = "algebra_1.exponent_rules"
    name = "Properties of Exponents"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.SSE.A.2", "CCSS.MATH.CONTENT.8.EE.A.1"]

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
        """Mild: Single-variable product and quotient rules with positive integer powers."""
        var = rng.choice(["x", "n", "m", "k", "a", "b", "p", "r", "v"])
        rule_type = rng.choice(["product_2", "product_3", "quotient"])

        if rule_type == "product_2":
            c1 = rng.choice([1, 2, 3, 4, 5])
            c2 = rng.choice([2, 3, 4, 5])
            p1 = rng.randint(1, 5)
            p2 = rng.randint(1, 5)

            t1 = _format_monomial(c1, {var: p1})
            t2 = _format_monomial(c2, {var: p2})
            eq_typst = f"{t1} dot {t2}"

            net_c = c1 * c2
            net_p = p1 + p2
            ans_typst = _format_positive_answer(net_c, 1, {var: net_p})

            steps = [
                "Apply the Product Rule for exponents: $ a^m dot a^n = a^(m + n) $",
                f"Group coefficients and powers: $ ({c1} dot {c2}) dot ({var}^{p1} dot {var}^{p2}) $",
                f"Multiply coefficients: $ {c1} dot {c2} = {net_c} $",
                f"Add exponents: $ {var}^({p1} + {p2}) = {var}^{net_p} $",
                f"Combined result: $ {ans_typst} $"
            ]

            distractors = [
                _format_positive_answer(net_c, 1, {var: p1 * p2}),  # Multiplied exponents
                _format_positive_answer(c1 + c2, 1, {var: net_p}),  # Added coefficients
                _format_positive_answer(net_c, 1, {var: net_p + 1}),  # Off-by-one exponent
                _format_positive_answer(c1 * c2, 1, {var: abs(p1 - p2) if abs(p1 - p2) > 0 else 1})
            ]

        elif rule_type == "product_3":
            c1 = rng.choice([1, 2, 3])
            c2 = rng.choice([1, 2, 3])
            c3 = rng.choice([2, 3, 4])
            p1 = rng.randint(1, 4)
            p2 = rng.randint(1, 4)
            p3 = rng.randint(1, 4)

            t1 = _format_monomial(c1, {var: p1})
            t2 = _format_monomial(c2, {var: p2})
            t3 = _format_monomial(c3, {var: p3})
            eq_typst = f"{t1} dot {t2} dot {t3}"

            net_c = c1 * c2 * c3
            net_p = p1 + p2 + p3
            ans_typst = _format_positive_answer(net_c, 1, {var: net_p})

            steps = [
                "Apply the Product Rule for exponents: $ a^m dot a^n dot a^p = a^(m + n + p) $",
                f"Multiply numerical coefficients: $ {c1} dot {c2} dot {c3} = {net_c} $",
                f"Add exponents of like bases: $ {var}^({p1} + {p2} + {p3}) = {var}^{net_p} $",
                f"Combined result: $ {ans_typst} $"
            ]

            distractors = [
                _format_positive_answer(net_c, 1, {var: p1 * p2 * p3}),
                _format_positive_answer(c1 + c2 + c3, 1, {var: net_p}),
                _format_positive_answer(net_c, 1, {var: net_p - 1})
            ]

        else:  # quotient
            c2 = rng.choice([1, 2, 3, 4])
            multiplier = rng.choice([1, 2, 3, 4, 5])
            c1 = c2 * multiplier
            p2 = rng.randint(1, 4)
            p1 = p2 + rng.randint(1, 4)  # ensure p1 > p2 for mild

            t1 = _format_monomial(c1, {var: p1})
            t2 = _format_monomial(c2, {var: p2})
            eq_typst = f"({t1}) / ({t2})"

            net_c = multiplier
            net_p = p1 - p2
            ans_typst = _format_positive_answer(net_c, 1, {var: net_p})

            steps = [
                "Apply the Quotient Rule for exponents: $ a^m / a^n = a^(m - n) $",
                f"Divide numerical coefficients: $ {c1} / {c2} = {net_c} $",
                f"Subtract exponents of matching bases: $ {var}^({p1} - {p2}) = {var}^{net_p} $",
                f"Combined result: $ {ans_typst} $"
            ]

            distractors = [
                _format_positive_answer(net_c, 1, {var: p1 + p2}),  # Added exponents instead of subtract
                _format_positive_answer(c1 - c2, 1, {var: net_p}) if c1 != c2 else _format_positive_answer(net_c + 1, 1, {var: net_p}),
                _format_positive_answer(net_c, 1, {var: p1 // p2 if p1 % p2 == 0 else net_p + 1}),
                _format_positive_answer(1, net_c, {var: net_p}) if net_c > 1 else _format_positive_answer(net_c, 1, {var: net_p + 2})
            ]

        valid_distractors = [d for d in dict.fromkeys(distractors) if d != ans_typst][:3]
        while len(valid_distractors) < 3:
            fake_p = (net_p + len(valid_distractors) + 1)
            candidate = _format_positive_answer(net_c, 1, {var: fake_p})
            if candidate not in valid_distractors and candidate != ans_typst:
                valid_distractors.append(candidate)

        return BaseProblem(
            id=f"alg1_exp_mild_{problem_idx}",
            prompt_text="Simplify. Your answer should contain only positive exponents.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=valid_distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Power of a power and negative exponents ((x^a)^b, x^-n = 1/x^n, (2x^3)^2)."""
        var = rng.choice(["x", "y", "m", "n", "k", "a", "b", "p"])
        sub_type = rng.choice(["power_of_power", "negative_product", "negative_quotient"])

        if sub_type == "power_of_power":
            coeff = rng.choice([2, 3, 4])
            power_in = rng.choice([-3, -2, -1, 2, 3, 4])
            power_out = rng.choice([-2, 2, 3])

            inner_monomial = _format_monomial(coeff, {var: power_in})
            eq_typst = f"({inner_monomial})^{power_out}"

            # Calculate mathematically
            # (c * var^p_in)^p_out = c^p_out * var^(p_in * p_out)
            net_power = power_in * power_out
            if power_out > 0:
                c_num = coeff ** power_out
                c_den = 1
            else:
                c_num = 1
                c_den = coeff ** abs(power_out)

            ans_typst = _format_positive_answer(c_num, c_den, {var: net_power})

            steps = [
                "Apply the Power of a Product Rule: $ (u dot v)^n = u^n dot v^n $",
                f"Distribute the outer exponent to the coefficient and the variable: $ ({coeff})^{power_out} dot ({var}^{power_in})^{power_out} $",
                f"Apply the Power of a Power Rule $ (a^m)^n = a^(m dot n) $: $ {var}^({power_in} dot {power_out}) = {var}^{net_power} $",
            ]
            if power_out > 0:
                steps.append(f"Evaluate coefficient: $ {coeff}^{power_out} = {c_num} $")
            else:
                steps.append(f"Evaluate coefficient using negative exponent rule: $ {coeff}^{power_out} = 1 / ({coeff}^{abs(power_out)}) = 1 / {c_den} $")

            if net_power < 0:
                steps.append(f"Rewrite variable using negative exponent rule $ a^(-n) = 1 / a^n $: $ {var}^{net_power} = 1 / ({var}^{abs(net_power)}) $")

            steps.append(f"Simplified positive-exponent result: $ {ans_typst} $")

            distractors = [
                # Multiplied base by outer exponent instead of exponentiating
                _format_positive_answer(coeff * power_out if power_out > 0 else 1, abs(coeff * power_out) if power_out < 0 else 1, {var: net_power}),
                # Added exponents in power of a power
                _format_positive_answer(c_num, c_den, {var: power_in + power_out}),
                # Forgetting to invert negative exponent
                f"{c_num if c_den == 1 else f'1/{c_den}'} {var}^{net_power}" if net_power < 0 else _format_positive_answer(c_num, c_den, {var: -net_power}),
                # Inverted power
                _format_positive_answer(c_num, c_den, {var: -net_power})
            ]

        elif sub_type == "negative_product":
            c1 = rng.choice([2, 3, 4, 5])
            c2 = rng.choice([2, 3, 4])
            p1 = rng.choice([-5, -4, -3, -2, -1])
            p2 = rng.choice([1, 2, 3, 4, 5, -2, -3])

            t1 = _format_monomial(c1, {var: p1})
            t2 = _format_monomial(c2, {var: p2})
            eq_typst = f"{t1} dot {t2}"

            net_c = c1 * c2
            net_p = p1 + p2
            ans_typst = _format_positive_answer(net_c, 1, {var: net_p})

            steps = [
                "Apply the Product Rule for exponents: $ a^m dot a^n = a^(m + n) $",
                f"Multiply coefficients: $ {c1} dot {c2} = {net_c} $",
                f"Add exponents: $ {var}^({p1} + ({p2})) = {var}^{net_p} $",
            ]
            if net_p < 0:
                steps.append(f"Apply negative exponent rule $ a^(-n) = 1 / a^n $: $ {var}^{net_p} = 1 / {var}^{abs(net_p)} $")
            steps.append(f"Final simplified answer: $ {ans_typst} $")

            distractors = [
                _format_positive_answer(net_c, 1, {var: -net_p}),  # Opposite sign
                _format_positive_answer(c1 + c2, 1, {var: net_p}),  # Added coefficients
                _format_positive_answer(net_c, 1, {var: p1 * p2}),  # Multiplied exponents
                _format_positive_answer(1, net_c, {var: net_p})
            ]

        else:  # negative_quotient
            c_div = rng.choice([2, 3, 4])
            c2 = rng.choice([2, 3, 4])
            c1 = c2 * c_div
            p1 = rng.choice([-4, -3, -2, 2, 3])
            p2 = rng.choice([-3, -2, 2, 3, 4])
            while p1 == p2:
                p2 = rng.choice([-3, -2, 2, 3, 4])

            t1 = _format_monomial(c1, {var: p1})
            t2 = _format_monomial(c2, {var: p2})
            eq_typst = f"({t1}) / ({t2})"

            net_p = p1 - p2
            ans_typst = _format_positive_answer(c_div, 1, {var: net_p})

            steps = [
                "Apply the Quotient Rule for exponents: $ a^m / a^n = a^(m - n) $",
                f"Divide coefficients: $ {c1} / {c2} = {c_div} $",
                f"Subtract denominator exponent from numerator: $ {var}^({p1} - ({p2})) = {var}^{net_p} $",
            ]
            if net_p < 0:
                steps.append(f"Apply negative exponent rule $ a^(-n) = 1 / a^n $: $ {var}^{net_p} = 1 / {var}^{abs(net_p)} $")
            steps.append(f"Final simplified answer: $ {ans_typst} $")

            distractors = [
                _format_positive_answer(c_div, 1, {var: p1 + p2}),  # Added exponents
                _format_positive_answer(c_div, 1, {var: -net_p}),  # Opposite sign
                _format_positive_answer(1, c_div, {var: net_p}),  # Inverted coefficient
                _format_positive_answer(c_div, 1, {var: p2 - p1})  # Subtracted wrong direction
            ]

        valid_distractors = [d for d in dict.fromkeys(distractors) if d != ans_typst][:3]
        while len(valid_distractors) < 3:
            offset = len(valid_distractors) + 1
            candidate = _format_positive_answer(2, 1, {var: offset})
            if candidate not in valid_distractors and candidate != ans_typst:
                valid_distractors.append(candidate)

        return BaseProblem(
            id=f"alg1_exp_med_{problem_idx}",
            prompt_text="Simplify. Your answer should contain only positive exponents.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=valid_distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Multi-variable rational expressions with negative exponents needing full simplification."""
        var_pairs = [("x", "y"), ("a", "b"), ("u", "v"), ("m", "n")]
        v1, v2 = rng.choice(var_pairs)

        sub_type = rng.choice(["rational_multivar", "power_of_quotient"])

        if sub_type == "rational_multivar":
            c_factor = rng.choice([2, 3, 4, 6])
            c2 = rng.choice([2, 3, 4])
            c1 = c2 * c_factor

            # Choose powers with at least 2 negative exponents
            p1 = rng.choice([-4, -3, -2, 2, 3])
            p2 = rng.choice([-3, -2, 1, 2, 4])
            q1 = rng.choice([-3, -2, 2, 3, 4])
            q2 = rng.choice([-4, -3, -1, 1, 2])

            # Ensure some negative exponents are present
            negs = [val for val in [p1, p2, q1, q2] if val < 0]
            if len(negs) < 2:
                p1 = -abs(p1) if p1 > 0 else p1
                q2 = -abs(q2) if q2 > 0 else q2

            top_str = _format_monomial(c1, {v1: p1, v2: q1})
            bot_str = _format_monomial(c2, {v1: p2, v2: q2})
            eq_typst = f"({top_str}) / ({bot_str})"

            net_p = p1 - p2
            net_q = q1 - q2
            ans_typst = _format_positive_answer(c_factor, 1, {v1: net_p, v2: net_q})

            steps = [
                f"Simplify numerical coefficients: $ {c1} / {c2} = {c_factor} $",
                f"Apply Quotient Rule for base ${v1}$: $ {v1}^({p1} - ({p2})) = {v1}^{net_p} $",
                f"Apply Quotient Rule for base ${v2}$: $ {v2}^({q1} - ({q2})) = {v2}^{net_q} $",
                "Rewrite all factors using positive exponents only ($ u^(-n) = 1 / u^n $):",
                f"Final simplified expression: $ {ans_typst} $"
            ]

            distractors = [
                _format_positive_answer(c_factor, 1, {v1: p1 + p2, v2: net_q}),  # Added powers for v1
                _format_positive_answer(c_factor, 1, {v1: net_p, v2: q1 + q2}),  # Added powers for v2
                _format_positive_answer(1, c_factor, {v1: net_p, v2: net_q}),  # Inverted coefficient
                _format_positive_answer(c_factor, 1, {v1: -net_p, v2: net_q}),  # Sign flip v1
                _format_positive_answer(c_factor, 1, {v1: net_p, v2: -net_q})   # Sign flip v2
            ]

        else:  # power_of_quotient: ((c1 a^p1 b^q1) / (c2 a^p2 b^q2))^k
            c1 = rng.choice([2, 3, 4])
            c2 = rng.choice([1, 2])
            if c1 == c2:
                c1 = 3
                c2 = 1

            p1 = rng.choice([-3, -2, 1, 2])
            p2 = rng.choice([-2, -1, 1, 2])
            q1 = rng.choice([-3, -2, 2, 3])
            q2 = rng.choice([-2, 1, 2])
            k = rng.choice([2, 3, -2])

            inner_top = _format_monomial(c1, {v1: p1, v2: q1})
            inner_bot = _format_monomial(c2, {v1: p2, v2: q2})
            eq_typst = f"(({inner_top}) / ({inner_bot}))^{k}"

            # Step 1: inside simplification
            g_in = math.gcd(c1, c2)
            c_in_n = c1 // g_in
            c_in_d = c2 // g_in
            net_p_in = p1 - p2
            net_q_in = q1 - q2

            # Step 2: outer exponent k
            if k > 0:
                c_out_n = c_in_n ** k
                c_out_d = c_in_d ** k
            else:
                c_out_n = c_in_d ** abs(k)
                c_out_d = c_in_n ** abs(k)

            net_p_out = net_p_in * k
            net_q_out = net_q_in * k

            ans_typst = _format_positive_answer(c_out_n, c_out_d, {v1: net_p_out, v2: net_q_out})

            inside_simplified = _format_positive_answer(c_in_n, c_in_d, {v1: net_p_in, v2: net_q_in})

            steps = [
                "Step 1: Simplify the expression inside parentheses first:",
                f"  - Coefficients: $ {c1} / {c2} = {c_in_n} / {c_in_d} $",
                f"  - Base ${v1}$: $ {v1}^({p1} - ({p2})) = {v1}^{net_p_in} $",
                f"  - Base ${v2}$: $ {v2}^({q1} - ({q2})) = {v2}^{net_q_in} $",
                f"  - Inside expression: $ {inside_simplified} $",
                f"Step 2: Apply the outer exponent ${k}$ to all factors:",
                f"  - Coefficient: $ ({c_in_n} / {c_in_d})^{k} = {c_out_n} / {c_out_d} $",
                f"  - Powers: $ ({v1}^{net_p_in})^{k} = {v1}^{net_p_out} $, $ ({v2}^{net_q_in})^{k} = {v2}^{net_q_out} $",
                "Step 3: Convert all variables to positive exponents:",
                f"Final answer: $ {ans_typst} $"
            ]

            distractors = [
                # Forgot to raise coefficient to power k
                _format_positive_answer(c_in_n, c_in_d, {v1: net_p_out, v2: net_q_out}),
                # Added outer power instead of multiplying
                _format_positive_answer(c_out_n, c_out_d, {v1: net_p_in + k, v2: net_q_in + k}),
                # Sign flip on powers
                _format_positive_answer(c_out_n, c_out_d, {v1: -net_p_out, v2: net_q_out}),
                _format_positive_answer(c_out_d, c_out_n, {v1: net_p_out, v2: net_q_out})  # Flipped fraction
            ]

        valid_distractors = [d for d in dict.fromkeys(distractors) if d != ans_typst][:3]
        while len(valid_distractors) < 3:
            offset = len(valid_distractors) + 1
            candidate = _format_positive_answer(1, 1, {v1: offset, v2: offset + 1})
            if candidate not in valid_distractors and candidate != ans_typst:
                valid_distractors.append(candidate)

        return BaseProblem(
            id=f"alg1_exp_spicy_{problem_idx}",
            prompt_text="Simplify. Your answer should contain only positive exponents.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=valid_distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
