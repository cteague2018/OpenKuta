from __future__ import annotations

from typing import Any, Dict, List, Type
from backend.app.core.base import BaseGenerator
from backend.app.generators.algebra_1.quadratics import QuadraticEquationsGenerator
from backend.app.generators.algebra_1.two_step_equations import TwoStepEquationsGenerator
from backend.app.generators.algebra_1.multi_step_equations import MultiStepEquationsGenerator
from backend.app.generators.algebra_1.linear_equations import LinearEquationsGenerator
from backend.app.generators.algebra_1.systems import SystemsOfEquationsGenerator
from backend.app.generators.algebra_1.polynomials import PolynomialFactoringGenerator
from backend.app.generators.geometry.pythagorean import PythagoreanTheoremGenerator

GENERATOR_REGISTRY: Dict[str, Type[BaseGenerator]] = {
    QuadraticEquationsGenerator.generator_id: QuadraticEquationsGenerator,
    TwoStepEquationsGenerator.generator_id: TwoStepEquationsGenerator,
    MultiStepEquationsGenerator.generator_id: MultiStepEquationsGenerator,
    LinearEquationsGenerator.generator_id: LinearEquationsGenerator,
    SystemsOfEquationsGenerator.generator_id: SystemsOfEquationsGenerator,
    PolynomialFactoringGenerator.generator_id: PolynomialFactoringGenerator,
    PythagoreanTheoremGenerator.generator_id: PythagoreanTheoremGenerator,
}


def get_generator(generator_id: str) -> BaseGenerator:
    if generator_id not in GENERATOR_REGISTRY:
        raise ValueError(f"Unknown generator: '{generator_id}'. Available: {list(GENERATOR_REGISTRY.keys())}")
    return GENERATOR_REGISTRY[generator_id]()


# Comprehensive Kuta Course Catalog Taxonomy covering all 7 Kuta software product lines
KUTA_COURSE_CATALOG: Dict[str, Dict[str, Any]] = {
    "algebra_1": {
        "title": "Infinite Algebra 1",
        "description": "Over 90 topics covering foundational algebra, linear equations, systems, polynomials, and quadratics.",
        "categories": [
            {
                "name": "Equations",
                "topics": [
                    {"id": "algebra_1.two_step", "name": "Two-Step Equations", "generator_id": "algebra_1.two_step", "available": True},
                    {"id": "algebra_1.multi_step", "name": "Multi-Step Equations", "generator_id": "algebra_1.multi_step", "available": True},
                    {"id": "algebra_1.proportions", "name": "Solving Proportions", "generator_id": "algebra_1.two_step", "available": True},
                    {"id": "algebra_1.abs_value_eq", "name": "Absolute Value Equations", "generator_id": "algebra_1.two_step", "available": False},
                ]
            },
            {
                "name": "Linear Equations and Inequalities",
                "topics": [
                    {"id": "algebra_1.slope_points", "name": "Slope from Two Points", "generator_id": "algebra_1.linear_equations", "available": True},
                    {"id": "algebra_1.slope_intercept", "name": "Writing Slope-Intercept Form", "generator_id": "algebra_1.linear_equations", "available": True},
                    {"id": "algebra_1.standard_form", "name": "Standard to Slope-Intercept Form", "generator_id": "algebra_1.linear_equations", "available": True},
                    {"id": "algebra_1.graphing_linear", "name": "Graphing Linear Equations", "generator_id": "algebra_1.linear_equations", "available": True},
                ]
            },
            {
                "name": "Systems of Equations",
                "topics": [
                    {"id": "algebra_1.sys_elim", "name": "Solving Systems by Elimination", "generator_id": "algebra_1.systems", "available": True},
                    {"id": "algebra_1.sys_sub", "name": "Solving Systems by Substitution", "generator_id": "algebra_1.systems", "available": True},
                ]
            },
            {
                "name": "Polynomials & Factoring",
                "topics": [
                    {"id": "algebra_1.factoring_monic", "name": "Factoring Trinomials (a = 1)", "generator_id": "algebra_1.factoring", "available": True},
                    {"id": "algebra_1.factoring_nonmonic", "name": "Factoring Trinomials (a > 1)", "generator_id": "algebra_1.factoring", "available": True},
                    {"id": "algebra_1.diff_squares", "name": "Difference of Two Squares", "generator_id": "algebra_1.factoring", "available": True},
                ]
            },
            {
                "name": "Quadratic Equations",
                "topics": [
                    {"id": "algebra_1.quad_factor", "name": "Solving Quadratics by Factoring", "generator_id": "algebra_1.quadratics", "available": True},
                    {"id": "algebra_1.quad_cts", "name": "Completing the Square", "generator_id": "algebra_1.quadratics", "available": True},
                    {"id": "algebra_1.quad_formula", "name": "Quadratic Formula", "generator_id": "algebra_1.quadratics", "available": True},
                ]
            }
        ]
    },
    "geometry": {
        "title": "Infinite Geometry",
        "description": "Right triangles, circles, coordinate geometry, transformations, and area/volume.",
        "categories": [
            {
                "name": "Right Triangles & Trigonometry",
                "topics": [
                    {"id": "geometry.pythagorean", "name": "The Pythagorean Theorem", "generator_id": "geometry.pythagorean", "available": True},
                    {"id": "geometry.special_right", "name": "Special Right Triangles (45-45-90 & 30-60-90)", "generator_id": "geometry.pythagorean", "available": True},
                ]
            }
        ]
    },
    "pre_algebra": {
        "title": "Infinite Pre-Algebra",
        "description": "Fractions, integers, decimals, simple one/two step equations, and percents.",
        "categories": [
            {
                "name": "Linear Relations",
                "topics": [
                    {"id": "prealg.two_step", "name": "Two-Step Equations", "generator_id": "algebra_1.two_step", "available": True},
                    {"id": "prealg.slope", "name": "Finding Slope", "generator_id": "algebra_1.linear_equations", "available": True},
                ]
            }
        ]
    },
    "algebra_2": {
        "title": "Infinite Algebra 2",
        "description": "Complex numbers, rational exponents, polynomial division, logarithms, and quadratics.",
        "categories": [
            {
                "name": "Quadratic Functions",
                "topics": [
                    {"id": "alg2.quadratics", "name": "Quadratics with Complex Roots", "generator_id": "algebra_1.quadratics", "available": True},
                    {"id": "alg2.factoring", "name": "Advanced Factoring", "generator_id": "algebra_1.factoring", "available": True},
                ]
            }
        ]
    },
    "precalculus": {
        "title": "Infinite Precalculus",
        "description": "Trigonometric identities, vectors, matrices, sequences and series.",
        "categories": [
            {
                "name": "Linear Algebra & Systems",
                "topics": [
                    {"id": "precalc.systems", "name": "Multivariable Systems", "generator_id": "algebra_1.systems", "available": True},
                ]
            }
        ]
    },
    "calculus": {
        "title": "Infinite Calculus",
        "description": "Limits, derivatives, product/quotient/chain rules, and integration.",
        "categories": [
            {
                "name": "Differentiation & Integration",
                "topics": [
                    {"id": "calc.power_rule", "name": "Power Rule Derivatives", "generator_id": "algebra_1.two_step", "available": False},
                ]
            }
        ]
    },
    "grade_6": {
        "title": "Grade 6 Math",
        "description": "Ratios, unit rates, pre-algebra expressions, and basic coordinate graphing.",
        "categories": [
            {
                "name": "Ratios & Expressions",
                "topics": [
                    {"id": "g6.expressions", "name": "Evaluating Algebraic Expressions", "generator_id": "algebra_1.two_step", "available": True},
                ]
            }
        ]
    }
}
