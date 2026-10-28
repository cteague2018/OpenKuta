from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Sequence, Tuple

import sympy as sp


@dataclass
class DifficultyLens:
    parameter_pools: Dict[str, Sequence[Any]]
    invariants: List[Callable[[Dict[str, Any]], bool]] = field(default_factory=list)
    inner_substitution: Callable[[sp.Symbol, random.Random], sp.Expr] = lambda x, rng: x


class DeclarativeTopicTemplate:
    def __init__(
        self,
        topic_id: str,
        prompt_stem: str,
        lenses: Dict[str, DifficultyLens],
        build_core_fn: Callable[[Dict[str, Any], sp.Expr], Tuple[sp.Basic, Any, List[sp.Basic]]],
    ):
        self.topic_id = topic_id
        self.prompt_stem = prompt_stem
        self.lenses = lenses
        self.build_core_fn = build_core_fn

    def sample_parameters(self, rng: random.Random, difficulty: str, max_tries: int = 500) -> Dict[str, Any]:
        lens = self.lenses[difficulty]
        keys = sorted(lens.parameter_pools.keys())
        for _ in range(max_tries):
            params = {k: rng.choice(lens.parameter_pools[k]) for k in keys}
            if all(inv(params) for inv in lens.invariants):
                return params
        raise RuntimeError(f"Could not satisfy parameter invariants for {self.topic_id} ({difficulty})")
