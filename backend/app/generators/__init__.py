from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Type
from backend.app.core.base import BaseGenerator
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
from backend.app.generators.geometry.pythagorean import (
    PythagoreanTheoremGenerator,
)

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
        raise ValueError(
            f"Unknown generator: '{generator_id}'. Available: "
            f"{list(GENERATOR_REGISTRY.keys())}"
        )
    return GENERATOR_REGISTRY[generator_id]()


# Comprehensive Kuta Course Catalog Taxonomy covering all 7 Kuta courses
_CATALOG_PATH = Path(__file__).resolve().parent / "catalog_data.json"
with open(_CATALOG_PATH, "r", encoding="utf-8") as _f:
    KUTA_COURSE_CATALOG: Dict[str, Dict[str, Any]] = json.load(_f)
