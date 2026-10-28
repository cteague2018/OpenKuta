from __future__ import annotations

import random

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
            # Distance, Rate, Time with varied vehicles and units
            mild_scenarios = [
                ("passenger car", "miles per hour", "miles", "hours", [45, 50, 55, 60, 65]),
                ("cyclist", "miles per hour", "miles", "hours", [12, 14, 15, 16, 18]),
                ("high-speed bullet train", "kilometers per hour", "kilometers", "hours", [120, 150, 180, 200]),
                ("motorboat", "miles per hour", "miles", "hours", [20, 24, 25, 30]),
                ("distance runner", "kilometers per hour", "kilometers", "hours", [10, 12, 14]),
            ]
            vehicle, speed_unit, dist_unit, time_unit, speed_choices = rng.choice(mild_scenarios)
            speed = rng.choice(speed_choices)
            t_val = rng.randint(2, 6)
            dist = speed * t_val
            q_text = f"A {vehicle} travels at an average speed of {speed} {speed_unit}. How far does it travel in {t_val} {time_unit}?"
            ans_str = f"{dist} {dist_unit}"
            distractors = [f"{dist + speed} {dist_unit}", f"{max(1, dist - speed)} {dist_unit}", f"{speed * (t_val + 1)} {dist_unit}"]
            steps = [
                "Use the distance formula: $ d = r * t $.",
                f"Substitute given rate $ r = {speed} $ and time $ t = {t_val} $.",
                f"Calculate: $ d = {speed} * {t_val} = {dist} $ {dist_unit}."
            ]
        elif difficulty == ProblemDifficulty.MEDIUM:
            flavor = rng.choice(["distance", "systems_tickets"])
            if flavor == "distance":
                med_dist_scenarios = [
                    ("Two trains leave the same station at the same time, traveling in opposite directions.", "One travels at {s1} {speed_u} and the other at {s2} {speed_u}. In how many {time_u} will they be {tot_dist} {dist_u} apart?", "mph", "miles", "hours"),
                    ("Two cyclists depart from a junction and ride in opposite directions along a trail.", "One pedals at {s1} {speed_u} and the other at {s2} {speed_u}. In how many {time_u} will they be {tot_dist} {dist_u} apart?", "mph", "miles", "hours"),
                    ("Two delivery vans leave a distribution center heading in opposite directions.", "One drives at {s1} {speed_u} and the other at {s2} {speed_u}. In how many {time_u} will they be {tot_dist} {dist_u} apart?", "km/h", "kilometers", "hours"),
                ]
                intro_text, q_template, speed_u, dist_u, time_u = rng.choice(med_dist_scenarios)
                s1 = rng.choice([35, 40, 45, 50, 55])
                s2 = rng.choice([45, 50, 55, 60, 65])
                t_val = rng.randint(2, 5)
                tot_dist = (s1 + s2) * t_val
                q_text = f"{intro_text} {q_template.format(s1=s1, s2=s2, speed_u=speed_u, time_u=time_u, tot_dist=tot_dist, dist_u=dist_u)}"
                ans_str = f"{t_val} {time_u}"
                distractors = [f"{t_val + 1} {time_u}", f"{t_val + 2} {time_u}", f"{max(1, t_val - 1)} {time_u}"]
                steps = [
                    f"Combined rate of separation: $ r = {s1} + {s2} = {s1 + s2} $ {speed_u}.",
                    f"Use distance formula: $ d = r * t ==> {tot_dist} = {s1 + s2} * t $.",
                    f"Divide both sides: $ t = {tot_dist} / {s1 + s2} = {t_val} $ {time_u}."
                ]
            else:
                systems_scenarios = [
                    ("Tickets to a school play", "children", "adults", (5, 6, 7), (10, 11, 12)),
                    ("Wristbands for a community carnival", "students", "general admission", (6, 7, 8), (12, 14, 15)),
                    ("Admission passes to a science museum", "youth", "adults", (8, 9, 10), (14, 16, 18)),
                ]
                event_name, group_a, group_b, p_a_range, p_b_range = rng.choice(systems_scenarios)
                c_price = rng.choice(p_a_range)
                a_price = rng.choice(p_b_range)
                c_count = rng.randint(6, 16)
                a_count = rng.randint(6, 16)
                tot_count = c_count + a_count
                tot_rev = c_price * c_count + a_price * a_count
                q_text = (
                    f"{event_name} cost \\${c_price} for {group_a} and \\${a_price} for {group_b}. "
                    f"A total of {tot_count} tickets were sold for \\${tot_rev}. How many {group_a} tickets were sold?"
                )
                ans_str = f"{c_count} tickets"
                distractors = [f"{a_count} tickets", f"{c_count + 3} tickets", f"{max(1, c_count - 2)} tickets"]
                steps = [
                    f"Let $ c $ = {group_a} tickets and $ a $ = {group_b} tickets.",
                    f"Set up system of equations: $ cases(c + a = {tot_count}, {c_price}c + {a_price}a = {tot_rev}) $.",
                    f"Substitute $ a = {tot_count} - c $ into the cost equation: $ {c_price}c + {a_price}({tot_count} - c) = {tot_rev} $.",
                    f"Solve for $ c $: $ {c_count} $ tickets."
                ]
        else:  # SPICY
            # Mixture word problem with varied solute and unit
            mix_scenarios = [
                ("acid solution", "liters", "L"),
                ("saline solution", "milliliters", "mL"),
                ("antifreeze coolant", "gallons", "gal"),
                ("sugar syrup", "fluid ounces", "fl oz"),
            ]
            solute_name, unit_full, unit_abbr = rng.choice(mix_scenarios)
            p1 = rng.choice([10, 15, 20, 25])
            p2 = rng.choice([40, 50, 60, 70])
            v1 = rng.choice([4, 6, 8, 10])
            target_p = rng.choice([25, 30, 35])
            if target_p <= p1:
                target_p = p1 + 10
            if target_p >= p2:
                target_p = p2 - 10
            num = v1 * (target_p - p1)
            den = (p2 - target_p)
            x_val = num // den if num % den == 0 else round(num / den, 1)

            q_text = (
                f"A lab technician has {v1} {unit_full} of a {p1}% {solute_name}. How many {unit_full} of a {p2}% {solute_name} "
                f"must be mixed in to obtain a solution that is {target_p}% {solute_name.split()[0]}?"
            )
            ans_str = f"{x_val} {unit_full}"
            distractors = [f"{x_val + 2} {unit_full}", f"{max(1, x_val - 2)} {unit_full}", f"{v1 * 2} {unit_full}"]
            steps = [
                f"Let $ x $ be the {unit_full} of {p2}% solution to add.",
                f"Set up solute balance: $ {p1 / 100} * {v1} + {p2 / 100} * x = {target_p / 100} * ({v1} + x) $.",
                "Solve the linear equation for $ x $.",
                f"Result: $ x = {x_val} $ {unit_full}."
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
