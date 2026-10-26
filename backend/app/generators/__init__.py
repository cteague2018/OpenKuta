from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Type

from backend.app.core.base import BaseGenerator
from backend.app.generators.algebra_1.absolute_value import (
    AbsoluteValueEquationsGenerator,
    GraphingAbsoluteValueGenerator,
)
from backend.app.generators.algebra_1.distributive_property import (
    DistributivePropertyGenerator,
)
from backend.app.generators.algebra_1.exponent_rules import (
    ExponentRulesGenerator,
)
from backend.app.generators.algebra_1.exponential_functions import (
    ExponentialFunctionsGenerator,
    GraphingExponentialGenerator,
)

# New High-Priority Classroom Generators
from backend.app.generators.algebra_1.inequalities import (
    GraphingInequalitiesGenerator,
    LinearInequalitiesGenerator,
)
from backend.app.generators.algebra_1.linear_equations import (
    GraphingLinearInequalitiesGenerator,
    GraphingLinesGenerator,
    LinearEquationsGenerator,
    SlopeGenerator,
    WritingLinearEquationsGenerator,
)
from backend.app.generators.algebra_1.literal_equations import (
    LiteralEquationsGenerator,
)
from backend.app.generators.algebra_1.multi_step_equations import (
    MultiStepEquationsGenerator,
)
from backend.app.generators.algebra_1.polynomials import (
    PolynomialAddSubGenerator,
    PolynomialFactoringGenerator,
    PolynomialMultiplyGenerator,
)

# Algebra 1 Generators
from backend.app.generators.algebra_1.quadratics import (
    GraphingQuadraticsGenerator,
    QuadraticEquationsGenerator,
    QuadraticsCompletingSquareGenerator,
    QuadraticsDiscriminantGenerator,
    QuadraticsFactoringGenerator,
    QuadraticsFormulaGenerator,
    QuadraticsSquareRootsGenerator,
)
from backend.app.generators.algebra_1.scientific_notation import (
    ScientificNotationGenerator,
)
from backend.app.generators.algebra_1.systems import (
    SystemsEliminationGenerator,
    SystemsGraphingGenerator,
    SystemsInequalitiesGenerator,
    SystemsOfEquationsGenerator,
    SystemsSubstitutionGenerator,
)
from backend.app.generators.algebra_1.two_step_equations import (
    TwoStepEquationsGenerator,
)
from backend.app.generators.algebra_1.verbal_expressions import (
    VerbalExpressionsGenerator,
)
from backend.app.generators.algebra_1.word_problems import (
    Algebra1WordProblemsGenerator,
)

# Algebra 2 Generators
from backend.app.generators.algebra_2.complex_numbers import (
    Algebra2ComplexNumbersGenerator,
)
from backend.app.generators.algebra_2.general_functions import (
    GeneralFunctionsGenerator,
)
from backend.app.generators.algebra_2.log_properties import (
    LogPropertiesGenerator,
)
from backend.app.generators.algebra_2.logarithms import (
    Algebra2LogarithmsGenerator,
)
from backend.app.generators.algebra_2.polynomial_division import (
    PolynomialDivisionGenerator,
)
from backend.app.generators.algebra_2.probability_statistics import (
    ProbabilityStatisticsGenerator,
)
from backend.app.generators.algebra_2.radicals import (
    Algebra2RadicalsGenerator,
)
from backend.app.generators.algebra_2.rational_expressions import (
    Algebra2RationalExpressionsGenerator,
)
from backend.app.generators.calculus.derivatives import (
    CalculusDerivativesGenerator,
    CalculusTangentLinesGenerator,
)
from backend.app.generators.calculus.diff_eq import (
    CalculusDiffEqGenerator,
)

# Calculus Generators
from backend.app.generators.calculus.implicit_diff import (
    ImplicitDifferentiationGenerator,
)
from backend.app.generators.calculus.integrals import (
    CalculusIntegralsGenerator,
)
from backend.app.generators.calculus.lhopital import (
    LhopitalGenerator,
)
from backend.app.generators.calculus.limits import (
    CalculusLimitsGenerator,
)
from backend.app.generators.calculus.riemann_sums import (
    CalculusRiemannSumsGenerator,
)
from backend.app.generators.curriculum_topics import build_topic_generator_registry
from backend.app.generators.geometry.angles_lines import (
    GeometryAnglesLinesGenerator,
)
from backend.app.generators.geometry.area_volume import (
    GeometryAreaVolumeGenerator,
)
from backend.app.generators.geometry.circles import (
    GeometryCirclesGenerator,
)
from backend.app.generators.geometry.coordinate_geometry import (
    CoordinateGeometryGenerator,
)

# Geometry Generators
from backend.app.generators.geometry.pythagorean import (
    PythagoreanTheoremGenerator,
)
from backend.app.generators.geometry.special_right_triangles import (
    SpecialRightTrianglesGenerator,
)
from backend.app.generators.geometry.triangles import (
    GeometryTrianglesGenerator,
)
from backend.app.generators.geometry.trigonometry import (
    GeometryTrigonometryGenerator,
)
from backend.app.generators.grade_6.factors_multiples import (
    Grade6FactorsMultiplesGenerator,
)
from backend.app.generators.grade_6.fractions_decimals import (
    Grade6FractionsDecimalsGenerator,
    RationalNumbersArithmeticGenerator,
)
from backend.app.generators.grade_6.integers import (
    Grade6IntegersGenerator,
)
from backend.app.generators.grade_6.one_step import (
    Grade6OneStepGenerator,
)
from backend.app.generators.grade_6.order_of_operations import (
    Grade6OrderOfOperationsGenerator,
)
from backend.app.generators.grade_6.percents import (
    Grade6PercentsGenerator,
)

# Grade 6 Generators
from backend.app.generators.grade_6.ratios_rates import (
    Grade6RatiosRatesGenerator,
)
from backend.app.generators.grade_6.statistics import (
    Grade6StatisticsGenerator,
)
from backend.app.generators.precalculus.matrices import (
    PrecalcMatricesGenerator,
)
from backend.app.generators.precalculus.polar_conics import (
    PrecalcPolarConicsGenerator,
)
from backend.app.generators.precalculus.sequences import (
    PrecalcSequencesGenerator,
)
from backend.app.generators.precalculus.triangle_trig import (
    TriangleTrigGenerator,
)
from backend.app.generators.precalculus.trig_advanced import (
    PrecalcTrigGenerator,
)

# Precalculus Generators
from backend.app.generators.precalculus.vectors import (
    PrecalcVectorsGenerator,
)

GENERATOR_REGISTRY: Dict[str, Type[BaseGenerator]] = {
    # Algebra 1
    QuadraticEquationsGenerator.generator_id: QuadraticEquationsGenerator,
    QuadraticsFactoringGenerator.generator_id: QuadraticsFactoringGenerator,
    QuadraticsSquareRootsGenerator.generator_id: QuadraticsSquareRootsGenerator,
    QuadraticsFormulaGenerator.generator_id: QuadraticsFormulaGenerator,
    QuadraticsDiscriminantGenerator.generator_id: QuadraticsDiscriminantGenerator,
    QuadraticsCompletingSquareGenerator.generator_id: QuadraticsCompletingSquareGenerator,
    TwoStepEquationsGenerator.generator_id: TwoStepEquationsGenerator,
    MultiStepEquationsGenerator.generator_id: MultiStepEquationsGenerator,
    LinearEquationsGenerator.generator_id: LinearEquationsGenerator,
    SlopeGenerator.generator_id: SlopeGenerator,
    GraphingLinesGenerator.generator_id: GraphingLinesGenerator,
    WritingLinearEquationsGenerator.generator_id: WritingLinearEquationsGenerator,
    GraphingLinearInequalitiesGenerator.generator_id: GraphingLinearInequalitiesGenerator,
    SystemsOfEquationsGenerator.generator_id: SystemsOfEquationsGenerator,
    SystemsGraphingGenerator.generator_id: SystemsGraphingGenerator,
    SystemsSubstitutionGenerator.generator_id: SystemsSubstitutionGenerator,
    SystemsEliminationGenerator.generator_id: SystemsEliminationGenerator,
    SystemsInequalitiesGenerator.generator_id: SystemsInequalitiesGenerator,
    PolynomialFactoringGenerator.generator_id: PolynomialFactoringGenerator,
    PolynomialAddSubGenerator.generator_id: PolynomialAddSubGenerator,
    PolynomialMultiplyGenerator.generator_id: PolynomialMultiplyGenerator,
    LinearInequalitiesGenerator.generator_id: LinearInequalitiesGenerator,
    GraphingInequalitiesGenerator.generator_id: GraphingInequalitiesGenerator,
    GraphingQuadraticsGenerator.generator_id: GraphingQuadraticsGenerator,
    GraphingAbsoluteValueGenerator.generator_id: GraphingAbsoluteValueGenerator,
    GraphingExponentialGenerator.generator_id: GraphingExponentialGenerator,
    RationalNumbersArithmeticGenerator.generator_id: RationalNumbersArithmeticGenerator,
    CalculusTangentLinesGenerator.generator_id: CalculusTangentLinesGenerator,
    ExponentRulesGenerator.generator_id: ExponentRulesGenerator,
    VerbalExpressionsGenerator.generator_id: VerbalExpressionsGenerator,
    AbsoluteValueEquationsGenerator.generator_id: (
        AbsoluteValueEquationsGenerator
    ),
    DistributivePropertyGenerator.generator_id: DistributivePropertyGenerator,
    LiteralEquationsGenerator.generator_id: LiteralEquationsGenerator,
    Algebra1WordProblemsGenerator.generator_id: Algebra1WordProblemsGenerator,
    ScientificNotationGenerator.generator_id: ScientificNotationGenerator,
    ExponentialFunctionsGenerator.generator_id: (
        ExponentialFunctionsGenerator
    ),

    # Geometry
    PythagoreanTheoremGenerator.generator_id: PythagoreanTheoremGenerator,
    GeometryAnglesLinesGenerator.generator_id: GeometryAnglesLinesGenerator,
    GeometryTrianglesGenerator.generator_id: GeometryTrianglesGenerator,
    GeometryTrigonometryGenerator.generator_id: GeometryTrigonometryGenerator,
    GeometryCirclesGenerator.generator_id: GeometryCirclesGenerator,
    GeometryAreaVolumeGenerator.generator_id: GeometryAreaVolumeGenerator,
    SpecialRightTrianglesGenerator.generator_id: SpecialRightTrianglesGenerator,
    CoordinateGeometryGenerator.generator_id: CoordinateGeometryGenerator,

    # Algebra 2
    Algebra2ComplexNumbersGenerator.generator_id: (
        Algebra2ComplexNumbersGenerator
    ),
    Algebra2LogarithmsGenerator.generator_id: Algebra2LogarithmsGenerator,
    Algebra2RationalExpressionsGenerator.generator_id: (
        Algebra2RationalExpressionsGenerator
    ),
    Algebra2RadicalsGenerator.generator_id: Algebra2RadicalsGenerator,
    LogPropertiesGenerator.generator_id: LogPropertiesGenerator,
    PolynomialDivisionGenerator.generator_id: PolynomialDivisionGenerator,
    GeneralFunctionsGenerator.generator_id: GeneralFunctionsGenerator,
    ProbabilityStatisticsGenerator.generator_id: (
        ProbabilityStatisticsGenerator
    ),

    # Precalculus
    PrecalcVectorsGenerator.generator_id: PrecalcVectorsGenerator,
    PrecalcMatricesGenerator.generator_id: PrecalcMatricesGenerator,
    PrecalcTrigGenerator.generator_id: PrecalcTrigGenerator,
    PrecalcSequencesGenerator.generator_id: PrecalcSequencesGenerator,
    PrecalcPolarConicsGenerator.generator_id: PrecalcPolarConicsGenerator,
    TriangleTrigGenerator.generator_id: TriangleTrigGenerator,

    # Calculus
    ImplicitDifferentiationGenerator.generator_id: (
        ImplicitDifferentiationGenerator
    ),
    CalculusDerivativesGenerator.generator_id: CalculusDerivativesGenerator,
    CalculusLimitsGenerator.generator_id: CalculusLimitsGenerator,
    CalculusIntegralsGenerator.generator_id: CalculusIntegralsGenerator,
    CalculusDiffEqGenerator.generator_id: CalculusDiffEqGenerator,
    CalculusRiemannSumsGenerator.generator_id: CalculusRiemannSumsGenerator,
    LhopitalGenerator.generator_id: LhopitalGenerator,

    # Grade 6
    Grade6RatiosRatesGenerator.generator_id: Grade6RatiosRatesGenerator,
    Grade6PercentsGenerator.generator_id: Grade6PercentsGenerator,
    Grade6FractionsDecimalsGenerator.generator_id: (
        Grade6FractionsDecimalsGenerator
    ),
    Grade6FactorsMultiplesGenerator.generator_id: (
        Grade6FactorsMultiplesGenerator
    ),
    Grade6OneStepGenerator.generator_id: Grade6OneStepGenerator,
    Grade6StatisticsGenerator.generator_id: Grade6StatisticsGenerator,
    Grade6OrderOfOperationsGenerator.generator_id: Grade6OrderOfOperationsGenerator,
    Grade6IntegersGenerator.generator_id: Grade6IntegersGenerator,
}

_BASE_GENERATOR_REGISTRY: Dict[str, Type[BaseGenerator]] = dict(GENERATOR_REGISTRY)

# Comprehensive Course Catalog Taxonomy covering all 7 curriculum tiers
_CATALOG_PATH = Path(__file__).resolve().parent / "catalog_data.json"
with open(_CATALOG_PATH, "r", encoding="utf-8") as _f:
    COURSE_CATALOG: Dict[str, Dict[str, Any]] = json.load(_f)

TOPIC_GENERATOR_REGISTRY: Dict[str, Type[BaseGenerator]] = build_topic_generator_registry(
    COURSE_CATALOG
)
GENERATOR_REGISTRY.update(TOPIC_GENERATOR_REGISTRY)


def get_generator(generator_id: str) -> BaseGenerator:
    if generator_id not in GENERATOR_REGISTRY:
        raise ValueError(
            f"Unknown generator: '{generator_id}'. Available: "
            f"{list(GENERATOR_REGISTRY.keys())}"
        )
    return GENERATOR_REGISTRY[generator_id]()
