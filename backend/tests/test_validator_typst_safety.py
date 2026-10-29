"""Regression tests for the Typst-safety rules in ``validate_generated_problem``.

``worksheet.typ.j2`` renders ``prompt_text``/``equation_typst``/``answer_typst`` and the
multiple-choice choices straight into a markup content block, so a stray ``*``, an
unbalanced ``[`` or a bare prose word inside ``$ ... $`` aborts the whole worksheet
compile with "unclosed delimiter" / "unknown variable". These cases pin the rules that
were added after the 671-generator sweep found 38 topics that could not compile.
"""

from backend.app.generators.validator import validate_generated_problem


def _errors(**fields: object) -> list[str]:
    payload = {
        "prompt_text": "Solve each problem.",
        "equation_typst": "$ x + 1 = 2 $",
        "answer_typst": "$ x = 1 $",
        "steps_typst": ["Isolate $x$."],
        "distractors": [],
    }
    payload.update(fields)
    return validate_generated_problem(payload)


def test_clean_problem_has_no_defects() -> None:
    assert _errors() == []


def test_bare_prose_word_inside_math_is_rejected() -> None:
    errors = _errors(answer_typst='$ Vertex: (1, 2) $')
    assert any("bare word" in e and "Vertex" in e for e in errors)


def test_quoted_prose_inside_math_is_accepted() -> None:
    assert _errors(answer_typst='$ "Vertex": (1, 2) $') == []
    assert _errors(answer_typst='$ "Asymptote": y = -2; "y-int": (0, -3) $') == []


def test_typst_math_symbols_are_accepted_unquoted() -> None:
    assert _errors(equation_typst="$ chevron.l sin(theta) = binom(n, k) norm(v) $") == []


def test_escaped_dollar_inside_math_keeps_delimiters_balanced() -> None:
    # The rates generators used to emit "\$45$ per item", where the leading '$' is
    # swallowed by the escape and the trailing one opens an unterminated math span.
    good = _errors(answer_typst="$ \\$45 $ per item")
    assert good == []
    bad = _errors(answer_typst="\\$45$ per item")
    assert any("unbalanced math delimiters" in e for e in bad)


def test_unbalanced_strong_emphasis_outside_math_is_rejected() -> None:
    errors = _errors(answer_typst="3.0 * 10^5")
    assert any("strong-emphasis" in e for e in errors)


def test_math_subscript_outside_math_is_rejected() -> None:
    errors = _errors(equation_typst="lim_(x -> 2) (2 x^2 + 3 x - 5)")
    assert any("subscript syntax" in e for e in errors)


def test_unbalanced_bracket_outside_math_is_rejected() -> None:
    errors = _errors(prompt_text="Solve the equation on the interval [0, 2pi).")
    assert any("unbalanced '['" in e for e in errors)
    assert _errors(prompt_text="Solve the equation on the interval $[0, 2pi)$.") == []


def test_lone_underscore_in_prose_is_tolerated() -> None:
    # Typst tolerates "S_n" in markup, so this must not be flagged as a defect.
    assert _errors(prompt_text="Evaluate the sum S_n of the finite arithmetic series.") == []


def test_derivative_notation_in_steps_uses_spaced_differential() -> None:
    assert _errors(steps_typst=["Recall $ (d)/(d x)[sin(u)] = cos(u) u' $."]) == []
    errors = _errors(steps_typst=["Recall $ d/dx[sin(u)] = cos(u) u' $."])
    assert any("bare word" in e and "dx" in e for e in errors)
