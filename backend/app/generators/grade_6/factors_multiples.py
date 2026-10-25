from __future__ import annotations

import math
import random
from typing import Dict

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


def _prime_factors(n: int) -> Dict[int, int]:
    factors: Dict[int, int] = {}
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    return factors


def _format_factorization(factors: Dict[int, int]) -> str:
    if not factors:
        return "1"
    parts = []
    for p in sorted(factors.keys()):
        exp = factors[p]
        if exp == 1:
            parts.append(f"{p}")
        else:
            parts.append(f"{p}^{exp}")
    return " dot ".join(parts)


class Grade6FactorsMultiplesGenerator(BaseGenerator):
    generator_id = "grade_6.factors_multiples"
    name = "Greatest Common Factor & Least Common Multiple"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.NS.B.4"]

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
        """Mild: GCF and LCM of 2 small numbers (under 50) with full prime factorizations."""
        pairs = [
            (12, 18), (16, 24), (20, 30), (18, 27), (24, 36),
            (15, 25), (14, 21), (12, 20), (28, 42), (30, 45), (16, 32), (18, 24)
        ]
        n1, n2 = rng.choice(pairs)
        is_gcf = rng.choice([True, False])

        f1 = _prime_factors(n1)
        f2 = _prime_factors(n2)
        f1_str = _format_factorization(f1)
        f2_str = _format_factorization(f2)

        if is_gcf:
            ans = math.gcd(n1, n2)
            common_primes: Dict[int, int] = {}
            for p in f1:
                if p in f2:
                    common_primes[p] = min(f1[p], f2[p])
            common_str = _format_factorization(common_primes)

            eq_typst = f"\"GCF of \" {n1} \" and \" {n2}"
            ans_typst = f"\"GCF\"({n1}, {n2}) = {ans}"

            steps = [
                "Find the prime factorization of each number:",
                f"$ {n1} = {f1_str} $",
                f"$ {n2} = {f2_str} $",
                f"Identify common prime factors with their lowest powers: $ {common_str} $",
                f"Multiply common prime factors: $ {ans} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Find the greatest common factor (GCF) of each pair of numbers."
            d1 = f"\"GCF\"({n1}, {n2}) = {ans * 2}"
            d2 = f"\"GCF\"({n1}, {n2}) = {max(1, ans // 2)}"
            d3 = f"\"GCF\"({n1}, {n2}) = {ans + 2}"
        else:
            ans = (n1 * n2) // math.gcd(n1, n2)
            all_primes: Dict[int, int] = {}
            for p in set(f1.keys()).union(f2.keys()):
                all_primes[p] = max(f1.get(p, 0), f2.get(p, 0))
            lcm_factors_str = _format_factorization(all_primes)

            eq_typst = f"\"LCM of \" {n1} \" and \" {n2}"
            ans_typst = f"\"LCM\"({n1}, {n2}) = {ans}"

            steps = [
                "Find the prime factorization of each number:",
                f"$ {n1} = {f1_str} $",
                f"$ {n2} = {f2_str} $",
                f"Take the highest power of each prime factor appearing in either factorization: $ {lcm_factors_str} $",
                f"Multiply the factors: $ {ans} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Find the least common multiple (LCM) of each pair of numbers."
            d1 = f"\"LCM\"({n1}, {n2}) = {ans * 2}"
            d2 = f"\"LCM\"({n1}, {n2}) = {ans // 2}"
            d3 = f"\"LCM\"({n1}, {n2}) = {n1 * n2}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"Answer = {ans + 3}")

        return BaseProblem(
            id=f"g6_fac_mild_{problem_idx}",
            prompt_text=prompt,
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"n1": n1, "n2": n2, "is_gcf": is_gcf, "answer": ans}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: GCF and LCM of 2 larger numbers (up to 120) with full prime factorizations."""
        pairs = [
            (48, 72), (54, 90), (60, 84), (56, 84), (72, 108),
            (64, 96), (75, 100), (80, 120), (45, 105), (63, 105), (84, 112)
        ]
        n1, n2 = rng.choice(pairs)
        is_gcf = rng.choice([True, False])

        f1 = _prime_factors(n1)
        f2 = _prime_factors(n2)
        f1_str = _format_factorization(f1)
        f2_str = _format_factorization(f2)

        if is_gcf:
            ans = math.gcd(n1, n2)
            common_primes: Dict[int, int] = {}
            for p in f1:
                if p in f2:
                    common_primes[p] = min(f1[p], f2[p])
            common_str = _format_factorization(common_primes)

            eq_typst = f"\"GCF of \" {n1} \" and \" {n2}"
            ans_typst = f"\"GCF\"({n1}, {n2}) = {ans}"

            steps = [
                "Find the prime factorization of each number:",
                f"$ {n1} = {f1_str} $",
                f"$ {n2} = {f2_str} $",
                f"Identify the common prime factors: $ {common_str} $",
                f"Multiply common prime factors: $ {ans} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Find the greatest common factor (GCF) of the numbers."
            d1 = f"\"GCF\"({n1}, {n2}) = {ans * 2}"
            d2 = f"\"GCF\"({n1}, {n2}) = {ans // 2}"
            d3 = f"\"GCF\"({n1}, {n2}) = {ans + 4}"
        else:
            ans = (n1 * n2) // math.gcd(n1, n2)
            all_primes: Dict[int, int] = {}
            for p in set(f1.keys()).union(f2.keys()):
                all_primes[p] = max(f1.get(p, 0), f2.get(p, 0))
            lcm_factors_str = _format_factorization(all_primes)

            eq_typst = f"\"LCM of \" {n1} \" and \" {n2}"
            ans_typst = f"\"LCM\"({n1}, {n2}) = {ans}"

            steps = [
                "Find the prime factorization of each number:",
                f"$ {n1} = {f1_str} $",
                f"$ {n2} = {f2_str} $",
                f"Take the highest power of each prime factor: $ {lcm_factors_str} $",
                f"Multiply: $ {ans} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Find the least common multiple (LCM) of the numbers."
            d1 = f"\"LCM\"({n1}, {n2}) = {ans * 2}"
            d2 = f"\"LCM\"({n1}, {n2}) = {ans // 2}"
            d3 = f"\"LCM\"({n1}, {n2}) = {ans + 24}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"Answer = {ans + 6}")

        return BaseProblem(
            id=f"g6_fac_med_{problem_idx}",
            prompt_text=prompt,
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"n1": n1, "n2": n2, "is_gcf": is_gcf, "answer": ans}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: GCF and LCM of 3 numbers (e.g. 12, 18, 30) with full prime factorizations."""
        triples = [
            (12, 18, 30), (16, 24, 36), (18, 24, 48), (12, 20, 28),
            (15, 20, 30), (20, 30, 50), (24, 36, 60), (14, 28, 42), (18, 27, 45)
        ]
        n1, n2, n3 = rng.choice(triples)
        is_gcf = rng.choice([True, False])

        f1 = _prime_factors(n1)
        f2 = _prime_factors(n2)
        f3 = _prime_factors(n3)
        f1_str = _format_factorization(f1)
        f2_str = _format_factorization(f2)
        f3_str = _format_factorization(f3)

        if is_gcf:
            ans = math.gcd(math.gcd(n1, n2), n3)
            common_primes: Dict[int, int] = {}
            for p in f1:
                if p in f2 and p in f3:
                    common_primes[p] = min(f1[p], f2[p], f3[p])
            common_str = _format_factorization(common_primes) if common_primes else "1"

            eq_typst = f"\"GCF of \" {n1}, {n2}, \" and \" {n3}"
            ans_typst = f"\"GCF\"({n1}, {n2}, {n3}) = {ans}"

            steps = [
                "Find the prime factorizations of all three numbers:",
                f"$ {n1} = {f1_str} $",
                f"$ {n2} = {f2_str} $",
                f"$ {n3} = {f3_str} $",
                f"Identify the prime factors shared by all three numbers with their lowest powers: $ {common_str} $",
                f"Multiply: $ {ans} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Find the greatest common factor (GCF) of the three numbers."
            d1 = f"\"GCF\"({n1}, {n2}, {n3}) = {ans * 2}"
            d2 = f"\"GCF\"({n1}, {n2}, {n3}) = {max(1, ans // 2)}"
            d3 = f"\"GCF\"({n1}, {n2}, {n3}) = {math.gcd(n1, n2)}"
        else:
            # LCM of 3 numbers
            lcm_12 = (n1 * n2) // math.gcd(n1, n2)
            ans = (lcm_12 * n3) // math.gcd(lcm_12, n3)

            all_primes: Dict[int, int] = {}
            for p in set(f1.keys()).union(f2.keys()).union(f3.keys()):
                all_primes[p] = max(f1.get(p, 0), f2.get(p, 0), f3.get(p, 0))
            lcm_factors_str = _format_factorization(all_primes)

            eq_typst = f"\"LCM of \" {n1}, {n2}, \" and \" {n3}"
            ans_typst = f"\"LCM\"({n1}, {n2}, {n3}) = {ans}"

            steps = [
                "Find the prime factorizations of all three numbers:",
                f"$ {n1} = {f1_str} $",
                f"$ {n2} = {f2_str} $",
                f"$ {n3} = {f3_str} $",
                f"Take the highest power of each prime factor appearing in any factorization: $ {lcm_factors_str} $",
                f"Multiply to obtain LCM: $ {ans} $",
                f"Result: $ {ans_typst} $"
            ]

            prompt = "Find the least common multiple (LCM) of the three numbers."
            d1 = f"\"LCM\"({n1}, {n2}, {n3}) = {ans * 2}"
            d2 = f"\"LCM\"({n1}, {n2}, {n3}) = {ans // 2}"
            d3 = f"\"LCM\"({n1}, {n2}, {n3}) = {lcm_12}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"Answer = {ans + 12}")

        return BaseProblem(
            id=f"g6_fac_spicy_{problem_idx}",
            prompt_text=prompt,
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"n1": n1, "n2": n2, "n3": n3, "is_gcf": is_gcf, "answer": ans}
        )
