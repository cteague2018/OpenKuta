from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class PrecalcSequencesGenerator(BaseGenerator):
    generator_id = "precalculus.sequences"
    name = "Sequences and Series"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSF.BF.A.2"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        a1 = rng.choice([2, 3, 5, 7, -4])
        d = rng.choice([3, 4, 5, -2, -3])
        n = rng.choice([10, 12, 15, 20])

        an = a1 + (n - 1) * d
        t1, t2, t3 = a1, a1 + d, a1 + 2*d
        eq_typst = f"{t1}, {t2}, {t3}, ... ; quad a_{n} = ?"
        ans_typst = f"a_{n} = {an}"

        steps = [
            f"Identify first term: $ a_1 = {a1} $",
            f"Find common difference: $ d = {t2} - ({t1}) = {d} $",
            f"Recall arithmetic sequence formula: $ a_n = a_1 + (n - 1) d $",
            f"Substitute $ n = {n} $: $ a_{n} = {a1} + ({n} - 1)({d}) $",
            f"Compute: $ {a1} + ({n-1})({d}) = {a1} + ({(n-1)*d}) = {an} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"pcalc_seq_{problem_idx}",
            prompt_text="Find the specified term in each arithmetic sequence.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"a_{n} = {an + d}", f"a_{n} = {an - 2*d}"],
            difficulty=difficulty,
            standards=self.standards
        )
