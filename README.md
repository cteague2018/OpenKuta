# OpenMathForge 📐⚡

[![Live Web Application](https://img.shields.io/badge/Live%20App-openmathforge.vercel.app-blue?style=flat-square)](https://openmathforge.vercel.app)
[![Production Quality Gates](https://github.com/cteague2018/OpenMathForge/actions/workflows/openmathforge-production-gates.yml/badge.svg)](https://github.com/cteague2018/OpenMathForge/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

An open-source, web-based algorithmic mathematics engine and curriculum generator built with SymPy and Typst as a modern, high-performance web platform.

OpenMathForge integrates procedural mathematical generation, sub-100ms vector typesetting, computer vision marker deskewing, symbolic CAS partial-credit grading, LMS roster synchronization, and IMS QTI 2.1 export.

---

## 🏗️ Architecture & Features

1. **Deterministic CAS Math Core**
   - Procedural backward parameterization via **SymPy**. Zero LLM hallucinations, guaranteed integer/rational invariants, full seed determinism.
   - Comprehensive curriculum catalog across 7 tiers: Grade 6 Math, Pre-Algebra, Algebra 1, Geometry, Algebra 2, Precalculus, and Calculus (43+ algorithmic generators).
2. **Typesetting & Anti-Cheating Document Engine**
   - Sub-100ms compilation via **Typst** (`typst-py`).
   - 4 ArUco 4x4 corner fiducials and metadata QR codes `{worksheet_id, form_id, seed, student_id}`.
   - Dynamic workspace clearance calculation to eliminate page overruns.
   - 4-form multi-scramble (Forms A, B, C, D) with unified 4-column master grading matrix.
3. **Computer Vision & CAS Grading**
   - OpenCV fiducial detection, perspective warp to canonical US-Letter (2550x3300 px at 300 DPI), and workspace box slicing.
   - SymPy step-difference CAS verifier ($\Delta = \text{simplify}(S_k - S_{k-1}) == 0$).
   - Automated error classification: arithmetic, sign, distribution, conceptual, with partial credit scoring.
4. **Classroom Management & Auto-Gradebook**
   - 1-click roster import supporting **Google Classroom**, **Canvas LMS**, **Clever**, and **OneRoster** CSVs.
   - Batch personalized PDF generation with unique student QR codes.
   - Direct grade sync into local class gradebooks.
5. **EdTech LMS Export**
   - Canvas-compliant **QTI 2.1** XML and ZIP package export with CCSS-M and TEKS curriculum tagging.
6. **Modern Studio UI**
   - Next.js 14 App Router, Tailwind CSS, KaTeX live mathematical preview, assignment tray, and camera vision grader dropzone.

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
