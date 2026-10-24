# Role: Computer Vision & Grading Pipeline Architect
Objective: Build the scan/photo alignment and line-by-line verification bridge.

Deliverables in `backend/app/grading/`:
1. `aligner.py`:
   - Load student scan (PDF or JPEG/PNG).
   - Detect 4 ArUco markers using `cv2.aruco`.
   - Apply perspective transform (`cv2.getPerspectiveTransform` and `cv2.warpPerspective`) to normalize skew, rotation, and camera angle to canonical US-Letter dimensions (2550 x 3300 px at 300 DPI).
   - Detect and decode the QR code to fetch the original worksheet metadata and problem seeds.
2. `extractor.py`:
   - Crop individual problem bounding boxes based on the template coordinates.
   - Apply adaptive binarization to boost faint pencil strokes and remove background shadows.
3. `verifier.py`:
   - Interface for feeding transcribed LaTeX steps into SymPy.
   - Calculate consecutive line difference $\Delta = \text{simplify}(\text{Step}_k - \text{Step}_{k-1})$.
   - Flag first failure point, classify error (sign, distribution, arithmetic, conceptual), and assign partial credit.

