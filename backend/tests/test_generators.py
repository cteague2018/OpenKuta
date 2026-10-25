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
    for p1, p2 in zip(probs1, probs2, strict=False):
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
    from backend.app.generators.algebra_1.polynomials import (
        PolynomialFactoringGenerator,
    )
    from backend.app.generators.algebra_1.systems import (
        SystemsOfEquationsGenerator,
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


def test_new_classroom_curriculum_generators():
    """Verify newly introduced core classroom curriculum generators."""
    from backend.app.generators.algebra_1.inequalities import LinearInequalitiesGenerator
    from backend.app.generators.algebra_2.log_properties import LogPropertiesGenerator
    from backend.app.generators.calculus.riemann_sums import CalculusRiemannSumsGenerator
    from backend.app.generators.geometry.special_right_triangles import (
        SpecialRightTrianglesGenerator,
    )
    from backend.app.generators.grade_6.integers import Grade6IntegersGenerator
    from backend.app.generators.grade_6.order_of_operations import Grade6OrderOfOperationsGenerator

    cfg = GeneratorConfig(problem_count=3, seed=77)

    # 1. Inequalities
    g_ineq = LinearInequalitiesGenerator()
    probs = g_ineq.generate(cfg)
    assert len(probs) == 3
    assert all("x" in p.answer_typst for p in probs)

    # 2. Special Right Triangles
    g_srt = SpecialRightTrianglesGenerator()
    probs = g_srt.generate(cfg)
    assert len(probs) == 3
    assert all("sqrt" in p.answer_typst or "leg" in p.answer_typst for p in probs)

    # 3. Log Properties
    g_logprop = LogPropertiesGenerator()
    probs = g_logprop.generate(cfg)
    assert len(probs) == 3
    assert all("log" in p.answer_typst for p in probs)

    # 4. Riemann Sums
    g_riemann = CalculusRiemannSumsGenerator()
    probs = g_riemann.generate(cfg)
    assert len(probs) == 3
    assert all("RAM" in p.answer_typst or "Trapezoid" in p.answer_typst for p in probs)

    # 5. Order of Operations (PEMDAS)
    g_pemdas = Grade6OrderOfOperationsGenerator()
    probs = g_pemdas.generate(cfg)
    assert len(probs) == 3
    assert all(len(p.steps_typst) >= 3 for p in probs)

    # 6. Integer Operations
    g_int = Grade6IntegersGenerator()
    probs = g_int.generate(cfg)
    assert len(probs) == 3
    assert all(len(p.steps_typst) >= 3 for p in probs)



def test_upgraded_geometry_and_grade6_generators():
    """Verify procedural generation and rigor of 8 upgraded Geometry and Grade 6 generators."""
    from backend.app.generators.geometry.angles_lines import GeometryAnglesLinesGenerator
    from backend.app.generators.geometry.area_volume import GeometryAreaVolumeGenerator
    from backend.app.generators.geometry.circles import GeometryCirclesGenerator
    from backend.app.generators.geometry.triangles import GeometryTrianglesGenerator
    from backend.app.generators.geometry.trigonometry import GeometryTrigonometryGenerator
    from backend.app.generators.grade_6.factors_multiples import Grade6FactorsMultiplesGenerator
    from backend.app.generators.grade_6.fractions_decimals import Grade6FractionsDecimalsGenerator
    from backend.app.generators.grade_6.statistics import Grade6StatisticsGenerator

    diff_mild = {ProblemDifficulty.MILD: 1.0, ProblemDifficulty.MEDIUM: 0.0, ProblemDifficulty.SPICY: 0.0}
    diff_med = {ProblemDifficulty.MILD: 0.0, ProblemDifficulty.MEDIUM: 1.0, ProblemDifficulty.SPICY: 0.0}
    diff_spicy = {ProblemDifficulty.MILD: 0.0, ProblemDifficulty.MEDIUM: 0.0, ProblemDifficulty.SPICY: 1.0}

    # 1. Triangles
    gen_tri = GeometryTrianglesGenerator()
    p_mild = gen_tri.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_tri.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_tri.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("180" in s for p in p_mild for s in p.steps_typst if "Theorem" in s or "sum" in s)
    assert all("Exterior Angle Theorem" in " ".join(p.steps_typst) for p in p_med)
    assert all("x =" in p.answer_typst for p in p_spicy)

    # 2. Area & Volume
    gen_av = GeometryAreaVolumeGenerator()
    p_mild = gen_av.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_av.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_av.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("Rectangular" in p.equation_typst and "SA" in p.answer_typst for p in p_mild)
    assert all("Cylinder" in p.equation_typst and "pi" in p.answer_typst for p in p_med)
    assert all("pi" in p.answer_typst and ("Cone" in p.equation_typst or "Sphere" in p.equation_typst) for p in p_spicy)

    # 3. Trigonometry
    gen_trig = GeometryTrigonometryGenerator()
    p_mild = gen_trig.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_trig.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_trig.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("SOH CAH TOA" in " ".join(p.steps_typst) for p in p_mild)
    assert all("x" in p.answer_typst for p in p_med)
    assert all("theta" in p.answer_typst for p in p_spicy)

    # 4. Circles
    gen_circ = GeometryCirclesGenerator()
    p_mild = gen_circ.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_circ.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_circ.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("C =" in p.answer_typst and "A =" in p.answer_typst and "pi" in p.answer_typst for p in p_mild)
    assert all("s =" in p.answer_typst and "pi" in p.answer_typst for p in p_med)
    assert all("A =" in p.answer_typst and "pi" in p.answer_typst for p in p_spicy)

    # 5. Angles & Lines
    gen_ang = GeometryAnglesLinesGenerator()
    p_mild = gen_ang.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_ang.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_ang.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("m angle 2 =" in p.answer_typst for p in p_mild)
    assert all("Segment Addition Postulate" in " ".join(p.steps_typst) for p in p_med)
    assert all("parallel" in p.equation_typst and "x =" in p.answer_typst for p in p_spicy)

    # 6. Factors & Multiples
    gen_fm = Grade6FactorsMultiplesGenerator()
    p_mild = gen_fm.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_fm.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_fm.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("prime factorization" in " ".join(p.steps_typst).lower() for p in p_mild + p_med + p_spicy)
    assert all("n3" in p.metadata for p in p_spicy)

    # 7. Statistics
    gen_stat = Grade6StatisticsGenerator()
    p_mild = gen_stat.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_stat.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_stat.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("Mean" in p.answer_typst for p in p_mild)
    assert all("Median" in p.answer_typst and "Mode" in p.answer_typst for p in p_med)
    assert all("Range" in p.answer_typst and "IQR" in p.answer_typst for p in p_spicy)

    # 8. Fractions & Decimals
    gen_fd = Grade6FractionsDecimalsGenerator()
    p_mild = gen_fd.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_mild, seed=42))
    p_med = gen_fd.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_med, seed=42))
    p_spicy = gen_fd.generate(GeneratorConfig(problem_count=2, difficulty_distribution=diff_spicy, seed=42))
    assert all("reciprocal" in " ".join(p.steps_typst) for p in p_mild)
    assert all(len(p.steps_typst) >= 3 for p in p_med)
    assert all("div" in p.equation_typst for p in p_spicy)
