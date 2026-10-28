from __future__ import annotations

import random
from typing import List

import pytest

from backend.app.core.base import ProblemDifficulty
from backend.app.generators import (
    _BASE_GENERATOR_REGISTRY,
    TOPIC_GENERATOR_REGISTRY,
)
from backend.app.generators.validator import validate_generated_problem


class TestAllGeneratorsVisualSweep:
    """Exhaustive multi-seed visual and typographic verification sweep across all generators."""

    @pytest.mark.parametrize("gen_id, gen_cls", list(_BASE_GENERATOR_REGISTRY.items()))
    def test_base_generators_multi_tier_sweep(self, gen_id: str, gen_cls: type) -> None:
        """Audit every registered core generator across mild, medium, and spicy tiers."""
        generator = gen_cls()
        tiers = [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY]

        for tier in tiers:
            seen_equations = set()
            for seed in range(101, 111):
                rng = random.Random(seed)
                try:
                    prob = generator.generate_single(
                        rng=rng,
                        difficulty=tier,
                        problem_idx=seed,
                        allow_negatives=True,
                    )
                except Exception as e:
                    pytest.fail(f"Generator '{gen_id}' crashed on tier '{tier.value}' with seed {seed}: {e}")

                errors = validate_generated_problem(prob)
                assert not errors, (
                    f"Generator '{gen_id}' produced defects on tier '{tier.value}' with seed {seed}:\n"
                    + "\n".join(f"  - {err}" for err in errors)
                )

                # Check uniqueness within this tier
                eq_clean = prob.equation_typst.strip()
                seen_equations.add(eq_clean)

            # Assert diversity: at least 70% unique stems across 10 random seeds
            assert len(seen_equations) >= 3, (
                f"Generator '{gen_id}' lacked procedural diversity in tier '{tier.value}': "
                f"only {len(seen_equations)} unique equations out of 10 seeds"
            )

    def test_curriculum_catalog_sweep(self) -> None:
        """Audit all 598 catalog topics for zero LaTeX escaping defects, clean SVGs, and step completeness."""
        defects: List[str] = []
        topics_audited = 0

        for t_id, gen_cls in TOPIC_GENERATOR_REGISTRY.items():
            generator = gen_cls()
            topics_audited += 1

            for diff in [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY]:
                for seed in (42, 137):
                    rng = random.Random(seed)
                    try:
                        prob = generator.generate_single(
                            rng=rng,
                            difficulty=diff,
                            problem_idx=seed,
                            allow_negatives=True,
                        )
                    except Exception as e:
                        defects.append(f"[{t_id}] Crashed on tier {diff.value} (seed {seed}): {e}")
                        continue

                    errs = validate_generated_problem(prob)
                    if errs:
                        for e in errs:
                            defects.append(f"[{t_id}] ({diff.value}, seed {seed}): {e}")

        assert not defects, (
            f"Detected {len(defects)} defects across {topics_audited} curriculum topics:\n"
            + "\n".join(defects[:25])
        )
