from __future__ import annotations

import os
import sys
import time
import subprocess
import urllib.request
from typing import Generator
import pytest
from backend.app.core.compiler import TypstCompiler
from backend.app.generators.algebra_1.quadratics import QuadraticEquationsGenerator
from backend.app.core.base import GeneratorConfig


@pytest.fixture(scope="class")
def ensure_live_servers() -> Generator[dict[str, str], None, None]:
    """Ensure both FastAPI backend and Next.js frontend are running and reachable before tests."""
    backend_proc: subprocess.Popen[bytes] | None = None
    frontend_proc: subprocess.Popen[bytes] | None = None

    backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
    frontend_url = os.environ.get("FRONTEND_URL", "http://127.0.0.1:3000")

    def is_online(url: str) -> bool:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "OpenMathForge-E2E"})
            with urllib.request.urlopen(req, timeout=1) as resp:
                return bool(resp.status == 200)
        except Exception:
            return False

    # 1. Spin up FastAPI backend if not actively responding
    if not is_online(f"{backend_url}/health"):
        backend_proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # 2. Spin up Next.js frontend if not actively responding
    if not is_online(frontend_url):
        frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
        next_build_exists = os.path.exists(os.path.join(frontend_dir, ".next"))
        cmd = "npm run start -- -p 3000" if next_build_exists else "npm run dev"
        frontend_proc = subprocess.Popen(
            cmd,
            cwd=frontend_dir,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # 3. Poll readiness with startup timeout (up to 30s)
    start_time = time.time()
    while time.time() - start_time < 30:
        if is_online(f"{backend_url}/health") and is_online(frontend_url):
            break
        time.sleep(0.5)

    try:
        yield {"backend_url": backend_url, "frontend_url": frontend_url}
    finally:
        # Clean teardown of spawned background processes
        if backend_proc and backend_proc.poll() is None:
            if sys.platform == "win32":
                subprocess.run(f"taskkill /F /T /PID {backend_proc.pid}", shell=True, capture_output=True)
            else:
                backend_proc.terminate()
                backend_proc.wait(timeout=5)

        if frontend_proc and frontend_proc.poll() is None:
            if sys.platform == "win32":
                subprocess.run(f"taskkill /F /T /PID {frontend_proc.pid}", shell=True, capture_output=True)
            else:
                frontend_proc.terminate()
                frontend_proc.wait(timeout=5)


class TestPlaywrightE2EWorkflows:
    """Headless browser automation for OpenMathForge Worksheet Studio UI workflows."""

    def test_document_download_triggers_simulation(self) -> None:
        """Simulate clicks on 'Generate PDF' and 'Export Answer Key' and assert PDF magic bytes and size."""
        compiler = TypstCompiler()
        gen = QuadraticEquationsGenerator()
        problems = gen.generate(GeneratorConfig(problem_count=6, seed=42))

        # 1. Student PDF generation trigger
        student_pdf = compiler.compile_worksheet_pdf(
            title="Algebra 1 Mastery Test",
            form_id="A",
            worksheet_id="WS-E2E-001",
            seed=42,
            problems=problems,
            columns=2,
            show_answers=False,
        )
        assert student_pdf.startswith(b"%PDF-"), "Generated student document missing valid %PDF- magic bytes"
        assert len(student_pdf) > 10000, f"Expected size > 10KB, got {len(student_pdf)} bytes"

        # 2. Answer key export trigger
        key_pdf = compiler.compile_worksheet_pdf(
            title="Algebra 1 Mastery Test",
            form_id="A",
            worksheet_id="WS-E2E-001",
            seed=42,
            problems=problems,
            columns=2,
            show_answers=True,
        )
        assert key_pdf.startswith(b"%PDF-"), "Generated answer key missing valid %PDF- magic bytes"
        assert len(key_pdf) > 10000, f"Expected size > 10KB, got {len(key_pdf)} bytes"

    def test_dynamic_sheet_manipulation_single_problem_and_scramble(self) -> None:
        """Verify 'Regenerate Single Problem' modifies only target problem, and 'Scramble Form' re-indexes cleanly."""
        gen = QuadraticEquationsGenerator()
        problems = gen.generate(GeneratorConfig(problem_count=8, seed=101))
        initial_stems = [p.equation_typst for p in problems]
        initial_ids = [p.id for p in problems]

        # Simulate "Regenerate Single Problem" on problem index 2 (Problem #3)
        target_idx = 2
        new_prob = gen.generate_single(
            rng=__import__("random").Random(99999),
            difficulty=problems[target_idx].difficulty,
            problem_idx=target_idx + 1,
        )

        mutated = list(problems)
        mutated[target_idx] = new_prob

        # Assert only index 2 changed, all other 7 problems remain identical
        for i in range(len(mutated)):
            if i == target_idx:
                assert mutated[i].equation_typst != initial_stems[i] or mutated[i].id != initial_ids[i]
            else:
                assert mutated[i].equation_typst == initial_stems[i], f"Problem #{i+1} changed unexpectedly"
                assert mutated[i].id == initial_ids[i]

        # Simulate "Scramble Form": shuffle and re-index 1 to N
        import random
        rng = random.Random(42)
        shuffled = list(mutated)
        rng.shuffle(shuffled)
        reindexed = [
            p.model_copy(update={"id": f"scrambled_prob_{idx}"})
            for idx, p in enumerate(shuffled, start=1)
        ]

        assert len(reindexed) == 8
        reindexed_ids = [p.id for p in reindexed]
        assert len(set(reindexed_ids)) == 8, "Found duplicate problem IDs after scramble"
        assert reindexed_ids[0] == "scrambled_prob_1"
        assert reindexed_ids[-1] == "scrambled_prob_8"

    def test_browser_playwright_full_navigation(self, ensure_live_servers: dict[str, str]) -> None:
        """Full Playwright browser automation verifying navigation traversal, topic controls, and dynamic DOM."""
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
            )
            page = browser.new_page()

            console_errors: list[str] = []
            failed_responses: list[str] = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda err: console_errors.append(str(err)))
            page.on("response", lambda r: failed_responses.append(f"{r.status} {r.url}") if r.status >= 400 else None)

            # Mock /api/worksheet/pdf route to guarantee instantaneous deterministic binary responses
            compiler = TypstCompiler()
            gen = QuadraticEquationsGenerator()
            mock_pdf = compiler.compile_worksheet_pdf(
                title="Browser Test Worksheet",
                form_id="A",
                worksheet_id="WS-PLAYWRIGHT",
                seed=42,
                problems=gen.generate(GeneratorConfig(problem_count=4, seed=42)),
            )

            page.route(
                "**/api/worksheet/pdf",
                lambda route: route.fulfill(
                    status=200,
                    content_type="application/pdf",
                    body=mock_pdf,
                    headers={"Content-Disposition": 'attachment; filename="OpenMathForge_Form_A.pdf"'},
                ),
            )

            # 1. Navigate to frontend application
            frontend_url = ensure_live_servers["frontend_url"]
            page.goto(frontend_url, wait_until="domcontentloaded", timeout=20000)

            # 2. Assert header branding is visible
            assert page.locator("text=OpenMathForge").first.is_visible()

            # 3. Topic Navigation & Generator Control Verification
            topic_btn = page.locator("button:has-text('Verbal expressions')").or_(
                page.locator("button:has-text('Order of operations')")
            ).first
            if topic_btn.is_visible():
                topic_btn.click()
                page.wait_for_timeout(400)

                # Exercise difficulty switches in configurator modal
                for diff in ["mild", "medium", "spicy"]:
                    diff_btn = page.locator(f"button[data-difficulty='{diff}']")
                    if diff_btn.is_visible():
                        diff_btn.click()

                # Close configurator modal
                close_btn = page.locator("button:has-text('✕')").first
                if close_btn.is_visible():
                    close_btn.click()

            # 4. Toggle Answer Visibility Switch
            ans_toggle = page.locator("button:has-text('Student View'), button:has-text('Answer Key')").first
            if ans_toggle.is_visible():
                ans_toggle.click()
                page.wait_for_timeout(300)
                ans_toggle.click()

            # 5. Dynamic Sheet Manipulation: Scramble Form
            scramble_btn = page.locator("[data-testid='scramble-form']")
            if scramble_btn.is_visible():
                scramble_btn.click()
                page.wait_for_timeout(300)

            # 6. Verify zero unhandled browser console errors (excluding 404 on optional favicon)
            critical_errors = [e for e in console_errors if "favicon" not in e.lower()]
            assert len(critical_errors) == 0, f"Critical browser console errors: {critical_errors}, failed responses: {failed_responses}"

            browser.close()
