from __future__ import annotations

import random
from typing import List

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class Algebra1WordProblemsGenerator(BaseGenerator):
    generator_id = "algebra_1.word_problems"
    name = "Algebra 1 Word Problems"
    category = "Algebra 1"
    standards = ["CCSS.MATH.CONTENT.HSA.CED.A.1", "CCSS.MATH.CONTENT.HSA.CED.A.2"]

    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        if difficulty == ProblemDifficulty.MILD:
            # Distance, Rate, Time basic
            speed = rng.choice([45, 50, 55, 60, 65])
            hours = rng.randint(2, 6)
            dist = speed * hours
            q_text = f"A passenger car travels at an average speed of {speed} miles per hour. How far does it travel in {hours} hours?"
            ans_str = f"{dist} miles"
            distractors = [f"{dist + speed} miles", f"{dist - speed} miles", f"{speed * (hours + 1)} miles"]
            steps = [
                f"Use the distance formula: $ d = r * t $.",
                f"Substitute given rate $ r = {speed} $ and time $ t = {hours} $.",
                f"Calculate: $ d = {speed} * {hours} = {dist} $ miles."
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            flavor = rng.choice(["distance", "systems_tickets"])
            if flavor == "distance":
                s1 = rng.choice([40, 50, 60])
                s2 = rng.choice([50, 60, 70])
                hours = rng.randint(2, 5)
                tot_dist = (s1 + s2) * hours
                q_text = (
                    f"Two trains leave the same station at the same time, traveling in opposite directions. "
                    f"One travels at {s1} mph and the other at {s2} mph. In how many hours will they be {tot_dist} miles apart?"
                )
                ans_str = f"{hours} hours"
                distractors = [f"{hours + 1} hours", f"{hours + 2} hours", f"{max(1, hours - 1)} hours"]
                steps = [
                    f"Combined rate of separation: $ r = {s1} + {s2} = {s1 + s2} $ mph.",
                    f"Use distance formula: $ d = r * t ==> {tot_dist} = {s1 + s2} * t $.",
                    f"Divide both sides: $ t = {tot_dist} / {s1 + s2} = {hours} $ hours."
                ]
            else:
                c_price = rng.choice([5, 6, 7])
                a_price = rng.choice([10, 11, 12])
                c_count = rng.randint(5, 15)
                a_count = rng.randint(5, 15)
                tot_count = c_count + a_count
                tot_rev = c_price * c_count + a_price * a_count
                q_text = (
                    f"Tickets to a school play cost ${c_price} for children and ${a_price} for adults. "
                    f"A total of {tot_count} tickets were sold for ${tot_rev}. How many children's tickets were sold?"
                )
                ans_str = f"{c_count} tickets"
                distractors = [f"{a_count} tickets", f"{c_count + 3} tickets", f"{max(1, c_count - 2)} tickets"]
                steps = [
                    f"Let $ c $ = children's tickets and $ a $ = adult tickets.",
                    f"Set up system of equations: $ cases(c + a = {tot_count}, {c_price}c + {a_price}a = {tot_rev}) $.",
                    f"Substitute $ a = {tot_count} - c $ into the cost equation: $ {c_price}c + {a_price}({tot_count} - c) = {tot_rev} $.",
                    f"Solve for $ c $: $ {c_count} $ tickets."
                ]
        else: # SPICY
            # Mixture word problem
            p1 = rng.choice([10, 20, 25])
            p2 = rng.choice([40, 50, 60])
            # Desired target concentration between p1 and p2
            # E.g. 5 liters of p1 + x liters of p2 = (5 + x) liters of target
            v1 = rng.choice([4, 6, 8, 10])
            target_p = rng.choice([30, 35])
            # v1 * p1 + x * p2 = (v1 + x) * target_p
            # v1 * (target_p - p1) = x * (p2 - target_p)
            num = v1 * (target_p - p1)
            den = (p2 - target_p)
            x_liters = num // den if num % den == 0 else round(num / den, 1)

            q_text = (
                f"A chemist has {v1} liters of a {p1}% acid solution. How many liters of a {p2}% acid solution "
                f"must be mixed in to obtain a solution that is {target_p}% acid?"
            )
            ans_str = f"{x_liters} liters"
            distractors = [f"{x_liters + 2} liters", f"{max(1, x_liters - 2)} liters", f"{v1 * 2} liters"]
            steps = [
                f"Let $ x $ be the liters of {p2}% solution to add.",
                f"Set up total acid balance: $ {p1 / 100} * {v1} + {p2 / 100} * x = {target_p / 100} * ({v1} + x) $.",
                f"Solve the linear equation for $ x $.",
                f"Result: $ x = {x_liters} $ liters."
            ]

        return BaseProblem(
            id=f"wordprob_{difficulty.value}_{problem_idx}",
            prompt_text="Solve each word problem.",
            equation_typst=q_text,
            answer_typst=ans_str,
            steps_typst=steps,
            distractors=distractors,
            difficulty=difficulty,
            standards=self.standards,
            metadata={"question": q_text}
        )

