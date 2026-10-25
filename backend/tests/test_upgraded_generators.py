from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.generators.algebra_1.exponent_rules import ExponentRulesGenerator
from backend.app.generators.algebra_2.polynomial_division import PolynomialDivisionGenerator
from backend.app.generators.algebra_2.radicals import Algebra2RadicalsGenerator
from backend.app.generators.algebra_2.rational_expressions import (
    Algebra2RationalExpressionsGenerator,
)
from backend.app.generators.calculus.diff_eq import CalculusDiffEqGenerator
from backend.app.generators.precalculus.matrices import PrecalcMatricesGenerator
from backend.app.generators.precalculus.polar_conics import PrecalcPolarConicsGenerator
from backend.app.generators.precalculus.sequences import PrecalcSequencesGenerator
from backend.app.generators.precalculus.trig_advanced import PrecalcTrigGenerator
from backend.app.generators.precalculus.vectors import PrecalcVectorsGenerator


def test_diff_eq_procedural():
    gen = CalculusDiffEqGenerator()

    # Mild: separable growth/decay dy/dx = ky
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=42))
    assert len(probs_mild) == 6
    for p in probs_mild:
        assert "(d y)/(d x) =" in p.equation_typst
        assert "y = C e^" in p.answer_typst
        assert len(p.steps_typst) >= 4

    # Medium: separable polynomial/rational diff eq
    probs_med = gen.generate(GeneratorConfig(problem_count=8, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=43))
    assert len(probs_med) == 8
    for p in probs_med:
        assert "(d y)/(d x) =" in p.equation_typst
        assert len(p.steps_typst) >= 4

    # Spicy: Newton's cooling or IVP
    probs_spicy = gen.generate(GeneratorConfig(problem_count=8, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=44))
    assert len(probs_spicy) == 8
    for p in probs_spicy:
        assert len(p.steps_typst) >= 4
        assert "e^" in p.answer_typst


def test_trig_advanced_procedural():
    gen = PrecalcTrigGenerator()

    # Mild: Linear trig equations with unit circle special angles
    probs_mild = gen.generate(GeneratorConfig(problem_count=8, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=50))
    for p in probs_mild:
        assert "sin(x)" in p.equation_typst or "cos(x)" in p.equation_typst
        assert len(p.steps_typst) >= 3

    # Medium: tan equations or factoring
    probs_med = gen.generate(GeneratorConfig(problem_count=8, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=51))
    for p in probs_med:
        assert "tan" in p.equation_typst or "cos" in p.equation_typst or "sin" in p.equation_typst
        assert len(p.steps_typst) >= 3

    # Spicy: quadratic trig or double angle
    probs_spicy = gen.generate(GeneratorConfig(problem_count=8, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=52))
    for p in probs_spicy:
        assert len(p.steps_typst) >= 4
        assert len(p.distractors) >= 2


def test_vectors_procedural():
    gen = PrecalcVectorsGenerator()

    # Mild: exact simplified radical magnitude
    probs_mild = gen.generate(GeneratorConfig(problem_count=8, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=60))
    for p in probs_mild:
        assert "norm(bold(v)) =" in p.answer_typst
        assert len(p.steps_typst) >= 3

    # Medium: dot product and angle theta
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=61))
    for p in probs_med:
        assert "bold(u) dot bold(v)" in p.answer_typst
        assert "theta" in p.answer_typst
        assert len(p.steps_typst) >= 4

    # Spicy: unit vector or linear combination
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=62))
    for p in probs_spicy:
        assert "angle.l" in p.answer_typst
        assert len(p.steps_typst) >= 3


def test_matrices_procedural():
    gen = PrecalcMatricesGenerator()

    # Mild: 2x2 determinants ad - bc
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=70))
    for p in probs_mild:
        assert p.answer_typst.lstrip("-").isdigit()
        assert len(p.steps_typst) >= 4

    # Medium: scalar ops or matrix multiplication
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=71))
    for p in probs_med:
        assert "mat(" in p.answer_typst
        assert len(p.steps_typst) >= 3

    # Spicy: 2x2 matrix inverse with invertibility check
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=72))
    for p in probs_spicy:
        assert "mat(" in p.answer_typst
        assert any("invertible" in s for s in p.steps_typst)
        assert len(p.steps_typst) >= 4


def test_sequences_procedural():
    gen = PrecalcSequencesGenerator()

    # Mild: arithmetic nth term
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=80))
    for p in probs_mild:
        assert "a_" in p.answer_typst
        assert len(p.steps_typst) >= 4

    # Medium: geometric nth term
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=81))
    for p in probs_med:
        assert "a_" in p.answer_typst
        assert len(p.steps_typst) >= 4

    # Spicy: arithmetic & geometric series partial sums
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=82))
    for p in probs_spicy:
        assert "S_" in p.answer_typst
        assert len(p.steps_typst) >= 4


def test_polar_conics_procedural():
    gen = PrecalcPolarConicsGenerator()

    # Mild: circle standard form
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=90))
    for p in probs_mild:
        assert "=" in p.answer_typst
        assert len(p.steps_typst) >= 3

    # Medium: ellipse center, vertices, foci
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=91))
    for p in probs_med:
        assert "Center:" in p.answer_typst
        assert "Vertices:" in p.answer_typst
        assert "Foci:" in p.answer_typst
        assert len(p.steps_typst) >= 4

    # Spicy: completing the square
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=92))
    for p in probs_spicy:
        assert "= 1" in p.answer_typst
        assert any("Complete the square" in s for s in p.steps_typst)
        assert len(p.steps_typst) >= 4


def test_radicals_procedural():
    gen = Algebra2RadicalsGenerator()

    # Mild: simplifying single radical
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=100))
    for p in probs_mild:
        assert "sqrt" in p.answer_typst
        assert len(p.steps_typst) >= 3

    # Medium: operations or rational exponents
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=101))
    for p in probs_med:
        assert len(p.steps_typst) >= 3

    # Spicy: solving radical equations with extraneous check
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=102))
    for p in probs_spicy:
        assert "x =" in p.answer_typst
        assert any("Check" in s for s in p.steps_typst)
        assert len(p.steps_typst) >= 4


def test_rational_expressions_procedural():
    gen = Algebra2RationalExpressionsGenerator()

    # Mild: simplifying with excluded values
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=110))
    for p in probs_mild:
        assert "x !=" in p.answer_typst
        assert any("excluded" in s for s in p.steps_typst)
        assert len(p.steps_typst) >= 3

    # Medium: multiplying / dividing with excluded values
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=111))
    for p in probs_med:
        assert "x !=" in p.answer_typst
        assert len(p.steps_typst) >= 3

    # Spicy: adding / subtracting with unlike denominators
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=112))
    for p in probs_spicy:
        assert "x !=" in p.answer_typst
        assert any("LCD" in s for s in p.steps_typst)
        assert len(p.steps_typst) >= 4


def test_exponent_rules_procedural():
    gen = ExponentRulesGenerator()

    # Mild: single-variable product and quotient
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=120))
    assert len(probs_mild) == 6
    for p in probs_mild:
        assert p.answer_typst
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(p.steps_typst) >= 4

    # Medium: power of a power and negative exponents
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=121))
    assert len(probs_med) == 6
    for p in probs_med:
        assert p.answer_typst
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(p.steps_typst) >= 4

    # Spicy: multi-variable rational expressions with negative exponents
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=122))
    assert len(probs_spicy) == 6
    for p in probs_spicy:
        assert p.answer_typst
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(p.steps_typst) >= 4


def test_polynomial_division_procedural():
    gen = PolynomialDivisionGenerator()

    # Mild: division with remainder 0
    probs_mild = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MILD: 1.0}, seed=130))
    assert len(probs_mild) == 6
    for p in probs_mild:
        assert p.answer_typst
        assert "/" not in p.answer_typst  # Remainder is 0, so no fraction in answer
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(p.steps_typst) >= 4

    # Medium: division of cubic with non-zero remainder
    probs_med = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.MEDIUM: 1.0}, seed=131))
    assert len(probs_med) == 6
    for p in probs_med:
        assert p.answer_typst
        assert "/" in p.answer_typst  # Non-zero remainder format
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(p.steps_typst) >= 5

    # Spicy: linear binomial with leading coefficient or missing term
    probs_spicy = gen.generate(GeneratorConfig(problem_count=6, difficulty_distribution={ProblemDifficulty.SPICY: 1.0}, seed=132))
    assert len(probs_spicy) == 6
    for p in probs_spicy:
        assert p.answer_typst
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(p.steps_typst) >= 5

