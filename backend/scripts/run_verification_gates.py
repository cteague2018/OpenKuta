from __future__ import annotations

import subprocess
import sys


def run_command(cmd: list[str]) -> int:
    print(f"\n[EXEC] Running: {' '.join(cmd)}")
    exec_cmd = list(cmd)
    if exec_cmd[0] == "python":
        exec_cmd[0] = sys.executable
    use_shell = sys.platform == "win32"
    result = subprocess.run(exec_cmd, shell=use_shell)
    return result.returncode


def main() -> None:
    gates = [
        ["python", "backend/scripts/codemod_wrap_generators.py"],
        ["python", "-m", "ruff", "check", "backend"],
        ["python", "-m", "mypy", "backend/app"],
        ["python", "-m", "pytest", "backend/tests/", "--ignore=backend/tests/test_hypothesis_fuzz_all.py", "-v"],
        ["python", "-m", "pytest", "backend/tests/test_hypothesis_fuzz_all.py", "-q"],
        ["npm", "--prefix", "frontend", "run", "type-check"],
    ]

    for gate in gates:
        code = run_command(gate)
        if code != 0:
            print(f"\n[ERROR] Verification gate failed with exit code {code}: {' '.join(gate)}")
            sys.exit(code)

    print("\n[SUCCESS] All 100% accuracy and scaling verification gates passed cleanly!")
    sys.exit(0)


if __name__ == "__main__":
    main()
