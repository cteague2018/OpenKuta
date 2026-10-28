from __future__ import annotations

import functools
import inspect
import random
import re
from typing import Any, Callable, List, Optional, Set, TypeVar, Union, cast

import sympy as sp
from mpmath import mp  # type: ignore[import-untyped]
from pydantic import BaseModel
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

F = TypeVar("F", bound=Callable[..., Any])
mp.dps = 50
_TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


class VerificationError(Exception):
    pass


class VerifiedMathematicalCore(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    problem_ast: sp.Basic
    target_variable: Optional[sp.Symbol] = None
    expected_solutions: Union[Set[sp.Basic], sp.Basic]
    distractor_asts: List[sp.Basic] = []
    domain: Any = sp.S.Reals


def fast_numeric_equivalence(expr_a: sp.Basic, expr_b: sp.Basic, symbols: List[sp.Symbol]) -> bool:
    if expr_a == expr_b:
        return True
    try:
        diff = expr_a - expr_b
    except Exception:
        return False

    if not symbols:
        try:
            return bool(abs(complex(diff.evalf(30))) < 1e-20)
        except Exception:
            try:
                return bool(sp.simplify(diff) == 0)
            except Exception:
                return False

    probe_vectors = [
        {s: sp.Float("1.7320508075688772") + i * sp.Float("0.51123") for i, s in enumerate(symbols)},
        {s: sp.Float("-2.23606797749979") - i * sp.Float("0.31415") for i, s in enumerate(symbols)},
    ]
    valid_probes = 0
    for vec in probe_vectors:
        try:
            val = diff.subs(vec).evalf(30)
            if abs(complex(val)) > 1e-18:
                return False
            valid_probes += 1
        except (ZeroDivisionError, ValueError, TypeError, OverflowError):
            continue
    try:
        return bool(sp.simplify(sp.cancel(diff)) == 0 if valid_probes > 0 else False)
    except Exception:
        return False


def validate_forward_truth(core: VerifiedMathematicalCore) -> None:
    if isinstance(core.problem_ast, sp.Equality):
        if core.target_variable is None:
            raise VerificationError("Relational problem_ast requires target_variable.")
        computed = sp.solveset(core.problem_ast, core.target_variable, domain=core.domain)
        if isinstance(computed, sp.Intersection):
            for arg in computed.args:
                if isinstance(arg, sp.FiniteSet):
                    computed = arg
                    break

        expected = (
            sp.FiniteSet(*core.expected_solutions)
            if isinstance(core.expected_solutions, (set, list, tuple))
            else sp.FiniteSet(core.expected_solutions)
        )
        if computed != expected:
            # Check numerical/symbolic equivalence element-by-element if sizes match
            if isinstance(computed, sp.FiniteSet) and len(computed) == len(expected):
                syms = [core.target_variable]
                all_matched = True
                for c_item in computed:
                    if not any(fast_numeric_equivalence(c_item, e_item, syms) for e_item in expected):
                        all_matched = False
                        break
                if not all_matched:
                    raise VerificationError(f"Forward Solver Mismatch: expected {expected}, computed {computed}")
            else:
                raise VerificationError(f"Forward Solver Mismatch: expected {expected}, computed {computed}")

        # Extraneous root check
        diff = core.problem_ast.lhs - core.problem_ast.rhs
        sols = (
            core.expected_solutions
            if isinstance(core.expected_solutions, (set, list, tuple))
            else [core.expected_solutions]
        )
        for sol in sols:
            try:
                val = diff.subs(core.target_variable, sol).evalf()
                if abs(complex(val)) > 1e-9:
                    raise VerificationError(f"Extraneous root check failed for sol={sol}")
            except Exception:
                pass

        # Distractor collision assertion
        for d_ast in core.distractor_asts:
            for sol in sols:
                if d_ast == sol or fast_numeric_equivalence(d_ast, sol, [core.target_variable]):
                    raise VerificationError(
                        f"Distractor collision detected: distractor {d_ast} == solution {sol}"
                    )
    else:
        expected_expr = core.expected_solutions
        if isinstance(expected_expr, (set, list, tuple)):
            expected_free = set().union(
                *(getattr(e, "free_symbols", set()) for e in expected_expr)
            )
        else:
            expected_free = getattr(expected_expr, "free_symbols", set())
        syms = list(core.problem_ast.free_symbols.union(expected_free))
        if not fast_numeric_equivalence(core.problem_ast, expected_expr, syms):
            raise VerificationError("Expression equivalence failed.")
        for d_ast in core.distractor_asts:
            if fast_numeric_equivalence(d_ast, expected_expr, syms):
                raise VerificationError(
                    "Distractor collision detected: distractor matches expected solution"
                )


def normalize_typst_math(s: str) -> str:
    s = s.replace("$", "").strip()
    s = re.sub(r'log_([0-9a-zA-Z]+)\((.*?)\)', r'log(\2, \1)', s)
    s = re.sub(r'\bln\((.*?)\)', r'log(\1)', s)
    s = re.sub(r'\bfrac\((.*?),\s*(.*?)\)', r'((\1)/(\2))', s)
    s = re.sub(r'\broot\((.*?),\s*(.*?)\)', r'((\2)**(1/(\1)))', s)
    s = re.sub(r'\babs\((.*?)\)', r'Abs(\1)', s)
    s = s.replace("^", "**")
    return s


def synthesize_verified_core(problem: Any) -> Optional[VerifiedMathematicalCore]:
    eq_str = getattr(problem, "equation_typst", "")
    ans_str = getattr(problem, "answer_typst", "")
    prompt = getattr(problem, "prompt_text", "")
    if not eq_str or not ans_str:
        return None

    # Exclude transcendental equations, differential equations, limits, integrals, matrices, conics, angles, and approximations
    eq_lower = eq_str.lower()
    ans_lower = ans_str.lower()
    prompt_lower = prompt.lower()

    if any(k in eq_lower for k in ["dif ", "integral", "lim_", "mat(", "cases(", "log", "ln", "sin", "cos", "tan", "sec", "csc", "cot", "theta"]):
        return None
    if any(k in ans_lower for k in ["approx", "degree", "°", "pi", "log", "ln", "sin", "cos", "tan", "dif", "c_", "circle", "theta"]):
        return None
    if any(k in prompt_lower for k in ["differential equation", "tangent line", "derivative", "word problem", "approximate", "estimate", "evaluate", "conic", "rotat"]):
        return None

    clean_eq = normalize_typst_math(eq_str)
    clean_ans = normalize_typst_math(ans_str)

    try:
        if "=" in clean_eq and "=" in clean_ans:
            eq_lhs, eq_rhs = clean_eq.split("=", 1)
            ans_lhs, ans_rhs = clean_ans.split("=", 1)
            var_name = ans_lhs.strip()
            if var_name.isalpha():
                var = sp.Symbol(var_name)
                lhs_ast = parse_expr(eq_lhs, transformations=_TRANSFORMS)
                rhs_ast = parse_expr(eq_rhs, transformations=_TRANSFORMS)
                eq_ast = sp.Eq(lhs_ast, rhs_ast)

                ans_parts = [p.strip() for p in ans_rhs.split(",") if p.strip()]
                sol_asts = {
                    parse_expr(p, transformations=_TRANSFORMS)
                    for p in ans_parts
                }

                dist_asts = []
                for d in getattr(problem, "distractors", []):
                    d_clean = normalize_typst_math(d)
                    if "=" in d_clean:
                        _, d_val = d_clean.split("=", 1)
                        try:
                            d_parsed = parse_expr(
                                d_val.strip(), transformations=_TRANSFORMS
                            )
                            dist_asts.append(d_parsed)
                        except Exception:
                            pass

                return VerifiedMathematicalCore(
                    problem_ast=eq_ast,
                    target_variable=var,
                    expected_solutions=sol_asts,
                    distractor_asts=dist_asts,
                )
    except Exception:
        pass
    return None


def verify_mathematical_truth(max_retries: int = 15) -> Callable[[F], F]:
    def decorator(gen_func: F) -> F:
        @functools.wraps(gen_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            sig = inspect.signature(gen_func)
            for attempt in range(max_retries):
                call_kwargs = dict(kwargs)
                call_args = list(args)

                if attempt > 0:
                    base_seed = kwargs.get("seed", 42)
                    effective_seed = base_seed + (attempt * 9973)
                    if "seed" in sig.parameters or any(
                        p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
                    ):
                        call_kwargs["seed"] = effective_seed
                    elif len(call_args) > 1 and isinstance(call_args[1], random.Random):
                        call_args[1] = random.Random(effective_seed)
                    elif "rng" in call_kwargs and isinstance(call_kwargs["rng"], random.Random):
                        call_kwargs["rng"] = random.Random(effective_seed)

                try:
                    problem = gen_func(*call_args, **call_kwargs)
                except Exception as ex:
                    last_error = ex
                    continue

                if not hasattr(problem, "metadata"):
                    return problem

                core: Optional[VerifiedMathematicalCore] = problem.metadata.get("_verified_ast")
                if not core:
                    core = synthesize_verified_core(problem)

                if core:
                    try:
                        validate_forward_truth(core)
                        if "_verified_ast" in problem.metadata:
                            del problem.metadata["_verified_ast"]
                        return problem
                    except VerificationError as exc:
                        last_error = exc
                        continue
                else:
                    from backend.app.generators.validator import validate_problem_sanity

                    try:
                        validate_problem_sanity(problem)
                        return problem
                    except Exception as exc:
                        last_error = exc
                        continue
            raise RuntimeError(f"Generator {gen_func.__name__} failed verification: {last_error}")

        return cast(F, wrapper)

    return decorator
