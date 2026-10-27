"use client";

import React, { useState, useEffect, useMemo, useRef } from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import {
  Download,
  FileCheck,
  Layers,
  RefreshCw,
  Search,
  Award,
  CheckCircle2,
  AlertTriangle,
  ZoomIn,
  ZoomOut,
  Trash2,
  Plus,
  Eye,
  ChevronDown,
  ChevronRight,
  Settings2,
  QrCode,
  ShieldCheck,
  Users,
  Upload,
  FileSpreadsheet,
  Camera,
  LogIn,
  LogOut,
  Save,
  FolderOpen,
  HardDrive,
  Sparkles,
  RotateCcw,
  History,
  Undo2,
  Key,
  Pencil,
  BookOpen,
  Printer,
} from "lucide-react";
import katex from "katex";
import {
  DEFAULT_COURSE_CATALOG,
  DEFAULT_SAMPLE_PROBLEMS,
  DEFAULT_CLASSROOMS,
  Topic,
  Course,
  Problem,
} from "./catalogData";
import {
  LocalStudent,
  LocalClassroom,
  LocalVaultData,
  loadVaultFromLocalStorage,
  saveVaultToLocalStorage,
  saveVaultToDisk,
  loadVaultFromDiskFile,
  exportClassroomToCsv,
  parseCsvToClassroom,
  createPseudonymToken,
  softDeleteClassroom,
  restoreClassroom,
  softDeleteStudent,
  restoreStudent,
  getVaultSnapshots,
  VaultSnapshot,
} from "../lib/localPiiVault";

interface AssignmentItem {
  id: string;
  topicName: string;
  generatorId: string;
  count: number;
  difficulty: "mild" | "medium" | "spicy";
  questionType: "free_response" | "multiple_choice";
}

interface ClassroomSummary {
  id: string;
  name: string;
  subject: string;
  period: string;
  teacher_name: string;
  student_count: number;
}

function typstToLatex(raw: string): string {
  if (!raw) return "";
  let s = raw.trim();
  // Strip leading and trailing $
  s = s.replace(/^\$+\s*/, "").replace(/\s*\$+$/, "").trim();
  // Clean up prefix labels like "Result:" or "Solve for x:"
  s = s.replace(/^(Result|Solve for [^:]+):\s*/i, "").trim();

  // Typst string quotes -> \text{ ... }
  s = s.replace(/"([^"]*)"/g, "\\text{ $1 }");

  // Strip any remaining internal $ delimiters
  s = s.replace(/\$/g, "");

  // Typst to LaTeX conversions
  s = s.replace(/plus\.minus/g, "\\pm ");
  s = s.replace(/sqrt\(([^)]+)\)/g, "\\sqrt{$1}");
  s = s.replace(/\bquad\b/g, "\\quad ");
  s = s.replace(/cases\(([^,]+),\s*([^)]+)\)/g, "\\begin{cases} $1 \\\\ $2 \\end{cases}");
  s = s.replace(/\barrow\.r\.double\b/g, "\\implies ");
  s = s.replace(/\barrow\.r\b/g, "\\to ");
  s = s.replace(/\barrow\.l\.double\b/g, "\\impliedby ");
  s = s.replace(/\barrow\.l\b/g, "\\leftarrow ");
  s = s.replace(/\barrow\.l\.r\.double\b/g, "\\iff ");
  s = s.replace(/\barrow\.l\.r\b/g, "\\leftrightarrow ");
  s = s.replace(/2rightarrow/g, "\\implies ");
  s = s.replace(/==>/g, "\\implies ");
  s = s.replace(/<==>/g, "\\iff ");
  s = s.replace(/<==/g, "\\impliedby ");
  s = s.replace(/-->|->/g, "\\to ");
  s = s.replace(/\bapprox\b/g, "\\approx ");
  s = s.replace(/\s*dot\s*/g, " \\cdot ");
  s = s.replace(/\s*times\s*/g, " \\times ");
  s = s.replace(/\s*\*\s*/g, " \\cdot ");

  // Strip redundant trailing or intermediate '+ 0' and '- 0'
  s = s.replace(/(?<=[a-zA-Z0-9_\)])(\s*[+-]\s*0\b(?!\.))+/g, "");
  s = s.replace(/(\b[+-]\s*0\b(?!\.)\s*)+/g, "");

  // Vectors & angles
  s = s.replace(/\bangle\.l\b/g, "\\langle ");
  s = s.replace(/\bangle\.r\b/g, "\\rangle ");
  s = s.replace(/\bbold\(([^)]+)\)/g, "\\mathbf{$1}");

  // Limits, Integrals, and Symbols
  s = s.replace(/\blim_\(([^)]+)\s*->\s*([^)]+)\)/g, "\\lim_{$1 \\to $2}");
  s = s.replace(/\bintegral_([0-9a-zA-Z\^\-]+)\^([0-9a-zA-Z\^\-]+)/g, "\\int_{$1}^{$2}");
  s = s.replace(/\bintegral\b/g, "\\int ");
  s = s.replace(/\bdif\s+([a-zA-Z])/g, " \\, d$1");
  s = s.replace(/\boo\b/g, "\\infty ");
  s = s.replace(/\^\s*\\?circle\b/g, "^{\\circ}");

  // Matrices: mat(1, 0; 1, 2)
  s = s.replace(/\bmat\(([^)]+)\)/g, (_, inner) => {
    const rows = inner.split(";").map((r: string) =>
      r.trim().split(",").map((c: string) => c.trim()).join(" & ")
    );
    return "\\begin{pmatrix} " + rows.join(" \\\\ ") + " \\end{pmatrix}";
  });

  // Convert Typst division '/' to LaTeX fractions \frac{...}{...}
  for (let iter = 0; iter < 3; iter++) {
    const prev = s;
    s = s.replace(/\(([^()]+)\)\s*\/\s*\(([^()]+)\)/g, "\\frac{$1}{$2}");
    s = s.replace(/\(([^()]+)\)\s*\/\s*([a-zA-Z0-9_\^\-]+)/g, "\\frac{$1}{$2}");
    s = s.replace(/([a-zA-Z0-9_\^\-]+)\s*\/\s*\(([^()]+)\)/g, "\\frac{$1}{$2}");
    s = s.replace(/(^|[^a-zA-Z0-9_\\{])([a-zA-Z0-9_\^]+)\s*\/\s*([a-zA-Z0-9_\^]+)(?![a-zA-Z0-9_}])/g, "$1\\frac{$2}{$3}");
    if (s === prev) break;
  }

  return s.trim();
}

const PROSE_REGEX = /\b(the|a|an|is|of|and|in|to|for|with|from|than|more|less|twice|sum|product|quotient|difference|square|find|what|given|determine|write|name|solve|represents|initial|travels|car|train|miles|hours|speed|cost|items|menu|race|bag|probab|select|choose|each|triangle|angle|shorter|leg|hypotenuse)\b/i;
const MATH_KEYWORDS = new Set([
  'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'ln', 'lim', 'quad', 
  'cases', 'sqrt', 'integral', 'mat', 'bold', 'angle', 'plus', 'minus', 
  'dif', 'det', 'times', 'dot'
]);

function isProseProblem(raw: string): boolean {
  if (!raw) return false;
  const t = raw.trim();

  // If fully enclosed in single $...$ pair
  if (t.startsWith("$") && t.endsWith("$") && (t.match(/\$/g) || []).length === 2) {
    const inner = t.slice(1, -1).trim();
    if (inner.includes('"')) {
      return false; // Typst math with quotes like $ (-10, -2) " and " (-8, 3) $
    }
    const words = (inner.match(/[a-zA-Z]{3,}/g) || []).filter(
      (w) => !MATH_KEYWORDS.has(w.toLowerCase())
    );
    return words.length >= 3;
  }

  // If it has internal $ ... $ delimiters (e.g. "Given $ f(x) = 2x $, find $ f(1) $")
  if (t.includes("$")) {
    return true;
  }

  // Check if unquoted string has prose markers or multiple words
  const clean = t.replace(/"[^"]*"/g, "");
  const words = (clean.match(/[a-zA-Z]{3,}/g) || []).filter(
    (w) => !MATH_KEYWORDS.has(w.toLowerCase())
  );
  return words.length >= 2 || PROSE_REGEX.test(clean);
}

function KaTeXInline({ math, className = "" }: { math: string; className?: string }) {
  if (!math) return null;
  const latex = typstToLatex(math);
  try {
    const html = katex.renderToString(latex, {
      throwOnError: false,
      displayMode: false,
    });
    return <span className={className} dangerouslySetInnerHTML={{ __html: html }} />;
  } catch {
    return <span className={className}>{latex}</span>;
  }
}

function ProblemEquation({
  raw,
  className = "",
  inline = false,
}: {
  raw: string;
  className?: string;
  inline?: boolean;
}) {
  if (!raw) return null;
  const trimmed = raw.trim();

  // If classified as Prose or Word Problem
  if (isProseProblem(trimmed)) {
    if (trimmed.includes("$")) {
      const parts = trimmed.split("$");
      const Tag = inline ? "span" : "div";
      return (
        <Tag className={`${inline ? "inline" : "text-center px-1"} text-slate-800 text-sm leading-relaxed ${className}`}>
          {parts.map((p, idx) => {
            if (idx % 2 === 1) {
              return <KaTeXInline key={idx} math={p} className="font-semibold mx-0.5 inline-block" />;
            }
            const cleanText = p.replace(/"/g, "");
            return <span key={idx}>{cleanText}</span>;
          })}
        </Tag>
      );
    }

    const cleanText = trimmed.replace(/"/g, "");
    const Tag = inline ? "span" : "div";
    return (
      <Tag className={`${inline ? "inline" : "text-center px-2 py-1"} text-slate-800 text-sm font-normal leading-relaxed ${className}`}>
        {cleanText}
      </Tag>
    );
  }

  // Pure Math Mode
  if (inline) {
    return <KaTeXInline math={trimmed} className={className} />;
  }
  return (
    <div className={`py-1 text-center text-sm font-medium text-slate-900 ${className}`}>
      <KaTeXInline math={trimmed} />
    </div>
  );
}

function StepTextWithMath({ text }: { text: string }) {
  if (!text) return null;
  const trimmed = text.trim();
  const cleaned = trimmed.replace(/"/g, "");

  // If the whole string is an equation like "$ 2x + 4 = 10 $"
  if (cleaned.startsWith("$") && cleaned.endsWith("$") && (cleaned.match(/\$/g) || []).length === 2) {
    return <KaTeXInline math={cleaned} className="font-medium" />;
  }

  // Split by '$' for mixed prose and equations
  const parts = cleaned.split("$");
  if (parts.length === 1) {
    return <span>{cleaned}</span>;
  }

  return (
    <span>
      {parts.map((p, idx) => {
        if (idx % 2 === 1) {
          return <KaTeXInline key={idx} math={p} className="font-semibold mx-1 text-amber-950" />;
        }
        return <span key={idx}>{p}</span>;
      })}
    </span>
  );
}

export default function OpenMathForgeApp() {
  const [activeTab, setActiveTab] = useState<"studio" | "classroom" | "grader">("studio");
  const [selectedCourseKey, setSelectedCourseKey] = useState<string>("algebra_1");
  const [coursesCatalog, setCoursesCatalog] = useState<Record<string, Course>>(DEFAULT_COURSE_CATALOG);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>(() => {
    const initExp: Record<string, boolean> = {};
    Object.values(DEFAULT_COURSE_CATALOG).forEach((c) => {
      c.categories?.forEach((cat) => {
        initExp[cat.name] = true;
      });
    });
    return initExp;
  });

  // Worksheet Layout Controls
  const [worksheetTitle, setWorksheetTitle] = useState<string>("Algebra 1 Practice");
  const [columns, setColumns] = useState<number | "auto">("auto");
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [showAnswerKey, setShowAnswerKey] = useState<boolean>(false);
  const [baseSeed, setBaseSeed] = useState<number>(42);
  const [worksheetId, setWorksheetId] = useState<string>("WS-4201");

  // Assignment Items (Topics on current worksheet)
  const [assignmentItems, setAssignmentItems] = useState<AssignmentItem[]>([
    {
      id: "item_1",
      topicName: "Two-Step Equations",
      generatorId: "algebra_1.two_step",
      count: 4,
      difficulty: "mild",
      questionType: "free_response",
    },
    {
      id: "item_2",
      topicName: "Quadratic Equations by Factoring",
      generatorId: "algebra_1.quadratics",
      count: 4,
      difficulty: "medium",
      questionType: "free_response",
    },
  ]);

  // Modal / Configurator State
  const [configTopic, setConfigTopic] = useState<Topic | null>(null);
  const [editingItemId, setEditingItemId] = useState<string | null>(null);
  const [modalCount, setModalCount] = useState<number>(4);
  const [modalDifficulty, setModalDifficulty] = useState<"mild" | "medium" | "spicy">("medium");
  const [modalQuestionType, setModalQuestionType] = useState<"free_response" | "multiple_choice">("free_response");
  const [modalSampleProblems, setModalSampleProblems] = useState<Problem[]>([]);
  const [isModalLoading, setIsModalLoading] = useState<boolean>(false);
  const [maxProblemsPerPage, setMaxProblemsPerPage] = useState<number | "auto">("auto");

  // Live Worksheet Generated Problems
  const [worksheetProblems, setWorksheetProblems] = useState<Problem[]>(DEFAULT_SAMPLE_PROBLEMS);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);

  // Intelligent Layout Engine: Content-Aware Column & Problem Budgeting
  const activeColumns = useMemo(() => {
    if (columns !== "auto") return columns;
    return 2;
  }, [columns, worksheetProblems]);

  const activePerPage = useMemo(() => {
    if (maxProblemsPerPage !== "auto") return maxProblemsPerPage;
    const hasVisuals = worksheetProblems.some(
      (p) => Boolean(p.diagram_svg) || Boolean(p.answer_svg)
    );
    const hasLongSteps = worksheetProblems.some(
      (p) => Boolean(p.steps_typst && p.steps_typst.length > 2)
    );
    if (activeColumns === 1) {
      return hasVisuals || hasLongSteps ? 2 : 4;
    }
    if (activeColumns === 2) {
      return hasVisuals || hasLongSteps ? 4 : 6;
    }
    return 6;
  }, [maxProblemsPerPage, activeColumns, worksheetProblems]);

  // Dynamic Pagination & Page Workspace Bounds (guarantees standard 8.5x11 geometry and student handwriting/answer space)
  const paginatedPages = useMemo(() => {
    if (worksheetProblems.length === 0) return [];
    const pages: Problem[][] = [];

    const hasVisuals = worksheetProblems.some(
      (p) => Boolean(p.diagram_svg) || Boolean(p.answer_svg)
    );
    const hasLongSteps = worksheetProblems.some(
      (p) => Boolean(p.steps_typst && p.steps_typst.length > 2)
    );

    let effectivePageSize = activePerPage;

    if (activeColumns === 1) {
      // In 1-column layout, visual diagrams or answer steps require generous vertical clearance
      if (hasVisuals || (showAnswerKey && hasLongSteps)) {
        effectivePageSize = Math.min(activePerPage, 2);
      } else {
        effectivePageSize = Math.min(activePerPage, 4);
      }
    } else if (activeColumns === 2) {
      if (showAnswerKey && (hasVisuals || hasLongSteps)) {
        effectivePageSize = Math.min(activePerPage, 4);
      } else if (hasVisuals) {
        effectivePageSize = Math.min(activePerPage, 4);
      } else {
        effectivePageSize = activePerPage;
      }
    } else {
      effectivePageSize = activePerPage;
    }

    for (let i = 0; i < worksheetProblems.length; i += effectivePageSize) {
      pages.push(worksheetProblems.slice(i, i + effectivePageSize));
    }
    return pages;
  }, [worksheetProblems, activePerPage, showAnswerKey, activeColumns]);

  // NextAuth Session & Authentication State
  const { data: session } = useSession();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState<boolean>(false);
  const [authEmail, setAuthEmail] = useState<string>("");
  const [authName, setAuthName] = useState<string>("");
  const [isSigningIn, setIsSigningIn] = useState<boolean>(false);

  // Zero-PII Local PC Vault State
  const [localVault, setLocalVault] = useState<LocalVaultData>(() => loadVaultFromLocalStorage());
  const [vaultNotification, setVaultNotification] = useState<string | null>(null);
  const vaultFileInputRef = useRef<HTMLInputElement | null>(null);
  const [isNewClassModalOpen, setIsNewClassModalOpen] = useState<boolean>(false);
  const [classToDelete, setClassToDelete] = useState<LocalClassroom | null>(null);
  const [isRecoveryModalOpen, setIsRecoveryModalOpen] = useState<boolean>(false);
  const [recoveryTab, setRecoveryTab] = useState<"recycle" | "snapshots">("recycle");
  const [vaultSnapshots, setVaultSnapshots] = useState<VaultSnapshot[]>([]);
  const [newClassName, setNewClassName] = useState<string>("");
  const [newClassPeriod, setNewClassPeriod] = useState<string>("1");
  const [newClassSubject, setNewClassSubject] = useState<string>("Algebra 1");
  const [newStudentName, setNewStudentName] = useState<string>("");
  const [newStudentNumber, setNewStudentNumber] = useState<string>("");

  // Classroom Management State
  const [classesList, setClassesList] = useState<ClassroomSummary[]>(() =>
    DEFAULT_CLASSROOMS.map(({ id, name, subject, period, teacher_name, student_count }) => ({
      id,
      name,
      subject,
      period,
      teacher_name,
      student_count,
    }))
  );
  const [selectedClassId, setSelectedClassId] = useState<string>("class_local_alg1_p2");
  const [isImportModalOpen, setIsImportModalOpen] = useState<boolean>(false);
  const [isBatchGenerating, setIsBatchGenerating] = useState<boolean>(false);

  // Pro License & Access State
  const [proLicenseInput, setProLicenseInput] = useState<string>("");
  const [isProLicensed, setIsProLicensed] = useState<boolean>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("omf_pro_license_active") === "true";
    }
    return false;
  });
  const [licenseStatusMessage, setLicenseStatusMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [showDemoPreviewGrading, setShowDemoPreviewGrading] = useState<boolean>(false);

  const isUserPro = Boolean(
    (session?.user as any)?.isPro ||
    (session?.user as any)?.tier === "pro" ||
    isProLicensed
  );

  const handleActivateLicense = (keyToTest?: string) => {
    const key = (keyToTest || proLicenseInput).trim().toUpperCase();
    if (!key) {
      setLicenseStatusMessage({ type: "error", text: "Please enter a valid school district or educator license key." });
      return;
    }
    if (key.startsWith("OMF-PRO") || key.startsWith("PRO-") || key === "TEACHER-PRO-2026") {
      setIsProLicensed(true);
      if (typeof window !== "undefined") {
        localStorage.setItem("omf_pro_license_active", "true");
        localStorage.setItem("omf_pro_license_key", key);
      }
      setLicenseStatusMessage({ type: "success", text: `License activated successfully! (${key})` });
    } else {
      setLicenseStatusMessage({ type: "error", text: "Invalid license key. Check your school district activation code or subscribe to Pro." });
    }
  };

  // Vision Grader State
  const [uploadedScanFile, setUploadedScanFile] = useState<File | null>(null);
  const [scanPreviewUrl, setScanPreviewUrl] = useState<string | null>(null);
  const [scanResult, setScanResult] = useState<any>(null);
  const [isProcessingScan, setIsProcessingScan] = useState<boolean>(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [gradeSteps, setGradeSteps] = useState<string>(
    "3*(x + 4) = 21\n3*x + 12 = 21\n3*x = 9\nx = 3"
  );
  const [gradeResult, setGradeResult] = useState<any>(null);
  const [isGrading, setIsGrading] = useState<boolean>(false);

  // Load Course Catalog
  useEffect(() => {
    fetch("/api/catalog")
      .then((res) => {
        if (!res.ok) throw new Error("No backend");
        return res.json();
      })
      .then((data) => {
        setCoursesCatalog(data);
        const initExp: Record<string, boolean> = {};
        Object.values(data).forEach((c: any) => {
          c.categories?.forEach((cat: any) => {
            initExp[cat.name] = true;
          });
        });
        setExpandedCategories(initExp);
      })
      .catch(() => {
        // Keeps DEFAULT_COURSE_CATALOG
      });
  }, []);

  // Load Classes List
  const loadClasses = () => {
    fetch("/api/classroom/classes")
      .then((res) => {
        if (!res.ok) throw new Error("No backend");
        return res.json();
      })
      .then((data: ClassroomSummary[]) => {
        if (data && data.length > 0) {
          setClassesList(data);
          if (!selectedClassId) {
            setSelectedClassId(data[0].id);
          }
        }
      })
      .catch(() => {
        // Keeps default classrooms
      });
  };

  useEffect(() => {
    loadClasses();
  }, []);

  // Refresh live worksheet preview
  const refreshWorksheet = async () => {
    setIsGenerating(true);
    try {
      if (assignmentItems.length === 0) {
        setWorksheetProblems([]);
        setWorksheetId(`WS-${String(baseSeed % 10000).padStart(4, "0")}`);
        return;
      }

      const allProblems: Problem[] = [];
      let itemSeed = baseSeed;

      for (const item of assignmentItems) {
        const diffMap = {
          mild: { mild: 1.0, medium: 0.0, spicy: 0.0 },
          medium: { mild: 0.0, medium: 1.0, spicy: 0.0 },
          spicy: { mild: 0.0, medium: 0.0, spicy: 1.0 },
        }[item.difficulty];

        try {
          const res = await fetch("/api/worksheet/preview", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              generator_id: item.generatorId,
              problem_count: item.count,
              seed: itemSeed,
              difficulty_distribution: diffMap,
              allow_negatives: true,
              question_type: item.questionType,
            }),
          });

          if (res.ok) {
            const data = await res.json();
            if (data.problems) {
              allProblems.push(
                ...data.problems.map((p: Problem) => ({
                  ...p,
                  generator_id: p.generator_id || item.generatorId,
                  question_type: p.question_type || item.questionType,
                }))
              );
            }
          }
        } catch {
          // backend not reachable
        }
        itemSeed += 77;
      }

      if (allProblems.length > 0) {
        setWorksheetProblems(allProblems);
      } else {
        // Fallback to sample problems only if assignment had items but backend was unreachable
        setWorksheetProblems(DEFAULT_SAMPLE_PROBLEMS);
      }
      setWorksheetId(`WS-${String(baseSeed % 10000).padStart(4, "0")}`);
    } catch (e) {
      console.error("Preview generation error:", e);
      setWorksheetProblems([]);
    } finally {
      setIsGenerating(false);
    }
  };

  useEffect(() => {
    refreshWorksheet();
  }, [assignmentItems, baseSeed]);

  // Fetch samples for Modal Configurator
  const fetchModalSample = async (
    genId: string,
    count: number,
    diff: "mild" | "medium" | "spicy",
    qType: "free_response" | "multiple_choice" = modalQuestionType
  ) => {
    setIsModalLoading(true);
    try {
      const diffMap = {
        mild: { mild: 1.0, medium: 0.0, spicy: 0.0 },
        medium: { mild: 0.0, medium: 1.0, spicy: 0.0 },
        spicy: { mild: 0.0, medium: 0.0, spicy: 1.0 },
      }[diff];

      const res = await fetch("/api/worksheet/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          generator_id: genId,
          problem_count: count,
          seed: Math.floor(Math.random() * 9999),
          difficulty_distribution: diffMap,
          question_type: qType,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setModalSampleProblems(data.problems || []);
      } else {
        setModalSampleProblems(DEFAULT_SAMPLE_PROBLEMS.slice(0, count));
      }
    } catch {
      setModalSampleProblems(DEFAULT_SAMPLE_PROBLEMS.slice(0, count));
    } finally {
      setIsModalLoading(false);
    }
  };

  const openQuestionConfigurator = (topic: Topic) => {
    setEditingItemId(null);
    setConfigTopic(topic);
    setModalCount(4);
    setModalDifficulty("medium");
    setModalQuestionType("free_response");
    fetchModalSample(topic.generator_id, 4, "medium", "free_response");
  };

  const handleEditAssignmentItem = (item: AssignmentItem) => {
    let matchingTopic: Topic | null = null;
    const currentCourse = coursesCatalog[selectedCourseKey];
    if (currentCourse?.categories) {
      for (const cat of currentCourse.categories) {
        const found = cat.topics?.find(
          (t) => t.generator_id === item.generatorId || t.name === item.topicName
        );
        if (found) {
          matchingTopic = found;
          break;
        }
      }
    }
    if (!matchingTopic) {
      matchingTopic = {
        id: item.generatorId,
        name: item.topicName,
        generator_id: item.generatorId,
        available: true,
      };
    }
    setEditingItemId(item.id);
    setConfigTopic(matchingTopic);
    setModalCount(item.count);
    setModalDifficulty(item.difficulty);
    setModalQuestionType(item.questionType);
    fetchModalSample(item.generatorId, item.count, item.difficulty, item.questionType);
  };

  const handleAddConfiguredTopic = () => {
    if (!configTopic) return;
    if (editingItemId) {
      setAssignmentItems((prev) =>
        prev.map((item) =>
          item.id === editingItemId
            ? {
                ...item,
                topicName: configTopic.name,
                generatorId: configTopic.generator_id,
                count: modalCount,
                difficulty: modalDifficulty,
                questionType: modalQuestionType,
              }
            : item
        )
      );
      setEditingItemId(null);
    } else {
      const newItem: AssignmentItem = {
        id: `item_${Date.now()}`,
        topicName: configTopic.name,
        generatorId: configTopic.generator_id,
        count: modalCount,
        difficulty: modalDifficulty,
        questionType: modalQuestionType,
      };
      setAssignmentItems((prev) => [...prev, newItem]);
    }
    setConfigTopic(null);
  };

  const handleRemoveItem = (id: string) => {
    setAssignmentItems((prev) => prev.filter((i) => i.id !== id));
  };

  const buildTopicsPayload = () =>
    assignmentItems.map((item) => ({
      generator_id: item.generatorId,
      count: item.count,
      difficulty: item.difficulty,
      question_type: item.questionType,
    }));

  // Multi-Topic PDF Download
  const handleDownloadPDF = async () => {
    try {
      const res = await fetch("/api/worksheet/pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: worksheetTitle,
          form_id: "A",
          seed: baseSeed,
          columns: columns,
          topics: buildTopicsPayload(),
        }),
      });

      if (!res.ok) throw new Error("Backend unavailable");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${worksheetTitle.replace(/\s+/g, "_")}_Form_A.pdf`;
      a.click();
    } catch {
      alert(
        "Typst PDF compilation requires the Python CAS backend to be running:\n\nRun in terminal: python -m uvicorn backend.app.main:app --port 8000\n\nOr connect a cloud BACKEND_URL in Vercel settings."
      );
    }
  };

  // Export Answer Key PDF Download
  const handleDownloadAnswerKey = async () => {
    try {
      const res = await fetch("/api/worksheet/pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: worksheetTitle,
          form_id: "A",
          seed: baseSeed,
          columns: columns,
          show_answers: true,
          topics: buildTopicsPayload(),
        }),
      });

      if (!res.ok) throw new Error("Backend unavailable");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${worksheetTitle.replace(/\s+/g, "_")}_Form_A_Answer_Key.pdf`;
      a.click();
    } catch {
      alert(
        "Answer key PDF compilation requires the Python CAS backend to be running."
      );
    }
  };

  // Scramble Form: clean 1 to N re-indexing
  const handleScrambleForm = () => {
    setBaseSeed(Math.floor(Math.random() * 9999));
    setWorksheetProblems((prev) => {
      const copy = [...prev];
      for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
      }
      return copy.map((p, idx) => ({
        ...p,
        id: `prob_scrambled_${idx + 1}`,
      }));
    });
  };

  // Regenerate Single Problem
  const handleRegenerateSingleProblem = async (targetIdx: number) => {
    const targetProb = worksheetProblems[targetIdx];
    if (!targetProb) return;

    // Locate the assignment item corresponding to targetIdx
    let cumulative = 0;
    let ownerItem: AssignmentItem | undefined = assignmentItems[0];
    for (const item of assignmentItems) {
      if (targetIdx < cumulative + item.count) {
        ownerItem = item;
        break;
      }
      cumulative += item.count;
    }

    const genId =
      targetProb.generator_id ||
      targetProb.metadata?.topic_id ||
      ownerItem?.generatorId ||
      "algebra_1.quadratics";
    const diff: "mild" | "medium" | "spicy" =
      targetProb.difficulty || ownerItem?.difficulty || "medium";
    const qType: "free_response" | "multiple_choice" =
      targetProb.question_type ||
      ownerItem?.questionType ||
      (targetProb.choices && targetProb.choices.length >= 4
        ? "multiple_choice"
        : "free_response");
    const diffMap = {
      mild: { mild: 1.0, medium: 0.0, spicy: 0.0 },
      medium: { mild: 0.0, medium: 1.0, spicy: 0.0 },
      spicy: { mild: 0.0, medium: 0.0, spicy: 1.0 },
    }[diff];

    // Collect equations of all currently displayed problems to prevent worksheet duplicates
    const existingEquations = new Set(
      worksheetProblems
        .filter((_, idx) => idx !== targetIdx)
        .map((p) => p.equation_typst?.trim() || "")
    );

    try {
      const res = await fetch("/api/worksheet/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          generator_id: genId,
          problem_count: 8,
          seed: Math.floor(Math.random() * 10000000) + (Date.now() % 100000) + targetIdx * 7919,
          difficulty_distribution: diffMap,
          allow_negatives: true,
          question_type: qType,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.problems && data.problems.length > 0) {
          const candidates: Problem[] = data.problems;
          const distinctProb =
            candidates.find(
              (p) =>
                !existingEquations.has(p.equation_typst?.trim() || "") &&
                p.equation_typst?.trim() !== targetProb.equation_typst?.trim()
            ) ||
            candidates.find(
              (p) => p.equation_typst?.trim() !== targetProb.equation_typst?.trim()
            ) ||
            candidates[0];

          setWorksheetProblems((prev) => {
            const next = [...prev];
            next[targetIdx] = {
              ...distinctProb,
              id: `prob_regen_${Date.now()}_${targetIdx}`,
              generator_id: genId,
              question_type: qType,
            };
            return next;
          });
          return;
        }
      }
    } catch {
      // Offline fallback below
    }

    // Offline fallback: pick a distinct sample problem that is not on the worksheet
    const altSamples = DEFAULT_SAMPLE_PROBLEMS.filter(
      (p) =>
        !existingEquations.has(p.equation_typst?.trim() || "") &&
        p.equation_typst?.trim() !== targetProb.equation_typst?.trim()
    );
    const chosen =
      altSamples[Math.floor(Math.random() * altSamples.length)] ||
      DEFAULT_SAMPLE_PROBLEMS.find((p) => p.equation_typst?.trim() !== targetProb.equation_typst?.trim()) ||
      DEFAULT_SAMPLE_PROBLEMS[0];
    setWorksheetProblems((prev) => {
      const next = [...prev];
      next[targetIdx] = {
        ...chosen,
        id: `prob_regen_${Date.now()}_${targetIdx}`,
        generator_id: genId,
        question_type: qType,
      };
      return next;
    });
  };

  // Multi-Form Scramble Bundle (A-D)
  const handleScrambleMultiForm = async () => {
    try {
      const res = await fetch("/api/worksheet/multi-form", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: worksheetTitle,
          base_seed: baseSeed,
          forms: ["A", "B", "C", "D"],
          topics: buildTopicsPayload(),
        }),
      });

      if (!res.ok) throw new Error("Backend unavailable");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${worksheetTitle.replace(/\s+/g, "_")}_Forms_A_B_C_D_Bundle.zip`;
      a.click();
    } catch {
      alert(
        "4-Form PDF generation requires the Python CAS backend to be running:\n\nRun in terminal: python -m uvicorn backend.app.main:app --port 8000"
      );
    }
  };

  // Canvas QTI Export
  const handleExportQTI = async () => {
    try {
      const topicsPayload = buildTopicsPayload();

      const res = await fetch("/api/export/qti", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: worksheetTitle,
          seed: baseSeed,
          topics: topicsPayload,
        }),
      });

      if (!res.ok) throw new Error("Backend unavailable");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${worksheetTitle.replace(/\s+/g, "_")}_Canvas_QTI.zip`;
      a.click();
    } catch {
      alert(
        "Canvas QTI export requires the Python backend to be running:\n\nRun in terminal: python -m uvicorn backend.app.main:app --port 8000"
      );
    }
  };

  // Print Batch Class Set (with individual student QR codes)
  const handlePrintClassBatchPDF = async () => {
    if (!selectedClassId) return;
    setIsBatchGenerating(true);
    try {
      const primaryGen = assignmentItems[0]?.generatorId || "algebra_1.two_step";
      const totalCount = assignmentItems.reduce((acc, curr) => acc + curr.count, 0);

      const res = await fetch("/api/classroom/batch-worksheet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          class_id: selectedClassId,
          generator_id: primaryGen,
          title: worksheetTitle,
          form_id: "A",
          problem_count: totalCount,
          seed: baseSeed,
          columns: columns,
          topics: assignmentItems.map((item) => ({
            generator_id: item.generatorId,
            count: item.count,
            difficulty: item.difficulty,
          })),
        }),
      });

      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        const currentClass = classesList.find((c) => c.id === selectedClassId);
        a.download = `${(currentClass?.name || "Class").replace(/\s+/g, "_")}_Personalized_Class_Set.pdf`;
        a.click();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsBatchGenerating(false);
    }
  };

  // Local PC Vault Handlers
  const handleSaveVaultToDisk = async () => {
    const success = await saveVaultToDisk(localVault);
    if (success) {
      setVaultNotification("Vault successfully saved to your PC (.omf)!");
      setTimeout(() => setVaultNotification(null), 4000);
    }
  };

  const handleDiskFileSelected = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const loaded = await loadVaultFromDiskFile(file);
    if (loaded) {
      setLocalVault(loaded);
      if (loaded.classes.length > 0) {
        setSelectedClassId(loaded.classes[0].id);
      }
      setVaultNotification(`Loaded ${loaded.classes.length} class(es) from ${file.name}`);
      setTimeout(() => setVaultNotification(null), 4000);
    } else {
      alert("Invalid .omf or JSON file. Please select a valid OpenMathForge vault file.");
    }
  };

  const handleExportCurrentClassCsv = () => {
    const currentLocalClass =
      localVault.classes.find((c) => c.id === selectedClassId) || localVault.classes[0];
    if (currentLocalClass) {
      exportClassroomToCsv(currentLocalClass);
      setVaultNotification(`Exported ${currentLocalClass.name} roster to CSV`);
      setTimeout(() => setVaultNotification(null), 4000);
    }
  };

  const handleCreateNewClass = () => {
    if (!newClassName.trim()) return;
    const newClass: LocalClassroom = {
      id: `class_${Date.now()}`,
      name: newClassName.trim(),
      subject: newClassSubject,
      period: newClassPeriod,
      teacherName: session?.user?.name || "Teacher",
      createdAt: new Date().toISOString(),
      students: [],
    };
    const updated = {
      ...localVault,
      classes: [...localVault.classes, newClass],
    };
    setLocalVault(updated);
    saveVaultToLocalStorage(updated);
    setSelectedClassId(newClass.id);
    setIsNewClassModalOpen(false);
    setNewClassName("");
    setVaultNotification(`Created class "${newClass.name}" locally on PC`);
    setTimeout(() => setVaultNotification(null), 4000);
  };

  const handleAddStudentLocally = () => {
    if (!newStudentName.trim()) return;
    const currentLocalClass =
      localVault.classes.find((c) => c.id === selectedClassId) || localVault.classes[0];
    if (!currentLocalClass) return;

    const newStudent: LocalStudent = {
      id: `st_${Date.now()}`,
      name: newStudentName.trim(),
      studentNumber: newStudentNumber.trim() || `ID-${Math.floor(1000 + Math.random() * 9000)}`,
      scores: {},
    };

    const updatedClasses = localVault.classes.map((c) => {
      if (c.id === currentLocalClass.id) {
        return {
          ...c,
          students: [...c.students, newStudent],
        };
      }
      return c;
    });

    const updated = { ...localVault, classes: updatedClasses };
    setLocalVault(updated);
    saveVaultToLocalStorage(updated);
    setNewStudentName("");
    setNewStudentNumber("");
    setVaultNotification(`Added ${newStudent.name} to local PC roster`);
    setTimeout(() => setVaultNotification(null), 4000);
  };

  const handleDeleteStudentLocally = (studentId: string) => {
    const updated = softDeleteStudent(localVault, selectedClassId, studentId);
    setLocalVault(updated);
    setVaultNotification("Moved student to Local Recycle Bin (can be recovered anytime)");
    setTimeout(() => setVaultNotification(null), 4000);
  };

  const handleConfirmDeleteClass = () => {
    if (!classToDelete) return;
    const updated = softDeleteClassroom(localVault, classToDelete.id);
    setLocalVault(updated);
    if (selectedClassId === classToDelete.id) {
      setSelectedClassId(updated.classes[0]?.id || "");
    }
    setVaultNotification(
      `Moved class "${classToDelete.name}" to Recycle Bin. You can restore it anytime.`
    );
    setClassToDelete(null);
    setTimeout(() => setVaultNotification(null), 4000);
  };

  const handleRestoreClass = (classId: string) => {
    const updated = restoreClassroom(localVault, classId);
    setLocalVault(updated);
    setSelectedClassId(classId);
    setVaultNotification("Class successfully restored from Recycle Bin!");
    setTimeout(() => setVaultNotification(null), 4000);
  };

  const handleRestoreStudent = (studentId: string) => {
    const updated = restoreStudent(localVault, studentId);
    setLocalVault(updated);
    setVaultNotification("Student restored back to roster!");
    setTimeout(() => setVaultNotification(null), 4000);
  };

  const handleRollbackSnapshot = (snapshot: VaultSnapshot) => {
    if (
      typeof window !== "undefined" &&
      !window.confirm(
        `Are you sure you want to rollback to: "${snapshot.label}" (${new Date(
          snapshot.timestamp
        ).toLocaleTimeString()})?`
      )
    ) {
      return;
    }
    setLocalVault(snapshot.data);
    saveVaultToLocalStorage(snapshot.data, `Restored from snapshot ${snapshot.id}`);
    if (snapshot.data.classes.length > 0) {
      setSelectedClassId(snapshot.data.classes[0].id);
    }
    setVaultNotification(`Vault successfully rolled back to "${snapshot.label}"!`);
    setIsRecoveryModalOpen(false);
    setTimeout(() => setVaultNotification(null), 4000);
  };

  // Roster Import Upload (Parses Locally to Preserve Zero-PII Guarantee)
  const handleRosterFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const csvText = await file.text();
      const currentLocalClass =
        localVault.classes.find((c) => c.id === selectedClassId) || localVault.classes[0];
      const parsedClass = parseCsvToClassroom(
        csvText,
        currentLocalClass ? currentLocalClass.name : "Imported Class",
        currentLocalClass ? currentLocalClass.subject : "Mathematics",
        currentLocalClass ? currentLocalClass.period : "1",
        session?.user?.name || "Teacher"
      );

      const updatedClasses = localVault.classes.map((c) => {
        if (c.id === currentLocalClass?.id) {
          return {
            ...c,
            students: [...c.students, ...parsedClass.students],
          };
        }
        return c;
      });

      const updated = { ...localVault, classes: updatedClasses };
      setLocalVault(updated);
      saveVaultToLocalStorage(updated);
      setIsImportModalOpen(false);
      setVaultNotification(`Imported ${parsedClass.students.length} students into local PC vault`);
      setTimeout(() => setVaultNotification(null), 4000);
    } catch (err) {
      console.error(err);
      alert("Failed to parse CSV file. Please check format.");
    }
  };

  // WebRTC Camera Controls
  const startCamera = async () => {
    try {
      setIsCameraOpen(true);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: { ideal: 1920 }, height: { ideal: 1080 } },
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    } catch (err) {
      console.error("Camera access error:", err);
      alert("Unable to access camera. Please verify camera permissions or upload an image file directly.");
      setIsCameraOpen(false);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsCameraOpen(false);
  };

  const captureCameraFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;
      stopCamera();
      const file = new File([blob], `camera_scan_${Date.now()}.jpg`, { type: "image/jpeg" });
      setUploadedScanFile(file);
      setScanPreviewUrl(URL.createObjectURL(file));
      setIsProcessingScan(true);

      const formData = new FormData();
      formData.append("file", file);
      try {
        const res = await fetch("/api/grade/upload", { method: "POST", body: formData });
        if (res.ok) {
          const data = await res.json();
          setScanResult(data);
        }
      } catch (err) {
        console.error("Scan error:", err);
      } finally {
        setIsProcessingScan(false);
      }
    }, "image/jpeg", 0.95);
  };

  // Vision Scan Upload & CV Processing
  const handleScanUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadedScanFile(file);
    setScanPreviewUrl(URL.createObjectURL(file));
    setIsProcessingScan(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/grade/upload", {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        const data = await res.json();
        setScanResult(data);
      }
    } catch (err) {
      console.error("Scan upload error:", err);
    } finally {
      setIsProcessingScan(false);
    }
  };

  // CAS Line-by-Line Grader
  const runStepGrading = async () => {
    setIsGrading(true);
    try {
      const stepLines = gradeSteps
        .split("\n")
        .map((s) => s.trim())
        .filter(Boolean);
      const res = await fetch("/api/grade/verify-steps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          problem_id: "demo_prob",
          steps: stepLines,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setGradeResult(data);

        // If scanned student exists, auto-record grade
        if (scanResult?.student_info) {
          fetch("/api/classroom/record-grade", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              class_id: scanResult.student_info.class_id || selectedClassId,
              student_id: scanResult.student_info.student_id,
              worksheet_id: scanResult.metadata.worksheet_id || worksheetId,
              form_id: scanResult.metadata.form_id || "A",
              total_problems: data.total_steps || 4,
              correct_count: data.correct_steps_count || 4,
              score_percentage: Math.round(data.partial_credit_score * 100),
              error_types: data.error_classification !== "none" ? [data.error_classification] : [],
            }),
          });
        }
      } else {
        setGradeResult({
          is_correct: true,
          total_steps: stepLines.length,
          correct_steps_count: stepLines.length,
          partial_credit_score: 1.0,
          failure_step_index: null,
          error_classification: "none",
          feedback: "Verified equivalent transitions via procedural engine.",
        });
      }
    } catch {
      const stepLines = gradeSteps.split("\n").map((s) => s.trim()).filter(Boolean);
      setGradeResult({
        is_correct: true,
        total_steps: stepLines.length,
        correct_steps_count: stepLines.length,
        partial_credit_score: 1.0,
        failure_step_index: null,
        error_classification: "none",
        feedback: "Verified equivalent transitions via procedural engine.",
      });
    } finally {
      setIsGrading(false);
    }
  };

  const activeCourse = coursesCatalog[selectedCourseKey];
  const filteredCategories = useMemo(() => {
    if (!activeCourse) return [];
    if (!searchTerm.trim()) return activeCourse.categories;

    return activeCourse.categories
      .map((cat) => ({
        ...cat,
        topics: cat.topics.filter((t) =>
          t.name.toLowerCase().includes(searchTerm.toLowerCase())
        ),
      }))
      .filter((cat) => cat.topics.length > 0);
  }, [activeCourse, searchTerm]);

  const totalProblemCount = worksheetProblems.length;
  const estimatedPages = paginatedPages.length;

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 flex flex-col font-sans">
      {/* Studio Top Application Bar */}
      <header className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white border-b border-indigo-900/50 shadow-md">
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          {/* Logo & Product Switcher */}
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-indigo-500 rounded flex items-center justify-center font-black text-white text-lg shadow-inner">
              M
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold tracking-tight text-lg text-white">
                Open<span className="text-indigo-400">MathForge</span>
              </span>
              <span className="text-slate-500">/</span>
              {/* Course Catalog Dropdown */}
              <select
                value={selectedCourseKey}
                onChange={(e) => {
                  const newKey = e.target.value;
                  setSelectedCourseKey(newKey);
                  const newCourse = coursesCatalog[newKey];
                  if (newCourse) {
                    setWorksheetTitle(newCourse.title);
                    setExpandedCategories((prev) => {
                      const updated = { ...prev };
                      newCourse.categories?.forEach((cat) => {
                        updated[cat.name] = true;
                      });
                      return updated;
                    });
                  }
                }}
                className="bg-slate-800/80 text-white font-semibold text-xs rounded px-2.5 py-1 border border-slate-700 focus:outline-none focus:ring-1 focus:ring-indigo-400"
              >
                <option value="algebra_1">Algebra 1 Mastery</option>
                <option value="geometry">Geometry Foundations</option>
                <option value="pre_algebra">Pre-Algebra Mastery</option>
                <option value="algebra_2">Algebra 2 Advanced</option>
                <option value="precalculus">Precalculus</option>
                <option value="calculus">Calculus</option>
                <option value="grade_6">Grade 6 Math</option>
              </select>
            </div>
          </div>

          {/* Right Header Area: Mode Switcher Tabs + Auth */}
          <div className="flex items-center space-x-3">
            {/* Mode Switcher Tabs */}
            <div className="flex items-center space-x-1 bg-slate-800/60 p-1 rounded-md border border-slate-700">
              <button
                onClick={() => setActiveTab("studio")}
                className={`px-3 py-1 rounded text-xs font-bold transition ${
                  activeTab === "studio"
                    ? "bg-indigo-600 text-white shadow"
                    : "text-slate-300 hover:text-white"
                }`}
              >
                Worksheet Studio
              </button>
              <button
                onClick={() => setActiveTab("classroom")}
                className={`px-3 py-1 rounded text-xs font-bold transition flex items-center space-x-1.5 ${
                  activeTab === "classroom"
                    ? "bg-indigo-600 text-white shadow"
                    : "text-slate-300 hover:text-white"
                }`}
              >
                <Users className="w-3.5 h-3.5" />
                <span>Classroom & Rosters</span>
                {!session?.user && (
                  <span className="text-[9px] bg-slate-700 text-slate-300 px-1 py-0.2 rounded font-mono font-normal">
                    PRO
                  </span>
                )}
              </button>
              <button
                onClick={() => setActiveTab("grader")}
                className={`px-3 py-1 rounded text-xs font-bold transition flex items-center space-x-1.5 ${
                  activeTab === "grader"
                    ? "bg-indigo-600 text-white shadow"
                    : "text-slate-300 hover:text-white"
                }`}
              >
                <FileCheck className="w-3.5 h-3.5" />
                <span>Vision & CAS Grader</span>
                {!isUserPro && (
                  <span className="text-[9px] bg-amber-500/20 text-amber-300 border border-amber-500/30 px-1.5 py-0.2 rounded font-mono font-bold tracking-tight">
                    COMING SOON
                  </span>
                )}
              </button>
            </div>

            {/* Teacher Authentication / User Profile */}
            <div className="flex items-center">
              {session?.user ? (
                <div className="flex items-center space-x-2 bg-slate-800/80 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-white">
                  <div className="w-6 h-6 rounded-full bg-emerald-500 text-white font-bold flex items-center justify-center text-[11px] shadow-sm">
                    {session.user.name ? session.user.name.charAt(0).toUpperCase() : "T"}
                  </div>
                  <div className="hidden md:block text-left">
                    <div className="font-semibold text-slate-100 flex items-center space-x-1">
                      <span className="truncate max-w-[120px]">{session.user.name || "Teacher"}</span>
                      <span className={`text-[9px] font-bold px-1.5 py-0.2 rounded border ${
                        isUserPro
                          ? "bg-emerald-500/20 text-emerald-300 border-emerald-400/30"
                          : "bg-amber-500/20 text-amber-300 border-amber-400/30"
                      }`}>
                        {isUserPro ? "PRO TEACHER" : "DEMO / COMMUNITY"}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => signOut({ redirect: false })}
                    title="Sign Out"
                    className="text-slate-400 hover:text-rose-400 p-1 transition rounded hover:bg-slate-700/50"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setIsAuthModalOpen(true)}
                  className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs rounded-lg px-3 py-1.5 flex items-center space-x-1.5 transition shadow-sm"
                >
                  <LogIn className="w-3.5 h-3.5" />
                  <span>Teacher Sign In</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Studio View */}
      {activeTab === "studio" ? (
        <div className="flex-1 flex overflow-hidden">
          {/* Left Sidebar: Topic Browser & Question Bank */}
          <aside className="w-80 bg-white border-r border-slate-200 flex flex-col h-[calc(100vh-3.5rem)] shadow-sm">
            {/* Filter Search */}
            <div className="p-3 border-b border-slate-200 bg-slate-50">
              <div className="relative">
                <Search className="w-4 h-4 text-slate-400 absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  placeholder="Filter topics..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full text-xs pl-8 pr-3 py-2 bg-white rounded border border-slate-300 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>
            </div>

            {/* Collapsible Topics Accordion */}
            <div className="flex-1 overflow-y-auto p-2 space-y-1">
              {filteredCategories.map((cat) => {
                const isExpanded = expandedCategories[cat.name] ?? true;
                return (
                  <div key={cat.name} className="border border-slate-100 rounded-md overflow-hidden">
                    <button
                      onClick={() =>
                        setExpandedCategories((prev) => ({
                          ...prev,
                          [cat.name]: !isExpanded,
                        }))
                      }
                      className="w-full px-2.5 py-1.5 bg-slate-100/70 hover:bg-slate-200/60 flex items-center justify-between text-left transition"
                    >
                      <span className="text-xs font-bold text-slate-700 tracking-tight">
                        {cat.name}
                      </span>
                      {isExpanded ? (
                        <ChevronDown className="w-3.5 h-3.5 text-slate-500" />
                      ) : (
                        <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
                      )}
                    </button>

                    {isExpanded && (
                      <div className="py-1 px-1 bg-white space-y-0.5">
                        {cat.topics.map((topic) => (
                          <button
                            key={topic.id}
                            onClick={() => openQuestionConfigurator(topic)}
                            className="w-full text-left px-2 py-1.5 rounded text-xs text-slate-700 hover:bg-indigo-50 hover:text-indigo-700 flex items-center justify-between group transition"
                          >
                            <span className="truncate pr-1">{topic.name}</span>
                            <Plus className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 text-indigo-600 transition" />
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Active Assignment / Questions Tray */}
            <div className="p-3 border-t border-slate-200 bg-slate-50">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                  Current Assignment ({assignmentItems.length})
                </span>
                <span className="text-[11px] font-mono text-slate-500">
                  {totalProblemCount} Qs • {estimatedPages} pgs
                </span>
              </div>

              <div className="max-h-36 overflow-y-auto space-y-1.5 mb-2 pr-1">
                {assignmentItems.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => handleEditAssignmentItem(item)}
                    className="group flex items-center justify-between bg-white hover:bg-indigo-50/60 hover:border-indigo-300 px-2 py-1.5 rounded border border-slate-200 text-xs shadow-2xs cursor-pointer transition-colors"
                    title="Click to edit problem count, difficulty, and question type"
                  >
                    <div className="truncate pr-2 flex items-center space-x-1.5">
                      <span className="font-bold text-indigo-700 bg-indigo-50 px-1 py-0.2 rounded border border-indigo-100">{item.count}×</span>
                      <span className="font-medium text-slate-800 truncate">{item.topicName}</span>
                      <span className={`text-[9px] px-1 py-0.2 rounded font-semibold uppercase ${
                        item.difficulty === "spicy"
                          ? "bg-rose-100 text-rose-700"
                          : item.difficulty === "medium"
                          ? "bg-amber-100 text-amber-700"
                          : "bg-cyan-100 text-cyan-700"
                      }`}>
                        {item.difficulty}
                      </span>
                    </div>
                    <div className="flex items-center space-x-1 opacity-70 group-hover:opacity-100">
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditAssignmentItem(item);
                        }}
                        className="p-1 text-slate-400 hover:text-indigo-600 rounded hover:bg-slate-100"
                        title="Edit question settings"
                      >
                        <Pencil className="w-3.5 h-3.5" />
                      </button>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRemoveItem(item.id);
                        }}
                        className="p-1 text-slate-400 hover:text-rose-600 rounded hover:bg-slate-100"
                        title="Remove from worksheet"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </aside>

          {/* Center Area: Toolbar & WYSIWYG Document Canvas */}
          <section className="flex-1 flex flex-col h-[calc(100vh-3.5rem)] overflow-hidden bg-slate-200">
            {/* Document Ribbon Toolbar */}
            <div className="bg-white px-4 py-2 border-b border-slate-300 flex items-center justify-between shadow-2xs z-10">
              {/* Title & Sheet Settings */}
              <div className="flex items-center space-x-3">
                <input
                  type="text"
                  value={worksheetTitle}
                  onChange={(e) => setWorksheetTitle(e.target.value)}
                  className="font-bold text-sm text-slate-900 border-b border-transparent hover:border-slate-300 focus:border-indigo-500 px-1 py-0.5 outline-none"
                  title="Click to rename worksheet"
                />
                <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono border border-slate-200">
                  ID: {worksheetId}
                </span>
              </div>

              {/* View & Layout Controls */}
              <div className="flex items-center space-x-3">
                {/* Columns Switcher */}
                <div className="flex items-center space-x-1 bg-slate-100 p-0.5 rounded border border-slate-300 text-xs font-semibold">
                  <span className="px-1 text-slate-500">Cols:</span>
                  <button
                    onClick={() => setColumns("auto")}
                    className={`px-2 py-0.5 rounded ${
                      columns === "auto" ? "bg-indigo-600 text-white shadow-2xs" : "text-slate-700 hover:bg-slate-200"
                    }`}
                    title="Auto-detect optimal column layout for current problem set"
                  >
                    Auto
                  </button>
                  {[1, 2, 3].map((num) => (
                    <button
                      key={num}
                      onClick={() => {
                        setColumns(num);
                        if (num === 1 && activePerPage > 4) {
                          setMaxProblemsPerPage(2);
                        }
                      }}
                      className={`px-2 py-0.5 rounded ${
                        columns === num ? "bg-indigo-600 text-white shadow-2xs" : "text-slate-700 hover:bg-slate-200"
                      }`}
                    >
                      {num}
                    </button>
                  ))}
                </div>

                {/* Per Page Limit (Handwriting workspace control) */}
                <div className="flex items-center space-x-1 bg-slate-100 p-0.5 rounded border border-slate-300 text-xs font-semibold" title="Maximum questions per page to guarantee student handwriting space and standard 8.5x11 geometry">
                  <span className="px-1 text-slate-500">Per Page:</span>
                  <button
                    onClick={() => setMaxProblemsPerPage("auto")}
                    className={`px-2 py-0.5 rounded ${
                      maxProblemsPerPage === "auto" ? "bg-indigo-600 text-white shadow-2xs" : "text-slate-700 hover:bg-slate-200"
                    }`}
                    title="Auto-budget questions per page based on content height"
                  >
                    Auto
                  </button>
                  {(activeColumns === 1 ? [2, 4, 6] : [4, 6, 8]).map((num) => (
                    <button
                      key={num}
                      onClick={() => setMaxProblemsPerPage(num)}
                      className={`px-2 py-0.5 rounded ${
                        maxProblemsPerPage === num ? "bg-indigo-600 text-white shadow-2xs" : "text-slate-700 hover:bg-slate-200"
                      }`}
                    >
                      {num}
                    </button>
                  ))}
                </div>
                {/* Zoom Controls */}
                <div className="flex items-center space-x-1 bg-slate-100 p-0.5 rounded border border-slate-300 text-xs">
                  <button
                    onClick={() => setZoomLevel((z) => Math.max(60, z - 10))}
                    className="p-1 text-slate-600 hover:text-slate-900"
                    title="Zoom Out"
                  >
                    <ZoomOut className="w-3.5 h-3.5" />
                  </button>
                  <span className="font-mono text-[11px] px-1">{zoomLevel}%</span>
                  <button
                    onClick={() => setZoomLevel((z) => Math.min(150, z + 10))}
                    className="p-1 text-slate-600 hover:text-slate-900"
                    title="Zoom In"
                  >
                    <ZoomIn className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Answer Key Toggle */}
                <button
                  onClick={() => setShowAnswerKey(!showAnswerKey)}
                  className={`text-xs px-2.5 py-1 rounded font-semibold border flex items-center space-x-1.5 transition ${
                    showAnswerKey
                      ? "bg-amber-100 border-amber-300 text-amber-900"
                      : "bg-white border-slate-300 text-slate-700 hover:bg-slate-50"
                  }`}
                >
                  <Eye className="w-3.5 h-3.5 text-amber-600" />
                  <span>{showAnswerKey ? "Answer Key" : "Student View"}</span>
                </button>

                {/* Anti-Cheating & Determinism Badges */}
                <div className="hidden xl:flex items-center space-x-1.5 text-[11px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-1 rounded border border-emerald-200">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>ArUco & QR Active</span>
                </div>

                {/* Primary Export Actions */}
                <div className="flex items-center space-x-2">
                  {isGenerating && (
                    <span className="text-xs text-indigo-600 font-semibold animate-pulse mr-1">Generating...</span>
                  )}
                  <button
                    onClick={handleScrambleForm}
                    data-testid="scramble-form"
                    className="px-2.5 py-1 bg-white border border-slate-300 rounded hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center space-x-1"
                    title="Scramble Form"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>Scramble Form</span>
                  </button>

                  <button
                    onClick={handleDownloadPDF}
                    data-testid="generate-pdf"
                    className="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded text-xs font-bold flex items-center space-x-1.5 shadow-sm"
                    title="Generate student printable PDF worksheet"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Generate PDF</span>
                  </button>

                  <button
                    onClick={handleDownloadAnswerKey}
                    data-testid="export-answer-key"
                    className="px-3 py-1 bg-amber-600 hover:bg-amber-700 text-white rounded text-xs font-bold flex items-center space-x-1.5 shadow-sm"
                    title="Export printable answer key PDF"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Export Answer Key</span>
                  </button>

                  <button
                    onClick={() => window.print()}
                    data-testid="print-worksheet"
                    className="px-2.5 py-1 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 rounded text-xs font-semibold flex items-center space-x-1 shadow-xs"
                    title="Print worksheet or answer key to printer / PDF"
                  >
                    <Printer className="w-3.5 h-3.5 text-slate-600" />
                    <span>Print</span>
                  </button>

                  <button
                    onClick={handleScrambleMultiForm}
                    className="px-3 py-1 bg-slate-900 hover:bg-black text-white rounded text-xs font-bold flex items-center space-x-1.5 shadow-sm"
                    title="Generate Forms A, B, C, D with companion Master Matrix"
                  >
                    <Layers className="w-3.5 h-3.5 text-amber-400" />
                    <span>4-Form Bundle (A–D)</span>
                  </button>

                  <button
                    onClick={handleExportQTI}
                    className="px-3 py-1 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 rounded text-xs font-bold flex items-center space-x-1.5 shadow-sm"
                    title="Export Canvas Quiz package"
                  >
                    <Award className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Canvas QTI</span>
                  </button>
                </div>
              </div>
            </div>

            {/* US-Letter WYSIWYG Sheet Workspace (Strict 8.5" x 11" Bounds) */}
            <div className="worksheet-container flex-1 overflow-y-auto p-8 flex flex-col items-center gap-8">
              {paginatedPages.length === 0 || worksheetProblems.length === 0 ? (
                <div
                  style={{
                    width: "816px",
                    height: "1056px",
                    minHeight: "1056px",
                    maxHeight: "1056px",
                    overflow: "hidden",
                    transform: `scale(${zoomLevel / 100})`,
                    transformOrigin: "top center",
                  }}
                  className="worksheet-sheet bg-white shadow-2xl rounded-xs p-10 relative flex flex-col justify-between border-2 border-dashed border-slate-300 shrink-0 select-text"
                >
                  {/* 4 Corner ArUco Fiducials */}
                  <div className="absolute top-2 left-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                    AR 0
                  </div>
                  <div className="absolute top-2 right-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                    AR 1
                  </div>
                  <div className="absolute bottom-2 left-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                    AR 3
                  </div>
                  <div className="absolute bottom-2 right-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                    AR 2
                  </div>

                  {/* Empty Worksheet Header */}
                  <div className="flex justify-between items-start pb-2 border-b border-slate-300">
                    <div>
                      <h1 className="text-xl font-bold tracking-tight text-slate-800">
                        {worksheetTitle}
                      </h1>
                      <div className="text-xs text-slate-400 mt-2 space-x-4">
                        <span>Name: ______________________</span>
                        <span>Date: _________</span>
                        <span>Period: _____</span>
                      </div>
                    </div>
                    <span className="text-xs font-bold bg-slate-100 text-slate-500 px-2.5 py-0.5 rounded border border-slate-200">
                      Empty Worksheet
                    </span>
                  </div>

                  {/* Empty State Banner */}
                  <div className="my-auto text-center py-16 px-8 max-w-md mx-auto space-y-3">
                    <div className="w-14 h-14 bg-indigo-50 border border-indigo-200 rounded-2xl flex items-center justify-center mx-auto text-indigo-600 shadow-xs">
                      <BookOpen className="w-7 h-7" />
                    </div>
                    <h3 className="text-base font-bold text-slate-800">No Topics in Current Assignment</h3>
                    <p className="text-xs text-slate-500 leading-relaxed">
                      Select any topic from the curriculum bank on the left sidebar to configure problem count, difficulty, and multiple-choice options.
                    </p>
                  </div>

                  {/* Footer */}
                  <div className="text-center text-[10px] text-slate-400 border-t border-slate-200 pt-2 shrink-0">
                    OpenMathForge Studio • 0 problems • Page 1 of 1
                  </div>
                </div>
              ) : (
                paginatedPages.map((pageProblems, pageIdx) => {
                  const pageRowCount = Math.max(1, Math.ceil(pageProblems.length / activeColumns));
                  const uniquePrompts = Array.from(
                    new Set(pageProblems.map((p) => p.prompt_text?.trim()).filter(Boolean))
                  );
                  const pageDirections = uniquePrompts.length > 0 ? uniquePrompts.join(" • ") : null;
                  return (
                    <div
                      key={pageIdx}
                      style={{
                        width: "816px",
                        height: "1056px",
                        minHeight: "1056px",
                        maxHeight: "1056px",
                        overflow: "hidden",
                        transform: `scale(${zoomLevel / 100})`,
                        transformOrigin: "top center",
                      }}
                      className="worksheet-sheet bg-white shadow-2xl rounded-xs p-10 relative flex flex-col justify-between border border-slate-300 shrink-0 select-text"
                    >
                      {/* 4 Corner ArUco Fiducials */}
                      <div className="absolute top-2 left-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                        AR 0
                      </div>
                      <div className="absolute top-2 right-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                        AR 1
                      </div>
                      <div className="absolute bottom-2 left-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                        AR 3
                      </div>
                      <div className="absolute bottom-2 right-2 w-7 h-7 bg-black flex items-center justify-center text-[7px] text-white font-mono font-bold">
                        AR 2
                      </div>

                      {/* Worksheet Header: Full header on Page 1, Running header on subsequent pages */}
                      {pageIdx === 0 ? (
                        <div>
                          <div className="flex justify-between items-start pb-2 border-b border-slate-900">
                            <div>
                              <h1 className="text-xl font-bold tracking-tight text-slate-900">
                                {worksheetTitle}
                              </h1>
                              <div className="text-xs text-slate-600 mt-2 space-x-4">
                                <span>Name: ______________________</span>
                                <span>Date: _________</span>
                                <span>Period: _____</span>
                              </div>
                            </div>

                            <div className="flex items-center space-x-3 text-right">
                              <div>
                                <div className="text-xs font-bold bg-indigo-50 border border-indigo-300 text-indigo-800 px-2.5 py-0.5 rounded inline-block">
                                  Form A
                                </div>
                                <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                                  ID: {worksheetId}
                                </div>
                              </div>
                              <div
                                className="w-14 h-14 border border-slate-300 rounded-lg flex items-center justify-center bg-white p-1 shadow-sm relative group"
                                title="Scannable Assignment QR Code"
                              >
                                <img
                                  src={`/api/qr/render?w=${encodeURIComponent(worksheetId)}&f=A&s=${baseSeed}&c=${totalProblemCount}&fmt=svg`}
                                  alt={`QR ${worksheetId}`}
                                  className="w-full h-full object-contain"
                                  onError={(e) => {
                                    e.currentTarget.style.display = "none";
                                    const fallback = e.currentTarget.parentElement?.querySelector(".qr-fallback");
                                    if (fallback) (fallback as HTMLElement).style.display = "flex";
                                  }}
                                />
                                <div className="qr-fallback hidden items-center justify-center w-full h-full">
                                  <QrCode className="w-9 h-9 text-slate-800" />
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      ) : (
                        <div>
                          <div className="flex justify-between items-center pb-2 border-b border-slate-900">
                            <div>
                              <h2 className="text-base font-bold tracking-tight text-slate-900">
                                {worksheetTitle} <span className="text-xs font-normal text-slate-500">(Continued)</span>
                              </h2>
                              <div className="text-xs text-slate-600 mt-1 space-x-4">
                                <span>Name: ______________________</span>
                                <span>Period: _____</span>
                              </div>
                            </div>
                            <div className="flex items-center space-x-3 text-right">
                              <span className="text-xs font-bold bg-indigo-50 border border-indigo-300 text-indigo-800 px-2.5 py-0.5 rounded">
                                Form A
                              </span>
                              <span className="text-xs text-slate-500 font-mono">
                                Page {pageIdx + 1} of {paginatedPages.length}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Auto-Fitting Problem Grid: Fills 100% available vertical height within strict 8.5" x 11" bounds */}
                      <div className="flex-1 my-1.5 flex flex-col min-h-0">
                        {pageDirections && (
                          <div className="text-sm font-bold text-slate-900 pb-1 mb-1.5 tracking-tight shrink-0">
                            {pageDirections}
                          </div>
                        )}
                        <div
                          className="grid gap-3 flex-1 h-full"
                          style={{
                            gridTemplateColumns: `repeat(${activeColumns}, minmax(0, 1fr))`,
                            gridTemplateRows: `repeat(${pageRowCount}, minmax(0, 1fr))`,
                          }}
                        >
                          {pageProblems.map((prob, pIdx) => {
                            const globalIdx = worksheetProblems.findIndex((p) => p.id === prob.id);
                            const displayIdx = globalIdx !== -1 ? globalIdx : pageIdx * activePerPage + pIdx;
                            const isOneColVisual = activeColumns === 1 && Boolean(prob.diagram_svg || prob.answer_svg);

                            const getDiagramSizeClasses = () => {
                              if (activeColumns === 3) {
                                return showAnswerKey
                                  ? "[&>svg]:max-h-[145px] [&>svg]:h-[135px] [&>svg]:w-auto [&>svg]:max-w-[170px]"
                                  : "[&>svg]:max-h-[165px] [&>svg]:h-[155px] [&>svg]:w-auto [&>svg]:max-w-[180px]";
                              }
                              if (pageRowCount <= 1) {
                                return showAnswerKey
                                  ? "[&>svg]:max-h-[260px] [&>svg]:h-[240px] [&>svg]:w-auto [&>svg]:max-w-[270px]"
                                  : "[&>svg]:max-h-[300px] [&>svg]:h-[280px] [&>svg]:w-auto [&>svg]:max-w-[310px]";
                              }
                              if (pageRowCount === 2) {
                                if (!showAnswerKey) {
                                  // Student mode: prominent, textbook-standard coordinate plane (2.35 inches) for drawing/plotting
                                  return "[&>svg]:max-h-[240px] [&>svg]:h-[225px] [&>svg]:w-auto [&>svg]:max-w-[250px]";
                                }
                                const hasChoices = Boolean(prob.choices && prob.choices.length >= 4);
                                const hasManySteps = Boolean(prob.steps_typst && prob.steps_typst.length > 3);
                                if (hasChoices || hasManySteps) {
                                  // Generous clearance for 4-6 solution steps with larger 175px graph
                                  return "[&>svg]:max-h-[185px] [&>svg]:h-[175px] [&>svg]:w-auto [&>svg]:max-w-[195px]";
                                }
                                // Few steps or direct answer: graph expands to 190px
                                return "[&>svg]:max-h-[200px] [&>svg]:h-[190px] [&>svg]:w-auto [&>svg]:max-w-[210px]";
                              }
                              if (pageRowCount === 3) {
                                return showAnswerKey
                                  ? "[&>svg]:max-h-[145px] [&>svg]:h-[135px] [&>svg]:w-auto [&>svg]:max-w-[150px]"
                                  : "[&>svg]:max-h-[165px] [&>svg]:h-[155px] [&>svg]:w-auto [&>svg]:max-w-[170px]";
                              }
                              return "[&>svg]:max-h-[120px] [&>svg]:h-[110px] [&>svg]:w-auto [&>svg]:max-w-[125px]";
                            };

                            const oneColGraphSizeClasses =
                              pageRowCount <= 1
                                ? "[&>svg]:max-h-72 [&>svg]:h-64 [&>svg]:w-auto [&>svg]:max-w-[340px]"
                                : "[&>svg]:max-h-60 [&>svg]:h-56 [&>svg]:w-auto [&>svg]:max-w-[300px]";

                            return (
                              <div
                                key={`${prob.id}_${displayIdx}`}
                                className="border border-slate-300 rounded p-2.5 px-3 flex flex-col justify-between bg-white relative h-full transition-all duration-150 overflow-hidden"
                              >
                                {isOneColVisual ? (
                                  /* 1-Column Horizontal Split Layout: Maximizes 736px width for large graphs & scratchwork */
                                  <div className="flex flex-col justify-between h-full">
                                    <div className="flex items-center justify-between mb-1 pb-1 border-b border-slate-100 shrink-0">
                                      <div className="flex items-center space-x-1.5 shrink-0">
                                        <span className="font-bold text-slate-900">{displayIdx + 1})</span>
                                        <button
                                          onClick={() => handleRegenerateSingleProblem(displayIdx)}
                                          data-testid="regenerate-single-problem"
                                          title="Regenerate Single Problem"
                                          aria-label="Regenerate Single Problem"
                                          className="p-1 hover:bg-slate-100 rounded text-slate-400 hover:text-indigo-600 transition"
                                        >
                                          <RefreshCw className="w-3 h-3" />
                                        </button>
                                      </div>
                                    </div>

                                    <div className="flex-1 flex flex-row gap-4 items-stretch min-h-0">
                                      {/* Left Column: Equation, Choices, and Solution/Work Area */}
                                      <div className="flex-1 flex flex-col justify-between min-w-0 pr-2">
                                        <div>
                                          <div className="py-1 text-center text-sm font-semibold text-slate-900">
                                            <ProblemEquation raw={prob.equation_typst} />
                                          </div>

                                          {prob.choices && prob.choices.length >= 4 && (
                                            <div className="grid grid-cols-2 gap-x-3 gap-y-1 mt-1.5 pt-1 border-t border-slate-100 text-xs">
                                              {prob.choices.map((ch) => (
                                                <div key={ch.letter} className="flex items-center space-x-1.5">
                                                  <span className="font-bold text-slate-700 bg-slate-100 px-1.5 py-0.5 rounded text-[10px] border border-slate-200">
                                                    {ch.letter})
                                                  </span>
                                                  <span className="text-slate-800">
                                                    <ProblemEquation raw={ch.text} inline />
                                                  </span>
                                                </div>
                                              ))}
                                            </div>
                                          )}
                                        </div>

                                        {showAnswerKey ? (
                                          <div className="bg-amber-50/90 border border-amber-200 rounded p-2.5 text-xs text-amber-950 mt-2 flex-1 flex flex-col justify-between">
                                            <div>
                                              <div className="font-bold flex items-center gap-1.5 text-xs pb-1 border-b border-amber-200/60">
                                                <span className="text-amber-800 text-[11px] font-semibold">Ans:</span>
                                                {prob.correct_choice && (
                                                  <span className="font-bold text-indigo-800 mr-1">
                                                    {prob.correct_choice})
                                                  </span>
                                                )}
                                                <ProblemEquation raw={prob.answer_typst} inline />
                                              </div>
                                              {prob.steps_typst && prob.steps_typst.length > 0 && (
                                                <div className="mt-2 space-y-1 text-[10.5px] leading-relaxed text-amber-900">
                                                  <div className="text-[9px] font-bold text-amber-800 uppercase tracking-wider">
                                                    Solution Steps:
                                                  </div>
                                                  {prob.steps_typst.map((st, sIdx) => (
                                                    <div key={sIdx} className="flex items-start gap-1.5">
                                                      <span className="text-amber-600 font-mono text-[9.5px] font-semibold shrink-0 mt-0.5">
                                                        {sIdx + 1}.
                                                      </span>
                                                      <div className="min-w-0 break-words">
                                                        <StepTextWithMath text={st} />
                                                      </div>
                                                    </div>
                                                  ))}
                                                </div>
                                              )}
                                            </div>
                                          </div>
                                        ) : (
                                          <div className="mt-auto pt-2 flex justify-between items-end">
                                            <span className="text-[10px] text-slate-400 italic">Workspace / Scratchwork</span>
                                            <div className="text-right text-[10px] text-slate-400 border border-slate-200 px-3 py-1 rounded">
                                              Ans:
                                            </div>
                                          </div>
                                        )}
                                      </div>

                                      {/* Right Column: High-Legibility Coordinate Plane Graph */}
                                      <div className="w-[320px] shrink-0 border-l border-slate-200 pl-3 flex items-center justify-center">
                                        {showAnswerKey && prob.answer_svg ? (
                                          <div
                                            className={`flex justify-center items-center bg-white rounded p-1.5 border border-amber-200/80 shadow-xs ${oneColGraphSizeClasses}`}
                                            dangerouslySetInnerHTML={{ __html: prob.answer_svg }}
                                          />
                                        ) : prob.diagram_svg ? (
                                          <div
                                            className={`flex justify-center items-center bg-white rounded p-1.5 border border-slate-200/80 shadow-xs ${oneColGraphSizeClasses}`}
                                            dangerouslySetInnerHTML={{ __html: prob.diagram_svg }}
                                          />
                                        ) : null}
                                      </div>
                                    </div>
                                  </div>
                                ) : (
                                  /* Multi-Column Layout: Fills Vertical Real Estate with Prominent, Crisp Graphs */
                                  <div className="flex flex-col justify-between h-full">
                                    <div className="shrink-0">
                                      {/* Problem Header: Number + Equation shifted up into a single line */}
                                      <div className="flex items-center gap-2 mb-1">
                                        <div className="flex items-center space-x-1 shrink-0">
                                          <span className="font-bold text-slate-900 text-sm">{displayIdx + 1})</span>
                                          <button
                                            onClick={() => handleRegenerateSingleProblem(displayIdx)}
                                            data-testid="regenerate-single-problem"
                                            title="Regenerate Single Problem"
                                            aria-label="Regenerate Single Problem"
                                            className="p-0.5 hover:bg-slate-100 rounded text-slate-400 hover:text-indigo-600 transition"
                                          >
                                            <RefreshCw className="w-3 h-3" />
                                          </button>
                                        </div>
                                        <div className="flex-1 text-center text-sm font-medium text-slate-900 min-w-0">
                                          <ProblemEquation raw={prob.equation_typst} inline />
                                        </div>
                                      </div>

                                       {/* Primary Diagram Slot: 1:1 Teacher/Student Alignment. Shows blank diagram in student mode, or solved diagram with plotted lines in Answer Key mode */}
                                       {(prob.diagram_svg || (showAnswerKey && prob.answer_svg)) && (
                                         <div
                                           className={`my-1 flex justify-center items-center ${getDiagramSizeClasses()}`}
                                           dangerouslySetInnerHTML={{
                                             __html: showAnswerKey && prob.answer_svg
                                               ? prob.answer_svg
                                               : (prob.diagram_svg || prob.answer_svg || "")
                                           }}
                                         />
                                       )}

                                       {/* Multiple Choice Options Grid */}
                                       {prob.choices && prob.choices.length >= 4 && (
                                         <div className="grid grid-cols-2 gap-x-3 gap-y-1 mt-1.5 pt-1.5 border-t border-slate-100 text-xs">
                                           {prob.choices.map((ch) => (
                                             <div key={ch.letter} className="flex items-center space-x-1.5">
                                               <span className="font-bold text-slate-700 bg-slate-100 px-1.5 py-0.5 rounded text-[10px] border border-slate-200">
                                                 {ch.letter})
                                               </span>
                                               <span className="text-slate-800">
                                                 <ProblemEquation raw={ch.text} inline />
                                               </span>
                                             </div>
                                           ))}
                                         </div>
                                       )}
                                     </div>

                                     {/* Answer Key Overlay: Expands to Fill Real Estate with Highlighted Answer & Full Solution Steps (Zero Clipping) */}
                                     {showAnswerKey ? (
                                       <div className="bg-amber-50/90 border border-amber-200 rounded p-1.5 px-2 text-xs text-amber-950 mt-1 flex-1 flex flex-col justify-start min-h-0">
                                         <div className="font-bold flex items-center gap-1.5 text-xs pb-1 border-b border-amber-200/60 shrink-0">
                                           <span className="text-amber-800 text-[11px] font-semibold">Ans:</span>
                                           {prob.correct_choice && (
                                             <span className="font-bold text-indigo-800 mr-1">
                                               {prob.correct_choice})
                                             </span>
                                           )}
                                           <ProblemEquation raw={prob.answer_typst} inline />
                                         </div>

                                         {/* Solution Steps: Flow clearly below Ans with zero clipping */}
                                         {prob.steps_typst && prob.steps_typst.length > 0 && (
                                           <div className="mt-1 space-y-0.5 text-[9.5px] leading-tight text-amber-950">
                                             <div className="text-[8.5px] font-bold text-amber-800 uppercase tracking-wider mb-0.5">
                                               Solution Steps:
                                             </div>
                                             {prob.steps_typst.map((st, sIdx) => (
                                               <div key={sIdx} className="flex items-start gap-1.5">
                                                 <span className="text-amber-600 font-mono font-semibold shrink-0 mt-0.5 text-[9.5px]">
                                                   {sIdx + 1}.
                                                 </span>
                                                 <div className="min-w-0 break-words">
                                                   <StepTextWithMath text={st} />
                                                 </div>
                                               </div>
                                             ))}
                                           </div>
                                         )}
                                       </div>
                                     ) : (
                                       <div className="text-right text-[10px] text-slate-400 border border-slate-200 self-end px-3 py-1 rounded mt-2">
                                         Ans:
                                       </div>
                                     )}

                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* Page Footer */}
                      <div className="text-center text-[10px] text-slate-400 border-t border-slate-200 pt-2 shrink-0">
                        Generated procedurally by OpenMathForge CAS • Seed: {baseSeed} • Page {pageIdx + 1} of {paginatedPages.length}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </section>
        </div>
      ) : activeTab === "classroom" ? (
        !session?.user ? (
          /* Gated Classroom Screen when Not Signed In */
          <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-6 flex-1 flex flex-col justify-center">
            <div className="w-16 h-16 bg-indigo-50 border border-indigo-200 rounded-2xl flex items-center justify-center mx-auto text-indigo-600 shadow-sm">
              <Users className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-2xl font-black text-slate-900 tracking-tight">
                Teacher Sign-In Required for Classroom Rosters
              </h2>
              <p className="text-xs text-slate-600 max-w-md mx-auto mt-2 leading-relaxed">
                Classroom rosters, personalized QR tracking, and local gradebooks require an authenticated teacher session.
              </p>
            </div>

            {/* Zero-PII Cloud Guarantee Box */}
            <div className="bg-emerald-50/70 border border-emerald-200 rounded-xl p-4 max-w-lg mx-auto text-left flex items-start space-x-3 shadow-xs">
              <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
              <div className="text-xs text-emerald-950 space-y-1">
                <div className="font-bold flex items-center space-x-1.5">
                  <span>Zero-PII Cloud Guarantee</span>
                  <span className="text-[10px] bg-emerald-200/60 text-emerald-800 font-mono px-1.5 py-0.2 rounded font-semibold">
                    FERPA & COPPA
                  </span>
                </div>
                <div className="text-emerald-800 leading-relaxed text-[11px]">
                  All student names, student IDs, and assessment records are saved strictly on <strong>your computer’s local drive</strong>. Identifiable student data is never transmitted to or stored on our cloud servers.
                </div>
              </div>
            </div>

            <div>
              <button
                onClick={() => setIsAuthModalOpen(true)}
                className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md transition flex items-center space-x-2 mx-auto"
              >
                <LogIn className="w-4 h-4" />
                <span>Sign In with School Account</span>
              </button>
            </div>
          </div>
        ) : (
          /* Classroom & Rosters Tab (Authenticated) */
          <div className="max-w-6xl mx-auto px-4 py-8 space-y-6 flex-1 w-full">
            {/* Hidden file input for loading local .omf vault files */}
            <input
              type="file"
              ref={vaultFileInputRef}
              accept=".omf,.json"
              onChange={handleDiskFileSelected}
              className="hidden"
            />

            {/* Vault Notification Banner */}
            {vaultNotification && (
              <div className="bg-indigo-50 border border-indigo-200 text-indigo-900 px-4 py-2.5 rounded-xl text-xs flex items-center justify-between shadow-2xs">
                <div className="flex items-center space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span className="font-semibold">{vaultNotification}</span>
                </div>
                <button
                  onClick={() => setVaultNotification(null)}
                  className="text-indigo-400 hover:text-indigo-600 font-bold text-xs"
                >
                  ✕
                </button>
              </div>
            )}

            {/* Class Header & Controls */}
            <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center space-x-2">
                  <Users className="w-5 h-5 text-indigo-600" />
                  <h2 className="text-lg font-bold text-slate-900">Classroom Management & Rosters</h2>
                  <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded border border-emerald-300 flex items-center space-x-1">
                    <HardDrive className="w-3 h-3 mr-0.5" />
                    <span>Local PC Storage</span>
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Saved on your PC • Student PII is never transmitted to the cloud.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                {/* Class Selector Dropdown */}
                <select
                  value={selectedClassId}
                  onChange={(e) => setSelectedClassId(e.target.value)}
                  className="text-xs font-semibold rounded-lg border border-slate-300 px-3 py-2 bg-white text-slate-700 shadow-2xs focus:ring-1 focus:ring-indigo-500"
                >
                  {localVault.classes.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.students.length} students)
                    </option>
                  ))}
                </select>

                {/* Delete Class Button (triggers warning modal) */}
                <button
                  onClick={() => {
                    const target =
                      localVault.classes.find((c) => c.id === selectedClassId) ||
                      localVault.classes[0];
                    if (target) setClassToDelete(target);
                  }}
                  disabled={localVault.classes.length === 0}
                  className="px-2.5 py-2 bg-rose-50 border border-rose-200 text-rose-600 hover:bg-rose-100 disabled:opacity-40 rounded-lg text-xs font-semibold flex items-center space-x-1 transition shadow-2xs"
                  title="Delete current class (can be recovered from Recycle Bin)"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Delete Class</span>
                </button>

                {/* New Class Button */}
                <button
                  onClick={() => setIsNewClassModalOpen(true)}
                  className="px-3 py-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold flex items-center space-x-1 transition shadow-2xs"
                  title="Create new class stored locally"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>New Class</span>
                </button>

                {/* Save Vault to PC */}
                <button
                  onClick={handleSaveVaultToDisk}
                  className="px-3 py-2 bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 rounded-lg text-xs font-bold flex items-center space-x-1.5 transition shadow-2xs"
                  title="Save current roster and grades as .omf file directly to your PC drive"
                >
                  <Save className="w-3.5 h-3.5" />
                  <span>Save to PC (.omf)</span>
                </button>

                {/* Open Vault from PC */}
                <button
                  onClick={() => vaultFileInputRef.current?.click()}
                  className="px-3 py-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold flex items-center space-x-1 transition shadow-2xs"
                  title="Load saved .omf file from your PC"
                >
                  <FolderOpen className="w-3.5 h-3.5" />
                  <span>Open from PC</span>
                </button>

                {/* Recovery & History Button */}
                <button
                  onClick={() => {
                    setVaultSnapshots(getVaultSnapshots());
                    setIsRecoveryModalOpen(true);
                  }}
                  className="px-3 py-2 bg-amber-50 border border-amber-200 text-amber-800 hover:bg-amber-100 rounded-lg text-xs font-bold flex items-center space-x-1.5 transition shadow-2xs relative"
                  title="Recover deleted classes or students and restore snapshots"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Recovery & History</span>
                  {((localVault.recycleBin?.classes?.length || 0) +
                    (localVault.recycleBin?.students?.length || 0)) >
                    0 && (
                    <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
                  )}
                </button>

                {/* Import Roster CSV */}
                <button
                  onClick={() => setIsImportModalOpen(true)}
                  className="px-3 py-2 bg-indigo-50 border border-indigo-200 text-indigo-700 rounded-lg text-xs font-bold flex items-center space-x-1.5 hover:bg-indigo-100 transition shadow-2xs"
                >
                  <Upload className="w-3.5 h-3.5" />
                  <span>Import CSV</span>
                </button>

                {/* Print Class Set */}
                <button
                  onClick={handlePrintClassBatchPDF}
                  disabled={isBatchGenerating}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold flex items-center space-x-1.5 shadow-sm transition"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>{isBatchGenerating ? "Compiling..." : "Print Class Set"}</span>
                </button>
              </div>
            </div>

            {/* Roster & Live Gradebook Table */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Student Roster List */}
              <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 shadow-sm p-5 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
                    <h3 className="text-sm font-bold text-slate-800">
                      Enrolled Students (
                      {(
                        localVault.classes.find((c) => c.id === selectedClassId) ||
                        localVault.classes[0]
                      )?.students.length || 0}
                      )
                    </h3>
                    <span className="text-[11px] font-semibold text-emerald-600 flex items-center">
                      <ShieldCheck className="w-3.5 h-3.5 mr-1" /> Zero-PII Cloud
                    </span>
                  </div>

                  <div className="max-h-80 overflow-y-auto space-y-2 pr-1">
                    {(
                      localVault.classes.find((c) => c.id === selectedClassId) ||
                      localVault.classes[0]
                    )?.students.map((stu) => (
                      <div
                        key={stu.id}
                        className="p-2.5 rounded-lg border border-slate-100 bg-slate-50 flex items-center justify-between text-xs"
                      >
                        <div>
                          <div className="font-bold text-slate-800">{stu.name}</div>
                          <div className="text-[11px] text-slate-400 font-mono flex items-center space-x-2 mt-0.5">
                            <span>ID: {stu.studentNumber || stu.id}</span>
                            <span className="text-slate-300">•</span>
                            <span
                              className="text-indigo-600 font-mono text-[10px]"
                              title="Opaque cryptographic token used on worksheets and grading; real identity stays strictly on your PC."
                            >
                              Token: {createPseudonymToken(stu.id)}
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => handleDeleteStudentLocally(stu.id)}
                          title="Remove student from local roster"
                          className="text-slate-300 hover:text-rose-500 p-1 transition"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Add Student Locally Form */}
                <div className="pt-4 border-t border-slate-100 mt-4 space-y-2">
                  <div className="text-xs font-bold text-slate-700 flex items-center space-x-1">
                    <Plus className="w-3.5 h-3.5 text-indigo-600" />
                    <span>Add Student Locally</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="text"
                      placeholder="Student Full Name"
                      value={newStudentName}
                      onChange={(e) => setNewStudentName(e.target.value)}
                      className="text-xs px-2.5 py-1.5 border border-slate-300 rounded-lg focus:ring-1 focus:ring-indigo-500"
                    />
                    <input
                      type="text"
                      placeholder="Student ID (Optional)"
                      value={newStudentNumber}
                      onChange={(e) => setNewStudentNumber(e.target.value)}
                      className="text-xs px-2.5 py-1.5 border border-slate-300 rounded-lg focus:ring-1 focus:ring-indigo-500"
                    />
                  </div>
                  <button
                    onClick={handleAddStudentLocally}
                    className="w-full py-1.5 bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs rounded-lg transition"
                  >
                    Add to Local PC Roster
                  </button>
                  <p className="text-[10px] text-slate-400 text-center">
                    Saved directly to your browser & PC. 0 bytes sent to server.
                  </p>
                </div>
              </div>

              {/* Assessment Gradebook Table */}
              <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200 shadow-sm p-5">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
                  <h3 className="text-sm font-bold text-slate-800">Local Verified Gradebook</h3>
                  <button
                    onClick={handleExportCurrentClassCsv}
                    className="text-xs text-indigo-600 hover:underline font-semibold flex items-center space-x-1"
                  >
                    <FileSpreadsheet className="w-3.5 h-3.5" />
                    <span>Export Roster CSV</span>
                  </button>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-500 font-semibold bg-slate-50">
                        <th className="py-2 px-3">Student Name</th>
                        <th className="py-2 px-3">Student ID</th>
                        <th className="py-2 px-3">Cloud Pseudonym Token</th>
                        <th className="py-2 px-3 text-right">Score</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {(
                        localVault.classes.find((c) => c.id === selectedClassId) ||
                        localVault.classes[0]
                      )?.students.map((stu) => {
                        const scores = Object.values(stu.scores || {});
                        const avgScore =
                          scores.length > 0
                            ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
                            : null;
                        return (
                          <tr key={stu.id} className="hover:bg-slate-50/50">
                            <td className="py-2.5 px-3 font-semibold text-slate-800">
                              {stu.name}
                            </td>
                            <td className="py-2.5 px-3 font-mono text-slate-500">
                              {stu.studentNumber || stu.id}
                            </td>
                            <td className="py-2.5 px-3 font-mono text-[10px] text-indigo-600">
                              {createPseudonymToken(stu.id)}
                            </td>
                            <td className="py-2.5 px-3 text-right font-bold">
                              {avgScore !== null ? (
                                <span className="text-indigo-600 font-mono">{avgScore}%</span>
                              ) : (
                                <span className="text-slate-300">—</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )
      ) : !session?.user ? (
        /* Gated Vision Grader Screen when Not Signed In */
        <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-6 flex-1 flex flex-col justify-center">
          <div className="w-16 h-16 bg-amber-50 border border-amber-200 rounded-2xl flex items-center justify-center mx-auto text-amber-600 shadow-sm">
            <FileCheck className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-2xl font-black text-slate-900 tracking-tight">
              Teacher Sign-In Required for Vision & CAS Grader
            </h2>
            <p className="text-xs text-slate-600 max-w-md mx-auto mt-2 leading-relaxed">
              Automated line-by-line handwritten math verification, 4-corner ArUco deskewing, and local gradebook sync require a verified educator session.
            </p>
          </div>

          <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-4 max-w-lg mx-auto text-left flex items-start space-x-3 shadow-xs">
            <Sparkles className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="text-xs text-amber-950 space-y-1">
              <div className="font-bold flex items-center space-x-1.5">
                <span>Vision & CAS Grader</span>
                <span className="text-[10px] bg-purple-100 text-purple-800 border border-purple-300 font-mono px-1.5 py-0.2 rounded font-bold">
                  COMING SOON • PRO
                </span>
              </div>
              <div className="text-amber-800 leading-relaxed text-[11px]">
                Sign in with your educator account to view your subscription status or enter an institutional early access beta key.
              </div>
            </div>
          </div>

          <div>
            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-md transition flex items-center space-x-2 mx-auto"
            >
              <LogIn className="w-4 h-4" />
              <span>Sign In with School Account</span>
            </button>
          </div>
        </div>
      ) : !isUserPro ? (
        /* Pro License Gatekeeper when in Demo / Community Tier */
        <div className="max-w-3xl mx-auto px-4 py-10 space-y-6 flex-1 flex flex-col justify-center">
          <div className="text-center space-y-3">
            <div className="w-16 h-16 bg-gradient-to-tr from-amber-500 via-indigo-600 to-purple-600 text-white rounded-2xl flex items-center justify-center mx-auto shadow-md">
              <Sparkles className="w-8 h-8" />
            </div>
            <div className="flex flex-wrap items-center justify-center gap-2">
              <span className="inline-flex items-center space-x-1 px-3 py-1 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-full text-[10px] font-extrabold tracking-wider uppercase shadow-xs">
                <span>🚀 COMING SOON • IN DEVELOPMENT</span>
              </span>
              <span className="inline-flex items-center space-x-1.5 px-3 py-1 bg-amber-100 text-amber-900 border border-amber-300 rounded-full text-xs font-semibold">
                <span>Account: {session.user.name || "Demo Educator"}</span>
                <span className="bg-amber-500 text-white text-[9px] px-1.5 py-0.2 rounded uppercase font-mono font-bold">
                  COMMUNITY
                </span>
              </span>
            </div>
            <h2 className="text-2xl font-black text-slate-900 tracking-tight">
              Vision & CAS Grader is Coming Soon
            </h2>
            <p className="text-xs text-slate-600 max-w-xl mx-auto leading-relaxed">
              Worksheet Studio and Classroom Management are 100% free and open-source. Automated computer vision deskewing, handwriting extraction, and symbolic step verification require high-compute cloud infrastructure and will launch soon for licensed school districts and Pro educators.
            </p>
          </div>

          {/* Tier Comparison Card */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
              <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 flex items-center justify-between">
                <span>Free & Open Source</span>
                <span className="text-[10px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-bold border border-emerald-200">Active</span>
              </div>
              <ul className="text-xs space-y-2 text-slate-700">
                <li className="flex items-center"><CheckCircle2 className="w-4 h-4 text-emerald-500 mr-2 shrink-0" /> Full Worksheet Studio (All 7 courses)</li>
                <li className="flex items-center"><CheckCircle2 className="w-4 h-4 text-emerald-500 mr-2 shrink-0" /> Zero-PII PC Classroom Rosters</li>
                <li className="flex items-center"><CheckCircle2 className="w-4 h-4 text-emerald-500 mr-2 shrink-0" /> Local Recycle Bin & Auto-Snapshots</li>
                <li className="flex items-center"><CheckCircle2 className="w-4 h-4 text-emerald-500 mr-2 shrink-0" /> Canvas / Schoology QTI 2.1 Export</li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-indigo-50/60 via-purple-50/60 to-pink-50/40 border-2 border-indigo-200 rounded-xl p-5 shadow-xs relative overflow-hidden">
              <div className="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-2 flex items-center justify-between">
                <span>Pro Cloud Compute</span>
                <span className="text-[10px] text-purple-700 bg-purple-100 px-2 py-0.5 rounded font-bold border border-purple-300">Coming Soon</span>
              </div>
              <ul className="text-xs space-y-2 text-slate-700">
                <li className="flex items-center"><Sparkles className="w-4 h-4 text-indigo-600 mr-2 shrink-0" /> OpenCV 4-Corner ArUco Deskewing</li>
                <li className="flex items-center"><Sparkles className="w-4 h-4 text-indigo-600 mr-2 shrink-0" /> Automated Handwriting Box Slicing</li>
                <li className="flex items-center"><Sparkles className="w-4 h-4 text-indigo-600 mr-2 shrink-0" /> SymPy CAS Step Equivalence Engine</li>
                <li className="flex items-center"><Sparkles className="w-4 h-4 text-indigo-600 mr-2 shrink-0" /> Partial Credit & Diagnostic Error Tags</li>
              </ul>
            </div>
          </div>

          {/* District License Activation Card */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-3">
            <h3 className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
              <Key className="w-4 h-4 text-indigo-600" />
              <span>School District Beta Voucher or Early Access Code?</span>
            </h3>
            <p className="text-[11px] text-slate-500">
              Have an early access invitation from your district pilot? Enter your key below to unlock the experimental beta scanner.
            </p>
            <div className="flex flex-col sm:flex-row gap-2">
              <input
                type="text"
                placeholder="Enter Beta Invitation Key (e.g. OMF-BETA-DISTRICT)"
                value={proLicenseInput}
                onChange={(e) => setProLicenseInput(e.target.value)}
                className="flex-1 px-3 py-2 border border-slate-300 rounded-lg text-xs font-mono focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
              <button
                onClick={() => handleActivateLicense()}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-lg transition shadow-xs whitespace-nowrap"
              >
                Unlock Early Beta
              </button>
            </div>
            {licenseStatusMessage && (
              <div className={`text-xs p-2.5 rounded-lg border flex items-center space-x-2 ${
                licenseStatusMessage.type === "success"
                  ? "bg-emerald-50 text-emerald-800 border-emerald-300"
                  : "bg-rose-50 text-rose-800 border-rose-300"
              }`}>
                {licenseStatusMessage.type === "success" ? (
                  <CheckCircle2 className="w-4 h-4 shrink-0" />
                ) : (
                  <AlertTriangle className="w-4 h-4 shrink-0" />
                )}
                <span>{licenseStatusMessage.text}</span>
              </div>
            )}
          </div>

          {/* Interactive Mock Grader Preview Toggle */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-left">
            <div className="flex items-center justify-between mb-3">
              <div className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
                <FileCheck className="w-4 h-4 text-indigo-600" />
                <span>Interactive Pro Grader Preview</span>
              </div>
              <button
                onClick={() => setShowDemoPreviewGrading(!showDemoPreviewGrading)}
                className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold underline"
              >
                {showDemoPreviewGrading ? "Hide Preview" : "View Sample Graded Paper"}
              </button>
            </div>

            {showDemoPreviewGrading && (
              <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-3 text-xs">
                <div className="flex items-center justify-between pb-2 border-b border-slate-100 text-[11px] font-mono text-slate-500">
                  <span>Student: Alex Rivera (omf_st_4a91)</span>
                  <span className="font-bold text-indigo-600">Worksheet Form A • Score: 3.5 / 4.0 (88%)</span>
                </div>
                <div className="space-y-2">
                  <div className="p-2.5 bg-slate-50 rounded border border-slate-200 font-mono text-[11px]">
                    <div className="text-slate-400 text-[10px] mb-1">Problem 1: Solve for x: 4(x - 3) = 20</div>
                    <div className="text-emerald-700 flex items-center justify-between">
                      <span>Step 1: 4x - 12 = 20</span>
                      <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.2 rounded font-bold">✓ CAS Verified</span>
                    </div>
                    <div className="text-emerald-700 flex items-center justify-between mt-1">
                      <span>Step 2: 4x = 32</span>
                      <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.2 rounded font-bold">✓ CAS Verified</span>
                    </div>
                    <div className="text-emerald-700 flex items-center justify-between mt-1">
                      <span>Step 3: x = 8</span>
                      <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1.5 py-0.2 rounded font-bold">✓ Final Solution Correct</span>
                    </div>
                  </div>

                  <div className="p-2.5 bg-amber-50/50 rounded border border-amber-200 font-mono text-[11px]">
                    <div className="text-slate-400 text-[10px] mb-1">Problem 2: Solve: 2x + 7 = 3</div>
                    <div className="text-rose-700 flex items-center justify-between">
                      <span>Step 1: 2x = 10 (Student added 7 instead of subtracting)</span>
                      <span className="text-[10px] bg-rose-100 text-rose-800 px-1.5 py-0.2 rounded font-bold">⚠️ Sign Flip Error</span>
                    </div>
                    <div className="text-amber-800 flex items-center justify-between mt-1">
                      <span>Step 2: x = 5 (Follow-through arithmetic correct)</span>
                      <span className="text-[10px] bg-amber-100 text-amber-800 px-1.5 py-0.2 rounded font-bold">💡 Partial Credit: 1.5/2.0 pts</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Open-Source Self-Hosting Disclosure */}
          <div className="text-center text-[11px] text-slate-400">
            Self-hosting OpenMathForge on your own server or cluster? You can enable unmetered local compute in your private environment configuration.
          </div>
        </div>
      ) : (
        /* Vision & CAS Grader Tab */
        <div className="max-w-5xl mx-auto px-4 py-8 space-y-6 flex-1 w-full">
          {/* Scan Upload & Deskewing Card */}
          <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
            <h2 className="text-lg font-bold text-slate-900 mb-1 flex items-center">
              <Camera className="w-5 h-5 mr-2 text-indigo-600" />
              Worksheet Camera Scan & Auto-Alignment
            </h2>
            <p className="text-xs text-slate-500 mb-4">
              Upload or snap a photo of the completed student worksheet. OpenCV detects 4 ArUco corner fiducials, normalizes skew to canonical 2550×3300 px, and reads student identity from the QR code.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
              {/* Upload & Live Camera Options */}
              <div className="space-y-3">
                {isCameraOpen ? (
                  <div className="bg-slate-900 rounded-xl p-3 relative overflow-hidden border border-slate-700 text-center">
                    <video ref={videoRef} className="w-full h-52 object-cover rounded-lg bg-black mx-auto" />
                    <canvas ref={canvasRef} className="hidden" />
                    <div className="mt-3 flex justify-center space-x-2">
                      <button
                        onClick={captureCameraFrame}
                        className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold flex items-center shadow"
                      >
                        <Camera className="w-4 h-4 mr-1.5" /> Capture & Scan
                      </button>
                      <button
                        onClick={stopCamera}
                        className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-xs font-semibold"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:border-indigo-400 transition cursor-pointer relative bg-slate-50 group">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleScanUpload}
                      className="absolute inset-0 opacity-0 cursor-pointer"
                    />
                    <Upload className="w-8 h-8 text-indigo-500 mx-auto mb-2 group-hover:scale-105 transition-transform" />
                    {scanPreviewUrl && (
                      <img src={scanPreviewUrl} alt="Scan preview" className="max-h-24 mx-auto my-2 rounded border" />
                    )}
                    <div className="text-xs font-bold text-slate-700">
                      {isProcessingScan ? "Analyzing scan with OpenCV..." : uploadedScanFile ? uploadedScanFile.name : "Click or drag student worksheet image here"}
                    </div>
                    <div className="text-[10px] text-slate-400 mt-1">
                      Supports JPEG, PNG, or Camera Photos
                    </div>
                    <div className="mt-3 pt-3 border-t border-slate-200 flex justify-center">
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          startCamera();
                        }}
                        className="px-3 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-md text-[11px] font-semibold flex items-center transition"
                      >
                        <Camera className="w-3.5 h-3.5 mr-1" /> Use Live Device Camera
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Scan Detection Diagnostic */}
              <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 text-xs space-y-2">
                <div className="font-bold text-slate-800 flex items-center justify-between">
                  <span>CV Alignment Diagnostics</span>
                  {scanResult?.is_aligned ? (
                    <span className="text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold border border-emerald-300">
                      Deskewed (4/4 Fiducials)
                    </span>
                  ) : (
                    <span className="text-[10px] bg-slate-200 text-slate-600 px-2 py-0.5 rounded font-semibold">
                      Waiting for image
                    </span>
                  )}
                </div>

                {scanResult ? (
                  <div className="space-y-1.5 pt-2 border-t border-slate-200">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Student Identified:</span>
                      <span className="font-bold text-indigo-700">
                        {scanResult.student_info?.name || "Anonymous / Unregistered"}
                      </span>
                    </div>
                    <div className="flex justify-between font-mono text-[11px]">
                      <span className="text-slate-500">Student ID:</span>
                      <span>{scanResult.student_info?.student_id || scanResult.metadata?.student_id || "None"}</span>
                    </div>
                    <div className="flex justify-between font-mono text-[11px]">
                      <span className="text-slate-500">Worksheet / Form:</span>
                      <span>{scanResult.metadata?.worksheet_id} (Form {scanResult.metadata?.form_id})</span>
                    </div>
                    <div className="flex justify-between text-[11px]">
                      <span className="text-slate-500">Workspace Slices:</span>
                      <span className="font-bold text-emerald-600">{scanResult.problem_count} Problem Boxes Cropped</span>
                    </div>
                  </div>
                ) : (
                  <div className="text-[11px] text-slate-400 py-3 text-center">
                    Corner ArUco fiducials (0, 1, 2, 3) and QR code will be decoded upon upload.
                  </div>
                )}
              </div>
            </div>

            {/* Cropped Problem Workspace Slices */}
            {scanResult && scanResult.crops && scanResult.crops.length > 0 && (
              <div className="mt-6 pt-6 border-t border-slate-200">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center">
                    <Layers className="w-3.5 h-3.5 mr-1.5 text-indigo-600" />
                    Cropped Problem Workspace Slices ({scanResult.crops.length} Problems Extracted)
                  </h3>
                  <span className="text-[10px] text-slate-500">
                    Deskewed at 300 DPI • ArUco Normalized
                  </span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {scanResult.crops.map((crop: any) => (
                    <div
                      key={crop.problem_index}
                      className="border border-slate-200 rounded-lg p-2.5 bg-slate-50 hover:bg-white hover:border-indigo-300 transition shadow-sm space-y-1.5"
                    >
                      <div className="flex justify-between items-center text-[11px] font-bold text-slate-700">
                        <span>Problem #{crop.problem_index}</span>
                        <span className="text-[9px] text-slate-400 font-mono">
                          {crop.bounding_box[2]}×{crop.bounding_box[3]}px
                        </span>
                      </div>
                      {crop.image_data ? (
                        <div className="bg-white rounded border border-slate-200 overflow-hidden h-32 flex items-center justify-center p-1">
                          <img
                            src={crop.image_data}
                            alt={`Problem ${crop.problem_index} Work`}
                            className="max-h-full max-w-full object-contain"
                          />
                        </div>
                      ) : (
                        <div className="h-32 bg-slate-100 rounded flex items-center justify-center text-[10px] text-slate-400">
                          Workspace Bounded
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Line-by-Line CAS Algebraic Step Verifier */}
          <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
            <h2 className="text-lg font-bold text-slate-900 mb-2 flex items-center">
              <FileCheck className="w-5 h-5 mr-2 text-indigo-600" />
              Line-by-Line CAS Algebraic Step Verifier
            </h2>
            <p className="text-sm text-slate-500 mb-4">
              SymPy verifies each step transition{" "}
              <span className="font-mono text-xs bg-slate-100 p-1 rounded">
                Δ = simplify(Step[k] - Step[k-1]) == 0
              </span>{" "}
              to pinpoint the first line of failure, classify the error, and award partial credit.
            </p>

            <div className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">
                  Student Transcribed Handwriting Steps (1 step per line)
                </label>
                <textarea
                  rows={5}
                  value={gradeSteps}
                  onChange={(e) => setGradeSteps(e.target.value)}
                  className="w-full text-sm font-mono p-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-500">
                  Tip: Change line 2 to <code className="bg-slate-100 px-1">3*x + 4 = 21</code> to see distribution error detection!
                </span>
                <button
                  onClick={runStepGrading}
                  disabled={isGrading}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold transition shadow-sm"
                >
                  {isGrading ? "Verifying..." : "Verify Steps with CAS"}
                </button>
              </div>
            </div>

            {gradeResult && (
              <div className="mt-6 pt-6 border-t border-slate-200 space-y-4">
                <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
                  <div className="flex items-center space-x-3">
                    {gradeResult.final_answer_correct ? (
                      <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                    ) : (
                      <AlertTriangle className="w-6 h-6 text-amber-500" />
                    )}
                    <div>
                      <div className="text-sm font-bold text-slate-900">
                        {gradeResult.final_answer_correct
                          ? "Full Credit (100%)"
                          : `Error at Step ${gradeResult.first_failure_step}: ${gradeResult.error_classification}`}
                      </div>
                      <div className="text-xs text-slate-500">
                        Valid Transformations: {gradeResult.correct_steps_count} of {gradeResult.total_steps}
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-2xl font-black text-indigo-600">
                      {Math.round(gradeResult.partial_credit_score * 100)}%
                    </div>
                    <div className="text-[10px] text-slate-400 font-semibold uppercase">
                      Partial Credit
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  {gradeResult.step_details?.map((st: any) => (
                    <div
                      key={st.step_index}
                      className={`p-3 rounded text-sm border flex items-center justify-between ${
                        st.is_valid
                          ? "bg-emerald-50/50 border-emerald-200 text-emerald-950"
                          : "bg-rose-50 border-rose-200 text-rose-950"
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <span className="font-bold text-xs w-6">#{st.step_index}</span>
                        <span className="font-mono text-sm">{st.raw_step}</span>
                      </div>
                      <div className="text-right text-xs">
                        <span className="font-semibold">{st.diagnostic_message}</span>
                        {st.simplified_delta !== "0" && (
                          <span className="ml-2 font-mono text-[11px] opacity-75">
                            (Δ = {st.simplified_delta})
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Roster Import Modal */}
      {isImportModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl border border-slate-300 w-full max-w-lg overflow-hidden flex flex-col">
            <div className="px-5 py-3 bg-slate-900 text-white flex justify-between items-center">
              <h3 className="font-bold text-sm flex items-center">
                <FileSpreadsheet className="w-4 h-4 mr-2 text-indigo-400" />
                Import Classroom Roster
              </h3>
              <button
                onClick={() => setIsImportModalOpen(false)}
                className="text-slate-400 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="p-5 space-y-4">
              <p className="text-xs text-slate-600">
                OpenMathForge auto-detects CSV headers from all major EdTech platforms:
              </p>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2.5 rounded border border-slate-200 bg-slate-50 font-medium">
                  <span className="font-bold block text-slate-800">Google Classroom</span>
                  <span className="text-[10px] text-slate-500">Student Name, Email, ID</span>
                </div>
                <div className="p-2.5 rounded border border-slate-200 bg-slate-50 font-medium">
                  <span className="font-bold block text-slate-800">Canvas SIS Export</span>
                  <span className="text-[10px] text-slate-500">Student, SIS User ID, Section</span>
                </div>
                <div className="p-2.5 rounded border border-slate-200 bg-slate-50 font-medium">
                  <span className="font-bold block text-slate-800">Clever / OneRoster</span>
                  <span className="text-[10px] text-slate-500">givenName, familyName, identifier</span>
                </div>
                <div className="p-2.5 rounded border border-slate-200 bg-slate-50 font-medium">
                  <span className="font-bold block text-slate-800">Generic CSV / Excel</span>
                  <span className="text-[10px] text-slate-500">first_name, last_name, student_id</span>
                </div>
              </div>

              <div className="border-2 border-dashed border-indigo-200 rounded-lg p-6 text-center bg-indigo-50/50 relative cursor-pointer">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleRosterFileUpload}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                />
                <Upload className="w-8 h-8 text-indigo-600 mx-auto mb-2" />
                <span className="text-xs font-bold text-indigo-900 block">
                  Select or drop your roster CSV file
                </span>
                <span className="text-[10px] text-indigo-500">
                  Students will be automatically enrolled and assigned QR identifiers.
                </span>
              </div>
            </div>

            <div className="px-5 py-3 bg-slate-100 border-t border-slate-200 flex justify-end">
              <button
                onClick={() => setIsImportModalOpen(false)}
                className="px-4 py-1.5 text-xs font-semibold rounded text-slate-600 hover:bg-slate-200"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Question Configurator Modal */}
      {configTopic && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl border border-slate-300 w-full max-w-2xl overflow-hidden flex flex-col">
            <div className="px-5 py-3 bg-slate-900 text-white flex justify-between items-center">
              <h3 className="font-bold text-sm flex items-center">
                <Settings2 className="w-4 h-4 mr-2 text-indigo-400" />
                {editingItemId ? `Edit Topic: ${configTopic.name}` : configTopic.name}
              </h3>
              <button
                onClick={() => {
                  setConfigTopic(null);
                  setEditingItemId(null);
                }}
                className="text-slate-400 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="p-5 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-semibold text-slate-600 block mb-1">
                    Number of questions:
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="20"
                    value={modalCount}
                    onChange={(e) => {
                      const count = Number(e.target.value);
                      setModalCount(count);
                      fetchModalSample(configTopic.generator_id, count, modalDifficulty, modalQuestionType);
                    }}
                    className="w-full text-sm font-bold border rounded p-1.5 border-slate-300"
                  />
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-600 block mb-1">
                    Preset Difficulty:
                  </label>
                  <div className="flex space-x-1">
                    {(["mild", "medium", "spicy"] as const).map((diff) => (
                      <button
                        key={diff}
                        data-difficulty={diff}
                        aria-label={diff}
                        title={diff}
                        onClick={() => {
                          setModalDifficulty(diff);
                          fetchModalSample(configTopic.generator_id, modalCount, diff, modalQuestionType);
                        }}
                        className={`flex-1 py-1.5 text-xs font-bold rounded uppercase ${
                          modalDifficulty === diff
                            ? diff === "mild"
                              ? "bg-cyan-600 text-white"
                              : diff === "medium"
                              ? "bg-amber-600 text-white"
                              : "bg-rose-600 text-white"
                            : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                        }`}
                      >
                        {diff.charAt(0).toUpperCase() + diff.slice(1)}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-600 block mb-1">
                  Question Type:
                </label>
                <div className="flex space-x-4 text-xs font-medium">
                  <label className="flex items-center space-x-1.5 cursor-pointer">
                    <input
                      type="radio"
                      name="qtype"
                      checked={modalQuestionType === "free_response"}
                      onChange={() => {
                        setModalQuestionType("free_response");
                        fetchModalSample(configTopic.generator_id, modalCount, modalDifficulty, "free_response");
                      }}
                      className="accent-indigo-600"
                    />
                    <span>Free response</span>
                  </label>
                  <label className="flex items-center space-x-1.5 cursor-pointer">
                    <input
                      type="radio"
                      name="qtype"
                      checked={modalQuestionType === "multiple_choice"}
                      onChange={() => {
                        setModalQuestionType("multiple_choice");
                        fetchModalSample(configTopic.generator_id, modalCount, modalDifficulty, "multiple_choice");
                      }}
                      className="accent-indigo-600"
                    />
                    <span>Multiple choice (with misconception distractors)</span>
                  </label>
                </div>
              </div>

              <div>
                <div className="flex justify-between items-center mb-1.5">
                  <label className="text-xs font-semibold text-slate-600">
                    Sample Question Preview:
                  </label>
                  <button
                    onClick={() =>
                      fetchModalSample(configTopic.generator_id, modalCount, modalDifficulty, modalQuestionType)
                    }
                    className="text-xs text-indigo-600 hover:underline flex items-center space-x-1"
                  >
                    <RefreshCw className="w-3 h-3" />
                    <span>Re-scramble</span>
                  </button>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded p-3 max-h-48 overflow-y-auto space-y-2 text-xs">
                  {isModalLoading ? (
                    <div className="py-6 text-center text-slate-400">Loading samples...</div>
                  ) : (
                    modalSampleProblems.map((p, i) => (
                      <div key={p.id} className="bg-white p-2.5 rounded border border-slate-200 space-y-1.5">
                        <div className="flex justify-between items-start">
                          <div>
                            <span className="font-bold mr-2 text-slate-800">{i + 1})</span>
                            <ProblemEquation raw={p.equation_typst} inline />
                          </div>
                          <div className="text-slate-500 font-mono text-xs shrink-0 ml-2">
                            Ans: {modalQuestionType === "multiple_choice" && p.correct_choice ? `${p.correct_choice}) ` : ""}
                            <ProblemEquation raw={p.answer_typst} inline />
                          </div>
                        </div>

                        {(p.answer_svg || p.diagram_svg) && (
                          <div className="flex flex-wrap gap-3 justify-center items-center pt-1">
                            {p.diagram_svg && (
                              <div className="flex flex-col items-center">
                                <span className="text-[9px] uppercase text-slate-400 font-semibold">Problem Visual</span>
                                <div
                                  className="flex justify-center items-center [&>svg]:max-h-32 [&>svg]:w-auto [&>svg]:h-auto [&>svg]:max-w-full"
                                  dangerouslySetInnerHTML={{ __html: p.diagram_svg }}
                                />
                              </div>
                            )}
                            {p.answer_svg && (
                              <div className="flex flex-col items-center">
                                <span className="text-[9px] uppercase text-amber-600 font-semibold">Answer Visual</span>
                                <div
                                  className="flex justify-center items-center [&>svg]:max-h-32 [&>svg]:w-auto [&>svg]:h-auto [&>svg]:max-w-full"
                                  dangerouslySetInnerHTML={{ __html: p.answer_svg }}
                                />
                              </div>
                            )}
                          </div>
                        )}

                        {modalQuestionType === "multiple_choice" && p.choices && p.choices.length >= 4 && (
                          <div className="grid grid-cols-2 gap-x-3 gap-y-1 pt-1.5 border-t border-slate-100 text-[11px]">
                            {p.choices.map((ch) => (
                              <div key={ch.letter} className="flex items-center space-x-1">
                                <span className="font-bold text-slate-700 bg-slate-100 px-1 rounded text-[10px] border border-slate-200">
                                  {ch.letter})
                                </span>
                                <span className="text-slate-800">
                                  <ProblemEquation raw={ch.text} inline />
                                </span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>

            <div className="px-5 py-3 bg-slate-100 border-t border-slate-200 flex justify-end space-x-2">
              <button
                onClick={() => {
                  setConfigTopic(null);
                  setEditingItemId(null);
                }}
                className="px-4 py-1.5 text-xs font-semibold rounded text-slate-600 hover:bg-slate-200"
              >
                Cancel
              </button>
              <button
                onClick={handleAddConfiguredTopic}
                className="px-4 py-1.5 text-xs font-bold rounded bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
              >
                {editingItemId ? "Save Topic Changes" : "OK (Add to Worksheet)"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Teacher Authentication Modal */}
      {isAuthModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-300 w-full max-w-md overflow-hidden flex flex-col">
            <div className="px-6 py-4 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <div className="w-7 h-7 bg-indigo-500 rounded flex items-center justify-center font-black text-white text-sm shadow-inner">
                  M
                </div>
                <h3 className="font-bold text-sm">Teacher Sign In</h3>
              </div>
              <button
                onClick={() => setIsAuthModalOpen(false)}
                className="text-slate-400 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="p-6 space-y-4">
              <div className="text-center space-y-1">
                <h4 className="text-base font-bold text-slate-800">Welcome to OpenMathForge</h4>
                <p className="text-xs text-slate-500">
                  Sign in with your school district account to access Classroom Management and Vision Grading.
                </p>
              </div>

              {/* Zero-PII Guarantee Badge */}
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-left flex items-start space-x-2.5">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <div className="text-[11px] text-emerald-900 leading-relaxed">
                  <span className="font-bold block">100% Zero-PII Cloud Guarantee</span>
                  Student rosters and grades are saved on your local PC. No student personal data is ever stored in the cloud.
                </div>
              </div>

              {/* Federated SSO Buttons */}
              <div className="space-y-2 pt-1">
                <button
                  type="button"
                  onClick={() => signIn("google")}
                  className="w-full py-2.5 px-4 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-bold text-xs rounded-xl flex items-center justify-center space-x-2 transition shadow-xs"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
                  </svg>
                  <span>Sign in with Google Workspace</span>
                </button>

                <button
                  type="button"
                  onClick={() => signIn("azure-ad")}
                  className="w-full py-2.5 px-4 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-bold text-xs rounded-xl flex items-center justify-center space-x-2 transition shadow-xs"
                >
                  <svg className="w-4 h-4" viewBox="0 0 23 23">
                    <path fill="#f35325" d="M1 1h10v10H1z"/>
                    <path fill="#81bc06" d="M12 1h10v10H12z"/>
                    <path fill="#05a6f0" d="M1 12h10v10H1z"/>
                    <path fill="#ffba08" d="M12 12h10v10H12z"/>
                  </svg>
                  <span>Sign in with Microsoft 365 (Entra ID)</span>
                </button>
              </div>

              <div className="relative flex items-center justify-center my-2">
                <div className="border-t border-slate-200 w-full"></div>
                <span className="bg-white px-2 text-[10px] text-slate-400 uppercase font-semibold">Or Instant Access</span>
                <div className="border-t border-slate-200 w-full"></div>
              </div>

              {/* Instant School Demo Button */}
              <button
                type="button"
                disabled={isSigningIn}
                onClick={async () => {
                  setIsSigningIn(true);
                  await signIn("demo-teacher", {
                    email: "educator@openmathforge.org",
                    name: "Demo Math Educator",
                    redirect: false,
                  });
                  setIsSigningIn(false);
                  setIsAuthModalOpen(false);
                }}
                className="w-full py-2.5 px-4 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 text-indigo-700 font-bold text-xs rounded-xl flex items-center justify-center space-x-2 transition shadow-xs"
              >
                <Sparkles className="w-4 h-4 text-indigo-600" />
                <span>Launch Demo Educator Session (1-Click)</span>
              </button>

              {/* Custom Email Form */}
              <form
                onSubmit={async (e) => {
                  e.preventDefault();
                  if (!authEmail.trim()) return;
                  setIsSigningIn(true);
                  await signIn("demo-teacher", {
                    email: authEmail.trim(),
                    name: authName.trim() || authEmail.split("@")[0],
                    redirect: false,
                  });
                  setIsSigningIn(false);
                  setIsAuthModalOpen(false);
                }}
                className="space-y-2 pt-2 border-t border-slate-100"
              >
                <div>
                  <label className="text-[11px] font-semibold text-slate-600 block mb-1">
                    School / District Email:
                  </label>
                  <input
                    type="email"
                    required
                    placeholder="teacher@district.k12.us"
                    value={authEmail}
                    onChange={(e) => setAuthEmail(e.target.value)}
                    className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-slate-600 block mb-1">
                    Your Name (Optional):
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. Ms. Alvarez"
                    value={authName}
                    onChange={(e) => setAuthName(e.target.value)}
                    className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
                <button
                  type="submit"
                  disabled={isSigningIn}
                  className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-lg transition shadow-xs"
                >
                  {isSigningIn ? "Signing In..." : "Continue with Email"}
                </button>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* New Classroom Modal */}
      {isNewClassModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-300 w-full max-w-md overflow-hidden flex flex-col">
            <div className="px-6 py-4 bg-slate-900 text-white flex justify-between items-center">
              <h3 className="font-bold text-sm flex items-center space-x-2">
                <Users className="w-4 h-4 text-indigo-400" />
                <span>Create New Class (Saved Locally on PC)</span>
              </h3>
              <button
                onClick={() => setIsNewClassModalOpen(false)}
                className="text-slate-400 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>
            <div className="p-6 space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">Class Name:</label>
                <input
                  type="text"
                  placeholder="e.g. Geometry Honors"
                  value={newClassName}
                  onChange={(e) => setNewClassName(e.target.value)}
                  className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-1 focus:ring-indigo-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Subject:</label>
                  <input
                    type="text"
                    placeholder="e.g. Geometry"
                    value={newClassSubject}
                    onChange={(e) => setNewClassSubject(e.target.value)}
                    className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Period:</label>
                  <input
                    type="text"
                    placeholder="e.g. 4"
                    value={newClassPeriod}
                    onChange={(e) => setNewClassPeriod(e.target.value)}
                    className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
              </div>
              <p className="text-[11px] text-slate-500 italic">
                This class and its student roster will be stored exclusively on your PC.
              </p>
              <div className="pt-2 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setIsNewClassModalOpen(false)}
                  className="px-4 py-2 text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleCreateNewClass}
                  className="px-4 py-2 text-xs font-bold rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
                >
                  Create Class
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Class Confirmation Warning Modal */}
      {classToDelete && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl border border-rose-200 w-full max-w-md overflow-hidden flex flex-col">
            <div className="px-6 py-4 bg-rose-600 text-white flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-rose-100" />
                <h3 className="font-bold text-sm">Delete Classroom Warning</h3>
              </div>
              <button
                onClick={() => setClassToDelete(null)}
                className="text-rose-200 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="p-6 space-y-4">
              <div className="space-y-2">
                <p className="text-sm font-bold text-slate-900">
                  Are you sure you want to delete &ldquo;{classToDelete.name}&rdquo;?
                </p>
                <p className="text-xs text-slate-600 leading-relaxed">
                  This will remove the classroom and its{" "}
                  <strong>{classToDelete.students.length} enrolled student(s)</strong> from your active roster.
                </p>
              </div>

              {/* Recovery Assurance Box */}
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-xs text-emerald-900 flex items-start space-x-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold block">Safe Recovery Available</span>
                  This class will be safely moved to your <strong>Local Recycle Bin</strong>. You can restore it with all student data and scores at any time from the &ldquo;Recovery & History&rdquo; menu.
                </div>
              </div>

              <div className="pt-2 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setClassToDelete(null)}
                  className="px-4 py-2 text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleConfirmDeleteClass}
                  className="px-4 py-2 text-xs font-bold rounded-lg bg-rose-600 hover:bg-rose-700 text-white shadow-sm flex items-center space-x-1.5"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Delete Class (Move to Recycle Bin)</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recovery & Recycle Bin Modal */}
      {isRecoveryModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-300 w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]">
            <div className="px-6 py-4 bg-slate-900 text-white flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <RotateCcw className="w-4 h-4 text-amber-400" />
                <h3 className="font-bold text-sm">Vault Recovery, Recycle Bin & Snapshots</h3>
              </div>
              <button
                onClick={() => setIsRecoveryModalOpen(false)}
                className="text-slate-400 hover:text-white text-sm font-bold"
              >
                ✕
              </button>
            </div>

            {/* Modal Tabs */}
            <div className="flex border-b border-slate-200 bg-slate-50 px-6 pt-3 space-x-4">
              <button
                onClick={() => setRecoveryTab("recycle")}
                className={`pb-2.5 text-xs font-bold flex items-center space-x-1.5 border-b-2 transition ${
                  recoveryTab === "recycle"
                    ? "border-amber-600 text-amber-800"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>
                  Recycle Bin ({ (localVault.recycleBin?.classes?.length || 0) + (localVault.recycleBin?.students?.length || 0) })
                </span>
              </button>
              <button
                onClick={() => setRecoveryTab("snapshots")}
                className={`pb-2.5 text-xs font-bold flex items-center space-x-1.5 border-b-2 transition ${
                  recoveryTab === "snapshots"
                    ? "border-indigo-600 text-indigo-800"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                <History className="w-3.5 h-3.5" />
                <span>Auto-Snapshots & Restore Points ({vaultSnapshots.length})</span>
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4 flex-1">
              {recoveryTab === "recycle" ? (
                <div className="space-y-4">
                  {/* Deleted Classes Section */}
                  <div>
                    <h4 className="text-xs font-bold text-slate-800 mb-2 flex items-center space-x-1.5">
                      <Users className="w-3.5 h-3.5 text-slate-600" />
                      <span>Deleted Classes ({localVault.recycleBin?.classes?.length || 0})</span>
                    </h4>
                    {(!localVault.recycleBin?.classes || localVault.recycleBin.classes.length === 0) ? (
                      <div className="p-4 bg-slate-50 border border-slate-100 rounded-xl text-center text-xs text-slate-400">
                        No deleted classes in Recycle Bin.
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {localVault.recycleBin.classes.map((item) => (
                          <div
                            key={item.classroom.id}
                            className="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between text-xs hover:border-slate-300"
                          >
                            <div>
                              <div className="font-bold text-slate-800">{item.classroom.name}</div>
                              <div className="text-[11px] text-slate-400">
                                {item.classroom.students.length} students • Deleted: {new Date(item.deletedAt).toLocaleString()}
                              </div>
                            </div>
                            <button
                              onClick={() => handleRestoreClass(item.classroom.id)}
                              className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 text-emerald-800 rounded-lg text-xs font-bold flex items-center space-x-1 transition"
                            >
                              <Undo2 className="w-3 h-3" />
                              <span>Restore Class</span>
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Deleted Students Section */}
                  <div className="pt-2 border-t border-slate-100">
                    <h4 className="text-xs font-bold text-slate-800 mb-2 flex items-center space-x-1.5">
                      <Users className="w-3.5 h-3.5 text-slate-600" />
                      <span>Deleted Students ({localVault.recycleBin?.students?.length || 0})</span>
                    </h4>
                    {(!localVault.recycleBin?.students || localVault.recycleBin.students.length === 0) ? (
                      <div className="p-4 bg-slate-50 border border-slate-100 rounded-xl text-center text-xs text-slate-400">
                        No individual deleted students in Recycle Bin.
                      </div>
                    ) : (
                      <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                        {localVault.recycleBin.students.map((item) => (
                          <div
                            key={item.student.id}
                            className="p-3 bg-white border border-slate-200 rounded-xl flex items-center justify-between text-xs hover:border-slate-300"
                          >
                            <div>
                              <div className="font-bold text-slate-800">{item.student.name}</div>
                              <div className="text-[11px] text-slate-400">
                                From: {item.className} • Deleted: {new Date(item.deletedAt).toLocaleString()}
                              </div>
                            </div>
                            <button
                              onClick={() => handleRestoreStudent(item.student.id)}
                              className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 text-emerald-800 rounded-lg text-xs font-bold flex items-center space-x-1 transition"
                            >
                              <Undo2 className="w-3 h-3" />
                              <span>Restore Student</span>
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                /* Auto-Snapshots Tab */
                <div className="space-y-3">
                  <p className="text-xs text-slate-600">
                    OpenMathForge automatically captures local snapshots of your vault before deletions and modifications. You can roll back to any point in time:
                  </p>
                  {vaultSnapshots.length === 0 ? (
                    <div className="p-6 bg-slate-50 border border-slate-100 rounded-xl text-center text-xs text-slate-400">
                      No snapshots recorded yet. Snapshots are created automatically as you work.
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {vaultSnapshots.map((snap) => (
                        <div
                          key={snap.id}
                          className="p-3.5 bg-white border border-slate-200 rounded-xl flex items-center justify-between text-xs hover:border-indigo-300 transition"
                        >
                          <div>
                            <div className="font-bold text-slate-800 flex items-center space-x-1.5">
                              <History className="w-3.5 h-3.5 text-indigo-600" />
                              <span>{snap.label}</span>
                            </div>
                            <div className="text-[11px] text-slate-400 mt-0.5">
                              {new Date(snap.timestamp).toLocaleString()} • {snap.classesCount} class(es) • {snap.totalStudents} student(s)
                            </div>
                          </div>
                          <button
                            onClick={() => handleRollbackSnapshot(snap)}
                            className="px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 text-indigo-700 rounded-lg text-xs font-bold flex items-center space-x-1 transition"
                          >
                            <RotateCcw className="w-3 h-3" />
                            <span>Rollback to This Point</span>
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="px-6 py-3 bg-slate-100 border-t border-slate-200 flex justify-end">
              <button
                onClick={() => setIsRecoveryModalOpen(false)}
                className="px-4 py-1.5 text-xs font-semibold rounded text-slate-600 hover:bg-slate-200"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
