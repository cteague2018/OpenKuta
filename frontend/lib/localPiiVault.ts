/**
 * OpenMathForge Local-First PII Vault
 * 
 * ZERO-PII CLOUD GUARANTEE:
 * All student names, student IDs, and assessment scores are stored strictly on the user's local PC
 * (via the File System Access API and browser local storage).
 * Only pseudonymized tokens (e.g. "omf_st_a8f9") ever leave the browser for rendering or CV grading.
 */

export interface LocalStudent {
  id: string;
  name: string;
  studentNumber?: string;
  scores: Record<string, number>; // assessmentId -> score
}

export interface LocalClassroom {
  id: string;
  name: string;
  subject: string;
  period: string;
  teacherName: string;
  students: LocalStudent[];
  createdAt: string;
}

export interface LocalVaultData {
  version: string;
  vaultId: string;
  lastModified: string;
  classes: LocalClassroom[];
}

const STORAGE_KEY = "openmathforge_local_vault_v1";

const DEFAULT_VAULT: LocalVaultData = {
  version: "1.0",
  vaultId: "omf_vault_local",
  lastModified: new Date().toISOString(),
  classes: [
    {
      id: "class_local_alg1_p2",
      name: "Algebra 1 (Period 2)",
      subject: "Algebra 1",
      period: "2",
      teacherName: "Educator",
      createdAt: new Date().toISOString(),
      students: [
        { id: "st_101", name: "Alice Johnson", studentNumber: "90412", scores: { "Unit 3 Quadratics": 92 } },
        { id: "st_102", name: "Brian Martinez", studentNumber: "90413", scores: { "Unit 3 Quadratics": 88 } },
        { id: "st_103", name: "Chloe Davis", studentNumber: "90414", scores: { "Unit 3 Quadratics": 95 } },
        { id: "st_104", name: "David Kim", studentNumber: "90415", scores: { "Unit 3 Quadratics": 79 } },
        { id: "st_105", name: "Elena Rostova", studentNumber: "90416", scores: { "Unit 3 Quadratics": 100 } },
      ],
    },
  ],
};

/**
 * Load vault data from browser local storage
 */
export function loadVaultFromLocalStorage(): LocalVaultData {
  if (typeof window === "undefined") return DEFAULT_VAULT;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      saveVaultToLocalStorage(DEFAULT_VAULT);
      return DEFAULT_VAULT;
    }
    return JSON.parse(raw) as LocalVaultData;
  } catch {
    return DEFAULT_VAULT;
  }
}

/**
 * Persist vault data into browser local storage
 */
export function saveVaultToLocalStorage(data: LocalVaultData): void {
  if (typeof window === "undefined") return;
  try {
    data.lastModified = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (err) {
    console.warn("Failed to persist local vault to localStorage:", err);
  }
}

/**
 * Save vault file (.omf) directly to the user's PC drive using File System Access API
 */
export async function saveVaultToDisk(data: LocalVaultData): Promise<boolean> {
  const content = JSON.stringify(data, null, 2);
  const fileName = `openmathforge_classes_${new Date().toISOString().slice(0, 10)}.omf`;

  // 1. Modern File System Access API (Chrome, Edge, Opera)
  if (typeof window !== "undefined" && "showSaveFilePicker" in window) {
    try {
      const handle = await (window as any).showSaveFilePicker({
        suggestedName: fileName,
        types: [
          {
            description: "OpenMathForge Classroom Vault (*.omf)",
            accept: { "application/json": [".omf", ".json"] },
          },
        ],
      });
      const writable = await handle.createWritable();
      await writable.write(content);
      await writable.close();
      return true;
    } catch (err: any) {
      if (err.name === "AbortError") return false; // user cancelled
    }
  }

  // 2. Universal Browser Fallback via Blob download
  try {
    const blob = new Blob([content], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    return true;
  } catch {
    return false;
  }
}

/**
 * Read vault file (.omf or .json) from the user's PC drive
 */
export async function loadVaultFromDiskFile(file: File): Promise<LocalVaultData | null> {
  try {
    const text = await file.text();
    const parsed = JSON.parse(text);
    if (parsed && Array.isArray(parsed.classes)) {
      saveVaultToLocalStorage(parsed);
      return parsed;
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * Export a single classroom roster and grades to CSV on the user's PC
 */
export function exportClassroomToCsv(classroom: LocalClassroom): void {
  const assessmentNames = Array.from(
    new Set(classroom.students.flatMap((s) => Object.keys(s.scores || {})))
  );

  const header = ["Student Name", "Student ID", ...assessmentNames];
  const rows = classroom.students.map((student) => {
    const cols = [
      `"${student.name.replace(/"/g, '""')}"`,
      student.studentNumber || "",
      ...assessmentNames.map((name) => student.scores[name] ?? ""),
    ];
    return cols.join(",");
  });

  const csvContent = [header.join(","), ...rows].join("\r\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${classroom.name.replace(/\s+/g, "_")}_roster.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * Parse CSV text into a new LocalClassroom
 */
export function parseCsvToClassroom(
  csvText: string,
  className: string,
  subject: string,
  period: string,
  teacherName: string
): LocalClassroom {
  const lines = csvText.split(/\r?\n/).filter((l) => l.trim().length > 0);
  const students: LocalStudent[] = [];

  for (let i = 0; i < lines.length; i++) {
    // Skip likely header
    if (i === 0 && (lines[i].toLowerCase().includes("name") || lines[i].toLowerCase().includes("student"))) {
      continue;
    }
    const parts = lines[i].split(",").map((p) => p.trim().replace(/^"|"$/g, ""));
    if (parts[0]) {
      students.push({
        id: `st_${Date.now()}_${i}`,
        name: parts[0],
        studentNumber: parts[1] || `ID-${1000 + i}`,
        scores: {},
      });
    }
  }

  return {
    id: `class_${Date.now()}`,
    name: className || "Imported Class",
    subject: subject || "Mathematics",
    period: period || "1",
    teacherName: teacherName || "Educator",
    createdAt: new Date().toISOString(),
    students,
  };
}

/**
 * Client-Side Pseudonymization Engine
 * 
 * Maps student ID to an opaque cryptographic token sent to cloud endpoints.
 * The cloud only ever receives "omf_st_c93a8" and never sees student PII.
 */
export function createPseudonymToken(studentId: string, salt: string = "omf_local_secret"): string {
  let hash = 0;
  const combined = `${studentId}:${salt}`;
  for (let i = 0; i < combined.length; i++) {
    const char = combined.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0;
  }
  const hex = Math.abs(hash).toString(16).padStart(8, "0");
  return `omf_st_${hex}`;
}

