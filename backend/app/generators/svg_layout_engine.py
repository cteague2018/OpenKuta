from __future__ import annotations

from typing import List

import sympy as sp

from backend.app.core.svg_layout import BBox, LineSegment, SVGCollisionSolver

__all__ = ["BBox", "LineSegment", "SVGCollisionSolver", "sample_function_singularity_aware"]


def sample_function_singularity_aware(
    expr: sp.Expr,
    var: sp.Symbol,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    base_samples: int = 200,
) -> List[float]:
    numer, denom = sp.together(expr).as_numer_denom()
    poles: List[float] = []
    if denom != 1:
        try:
            poles = [
                float(p.evalf())
                for p in sp.solveset(denom, var, domain=sp.S.Reals)
                if x_min <= float(p.evalf()) <= x_max
            ]
        except Exception:
            pass

    critical_points: List[float] = []
    try:
        deriv = sp.diff(expr, var)
        critical_points = [
            float(cp.evalf())
            for cp in sp.solveset(deriv, var, domain=sp.S.Reals)
            if x_min <= float(cp.evalf()) <= x_max
        ]
    except Exception:
        pass

    xs = [x_min + (x_max - x_min) * (i / base_samples) for i in range(base_samples + 1)]
    for p in poles:
        xs.extend([p - 1e-4, p + 1e-4])
    for cp in critical_points:
        xs.append(cp)

    return sorted(set(x for x in xs if x_min <= x <= x_max))
