from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import sympy as sp


class ErrorType(str, Enum):
    NONE = "none"
    SIGN_ERROR = "sign_error"
    DISTRIBUTION_ERROR = "distribution_error"
    ARITHMETIC_ERROR = "arithmetic_error"
    CONCEPTUAL_ERROR = "conceptual_error"


@dataclass
class StepVerification:
    step_index: int
    raw_step: str
    is_valid: bool
    simplified_delta: str
    error_type: ErrorType = ErrorType.NONE
    diagnostic_message: str = ""


@dataclass
class ProblemGradingReport:
    problem_id: str
    total_steps: int
    correct_steps_count: int
    first_failure_step: Optional[int]
    error_classification: ErrorType
    partial_credit_score: float  # 0.0 to 1.0
    step_details: List[StepVerification]
    final_answer_correct: bool


class CASStepVerifier:
    """Line-by-line algebraic equivalence verifier using SymPy with misconception classification."""

    def __init__(self) -> None:
        self.x = sp.Symbol('x')

    def parse_latex_to_sympy(self, step_str: str) -> sp.Expr | Tuple[sp.Expr, sp.Expr]:
        """Convert a LaTeX / math step into SymPy expression(s)."""
        s = step_str.replace("$", "").strip()

        # Handle common LaTeX tokens
        s = re.sub(r'\\frac\{([^\}]+)\}\{([^\}]+)\}', r'(\1)/(\2)', s)
        s = re.sub(r'\\cdot', r'*', s)
        s = re.sub(r'\\pm', r'+', s)
        s = re.sub(r'\\times', r'*', s)
        s = s.replace("{", "(").replace("}", ")")

        # Check for equation (=)
        if "=" in s:
            parts = s.split("=")
            lhs_str = parts[0].strip()
            rhs_str = parts[1].strip()
            lhs = sp.sympify(lhs_str)
            rhs = sp.sympify(rhs_str)
            return (lhs, rhs)
        else:
            return sp.sympify(s)

    def extract_difference_expr(self, step_obj: sp.Expr | Tuple[sp.Expr, sp.Expr]) -> sp.Expr:
        """Normalize an equation or expression into an invariant difference expression."""
        if isinstance(step_obj, tuple):
            lhs, rhs = step_obj
            return lhs - rhs
        return step_obj

    def are_equivalent(
        self,
        step_prev: sp.Expr | Tuple[sp.Expr, sp.Expr],
        step_curr: sp.Expr | Tuple[sp.Expr, sp.Expr],
    ) -> Tuple[bool, sp.Expr]:
        """Check if step_curr is an algebraically valid transition from step_prev."""
        expr_prev = self.extract_difference_expr(step_prev)
        expr_curr = self.extract_difference_expr(step_curr)

        # Delta between expressions
        delta = sp.simplify(expr_curr - expr_prev)
        if delta == 0:
            return True, delta

        # If both are equations (expr = 0), check if one is a non-zero scalar multiple of the other
        # e.g., 2x + 4 = 0 is equivalent to x + 2 = 0
        try:
            ratio = sp.simplify(expr_curr / expr_prev)
            if ratio.is_constant() and ratio != 0:
                return True, sp.Integer(0)
        except Exception:
            pass

        return False, delta

    def classify_error(
        self,
        prev_expr: sp.Expr,
        curr_expr: sp.Expr,
        delta: sp.Expr,
        prev_raw: str = "",
        curr_raw: str = "",
    ) -> Tuple[ErrorType, str]:
        """Classify student error based on algebraic structure of delta and expression syntax."""
        # Check for distribution error (e.g. 3*(x+4) -> 3x+4 where parentheses were dropped without multiplying)
        if ("(" in prev_raw or ")" in prev_raw) and ("(" not in curr_raw or ")" not in curr_raw):
            # Check if leading coefficients match (e.g. 3x == 3x) but delta is nonzero constant
            try:
                prev_poly = sp.Poly(prev_expr, self.x)
                curr_poly = sp.Poly(curr_expr, self.x)
                if prev_poly.degree() == curr_poly.degree() and prev_poly.LC() == curr_poly.LC():
                    return ErrorType.DISTRIBUTION_ERROR, "Incomplete distribution: factor not applied to all terms in parentheses"
            except Exception:
                pass

        # Sign error check
        if sp.simplify(curr_expr + prev_expr) == 0:
            return ErrorType.SIGN_ERROR, "Total sign inversion across equation"

        # Check if error is pure arithmetic (delta is a constant number, no variable)
        if not delta.has(self.x):
            return ErrorType.ARITHMETIC_ERROR, f"Arithmetic calculation discrepancy of {delta}"

        try:
            prev_poly = sp.Poly(prev_expr, self.x)
            curr_poly = sp.Poly(curr_expr, self.x)

            if prev_poly.degree() == curr_poly.degree():
                if prev_poly.LC() == curr_poly.LC():
                    return ErrorType.DISTRIBUTION_ERROR, "Incomplete distribution or operation across terms"
                else:
                    return ErrorType.CONCEPTUAL_ERROR, "Coefficient balance violation"
        except Exception:
            pass

        return ErrorType.CONCEPTUAL_ERROR, "Invalid algebraic transition"

    def verify_solution_steps(
        self,
        problem_id: str,
        steps: List[str],
        expected_roots: Optional[List[Any]] = None,
    ) -> ProblemGradingReport:
        """Verify step-by-step handwriting transcription, find failure point, and award partial credit."""
        if not steps:
            return ProblemGradingReport(
                problem_id=problem_id,
                total_steps=0,
                correct_steps_count=0,
                first_failure_step=None,
                error_classification=ErrorType.NONE,
                partial_credit_score=0.0,
                step_details=[],
                final_answer_correct=False,
            )

        parsed_steps: List[Any] = []
        parse_errors: Dict[int, str] = {}

        for idx, s in enumerate(steps):
            try:
                parsed = self.parse_latex_to_sympy(s)
                parsed_steps.append(parsed)
            except Exception as e:
                parsed_steps.append(None)
                parse_errors[idx] = str(e)

        step_details: List[StepVerification] = []
        first_failure: Optional[int] = None
        error_class = ErrorType.NONE

        # First step is usually the problem statement, considered valid baseline
        step_details.append(
            StepVerification(
                step_index=1,
                raw_step=steps[0],
                is_valid=True,
                simplified_delta="0",
                error_type=ErrorType.NONE,
                diagnostic_message="Given equation / starting step",
            )
        )

        for i in range(1, len(steps)):
            prev = parsed_steps[i - 1]
            curr = parsed_steps[i]

            if prev is None or curr is None:
                step_details.append(
                    StepVerification(
                        step_index=i + 1,
                        raw_step=steps[i],
                        is_valid=False,
                        simplified_delta="parse_error",
                        error_type=ErrorType.CONCEPTUAL_ERROR,
                        diagnostic_message=f"Syntax parsing failure: {parse_errors.get(i, 'unrecognized syntax')}",
                    )
                )
                if first_failure is None:
                    first_failure = i + 1
                    error_class = ErrorType.CONCEPTUAL_ERROR
                continue

            eq, delta = self.are_equivalent(prev, curr)
            if eq:
                step_details.append(
                    StepVerification(
                        step_index=i + 1,
                        raw_step=steps[i],
                        is_valid=True,
                        simplified_delta=str(delta),
                        error_type=ErrorType.NONE,
                        diagnostic_message="Valid algebraic transformation",
                    )
                )
            else:
                prev_diff = self.extract_difference_expr(prev)
                curr_diff = self.extract_difference_expr(curr)
                etype, diag = self.classify_error(
                    prev_diff,
                    curr_diff,
                    delta,
                    prev_raw=steps[i - 1],
                    curr_raw=steps[i],
                )

                step_details.append(
                    StepVerification(
                        step_index=i + 1,
                        raw_step=steps[i],
                        is_valid=False,
                        simplified_delta=str(delta),
                        error_type=etype,
                        diagnostic_message=diag,
                    )
                )
                if first_failure is None:
                    first_failure = i + 1
                    error_class = etype

        total_transitions = max(1, len(steps) - 1)
        valid_transitions = sum(1 for s in step_details[1:] if s.is_valid)
        score = valid_transitions / total_transitions

        # Check final answer correctness
        final_answer_correct = (first_failure is None)

        return ProblemGradingReport(
            problem_id=problem_id,
            total_steps=len(steps),
            correct_steps_count=valid_transitions + 1,
            first_failure_step=first_failure,
            error_classification=error_class,
            partial_credit_score=round(score, 2),
            step_details=step_details,
            final_answer_correct=final_answer_correct,
        )
