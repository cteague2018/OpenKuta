# OpenMathForge 📐⚡

[![Live Web Application](https://img.shields.io/badge/Live%20App-openmathforge.vercel.app-blue?style=flat-square)](https://openmathforge.vercel.app)
[![Production Quality Gates](https://github.com/cteague2018/OpenMathForge/actions/workflows/openmathforge-production-gates.yml/badge.svg)](https://github.com/cteague2018/OpenMathForge/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

An open-source, web-based algorithmic mathematics engine and curriculum generator built with SymPy and Typst as a modern, high-performance web platform.

OpenMathForge integrates procedural mathematical generation, sub-100ms vector typesetting, computer vision marker deskewing, symbolic CAS partial-credit grading, LMS roster synchronization, and IMS QTI 2.1 export.

---

## 🏗️ Architecture & Features

1. **Deterministic CAS Math Core & 598-Topic 1:1 Curriculum Engine**
   - Procedural backward parameterization via **SymPy**. Zero LLM hallucinations, guaranteed integer/rational invariants, full seed determinism.
   - **100% 1-to-1 Curriculum Coverage**: All **598 curriculum topics and subtopics** across 7 courses (`grade_6`, `pre_algebra`, `algebra_1`, `geometry`, `algebra_2`, `precalculus`, and `calculus`) map to dedicated, dynamically registered topic generators (`generator_id == topic.id`) alongside 73 base domain generators (`671` total registered generators).
   - **Difficulty-Invariant Subtopic Fidelity**: Every topic and subtopic generates strictly relevant problems at all 3 difficulty tiers (`mild`, `medium`, `spicy`) without cross-topic multiplexing, verified by automated forensic audit suites (`backend/tests/test_forensic_topic_audit.py` and `tests/functional/test_topic_problem_integrity.py`).
2. **Vector SVG Visuals, Graphs, Geometric Diagrams & Data Tables**
   - Pure-Python deterministic SVG engine (`backend/app/core/svg_utils.py`) generating publication-grade vector graphics (`diagram_svg` for problem prompts and `answer_svg` for plotted answer keys):
     - **Coordinate Planes & Function Plotters**: Linear equations, inequalities with half-plane shading, systems of equations/inequalities, quadratics, polynomials, rationals with asymptotes, exponentials, logarithms, piecewise functions, conics, polar grids, slope fields, and Riemann sum rectangles/shaded integrals.
     - **Number Lines**: Single and compound inequalities with open/closed boundary circles and directional rays.
     - **Geometric Figures**: Labeled right and general triangles, parallel lines cut by a transversal, polygons, circles with radii/chords/arcs/secants, and 3D solids (prisms, cylinders, cones, spheres, pyramids).
     - **Statistical Plots & Structured Tables**: Box-and-whisker plots, histograms/dot plots, stem-and-leaf plots, Venn diagrams, two-way frequency tables, and calculus function/derivative tables.
3. **Typesetting & Anti-Cheating Document Engine**
   - Sub-100ms compilation via **Typst** (`typst-py`) with native inline SVG rendering (`image.decode`) for both problem prompts and multi-form answer keys.
   - 4 ArUco 4x4 corner fiducials and metadata QR codes `{worksheet_id, form_id, seed, student_id}`.
   - Dynamic workspace clearance calculation to eliminate page overruns.
   - 4-form multi-scramble (Forms A, B, C, D) with unified 4-column master grading matrix.
4. **Computer Vision & CAS Grading**
   - OpenCV fiducial detection, perspective warp to canonical US-Letter (2550x3300 px at 300 DPI), and workspace box slicing.
   - SymPy step-difference CAS verifier ($\Delta = \text{simplify}(S_k - S_{k-1}) == 0$).
   - Automated error classification: arithmetic, sign, distribution, conceptual, with partial credit scoring.
5. **Classroom Management & Auto-Gradebook**
   - 1-click roster import supporting **Google Classroom**, **Canvas LMS**, **Clever**, and **OneRoster** CSVs.
   - Batch personalized PDF generation with unique student QR codes.
   - Direct grade sync into local class gradebooks.
6. **EdTech LMS Export**
   - Canvas-compliant **QTI 2.1** XML and ZIP package export with CCSS-M and TEKS curriculum tagging.
7. **Modern Studio UI**
   - Next.js 14 App Router, Tailwind CSS, KaTeX live mathematical preview, interactive inline SVG diagram/graph rendering for problems and answer keys, assignment tray, and camera vision grader dropzone.

---

## 🚀 Quick Start

### 1. Backend (FastAPI + CAS Core)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate # On macOS/Linux

# Install backend dependencies
pip install -e .

# Run test suite
pytest -v

# Start FastAPI server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend (Next.js 14 Studio)
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the OpenMathForge Studio.

---

## 🌐 Deployment to Vercel & Render

### Frontend (Vercel)
- Set Root Directory to `frontend`.
- Set Environment Variable `BACKEND_URL` to your deployed FastAPI backend URL on Render (e.g., `https://openmathforge-backend.onrender.com`).

### Backend (Render)
- Configured via `render.yaml` with automated Docker build (`Dockerfile`).

---

## ⚖️ Open Source & Privacy Mission
OpenMathForge is an independent, community-driven free and open-source software project released under the MIT License. Built for mathematics educators worldwide, it provides modern algorithmic authoring, high-speed Typst vector compilation, and local-first zero-PII privacy protection.

---

## 📄 License
MIT License. Open source and built for educators worldwide.
