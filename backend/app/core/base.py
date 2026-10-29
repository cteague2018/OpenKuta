from __future__ import annotations

import random
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


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
    equation_latex: Optional[str] = Field(default=None, description="Pre-rendered KaTeX LaTeX equation")
    answer_latex: Optional[str] = Field(default=None, description="Pre-rendered KaTeX LaTeX answer")
    steps_typst: List[str] = Field(default_factory=list, description="Step-by-step solution steps")
    distractors: List[str] = Field(default_factory=list, description="Common misconception-based distractors")
    choices: List[Dict[str, str]] = Field(default_factory=list, description="Multiple-choice options A, B, C, D with letter and text")
    correct_choice: Optional[str] = Field(default=None, description="Letter of correct multiple-choice option (A, B, C, D)")
    question_type: str = Field(default="free_response", description="free_response or multiple_choice")
    difficulty: ProblemDifficulty = Field(default=ProblemDifficulty.MILD, description="Difficulty tier")
    bounding_box: Optional[BoundingBox] = Field(default=None, description="Pre-computed workspace bounding box")
    standards: List[str] = Field(default_factory=list, description="Curriculum standard codes (e.g., CCSS.MATH.CONTENT.HSA.REI.B.4)")
    diagram_svg: Optional[str] = Field(default=None, description="Optional SVG diagram/graph/table rendered in the problem prompt area")
    answer_svg: Optional[str] = Field(default=None, description="Optional SVG diagram/graph/plot rendered in the answer key")
    generator_id: Optional[str] = Field(default=None, description="Generator ID that produced this problem")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary generator metadata")

    @model_validator(mode="before")
    @classmethod
    def sanitize_math_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            def clean_str(val: str) -> str:
                if not isinstance(val, str):
                    return val
                # Strip redundant '+ 0' and '- 0' terms
                s = re.sub(r'(?<=[a-zA-Z0-9_\)])(\s*[+-]\s*0\b(?!\.))+', '', val)
                s = re.sub(r'(\b[+-]\s*0\b(?!\.)\s*)+', '', s)
                # Normalize unsimplified double signs in math expressions
                s = re.sub(r'\+\s*-\s*', '- ', s)
                s = re.sub(r'-\s*-\s*', '+ ', s)
                s = re.sub(r'\+\s*\+\s*', '+ ', s)
                s = re.sub(r'--(?=[0-9a-zA-Z])', '', s)
                # Normalize Typst arrows to standard double arrows/implications
                s = re.sub(r'\barrow\.r\.double\b', '==>', s)
                s = re.sub(r'\barrow\.r\b', '->', s)
                s = re.sub(r'\barrow\.l\.double\b', '<==', s)
                s = re.sub(r'\barrow\.l\b', '<-', s)
                s = re.sub(r'\barrow\.l\.r\.double\b', '<==>', s)
                s = re.sub(r'\barrow\.l\.r\b', '<->', s)
                # Replace legacy ^circle or ^\circle with standard degree symbol °
                s = re.sub(r'\^\\?circle\b', '°', s)
                s = re.sub(r'(\d|\)|theta|\b[a-zA-Z])\s*(?:deg|degrees)\b', r'\1°', s, flags=re.IGNORECASE)
                s = s.replace('&deg;', '°').replace('&#176;', '°')
                # Clean unsimplified unit coefficients: '+ 1y' -> '+ y', '- 1y' -> '- y', ' 1y' -> ' y'
                s = re.sub(r'([+\-=(,]\s*)1([a-zA-Z])\b', r'\1\2', s)
                s = re.sub(r'(^|\s)1([a-zA-Z])\b', r'\1\2', s)
                return s

            for key in ["equation_typst", "answer_typst", "prompt_text", "diagram_svg", "answer_svg"]:
                if key in data and isinstance(data[key], str):
                    data[key] = clean_str(data[key])
            if "prompt_text" in data and isinstance(data["prompt_text"], str):
                p = data["prompt_text"]
                p = re.sub(r'\bm\s+angle\s+([A-Za-z0-9_]+)\b', r'm∠\1', p, flags=re.IGNORECASE)
                p = re.sub(r'\bangle\s+([A-Z]{1,3})\b', r'∠\1', p)
                p = re.sub(r'\bm\s+angle\b', 'm∠', p, flags=re.IGNORECASE)
                p = re.sub(r'\btriangle\s+([A-Z]{3})\b', r'△\1', p)
                data["prompt_text"] = p
            if "steps_typst" in data and isinstance(data["steps_typst"], list):
                data["steps_typst"] = [clean_str(item) for item in data["steps_typst"]]
            if "distractors" in data and isinstance(data["distractors"], list):
                clean_ans = clean_str(data.get("answer_typst", "")).strip()
                seen = {clean_ans}
                unique_d = []
                for item in data["distractors"]:
                    cs = clean_str(item).strip()
                    if cs and cs not in seen:
                        seen.add(cs)
                        unique_d.append(cs)

                # Guarantee at least 3 distinct non-colliding distractors
                has_dollars = clean_ans.startswith("$") and clean_ans.endswith("$")
                stripped = clean_ans.replace("$", "").strip()
                offset = 1
                while len(unique_d) < 3:
                    if "=" in stripped:
                        vpart, valpart = stripped.split("=", 1)
                        try:
                            num = int(valpart.strip())
                            fb_raw = f"{vpart.strip()} = {num + offset}"
                        except Exception:
                            fb_raw = f"{stripped} + {offset}"
                    elif ">" in stripped:
                        vpart, valpart = stripped.split(">", 1)
                        try:
                            num = int(valpart.strip())
                            fb_raw = f"{vpart.strip()} > {num + offset}"
                        except Exception:
                            fb_raw = f"{stripped} + {offset}"
                    elif "<" in stripped:
                        vpart, valpart = stripped.split("<", 1)
                        try:
                            num = int(valpart.strip())
                            fb_raw = f"{vpart.strip()} < {num + offset}"
                        except Exception:
                            fb_raw = f"{stripped} + {offset}"
                    else:
                        fb_raw = f"{stripped} + {offset}"

                    fallback = f"$ {fb_raw} $" if has_dollars else fb_raw
                    if fallback not in seen:
                        seen.add(fallback)
                        unique_d.append(fallback)
                    offset += 1
                    if offset > 15:
                        break

                data["distractors"] = unique_d
        return data

    @model_validator(mode="after")
    def populate_latex_fields(self) -> BaseProblem:
        def typst_to_clean_latex(s: str) -> str:
            res = s.replace("$", "").replace("°", "^{\\circ}").strip()
            res = re.sub(r'\^\\?circle\b', r'^{\\circ}', res)

            # Protect strings in quotes so words like 'angle' inside text labels aren't transformed into math symbols
            quoted_strings: list[str] = []

            def _extract_quoted(match: re.Match) -> str:
                quoted_strings.append(match.group(1))
                return f"___LATEX_TEXT_{len(quoted_strings) - 1}___"

            res = re.sub(r'"([^"]*)"', _extract_quoted, res)

            # Convert Typst cases(...) into LaTeX \begin{cases} ... \end{cases}
            pos = 0
            while True:
                idx = res.find("cases(", pos)
                if idx == -1:
                    break
                start = idx + len("cases(")
                depth = 1
                end = -1
                for i in range(start, len(res)):
                    if res[i] == '(':
                        depth += 1
                    elif res[i] == ')':
                        depth -= 1
                        if depth == 0:
                            end = i
                            break
                if end == -1:
                    pos = idx + 6
                    continue

                inner = res[start:end]
                items: list[str] = []
                curr: list[str] = []
                d = 0
                for ch in inner:
                    if ch == '(':
                        d += 1
                        curr.append(ch)
                    elif ch == ')':
                        d -= 1
                        curr.append(ch)
                    elif ch == ',' and d == 0:
                        items.append("".join(curr).strip())
                        curr = []
                    else:
                        curr.append(ch)
                if curr:
                    items.append("".join(curr).strip())

                latex_cases = r"\begin{cases} " + r" \\ ".join(items) + r" \end{cases}"
                res = res[:idx] + latex_cases + res[end + 1:]
                pos = idx + len(latex_cases)

            # Clean unsimplified unit coefficients in LaTeX string
            res = re.sub(r'([+\-=(,]\s*)1([a-zA-Z])\b', r'\1\2', res)
            res = re.sub(r'(^|\s)1([a-zA-Z])\b', r'\1\2', res)

            # Convert Typst arrows to standard LaTeX
            res = re.sub(r'==>|\barrow\.r\.double\b', r'\\implies ', res)
            res = re.sub(r'->|\barrow\.r\b', r'\\to ', res)
            res = re.sub(r'<==>|\barrow\.l\.r\.double\b', r'\\iff ', res)
            res = re.sub(r'<==|\barrow\.l\.double\b', r'\\impliedby ', res)

            # Normalize unicode angle symbols
            res = re.sub(r'm∠([A-Za-z0-9_]+)', r'm\\angle \1', res)
            res = re.sub(r'∠([A-Za-z0-9_]+)', r'\\angle \1', res)
            res = res.replace('m∠', r'm\angle ').replace('∠', r'\angle ')

            # Normalize typst 'm angle' and 'angle'
            res = re.sub(r'\bm\s+angle\s+([A-Za-z0-9_]+)\b', r'm\\angle \1', res, flags=re.IGNORECASE)
            res = re.sub(r'(?<!\\)\bangle\s+([A-Z]{1,3})\b', r'\\angle \1', res)
            res = re.sub(r'\bm\s+angle\b', r'm\\angle ', res, flags=re.IGNORECASE)
            res = re.sub(r'\btriangle\s+([A-Za-z0-9_]+)\b', r'\\triangle \1', res)
            res = re.sub(r'\bquad\b', r'\\quad ', res)

            # Restore quoted strings wrapped in LaTeX \text{...}
            for idx, text in enumerate(quoted_strings):
                res = res.replace(f"___LATEX_TEXT_{idx}___", f"\\text{{{text}}}")

            return res.strip()

        if not self.equation_latex:
            self.equation_latex = typst_to_clean_latex(self.equation_typst)
        if not self.answer_latex:
            self.answer_latex = typst_to_clean_latex(self.answer_typst)
        return self


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
    question_type: str = Field(default="free_response", description="Question type: free_response or multiple_choice")


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
        seen_equations: set = set()

        for idx, difficulty in enumerate(tiers, start=1):
            prob: Optional[BaseProblem] = None
            # Retry up to 50 times with diverse RNG state to guarantee distinct problems in every batch
            for attempt in range(50):
                candidate = self.generate_single(
                    rng=rng,
                    difficulty=difficulty,
                    problem_idx=idx + attempt * 17,
                    allow_negatives=config.allow_negatives
                )
                eq_key = candidate.equation_typst.strip()
                if eq_key not in seen_equations or attempt == 49:
                    seen_equations.add(eq_key)
                    prob = candidate
                    break

            if prob is not None:
                prob.generator_id = self.generator_id
                prob.question_type = config.question_type
                if config.question_type == "multiple_choice":
                    self._populate_multiple_choice_choices(prob, rng)
                problems.append(prob)

        return problems

    def _populate_multiple_choice_choices(self, prob: BaseProblem, rng: random.Random) -> None:
        """Construct deterministic A, B, C, D multiple-choice options from answer and distractors."""
        clean_ans = prob.answer_typst.strip()
        distractors = [d.strip() for d in prob.distractors if d.strip() and d.strip() != clean_ans]

        # Deduplicate while preserving order
        seen = {clean_ans}
        unique_distractors = []
        for d in distractors:
            if d not in seen:
                seen.add(d)
                unique_distractors.append(d)

        # Synthesize fallback distractors if fewer than 3 are available
        offset = 1
        while len(unique_distractors) < 3:
            if clean_ans.startswith("$") and clean_ans.endswith("$"):
                inner = clean_ans[1:-1].strip()
                fallback = f"$ {inner} + {offset} $"
            else:
                fallback = f"{clean_ans} + {offset}"
            if fallback not in seen:
                seen.add(fallback)
                unique_distractors.append(fallback)
            offset += 1
            if offset > 10:
                break

        options = [clean_ans] + unique_distractors[:3]
        rng.shuffle(options)

        letters = ["A", "B", "C", "D"]
        choices = []
        correct_letter = "A"
        for i, opt in enumerate(options[:4]):
            let = letters[i]
            if opt == clean_ans:
                correct_letter = let
            choices.append({"letter": let, "text": opt})

        prob.choices = choices
        prob.correct_choice = correct_letter
