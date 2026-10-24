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
    description: "Foundational algebra, linear equations, inequalities, systems, polynomials, factoring, and quadratics.",
    categories: [
      {
        name: "Foundations & Expressions",
        topics: [
          { id: "a1.verbal_expr", name: "Verbal Expressions to Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "a1.order_of_ops", name: "Order of Operations", generator_id: "algebra_1.two_step", available: true },
          { id: "a1.evaluating_expr", name: "Evaluating Algebraic Expressions", generator_id: "algebra_1.two_step", available: true },
          { id: "a1.distributive", name: "The Distributive Property", generator_id: "algebra_1.multi_step", available: true },
        ],
      },
      {
        name: "Linear Equations",
        topics: [
          { id: "algebra_1.two_step", name: "Two-Step Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "algebra_1.multi_step", name: "Multi-Step Equations", generator_id: "algebra_1.multi_step", available: true },
          { id: "a1.vars_both_sides", name: "Equations with Variables on Both Sides", generator_id: "algebra_1.multi_step", available: true },
          { id: "algebra_1.proportions", name: "Solving Proportions", generator_id: "algebra_1.two_step", available: true },
          { id: "a1.literal_eq", name: "Literal Equations and Formulas", generator_id: "algebra_1.two_step", available: true },
          { id: "algebra_1.abs_value_eq", name: "Absolute Value Equations", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "Linear Inequalities",
        topics: [
          { id: "a1.graph_ineq", name: "Graphing Single-Variable Inequalities", generator_id: "algebra_1.two_step", available: true },
          { id: "a1.two_step_ineq", name: "Two-Step Linear Inequalities", generator_id: "algebra_1.two_step", available: true },
          { id: "a1.multi_step_ineq", name: "Multi-Step Inequalities", generator_id: "algebra_1.multi_step", available: true },
          { id: "a1.compound_ineq", name: "Compound Inequalities (And / Or)", generator_id: "algebra_1.multi_step", available: true },
        ],
      },
      {
        name: "Slope & Graphing Lines",
        topics: [
          { id: "algebra_1.slope_points", name: "Slope from Two Points", generator_id: "algebra_1.linear_equations", available: true },
          { id: "algebra_1.slope_intercept", name: "Writing Slope-Intercept Form", generator_id: "algebra_1.linear_equations", available: true },
          { id: "algebra_1.standard_form", name: "Standard to Slope-Intercept Form", generator_id: "algebra_1.linear_equations", available: true },
          { id: "a1.point_slope", name: "Point-Slope Form", generator_id: "algebra_1.linear_equations", available: true },
          { id: "algebra_1.graphing_linear", name: "Graphing Linear Equations", generator_id: "algebra_1.linear_equations", available: true },
          { id: "a1.parallel_perp", name: "Equations of Parallel and Perpendicular Lines", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Systems of Equations",
        topics: [
          { id: "algebra_1.sys_elim", name: "Solving Systems by Elimination", generator_id: "algebra_1.systems", available: true },
          { id: "algebra_1.sys_sub", name: "Solving Systems by Substitution", generator_id: "algebra_1.systems", available: true },
          { id: "a1.sys_graphing", name: "Solving Systems by Graphing", generator_id: "algebra_1.systems", available: true },
          { id: "a1.sys_ineq", name: "Systems of Linear Inequalities", generator_id: "algebra_1.systems", available: true },
        ],
      },
      {
        name: "Polynomials & Factoring",
        topics: [
          { id: "a1.poly_add_sub", name: "Adding and Subtracting Polynomials", generator_id: "algebra_1.factoring", available: true },
          { id: "a1.poly_multiply", name: "Multiplying Monomials and Polynomials", generator_id: "algebra_1.factoring", available: true },
          { id: "a1.binomial_foil", name: "Multiplying Binomials (FOIL)", generator_id: "algebra_1.factoring", available: true },
          { id: "a1.factoring_gcf", name: "Factoring by Greatest Common Factor", generator_id: "algebra_1.factoring", available: true },
          { id: "algebra_1.factoring_monic", name: "Factoring Trinomials (a = 1)", generator_id: "algebra_1.factoring", available: true },
          { id: "algebra_1.factoring_nonmonic", name: "Factoring Trinomials (a > 1)", generator_id: "algebra_1.factoring", available: true },
          { id: "algebra_1.diff_squares", name: "Difference of Two Squares", generator_id: "algebra_1.factoring", available: true },
          { id: "a1.grouping", name: "Factoring by Grouping", generator_id: "algebra_1.factoring", available: true },
        ],
      },
      {
        name: "Quadratic Equations",
        topics: [
          { id: "algebra_1.quad_factor", name: "Solving Quadratics by Factoring", generator_id: "algebra_1.quadratics", available: true },
          { id: "a1.quad_square_roots", name: "Solving Quadratics by Square Roots", generator_id: "algebra_1.quadratics", available: true },
          { id: "algebra_1.quad_cts", name: "Completing the Square", generator_id: "algebra_1.quadratics", available: true },
          { id: "algebra_1.quad_formula", name: "The Quadratic Formula", generator_id: "algebra_1.quadratics", available: true },
          { id: "a1.discriminant", name: "The Discriminant and Nature of Roots", generator_id: "algebra_1.quadratics", available: true },
        ],
      },
    ],
  },

  geometry: {
    title: "Infinite Geometry",
    description: "Lines, angles, triangles, right triangle trigonometry, quadrilaterals, circles, transformations, area and volume.",
    categories: [
      {
        name: "Basics of Geometry",
        topics: [
          { id: "geom.points_lines", name: "Points, Lines, and Planes", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.seg_addition", name: "The Segment Addition Postulate", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.midpoint_dist", name: "Midpoint and Distance Formulas", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.angle_measure", name: "Angle Classification and Measure", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.angle_addition", name: "The Angle Addition Postulate", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.comp_supp", name: "Complementary and Supplementary Angles", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.vertical_angles", name: "Vertical Angles and Linear Pairs", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Parallel & Perpendicular Lines",
        topics: [
          { id: "geom.parallel_transversals", name: "Parallel Lines Cut by a Transversal", generator_id: "algebra_1.linear_equations", available: true },
          { id: "geom.alternate_angles", name: "Alternate Interior & Exterior Angles", generator_id: "algebra_1.linear_equations", available: true },
          { id: "geom.consecutive_angles", name: "Consecutive Interior Angles", generator_id: "algebra_1.linear_equations", available: true },
          { id: "geom.parallel_slopes", name: "Slopes of Parallel and Perpendicular Lines", generator_id: "algebra_1.linear_equations", available: true },
          { id: "geom.parallel_eqs", name: "Equations of Parallel and Perpendicular Lines", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Triangles & Congruence",
        topics: [
          { id: "geom.classify_triangles", name: "Classifying Triangles (Sides & Angles)", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.triangle_angle_sum", name: "The Triangle Angle Sum Theorem", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.exterior_angles", name: "The Exterior Angle Theorem", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.congruence_sss_sas", name: "SSS and SAS Triangle Congruence", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.congruence_asa_aas", name: "ASA and AAS Triangle Congruence", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.congruence_hl", name: "Hypotenuse-Leg (HL) Congruence", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.isosceles_equilateral", name: "Isosceles and Equilateral Triangles", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.midsegment", name: "The Triangle Midsegment Theorem", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Right Triangles & Trigonometry",
        topics: [
          { id: "geometry.pythagorean", name: "The Pythagorean Theorem", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.pythagorean_converse", name: "Converse of the Pythagorean Theorem", generator_id: "geometry.pythagorean", available: true },
          { id: "geometry.special_right", name: "Special Right Triangles (45-45-90 & 30-60-90)", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.trig_ratios", name: "Trigonometric Ratios (Sine, Cosine, Tangent)", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.inverse_trig", name: "Inverse Trigonometric Ratios & Angles", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.solving_right_triangles", name: "Solving Right Triangles", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.elevation_depression", name: "Angles of Elevation and Depression", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Quadrilaterals & Polygons",
        topics: [
          { id: "geom.polygon_angle_sums", name: "Angles of Polygons (Interior & Exterior)", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.parallelograms", name: "Properties of Parallelograms", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.special_parallelograms", name: "Rectangles, Rhombi, and Squares", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.trapezoids_kites", name: "Properties of Trapezoids and Kites", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Similarity",
        topics: [
          { id: "geom.ratios_proportions", name: "Ratios and Proportions in Geometry", generator_id: "algebra_1.two_step", available: true },
          { id: "geom.similar_polygons", name: "Similar Polygons and Scale Factors", generator_id: "algebra_1.two_step", available: true },
          { id: "geom.similar_triangles_aa", name: "Triangle Similarity (AA, SAS, SSS)", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.proportionality", name: "Triangle Proportionality Theorem", generator_id: "algebra_1.two_step", available: true },
          { id: "geom.right_triangle_similarity", name: "Similarity in Right Triangles (Geometric Mean)", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Transformations",
        topics: [
          { id: "geom.translations", name: "Translations on the Coordinate Plane", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.reflections", name: "Reflections across Axes and Lines", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.rotations", name: "Rotations about the Origin (90, 180, 270)", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.dilations", name: "Dilations and Scale Factors", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Circles",
        topics: [
          { id: "geom.tangents", name: "Tangents to Circles", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.arcs_central_angles", name: "Arcs and Central Angles", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.arc_length_sector", name: "Arc Length and Sector Area", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.inscribed_angles", name: "Inscribed Angles and Polygons", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.segment_lengths", name: "Chord, Secant, and Tangent Segments", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.circle_equations", name: "Equations of Circles in Standard Form", generator_id: "algebra_1.quadratics", available: true },
        ],
      },
      {
        name: "Surface Area & Volume",
        topics: [
          { id: "geom.sa_prisms_cylinders", name: "Surface Area of Prisms and Cylinders", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.sa_pyramids_cones", name: "Surface Area of Pyramids and Cones", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.vol_prisms_cylinders", name: "Volume of Prisms and Cylinders", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.vol_pyramids_cones", name: "Volume of Pyramids and Cones", generator_id: "geometry.pythagorean", available: true },
          { id: "geom.spheres", name: "Surface Area and Volume of Spheres", generator_id: "geometry.pythagorean", available: true },
        ],
      },
    ],
  },

  grade_6: {
    title: "Grade 6 Math",
    description: "Ratios, unit rates, negative integers, expressions, one-step equations, area, and statistics.",
    categories: [
      {
        name: "Ratios & Rates",
        topics: [
          { id: "g6.ratios", name: "Understanding Ratios and Equivalent Ratios", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.unit_rates", name: "Unit Rates and Price Comparisons", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.ratio_tables", name: "Ratio Tables and Graphing Ratios", generator_id: "algebra_1.linear_equations", available: true },
          { id: "g6.convert_units", name: "Converting Measurement Units", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.percents", name: "Percents and Percent of a Quantity", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "The Number System",
        topics: [
          { id: "g6.divide_fractions", name: "Dividing Fractions by Fractions", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.decimal_ops", name: "Multi-Digit Decimal Operations (+, -, *, /)", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.gcf_lcm", name: "Greatest Common Factor (GCF) and LCM", generator_id: "algebra_1.factoring", available: true },
          { id: "g6.integers_number_line", name: "Positive and Negative Numbers on Number Line", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.absolute_value", name: "Absolute Value and Comparing Integers", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.coordinate_plane", name: "The Four-Quadrant Coordinate Plane", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Expressions & Variables",
        topics: [
          { id: "g6.exponents", name: "Evaluating Numerical Expressions with Exponents", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.order_of_operations", name: "Order of Operations with Parentheses", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.expressions", name: "Evaluating Algebraic Expressions", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.writing_expressions", name: "Writing Expressions from Word Phrases", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.distributive", name: "Distributive Property with Variables", generator_id: "algebra_1.multi_step", available: true },
          { id: "g6.combine_like_terms", name: "Combining Like Terms to Form Equivalent Expressions", generator_id: "algebra_1.multi_step", available: true },
        ],
      },
      {
        name: "Equations & Inequalities",
        topics: [
          { id: "g6.one_step_add_sub", name: "One-Step Addition and Subtraction Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.one_step_mult_div", name: "One-Step Multiplication and Division Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.equations_decimals", name: "Solving Equations with Decimals and Fractions", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.graph_inequalities", name: "Writing and Graphing Single-Variable Inequalities", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.independent_dependent", name: "Independent and Dependent Variables in Tables & Graphs", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Geometry & Area",
        topics: [
          { id: "g6.area_parallelograms", name: "Area of Parallelograms", generator_id: "geometry.pythagorean", available: true },
          { id: "g6.area_triangles", name: "Area of Triangles and Right Triangles", generator_id: "geometry.pythagorean", available: true },
          { id: "g6.area_trapezoids", name: "Area of Trapezoids and Composite Figures", generator_id: "geometry.pythagorean", available: true },
          { id: "g6.volume_prisms", name: "Volume of Rectangular Prisms with Fractional Lengths", generator_id: "geometry.pythagorean", available: true },
          { id: "g6.nets_surface_area", name: "Surface Area from Nets of Prisms and Pyramids", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Statistics & Distributions",
        topics: [
          { id: "g6.mean_median_mode", name: "Measures of Center: Mean, Median, and Mode", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.range_variability", name: "Range and Mean Absolute Deviation (MAD)", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.dot_plots", name: "Creating and Interpreting Dot Plots", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.histograms", name: "Histograms and Frequency Tables", generator_id: "algebra_1.two_step", available: true },
          { id: "g6.box_plots", name: "Box-and-Whisker Plots (Quartiles & IQR)", generator_id: "algebra_1.two_step", available: true },
        ],
      },
    ],
  },

  pre_algebra: {
    title: "Infinite Pre-Algebra",
    description: "Fractions, integers, decimals, one/two-step equations, proportions, percent change, slope, and plane figures.",
    categories: [
      {
        name: "Arithmetic & Number Theory",
        topics: [
          { id: "prealg.integers", name: "Operations with Positive and Negative Integers", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.fractions", name: "Fraction Operations and Mixed Numbers", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.decimals_sci", name: "Decimals and Scientific Notation", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.order_of_ops", name: "Order of Operations with Exponents", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "Equations & Inequalities",
        topics: [
          { id: "prealg.one_step", name: "One-Step Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.two_step", name: "Two-Step Equations", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.multi_step", name: "Multi-Step Equations with Distribution", generator_id: "algebra_1.multi_step", available: true },
          { id: "prealg.inequalities", name: "Graphing One- and Two-Step Inequalities", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "Ratios, Proportions & Percents",
        topics: [
          { id: "prealg.proportions", name: "Solving Proportions and Word Problems", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.percent_equation", name: "The Percent Proportion and Equation", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.percent_change", name: "Percent of Change, Markup, and Discount", generator_id: "algebra_1.two_step", available: true },
          { id: "prealg.simple_interest", name: "Simple Interest (I = Prt)", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "Linear Relations & Functions",
        topics: [
          { id: "prealg.coord_graphing", name: "Graphing Points on Coordinate Plane", generator_id: "algebra_1.linear_equations", available: true },
          { id: "prealg.slope", name: "Finding Slope from Tables, Graphs, and Points", generator_id: "algebra_1.linear_equations", available: true },
          { id: "prealg.slope_intercept", name: "Graphing in Slope-Intercept Form (y = mx + b)", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Geometry & Measurement",
        topics: [
          { id: "prealg.perimeter_area", name: "Perimeter and Area of Plane Figures", generator_id: "geometry.pythagorean", available: true },
          { id: "prealg.pythagorean", name: "The Pythagorean Theorem", generator_id: "geometry.pythagorean", available: true },
          { id: "prealg.surface_area", name: "Surface Area of Prisms and Cylinders", generator_id: "geometry.pythagorean", available: true },
          { id: "prealg.volume", name: "Volume of Prisms and Cylinders", generator_id: "geometry.pythagorean", available: true },
        ],
      },
    ],
  },

  algebra_2: {
    title: "Infinite Algebra 2",
    description: "Complex numbers, quadratics, polynomials, radical & rational exponents, exponential & logarithmic functions, and series.",
    categories: [
      {
        name: "Linear Systems & Matrices",
        topics: [
          { id: "alg2.sys_2var", name: "Systems of Two Linear Equations", generator_id: "algebra_1.systems", available: true },
          { id: "alg2.sys_3var", name: "Systems of Three Linear Equations", generator_id: "algebra_1.systems", available: true },
          { id: "alg2.matrices", name: "Matrix Operations (Addition, Scalar, Multiplication)", generator_id: "algebra_1.systems", available: true },
        ],
      },
      {
        name: "Quadratic Relations & Complex Numbers",
        topics: [
          { id: "alg2.complex_numbers", name: "Operations with Complex Numbers (i)", generator_id: "algebra_1.quadratics", available: true },
          { id: "alg2.quadratics", name: "Quadratics with Complex Roots", generator_id: "algebra_1.quadratics", available: true },
          { id: "alg2.vertex_form", name: "Vertex Form and Graphing Parabolas", generator_id: "algebra_1.quadratics", available: true },
          { id: "alg2.factoring", name: "Advanced Factoring (Trinomials, Grouping, Sum/Diff of Cubes)", generator_id: "algebra_1.factoring", available: true },
        ],
      },
      {
        name: "Polynomial Functions",
        topics: [
          { id: "alg2.synthetic_div", name: "Synthetic Division and Remainder Theorem", generator_id: "algebra_1.factoring", available: true },
          { id: "alg2.finding_roots", name: "Finding All Roots of Polynomial Functions", generator_id: "algebra_1.factoring", available: true },
          { id: "alg2.graphing_poly", name: "End Behavior and Turning Points of Polynomials", generator_id: "algebra_1.factoring", available: true },
        ],
      },
      {
        name: "Radicals & Rational Exponents",
        topics: [
          { id: "alg2.rational_exponents", name: "Simplifying nth Roots and Rational Exponents", generator_id: "algebra_1.quadratics", available: true },
          { id: "alg2.radical_equations", name: "Solving Radical Equations with Extraneous Solutions", generator_id: "algebra_1.multi_step", available: true },
          { id: "alg2.inverse_functions", name: "Function Compositions and Inverses", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Exponential & Logarithmic Functions",
        topics: [
          { id: "alg2.exp_growth_decay", name: "Graphing Exponential Growth and Decay", generator_id: "algebra_1.linear_equations", available: true },
          { id: "alg2.log_properties", name: "Properties of Logarithms (Product, Quotient, Power)", generator_id: "algebra_1.multi_step", available: true },
          { id: "alg2.solving_exp_log", name: "Solving Exponential and Logarithmic Equations", generator_id: "algebra_1.multi_step", available: true },
        ],
      },
      {
        name: "Rational Functions",
        topics: [
          { id: "alg2.rational_ops", name: "Simplifying, Multiplying, and Dividing Rational Expressions", generator_id: "algebra_1.factoring", available: true },
          { id: "alg2.complex_fractions", name: "Adding and Subtracting Complex Fractions", generator_id: "algebra_1.factoring", available: true },
          { id: "alg2.rational_equations", name: "Solving Rational Equations", generator_id: "algebra_1.multi_step", available: true },
        ],
      },
      {
        name: "Sequences & Series",
        topics: [
          { id: "alg2.arithmetic_seq", name: "Arithmetic Sequences and Partial Sums", generator_id: "algebra_1.two_step", available: true },
          { id: "alg2.geometric_seq", name: "Geometric Sequences and Infinite Geometric Series", generator_id: "algebra_1.two_step", available: true },
          { id: "alg2.binomial_theorem", name: "The Binomial Theorem & Pascal's Triangle", generator_id: "algebra_1.factoring", available: true },
        ],
      },
    ],
  },

  precalculus: {
    title: "Infinite Precalculus",
    description: "Trigonometric functions, analytic trigonometry, vectors, matrices, polar coordinates, and conic sections.",
    categories: [
      {
        name: "Functions & Graphs",
        topics: [
          { id: "precalc.transformations", name: "Transformations of Parent Functions", generator_id: "algebra_1.linear_equations", available: true },
          { id: "precalc.piecewise", name: "Piecewise-Defined Functions", generator_id: "algebra_1.linear_equations", available: true },
          { id: "precalc.compositions", name: "Composite and Inverse Functions", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Polynomial & Rational Functions",
        topics: [
          { id: "precalc.rational_asymptotes", name: "Vertical, Horizontal, and Slant Asymptotes", generator_id: "algebra_1.factoring", available: true },
          { id: "precalc.partial_fractions", name: "Partial Fraction Decomposition", generator_id: "algebra_1.systems", available: true },
        ],
      },
      {
        name: "Trigonometric Functions",
        topics: [
          { id: "precalc.unit_circle", name: "Radian Measure and Unit Circle Trigonometry", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.right_triangle_trig", name: "Right Triangle Trigonometry", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.trig_graphs", name: "Graphs of Sine, Cosine, and Tangent (Amplitude & Period)", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Analytic Trigonometry",
        topics: [
          { id: "precalc.trig_identities", name: "Verifying Fundamental Trigonometric Identities", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.sum_diff_formulas", name: "Sum and Difference Formulas", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.double_half_angle", name: "Double-Angle and Half-Angle Formulas", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.trig_equations", name: "Solving Trigonometric Equations", generator_id: "algebra_1.quadratics", available: true },
        ],
      },
      {
        name: "Law of Sines & Cosines",
        topics: [
          { id: "precalc.law_of_sines", name: "Law of Sines (Ambiguous Case SSA)", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.law_of_cosines", name: "Law of Cosines", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.heron_formula", name: "Area of Oblique Triangles (Heron's Formula)", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Polar Coordinates & Vectors",
        topics: [
          { id: "precalc.polar_conversion", name: "Polar and Rectangular Coordinate Conversion", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.vectors_2d", name: "Vector Component Form, Magnitude, and Direction", generator_id: "geometry.pythagorean", available: true },
          { id: "precalc.dot_product", name: "Dot Product and Angle Between Vectors", generator_id: "geometry.pythagorean", available: true },
        ],
      },
      {
        name: "Linear Algebra & Systems",
        topics: [
          { id: "precalc.systems", name: "Multivariable Systems and Gaussian Elimination", generator_id: "algebra_1.systems", available: true },
          { id: "precalc.matrix_inverses", name: "Matrix Inverses and Determinants", generator_id: "algebra_1.systems", available: true },
        ],
      },
    ],
  },

  calculus: {
    title: "Infinite Calculus",
    description: "Limits, continuity, differentiation rules, derivative applications, integration, and differential equations.",
    categories: [
      {
        name: "Limits & Continuity",
        topics: [
          { id: "calc.limits_eval", name: "Evaluating Limits Algebraically (Factoring & Conjugates)", generator_id: "algebra_1.factoring", available: true },
          { id: "calc.one_sided_limits", name: "One-Sided Limits and Infinite Limits", generator_id: "algebra_1.factoring", available: true },
          { id: "calc.limits_infinity", name: "Limits at Infinity and Horizontal Asymptotes", generator_id: "algebra_1.factoring", available: true },
          { id: "calc.continuity", name: "Continuity and the Intermediate Value Theorem", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "Differentiation: Fundamentals & Rules",
        topics: [
          { id: "calc.def_derivative", name: "Definition of the Derivative (Difference Quotient)", generator_id: "algebra_1.two_step", available: true },
          { id: "calc.power_rule", name: "Power Rule, Constant Multiple, and Sum Rules", generator_id: "algebra_1.two_step", available: true },
          { id: "calc.product_quotient", name: "The Product and Quotient Rules", generator_id: "algebra_1.factoring", available: true },
          { id: "calc.chain_rule", name: "The Chain Rule", generator_id: "algebra_1.two_step", available: true },
          { id: "calc.trig_derivatives", name: "Derivatives of Trigonometric Functions", generator_id: "geometry.pythagorean", available: true },
          { id: "calc.exp_log_derivatives", name: "Exponential and Logarithmic Derivatives", generator_id: "algebra_1.two_step", available: true },
          { id: "calc.implicit_diff", name: "Implicit Differentiation", generator_id: "algebra_1.linear_equations", available: true },
        ],
      },
      {
        name: "Applications of Derivatives",
        topics: [
          { id: "calc.tangent_lines", name: "Tangent and Normal Lines to Curves", generator_id: "algebra_1.linear_equations", available: true },
          { id: "calc.related_rates", name: "Related Rates of Change", generator_id: "geometry.pythagorean", available: true },
          { id: "calc.mvt_rolle", name: "Mean Value Theorem and Rolle's Theorem", generator_id: "algebra_1.quadratics", available: true },
          { id: "calc.extrema_first_deriv", name: "First Derivative Test (Increasing/Decreasing & Extrema)", generator_id: "algebra_1.quadratics", available: true },
          { id: "calc.concavity_second_deriv", name: "Second Derivative Test (Concavity & Inflection Points)", generator_id: "algebra_1.quadratics", available: true },
          { id: "calc.optimization", name: "Applied Optimization Problems", generator_id: "algebra_1.quadratics", available: true },
          { id: "calc.lhopital", name: "L'Hopital's Rule for Indeterminate Forms", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "Integration & Antiderivatives",
        topics: [
          { id: "calc.antiderivatives", name: "Indefinite Integrals and the Power Rule", generator_id: "algebra_1.two_step", available: true },
          { id: "calc.u_substitution", name: "Integration by U-Substitution", generator_id: "algebra_1.two_step", available: true },
          { id: "calc.riemann_sums", name: "Riemann Sums and Definite Integral Definition", generator_id: "algebra_1.two_step", available: true },
          { id: "calc.ftc", name: "The Fundamental Theorem of Calculus (Parts 1 & 2)", generator_id: "algebra_1.two_step", available: true },
        ],
      },
      {
        name: "Applications of Integrals",
        topics: [
          { id: "calc.area_between_curves", name: "Area Between Two Curves", generator_id: "algebra_1.quadratics", available: true },
          { id: "calc.vol_disks_washers", name: "Volumes of Solids of Revolution: Disks and Washers", generator_id: "algebra_1.quadratics", available: true },
          { id: "calc.vol_cylindrical_shells", name: "Volumes of Solids of Revolution: Cylindrical Shells", generator_id: "algebra_1.quadratics", available: true },
          { id: "calc.differential_equations", name: "Separable Differential Equations and Exponential Growth", generator_id: "algebra_1.multi_step", available: true },
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
    steps_typst: ["4 x + 7 = 31", "Subtract 7: 4 x = 24", "Divide by 4: x = 6"],
    distractors: ["$x = 7$", "$x = 5$", "$x = -6$"],
    difficulty: "mild",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_2",
    prompt_text: "Solve for x:",
    equation_typst: "$-3 x - 8 = 13$",
    answer_typst: "$x = -7$",
    steps_typst: ["-3 x - 8 = 13", "Add 8: -3 x = 21", "Divide by -3: x = -7"],
    distractors: ["$x = 7$", "$x = -5$", "$x = -8$"],
    difficulty: "mild",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_3",
    prompt_text: "Solve for x:",
    equation_typst: "$5 (x - 2) = 25$",
    answer_typst: "$x = 7$",
    steps_typst: ["5 (x - 2) = 25", "Distribute 5: 5 x - 10 = 25", "Add 10: 5 x = 35", "Divide by 5: x = 7"],
    distractors: ["$x = 5$", "$x = 3$", "$x = -7$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_4",
    prompt_text: "Solve for x:",
    equation_typst: "$2 x / 3 + 4 = 10$",
    answer_typst: "$x = 9$",
    steps_typst: ["2 x / 3 + 4 = 10", "Subtract 4: 2 x / 3 = 6", "Multiply by 3: 2 x = 18", "Divide by 2: x = 9"],
    distractors: ["$x = 6$", "$x = 12$", "$x = -9$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.3"],
  },
  {
    id: "demo_5",
    prompt_text: "Solve by factoring:",
    equation_typst: "$x^2 - 5 x + 6 = 0$",
    answer_typst: "$x = 2, 3$",
    steps_typst: ["x^2 - 5 x + 6 = 0", "Factor: (x - 2)(x - 3) = 0", "Solve factors: x = 2, 3"],
    distractors: ["$x = -2, -3$", "$x = 1, 6$", "$x = -1, -6$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.4.B"],
  },
  {
    id: "demo_6",
    prompt_text: "Solve by factoring:",
    equation_typst: "$x^2 + 7 x + 12 = 0$",
    answer_typst: "$x = -3, -4$",
    steps_typst: ["x^2 + 7 x + 12 = 0", "Factor: (x + 3)(x + 4) = 0", "Solve factors: x = -3, -4"],
    distractors: ["$x = 3, 4$", "$x = -2, -6$", "$x = 2, 6$"],
    difficulty: "medium",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.4.B"],
  },
  {
    id: "demo_7",
    prompt_text: "Solve by factoring:",
    equation_typst: "$2 x^2 - 7 x + 3 = 0$",
    answer_typst: "$x = 1/2, 3$",
    steps_typst: ["2 x^2 - 7 x + 3 = 0", "Factor: (2 x - 1)(x - 3) = 0", "Solve factors: x = 1/2, 3"],
    distractors: ["$x = -1/2, -3$", "$x = 1, 3/2$", "$x = 2, 3$"],
    difficulty: "spicy",
    standards: ["CCSS.MATH.CONTENT.HSA.REI.B.4.B"],
  },
  {
    id: "demo_8",
    prompt_text: "Solve using the quadratic formula:",
    equation_typst: "$x^2 - 4 x - 5 = 0$",
    answer_typst: "$x = 5, -1$",
    steps_typst: ["x^2 - 4 x - 5 = 0", "Formula: x = (4 +- sqrt(16 - 4(1)(-5))) / 2", "Simplify: x = (4 +- 6) / 2", "Result: x = 5, -1"],
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
