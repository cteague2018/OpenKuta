from __future__ import annotations

import re

import sympy as sp
from sympy.printing.str import StrPrinter


def sympy_to_typst(expr: sp.Expr | int | float | str) -> str:
    """Convert a SymPy expression or number into clean Typst math format."""
    parsed: sp.Basic = sp.sympify(expr) if isinstance(expr, (int, float, str)) else expr

    # Convert to standard string and adjust operators for Typst math
    # Typst math syntax uses:
    # - ^ for powers: x^2
    # - / for fractions: (a)/(b)
    # - sqrt(x)
    # - standard symbols
    s = StrPrinter().doprint(parsed)

    # SymPy formats powers as ** -> convert to ^
    s = s.replace("**", "^")

    # SymPy prints multiplication with *, Typst math supports implicit or explicit
    # Replace * with space or omit between digits and letters
    # E.g., 2*x -> 2x, but 2*3 -> 2 dot 3
    # Replace integer * symbol: e.g. 5*x -> 5x, 5*(x + 1) -> 5(x + 1)
    s = re.sub(r'(\d+)\*([a-zA-Z\(])', r'\1\2', s)
    # Replace symbol * symbol: e.g. x*y -> x y
    s = re.sub(r'([a-zA-Z\)])\*([a-zA-Z\(])', r'\1 \2', s)

    # Fractions: if it's a Rational, format as a/b
    if isinstance(parsed, sp.Rational) and parsed.q != 1:
        if parsed.p < 0:
            return f"-({abs(parsed.p)}/{parsed.q})"
        return f"{parsed.p}/{parsed.q}"

    return str(s)


def format_polynomial_typst(
    poly_expr: sp.Expr | int | float | str, var: sp.Symbol = sp.Symbol('x')
) -> str:
    """Format polynomial nicely with proper spacing and signs for Typst math.

    ``poly_expr`` is sympified by :class:`sympy.Poly`, so plain numbers (e.g. a
    degenerate ``int`` coefficient expression) are accepted as well as ``Expr``.
    """
    poly = sp.Poly(poly_expr, var)
    coeffs = poly.all_coeffs()
    degree = poly.degree()

    terms: list[str] = []
    for i, c in enumerate(coeffs):
        p = degree - i
        if c == 0:
            continue

        c_abs = abs(c)
        sign = "-" if c < 0 else ("+" if terms else "")

        if p == 0:
            term_str = str(c_abs)
        elif p == 1:
            term_str = f"{c_abs if c_abs != 1 else ''}{var}"
        else:
            term_str = f"{c_abs if c_abs != 1 else ''}{var}^{p}"

        if sign == "+":
            terms.append(f"+ {term_str}")
        elif sign == "-":
            terms.append(f"- {term_str}" if terms else f"-{term_str}")
        else:
            terms.append(term_str)

    return " ".join(terms) if terms else "0"
