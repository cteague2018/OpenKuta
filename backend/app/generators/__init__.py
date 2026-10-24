from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Type

from backend.app.core.base import BaseGenerator

# Algebra 1 Generators
from backend.app.generators.algebra_1.quadratics import (
    QuadraticEquationsGenerator,
)
from backend.app.generators.algebra_1.two_step_equations import (
    TwoStepEquationsGenerator,
)
from backend.app.generators.algebra_1.multi_step_equations import (
    MultiStepEquationsGenerator,
)
from backend.app.generators.algebra_1.linear_equations import (
    LinearEquationsGenerator,
)
from backend.app.generators.algebra_1.systems import (
    SystemsOfEquationsGenerator,
)
from backend.app.generators.algebra_1.polynomials import (
    PolynomialFactoringGenerator,
)

# Geometry Generators
from backend.app.generators.geometry.pythagorean import (
    PythagoreanTheoremGenerator,
)
from backend.app.generators.geometry.angles_lines import (
    GeometryAnglesLinesGenerator,
)
from backend.app.generators.geometry.triangles import (
    GeometryTrianglesGenerator,
)
from backend.app.generators.geometry.trigonometry import (
    GeometryTrigonometryGenerator,
)
from backend.app.generators.geometry.circles import (
    GeometryCirclesGenerator,
)
from backend.app.generators.geometry.area_volume import (
    GeometryAreaVolumeGenerator,
)

# Algebra 2 Generators
from backend.app.generators.algebra_2.complex_numbers import (
    Algebra2ComplexNumbersGenerator,
)
from backend.app.generators.algebra_2.logarithms import (
    Algebra2LogarithmsGenerator,
)
from backend.app.generators.algebra_2.rational_expressions import (
    Algebra2RationalExpressionsGenerator,
)
from backend.app.generators.algebra_2.radicals import (
    Algebra2RadicalsGenerator,
)

# Precalculus Generators
from backend.app.generators.precalculus.vectors import (
    PrecalcVectorsGenerator,
)
from backend.app.generators.precalculus.matrices import (
    PrecalcMatricesGenerator,
)
from backend.app.generators.precalculus.trig_advanced import (
    PrecalcTrigGenerator,
)
from backend.app.generators.precalculus.sequences import (
    PrecalcSequencesGenerator,
)
from backend.app.generators.precalculus.polar_conics import (
    PrecalcPolarConicsGenerator,
)

# Calculus Generators
from backend.app.generators.calculus.implicit_diff import (
    ImplicitDifferentiationGenerator,
)
from backend.app.generators.calculus.derivatives import (
    CalculusDerivativesGenerator,
)
from backend.app.generators.calculus.limits import (
    CalculusLimitsGenerator,
)
from backend.app.generators.calculus.integrals import (
    CalculusIntegralsGenerator,
)
from backend.app.generators.calculus.diff_eq import (
    CalculusDiffEqGenerator,
)

# Grade 6 Generators
from backend.app.generators.grade_6.ratios_rates import (
    Grade6RatiosRatesGenerator,
)
from backend.app.generators.grade_6.percents import (
    Grade6PercentsGenerator,
)
from backend.app.generators.grade_6.fractions_decimals import (
    Grade6FractionsDecimalsGenerator,
)
from backend.app.generators.grade_6.factors_multiples import (
    Grade6FactorsMultiplesGenerator,
)
from backend.app.generators.grade_6.one_step import (
    Grade6OneStepGenerator,
)
from backend.app.generators.grade_6.statistics import (
    Grade6StatisticsGenerator,
)

GENERATOR_REGISTRY: Dict[str, Type[BaseGenerator]] = {
    # Algebra 1
    QuadraticEquationsGenerator.generator_id: QuadraticEquationsGenerator,
    TwoStepEquationsGenerator.generator_id: TwoStepEquationsGenerator,
    MultiStepEquationsGenerator.generator_id: MultiStepEquationsGenerator,
    LinearEquationsGenerator.generator_id: LinearEquationsGenerator,
    SystemsOfEquationsGenerator.generator_id: SystemsOfEquationsGenerator,
    PolynomialFactoringGenerator.generator_id: PolynomialFactoringGenerator,

    # Geometry
    PythagoreanTheoremGenerator.generator_id: PythagoreanTheoremGenerator,
    GeometryAnglesLinesGenerator.generator_id: GeometryAnglesLinesGenerator,
    GeometryTrianglesGenerator.generator_id: GeometryTrianglesGenerator,
    GeometryTrigonometryGenerator.generator_id: GeometryTrigonometryGenerator,
    GeometryCirclesGenerator.generator_id: GeometryCirclesGenerator,
    GeometryAreaVolumeGenerator.generator_id: GeometryAreaVolumeGenerator,

    # Algebra 2
    Algebra2ComplexNumbersGenerator.generator_id: (
        Algebra2ComplexNumbersGenerator
    ),
    Algebra2LogarithmsGenerator.generator_id: Algebra2LogarithmsGenerator,
    Algebra2RationalExpressionsGenerator.generator_id: (
        Algebra2RationalExpressionsGenerator
    ),
    Algebra2RadicalsGenerator.generator_id: Algebra2RadicalsGenerator,

    # Precalculus
    PrecalcVectorsGenerator.generator_id: PrecalcVectorsGenerator,
    PrecalcMatricesGenerator.generator_id: PrecalcMatricesGenerator,
    PrecalcTrigGenerator.generator_id: PrecalcTrigGenerator,
    PrecalcSequencesGenerator.generator_id: PrecalcSequencesGenerator,
    PrecalcPolarConicsGenerator.generator_id: PrecalcPolarConicsGenerator,

    # Calculus
    ImplicitDifferentiationGenerator.generator_id: (
        ImplicitDifferentiationGenerator
    ),
    CalculusDerivativesGenerator.generator_id: CalculusDerivativesGenerator,
    CalculusLimitsGenerator.generator_id: CalculusLimitsGenerator,
    CalculusIntegralsGenerator.generator_id: CalculusIntegralsGenerator,
    CalculusDiffEqGenerator.generator_id: CalculusDiffEqGenerator,

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
}


def get_generator(generator_id: str) -> BaseGenerator:
    if generator_id not in GENERATOR_REGISTRY:
        raise ValueError(
            f"Unknown generator: '{generator_id}'. Available: "
            f"{list(GENERATOR_REGISTRY.keys())}"
        )
    return GENERATOR_REGISTRY[generator_id]()


# Comprehensive Kuta Course Catalog Taxonomy covering all 7 Kuta courses
_CATALOG_PATH = Path(__file__).resolve().parent / "catalog_data.json"
with open(_CATALOG_PATH, "r", encoding="utf-8") as _f:
    KUTA_COURSE_CATALOG: Dict[str, Dict[str, Any]] = json.load(_f)
