# Role: Deterministic CAS & Procedural Generator Specialist
Objective: Build backward-parameterized math problem generators using SymPy with strict deterministic seeds.

Deliverables in `backend/app/core/` & `backend/app/generators/`:
1. `backend/app/core/base.py`:
   - `ProblemDifficulty` enum (MILD, MEDIUM, SPICY).
   - `BoundingBox` model for pixel/typst workspace boundaries.
   - `BaseProblem` Pydantic v2 model (id, prompt_text, equation_typst, answer_typst, steps_typst, distractors, bounding_box).
   - `GeneratorConfig` Pydantic v2 model (problem_count, difficulty_distribution, allow_negatives, seed, form_ids).
   - `BaseGenerator` abstract base class defining `generate(config)` interface.
2. `backend/app/generators/algebra_1/quadratics.py`:
   - Factoring ($a=1$, $a \ne 1$, difference of squares).
   - Completing the square (yielding rational or radical answers).
   - Quadratic formula with radical simplification.
3. `backend/app/generators/algebra_1/two_step_equations.py`:
   - Linear equations $a x + b = c$ with rational parameterization.
   - Distractor generator targeting common algebraic misconceptions (dropping signs, wrong inverse operations).

