from __future__ import annotations

from typing import Tuple

import sympy as sp
from sympy.core.numbers import Rational
from sympy.printing.latex import LatexPrinter
from sympy.printing.str import StrPrinter


class SymPyToTypstPrinter(StrPrinter):
    def _print_Add(self, expr: sp.Add) -> str:
        terms = expr.args
        out = []
        for i, term in enumerate(terms):
            if i == 0:
                out.append(str(self._print(term)))
            else:
                coeff, rest = term.as_coeff_Mul()
                if coeff.is_negative:
                    pos_term = sp.Mul(-coeff, rest, evaluate=False) if coeff != -1 else rest
                    if rest == 1:
                        pos_term = -coeff
                    out.append(f" - {self._print(pos_term)}")
                else:
                    out.append(f" + {self._print(term)}")
        return "".join(out)

    def _print_Mul(self, expr: sp.Mul) -> str:
        coeff, args = expr.as_coeff_mul()
        if coeff == 1 and len(args) == 1:
            return str(self._print(args[0]))
        if coeff == -1 and len(args) == 1:
            inner = str(self._print(args[0]))
            return f"-({inner})" if args[0].is_Add else f"-{inner}"

        numer, denom = expr.as_numer_denom()
        if denom != 1:
            return f"frac({self._print(numer)}, {self._print(denom)})"

        formatted_factors = []
        for factor in expr.args:
            if factor == 1:
                continue
            s = str(self._print(factor))
            formatted_factors.append(f"({s})" if factor.is_Add else s)
        return " ".join(formatted_factors)

    def _print_Rational(self, expr: Rational) -> str:
        if expr.q == 1:
            return str(expr.p)
        return f"-frac({abs(expr.p)}, {expr.q})" if expr.p < 0 else f"frac({expr.p}, {expr.q})"

    def _print_Pow(self, expr: sp.Pow) -> str:
        base, exp = expr.base, expr.exp
        if exp == sp.Rational(1, 2):
            return f"sqrt({self._print(base)})"
        if isinstance(exp, Rational) and exp.p == 1 and exp.q > 2:
            return f"root({exp.q}, {self._print(base)})"
        if exp == -1:
            return f"frac(1, {self._print(base)})"

        base_str = str(self._print(base))
        if base.is_Add or base.is_Mul or (base.is_Number and base < 0) or isinstance(base, Rational):
            base_str = f"({base_str})"
        exp_str = str(self._print(exp))
        if exp.is_Add or exp.is_Mul or isinstance(exp, Rational):
            exp_str = f"({exp_str})"
        return f"{base_str}^{exp_str}"

    def _print_Equality(self, expr: sp.Equality) -> str:
        return f"{self._print(expr.lhs)} = {self._print(expr.rhs)}"

    def _print_StrictLessThan(self, expr: sp.StrictLessThan) -> str:
        return f"{self._print(expr.lhs)} < {self._print(expr.rhs)}"

    def _print_LessThan(self, expr: sp.LessThan) -> str:
        return f"{self._print(expr.lhs)} <= {self._print(expr.rhs)}"

    def _print_StrictGreaterThan(self, expr: sp.StrictGreaterThan) -> str:
        return f"{self._print(expr.lhs)} > {self._print(expr.rhs)}"

    def _print_GreaterThan(self, expr: sp.GreaterThan) -> str:
        return f"{self._print(expr.lhs)} >= {self._print(expr.rhs)}"

    def _print_Abs(self, expr: sp.Abs) -> str:
        return f"abs({self._print(expr.args[0])})"

    def _print_MatrixBase(self, expr: sp.MatrixBase) -> str:
        rows = []
        for i in range(expr.rows):
            row_items = [str(self._print(expr[i, j])) for j in range(expr.cols)]
            rows.append(", ".join(row_items))
        return f"mat({'; '.join(rows)})"


_TYPST_PRINTER = SymPyToTypstPrinter()
_LATEX_PRINTER = LatexPrinter({"mul_symbol": None, "fold_short_frac": False})


def serialize_math_ast(expr: sp.Basic) -> Tuple[str, str]:
    return f"${_TYPST_PRINTER.doprint(expr)}$", str(_LATEX_PRINTER.doprint(expr))
