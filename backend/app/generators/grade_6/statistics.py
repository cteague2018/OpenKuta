from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class Grade6StatisticsGenerator(BaseGenerator):
    generator_id = "grade_6.statistics"
    name = "Data Sets & Measures of Center"
    category = "Grade 6"
    standards = ["CCSS.MATH.CONTENT.6.SP.B.5.C"]

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
        """Mild: Mean of a data set with step-by-step addition and division."""
        mean_target = rng.choice([12, 14, 15, 16, 18, 20, 22, 25])
        n = rng.choice([5, 6])

        # Generate n numbers summing to n * mean_target
        if n == 5:
            delta1 = rng.choice([-6, -4, -2])
            delta2 = rng.choice([2, 4, 6])
            delta3 = rng.choice([-3, -1])
            delta4 = rng.choice([1, 3])
            delta5 = -(delta1 + delta2 + delta3 + delta4)
            nums = [mean_target + d for d in [delta1, delta2, delta3, delta4, delta5]]
        else:
            delta1 = rng.choice([-5, -3, -1])
            delta2 = rng.choice([1, 3, 5])
            delta3 = rng.choice([-4, -2])
            delta4 = rng.choice([2, 4])
            delta5 = rng.choice([-2, 2])
            delta6 = -(delta1 + delta2 + delta3 + delta4 + delta5)
            nums = [mean_target + d for d in [delta1, delta2, delta3, delta4, delta5, delta6]]

        rng.shuffle(nums)
        total_sum = sum(nums)
        data_str = ", ".join(str(x) for x in nums)
        sum_expr = " + ".join(str(x) for x in nums)

        eq_typst = f"\"Data: \" {data_str}"
        ans_typst = f"\"Mean\" = {mean_target}"

        steps = [
            "Recall definition of the mean: $ \"Mean\" = (\"Sum of data values\") / (\"Number of data values\") $",
            f"Count the number of data values: $ n = {n} $",
            f"Add all values: $ {sum_expr} = {total_sum} $",
            f"Divide sum by $ n $: $ {total_sum} / {n} = {mean_target} $",
            f"Result: $ {ans_typst} $"
        ]

        dist1 = f"\"Mean\" = {mean_target + 2}"
        dist2 = f"\"Mean\" = {mean_target - 2}"
        dist3 = f"\"Mean\" = {total_sum // (n - 1)}"

        distractors = list(dict.fromkeys([dist1, dist2, dist3]))
        while len(distractors) < 2:
            distractors.append(f"\"Mean\" = {mean_target + 1}")

        return BaseProblem(
            id=f"g6_stat_mild_{problem_idx}",
            prompt_text="Find the mean of the data set.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards,
            metadata={"mean": mean_target, "n": n, "sum": total_sum}
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Median (ordered list, finding middle element or average of middle two) and Mode."""
        n = rng.choice([7, 8])
        mode_val = rng.choice([12, 14, 15, 17, 18, 20, 22])

        # Pick distinct base values around mode_val
        others = [mode_val - 6, mode_val - 4, mode_val - 2, mode_val + 2, mode_val + 5, mode_val + 7]
        rng.shuffle(others)

        if n == 7:
            # 2 copies of mode_val, 5 distinct others
            nums = [mode_val, mode_val] + others[:5]
        else:
            # 2 copies of mode_val, 6 distinct others
            nums = [mode_val, mode_val] + others[:6]

        rng.shuffle(nums)
        sorted_nums = sorted(nums)

        median_val: float | int
        if n % 2 == 1:
            mid_idx = n // 2
            median_val = sorted_nums[mid_idx]
            median_step = f"Since $ n = {n} $ is odd, the median is the middle value at position $ {(n+1)//2} $: $ \"Median\" = {median_val} $."
        else:
            m1 = sorted_nums[n // 2 - 1]
            m2 = sorted_nums[n // 2]
            if (m1 + m2) % 2 == 0:
                median_val = (m1 + m2) // 2
                median_step = f"Since $ n = {n} $ is even, the median is the mean of the two middle values ($ {m1} $ and $ {m2} $): $ \"Median\" = ({m1} + {m2}) / 2 = {median_val} $."
            else:
                median_val = round((m1 + m2) / 2, 1)
                median_step = f"Since $ n = {n} $ is even, the median is the mean of the two middle values ($ {m1} $ and $ {m2} $): $ \"Median\" = ({m1} + {m2}) / 2 = {median_val} $."

        data_str = ", ".join(str(x) for x in nums)
        sorted_str = ", ".join(str(x) for x in sorted_nums)

        eq_typst = f"\"Data: \" {data_str}"
        ans_typst = f"\"Median\" = {median_val}, quad \"Mode\" = {mode_val}"

        steps = [
            f"Order the data set from least to greatest: $ {sorted_str} $",
            f"Count total data points: $ n = {n} $",
            median_step,
            f"Identify the mode (the value appearing most frequently): $ {mode_val} $ appears 2 times.",
            f"Result: $ {ans_typst} $"
        ]

        # Distractor 1: used unordered list middle
        unordered_mid = nums[n // 2]
        d1 = f"\"Median\" = {unordered_mid}, quad \"Mode\" = {mode_val}"
        # Distractor 2: swapped median and mode
        d2 = f"\"Median\" = {mode_val}, quad \"Mode\" = {median_val}"
        # Distractor 3: arithmetic variation in median
        d3 = f"\"Median\" = {median_val + 2}, quad \"Mode\" = {mode_val}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"\"Median\" = {median_val + 1}, quad \"Mode\" = {mode_val}")

        return BaseProblem(
            id=f"g6_stat_med_{problem_idx}",
            prompt_text="Find the median and mode of the data set.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards,
            metadata={"median": median_val, "mode": mode_val, "n": n}
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Range (max - min) and Interquartile Range (IQR = Q3 - Q1) from 5-number summary."""
        # Use 8 data points for clean quartile splits: lower half 4 values, upper half 4 values
        # To guarantee integer Q1 and Q3, lower half middle two sum to even, upper half middle two sum to even
        base = rng.choice([10, 15, 20, 25])
        # 8 ordered values:
        x1 = base
        x2 = base + rng.choice([2, 4])
        x3 = x2 + rng.choice([2, 4])
        x4 = x3 + rng.choice([1, 3])
        x5 = x4 + rng.choice([2, 4])
        x6 = x5 + rng.choice([2, 4])
        x7 = x6 + rng.choice([2, 4])
        x8 = x7 + rng.choice([3, 5])

        sorted_nums = [x1, x2, x3, x4, x5, x6, x7, x8]
        nums = list(sorted_nums)
        rng.shuffle(nums)

        min_val = x1
        max_val = x8
        range_val = max_val - min_val

        # Lower half: x1, x2, x3, x4 -> Q1 = (x2 + x3) / 2
        q1 = (x2 + x3) // 2 if (x2 + x3) % 2 == 0 else round((x2 + x3) / 2, 1)
        # Upper half: x5, x6, x7, x8 -> Q3 = (x6 + x7) / 2
        q3 = (x6 + x7) // 2 if (x6 + x7) % 2 == 0 else round((x6 + x7) / 2, 1)
        q2 = (x4 + x5) // 2 if (x4 + x5) % 2 == 0 else round((x4 + x5) / 2, 1)

        iqr_val = round(q3 - q1, 1) if isinstance(q3, float) or isinstance(q1, float) else q3 - q1

        data_str = ", ".join(str(x) for x in nums)
        sorted_str = ", ".join(str(x) for x in sorted_nums)
        lower_str = f"{x1}, {x2}, {x3}, {x4}"
        upper_str = f"{x5}, {x6}, {x7}, {x8}"

        eq_typst = f"\"Data: \" {data_str}"
        ans_typst = f"\"Range\" = {range_val}, quad \"IQR\" = {iqr_val}"

        steps = [
            f"Order the data set from least to greatest: $ {sorted_str} $",
            f"Identify Minimum and Maximum: $ \"Min\" = {min_val}, quad \"Max\" = {max_val} $",
            f"Calculate the Range: $ \"Range\" = \"Max\" - \"Min\" = {max_val} - {min_val} = {range_val} $",
            f"Find the median ($ Q_2 $): $ Q_2 = ({x4} + {x5}) / 2 = {q2} $",
            f"Find the first quartile ($ Q_1 $), the median of the lower half ($ {lower_str} $): $ Q_1 = ({x2} + {x3}) / 2 = {q1} $",
            f"Find the third quartile ($ Q_3 $), the median of the upper half ($ {upper_str} $): $ Q_3 = ({x6} + {x7}) / 2 = {q3} $",
            f"Calculate the Interquartile Range ($ \"IQR\" $): $ \"IQR\" = Q_3 - Q_1 = {q3} - {q1} = {iqr_val} $",
            f"Result: $ {ans_typst} $"
        ]

        d1 = f"\"Range\" = {iqr_val}, quad \"IQR\" = {range_val}"  # swapped
        d2 = f"\"Range\" = {range_val}, quad \"IQR\" = {q3 + q1}"  # added Q3 and Q1
        d3 = f"\"Range\" = {range_val + 2}, quad \"IQR\" = {iqr_val + 2}"

        distractors = list(dict.fromkeys([d1, d2, d3]))
        while len(distractors) < 2:
            distractors.append(f"\"Range\" = {range_val}, quad \"IQR\" = 10")

        return BaseProblem(
            id=f"g6_stat_spicy_{problem_idx}",
            prompt_text="Find the range and interquartile range (IQR) of the data set.",
            equation_typst=f"$ {eq_typst} $",
            answer_typst=f"$ {ans_typst} $",
            steps_typst=steps,
            distractors=[f"$ {d} $" for d in distractors[:3]],
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards,
            metadata={"min": min_val, "max": max_val, "q1": q1, "median": q2, "q3": q3, "range": range_val, "iqr": iqr_val}
        )
