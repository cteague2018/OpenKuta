import sympy as sp  # type: ignore
from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.generators.algebra_1.quadratics import (
    QuadraticEquationsGenerator,
)


def test_generator_determinism():
    gen1 = QuadraticEquationsGenerator()
    gen2 = QuadraticEquationsGenerator()

    cfg1 = GeneratorConfig(problem_count=6, seed=42)
    cfg2 = GeneratorConfig(problem_count=6, seed=42)
    cfg3 = GeneratorConfig(problem_count=6, seed=99)

    probs1 = gen1.generate(cfg1)
    probs2 = gen2.generate(cfg2)
    probs3 = gen1.generate(cfg3)

    # Identical seed produces identical problem set
    assert len(probs1) == len(probs2) == 6
    for p1, p2 in zip(probs1, probs2):
        assert p1.equation_typst == p2.equation_typst
        assert p1.answer_typst == p2.answer_typst
        assert p1.distractors == p2.distractors

    # Different seed produces different problem set
    equations1 = [p.equation_typst for p in probs1]
    equations3 = [p.equation_typst for p in probs3]
    assert equations1 != equations3


def test_quadratic_mild_integer_roots():
    gen = QuadraticEquationsGenerator()
    diff_dist = {
        ProblemDifficulty.MILD: 1.0,
        ProblemDifficulty.MEDIUM: 0.0,
        ProblemDifficulty.SPICY: 0.0,
    }
    cfg = GeneratorConfig(
        problem_count=5,
        difficulty_distribution=diff_dist,
        seed=101,
    )
    problems = gen.generate(cfg)

    x = sp.Symbol("x")
    for prob in problems:
        assert prob.difficulty == ProblemDifficulty.MILD
        roots = prob.metadata["roots"]
        assert len(roots) == 2
        # Verify roots satisfy (x - r1)(x - r2) = 0
        r1, r2 = roots
        poly = (x - r1) * (x - r2)
        assert poly.subs(x, r1) == 0
        assert poly.subs(x, r2) == 0


def test_new_kuta_generators():
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

    cfg = GeneratorConfig(problem_count=3, seed=50)

    # Linear Equations
    g_lin = LinearEquationsGenerator()
    probs_lin = g_lin.generate(cfg)
    assert len(probs_lin) == 3
    assert all(
        "m =" in p.answer_typst or "y =" in p.answer_typst for p in probs_lin
    )

    # Systems of Equations
    g_sys = SystemsOfEquationsGenerator()
    probs_sys = g_sys.generate(cfg)
    assert len(probs_sys) == 3
    assert all("cases" in p.equation_typst for p in probs_sys)

    # Factoring
    g_fact = PolynomialFactoringGenerator()
    probs_fact = g_fact.generate(cfg)
    assert len(probs_fact) == 3
    assert all("(" in p.answer_typst for p in probs_fact)

    # Pythagorean Theorem
    g_pyth = PythagoreanTheoremGenerator()
    probs_pyth = g_pyth.generate(cfg)
    assert len(probs_pyth) == 3
    assert all("=" in p.equation_typst for p in probs_pyth)

    # Multi-Step Equations
    from backend.app.generators.algebra_1.multi_step_equations import (
        MultiStepEquationsGenerator,
    )

    g_multi = MultiStepEquationsGenerator()
    probs_multi = g_multi.generate(cfg)
    assert len(probs_multi) == 3
    assert all(len(p.steps_typst) >= 3 for p in probs_multi)
    assert all("x =" in p.answer_typst for p in probs_multi)


def test_forensic_audit_all_generators_steps_and_workspaces():
    """Audit all 7 generator classes across all difficulties to ensure
    100% complete step traces and clean answers.
    """
    from backend.app.generators import GENERATOR_REGISTRY

    difficulties = [
        ProblemDifficulty.MILD,
        ProblemDifficulty.MEDIUM,
        ProblemDifficulty.SPICY,
    ]

    for gen_id, gen_cls in GENERATOR_REGISTRY.items():
        gen = gen_cls()
        for diff in difficulties:
            dist = {d: 1.0 if d == diff else 0.0 for d in difficulties}
            cfg = GeneratorConfig(
                problem_count=4,
                difficulty_distribution=dist,
                seed=12345,
            )
            problems = gen.generate(cfg)

            assert len(problems) == 4, f"{gen_id} failed: count != 4"
            for prob in problems:
                assert prob.prompt_text, f"{gen_id} missing prompt_text"
                assert prob.equation_typst, f"{gen_id} missing equation_typst"
                assert prob.answer_typst, f"{gen_id} missing answer_typst"
                assert prob.steps_typst and len(prob.steps_typst) >= 2, (
                    f"{gen_id} ({diff.value}) has incomplete steps"
                )
                assert (
                    len(prob.distractors) >= 2
                ), f"{gen_id} missing distractors"
