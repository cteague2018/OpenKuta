from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Tuple, Union

from backend.app.core.base import BaseProblem

# Regex to detect unparsed Python template tokens like {entity_a}, {deg}, etc.
# Exclude known Typst constructs like ^{...} or math subscripts if any, but template tokens are usually word identifiers
UNPARSED_TOKEN_REGEX = re.compile(r"(?<![\^_\\a-zA-Z])\{[a-zA-Z_][a-zA-Z0-9_]+\}")

# Corrupted LaTeX tokens resulting from unescaped Python string escapes:
# \a -> \x07 (bell), leaving 'rangle' from '\angle'
# \b -> \x08 (backspace), leaving 'eta' from '\beta'
# \f -> \x0c (formfeed), leaving 'rac' from '\frac'
# \t -> \x09 (tab), leaving 'heta' from '\theta' or 'an' from '\tan'
# \r -> \x0d (carriage return), leaving 'ho' from '\rho'
CORRUPTED_LATEX_PATTERNS = [
    (re.compile(r"\brangle\b", re.IGNORECASE), "Corrupted LaTeX: 'rangle' found (likely unescaped '\\angle' in non-raw string)"),
    (re.compile(r"\bmangle\b", re.IGNORECASE), "Corrupted LaTeX: 'mangle' found (likely 'm\\angle' unescaped)"),
    (re.compile(r"\brac\{", re.IGNORECASE), "Corrupted LaTeX: 'rac{' found (likely unescaped '\\frac' in non-raw string)"),
    (re.compile(r"(?<![a-zA-Z])\\x07"), "Raw ASCII bell character (\\x07) detected in string"),
    (re.compile(r"(?<![a-zA-Z])\\x08"), "Raw ASCII backspace character (\\x08) detected in string"),
    (re.compile(r"(?<![a-zA-Z])\\x0c"), "Raw ASCII formfeed character (\\x0c) detected in string"),
    (re.compile(r"(?<![a-zA-Z])\\x0b"), "Raw ASCII vertical tab character (\\x0b) detected in string"),
]

# Double signs that indicate unsimplified arithmetic
DOUBLE_SIGN_REGEX = re.compile(r"(?:[+\-]\s*-[0-9a-zA-Z]|[+\-]\s*\+[0-9a-zA-Z]|\+\s*-|-\s*\+|-\s*-|\+\s*\+)")

# Undefined / NaN / null tokens
FORBIDDEN_LITERALS = ["None", "[object Object]", "NaN", "null"]

# Whitespace-free Typst math identifiers/symbols that may appear unquoted inside
# $...$ content. worksheet.typ.j2 renders prompt_text/equation_typst/answer_typst
# straight into a markup content block, so any *other* bare multi-letter word makes
# Typst abort with "unknown variable: <word>".
TYPST_MATH_WORDS = frozenset(
    """
    sin cos tan cot sec csc sinh cosh tanh coth sech csch
    arcsin arccos arctan arccot arcsec arccsc
    log ln lg exp lim liminf limsup max min sup inf gcd lcm det dim mod
    quad space dot times div plus minus approx equiv leq geq neq lt gt le ge
    in not subset supset union inter emptyset oo infinity
    sum product int integral oint prod partial nabla forall exists therefore
    and or if else cases mat vec attach frac sqrt root abs floor ceil round angle
    left right arrow limits degree prime primes dif compose star circle square triangle
    parallel perp prop dots upright bold italic serif display inline script chevron binom
    bb cal scr frak op hat tilde vec overline underline text norm
    alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron
    pi rho sigma tau upsilon phi chi psi omega
    Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega
    NN ZZ QQ RR CC
    """.split()
)

# Bare multi-letter words inside math: not preceded by an escape, a '.' field
# access (arrow.r, dot.c) or a '#' code marker.
MATH_BARE_WORD_REGEX = re.compile(r"(?<![\\a-zA-Z.#])([a-zA-Z]{2,})(?![a-zA-Z])")

# Quoted strings inside math are legitimate text (e.g. $ "Vertex": (1, 2) $).
MATH_QUOTED_STRING_REGEX = re.compile(r'"(?:[^"\\]|\\.)*"')


def _count_unescaped(text: str, char: str) -> int:
    """Count occurrences of ``char`` that are not backslash-escaped."""
    count = 0
    i = 0
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == char:
            count += 1
        i += 1
    return count


def _split_typst_math(text: str) -> Tuple[List[str], List[str], bool]:
    """Split a field into (markup segments, math segments, math_terminated).

    Tracks backslash escapes and, inside math, ``"..."`` string literals so a
    quoted dollar sign is not mistaken for a delimiter.
    """
    markup: List[str] = []
    math: List[str] = []
    buf: List[str] = []
    in_math = False
    i = 0
    length = len(text)
    while i < length:
        ch = text[i]
        if ch == "\\" and i + 1 < length:
            buf.append(text[i:i + 2])
            i += 2
            continue
        if ch == "$":
            (math if in_math else markup).append("".join(buf))
            buf = []
            in_math = not in_math
            i += 1
            continue
        if in_math and ch == '"':
            j = i + 1
            while j < length and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            buf.append(text[i:j + 1])
            i = j + 1
            continue
        buf.append(ch)
        i += 1
    (math if in_math else markup).append("".join(buf))
    return markup, math, not in_math


def _audit_text_field(text: str, field_name: str) -> List[str]:
    """Audit a single string field for typographic, escaping, and formatting defects."""
    errors: List[str] = []
    if not isinstance(text, str):
        return [f"Field '{field_name}' is not a string (type: {type(text).__name__})"]

    # 1. ASCII Control Characters (Bell, Backspace, Formfeed, Vertical Tab)
    for ctrl_code, ctrl_name in [("\x07", "Bell (\\x07)"), ("\x08", "Backspace (\\x08)"), ("\x0c", "Formfeed (\\x0c)"), ("\x0b", "VTab (\\x0b)")]:
        if ctrl_code in text:
            errors.append(f"Field '{field_name}' contains illegal ASCII control character: {ctrl_name}")

    # 2. Corrupted LaTeX patterns
    for pat, desc in CORRUPTED_LATEX_PATTERNS:
        if pat.search(text):
            errors.append(f"Field '{field_name}' has {desc}")

    # 3. Unparsed Template Tokens (e.g. {deg}, {entity_b}, {variable})
    # Filter out valid Typst sets like {1, 2, 3} or cases(1, 2)
    unparsed_matches = UNPARSED_TOKEN_REGEX.findall(text)
    for m in unparsed_matches:
        # Ignore if it's purely digits or standard set syntax
        inner = m[1:-1]
        if not inner.isdigit():
            errors.append(f"Field '{field_name}' contains unparsed template token '{m}'")

    # 4. Forbidden literal artifacts
    for lit in FORBIDDEN_LITERALS:
        # Look for literal as standalone word
        if re.search(rf"\b{re.escape(lit)}\b", text):
            errors.append(f"Field '{field_name}' contains forbidden literal token '{lit}'")

    # 5. Math delimiter parity + markup safety.
    # Typst toggles math with unescaped '$'; inside math, "$" only counts as a
    # delimiter when it is not part of a "..." string literal.
    markup_parts, math_parts, math_terminated = _split_typst_math(text)
    if not math_terminated:
        errors.append(f"Field '{field_name}' has unbalanced math delimiters: unterminated '$'")
    for part in markup_parts:
        # Everything outside $...$ lands inside the [ ... ] content block of
        # worksheet.typ.j2, where '*' toggles strong emphasis, '[' opens a nested
        # block and 'sub_(' starts a math-style subscript. Each of those aborts
        # the whole document with "unclosed delimiter" when left unbalanced.
        # (A lone '_' in prose such as "S_n" is tolerated by Typst and is not flagged.)
        if _count_unescaped(part, "*") % 2:
            errors.append(
                f"Field '{field_name}' has an unbalanced strong-emphasis '*' outside math; "
                f"Typst aborts with \"unclosed delimiter\" (use a $ ... $ math span instead)"
            )
        if _count_unescaped(part, "[") != _count_unescaped(part, "]"):
            errors.append(
                f"Field '{field_name}' has unbalanced '[' / ']' outside math; "
                f"escape literal brackets as \\[ and \\] or wrap them in $ ... $"
            )
        if "_(" in part:
            errors.append(
                f"Field '{field_name}' uses math subscript syntax '_(' outside math; "
                f"wrap that expression in $ ... $"
            )
    for part in math_parts:
        if _count_unescaped(part, '"') % 2:
            errors.append(f"Field '{field_name}' has an unterminated quote inside $ ... $ math")
        # Bare multi-letter words are read as identifiers by Typst and abort the
        # compile with "unknown variable: <word>"; prose must be quoted.
        for word in MATH_BARE_WORD_REGEX.findall(MATH_QUOTED_STRING_REGEX.sub(" ", part)):
            if word in TYPST_MATH_WORDS:
                continue
            errors.append(
                f"Field '{field_name}' uses the bare word '{word}' inside $ ... $ math; "
                f"quote it as \"{word}\" (Typst would report: unknown variable: {word})"
            )

    # 6. Double signs (e.g., '+ -' or '- -')
    # Skip if inside text explanations or set definitions, but flag in math equations
    if field_name in ["equation_typst", "answer_typst"]:
        # Find double signs that are not '+-' for plus-minus
        m_ds = DOUBLE_SIGN_REGEX.search(text)
        if m_ds:
            errors.append(f"Field '{field_name}' contains unsimplified double sign: '{m_ds.group(0)}'")

    # 7. Raw HTML entities in text fields (e.g. &#176; or &amp;)
    if "&#" in text or "&amp;#" in text or "&deg;" in text:
        errors.append(f"Field '{field_name}' contains raw HTML entity: use UTF-8 characters like '°' instead")

    return errors


def _audit_svg(svg_str: str, field_name: str) -> List[str]:
    """Audit an SVG string for XML well-formedness, viewBox validity, and geometric integrity."""
    errors: List[str] = []
    if not svg_str or not isinstance(svg_str, str):
        return [f"Field '{field_name}' is empty or not a string"]

    # 1. XML Well-Formedness
    try:
        root = ET.fromstring(svg_str)
    except ET.ParseError as e:
        return [f"Field '{field_name}' failed XML parsing: {str(e)}"]

    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag != "svg":
        errors.append(f"Field '{field_name}' root element is '<{tag}>', expected '<svg>'")

    # 2. ViewBox Validity
    viewbox = root.attrib.get("viewBox")
    if viewbox:
        vb_parts = viewbox.strip().split()
        if len(vb_parts) == 4:
            try:
                min_x, min_y, w, h = [float(p) for p in vb_parts]
                if w <= 0 or h <= 0:
                    errors.append(f"Field '{field_name}' viewBox has non-positive width/height ({w}x{h})")
            except ValueError:
                errors.append(f"Field '{field_name}' viewBox contains invalid numeric values: '{viewbox}'")
        else:
            errors.append(f"Field '{field_name}' viewBox does not have 4 coordinate parameters: '{viewbox}'")

    # 3. Text Elements Validation (Check for unescaped tokens or template mash)
    # Search all text tags (with or without SVG namespace)
    for text_el in root.iter():
        t_tag = text_el.tag.split("}")[-1] if "}" in text_el.tag else text_el.tag
        if t_tag == "text":
            content = (text_el.text or "").strip()
            if "{" in content or "}" in content:
                errors.append(f"Field '{field_name}' text element contains unparsed template token: '{content}'")
            if any(lit in content for lit in ["NaN", "undefined", "[object Object]"]):
                errors.append(f"Field '{field_name}' text element contains invalid literal: '{content}'")
            if "_degrees" in content or "deg" in content and "{" in content:
                errors.append(f"Field '{field_name}' text element contains template artifact: '{content}'")

    # 4. Path and Arc Geometry Check
    # Verify arc paths <path d="... A rx ry rot large_arc sweep x y ...">
    for path_el in root.iter():
        p_tag = path_el.tag.split("}")[-1] if "}" in path_el.tag else path_el.tag
        if p_tag == "path":
            d = path_el.attrib.get("d", "")
            # Check for NaN in path commands
            if "nan" in d.lower():
                errors.append(f"Field '{field_name}' path 'd' attribute contains NaN: '{d}'")

    return errors


def validate_generated_problem(problem: Union[BaseProblem, Dict[str, Any]]) -> List[str]:
    """
    Universal Problem Sanity Linter.
    Inspects every field of a generated problem payload for:
    1. LaTeX escaping & control characters
    2. Template token completeness
    3. SVG well-formedness and geometric consistency
    4. Mathematical formatting and delimiter balance
    """
    errors: List[str] = []

    # Normalize to dictionary
    if isinstance(problem, BaseProblem):
        p_dict = problem.model_dump()
    elif isinstance(problem, dict):
        p_dict = problem
    else:
        return [f"Invalid problem object type: {type(problem).__name__}"]

    # Required String Fields
    req_fields = ["prompt_text", "equation_typst", "answer_typst"]
    for rf in req_fields:
        val = p_dict.get(rf)
        if not val or not isinstance(val, str) or not val.strip():
            errors.append(f"Missing or empty required field: '{rf}'")
        else:
            errors.extend(_audit_text_field(val, rf))

    # List Fields (steps_typst, distractors)
    for lf in ["steps_typst", "distractors"]:
        items = p_dict.get(lf, [])
        if isinstance(items, list):
            for idx, item in enumerate(items):
                if isinstance(item, str):
                    errors.extend(_audit_text_field(item, f"{lf}[{idx}]"))
                else:
                    errors.append(f"Item {idx} in '{lf}' is not a string (type: {type(item).__name__})")

    # Multiple Choice Choices
    choices = p_dict.get("choices", [])
    if isinstance(choices, list) and len(choices) > 0:
        for idx, ch in enumerate(choices):
            if isinstance(ch, dict):
                text_val = ch.get("text", "")
                errors.extend(_audit_text_field(text_val, f"choices[{idx}].text"))
            else:
                errors.append(f"Choice {idx} is not a dict")

    # SVG Validation
    for svg_field in ["diagram_svg", "answer_svg"]:
        svg_content = p_dict.get(svg_field)
        if svg_content:
            errors.extend(_audit_svg(svg_content, svg_field))

    return errors


def validate_problem_sanity(problem: Any) -> None:
    errors = validate_generated_problem(problem)
    if errors:
        raise ValueError(
            f"Problem sanity validation failed with {len(errors)} defects:\n"
            + "\n".join(f"  - {err}" for err in errors)
        )
