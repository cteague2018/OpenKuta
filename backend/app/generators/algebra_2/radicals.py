from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


def simplify_radical(n: int) -> tuple[int, int]:
    k = 1
    p = n
    d = 2
    while d * d <= p:
        while p % (d * d) == 0:
            k *= d
            p //= (d * d)
        d += 1
    return k, p


class Algebra2RadicalsGenerator(BaseGenerator):
    generator_id = "algebra_2.radicals"
    name = "Radicals & Rational Exponents"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSN.RN.A.2", "CCSS.MATH.CONTENT.HSA.REI.A.2"]

    @verify_mathematical_truth()
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
        """Mild: Simplifying single radicals sqrt(k^2 * p) with perfect square factoring."""
        k = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        p = rng.choice([2, 3, 5, 6, 7, 10, 11])
        num = (k * k) * p

        eq_typst = f"sqrt({num})"
        ans_typst = f"{k} sqrt({p})"

        steps = [
            f"Find the largest perfect square factor of {num}: $ {k*k} dot {p} = {num} $",
            f"Rewrite using product property of square roots: $ sqrt({k*k}) dot sqrt({p}) $",
            f"Evaluate the square root of the perfect square: $ sqrt({k*k}) = {k} $",
            f"Result: $ {ans_typst} $"
        ]

        distractors = [
            f"{k*k} sqrt({p})",
            f"{p} sqrt({k})",
            f"{k + p}"
        ]

        return BaseProblem(
            id=f"a2_rad_mild_{problem_idx}",
            prompt_text="Simplify each radical expression completely.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Operations with radicals (multiplying/adding like radicals) or rational exponents."""
        subtype = rng.choice(["rational_exponent", "operations"])

        if subtype == "rational_exponent":
            # N^(m/n)
            cases = [
                (27, 2, 3, 3, 9),
                (8, 2, 3, 2, 4),
                (8, 4, 3, 2, 16),
                (16, 3, 4, 2, 8),
                (16, 5, 4, 2, 32),
                (32, 2, 5, 2, 4),
                (32, 3, 5, 2, 8),
                (64, 2, 3, 4, 16),
                (25, 3, 2, 5, 125),
                (49, 3, 2, 7, 343),
                (81, 3, 4, 3, 27),
            ]
            N, m, n, base, val = rng.choice(cases)
            is_neg = rng.choice([True, False])

            if is_neg:
                eq_typst = f"{N}^(-{m}/{n})"
                ans_typst = f"1/{val}"
                steps = [
                    f"Rewrite negative exponent as reciprocal: $ {N}^(-{m}/{n}) = 1 / ({N}^({m}/{n})) $",
                    f"Express rational exponent in radical form: $ {N}^({m}/{n}) = (root({n}, {N}))^({m}) $",
                    f"Evaluate the {n}th root: $ root({n}, {N}) = {base} $",
                    f"Raise to power {m}: $ ({base})^({m}) = {val} $",
                    f"Combine with reciprocal: $ {ans_typst} $"
                ]
                distractors = [
                    f"-{val}",
                    f"1/{val * base}",
                    f"{val}"
                ]
            else:
                eq_typst = f"{N}^({m}/{n})"
                ans_typst = f"{val}"
                steps = [
                    f"Express rational exponent using radical notation: $ {N}^({m}/{n}) = (root({n}, {N}))^({m}) $",
                    f"Evaluate the {n}th root: $ root({n}, {N}) = {base} $",
                    f"Raise to power {m}: $ ({base})^({m}) = {val} $",
                    f"Result: $ {ans_typst} $"
                ]
                distractors = [
                    f"{val + base}",
                    f"{val * 2}",
                    f"{N // n}"
                ]

            prompt = "Evaluate each expression with rational exponents."
        else:
            # Radical addition: c1 * sqrt(k1^2 * p) + c2 * sqrt(k2^2 * p)
            p = rng.choice([2, 3, 5])
            k1 = rng.choice([2, 3, 4])
            k2 = rng.choice([2, 3, 5])
            if k1 == k2:
                k2 += 1
            c1 = rng.choice([2, 3, 4])
            c2 = rng.choice([2, 3, 5])

            s1 = (k1 * k1) * p
            s2 = (k2 * k2) * p
            tot_k = c1 * k1 + c2 * k2

            eq_typst = f"{c1} sqrt({s1}) + {c2} sqrt({s2})"
            ans_typst = f"{tot_k} sqrt({p})"

            steps = [
                f"Simplify first radical: $ {c1} sqrt({s1}) = {c1} dot sqrt({k1*k1} dot {p}) = {c1} dot {k1} sqrt({p}) = {c1*k1} sqrt({p}) $",
                f"Simplify second radical: $ {c2} sqrt({s2}) = {c2} dot sqrt({k2*k2} dot {p}) = {c2} dot {k2} sqrt({p}) = {c2*k2} sqrt({p}) $",
                f"Combine like radical terms: $ {c1*k1} sqrt({p}) + {c2*k2} sqrt({p}) = ({c1*k1} + {c2*k2}) sqrt({p}) $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"{c1 + c2} sqrt({s1 + s2})",
                f"{tot_k + 2} sqrt({p})",
                f"{c1*k1 * c2*k2} sqrt({p})"
            ]

            prompt = "Simplify each radical expression completely."

        return BaseProblem(
            id=f"a2_rad_med_{problem_idx}",
            prompt_text=prompt,
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Solving radical equations sqrt(ax + b) = c with check for extraneous solutions."""
        cases = [
            {
                "eq": "sqrt(2 x + 15) = x",
                "a": 2, "b": 15, "rhs": "x",
                "quad": "x^2 - 2 x - 15 = 0",
                "factored": "(x - 5)(x + 3) = 0",
                "candidates": [5, -3],
                "valid": [5],
                "extraneous": [-3],
                "steps": [
                    "Square both sides to eliminate the radical: $ (sqrt(2 x + 15))^2 = (x)^2 ==> 2 x + 15 = x^2 $",
                    "Rearrange into standard quadratic form: $ x^2 - 2 x - 15 = 0 $",
                    "Factor the quadratic: $ (x - 5)(x + 3) = 0 ==> x = 5 \" or \" x = -3 $",
                    "Check candidate $x = 5$: $ sqrt(2(5) + 15) = sqrt(25) = 5 = 5 $ (Valid)",
                    "Check candidate $x = -3$: $ sqrt(2(-3) + 15) = sqrt(9) = 3 != -3 $ (Extraneous)",
                    "Final solution: $ x = 5 $"
                ],
                "ans": "x = 5",
                "distractors": ["x = 5, -3", "x = -3", "x = 25"]
            },
            {
                "eq": "sqrt(3 x + 18) = x",
                "a": 3, "b": 18, "rhs": "x",
                "quad": "x^2 - 3 x - 18 = 0",
                "factored": "(x - 6)(x + 3) = 0",
                "candidates": [6, -3],
                "valid": [6],
                "extraneous": [-3],
                "steps": [
                    "Square both sides: $ 3 x + 18 = x^2 $",
                    "Rearrange: $ x^2 - 3 x - 18 = 0 $",
                    "Factor: $ (x - 6)(x + 3) = 0 ==> x = 6 \" or \" x = -3 $",
                    "Check $x = 6$: $ sqrt(3(6) + 18) = sqrt(36) = 6 = 6 $ (Valid)",
                    "Check $x = -3$: $ sqrt(3(-3) + 18) = sqrt(9) = 3 != -3 $ (Extraneous)",
                    "Final solution: $ x = 6 $"
                ],
                "ans": "x = 6",
                "distractors": ["x = 6, -3", "x = -3", "x = 9"]
            },
            {
                "eq": "sqrt(4 x + 21) = x",
                "a": 4, "b": 21, "rhs": "x",
                "quad": "x^2 - 4 x - 21 = 0",
                "factored": "(x - 7)(x + 3) = 0",
                "candidates": [7, -3],
                "valid": [7],
                "extraneous": [-3],
                "steps": [
                    "Square both sides: $ 4 x + 21 = x^2 $",
                    "Rearrange: $ x^2 - 4 x - 21 = 0 $",
                    "Factor: $ (x - 7)(x + 3) = 0 ==> x = 7 \" or \" x = -3 $",
                    "Check $x = 7$: $ sqrt(4(7) + 21) = sqrt(49) = 7 = 7 $ (Valid)",
                    "Check $x = -3$: $ sqrt(4(-3) + 21) = sqrt(9) = 3 != -3 $ (Extraneous)",
                    "Final solution: $ x = 7 $"
                ],
                "ans": "x = 7",
                "distractors": ["x = 7, -3", "x = -3", "x = 21/4"]
            },
            {
                "eq": "sqrt(10 - 3 x) = x",
                "a": -3, "b": 10, "rhs": "x",
                "quad": "x^2 + 3 x - 10 = 0",
                "factored": "(x + 5)(x - 2) = 0",
                "candidates": [2, -5],
                "valid": [2],
                "extraneous": [-5],
                "steps": [
                    "Square both sides: $ 10 - 3 x = x^2 $",
                    "Rearrange: $ x^2 + 3 x - 10 = 0 $",
                    "Factor: $ (x + 5)(x - 2) = 0 ==> x = 2 \" or \" x = -5 $",
                    "Check $x = 2$: $ sqrt(10 - 3(2)) = sqrt(4) = 2 = 2 $ (Valid)",
                    "Check $x = -5$: $ sqrt(10 - 3(-5)) = sqrt(25) = 5 != -5 $ (Extraneous)",
                    "Final solution: $ x = 2 $"
                ],
                "ans": "x = 2",
                "distractors": ["x = 2, -5", "x = -5", "x = 10/3"]
            },
            {
                "eq": "sqrt(2 x + 3) = x",
                "a": 2, "b": 3, "rhs": "x",
                "quad": "x^2 - 2 x - 3 = 0",
                "factored": "(x - 3)(x + 1) = 0",
                "candidates": [3, -1],
                "valid": [3],
                "extraneous": [-1],
                "steps": [
                    "Square both sides: $ 2 x + 3 = x^2 $",
                    "Rearrange: $ x^2 - 2 x - 3 = 0 $",
                    "Factor: $ (x - 3)(x + 1) = 0 ==> x = 3 \" or \" x = -1 $",
                    "Check $x = 3$: $ sqrt(2(3) + 3) = sqrt(9) = 3 = 3 $ (Valid)",
                    "Check $x = -1$: $ sqrt(2(-1) + 3) = sqrt(1) = 1 != -1 $ (Extraneous)",
                    "Final solution: $ x = 3 $"
                ],
                "ans": "x = 3",
                "distractors": ["x = 3, -1", "x = -1", "x = 9"]
            },
            {
                "eq": "sqrt(5 x - 6) = x",
                "a": 5, "b": -6, "rhs": "x",
                "quad": "x^2 - 5 x + 6 = 0",
                "factored": "(x - 2)(x - 3) = 0",
                "candidates": [2, 3],
                "valid": [2, 3],
                "extraneous": [],
                "steps": [
                    "Square both sides: $ 5 x - 6 = x^2 $",
                    "Rearrange: $ x^2 - 5 x + 6 = 0 $",
                    "Factor: $ (x - 2)(x - 3) = 0 ==> x = 2 \" or \" x = 3 $",
                    "Check $x = 2$: $ sqrt(5(2) - 6) = sqrt(4) = 2 = 2 $ (Valid)",
                    "Check $x = 3$: $ sqrt(5(3) - 6) = sqrt(9) = 3 = 3 $ (Valid)",
                    "Both solutions are valid: $ x = 2, 3 $"
                ],
                "ans": "x = 2, 3",
                "distractors": ["x = 2", "x = 3", "x = 6/5"]
            }
        ]

        c = rng.choice(cases)
        steps_raw = c["steps"]
        steps_val = [str(s) for s in steps_raw] if isinstance(steps_raw, list) else [str(steps_raw)]
        dist_raw = c["distractors"]
        dist_val = [str(d) for d in dist_raw] if isinstance(dist_raw, list) else [str(dist_raw)]
        return BaseProblem(
            id=f"a2_rad_spicy_{problem_idx}",
            prompt_text="Solve each radical equation. Remember to check for extraneous solutions.",
            equation_typst=str(c["eq"]),
            answer_typst=str(c["ans"]),
            steps_typst=steps_val,
            distractors=dist_val,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
