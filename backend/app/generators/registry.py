from __future__ import annotations

import random
from typing import Any, Callable, Dict, Type, cast

from backend.app.core.base import (
    BaseGenerator,
    BaseProblem,
    GeneratorConfig,
    ProblemDifficulty,
)
from backend.app.generators import GENERATOR_REGISTRY


def _make_generator_callable(
    gen_cls: Type[BaseGenerator], gen_id: str
) -> Callable[..., BaseProblem]:
    def gen_fn(seed: int = 42, difficulty: str = "mild") -> BaseProblem:
        diff_enum = ProblemDifficulty(difficulty.lower())
        try:
            inst = gen_cls(seed=seed)
        except TypeError:
            try:
                inst = gen_cls()
            except TypeError:
                inst = cast(Any, gen_cls)(
                    GeneratorConfig(
                        problem_count=1,
                        seed=seed,
                        difficulty_distribution={diff_enum: 1.0},
                    )
                )
        rng = random.Random(seed)
        if hasattr(inst, "generate_single"):
            try:
                prob = inst.generate_single(
                    rng=rng,
                    difficulty=diff_enum,
                    problem_idx=1,
                    allow_negatives=True,
                )
                if not prob.generator_id:
                    prob.generator_id = gen_id
                return prob
            except Exception:
                pass

        cfg = GeneratorConfig(
            problem_count=1,
            seed=seed,
            difficulty_distribution={diff_enum: 1.0},
        )
        problems = inst.generate(cfg)
        prob = problems[0]
        if not prob.generator_id:
            prob.generator_id = gen_id
        return prob

    safe_name = f"generate_{gen_id.replace('.', '_').replace('-', '_')}"
    gen_fn.__name__ = safe_name
    return gen_fn


def get_all_registered_generators() -> Dict[str, Callable[..., BaseProblem]]:
    return {
        gen_id: _make_generator_callable(gen_cls, gen_id)
        for gen_id, gen_cls in GENERATOR_REGISTRY.items()
    }
