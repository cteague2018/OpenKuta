from __future__ import annotations

import math
import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class ProbabilityStatisticsGenerator(BaseGenerator):
    generator_id = "algebra_2.probability_statistics"
    name = "Probability and Statistics"
    category = "Algebra 2"
    standards = ["CCSS.MATH.CONTENT.HSS.CP.A.1", "CCSS.MATH.CONTENT.HSS.CP.B.9"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Fundamental Counting Principle
            n1 = rng.randint(3, 6)
            n2 = rng.randint(4, 7)
            n3 = rng.randint(2, 5)
            total = n1 * n2 * n3
            q_str = f"A restaurant menu offers {n1} appetizers, {n2} main courses, and {n3} desserts. How many different 3-course meals can be ordered?"
            ans_str = f"{total} meals"
            distractors = [f"{n1 + n2 + n3} meals", f"{total + 10} meals", f"{n1 * n2} meals"]
            steps = [
                "Use the Fundamental Counting Principle: multiply the number of choices for each course.",
                f"Total combinations: $ {n1} * {n2} * {n3} = {total} $."
            ]

        elif difficulty == ProblemDifficulty.MEDIUM:
            # Permutations vs Combinations
            flavor = rng.choice(["permutation", "combination"])
            if flavor == "permutation":
                n = rng.randint(6, 10)
                r = rng.randint(2, 4)
                val = math.perm(n, r)
                q_str = f"In a race with {n} runners, in how many different ways can the top {r} finishers (1st, 2nd, etc.) be awarded?"
                ans_str = f"{val} ways"
                wrong = math.comb(n, r)
                distractors = [f"{wrong} ways", f"{val - 12} ways", f"{n * r} ways"]
                steps = [
                    f"Order matters, so use permutations: $ P({n}, {r}) = {n}! / ({n} - {r})! $.",
                    f"Compute: $ {val} $ ways."
                ]
            else:
                n = rng.randint(7, 12)
                r = rng.randint(2, 4)
                val = math.comb(n, r)
                q_str = f"A committee of {r} members is to be selected from a group of {n} volunteers. How many different committees can be formed?"
                ans_str = f"{val} committees"
                wrong = math.perm(n, r)
                distractors = [f"{wrong} committees", f"{val * 2} committees", f"{n * r} committees"]
                steps = [
                    f"Order does not matter, so use combinations: $ C({n}, {r}) = {n}! / ({r}! * ({n} - {r})!) $.",
                    f"Compute: $ {val} $ committees."
                ]

        else:  # SPICY
            # Probability with combinations
            # In a bag of 5 red and 6 blue marbles, probability of drawing 2 red
            red = rng.randint(4, 6)
            blue = rng.randint(5, 7)
            total_marbles = red + blue
            draw = 2

            fav = math.comb(red, draw)
            total_outcomes = math.comb(total_marbles, draw)
            g = math.gcd(fav, total_outcomes)
            ans_frac = f"{fav // g} / {total_outcomes // g}"

            q_str = (
                f"A bag contains {red} red marbles and {blue} blue marbles. If {draw} marbles are drawn at random without replacement, "
                f"what is the probability that both marbles are red?"
            )
            ans_str = f"P(2 red) = {ans_frac}"
            distractors = [
                f"P(2 red) = {red} / {total_marbles}",
                f"P(2 red) = {(fav // g) + 1} / {total_outcomes // g}",
                f"P(2 red) = {blue // g} / {total_outcomes // g}",
            ]

            steps = [
                f"Total marbles = $ {red} + {blue} = {total_marbles} $.",
                f"Favorable outcomes (choosing {draw} red from {red}): $ C({red}, {draw}) = {fav} $.",
                f"Total possible outcomes (choosing {draw} from {total_marbles}): $ C({total_marbles}, {draw}) = {total_outcomes} $.",
                f"Probability = $ {fav} / {total_outcomes} = {ans_frac} $."
            ]

        return BaseProblem(
            id=f"prob_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each counting or probability problem.",
            equation_typst=q_str,
            answer_typst=ans_str,
            steps_typst=steps,
            distractors=distractors,
            difficulty=difficulty,
            standards=self.standards,
            metadata={"problem": q_str}
        )
