from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProblemDifficulty(str, Enum):
    MILD = "mild"
    MEDIUM = "medium"
    SPICY = "spicy"


class BoundingBox(BaseModel):
    x: float = Field(default=0.0, description="X coordinate (pt or normalized)")
    y: float = Field(default=0.0, description="Y coordinate (pt or normalized)")
    width: float = Field(default=0.0, description="Box width (pt or normalized)")
    height: float = Field(default=0.0, description="Box height (pt or normalized)")


class BaseProblem(BaseModel):
    id: str = Field(..., description="Unique problem identifier")
    prompt_text: str = Field(..., description="Problem prompt instructions")
    equation_typst: str = Field(..., description="Problem equation in Typst syntax")
    answer_typst: str = Field(..., description="Final simplified answer in Typst syntax")
    steps_typst: List[str] = Field(default_factory=list, description="Step-by-step solution steps")
    distractors: List[str] = Field(default_factory=list, description="Common misconception-based distractors")
    difficulty: ProblemDifficulty = Field(default=ProblemDifficulty.MILD, description="Difficulty tier")
    bounding_box: Optional[BoundingBox] = Field(default=None, description="Pre-computed workspace bounding box")
    standards: List[str] = Field(default_factory=list, description="Curriculum standard codes (e.g., CCSS.MATH.CONTENT.HSA.REI.B.4)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary generator metadata")

    @property
    def equation_latex(self) -> str:
        """Helper returning basic LaTeX equivalent for web preview."""
        # Convert common typst math symbols to LaTeX if needed
        eq = self.equation_typst
        eq = eq.replace("$", "").strip()
        # Basic replacement for fractions: (a) / (b) or a/b -> \frac{a}{b}
        return eq

    @property
    def answer_latex(self) -> str:
        ans = self.answer_typst.replace("$", "").strip()
        return ans


class GeneratorConfig(BaseModel):
    problem_count: int = Field(default=10, ge=1, le=50, description="Number of problems to generate")
    difficulty_distribution: Dict[ProblemDifficulty, float] = Field(
        default_factory=lambda: {
            ProblemDifficulty.MILD: 0.4,
            ProblemDifficulty.MEDIUM: 0.4,
            ProblemDifficulty.SPICY: 0.2,
        },
        description="Target distribution weights of difficulty tiers"
    )
    allow_negatives: bool = Field(default=True, description="Allow negative integer coefficients/constants")
    seed: Optional[int] = Field(default=None, description="Explicit deterministic pseudo-random seed")
    form_ids: List[str] = Field(default_factory=lambda: ["A", "B", "C", "D"], description="Variant form identifiers")


class BaseGenerator(ABC):
    """Abstract base class for all backward-parameterized math problem generators."""

    generator_id: str = "base"
    name: str = "Base Generator"
    category: str = "General"
    standards: List[str] = []

    def __init__(self, seed: Optional[int] = None) -> None:
        self.default_seed = seed

    @abstractmethod
    def generate_single(
        self,
        rng: random.Random,
        difficulty: ProblemDifficulty,
        problem_idx: int,
        allow_negatives: bool = True
    ) -> BaseProblem:
        """Generate a single deterministic problem via backward parameterization."""
        pass

    def generate(self, config: GeneratorConfig) -> List[BaseProblem]:
        """Generate a batch of problems adhering to the configuration and seed invariants."""
        active_seed = config.seed if config.seed is not None else self.default_seed
        rng = random.Random(active_seed)

        # Calculate exact counts per difficulty based on distribution
        dist = config.difficulty_distribution
        tiers: List[ProblemDifficulty] = []
        for tier in [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY]:
            weight = dist.get(tier, 0.0)
            count = int(round(config.problem_count * weight))
            tiers.extend([tier] * count)

        # Adjust count to match problem_count exactly
        while len(tiers) < config.problem_count:
            tiers.append(ProblemDifficulty.MEDIUM)
        if len(tiers) > config.problem_count:
            tiers = tiers[:config.problem_count]

        problems: List[BaseProblem] = []
        for idx, difficulty in enumerate(tiers, start=1):
            prob = self.generate_single(
                rng=rng,
                difficulty=difficulty,
                problem_idx=idx,
                allow_negatives=config.allow_negatives
            )
            problems.append(prob)

        return problems

