# Role: Fullstack API & Web Interface Engineer
Objective: Wire the deterministic backend to a high-speed Next.js interface with live KaTeX rendering.

Deliverables in `backend/app/api/` & `frontend/`:
1. FastAPI Endpoints:
   - `POST /api/worksheet/pdf`: Compiles printable worksheet PDF with ArUco corners and QR code.
   - `POST /api/worksheet/multi-form`: Scrambles Form A–D worksheets with unified matrix key.
   - `POST /api/grade/upload`: Receives scan, performs CV deskew, crops bounding boxes, verifies steps.
   - `POST /api/export/qti`: Generates QTI 2.1 zip package for Canvas/Schoology import.
   - `GET /api/standards`: Lists CCSS and TEKS curriculum alignments.
2. Next.js 14 Frontend:
   - Topic tree with CCSS standard filter.
   - Live KaTeX worksheet preview with "Mild / Medium / Spicy" tiered sliders.
   - 1-Click "Scramble 4 Forms (A/B/C/D)" button.
   - "Grade Scans" tab with camera upload, perspective preview, and error breakdown heatmap.

