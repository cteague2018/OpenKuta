from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class PrecalcSequencesGenerator(BaseGenerator):
    generator_id = "precalculus.sequences"
    name = "Sequences and Series"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSF.BF.A.2"]

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
        """Mild: Arithmetic sequences: find nth term a_n = a_1 + (n-1)d."""
        a1 = rng.choice([-15, -12, -8, -5, 2, 3, 5, 7, 9, 12, 16])
        d = rng.choice([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8])
        n = rng.choice([10, 12, 14, 15, 18, 20, 22, 25])

        an = a1 + (n - 1) * d
        t1, t2, t3, t4 = a1, a1 + d, a1 + 2 * d, a1 + 3 * d

        eq_typst = f"{t1}, {t2}, {t3}, {t4}, ...; quad a_{n} = ?"
        ans_typst = f"a_{n} = {an}"

        steps = [
            f"Identify first term: $ a_1 = {a1} $",
            f"Find common difference: $ d = {t2} - ({t1}) = {d} $",
            "Recall arithmetic sequence formula: $ a_n = a_1 + (n - 1) d $",
            f"Substitute $n = {n}$: $ a_{n} = {a1} + ({n} - 1)({d}) $",
            f"Compute: $ a_{n} = {a1} + ({(n - 1) * d}) = {an} $",
            f"Result: $ {ans_typst} $"
        ]

        distractors = [
            f"a_{n} = {an + d}",
            f"a_{n} = {an - d}",
            f"a_{n} = {a1 + n * d}"
        ]

        return BaseProblem(
            id=f"pcalc_seq_mild_{problem_idx}",
            prompt_text="Find the specified term in each arithmetic sequence.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Geometric sequences: find nth term a_n = a_1 * r^(n-1)."""
        a1 = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        r = rng.choice([-3, -2, 2, 3])
        n = rng.choice([5, 6, 7, 8])

        an = a1 * (r ** (n - 1))
        t1, t2, t3 = a1, a1 * r, a1 * (r ** 2)

        eq_typst = f"{t1}, {t2}, {t3}, ...; quad a_{n} = ?"
        ans_typst = f"a_{n} = {an}"

        steps = [
            f"Identify first term: $ a_1 = {a1} $",
            f"Find common ratio: $ r = ({t2}) / ({t1}) = {r} $",
            "Recall geometric sequence formula: $ a_n = a_1 dot r^(n - 1) $",
            f"Substitute $n = {n}$: $ a_{n} = ({a1}) dot ({r})^({n} - 1) = ({a1}) dot ({r}^({n - 1})) $",
            f"Evaluate power: $ ({r})^({n - 1}) = {r ** (n - 1)} $",
            f"Multiply: $ a_{n} = ({a1}) dot ({r ** (n - 1)}) = {an} $"
        ]

        distractors = [
            f"a_{n} = {an * r}",
            f"a_{n} = {-an}",
            f"a_{n} = {a1 * (r ** n)}"
        ]

        return BaseProblem(
            id=f"pcalc_seq_med_{problem_idx}",
            prompt_text="Find the specified term in each geometric sequence.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Arithmetic and Geometric series partial sums: S_n = n/2 (a_1 + a_n) and S_n = a_1(1 - r^n)/(1 - r)."""
        series_type = rng.choice(["arithmetic", "geometric"])

        if series_type == "arithmetic":
            a1 = rng.choice([-8, -5, -2, 3, 4, 6, 8, 10])
            d = rng.choice([-4, -3, 2, 3, 4, 5])
            n = rng.choice([10, 12, 14, 16, 20])

            an = a1 + (n - 1) * d
            sn = n * (a1 + an) // 2

            t1, t2, t3 = a1, a1 + d, a1 + 2 * d
            eq_typst = f"{t1} + {t2} + {t3} + ... + a_{n}, quad \"where \" a_{n} = {an}"
            ans_typst = f"S_{n} = {sn}"

            steps = [
                f"Identify arithmetic series parameters: first term $a_1 = {a1}$, last term $a_{n} = {an}$, $n = {n}$",
                "Recall arithmetic series partial sum formula: $ S_n = n/2 (a_1 + a_n) $",
                f"Substitute values: $ S_{n} = ({n}/2) [({a1}) + ({an})] $",
                f"Compute sum inside brackets: $ ({a1}) + ({an}) = {a1 + an} $",
                f"Multiply: $ S_{n} = {n // 2 if n % 2 == 0 else f'{n}/2'} dot ({a1 + an}) = {sn} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"S_{n} = {sn + an}",
                f"S_{n} = {sn - a1}",
                f"S_{n} = {n * an}"
            ]

            prompt = "Find the sum of each arithmetic series."
        else:
            # Geometric Series: S_n = a1(1 - r^n)/(1 - r)
            a1 = rng.choice([2, 3, 4, 5, -2, -3])
            r = rng.choice([-2, 2, 3])
            n = rng.choice([5, 6, 7])

            r_pow_n = r ** n
            sn = a1 * (1 - r_pow_n) // (1 - r)

            t1, t2, t3 = a1, a1 * r, a1 * (r ** 2)
            eq_typst = f"{t1} + {t2} + {t3} + ... quad (\"first \" {n} \" terms\")"
            ans_typst = f"S_{n} = {sn}"

            steps = [
                f"Identify geometric series parameters: $ a_1 = {a1} $, $ r = ({t2}) / ({t1}) = {r} $, $ n = {n} $",
                "Recall geometric series sum formula: $ S_n = (a_1 (1 - r^n)) / (1 - r) $",
                f"Compute power $r^n$: $ ({r})^({n}) = {r_pow_n} $",
                f"Substitute into formula: $ S_{n} = ({a1} (1 - ({r_pow_n}))) / (1 - ({r})) $",
                f"Simplify numerator and denominator: $ ({a1} dot ({1 - r_pow_n})) / ({1 - r}) = {sn} $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"S_{n} = {sn + r_pow_n}",
                f"S_{n} = {a1 * r_pow_n}",
                f"S_{n} = {sn - a1}"
            ]

            prompt = "Find the sum of each geometric series."

        return BaseProblem(
            id=f"pcalc_seq_spicy_{problem_idx}",
            prompt_text=prompt,
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
