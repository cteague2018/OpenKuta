from __future__ import annotations

import pytest

from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.generators import COURSE_CATALOG, GENERATOR_REGISTRY, get_generator


def get_all_topics():
    topics = []
    for course_id, course_data in COURSE_CATALOG.items():
        course_title = course_data.get("title", course_id)
        for cat in course_data.get("categories", []):
            cat_name = cat.get("name", "")
            for top in cat.get("topics", []):
                t_name = top.get("name", "")
                gid = top.get("generator_id", "")
                topics.append((course_title, cat_name, t_name, gid))
    return topics


ALL_TOPICS = get_all_topics()


class TestTopicProblemIntegrity:
    """Verifies that EVERY topic across EVERY curriculum tier has a registered generator,
    generates problem sets adhering to topic invariants, and generates multiple-choice options.
    """

    def test_all_catalog_topics_have_registered_generators(self):
        """Ensure 100% of topics in the catalog resolve to valid generators without fallback."""
        unregistered = []
        for course_title, cat_name, t_name, gid in ALL_TOPICS:
            if gid not in GENERATOR_REGISTRY:
                unregistered.append(f"{course_title} -> {cat_name} -> {t_name} (generator_id: {gid})")

        assert len(unregistered) == 0, f"Found {len(unregistered)} topics with unregistered generators: {unregistered[:5]}"

    def test_every_generator_produces_valid_free_response_and_multiple_choice(self):
        """Test problem generation and multiple-choice distractors for each unique generator."""
        unique_gids = sorted(list(set(gid for _, _, _, gid in ALL_TOPICS)))

        for gid in unique_gids:
            gen = get_generator(gid)

            # 1. Free response test
            fr_config = GeneratorConfig(
                problem_count=4,
                seed=42,
                difficulty_distribution={
                    ProblemDifficulty.MILD: 0.25,
                    ProblemDifficulty.MEDIUM: 0.5,
                    ProblemDifficulty.SPICY: 0.25,
                },
                question_type="free_response"
            )
            fr_probs = gen.generate(fr_config)
            assert len(fr_probs) == 4, f"Generator '{gid}' did not produce 4 problems"
            for p in fr_probs:
                assert p.equation_typst, f"Generator '{gid}' produced problem without equation"
                assert p.answer_typst, f"Generator '{gid}' produced problem without answer"
                assert len(p.steps_typst) >= 1, f"Generator '{gid}' produced problem without solution steps"

            # 2. Multiple choice test
            mc_config = GeneratorConfig(
                problem_count=4,
                seed=77,
                question_type="multiple_choice"
            )
            mc_probs = gen.generate(mc_config)
            assert len(mc_probs) == 4
            for p in mc_probs:
                assert len(p.choices) == 4, f"Generator '{gid}' failed to generate 4 multiple-choice options"
                letters = [c["letter"] for c in p.choices]
                assert letters == ["A", "B", "C", "D"], f"Choices letters invalid: {letters}"
                assert p.correct_choice in ["A", "B", "C", "D"], f"Invalid correct_choice: {p.correct_choice}"

                # Ensure options are not empty and are distinct
                option_texts = [c["text"].strip() for c in p.choices]
                assert all(len(t) > 0 for t in option_texts)
                assert len(set(option_texts)) == 4, f"Generator '{gid}' produced duplicate choices: {option_texts}"

    @pytest.mark.parametrize(
        "topic_keyword,expected_substrs",
        [
            ("verbal expression", ["sum", "less", "more", "product", "quotient", "times", "difference"]),
            ("absolute value equation", ["|", "abs"]),
            ("the distributive property", ["(", ")"]),
            ("literal equation", ["solve for", "="]),
            ("derivatives", ["'", "d/dx", "diff", "deriv"]),
            ("integrals", ["integral", "int", "dx"]),
            ("matrices", ["mat(", "[", "matrix"]),
            ("sequences", ["a_", "sequence", "series", "sum", "term"]),
            ("scientific notation", ["10^", "scientific", "standard", "decimal"]),
            ("exponential function", ["^", "growth", "decay", "initial", "f(t)"]),
            ("word problem", ["mph", "miles", "liters", "hours", "chemist", "people", "population", "tickets", "sold", "years"]),
            ("probability", ["probability", "ways", "committees", "meals", "p("]),
            ("solving by graphing", ["graph", "graphing", "line"]),
            ("solving by substitution", ["substitution", "substitute"]),
            ("solving by elimination", ["elimination", "eliminate"]),
            ("systems of inequalities", ["inequalit", "shade", "region"]),
            ("taking square roots", ["square root", "roots", "sqrt"]),
            ("discriminant", ["discriminant", "solution"]),
            ("graphing single-variable inequalities", ["number line", "graph", "circle", "arrow", "inequalit"]),
            ("slope, tangent, and normal lines", ["tangent", "normal", "slope", "derivative", "point"]),
            ("multiplying special cases", ["product", "binomial", "x^", "x", "foil", "^2", "square"]),
        ]
    )
    def test_topic_domain_invariants(self, topic_keyword, expected_substrs):
        """Verifies that problem sets for specific domains actually contain respective mathematical syntax."""
        matching_topics = [
            (c, cat, name, gid)
            for c, cat, name, gid in ALL_TOPICS
            if topic_keyword in name.lower() or topic_keyword in cat.lower()
        ]

        assert len(matching_topics) > 0, f"No catalog topics matched '{topic_keyword}'"

        for course, _cat, name, gid in matching_topics[:5]:
            gen = get_generator(gid)
            probs = gen.generate(GeneratorConfig(problem_count=3, seed=101))
            corpus = " ".join(
                f"{p.prompt_text} {p.equation_typst} {p.answer_typst} {' '.join(p.steps_typst)}"
                for p in probs
            ).lower()

            matched = any(sub in corpus for sub in expected_substrs)
            assert matched, (
                f"Topic '{name}' in '{course}' generated problems unrelated to '{topic_keyword}'.\n"
                f"Corpus: {corpus[:200]}..."
            )
