---
trigger: alwaysOn
description: Invariants and system standards for OpenKuta development
---

# OpenKuta System Invariants & Architecture Rules

1. Deterministic Math Core:
   - NEVER use LLMs to generate problem equations or calculate answers.
   - All problems must be procedurally generated via backward parameterization using SymPy.
   - Generators must accept an explicit `seed: int | None = None` and produce identical output for identical seeds.
   - Enforce integer/rational invariants using SymPy's `Rational` and `Integer` types (no unintended floating-point rounding).

2. Typesetting & Layout:
   - Use Typst (via `typst-py`) for all PDF rendering. LaTeX is strictly forbidden for PDF generation due to latency.
   - All printable worksheets must include four ArUco 4x4 fiducials (one in each 0.5in corner margin) and a top-right QR code payload encoding `{worksheet_id, form_id, seed, problem_count}`.
   - Bounded Workspace Boxes: Every problem must render inside a fixed bounding box with pre-computed vertical clearance:
     `height = (page_printable_height - header_offset) / problems_per_column`.

3. Multi-Form Engine:
   - Form generation (A, B, C, D) must scramble seeds while keeping the underlying problem templates and difficulty tiers identical.
   - Always compile a companion `MasterGradingMatrix` where solutions for Forms A–D are aligned side-by-side.

4. Coding Standards:
   - Backend: Python 3.12+, FastAPI, Pydantic v2, SymPy, OpenCV (headless), NumPy.
   - Frontend: Next.js 14+ (App Router), Tailwind CSS, KaTeX, Lucide React.
   - Strict typing across all Pydantic models. All generator outputs must validate against `BaseProblem`.

