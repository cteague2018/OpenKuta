from __future__ import annotations

import random

from backend.app.core.base import BaseGenerator, BaseProblem, ProblemDifficulty


class PrecalcMatricesGenerator(BaseGenerator):
    generator_id = "precalculus.matrices"
    name = "Matrices (Operations, Determinants, Inverses)"
    category = "Precalculus"
    standards = ["CCSS.MATH.CONTENT.HSN.VM.C.8", "CCSS.MATH.CONTENT.HSN.VM.C.10"]

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
        """Mild: 2x2 determinants with clear step-by-step ad - bc calculation."""
        a = rng.choice([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
        b = rng.choice([-6, -4, -3, -1, 1, 2, 3, 4, 5])
        c = rng.choice([-5, -3, -2, 1, 2, 3, 4, 5])
        d = rng.choice([-6, -4, -2, 1, 2, 3, 5, 6])

        det = a * d - b * c
        eq_typst = f"mat({a}, {b}; {c}, {d})"
        ans_typst = f"{det}"

        steps = [
            "Recall 2x2 determinant formula: $ det mat(a, b; c, d) = a d - b c $",
            f"Identify matrix entries: $ a = {a}, b = {b}, c = {c}, d = {d} $",
            f"Compute main diagonal product: $ ({a}) dot ({d}) = {a*d} $",
            f"Compute anti-diagonal product: $ ({b}) dot ({c}) = {b*c} $",
            f"Subtract: $ ({a*d}) - ({b*c}) = {ans_typst} $"
        ]

        distractors = [
            f"{a*d + b*c}",
            f"{b*c - a*d}",
            f"{det + (4 if det >= 0 else -4)}"
        ]

        return BaseProblem(
            id=f"pcalc_mat_mild_{problem_idx}",
            prompt_text="Evaluate the determinant of each 2x2 matrix.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MILD,
            standards=self.standards
        )

    def _generate_medium(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Medium: Matrix operations (scalar multiplication/addition or matrix multiplication)."""
        subtype = rng.choice(["add_scale", "multiply"])

        if subtype == "add_scale":
            k = rng.choice([2, 3, -2])
            a11, a12 = rng.choice([-3, -2, 1, 2, 3]), rng.choice([-2, 0, 2, 4])
            a21, a22 = rng.choice([-4, 1, 3, 5]), rng.choice([-1, 2, -3, 3])

            b11, b12 = rng.choice([-2, 1, 2, 3]), rng.choice([-3, -1, 2, 4])
            b21, b22 = rng.choice([1, 2, -2, 4]), rng.choice([-2, 3, 1, 5])

            c11 = k * a11 + b11
            c12 = k * a12 + b12
            c21 = k * a21 + b21
            c22 = k * a22 + b22

            eq_typst = f"{k} mat({a11}, {a12}; {a21}, {a22}) + mat({b11}, {b12}; {b21}, {b22})"
            ans_typst = f"mat({c11}, {c12}; {c21}, {c22})"

            scaled_typst = f"mat({k*a11}, {k*a12}; {k*a21}, {k*a22})"
            steps = [
                f"Distribute scalar {k} into the first matrix: $ {k} mat({a11}, {a12}; {a21}, {a22}) = {scaled_typst} $",
                f"Add corresponding elements: $ {scaled_typst} + mat({b11}, {b12}; {b21}, {b22}) $",
                f"Compute each element: $ mat(({k*a11}) + ({b11}), ({k*a12}) + ({b12}); ({k*a21}) + ({b21}), ({k*a22}) + ({b22})) $",
                f"Result: $ {ans_typst} $"
            ]

            distractors = [
                f"mat({k*(a11+b11)}, {k*(a12+b12)}; {k*(a21+b21)}, {k*(a22+b22)})",
                f"mat({c11 + 1}, {c12 - 1}; {c21 - 2}, {c22 + 2})",
                f"mat({a11 + b11}, {a12 + b12}; {a21 + b21}, {a22 + b22})"
            ]

            prompt = "Perform the indicated matrix operations."
        else:
            # 2x2 Matrix Multiplication A * B
            a11, a12 = rng.choice([-2, -1, 1, 2, 3]), rng.choice([-1, 0, 2, 3])
            a21, a22 = rng.choice([-3, 1, 2, 4]), rng.choice([-2, 1, 2, 3])

            b11, b12 = rng.choice([-2, 1, 2, 3]), rng.choice([-1, 2, 0, 3])
            b21, b22 = rng.choice([-1, 2, 1, -2]), rng.choice([1, 2, -2, 3])

            c11 = a11 * b11 + a12 * b21
            c12 = a11 * b12 + a12 * b22
            c21 = a21 * b11 + a22 * b21
            c22 = a21 * b12 + a22 * b22

            eq_typst = f"mat({a11}, {a12}; {a21}, {a22}) dot mat({b11}, {b12}; {b21}, {b22})"
            ans_typst = f"mat({c11}, {c12}; {c21}, {c22})"

            steps = [
                "Apply matrix multiplication formula (row dot column):",
                f"Row 1 dot Col 1: $ ({a11})({b11}) + ({a12})({b21}) = {a11*b11} + {a12*b21} = {c11} $",
                f"Row 1 dot Col 2: $ ({a11})({b12}) + ({a12})({b22}) = {a11*b12} + {a12*b22} = {c12} $",
                f"Row 2 dot Col 1: $ ({a21})({b11}) + ({a22})({b21}) = {a21*b11} + {a22*b21} = {c21} $",
                f"Row 2 dot Col 2: $ ({a21})({b12}) + ({a22})({b22}) = {a21*b12} + {a22*b22} = {c22} $",
                f"Assemble product matrix: $ {ans_typst} $"
            ]

            distractors = [
                f"mat({a11*b11}, {a12*b12}; {a21*b21}, {a22*b22})",
                f"mat({c11 + 2}, {c12}; {c21}, {c22 - 2})",
                f"mat({c21}, {c22}; {c11}, {c12})"
            ]

            prompt = "Find the matrix product."

        return BaseProblem(
            id=f"pcalc_mat_med_{problem_idx}",
            prompt_text=prompt,
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.MEDIUM,
            standards=self.standards
        )

    def _generate_spicy(self, rng: random.Random, problem_idx: int) -> BaseProblem:
        """Spicy: 2x2 matrix inverse A^(-1) = (1/det) * mat(d, -b; -c, a), checking det != 0."""
        # Carefully generate matrices with clean determinants (+/-1, +/-2, +/-3)
        candidate_matrices = [
            (3, 1, 5, 2),   # det = 6 - 5 = 1
            (2, 5, 1, 3),   # det = 6 - 5 = 1
            (4, 3, 3, 2),   # det = 8 - 9 = -1
            (5, 2, 2, 1),   # det = 5 - 4 = 1
            (1, 2, 3, 4),   # det = 4 - 6 = -2
            (3, 2, 2, 2),   # det = 6 - 4 = 2
            (2, 1, 4, 3),   # det = 6 - 4 = 2
            (3, -1, -2, 1), # det = 3 - 2 = 1
            (4, 1, 2, 1),   # det = 4 - 2 = 2
            (2, 3, 1, 2),   # det = 4 - 3 = 1
            (1, -2, -1, 3), # det = 3 - 2 = 1
            (3, 4, 1, 2),   # det = 6 - 4 = 2
            (2, 4, 1, 3),   # det = 6 - 4 = 2
            (5, 3, 3, 2),   # det = 10 - 9 = 1
            (4, 2, 3, 2),   # det = 8 - 6 = 2
        ]

        a, b, c, d = rng.choice(candidate_matrices)
        det = a * d - b * c

        eq_typst = f"mat({a}, {b}; {c}, {d})"

        if det == 1:
            ans_typst = f"mat({d}, {-b}; {-c}, {a})"
        elif det == -1:
            ans_typst = f"mat({-d}, {b}; {c}, {-a})"
        else:
            ans_typst = f"1/({det}) mat({d}, {-b}; {-c}, {a})"

        steps = [
            "Recall inverse formula: $ A^(-1) = 1/(det(A)) mat(d, -b; -c, a) $",
            f"Calculate determinant: $ det(A) = ({a})({d}) - ({b})({c}) = {a*d} - ({b*c}) = {det} $",
            f"Verify invertibility: Since $det(A) = {det} != 0$, the matrix is invertible.",
            f"Form the adjugate matrix: swap diagonal entries and negate off-diagonal entries: $ mat({d}, {-b}; {-c}, {a}) $",
            f"Multiply by $1/({det})$: $ {ans_typst} $"
        ]

        distractors = [
            f"mat({a}, {c}; {b}, {d})",
            f"mat({d}, {b}; {c}, {a})",
            f"1/({det}) mat({a}, {-b}; {-c}, {d})"
        ]

        return BaseProblem(
            id=f"pcalc_mat_spicy_{problem_idx}",
            prompt_text="Find the inverse of the 2x2 matrix, if it exists.",
            equation_typst=eq_typst,
            answer_typst=ans_typst,
            steps_typst=steps,
            distractors=distractors,
            difficulty=ProblemDifficulty.SPICY,
            standards=self.standards
        )
