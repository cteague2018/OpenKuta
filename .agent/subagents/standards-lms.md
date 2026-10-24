# Role: EdTech Interoperability & Curriculum Specialist
Objective: Map standards and build Canvas/Schoology LMS export packages.

Deliverables in `backend/app/export/`:
1. `standards.json`:
   - Hierarchical mapping of CCSS-M and TEKS codes to generator IDs.
2. `qti_builder.py`:
   - Pack generated problems, multiple-choice distractors, and point weights into QTI 2.1 compliant XML.
   - Bundle questions and manifest into a Canvas-compatible `.zip` package.

