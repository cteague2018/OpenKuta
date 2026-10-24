export interface Topic {
  id: string;
  name: string;
  generator_id: string;
  available: boolean;
}

export interface Category {
  name: string;
  topics: Topic[];
}

export interface Course {
  title: string;
  description: string;
  categories: Category[];
}

export interface Problem {
  id: string;
  prompt_text: string;
  equation_typst: string;
  answer_typst: string;
  steps_typst: string[];
  distractors: string[];
  difficulty: "mild" | "medium" | "spicy";
  standards: string[];
}

export const DEFAULT_COURSE_CATALOG: Record<string, Course> = {
  algebra_1: {
    title: "Infinite Algebra 1",
    description: "Over 90 topics covering foundational algebra, linear equations, systems, polynomials, and quadratics.",
    categories: [
      {
        name: "Equations",
        topics: [
          { id: "algebra_1.two_step", name: "Two-Step Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "algebra_1.multi_step", name: "Multi-Step Equations", generator_id: "algebra_1.multi_step", available: true },
          { id: "algebra_1.proportions", name: "Solving Proportions", generator_id: "algebra_1.two_step", available: true },
          { id: "algebra_1.abs_value_eq", name: "Absolute Value Equations", generator_id: "algebra_1.two_step", available: false },
        ],
      },
      {
        name: "Linear Equations and Inequalities",
        topics: [
          { id: "algebra_1.slope_points", name: "Slope from Two Points", generator_id: "algebra_1.linear_equations", available: true },
          { id: "algebra_1.slope_intercept", name: "Writing Slope-Intercept Form", generator_id: "algebra_1.linear_equations", available: true },
          { id: "algebra_1.standard_form", name: "Standard to Slope-Intercept Form", generator_id: "algebra_1.linear_equations", available: true },
          { id: "algebra_1.graphing_linear", name: "Graphing Linear Equations", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Systems of Equations",
        topics: [
          { id: "algebra_1.sys_elim", name: "Solving Systems by Elimination", generator_id: "algebra_1.systems", available: true },
          { id: "algebra_1.sys_sub", name: "Solving Systems by Substitution", generator_id: "algebra_1.systems", available: true },
        ],
      },
      {
        name: "Polynomials & Factoring",
        topics: [
          { id: "algebra_1.factoring_monic", name: "Factoring Trinomials (a = 1)", generator_id: "algebra_1.factoring", available: true },
          { id: "algebra_1.factoring_nonmonic", name: "Factoring Trinomials (a > 1)", generator_id: "algebra_1.factoring", available: true },
          { id: "algebra_1.diff_squares", name: "Difference of Two Squares", generator_id: "algebra_1.factoring", available: true },
        ],
      },
      {
        name: "Quadratic Equations",
        topics: [
          { id: "algebra_1.quad_factor", name: "Solving Quadratics by Factoring", generator_id: "algebra_1.quadratics", available: true },
          { id: "algebra_1.quad_cts", name: "Completing the Square", generator_id: "algebra_1.quadratics", available: true },
          { id: "algebra_1.quad_formula", name: "Quadratic Formula", generator_id: "algebra_1.quadratics", available: true },
        ],
      },
    ],
  },
  geometry: {
    title: "Infinite Geometry",
    description: "Right triangles, circles, coordinate geometry, transformations, and area/volume.",
    categories: [
      {
        name: "Right Triangles & Trigonometry",
        topics: [
          { id: "geometry.pythagorean", name: "The Pythagorean Theorem", generator_id: "geometry.pythagorean", available: true },
          { id: "geometry.special_right", name: "Special Right Triangles (45-45-90 & 30-60-90)", generator_id: "geometry.pythagorean", available: true },
        ],
      },
    ],
  },
  pre_algebra: {
    title: "Infinite Pre-Algebra",
    description: "Fractions, integers, decimals, simple one/two step equations, and percents.",
    categories: [
      {
        name: "Linear Relations",
        topics: [
          { id: "prealg.two_step", name: "Two-Step Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.slope", name: "Finding Slope", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
    ],
  },
  algebra_2: {
    title: "Infinite Algebra 2",
    description: "Complex numbers, rational exponents, polynomial division, logarithms, and quadratics.",
    categories: [
      {
        name: "Quadratic Functions",
        topics: [
          { id: "alg2.quadratics", name: "Quadratics with Complex Roots", generator_id: "algebra_1.quadratics", available: true },
          { id: "alg2.factoring", name: "Advanced Factoring", generator_id: "algebra_1.factoring", available: true },
        ],
      },
    ],
  },
  precalculus: {
    title: "Infinite Precalculus",
    description: "Trigonometric identities, vectors, matrices, sequences and series.",
    categories: [
      {
        name: "Linear Algebra & Systems",
        topics: [
          { id: "precalc.systems", name: "Multivariable Systems", generator_id: "algebra_1.systems", available: true },
        ],
      },
    ],
  },
  calculus: {
    title: "Infinite Calculus",
    description: "Limits, derivatives, product/quotient/chain rules, and integration.",
    categories: [
      {
        name: "Differentiation & Integration",
        topics: [
          { id: "calc.power_rule", name: "Power Rule Derivatives", generator_id: "algebra_1.two_step", available: false },
        ],
      },
    ],
  },
  grade_6: {
    title: "Grade 6 Math",
    description: "Ratios, unit rates, pre-algebra expressions, and basic coordinate graphing.",
    categories: [
      {
        name: "Ratios & Expressions",
        topics: [
          { id: "g6.expressions", name: "Evaluating Algebraic Expressions", generator_id: "algebra_1.two_step", available: true },
        ],
      },
    ],
  },
};

export const DEFAULT_SAMPLE_PROBLEMS: Problem[] = [
  {
    id: "demo_1",
    prompt_text: "Solve for x:",
    equation_typst: "$4 x + 7 = 31$",
    answer_typst: "$x = 6$",
    steps_typst: ["4 x + 7 = 31", "4 x = 24", "x = 6"],
    distractors: ["$x = 7$", "$x = 5$", "$x = -6$"],
    difficulty: "mild",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_2",
    prompt_text: "Solve for x:",
    equation_typst: "$-3 x - 8 = 13$",
    answer_typst: "$x = -7$",
    steps_typst: ["-3 x - 8 = 13", "-3 x = 21", "x = -7"],
    distractors: ["$x = 7$", "$x = -5$", "$x = -8$"],
    difficulty: "mild",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_3",
    prompt_text: "Solve for x:",
    equation_typst: "$5 (x - 2) = 25$",
    answer_typst: "$x = 7$",
    steps_typst: ["5 (x - 2) = 25", "5 x - 10 = 25", "5 x = 35", "x = 7"],
    distractors: ["$x = 5$", "$x = 3$", "$x = -7$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_4",
    prompt_text: "Solve for x:",
    equation_typst: "$2 x / 3 + 4 = 10$",
    answer_typst: "$x = 9$",
    steps_typst: ["2 x / 3 + 4 = 10", "2 x / 3 = 6", "2 x = 18", "x = 9"],
    distractors: ["$x = 6$", "$x = 12$", "$x = -9$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_5",
    prompt_text: "Solve by factoring:",
    equation_typst: "$x^2 - 5 x + 6 = 0$",
    answer_typst: "$x = 2, 3$",
    steps_typst: ["x^2 - 5 x + 6 = 0", "(x - 2)(x - 3) = 0", "x = 2, 3"],
    distractors: ["$x = -2, -3$", "$x = 1, 6$", "$x = -1, -6$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.4.B"],
  },
  {
    id: "demo_6",
    prompt_text: "Solve by factoring:",
    equation_typst: "$x^2 + 7 x + 12 = 0$",
    answer_typst: "$x = -3, -4$",
    steps_typst: ["x^2 + 7 x + 12 = 0", "(x + 3)(x + 4) = 0", "x = -3, -4"],
    distractors: ["$x = 3, 4$", "$x = -2, -6$", "$x = 2, 6$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.4.B"],
  },
  {
    id: "demo_7",
    prompt_text: "Solve by factoring:",
    equation_typst: "$2 x^2 - 7 x + 3 = 0$",
    answer_typst: "$x = 1/2, 3$",
    steps_typst: ["2 x^2 - 7 x + 3 = 0", "(2 x - 1)(x - 3) = 0", "x = 1/2, 3"],
    distractors: ["$x = -1/2, -3$", "$x = 1, 3/2$", "$x = 2, 3$"],
    difficulty: "spicy",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.4.B"],
  },
  {
    id: "demo_8",
    prompt_text: "Solve using the quadratic formula:",
    equation_typst: "$x^2 - 4 x - 5 = 0$",
    answer_typst: "$x = 5, -1$",
    steps_typst: ["x = (4 +- sqrt(16 - 4(1)(-5))) / 2", "x = (4 +- sqrt(36)) / 2", "x = (4 +- 6) / 2", "x = 5, -1"],
    distractors: ["$x = -5, 1$", "$x = 4, -5$", "$x = 2 +- sqrt(5)$"],
    difficulty: "spicy",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.4.B"],
  },
];

export const DEFAULT_CLASSROOMS = [
  {
    id: "cls_alg1_p3",
    name: "Algebra 1 - Honors",
    subject: "Algebra 1",
    period: "Period 3",
    teacher_name: "C. Teague",
    student_count: 5,
    students: [
      { id: "st_1", student_id: "STU-1001", first_name: "Lucas", last_name: "Alvarez", email: "l.alvarez@school.edu", period: "Period 3" },
      { id: "st_2", student_id: "STU-1002", first_name: "Maya", last_name: "Chen", email: "m.chen@school.edu", period: "Period 3" },
      { id: "st_3", student_id: "STU-1003", first_name: "Jordan", last_name: "Smith", email: "j.smith@school.edu", period: "Period 3" },
      { id: "st_4", student_id: "STU-1004", first_name: "Emma", last_name: "Davis", email: "e.davis@school.edu", period: "Period 3" },
      { id: "st_5", student_id: "STU-1005", first_name: "Noah", last_name: "Patel", email: "n.patel@school.edu", period: "Period 3" },
    ],
    gradebook: [
      { student_id: "STU-1001", name: "Lucas Alvarez", email: "l.alvarez@school.edu", status: "graded", score_percentage: 100, correct_count: 8, total_problems: 8, error_types: [], submitted_at: "2026-10-24 10:14 AM" },
      { student_id: "STU-1002", name: "Maya Chen", email: "m.chen@school.edu", status: "graded", score_percentage: 87.5, correct_count: 7, total_problems: 8, error_types: ["sign_error"], submitted_at: "2026-10-24 10:18 AM" },
      { student_id: "STU-1003", name: "Jordan Smith", email: "j.smith@school.edu", status: "graded", score_percentage: 75.0, correct_count: 6, total_problems: 8, error_types: ["distribution_error", "arithmetic_error"], submitted_at: "2026-10-24 10:22 AM" },
      { student_id: "STU-1004", name: "Emma Davis", email: "e.davis@school.edu", status: "pending", score_percentage: undefined, correct_count: undefined, total_problems: 8, error_types: [], submitted_at: undefined },
      { student_id: "STU-1005", name: "Noah Patel", email: "n.patel@school.edu", status: "pending", score_percentage: undefined, correct_count: undefined, total_problems: 8, error_types: [], submitted_at: undefined },
    ],
  },
  {
    id: "cls_geom_p5",
    name: "Geometry - Academic",
    subject: "Geometry",
    period: "Period 5",
    teacher_name: "C. Teague",
    student_count: 4,
    students: [
      { id: "st_6", student_id: "STU-2001", first_name: "Ethan", last_name: "Johnson", email: "e.johnson@school.edu", period: "Period 5" },
      { id: "st_7", student_id: "STU-2002", first_name: "Sophia", last_name: "Martinez", email: "s.martinez@school.edu", period: "Period 5" },
      { id: "st_8", student_id: "STU-2003", first_name: "Liam", last_name: "Williams", email: "l.williams@school.edu", period: "Period 5" },
      { id: "st_9", student_id: "STU-2004", first_name: "Olivia", last_name: "Brown", email: "o.brown@school.edu", period: "Period 5" },
    ],
    gradebook: [
      { student_id: "STU-2001", name: "Ethan Johnson", email: "e.johnson@school.edu", status: "graded", score_percentage: 100, correct_count: 6, total_problems: 6, error_types: [], submitted_at: "2026-10-24 11:05 AM" },
      { student_id: "STU-2002", name: "Sophia Martinez", email: "s.martinez@school.edu", status: "graded", score_percentage: 83.3, correct_count: 5, total_problems: 6, error_types: ["arithmetic_error"], submitted_at: "2026-10-24 11:12 AM" },
      { student_id: "STU-2003", name: "Liam Williams", email: "l.williams@school.edu", status: "pending", score_percentage: undefined, correct_count: undefined, total_problems: 6, error_types: [], submitted_at: undefined },
      { student_id: "STU-2004", name: "Olivia Brown", email: "o.brown@school.edu", status: "pending", score_percentage: undefined, correct_count: undefined, total_problems: 6, error_types: [], submitted_at: undefined },
    ],
  },
];

