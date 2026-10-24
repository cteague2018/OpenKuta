# Role: Typesetting & Document Architecture Specialist
Objective: Build the Typst worksheet engine with anti-cheating markers and dynamic spacing.

Deliverables in `backend/app/templates/` & `backend/app/core/`:
1. `worksheet.typ.j2`:
   - ArUco marker placement at the 4 extreme margins.
   - QR code box in header (using `typst-qr` or pre-rendered SVG payload).
   - Form variant header tag ("Form A", "Form B", etc.).
   - 3-Tier Sectioning: "Mild" (procedural), "Medium" (algebraic), "Spicy" (challenge).
   - Dynamic workspace boxes calculating height to guarantee no page overruns.
2. `matrix_key.typ.j2`:
   - Single-page 4-column teacher matrix aligning Form A, B, C, D answers by problem number.
3. `compiler.py`:
   - Fast async execution compiling Typst buffers to PDF in <100ms.

