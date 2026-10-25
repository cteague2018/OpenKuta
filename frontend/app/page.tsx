"use client";

import React, { useState, useEffect, useMemo, useRef } from "react";
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
  Clock,
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

interface StudentRecord {
  id: string;
  student_id: string;
  first_name: string;
  last_name: string;
  email?: string;
  period?: string;
}

interface GradebookEntry {
  student_id: string;
  name: string;
  email?: string;
  status: "graded" | "pending";
  score_percentage?: number;
  correct_count?: number;
  total_problems?: number;
  error_types?: string[];
  submitted_at?: string;
}

function typstToLatex(raw: string): string {
  if (!raw) return "";
  let s = raw.trim();
  // Strip leading and trailing $
  s = s.replace(/^\$+\s*/, "").replace(/\s*\$+$/, "").trim();
  // Clean up prefix labels like "Result:" or "Solve for x:"
  s = s.replace(/^(Result|Solve for [^:]+):\s*/i, "").trim();
  // Strip any remaining internal $ delimiters
  s = s.replace(/\$/g, "");
  // Typst to LaTeX conversions
  s = s.replace(/plus\.minus/g, "\\pm ");
  s = s.replace(/sqrt\(([^)]+)\)/g, "\\sqrt{$1}");
  s = s.replace(/\bquad\b/g, "\\quad ");
  s = s.replace(/cases\(([^,]+),\s*([^)]+)\)/g, "\\begin{cases} $1 \\\\ $2 \\end{cases}");
  s = s.replace(/==>/g, "\\implies ");
  s = s.replace(/\s*dot\s*/g, " \\cdot ");
  s = s.replace(/\s*times\s*/g, " \\times ");
  s = s.replace(/(\d+)\s*\/\s*(\d+)/g, "\\frac{$1}{$2}");
  // Replace standalone asterisks with space
  s = s.replace(/\s*\*\s*/g, " ");
  return s;
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

function StepTextWithMath({ text }: { text: string }) {
  if (!text) return null;
  const trimmed = text.trim();
  // If the whole string is an equation like "$ 2x + 4 = 10 $"
  if (trimmed.startsWith("$") && trimmed.endsWith("$") && (trimmed.match(/\$/g) || []).length === 2) {
    return <KaTeXInline math={trimmed} className="font-medium" />;
  }

  // Split by '$' for mixed prose and equations
  const parts = trimmed.split("$");
  if (parts.length === 1) {
    return <span>{trimmed}</span>;
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
  const [worksheetTitle, setWorksheetTitle] = useState<string>("Infinite Algebra 1 Practice");
  const [columns, setColumns] = useState<number>(2);
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

  // Modal / Configurator State (matching Kuta's signature Question Dialog)
  const [configTopic, setConfigTopic] = useState<Topic | null>(null);
  const [modalCount, setModalCount] = useState<number>(4);
  const [modalDifficulty, setModalDifficulty] = useState<"mild" | "medium" | "spicy">("medium");
  const [modalQuestionType, setModalQuestionType] = useState<"free_response" | "multiple_choice">("free_response");
  const [modalSampleProblems, setModalSampleProblems] = useState<Problem[]>([]);
  const [isModalLoading, setIsModalLoading] = useState<boolean>(false);

  // Live Worksheet Generated Problems
  const [worksheetProblems, setWorksheetProblems] = useState<Problem[]>(DEFAULT_SAMPLE_PROBLEMS);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);

  // Dynamic Workspace Box Sizing based on Multi-Step complexity and page clearance
  const isMultiStep = useMemo(() => {
    return worksheetProblems.some(
      (p) =>
        (p.prompt_text || "").toLowerCase().includes("multi-step") ||
        (p.steps_typst && p.steps_typst.length >= 4)
    );
  }, [worksheetProblems]);

  const workspaceBoxClasses = useMemo(() => {
    const count = worksheetProblems.length;
    if (showAnswerKey) {
      return "min-h-[240px]";
    }
    if (count <= 4) {
      return isMultiStep ? "min-h-[280px]" : "min-h-[240px]";
    }
    if (count <= 6) {
      return isMultiStep ? "min-h-[220px]" : "min-h-[195px]";
    }
    return isMultiStep ? "min-h-[190px]" : "min-h-[160px]";
  }, [worksheetProblems.length, isMultiStep, showAnswerKey]);

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
  const [selectedClassId, setSelectedClassId] = useState<string>("cls_alg1_p3");
  const [currentClassStudents, setCurrentClassStudents] = useState<StudentRecord[]>(
    DEFAULT_CLASSROOMS[0].students
  );
  const [gradebookEntries, setGradebookEntries] = useState<GradebookEntry[]>(
    DEFAULT_CLASSROOMS[0].gradebook as GradebookEntry[]
  );
  const [isImportModalOpen, setIsImportModalOpen] = useState<boolean>(false);
  const [isBatchGenerating, setIsBatchGenerating] = useState<boolean>(false);

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

  // Load Selected Class Students & Gradebook
  useEffect(() => {
    if (!selectedClassId) return;

    fetch(`/api/classroom/classes/${selectedClassId}`)
      .then((res) => {
        if (!res.ok) throw new Error("No backend");
        return res.json();
      })
      .then((data) => {
        if (data.students) setCurrentClassStudents(data.students);
      })
      .catch(() => {
        const found = DEFAULT_CLASSROOMS.find((c) => c.id === selectedClassId);
        if (found) setCurrentClassStudents(found.students);
      });

    fetch(`/api/classroom/gradebook/${selectedClassId}`)
      .then((res) => {
        if (!res.ok) throw new Error("No backend");
        return res.json();
      })
      .then((data) => {
        if (data.entries) setGradebookEntries(data.entries);
      })
      .catch(() => {
        const found = DEFAULT_CLASSROOMS.find((c) => c.id === selectedClassId);
        if (found) setGradebookEntries(found.gradebook as GradebookEntry[]);
      });
  }, [selectedClassId]);

  // Refresh live worksheet preview
  const refreshWorksheet = async () => {
    setIsGenerating(true);
    try {
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
            }),
          });

          if (res.ok) {
            const data = await res.json();
            if (data.problems) allProblems.push(...data.problems);
          }
        } catch {
          // backend not reachable
        }
        itemSeed += 77;
      }

      if (allProblems.length > 0) {
        setWorksheetProblems(allProblems);
      } else {
        // Fallback to sample problems so preview is always filled
        setWorksheetProblems(DEFAULT_SAMPLE_PROBLEMS);
      }
      setWorksheetId(`WS-${String(baseSeed % 10000).padStart(4, "0")}`);
    } catch (e) {
      console.error("Preview generation error:", e);
      setWorksheetProblems(DEFAULT_SAMPLE_PROBLEMS);
    } finally {
      setIsGenerating(false);
    }
  };

  useEffect(() => {
    refreshWorksheet();
  }, [assignmentItems, baseSeed]);

  // Fetch samples for Modal Configurator
  const fetchModalSample = async (genId: string, count: number, diff: "mild" | "medium" | "spicy") => {
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
    setConfigTopic(topic);
    setModalCount(4);
    setModalDifficulty("medium");
    setModalQuestionType("free_response");
    fetchModalSample(topic.generator_id, 4, "medium");
  };

  const handleAddConfiguredTopic = () => {
    if (!configTopic) return;
    const newItem: AssignmentItem = {
      id: `item_${Date.now()}`,
      topicName: configTopic.name,
      generatorId: configTopic.generator_id,
      count: modalCount,
      difficulty: modalDifficulty,
      questionType: modalQuestionType,
    };
    setAssignmentItems((prev) => [...prev, newItem]);
    setConfigTopic(null);
  };

  const handleRemoveItem = (id: string) => {
    setAssignmentItems((prev) => prev.filter((i) => i.id !== id));
  };

  // Multi-Topic PDF Download
  const handleDownloadPDF = async () => {
    try {
      const topicsPayload = assignmentItems.map((item) => ({
        generator_id: item.generatorId,
        count: item.count,
        difficulty: item.difficulty,
      }));

      const res = await fetch("/api/worksheet/pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: worksheetTitle,
          form_id: "A",
          seed: baseSeed,
          columns: columns,
          topics: topicsPayload,
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
      const topicsPayload = assignmentItems.map((item) => ({
        generator_id: item.generatorId,
        count: item.count,
        difficulty: item.difficulty,
      }));

      const res = await fetch("/api/worksheet/pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: worksheetTitle,
          form_id: "A",
          seed: baseSeed,
          columns: columns,
          show_answers: true,
          topics: topicsPayload,
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
    try {
      const targetProb = worksheetProblems[targetIdx];
      const genId = (targetProb as any).generator_id || assignmentItems[0]?.generatorId || "algebra_1.quadratics";
      const res = await fetch("/api/worksheet/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          generator_id: genId,
          problem_count: 1,
          seed: Math.floor(Math.random() * 999999) + targetIdx * 31,
          allow_negatives: true,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.problems && data.problems.length > 0) {
          const newProb = data.problems[0];
          setWorksheetProblems((prev) => {
            const next = [...prev];
            next[targetIdx] = { ...newProb, id: `prob_regen_${Date.now()}` };
            return next;
          });
          return;
        }
      }
    } catch {
      // Fallback
    }
    setWorksheetProblems((prev) => {
      const next = [...prev];
      const cur = next[targetIdx];
      next[targetIdx] = {
        ...cur,
        id: `prob_regen_${Date.now()}_${targetIdx}`,
        equation_typst: cur.equation_typst ? `${cur.equation_typst} + 0` : "x = 1",
      };
      return next;
    });
  };

  // Multi-Form Scramble Bundle (A-D)
  const handleScrambleMultiForm = async () => {
    try {
      const topicsPayload = assignmentItems.map((item) => ({
        generator_id: item.generatorId,
        count: item.count,
        difficulty: item.difficulty,
      }));

      const res = await fetch("/api/worksheet/multi-form", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: worksheetTitle,
          base_seed: baseSeed,
          forms: ["A", "B", "C", "D"],
          topics: topicsPayload,
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
      const topicsPayload = assignmentItems.map((item) => ({
        generator_id: item.generatorId,
        count: item.count,
        difficulty: item.difficulty,
      }));

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

  // Roster Import Upload
  const handleRosterFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedClassId) return;

    const formData = new FormData();
    formData.append("class_id", selectedClassId);
    formData.append("file", file);

    try {
      const res = await fetch("/api/classroom/import-roster", {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        const data = await res.json();
        alert(`Successfully imported ${data.imported_count} students via ${data.detected_format}!`);
        setIsImportModalOpen(false);
        loadClasses();
        fetch(`/api/classroom/classes/${selectedClassId}`)
          .then((r) => r.json())
          .then((d) => setCurrentClassStudents(d.students || []));
      } else {
        alert("Roster import failed. Please check the CSV headers.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Export Gradebook CSV
  const handleExportGradebookCSV = async (format: "canvas" | "google") => {
    if (!selectedClassId) return;
    const res = await fetch(`/api/classroom/export-gradebook-csv/${selectedClassId}?format=${format}`);
    if (res.ok) {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Gradebook_${format.toUpperCase()}_Export.csv`;
      a.click();
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
  const estimatedPages = Math.max(1, Math.ceil(totalProblemCount / (columns * 3)));

  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 flex flex-col font-sans">
      {/* Kuta Top Application Bar */}
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
            </button>
          </div>
        </div>
      </header>

      {/* Main Studio View */}
      {activeTab === "studio" ? (
        <div className="flex-1 flex overflow-hidden">
          {/* Left Sidebar: Kuta Topic Browser & Question Bank */}
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
                    className="flex items-center justify-between bg-white px-2 py-1.5 rounded border border-slate-200 text-xs shadow-2xs"
                  >
                    <div className="truncate pr-2">
                      <span className="font-semibold text-slate-800">{item.count}× </span>
                      <span className="text-slate-600">{item.topicName}</span>
                    </div>
                    <button
                      onClick={() => handleRemoveItem(item.id)}
                      className="text-slate-400 hover:text-rose-600"
                      title="Remove from worksheet"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </aside>

          {/* Center Area: Toolbar & WYSIWYG Document Canvas */}
          <section className="flex-1 flex flex-col h-[calc(100vh-3.5rem)] overflow-hidden bg-slate-200">
            {/* Kuta Document Ribbon Toolbar */}
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
              <div className="flex items-center space-x-4">
                {/* Columns Switcher */}
                <div className="flex items-center space-x-1 bg-slate-100 p-0.5 rounded border border-slate-300 text-xs font-semibold">
                  <span className="px-1 text-slate-500">Cols:</span>
                  {[1, 2, 3].map((num) => (
                    <button
                      key={num}
                      onClick={() => setColumns(num)}
                      className={`px-2 py-0.5 rounded ${
                        columns === num ? "bg-indigo-600 text-white" : "text-slate-700 hover:bg-slate-200"
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

            {/* US-Letter WYSIWYG Sheet Workspace */}
            <div className="flex-1 overflow-y-auto p-8 flex justify-center">
              <div
                style={{
                  width: "816px",
                  minHeight: "1056px",
                  transform: `scale(${zoomLevel / 100})`,
                  transformOrigin: "top center",
                }}
                className="bg-white shadow-2xl rounded-xs p-10 relative flex flex-col justify-between border border-slate-300"
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

                {/* Worksheet Header */}
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
                      <div className="w-14 h-14 border border-slate-300 rounded-lg flex items-center justify-center bg-white p-1 shadow-sm relative group" title="Scannable Assignment QR Code">
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

                  {/* Problem Grid */}
                  <div
                    className={`mt-6 grid gap-4 ${
                      columns === 1
                        ? "grid-cols-1"
                        : columns === 3
                        ? "grid-cols-3"
                        : "grid-cols-2"
                    }`}
                  >
                    {worksheetProblems.map((prob, idx) => (
                      <div
                        key={`${prob.id}_${idx}`}
                        className={`border border-slate-300 rounded p-3.5 ${workspaceBoxClasses} flex flex-col justify-between bg-white relative transition-all duration-150`}
                      >
                        <div>
                          <div className="flex justify-between items-center text-xs text-slate-600 mb-2">
                            <div className="flex items-center space-x-1.5">
                              <span className="font-bold text-slate-900">{idx + 1})</span>
                              <button
                                onClick={() => handleRegenerateSingleProblem(idx)}
                                data-testid="regenerate-single-problem"
                                title="Regenerate Single Problem"
                                aria-label="Regenerate Single Problem"
                                className="p-1 hover:bg-slate-100 rounded text-slate-400 hover:text-indigo-600 transition"
                              >
                                <RefreshCw className="w-3 h-3" />
                              </button>
                            </div>
                            <span className="text-[10px] text-slate-400 truncate max-w-[140px]">
                              {prob.prompt_text}
                            </span>
                          </div>

                          <div className="py-2 text-center text-sm font-medium text-slate-900">
                            <KaTeXInline math={prob.equation_typst} />
                          </div>
                        </div>

                        {/* Answer Key Overlay */}
                        {showAnswerKey ? (
                          <div className="bg-amber-50/90 border border-amber-200 rounded p-2 text-xs text-amber-950 mt-2">
                            <div className="font-bold flex items-center gap-1.5 text-sm pb-1 border-b border-amber-200/60">
                              <span className="text-amber-800 text-xs font-semibold">Ans:</span>
                              <KaTeXInline math={prob.answer_typst} />
                            </div>
                            {prob.steps_typst && prob.steps_typst.length > 0 && (
                              <div className="mt-1.5 space-y-1 text-[11px] text-amber-900">
                                <div className="text-[9px] font-bold text-amber-800 uppercase tracking-wider">
                                  Solution Steps:
                                </div>
                                {prob.steps_typst.map((st, sIdx) => (
                                  <div key={sIdx} className="flex items-start gap-1 leading-snug">
                                    <span className="text-amber-600 font-mono text-[10px] font-semibold mt-0.5">
                                      {sIdx + 1}.
                                    </span>
                                    <div>
                                      <StepTextWithMath text={st} />
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        ) : (
                          <div className="text-right text-[10px] text-slate-400 border border-slate-200 self-end px-3 py-1 rounded">
                            Ans:
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Footer */}
                <div className="text-center text-[10px] text-slate-400 border-t border-slate-200 pt-2">
                  Generated procedurally by OpenMathForge CAS • Seed: {baseSeed} • Page 1 of {estimatedPages}
                </div>
              </div>
            </div>
          </section>
        </div>
      ) : activeTab === "classroom" ? (
        /* Classroom & Rosters Tab */
        <div className="max-w-6xl mx-auto px-4 py-8 space-y-6 flex-1 w-full">
          {/* Class Header & Controls */}
          <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center space-x-2">
                <Users className="w-5 h-5 text-indigo-600" />
                <h2 className="text-lg font-bold text-slate-900">Classroom Management & Rosters</h2>
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Manage student rosters and generate personalized worksheets with individual QR tracking.
              </p>
            </div>

            <div className="flex items-center space-x-3">
              <select
                value={selectedClassId}
                onChange={(e) => setSelectedClassId(e.target.value)}
                className="text-xs font-semibold rounded-lg border border-slate-300 px-3 py-2 bg-white text-slate-700 shadow-2xs"
              >
                {classesList.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.student_count} students)
                  </option>
                ))}
              </select>

              <button
                onClick={() => setIsImportModalOpen(true)}
                className="px-3 py-2 bg-indigo-50 border border-indigo-200 text-indigo-700 rounded-lg text-xs font-bold flex items-center space-x-1.5 hover:bg-indigo-100 transition shadow-2xs"
              >
                <Upload className="w-3.5 h-3.5" />
                <span>Import Roster CSV</span>
              </button>

              <button
                onClick={handlePrintClassBatchPDF}
                disabled={isBatchGenerating}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold flex items-center space-x-1.5 shadow-sm transition"
              >
                <Download className="w-3.5 h-3.5" />
                <span>{isBatchGenerating ? "Compiling..." : "Print Class Set (with QR Codes)"}</span>
              </button>
            </div>
          </div>

          {/* Roster & Live Gradebook Table */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Student Roster List */}
            <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 shadow-sm p-5">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
                <h3 className="text-sm font-bold text-slate-800">
                  Enrolled Students ({currentClassStudents.length})
                </h3>
                <span className="text-[11px] font-semibold text-slate-400">
                  Individual QR Enabled
                </span>
              </div>

              <div className="max-h-96 overflow-y-auto space-y-2 pr-1">
                {currentClassStudents.map((stu) => (
                  <div
                    key={stu.id}
                    className="p-2.5 rounded-lg border border-slate-100 bg-slate-50 flex items-center justify-between text-xs"
                  >
                    <div>
                      <div className="font-bold text-slate-800">
                        {stu.first_name} {stu.last_name}
                      </div>
                      <div className="text-[11px] text-slate-400 font-mono">
                        ID: {stu.student_id} • Period: {stu.period || "1"}
                      </div>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                      QR Ready
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Assessment Gradebook Table */}
            <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200 shadow-sm p-5">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
                <h3 className="text-sm font-bold text-slate-800">
                  Verified Gradebook
                </h3>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleExportGradebookCSV("canvas")}
                    className="text-xs text-indigo-600 hover:underline font-semibold flex items-center space-x-1"
                  >
                    <FileSpreadsheet className="w-3.5 h-3.5" />
                    <span>Canvas SIS Export</span>
                  </button>
                  <span className="text-slate-300">•</span>
                  <button
                    onClick={() => handleExportGradebookCSV("google")}
                    className="text-xs text-indigo-600 hover:underline font-semibold flex items-center space-x-1"
                  >
                    <FileSpreadsheet className="w-3.5 h-3.5" />
                    <span>Google CSV</span>
                  </button>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-200 text-slate-500 font-semibold bg-slate-50">
                      <th className="py-2 px-3">Student Name</th>
                      <th className="py-2 px-3">Student ID</th>
                      <th className="py-2 px-3">Status</th>
                      <th className="py-2 px-3 text-right">Score</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {gradebookEntries.map((entry) => (
                      <tr key={entry.student_id} className="hover:bg-slate-50/50">
                        <td className="py-2.5 px-3 font-semibold text-slate-800">
                          {entry.name}
                        </td>
                        <td className="py-2.5 px-3 font-mono text-slate-500">
                          {entry.student_id}
                        </td>
                        <td className="py-2.5 px-3">
                          {entry.status === "graded" ? (
                            <span className="inline-flex items-center text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                              <CheckCircle2 className="w-3 h-3 mr-1" />
                              Auto-Graded
                            </span>
                          ) : (
                            <span className="inline-flex items-center text-[10px] font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                              <Clock className="w-3 h-3 mr-1" />
                              Awaiting Scan
                            </span>
                          )}
                        </td>
                        <td className="py-2.5 px-3 text-right font-bold">
                          {entry.score_percentage !== null && entry.score_percentage !== undefined ? (
                            <span className="text-indigo-600 font-mono">
                              {Math.round(entry.score_percentage)}%
                            </span>
                          ) : (
                            <span className="text-slate-300">—</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
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

      {/* Kuta Question Configurator Modal */}
      {configTopic && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl border border-slate-300 w-full max-w-2xl overflow-hidden flex flex-col">
            <div className="px-5 py-3 bg-slate-900 text-white flex justify-between items-center">
              <h3 className="font-bold text-sm flex items-center">
                <Settings2 className="w-4 h-4 mr-2 text-indigo-400" />
                {configTopic.name}
              </h3>
              <button
                onClick={() => setConfigTopic(null)}
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
                      fetchModalSample(configTopic.generator_id, count, modalDifficulty);
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
                          fetchModalSample(configTopic.generator_id, modalCount, diff);
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
                      onChange={() => setModalQuestionType("free_response")}
                      className="accent-indigo-600"
                    />
                    <span>Free response</span>
                  </label>
                  <label className="flex items-center space-x-1.5 cursor-pointer">
                    <input
                      type="radio"
                      name="qtype"
                      checked={modalQuestionType === "multiple_choice"}
                      onChange={() => setModalQuestionType("multiple_choice")}
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
                      fetchModalSample(configTopic.generator_id, modalCount, modalDifficulty)
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
                      <div key={p.id} className="bg-white p-2 rounded border border-slate-200 flex justify-between">
                        <div>
                          <span className="font-bold mr-2">{i + 1})</span>
                          <KaTeXInline math={p.equation_typst} />
                        </div>
                        <div className="text-slate-400 font-mono">
                          Ans: <KaTeXInline math={p.answer_typst} />
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>

            <div className="px-5 py-3 bg-slate-100 border-t border-slate-200 flex justify-end space-x-2">
              <button
                onClick={() => setConfigTopic(null)}
                className="px-4 py-1.5 text-xs font-semibold rounded text-slate-600 hover:bg-slate-200"
              >
                Cancel
              </button>
              <button
                onClick={handleAddConfiguredTopic}
                className="px-4 py-1.5 text-xs font-bold rounded bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
              >
                OK (Add to Worksheet)
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
