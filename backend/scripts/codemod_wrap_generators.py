from __future__ import annotations

import ast
import os
import re

TARGET_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "generators")


class GeneratorCodemodTransformer(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.modified = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.generic_visit(node)
        if node.name.startswith("generate_") and not any(
            (isinstance(d, ast.Name) and d.id == "verify_mathematical_truth")
            or (isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "verify_mathematical_truth")
            for d in node.decorator_list
        ):
            node.decorator_list.append(
                ast.Call(
                    func=ast.Name(id="verify_mathematical_truth", ctx=ast.Load()),
                    args=[],
                    keywords=[],
                )
            )
            self.modified = True
        return node


def instrument_file_source(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    try:
        tree = ast.parse(src, filename=path)
    except Exception:
        return False

    transformer = GeneratorCodemodTransformer()
    transformer.visit(tree)

    if not transformer.modified:
        return False

    import_stmt = "from backend.app.generators.verification_gate import verify_mathematical_truth\n"
    has_import = "verify_mathematical_truth" in src

    lines = src.splitlines(keepends=True)
    new_lines: list[str] = []
    import_inserted = has_import

    for line in lines:
        new_lines.append(line)
        if not import_inserted and "from __future__ import annotations" in line:
            new_lines.append(import_stmt)
            import_inserted = True

        match = re.match(r"^(\s*)def (generate_[a-zA-Z0-9_]*)\s*\(", line)
        if match:
            # We want to insert the decorator BEFORE def line
            def_line = new_lines.pop()
            indent = match.group(1)
            prev_chunk = "".join(new_lines[-3:]) if len(new_lines) >= 3 else "".join(new_lines)
            if "@verify_mathematical_truth" not in prev_chunk:
                new_lines.append(f"{indent}@verify_mathematical_truth()\n")
            new_lines.append(def_line)

    if not import_inserted:
        new_lines.insert(0, import_stmt)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(new_lines)

    return True


def run_codemod() -> None:
    count = 0
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".py") and file != "verification_gate.py":
                path = os.path.join(root, file)
                if instrument_file_source(path):
                    count += 1
    print(f"Codemod complete: All generators instrumented with @verify_mathematical_truth ({count} files updated).")


if __name__ == "__main__":
    run_codemod()

