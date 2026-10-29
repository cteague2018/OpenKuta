from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty
from backend.app.generators.verification_gate import verify_mathematical_truth


class PrecalcTrigGenerator(BaseGenerator):
    generator_id = "precalculus.trig"
    name = "Trigonometric Equations & Identities"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSF.TF.C.8", "CCSS.MATH.CONTENT.HSF.TF.C.9"]

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
        """Mild: Linear trig equations a*sin(x) + b = 0 or a*cos(x) + b = 0."""
        cases = [
            # (fn, eq_typst, val_str, ref_angle, quads, ans_typst, distractors)
            ("sin", "2 sin(x) - 1 = 0", "1/2", "pi/6", "I and II", "pi/6, 5 pi/6", ["pi/3, 2 pi/3", "7 pi/6, 11 pi/6", "pi/6, 11 pi/6"]),
            ("sin", "2 sin(x) + 1 = 0", "-1/2", "pi/6", "III and IV", "7 pi/6, 11 pi/6", ["pi/6, 5 pi/6", "4 pi/3, 5 pi/3", "5 pi/6, 7 pi/6"]),
            ("sin", "2 sin(x) - sqrt(2) = 0", "(sqrt(2))/2", "pi/4", "I and II", "pi/4, 3 pi/4", ["pi/4, 7 pi/4", "5 pi/4, 7 pi/4", "pi/3, 2 pi/3"]),
            ("sin", "2 sin(x) + sqrt(2) = 0", "-(sqrt(2))/2", "pi/4", "III and IV", "5 pi/4, 7 pi/4", ["pi/4, 3 pi/4", "3 pi/4, 5 pi/4", "2 pi/3, 4 pi/3"]),
            ("sin", "2 sin(x) - sqrt(3) = 0", "(sqrt(3))/2", "pi/3", "I and II", "pi/3, 2 pi/3", ["pi/6, 5 pi/6", "4 pi/3, 5 pi/3", "pi/3, 5 pi/3"]),
            ("sin", "2 sin(x) + sqrt(3) = 0", "-(sqrt(3))/2", "pi/3", "III and IV", "4 pi/3, 5 pi/3", ["pi/3, 2 pi/3", "7 pi/6, 11 pi/6", "2 pi/3, 4 pi/3"]),
            ("sin", "sin(x) - 1 = 0", "1", "pi/2", "boundary (positive y-axis)", "pi/2", ["3 pi/2", "0, pi", "pi"]),
            ("sin", "sin(x) + 1 = 0", "-1", "3 pi/2", "boundary (negative y-axis)", "3 pi/2", ["pi/2", "pi", "0, 2 pi"]),

            ("cos", "2 cos(x) - 1 = 0", "1/2", "pi/3", "I and IV", "pi/3, 5 pi/3", ["pi/6, 11 pi/6", "2 pi/3, 4 pi/3", "pi/3, 2 pi/3"]),
            ("cos", "2 cos(x) + 1 = 0", "-1/2", "pi/3", "II and III", "2 pi/3, 4 pi/3", ["pi/3, 5 pi/3", "5 pi/6, 7 pi/6", "4 pi/3, 5 pi/3"]),
            ("cos", "2 cos(x) - sqrt(2) = 0", "(sqrt(2))/2", "pi/4", "I and IV", "pi/4, 7 pi/4", ["pi/4, 3 pi/4", "3 pi/4, 5 pi/4", "pi/6, 11 pi/6"]),
            ("cos", "2 cos(x) + sqrt(2) = 0", "-(sqrt(2))/2", "pi/4", "II and III", "3 pi/4, 5 pi/4", ["pi/4, 7 pi/4", "5 pi/4, 7 pi/4", "2 pi/3, 4 pi/3"]),
            ("cos", "2 cos(x) - sqrt(3) = 0", "(sqrt(3))/2", "pi/6", "I and IV", "pi/6, 11 pi/6", ["pi/6, 5 pi/6", "pi/3, 5 pi/3", "5 pi/6, 7 pi/6"]),
            ("cos", "2 cos(x) + sqrt(3) = 0", "-(sqrt(3))/2", "pi/6", "II and III", "5 pi/6, 7 pi/6", ["pi/6, 11 pi/6", "7 pi/6, 11 pi/6", "2 pi/3, 4 pi/3"]),
            ("cos", "cos(x) - 1 = 0", "1", "0", "boundary (positive x-axis)", "0", ["pi", "pi/2, 3 pi/2", "2 pi"]),
            ("cos", "cos(x) + 1 = 0", "-1", "pi", "boundary (negative x-axis)", "pi", ["0", "pi/2", "3 pi/2"])
        ]

        fn, eq_typst, val_str, ref_ang, quads, ans_typst, distractors = rng.choice(cases)

        fn_name = "sine" if fn == "sin" else "cosine"
        steps = [
            f"Isolate the {fn_name} term: $ {fn}(x) = {val_str} $",
            f"Determine reference angle in $[0, pi/2]$: $ theta_\"ref\" = {ref_ang} $",
            f"{fn_name.capitalize()} has value ${val_str}$ in Quadrants / positions: {quads}.",
            f"Calculate all angles in $[0, 2 pi)$: $ x = {ans_typst} $"
        ]

        return BaseProblem(
            id=f"pcalc_trig_mild_{problem_idx}",
            prompt_text="Find all solutions to each equation in the interval $[0, 2 pi)$.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Tangent equations or factoring equations like 2 cos^2(x) - cos(x) = 0 or sin(2x) = cos(x)."""
        medium_cases = [
            # Tangent linear equations
            {
                "eq": "tan(x) - 1 = 0",
                "ans": "pi/4, 5 pi/4",
                "steps": [
                    "Isolate tan(x): $ tan(x) = 1 $",
                    "Find reference angle in $[0, pi/2]$: $ theta_\"ref\" = pi/4 $",
                    "Tangent is positive in Quadrants I and III",
                    "Solutions in $[0, 2 pi)$: $ x = pi/4, 5 pi/4 $"
                ],
                "distractors": ["3 pi/4, 7 pi/4", "pi/4, 3 pi/4", "pi/6, 7 pi/6"]
            },
            {
                "eq": "tan(x) + 1 = 0",
                "ans": "3 pi/4, 7 pi/4",
                "steps": [
                    "Isolate tan(x): $ tan(x) = -1 $",
                    "Find reference angle: $ theta_\"ref\" = pi/4 $",
                    "Tangent is negative in Quadrants II and IV",
                    "Solutions in $[0, 2 pi)$: $ x = 3 pi/4, 7 pi/4 $"
                ],
                "distractors": ["pi/4, 5 pi/4", "3 pi/4, 5 pi/4", "2 pi/3, 5 pi/3"]
            },
            {
                "eq": "sqrt(3) tan(x) - 1 = 0",
                "ans": "pi/6, 7 pi/6",
                "steps": [
                    "Isolate tan(x): $ tan(x) = 1/(sqrt(3)) = (sqrt(3))/3 $",
                    "Find reference angle: $ theta_\"ref\" = pi/6 $",
                    "Tangent is positive in Quadrants I and III",
                    "Solutions in $[0, 2 pi)$: $ x = pi/6, 7 pi/6 $"
                ],
                "distractors": ["pi/3, 4 pi/3", "5 pi/6, 11 pi/6", "pi/6, 5 pi/6"]
            },
            {
                "eq": "tan(x) - sqrt(3) = 0",
                "ans": "pi/3, 4 pi/3",
                "steps": [
                    "Isolate tan(x): $ tan(x) = sqrt(3) $",
                    "Find reference angle: $ theta_\"ref\" = pi/3 $",
                    "Tangent is positive in Quadrants I and III",
                    "Solutions in $[0, 2 pi)$: $ x = pi/3, 4 pi/3 $"
                ],
                "distractors": ["pi/6, 7 pi/6", "2 pi/3, 5 pi/3", "pi/3, 2 pi/3"]
            },
            # Factoring common trig terms
            {
                "eq": "2 cos^2(x) - cos(x) = 0",
                "ans": "pi/3, pi/2, 3 pi/2, 5 pi/3",
                "steps": [
                    "Factor out common term $cos(x)$: $ cos(x) (2 cos(x) - 1) = 0 $",
                    "Set each factor to zero: $ cos(x) = 0 $ or $ 2 cos(x) - 1 = 0 ==> cos(x) = 1/2 $",
                    "Solve $cos(x) = 0$ on $[0, 2 pi)$: $ x = pi/2, 3 pi/2 $",
                    "Solve $cos(x) = 1/2$ on $[0, 2 pi)$: Quadrants I and IV give $ x = pi/3, 5 pi/3 $",
                    "Combine all solutions in ascending order: $ x = pi/3, pi/2, 3 pi/2, 5 pi/3 $"
                ],
                "distractors": ["pi/6, pi/2, 3 pi/2, 11 pi/6", "pi/3, 2 pi/3, 4 pi/3, 5 pi/3", "0, pi/3, pi, 5 pi/3"]
            },
            {
                "eq": "2 cos^2(x) + cos(x) = 0",
                "ans": "pi/2, 2 pi/3, 4 pi/3, 3 pi/2",
                "steps": [
                    "Factor out $cos(x)$: $ cos(x) (2 cos(x) + 1) = 0 $",
                    "Set each factor to zero: $ cos(x) = 0 $ or $ cos(x) = -1/2 $",
                    "Solve $cos(x) = 0$: $ x = pi/2, 3 pi/2 $",
                    "Solve $cos(x) = -1/2$: Quadrants II and III give $ x = 2 pi/3, 4 pi/3 $",
                    "Combine all solutions: $ x = pi/2, 2 pi/3, 4 pi/3, 3 pi/2 $"
                ],
                "distractors": ["pi/3, pi/2, 3 pi/2, 5 pi/3", "2 pi/3, pi, 4 pi/3", "5 pi/6, pi/2, 3 pi/2, 7 pi/6"]
            },
            {
                "eq": "2 sin^2(x) - sin(x) = 0",
                "ans": "0, pi/6, 5 pi/6, pi",
                "steps": [
                    "Factor out $sin(x)$: $ sin(x) (2 sin(x) - 1) = 0 $",
                    "Set factors to zero: $ sin(x) = 0 $ or $ sin(x) = 1/2 $",
                    "Solve $sin(x) = 0$ in $[0, 2 pi)$: $ x = 0, pi $",
                    "Solve $sin(x) = 1/2$ in $[0, 2 pi)$: Quadrants I and II give $ x = pi/6, 5 pi/6 $",
                    "Combine all solutions: $ x = 0, pi/6, 5 pi/6, pi $"
                ],
                "distractors": ["0, pi/3, 2 pi/3, pi", "pi/6, 5 pi/6, 7 pi/6, 11 pi/6", "0, pi/2, pi, 3 pi/2"]
            },
            # Double angle factoring: sin(2x) = cos(x)
            {
                "eq": "sin(2 x) = cos(x)",
                "ans": "pi/6, pi/2, 5 pi/6, 3 pi/2",
                "steps": [
                    "Apply double-angle identity $sin(2 x) = 2 sin(x) cos(x)$: $ 2 sin(x) cos(x) = cos(x) $",
                    "Rearrange to set equal to zero: $ 2 sin(x) cos(x) - cos(x) = 0 $",
                    "Factor out $cos(x)$: $ cos(x) (2 sin(x) - 1) = 0 $",
                    "Branch 1 ($cos(x) = 0$): $ x = pi/2, 3 pi/2 $",
                    "Branch 2 ($sin(x) = 1/2$): $ x = pi/6, 5 pi/6 $",
                    "Combine all solutions in $[0, 2 pi)$: $ x = pi/6, pi/2, 5 pi/6, 3 pi/2 $"
                ],
                "distractors": ["pi/3, pi/2, 2 pi/3, 3 pi/2", "pi/6, 5 pi/6, 7 pi/6, 11 pi/6", "0, pi/6, pi/2, pi"]
            },
            {
                "eq": "sin(2 x) + cos(x) = 0",
                "ans": "pi/2, 7 pi/6, 3 pi/2, 11 pi/6",
                "steps": [
                    "Apply identity $sin(2 x) = 2 sin(x) cos(x)$: $ 2 sin(x) cos(x) + cos(x) = 0 $",
                    "Factor out $cos(x)$: $ cos(x) (2 sin(x) + 1) = 0 $",
                    "Branch 1 ($cos(x) = 0$): $ x = pi/2, 3 pi/2 $",
                    "Branch 2 ($sin(x) = -1/2$): $ x = 7 pi/6, 11 pi/6 $",
                    "Combine all solutions: $ x = pi/2, 7 pi/6, 3 pi/2, 11 pi/6 $"
                ],
                "distractors": ["pi/6, pi/2, 5 pi/6, 3 pi/2", "2 pi/3, pi/2, 4 pi/3, 3 pi/2", "0, pi, 7 pi/6, 11 pi/6"]
            }
        ]

        c = rng.choice(medium_cases)
        return BaseProblem(
            id=f"pcalc_trig_med_{problem_idx}",
            prompt_text="Find all solutions to each equation in the interval $[0, 2 pi)$.",
            equation_typst=str(c["eq"]),
            answer_typst=str(c["ans"]),
            steps_typst=list(c["steps"]),
            distractors=list(c["distractors"]),
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: Quadratic trig equations or double angle substitutions."""
        spicy_cases = [
            # Quadratic in sin: 2 sin^2(x) + 3 sin(x) + 1 = 0
            {
                "eq": "2 sin^2(x) + 3 sin(x) + 1 = 0",
                "ans": "7 pi/6, 3 pi/2, 11 pi/6",
                "steps": [
                    "Treat as quadratic in $u = sin(x)$: $ 2 u^2 + 3 u + 1 = 0 $",
                    "Factor the quadratic: $ (2 u + 1)(u + 1) = 0 ==> (2 sin(x) + 1)(sin(x) + 1) = 0 $",
                    "Set each factor to zero: $ sin(x) = -1/2 $ or $ sin(x) = -1 $",
                    "For $sin(x) = -1/2$, reference angle is $pi/6$ in Quad III & IV: $ x = 7 pi/6, 11 pi/6 $",
                    "For $sin(x) = -1$: $ x = 3 pi/2 $",
                    "Combine all distinct solutions: $ x = 7 pi/6, 3 pi/2, 11 pi/6 $"
                ],
                "distractors": ["pi/6, pi/2, 5 pi/6", "7 pi/6, 5 pi/4, 11 pi/6", "4 pi/3, 3 pi/2, 5 pi/3"]
            },
            # Quadratic in sin: 2 sin^2(x) - 3 sin(x) + 1 = 0
            {
                "eq": "2 sin^2(x) - 3 sin(x) + 1 = 0",
                "ans": "pi/6, pi/2, 5 pi/6",
                "steps": [
                    "Treat as quadratic in $u = sin(x)$: $ 2 u^2 - 3 u + 1 = 0 $",
                    "Factor: $ (2 sin(x) - 1)(sin(x) - 1) = 0 $",
                    "Set each factor to zero: $ sin(x) = 1/2 $ or $ sin(x) = 1 $",
                    "For $sin(x) = 1/2$, Quad I & II: $ x = pi/6, 5 pi/6 $",
                    "For $sin(x) = 1$: $ x = pi/2 $",
                    "Combine all distinct solutions: $ x = pi/6, pi/2, 5 pi/6 $"
                ],
                "distractors": ["7 pi/6, 3 pi/2, 11 pi/6", "pi/3, pi/2, 2 pi/3", "pi/6, pi/4, 5 pi/6"]
            },
            # Quadratic in cos: 2 cos^2(x) - 3 cos(x) + 1 = 0
            {
                "eq": "2 cos^2(x) - 3 cos(x) + 1 = 0",
                "ans": "0, pi/3, 5 pi/3",
                "steps": [
                    "Treat as quadratic in $u = cos(x)$: $ 2 u^2 - 3 u + 1 = 0 $",
                    "Factor: $ (2 cos(x) - 1)(cos(x) - 1) = 0 $",
                    "Set each factor to zero: $ cos(x) = 1/2 $ or $ cos(x) = 1 $",
                    "For $cos(x) = 1/2$, Quad I & IV: $ x = pi/3, 5 pi/3 $",
                    "For $cos(x) = 1$: $ x = 0 $",
                    "Combine all distinct solutions: $ x = 0, pi/3, 5 pi/3 $"
                ],
                "distractors": ["pi/3, pi, 5 pi/3", "0, 2 pi/3, 4 pi/3", "pi/6, pi/2, 11 pi/6"]
            },
            # Quadratic in cos: 2 cos^2(x) + 3 cos(x) + 1 = 0
            {
                "eq": "2 cos^2(x) + 3 cos(x) + 1 = 0",
                "ans": "2 pi/3, pi, 4 pi/3",
                "steps": [
                    "Treat as quadratic in $u = cos(x)$: $ 2 u^2 + 3 u + 1 = 0 $",
                    "Factor: $ (2 cos(x) + 1)(cos(x) + 1) = 0 $",
                    "Set each factor to zero: $ cos(x) = -1/2 $ or $ cos(x) = -1 $",
                    "For $cos(x) = -1/2$, Quad II & III: $ x = 2 pi/3, 4 pi/3 $",
                    "For $cos(x) = -1$: $ x = pi $",
                    "Combine all distinct solutions: $ x = 2 pi/3, pi, 4 pi/3 $"
                ],
                "distractors": ["0, pi/3, 5 pi/3", "5 pi/6, pi, 7 pi/6", "2 pi/3, 3 pi/2, 4 pi/3"]
            },
            # Double angle: cos(2x) + sin(x) = 0
            {
                "eq": "cos(2 x) + sin(x) = 0",
                "ans": "pi/2, 7 pi/6, 11 pi/6",
                "steps": [
                    "Substitute double-angle identity $cos(2 x) = 1 - 2 sin^2(x)$: $ 1 - 2 sin^2(x) + sin(x) = 0 $",
                    "Multiply by -1 to put in standard form: $ 2 sin^2(x) - sin(x) - 1 = 0 $",
                    "Factor: $ (2 sin(x) + 1)(sin(x) - 1) = 0 $",
                    "Set factors to zero: $ sin(x) = -1/2 $ or $ sin(x) = 1 $",
                    "For $sin(x) = -1/2$: Quad III & IV give $ x = 7 pi/6, 11 pi/6 $",
                    "For $sin(x) = 1$: $ x = pi/2 $",
                    "Solutions in $[0, 2 pi)$: $ x = pi/2, 7 pi/6, 11 pi/6 $"
                ],
                "distractors": ["3 pi/2, pi/6, 5 pi/6", "pi/2, 4 pi/3, 5 pi/3", "pi/6, pi/2, 5 pi/6"]
            },
            # Double angle: cos(2x) - cos(x) = 0
            {
                "eq": "cos(2 x) - cos(x) = 0",
                "ans": "0, 2 pi/3, 4 pi/3",
                "steps": [
                    "Substitute double-angle identity $cos(2 x) = 2 cos^2(x) - 1$: $ 2 cos^2(x) - cos(x) - 1 = 0 $",
                    "Factor the quadratic: $ (2 cos(x) + 1)(cos(x) - 1) = 0 $",
                    "Set factors to zero: $ cos(x) = -1/2 $ or $ cos(x) = 1 $",
                    "For $cos(x) = -1/2$: Quad II & III give $ x = 2 pi/3, 4 pi/3 $",
                    "For $cos(x) = 1$: $ x = 0 $",
                    "Solutions in $[0, 2 pi)$: $ x = 0, 2 pi/3, 4 pi/3 $"
                ],
                "distractors": ["0, pi/3, 5 pi/3", "pi, 2 pi/3, 4 pi/3", "pi/2, 2 pi/3, 4 pi/3"]
            }
        ]

        c = rng.choice(spicy_cases)
        return BaseProblem(
            id=f"pcalc_trig_spicy_{problem_idx}",
            prompt_text="Find all solutions to each equation in the interval $[0, 2 pi)$.",
            equation_typst=str(c["eq"]),
            answer_typst=str(c["ans"]),
            steps_typst=list(c["steps"]),
            distractors=list(c["distractors"]),
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
