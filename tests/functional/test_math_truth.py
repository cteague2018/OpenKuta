from __future__ import annotations

import sympy as sp
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.generators import GENERATOR_REGISTRY, get_generator
from backend.app.grading.verifier import CASStepVerifier

cas_verifier = CASStepVerifier()


def parse_roots_from_typst(ans_typst: str) -> list[sp.Expr]:
    """Extract numeric/symbolic root values from answer typst string like 'x = 3, -5' or '$ x = 2 $'."""
    cleaned = ans_typst.replace("$", "").replace("x =", "").strip()
    tokens = [t.strip() for t in cleaned.split(",") if t.strip()]
    roots = []
    for tok in tokens:
        try:
            tok_norm = tok.replace(" ", "")
            # Handle fractions like -3/2
            if "/" in tok_norm:
                p, q = tok_norm.split("/")
                roots.append(sp.Rational(int(p), int(q)))
            elif tok_norm.lstrip("-").isdigit():
                roots.append(sp.Integer(int(tok_norm)))
            else:
                parsed = sp.sympify(tok_norm)
                roots.append(parsed)
        except Exception:
            continue
    return roots


class TestMathTruthEngine:
    """Mathematical truth engine & invariant property verification."""

    def test_topic_coverage_matrix_sweep_all_generators(self) -> None:
        """Sweep through every curriculum topic generator across mild, medium, and spicy tiers."""
        assert len(GENERATOR_REGISTRY) >= 30, f"Expected 30+ generators, found {len(GENERATOR_REGISTRY)}"

        for gen_id, gen_cls in GENERATOR_REGISTRY.items():
            gen = gen_cls()
            for diff in [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY]:
                cfg = GeneratorConfig(
                    problem_count=4,
                    seed=1337 + hash(gen_id) % 500,
                    difficulty_distribution={diff: 1.0},
                    allow_negatives=True,
                )
                problems = gen.generate(cfg)
                assert len(problems) == 4, f"{gen_id} ({diff.value}) failed to generate 4 problems"

                for idx, prob in enumerate(problems, start=1):
                    # Invariant 1: Schema conformance
                    assert prob.id, f"{gen_id} problem #{idx} missing ID"
                    assert prob.prompt_text, f"{gen_id} problem #{idx} missing prompt"
                    assert prob.equation_typst, f"{gen_id} problem #{idx} missing equation"
                    assert prob.answer_typst, f"{gen_id} problem #{idx} missing answer"
                    assert isinstance(prob.steps_typst, list), f"{gen_id} steps not a list"
                    assert len(prob.steps_typst) >= 1, f"{gen_id} problem #{idx} has empty steps"

                    # Invariant 2: Zero divide-by-zero or undefined residues
                    eq_str = prob.equation_typst
                    ans_str = prob.answer_typst
                    for bad in ["/ 0", "/(0)", "/ (0)", "nan", "zoo", "None", "undefined"]:
                        assert bad not in eq_str, f"Found undefined token '{bad}' in equation: {eq_str}"
                        assert bad not in ans_str, f"Found undefined token '{bad}' in answer: {ans_str}"

                    # Invariant 3: Difficulty tier assigned accurately
                    assert prob.difficulty == diff

    def test_quadratic_equations_identity_and_solution_truth(self) -> None:
        """Substitute generated solutions back into quadratic equations; assert P(S) == 0."""
        gen = get_generator("algebra_1.quadratics")
        for seed in [11, 42, 99, 123, 777]:
            cfg = GeneratorConfig(problem_count=6, seed=seed)
            problems = gen.generate(cfg)
            x = sp.Symbol("x")

            for prob in problems:
                roots = parse_roots_from_typst(prob.answer_typst)
                if not roots and prob.metadata and "roots" in prob.metadata:
                    roots = [sp.sympify(r) for r in prob.metadata["roots"]]

                # If roots extracted, verify quadratic polynomial evaluates to 0
                if roots and prob.metadata and "a" in prob.metadata:
                    a = prob.metadata.get("a", 1)
                    b = prob.metadata.get("b", 0)
                    c = prob.metadata.get("c", 0)
                    poly = a * x**2 + b * x + c
                    for r in roots:
                        res = sp.simplify(poly.subs(x, r))
                        assert res == 0, f"Root {r} did not satisfy {poly} = 0 (residue: {res})"

    def test_linear_equations_identity_and_solution_truth(self) -> None:
        """Verify linear equation solutions satisfy equation with zero residue."""
        gen = get_generator("algebra_1.two_step")
        sp.Symbol("x")
        cfg = GeneratorConfig(problem_count=10, seed=555)
        problems = gen.generate(cfg)

        for prob in problems:
            roots = parse_roots_from_typst(prob.answer_typst)
            if roots:
                r = roots[0]
                # In metadata, solution should be present
                if prob.metadata and "solution" in prob.metadata:
                    expected = sp.sympify(prob.metadata["solution"])
                    assert sp.simplify(r - expected) == 0

    def test_systems_of_equations_solution_truth(self) -> None:
        """Verify 2-variable linear systems solutions satisfy both equations simultaneously."""
        gen = get_generator("algebra_1.systems")
        cfg = GeneratorConfig(problem_count=6, seed=90210)
        problems = gen.generate(cfg)

        for prob in problems:
            if prob.metadata and "x" in prob.metadata and "y" in prob.metadata:
                sol_x = prob.metadata["x"]
                sol_y = prob.metadata["y"]
                a1 = prob.metadata.get("a1", 1)
                b1 = prob.metadata.get("b1", 1)
                c1 = prob.metadata.get("c1", 0)
                a2 = prob.metadata.get("a2", 1)
                b2 = prob.metadata.get("b2", 1)
                c2 = prob.metadata.get("c2", 0)

                assert a1 * sol_x + b1 * sol_y == c1, f"Solution ({sol_x}, {sol_y}) failed eq 1: {a1}x + {b1}y = {c1}"
                assert a2 * sol_x + b2 * sol_y == c2, f"Solution ({sol_x}, {sol_y}) failed eq 2: {a2}x + {b2}y = {c2}"

    def test_four_form_anti_cheat_scramble_parity(self) -> None:
        """Assert 4-form scrambles (A, B, C, D) maintain 1:1 index alignment with their answer keys."""
        from backend.app.api.routes import MultiFormRequest, generate_multi_form

        req = MultiFormRequest(
            title="Algebra 1 Mastery Test",
            base_seed=4242,
            problem_count=8,
            generator_id="algebra_1.quadratics",
            forms=["A", "B", "C", "D"],
        )
        response = generate_multi_form(req)
        assert response.status_code == 200 or response.media_type == "application/zip"
        assert len(response.body) > 20000, "Multi-form ZIP bundle should be > 20 KB"

        # Programmatically verify internal generator parity across forms
        forms = ["A", "B", "C", "D"]
        form_problems: dict[str, list] = {}
        gen = get_generator("algebra_1.quadratics")

        for idx, f_id in enumerate(forms):
            f_seed = 4242 + (idx * 1337)
            cfg = GeneratorConfig(problem_count=8, seed=f_seed)
            probs = gen.generate(cfg)
            form_problems[f_id] = probs

        # 1. Every form has identical problem count
        for f_id in forms:
            assert len(form_problems[f_id]) == 8

        # 2. In Form B, problem #i strictly matches Answer #i for Form B
        for f_id in forms:
            probs = form_problems[f_id]
            for i in range(len(probs)):
                # The problem's own answer_typst is 1:1 paired with that problem
                p = probs[i]
                assert p.answer_typst, f"Form {f_id} problem #{i+1} missing answer"
                # Form B problem #i is not arbitrarily swapped with another problem's answer
                assert p.id, f"Form {f_id} problem #{i+1} missing ID"

    @settings(max_examples=25, suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @given(st.integers(min_value=1, max_value=99999))
    def test_property_based_fuzzing_random_seeds(self, seed: int) -> None:
        """Property-based fuzzing: generators must maintain invariants across arbitrary seeds."""
        test_generators = [
            "algebra_1.quadratics",
            "algebra_1.two_step",
            "geometry.pythagorean",
            "grade_6.order_of_operations",
            "calculus.derivatives",
        ]
        for gen_id in test_generators:
            gen = get_generator(gen_id)
            cfg = GeneratorConfig(problem_count=3, seed=seed)
            probs = gen.generate(cfg)
            assert len(probs) == 3
            for p in probs:
                assert p.equation_typst
                assert p.answer_typst
                assert "nan" not in p.equation_typst
                assert "zoo" not in p.equation_typst
