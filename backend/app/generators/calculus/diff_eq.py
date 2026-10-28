from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class CalculusDiffEqGenerator(BaseGenerator):
    generator_id = "calculus.diff_eq"
    name = "Differential Equations (Separable & Growth)"
    category = "Calculus"
    standards = ["AP.CALC.FUN-7.D", "AP.CALC.FUN-7.E"]

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
        """Mild: dy/dx = ky (separable exponential growth/decay)."""
        k = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])
        k_str = f"{k}"

        eq_typst = f"(d y)/(d x) = {k_str} y"
        ans_typst = f"y = C e^({k_str} x)"

        steps = [
            f"Separate variables by dividing by y and multiplying by dif x: $ 1/y dif y = {k_str} dif x $",
            f"Integrate both sides: $ integral 1/y dif y = integral {k_str} dif x $",
            f"Evaluate integrals: $ ln|y| = {k_str} x + C_1 $",
            f"Exponentiate both sides: $ |y| = e^({k_str} x + C_1) = e^(C_1) dot e^({k_str} x) $",
            f"Let $C = plus.minus e^(C_1)$ to write the general solution: $ {ans_typst} $"
        ]

        distractors = [
            f"y = {k_str} x + C",
            f"y = C e^(-{k_str} x)",
            f"y = 1/({k_str}) e^({k_str} x)"
        ]

        return BaseProblem(
            id=f"calc_de_mild_{problem_idx}",
            prompt_text="Find the general solution of each differential equation.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: dy/dx = a*x/y or dy/dx = a*x^2*y."""
        subtype = rng.choice(["rational", "poly_growth"])

        if subtype == "rational":
            # dy/dx = a*x / y  ==> y dy = a x dx ==> y^2 / 2 = a x^2 / 2 + C1 ==> y^2 - a x^2 = C
            a = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])
            if a == 1:
                eq_typst = "(d y)/(d x) = x / y"
                x_term = "x"
                ans_typst = "y^2 - x^2 = C"
                step_rearrange = "y^2 - x^2 = C"
            elif a == -1:
                eq_typst = "(d y)/(d x) = -x / y"
                x_term = "-x"
                ans_typst = "y^2 + x^2 = C"
                step_rearrange = "y^2 + x^2 = C"
            elif a > 1:
                eq_typst = f"(d y)/(d x) = ({a} x) / y"
                x_term = f"{a} x"
                ans_typst = f"y^2 - {a} x^2 = C"
                step_rearrange = f"y^2 - {a} x^2 = C"
            else:
                eq_typst = f"(d y)/(d x) = -({abs(a)} x) / y"
                x_term = f"{a} x"
                ans_typst = f"y^2 + {abs(a)} x^2 = C"
                step_rearrange = f"y^2 + {abs(a)} x^2 = C"

            steps = [
                f"Separate variables by multiplying by y and dif x: $ y dif y = ({x_term}) dif x $",
                f"Integrate both sides: $ integral y dif y = integral ({x_term}) dif x $",
                f"Evaluate antiderivatives: $ (y^2)/2 = ({a} x^2)/2 + C_1 $",
                f"Multiply by 2 and let $C = 2 C_1$: $ {step_rearrange} $",
                f"Implicit general solution: $ {ans_typst} $"
            ]

            distractors = [
                f"y^2 = {a} x + C",
                f"y = {a} x^2 + C",
                f"y^2 + {abs(a) if a > 0 else -abs(a)} x^2 = C"
            ]
        else:
            # dy/dx = a*x^2*y ==> 1/y dy = a x^2 dx ==> ln|y| = (a/3) x^3 + C1 ==> y = C e^((a/3) x^3)
            a = rng.choice([-3, -2, -1, 1, 2, 3, 6])
            if a == 1:
                eq_typst = "(d y)/(d x) = x^2 y"
                int_str = "(1/3) x^3"
            elif a == -1:
                eq_typst = "(d y)/(d x) = -x^2 y"
                int_str = "(-1/3) x^3"
            elif a == 3:
                eq_typst = "(d y)/(d x) = 3 x^2 y"
                int_str = "x^3"
            elif a == -3:
                eq_typst = "(d y)/(d x) = -3 x^2 y"
                int_str = "-x^3"
            elif a == 6:
                eq_typst = "(d y)/(d x) = 6 x^2 y"
                int_str = "2 x^3"
            elif a == 2:
                eq_typst = "(d y)/(d x) = 2 x^2 y"
                int_str = "(2/3) x^3"
            else:
                eq_typst = f"(d y)/(d x) = {a} x^2 y"
                int_str = f"({a}/3) x^3"

            ans_typst = f"y = C e^({int_str})"

            steps = [
                f"Separate variables: $ 1/y dif y = ({a} x^2) dif x $" if abs(a) != 1 else f"Separate variables: $ 1/y dif y = {'x^2' if a == 1 else '-x^2'} dif x $",
                f"Integrate both sides: $ integral 1/y dif y = integral ({a} x^2) dif x $" if abs(a) != 1 else f"Integrate both sides: $ integral 1/y dif y = integral {'x^2' if a == 1 else '-x^2'} dif x $",
                f"Compute antiderivatives: $ ln|y| = {int_str} + C_1 $",
                f"Exponentiate both sides: $ |y| = e^({int_str} + C_1) = e^(C_1) dot e^({int_str}) $",
                f"General solution: $ {ans_typst} $"
            ]

            distractors = [
                f"y = {a} x^3 + C",
                f"y = C e^({a} x^2)",
                f"y = C e^(-({int_str}))"
            ]

        return BaseProblem(
            id=f"calc_de_med_{problem_idx}",
            prompt_text="Find the general solution of each differential equation.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: dy/dx = k*(y - T) (Newton's Law of Cooling) or IVP dy/dx = 2xy with y(0) = c."""
        subtype = rng.choice(["cooling", "ivp"])

        if subtype == "cooling":
            k = rng.choice([-4, -3, -2, 2, 3, 4])
            t_env = rng.choice([20, 25, 40, 68, 70, 75])

            eq_typst = f"(d y)/(d x) = {k} (y - {t_env})"
            ans_typst = f"y = {t_env} + C e^({k} x)"

            steps = [
                f"Separate variables by dividing by $(y - {t_env})$: $ 1/(y - {t_env}) dif y = {k} dif x $",
                f"Integrate both sides: $ integral 1/(y - {t_env}) dif y = integral {k} dif x $",
                f"Evaluate integrals: $ ln|y - {t_env}| = {k} x + C_1 $",
                f"Exponentiate both sides: $ |y - {t_env}| = e^({k} x + C_1) = e^(C_1) dot e^({k} x) $",
                f"Solve for y (letting $C = plus.minus e^(C_1)$): $ {ans_typst} $"
            ]

            distractors = [
                f"y = {t_env} - C e^(-{k} x)",
                f"y = C e^({k} x) - {t_env}",
                f"y = {t_env} + {k} x + C"
            ]

            prompt = "Find the general solution of the differential equation."
        else:
            # IVP: dy/dx = 2a x y with y(0) = c
            a = rng.choice([-2, -1, 1, 2, 3])
            c = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            coeff = 2 * a

            eq_coeff_str = f"{coeff} x y" if coeff != 1 else "x y"
            if coeff == -1:
                eq_coeff_str = "-x y"

            exp_str = f"{a} x^2" if a != 1 else "x^2"
            if a == -1:
                exp_str = "-x^2"

            eq_typst = f"(d y)/(d x) = {eq_coeff_str}, quad y(0) = {c}"
            ans_typst = f"y = {c} e^({exp_str})"

            steps = [
                f"Separate variables: $ 1/y dif y = {coeff} x dif x $",
                f"Integrate both sides: $ integral 1/y dif y = integral {coeff} x dif x $",
                f"Evaluate antiderivatives: $ ln|y| = {exp_str} + C_1 ==> y = C e^({exp_str}) $",
                f"Apply initial condition $y(0) = {c}$: $ {c} = C e^({a}(0)^2) = C dot 1 ==> C = {c} $",
                f"Substitute C to obtain the particular solution: $ {ans_typst} $"
            ]

            distractors = [
                f"y = {c} e^({coeff} x)",
                f"y = {c} e^(-({exp_str}))",
                f"y = {exp_str} + {c}"
            ]

            prompt = "Solve the initial value problem."

        return BaseProblem(
            id=f"calc_de_spicy_{problem_idx}",
            prompt_text=prompt,
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
