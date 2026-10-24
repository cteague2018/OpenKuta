from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Grade6StatisticsGenerator(BaseGenerator):
    generator_id = "grade_6.statistics"
    name = "Data Sets & Measures of Center"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.SP.B.5.C"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        idx = problem_idx
        mean_target = rng.choice([12, 14, 15, 18, 20])
        # Pick 5 numbers with integer average
        d1 = mean_target - rng.choice([2, 4])
        d2 = mean_target + rng.choice([2, 4])
        d3 = mean_target - rng.choice([1, 3])
        d4 = mean_target + rng.choice([1, 3])
        d5 = 5 * mean_target - (d1 + d2 + d3 + d4)

        nums = [d1, d2, d3, d4, d5]
        rng.shuffle(nums)
        data_str = ", ".join(str(n) for n in nums)
        eq_typst = f"\"Data: \" {data_str}"
        ans_typst = f"\"Mean = \" {mean_target}"

        steps = [
            f"Recall definition of mean: $ \"Mean\" = (\"Sum of values\") / (\"Number of values\") $",
            f"Add all values: $ {d1} + {d2} + {d3} + {d4} + {d5} = {5 * mean_target} $",
            f"Divide by number of data points (5): $ ({5 * mean_target}) / 5 = {mean_target} $",
            f"Result: $ {ans_typst} $"
        ]

        return BaseProblem(
            id=f"g6_stat_{problem_idx}",
            prompt_text="Find the mean of the data set.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=[f"Mean = {mean_target + 2}", f"Mean = {mean_target - 1}"],
            difficulty=difficulty,
            standards=self.standards
        )
