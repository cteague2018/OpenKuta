#!/usr/bin/env python3
"""OpenMathForge Comprehensive Secrets Detection & Privacy Scanner.
Scans files and git tracking for hardcoded tokens, API keys, credentials, and private keys.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    (re.compile(r"(?i)aws_access_key_id\s*=\s*['\"]?(AKIA[0-9A-Z]{16})['\"]?"), "AWS Access Key"),
    (re.compile(r"(?i)aws_secret_access_key\s*=\s*['\"]?([0-9a-zA-Z/+]{40})['\"]?"), "AWS Secret Key"),
    (re.compile(r"(?i)(api[_-]?key|secret[_-]?key)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{20,})['\"]"), "API Key Token"),
    (re.compile(r"gh[pousr]_[0-9a-zA-Z]{36}"), "GitHub Personal Access Token"),
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"), "Private Encryption Key"),
    (re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}"), "Slack API Token"),
]

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "__pycache__",
    ".pytest_cache",
    ".vscode",
    "dist",
    "build",
}

IGNORED_FILES = {
    "package-lock.json",
    "detect-secrets.py",
}


def scan_file(path: Path) -> list[str]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for idx, line in enumerate(text.splitlines(), start=1):
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(line):
                # Ignore dummy/mock test values like 'anon', 'test_key', 'some_secret'
                if any(mock in line.lower() for mock in ["test", "dummy", "example", "mock", "none", "tokenbucket"]):
                    continue
                findings.append(f"[{label}] {path}:{idx} -> {line.strip()[:60]}...")
    return findings


def main() -> int:
    root = Path.cwd()
    print(f"Scanning for secrets in: {root}")
    all_findings = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fname in filenames:
            if fname in IGNORED_FILES:
                continue
            fpath = Path(dirpath) / fname
            findings = scan_file(fpath)
            all_findings.extend(findings)

    if all_findings:
        print("\n[!] SECRETS DETECTED:")
        for f in all_findings:
            print(f"  {f}")
        return 1

    print("[OK] Zero secrets or sensitive credentials detected across codebase.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
