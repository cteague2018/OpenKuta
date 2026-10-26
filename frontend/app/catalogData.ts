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

export interface Choice {
  letter: string;
  text: string;
}

export interface Problem {
  id: string;
  prompt_text: string;
  equation_typst: string;
  answer_typst: string;
  steps_typst: string[];
  distractors: string[];
  choices?: Choice[];
  correct_choice?: string;
  question_type?: "free_response" | "multiple_choice";
  difficulty: "mild" | "medium" | "spicy";
  standards: string[];
}

export const DEFAULT_COURSE_CATALOG: Record<string, Course> = {
  "algebra_1": {
    "title": "Algebra 1",
    "description": "Covers all typical algebra material, over 90 topics in all, from adding and subtracting positives and negatives to solving rational equations.",
    "categories": [
      {
        "name": "Beginning Algebra",
        "topics": [
          {
            "id": "algebra_1.beginning_algeb.verbal_expressions",
            "name": "Verbal expressions",
            "generator_id": "algebra_1.verbal_expressions",
            "available": true
          },
          {
            "id": "algebra_1.beginning_algeb.order_of_operations",
            "name": "Order of operations",
            "generator_id": "grade_6.order_of_operations",
            "available": true
          },
          {
            "id": "algebra_1.beginning_algeb.sets_of_numbers",
            "name": "Sets of numbers",
            "generator_id": "algebra_1.scientific_notation",
            "available": true
          },
          {
            "id": "algebra_1.beginning_algeb.adding_and_subtracting_ra",
            "name": "Adding and subtracting rational numbers",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_1.beginning_algeb.multiplying_rational_numb",
            "name": "Multiplying rational numbers",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_1.beginning_algeb.dividing_rational_numbers",
            "name": "Dividing rational numbers",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_1.beginning_algeb.the_distributive_property",
            "name": "The Distributive Property",
            "generator_id": "algebra_1.distributive_property",
            "available": true
          }
        ]
      },
      {
        "name": "Equations",
        "topics": [
          {
            "id": "algebra_1.equations.one_step_equations",
            "name": "One-step equations",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "algebra_1.equations.two_step_equations",
            "name": "Two-step equations",
            "generator_id": "algebra_1.two_step",
            "available": true
          },
          {
            "id": "algebra_1.equations.multi_step_equations",
            "name": "Multi-step equations",
            "generator_id": "algebra_1.multi_step",
            "available": true
          },
          {
            "id": "algebra_1.equations.absolute_value_equations",
            "name": "Absolute value equations",
            "generator_id": "algebra_1.absolute_value",
            "available": true
          },
          {
            "id": "algebra_1.equations.mixture_word_problems",
            "name": "Mixture word problems",
            "generator_id": "algebra_1.word_problems",
            "available": true
          },
          {
            "id": "algebra_1.equations.distance_rate_time_word_p",
            "name": "Distance, rate, time word problems",
            "generator_id": "algebra_1.word_problems",
            "available": true
          },
          {
            "id": "algebra_1.equations.work_word_problems",
            "name": "Work word problems",
            "generator_id": "algebra_1.word_problems",
            "available": true
          },
          {
            "id": "algebra_1.equations.literal_equations",
            "name": "Literal equations",
            "generator_id": "algebra_1.literal_equations",
            "available": true
          }
        ]
      },
      {
        "name": "Inequalities",
        "topics": [
          {
            "id": "algebra_1.inequalities.graphing_single_variable_",
            "name": "Graphing single-variable inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "algebra_1.inequalities.one_step_inequalities",
            "name": "One-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "algebra_1.inequalities.two_step_inequalities",
            "name": "Two-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "algebra_1.inequalities.multi_step_inequalities",
            "name": "Multi-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "algebra_1.inequalities.compound_inequalities",
            "name": "Compound inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "algebra_1.inequalities.absolute_value_inequaliti",
            "name": "Absolute value inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          }
        ]
      },
      {
        "name": "Proportions and Percents",
        "topics": [
          {
            "id": "algebra_1.proportions_and.solving_proportions",
            "name": "Solving proportions",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "algebra_1.proportions_and.percents",
            "name": "Percents",
            "generator_id": "grade_6.percents",
            "available": true
          },
          {
            "id": "algebra_1.proportions_and.percent_of_change",
            "name": "Percent of change",
            "generator_id": "grade_6.percents",
            "available": true
          }
        ]
      },
      {
        "name": "Relations and Introduction to Functions",
        "topics": [
          {
            "id": "algebra_1.relations_and_i.discrete_relations",
            "name": "Discrete relations",
            "generator_id": "algebra_1.two_step",
            "available": true
          },
          {
            "id": "algebra_1.relations_and_i.continuous_relations",
            "name": "Continuous relations",
            "generator_id": "algebra_1.two_step",
            "available": true
          },
          {
            "id": "algebra_1.relations_and_i.evaluating_and_graphing_f",
            "name": "Evaluating and graphing functions",
            "generator_id": "algebra_2.general_functions",
            "available": true
          }
        ]
      },
      {
        "name": "Linear Equations and Inequalities",
        "topics": [
          {
            "id": "algebra_1.linear_equation.slope",
            "name": "Slope",
            "generator_id": "algebra_1.slope",
            "available": true
          },
          {
            "id": "algebra_1.linear_equation.more_on_slope",
            "name": "More on slope",
            "generator_id": "algebra_1.slope",
            "available": true
          },
          {
            "id": "algebra_1.linear_equation.graphing_linear_equations",
            "name": "Graphing linear equations",
            "generator_id": "algebra_1.graphing_lines",
            "available": true
          },
          {
            "id": "algebra_1.linear_equation.writing_linear_equations",
            "name": "Writing linear equations",
            "generator_id": "algebra_1.writing_linear_equations",
            "available": true
          },
          {
            "id": "algebra_1.linear_equation.graphing_linear_inequalit",
            "name": "Graphing linear inequalities",
            "generator_id": "algebra_1.graphing_linear_inequalities",
            "available": true
          },
          {
            "id": "algebra_1.linear_equation.graphing_absolute_value_e",
            "name": "Graphing absolute value equations",
            "generator_id": "algebra_1.absolute_value",
            "available": true
          },
          {
            "id": "algebra_1.linear_equation.direct_and_inverse_variat",
            "name": "Direct and inverse variation",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          }
        ]
      },
      {
        "name": "Systems of Equations and Inequalities",
        "topics": [
          {
            "id": "algebra_1.systems_of_equa.solving_by_graphing",
            "name": "Solving by graphing",
            "generator_id": "algebra_1.systems_graphing",
            "available": true
          },
          {
            "id": "algebra_1.systems_of_equa.solving_by_elimination",
            "name": "Solving by elimination",
            "generator_id": "algebra_1.systems_elimination",
            "available": true
          },
          {
            "id": "algebra_1.systems_of_equa.solving_by_substitution",
            "name": "Solving by substitution",
            "generator_id": "algebra_1.systems_substitution",
            "available": true
          },
          {
            "id": "algebra_1.systems_of_equa.graphing_systems_of_inequ",
            "name": "Graphing systems of inequalities",
            "generator_id": "algebra_1.systems_inequalities",
            "available": true
          },
          {
            "id": "algebra_1.systems_of_equa.word_problems",
            "name": "Word problems",
            "generator_id": "algebra_1.word_problems",
            "available": true
          }
        ]
      },
      {
        "name": "Exponents",
        "topics": [
          {
            "id": "algebra_1.exponents.properties_of_exponents",
            "name": "Properties of exponents",
            "generator_id": "algebra_1.exponent_rules",
            "available": true
          },
          {
            "id": "algebra_1.exponents.graphing_exponential_func",
            "name": "Graphing exponential functions",
            "generator_id": "algebra_1.exponential_functions",
            "available": true
          },
          {
            "id": "algebra_1.exponents.writing_scientific_notati",
            "name": "Writing scientific notation",
            "generator_id": "algebra_1.scientific_notation",
            "available": true
          },
          {
            "id": "algebra_1.exponents.operations_and_scientific",
            "name": "Operations and scientific notation",
            "generator_id": "algebra_1.scientific_notation",
            "available": true
          },
          {
            "id": "algebra_1.exponents.addition_subtraction_and_",
            "name": "Addition/Subtraction and scientific notation",
            "generator_id": "algebra_1.scientific_notation",
            "available": true
          },
          {
            "id": "algebra_1.exponents.discrete_exponential_grow",
            "name": "Discrete exponential growth and decay word problems",
            "generator_id": "algebra_1.exponential_functions",
            "available": true
          }
        ]
      },
      {
        "name": "Polynomials",
        "topics": [
          {
            "id": "algebra_1.polynomials.naming",
            "name": "Naming",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_1.polynomials.adding_and_subtracting",
            "name": "Adding and subtracting",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_1.polynomials.dividing",
            "name": "Dividing",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_1.polynomials.multiplying",
            "name": "Multiplying",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_1.polynomials.multiplying_special_cases",
            "name": "Multiplying special cases",
            "generator_id": "algebra_1.factoring",
            "available": true
          }
        ]
      },
      {
        "name": "Factoring",
        "topics": [
          {
            "id": "algebra_1.factoring.common_factor_only",
            "name": "Common factor only",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_1.factoring.quadratic_expressions",
            "name": "Quadratic expressions",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_1.factoring.special_cases",
            "name": "Special cases",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_1.factoring.by_grouping",
            "name": "By grouping",
            "generator_id": "algebra_1.factoring",
            "available": true
          }
        ]
      },
      {
        "name": "Quadratic Functions",
        "topics": [
          {
            "id": "algebra_1.quadratic_funct.graphing",
            "name": "Graphing",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_1.quadratic_funct.graphing_quadratic_inequa",
            "name": "Graphing quadratic inequalities",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_1.quadratic_funct.solving_equations_by_taki",
            "name": "Solving equations by taking square roots",
            "generator_id": "algebra_1.quadratics_square_roots",
            "available": true
          },
          {
            "id": "algebra_1.quadratic_funct.solving_equations_by_fact",
            "name": "Solving equations by factoring",
            "generator_id": "algebra_1.quadratics_factoring",
            "available": true
          },
          {
            "id": "algebra_1.quadratic_funct.solving_equations_with_th",
            "name": "Solving equations with the Quadratic Formula",
            "generator_id": "algebra_1.quadratics_formula",
            "available": true
          },
          {
            "id": "algebra_1.quadratic_funct.understanding_the_discrim",
            "name": "Understanding the discriminant",
            "generator_id": "algebra_1.quadratics_discriminant",
            "available": true
          },
          {
            "id": "algebra_1.quadratic_funct.completing_the_square_by_",
            "name": "Completing the square by finding the constant",
            "generator_id": "algebra_1.quadratics_completing_square",
            "available": true
          },
          {
            "id": "algebra_1.quadratic_funct.solving_equations_by_comp",
            "name": "Solving equations by completing the square",
            "generator_id": "algebra_1.quadratics_completing_square",
            "available": true
          }
        ]
      },
      {
        "name": "Radical Expressions",
        "topics": [
          {
            "id": "algebra_1.radical_express.simplifying_single_radica",
            "name": "Simplifying single radicals",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_1.radical_express.the_distance_formula",
            "name": "The Distance Formula",
            "generator_id": "geometry.coordinate_geometry",
            "available": true
          },
          {
            "id": "algebra_1.radical_express.the_midpoint_formula",
            "name": "The Midpoint Formula",
            "generator_id": "geometry.coordinate_geometry",
            "available": true
          },
          {
            "id": "algebra_1.radical_express.adding_and_subtracting",
            "name": "Adding and subtracting",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_1.radical_express.multiplying",
            "name": "Multiplying",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_1.radical_express.dividing",
            "name": "Dividing",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_1.radical_express.equations",
            "name": "Equations",
            "generator_id": "algebra_2.radicals",
            "available": true
          }
        ]
      },
      {
        "name": "Rational Expressions",
        "topics": [
          {
            "id": "algebra_1.rational_expres.simplifying_and_excluded_",
            "name": "Simplifying and excluded values",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_1.rational_expres.multiplying_and_dividing",
            "name": "Multiplying and dividing",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_1.rational_expres.adding_and_subtracting",
            "name": "Adding and subtracting",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_1.rational_expres.equations",
            "name": "Equations",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          }
        ]
      },
      {
        "name": "Beginning Trigonometry",
        "topics": [
          {
            "id": "algebra_1.beginning_trigo.finding_sine_cosine_tange",
            "name": "Finding sine, cosine, tangent",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "algebra_1.beginning_trigo.finding_angles",
            "name": "Finding angles",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "algebra_1.beginning_trigo.find_missing_sides_of_tri",
            "name": "Find missing sides of triangles",
            "generator_id": "geometry.trigonometry",
            "available": true
          }
        ]
      },
      {
        "name": "Statistics",
        "topics": [
          {
            "id": "algebra_1.statistics.visualizing_data",
            "name": "Visualizing data",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "algebra_1.statistics.center_and_spread",
            "name": "Center and spread",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "algebra_1.statistics.scatter_plots",
            "name": "Scatter plots",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "algebra_1.statistics.using_statistical_models",
            "name": "Using statistical models",
            "generator_id": "grade_6.statistics",
            "available": true
          }
        ]
      }
    ]
  },
  "geometry": {
    "title": "Geometry",
    "description": "Covers all typical Geometry material, beginning with a review of important Algebra 1 concepts and going through transformations, over 85 topics in all.",
    "categories": [
      {
        "name": "Review of Algebra",
        "topics": [
          {
            "id": "geometry.review_of_algeb.multi_step_equations",
            "name": "Multi-step equations",
            "generator_id": "algebra_1.multi_step",
            "available": true
          },
          {
            "id": "geometry.review_of_algeb.simplifying_square_roots",
            "name": "Simplifying square roots",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "geometry.review_of_algeb.adding_and_subtracting_sq",
            "name": "Adding and subtracting square roots",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "geometry.review_of_algeb.multiplying_square_roots",
            "name": "Multiplying square roots",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "geometry.review_of_algeb.dividing_square_roots",
            "name": "Dividing square roots",
            "generator_id": "algebra_2.radicals",
            "available": true
          }
        ]
      },
      {
        "name": "Basics of Geometry",
        "topics": [
          {
            "id": "geometry.basics_of_geome.line_segments_and_their_m",
            "name": "Line segments and their measures",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.basics_of_geome.segment_addition_postulat",
            "name": "Segment Addition Postulate",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.basics_of_geome.angles_and_their_measures",
            "name": "Angles and their measures",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.basics_of_geome.classifying_angles",
            "name": "Classifying angles",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.basics_of_geome.basic_angle_terminology",
            "name": "Basic angle terminology",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.basics_of_geome.angle_addition_postulate",
            "name": "Angle Addition Postulate",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.basics_of_geome.angle_relationships",
            "name": "Angle relationships",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.basics_of_geome.geometric_diagrams_and_no",
            "name": "Geometric diagrams and notation",
            "generator_id": "geometry.triangles",
            "available": true
          }
        ]
      },
      {
        "name": "Parallel Lines and the Coordinate Plane",
        "topics": [
          {
            "id": "geometry.parallel_lines_.parallel_lines_and_transv",
            "name": "Parallel lines and transversals",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.parallel_lines_.points_of_the_coordinate_",
            "name": "Points of the coordinate plane",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.parallel_lines_.the_midpoint_formula",
            "name": "The Midpoint Formula",
            "generator_id": "geometry.coordinate_geometry",
            "available": true
          },
          {
            "id": "geometry.parallel_lines_.the_distance_formula",
            "name": "The Distance Formula",
            "generator_id": "geometry.coordinate_geometry",
            "available": true
          },
          {
            "id": "geometry.parallel_lines_.slope_and_lines",
            "name": "Slope and lines",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "geometry.parallel_lines_.graphing_linear_equations",
            "name": "Graphing linear equations",
            "generator_id": "algebra_1.graphing_lines",
            "available": true
          },
          {
            "id": "geometry.parallel_lines_.writing_linear_equations",
            "name": "Writing linear equations",
            "generator_id": "algebra_1.writing_linear_equations",
            "available": true
          }
        ]
      },
      {
        "name": "Congruent Triangles",
        "topics": [
          {
            "id": "geometry.congruent_trian.classifying_triangles",
            "name": "Classifying triangles",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.congruent_trian.triangle_angle_sum",
            "name": "Triangle angle sum",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.congruent_trian.exterior_angle_theorem",
            "name": "Exterior Angle Theorem",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.congruent_trian.triangles_and_congruence",
            "name": "Triangles and congruence",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.congruent_trian.proving_triangles_congrue",
            "name": "Proving triangles congruent",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.congruent_trian.isosceles_and_equilateral",
            "name": "Isosceles and equilateral triangles",
            "generator_id": "geometry.triangles",
            "available": true
          }
        ]
      },
      {
        "name": "Properties of Triangles",
        "topics": [
          {
            "id": "geometry.properties_of_t.midsegment",
            "name": "Midsegment",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.properties_of_t.angle_bisectors",
            "name": "Angle bisectors",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.properties_of_t.medians",
            "name": "Medians",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.properties_of_t.centroid",
            "name": "Centroid",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.properties_of_t.triangle_inequality_theor",
            "name": "Triangle Inequality Theorem",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.properties_of_t.inequalities_in_one_trian",
            "name": "Inequalities in one triangle",
            "generator_id": "geometry.triangles",
            "available": true
          }
        ]
      },
      {
        "name": "Quadrilaterals and Polygons",
        "topics": [
          {
            "id": "geometry.quadrilaterals_.classifying",
            "name": "Classifying",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.angles",
            "name": "Angles",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.parallelograms",
            "name": "Parallelograms",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.trapezoids",
            "name": "Trapezoids",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.rhombuses",
            "name": "Rhombuses",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.kites",
            "name": "Kites",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.area_of_triangles_and_qua",
            "name": "Area of triangles and quadrilaterals",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.polygon_basics",
            "name": "Polygon basics",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.quadrilaterals_.area_of_regular_polygons",
            "name": "Area of regular polygons",
            "generator_id": "geometry.area_volume",
            "available": true
          }
        ]
      },
      {
        "name": "Similarity",
        "topics": [
          {
            "id": "geometry.similarity.solving_proportions",
            "name": "Solving proportions",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "geometry.similarity.similar_polygons",
            "name": "Similar polygons",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.similarity.similar_triangles",
            "name": "Similar triangles",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.similarity.similar_right_triangles",
            "name": "Similar right triangles",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.similarity.proportional_parts_in_tri",
            "name": "Proportional parts in triangles and parallel lines",
            "generator_id": "geometry.triangles",
            "available": true
          }
        ]
      },
      {
        "name": "Right Triangles",
        "topics": [
          {
            "id": "geometry.right_triangles.the_pythagorean_theorem",
            "name": "The Pythagorean Theorem",
            "generator_id": "geometry.pythagorean",
            "available": true
          },
          {
            "id": "geometry.right_triangles.multi_step_pythagorean_th",
            "name": "Multi-step Pythagorean Theorem problems",
            "generator_id": "geometry.pythagorean",
            "available": true
          },
          {
            "id": "geometry.right_triangles.special_right_triangles",
            "name": "Special right triangles",
            "generator_id": "geometry.special_right_triangles",
            "available": true
          },
          {
            "id": "geometry.right_triangles.multi_step_special_right_",
            "name": "Multi-step special right triangle problems",
            "generator_id": "geometry.pythagorean",
            "available": true
          }
        ]
      },
      {
        "name": "Trigonometry",
        "topics": [
          {
            "id": "geometry.trigonometry.finding_trig_ratios",
            "name": "Finding trig. ratios",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "geometry.trigonometry.finding_angle_measures",
            "name": "Finding angle measures",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "geometry.trigonometry.solving_right_triangles",
            "name": "Solving right triangles",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "geometry.trigonometry.multi_step_trig_problems",
            "name": "Multi-step trig. problems",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "geometry.trigonometry.rhombuses_and_kites_with_",
            "name": "Rhombuses and kites with right triangles",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "geometry.trigonometry.trigonometry_and_area",
            "name": "Trigonometry and area",
            "generator_id": "geometry.trigonometry",
            "available": true
          }
        ]
      },
      {
        "name": "Surface Area and Volume",
        "topics": [
          {
            "id": "geometry.surface_area_an.solid_figures_identifying",
            "name": "Solid figures: identifying, volume, and area",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "geometry.surface_area_an.nets_of_solids",
            "name": "Nets of solids",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "geometry.surface_area_an.similar_solids",
            "name": "Similar solids",
            "generator_id": "geometry.area_volume",
            "available": true
          }
        ]
      },
      {
        "name": "Circles",
        "topics": [
          {
            "id": "geometry.circles.naming_arcs_and_central_a",
            "name": "Naming arcs and central angles",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.measures_of_arcs_and_cent",
            "name": "Measures of arcs and central angles",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.arcs_and_chords",
            "name": "Arcs and chords",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.circumference_and_area",
            "name": "Circumference and area",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.arc_length_and_sector_are",
            "name": "Arc length and sector area",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.inscribed_angles",
            "name": "Inscribed angles",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.tangents",
            "name": "Tangents",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.secant_and_tangent_angles",
            "name": "Secant and tangent angles",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.segment_measures",
            "name": "Segment measures",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.using_equations_of_circle",
            "name": "Using equations of circles",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "geometry.circles.writing_equations_of_circ",
            "name": "Writing equations of circles",
            "generator_id": "geometry.circles",
            "available": true
          }
        ]
      },
      {
        "name": "Transformations",
        "topics": [
          {
            "id": "geometry.transformations.translations_rotations_re",
            "name": "Translations, rotations, reflections, and dilations",
            "generator_id": "geometry.triangles",
            "available": true
          }
        ]
      },
      {
        "name": "Probability and Statistics",
        "topics": [
          {
            "id": "geometry.probability_and.sample_spaces_and_the_fun",
            "name": "Sample spaces and the Fundamental Counting Principle",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.probability_of_independen",
            "name": "Probability of independent and dependent events, word problems",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.probability_of_independen",
            "name": "Probability of independent and dependent events",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.probability_of_mutually_e",
            "name": "Probability of mutually exclusive events, word problems",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.probability_of_mutually_e",
            "name": "Probability of mutually exclusive events",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.permutations",
            "name": "Permutations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.combinations",
            "name": "Combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.permutations_vs_combinati",
            "name": "Permutations vs combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "geometry.probability_and.probability_with_permutat",
            "name": "Probability with permutations and combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          }
        ]
      },
      {
        "name": "Constructions",
        "topics": [
          {
            "id": "geometry.constructions.line_segments",
            "name": "Line segments",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.constructions.perpendicular_segments",
            "name": "Perpendicular segments",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.constructions.angles",
            "name": "Angles",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.constructions.triangles",
            "name": "Triangles",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.constructions.medians_of_a_triangle",
            "name": "Medians of a triangle",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.constructions.altitudes_of_a_triangle",
            "name": "Altitudes of a triangle",
            "generator_id": "geometry.triangles",
            "available": true
          },
          {
            "id": "geometry.constructions.angle_bisectors",
            "name": "Angle bisectors",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "geometry.constructions.circles",
            "name": "Circles",
            "generator_id": "geometry.circles",
            "available": true
          }
        ]
      }
    ]
  },
  "algebra_2": {
    "title": "Algebra 2",
    "description": "Covers all typical Algebra 2 material, beginning with a few major Algebra 1 concepts and going through trigonometry, over 125 topics in all.",
    "categories": [
      {
        "name": "Beginning Algebra",
        "topics": [
          {
            "id": "algebra_2.beginning_algeb.order_of_operations",
            "name": "Order of operations",
            "generator_id": "grade_6.order_of_operations",
            "available": true
          },
          {
            "id": "algebra_2.beginning_algeb.simplifying_algebraic_exp",
            "name": "Simplifying algebraic expressions",
            "generator_id": "algebra_1.two_step",
            "available": true
          }
        ]
      },
      {
        "name": "Equations and Inequalities",
        "topics": [
          {
            "id": "algebra_2.equations_and_i.multi_step_equations",
            "name": "Multi-step equations",
            "generator_id": "algebra_1.multi_step",
            "available": true
          },
          {
            "id": "algebra_2.equations_and_i.work_word_problems",
            "name": "Work word problems",
            "generator_id": "algebra_1.word_problems",
            "available": true
          },
          {
            "id": "algebra_2.equations_and_i.distance_rate_time_word_p",
            "name": "Distance, rate, time word problems",
            "generator_id": "algebra_1.word_problems",
            "available": true
          },
          {
            "id": "algebra_2.equations_and_i.mixture_word_problems",
            "name": "Mixture word problems",
            "generator_id": "algebra_1.word_problems",
            "available": true
          },
          {
            "id": "algebra_2.equations_and_i.absolute_value_equations",
            "name": "Absolute value equations",
            "generator_id": "algebra_1.absolute_value",
            "available": true
          },
          {
            "id": "algebra_2.equations_and_i.multi_step_inequalities",
            "name": "Multi-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "algebra_2.equations_and_i.compound_inequalities",
            "name": "Compound inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "algebra_2.equations_and_i.absolute_value_inequaliti",
            "name": "Absolute value inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          }
        ]
      },
      {
        "name": "Relations and Introduction to Functions",
        "topics": [
          {
            "id": "algebra_2.relations_and_i.discrete_relations",
            "name": "Discrete relations",
            "generator_id": "algebra_1.two_step",
            "available": true
          },
          {
            "id": "algebra_2.relations_and_i.continuous_relations",
            "name": "Continuous relations",
            "generator_id": "algebra_1.two_step",
            "available": true
          },
          {
            "id": "algebra_2.relations_and_i.evaluating_and_graphing_f",
            "name": "Evaluating and graphing functions",
            "generator_id": "algebra_2.general_functions",
            "available": true
          }
        ]
      },
      {
        "name": "Linear Relations and Functions",
        "topics": [
          {
            "id": "algebra_2.linear_relation.graphing_linear_equations",
            "name": "Graphing linear equations",
            "generator_id": "algebra_1.graphing_lines",
            "available": true
          },
          {
            "id": "algebra_2.linear_relation.writing_linear_equations",
            "name": "Writing linear equations",
            "generator_id": "algebra_1.writing_linear_equations",
            "available": true
          },
          {
            "id": "algebra_2.linear_relation.graphing_absolute_value_e",
            "name": "Graphing absolute value equations",
            "generator_id": "algebra_1.absolute_value",
            "available": true
          },
          {
            "id": "algebra_2.linear_relation.graphing_linear_inequalit",
            "name": "Graphing linear inequalities",
            "generator_id": "algebra_1.graphing_linear_inequalities",
            "available": true
          },
          {
            "id": "algebra_2.linear_relation.direct_and_inverse_variat",
            "name": "Direct and Inverse Variation",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          }
        ]
      },
      {
        "name": "Systems of Equations and Inequalities",
        "topics": [
          {
            "id": "algebra_2.systems_of_equa.graphing_systems_of_linea",
            "name": "Graphing systems of linear inequalities",
            "generator_id": "algebra_1.systems_inequalities",
            "available": true
          },
          {
            "id": "algebra_2.systems_of_equa.solving_systems_by_graphi",
            "name": "Solving systems by graphing (2 variables)",
            "generator_id": "algebra_1.systems_graphing",
            "available": true
          },
          {
            "id": "algebra_2.systems_of_equa.solving_systems_by_elimin",
            "name": "Solving systems by elimination (2 variables)",
            "generator_id": "algebra_1.systems_elimination",
            "available": true
          },
          {
            "id": "algebra_2.systems_of_equa.solving_systems_by_substi",
            "name": "Solving systems by substitution (2 variables)",
            "generator_id": "algebra_1.systems_substitution",
            "available": true
          },
          {
            "id": "algebra_2.systems_of_equa.systems_of_equations_word",
            "name": "Systems of equations word problems (2 variables)",
            "generator_id": "algebra_1.systems",
            "available": true
          },
          {
            "id": "algebra_2.systems_of_equa.points_in_three_dimension",
            "name": "Points in three dimensions",
            "generator_id": "algebra_1.systems",
            "available": true
          },
          {
            "id": "algebra_2.systems_of_equa.planes",
            "name": "Planes",
            "generator_id": "algebra_1.systems",
            "available": true
          },
          {
            "id": "algebra_2.systems_of_equa.solving_systems_with_thre",
            "name": "Solving systems with three variables",
            "generator_id": "algebra_1.systems",
            "available": true
          }
        ]
      },
      {
        "name": "Matrices",
        "topics": [
          {
            "id": "algebra_2.matrices.operations",
            "name": "Operations",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "algebra_2.matrices.determinants",
            "name": "Determinants",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "algebra_2.matrices.inverses",
            "name": "Inverses",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "algebra_2.matrices.cramer_s_rule",
            "name": "Cramer's Rule",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "algebra_2.matrices.equations",
            "name": "Equations",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "algebra_2.matrices.geometric_transformations",
            "name": "Geometric transformations",
            "generator_id": "precalculus.matrices",
            "available": true
          }
        ]
      },
      {
        "name": "Complex Numbers",
        "topics": [
          {
            "id": "algebra_2.complex_numbers.operations",
            "name": "Operations",
            "generator_id": "algebra_2.complex_numbers",
            "available": true
          },
          {
            "id": "algebra_2.complex_numbers.graphing",
            "name": "Graphing",
            "generator_id": "algebra_2.complex_numbers",
            "available": true
          },
          {
            "id": "algebra_2.complex_numbers.absolute_value",
            "name": "Absolute value",
            "generator_id": "algebra_2.complex_numbers",
            "available": true
          },
          {
            "id": "algebra_2.complex_numbers.rationalizing_denominator",
            "name": "Rationalizing denominators",
            "generator_id": "algebra_2.complex_numbers",
            "available": true
          }
        ]
      },
      {
        "name": "Quadratic Functions and Inequalities",
        "topics": [
          {
            "id": "algebra_2.quadratic_funct.graphing_quadratic_functi",
            "name": "Graphing quadratic functions",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.graphing_quadratic_inequa",
            "name": "Graphing quadratic inequalities",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.factoring_quadratic_expre",
            "name": "Factoring quadratic expressions",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.factoring_special_case_qu",
            "name": "Factoring special case quadratic expressions",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.solving_equations_by_taki",
            "name": "Solving equations by taking square roots",
            "generator_id": "algebra_1.quadratics_square_roots",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.solving_equations_by_fact",
            "name": "Solving equations by factoring",
            "generator_id": "algebra_1.quadratics_factoring",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.completing_the_square",
            "name": "Completing the square",
            "generator_id": "algebra_1.quadratics_completing_square",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.solving_equations_by_comp",
            "name": "Solving equations by completing the square",
            "generator_id": "algebra_1.quadratics_completing_square",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.solving_equations_with_th",
            "name": "Solving equations with the Quadratic Formula",
            "generator_id": "algebra_1.quadratics_formula",
            "available": true
          },
          {
            "id": "algebra_2.quadratic_funct.the_discriminant",
            "name": "The discriminant",
            "generator_id": "algebra_1.quadratics_discriminant",
            "available": true
          }
        ]
      },
      {
        "name": "Polynomial Functions",
        "topics": [
          {
            "id": "algebra_2.polynomial_func.naming",
            "name": "Naming",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.adding_and_subtracting",
            "name": "Adding and subtracting",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.multiplying",
            "name": "Multiplying",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.multiplying_special_cases",
            "name": "Multiplying special cases",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.the_binomial_theorem",
            "name": "The Binomial Theorem",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.dividing",
            "name": "Dividing",
            "generator_id": "algebra_2.polynomial_division",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.factoring_by_grouping",
            "name": "Factoring by grouping",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.factoring_a_sum_differenc",
            "name": "Factoring a sum/difference of cubes",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.factoring_quadratic_form",
            "name": "Factoring quadratic form",
            "generator_id": "algebra_1.quadratics",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.factoring_all_techniques",
            "name": "Factoring, all techniques",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.the_remainder_theorem",
            "name": "The Remainder Theorem",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.writing_functions",
            "name": "Writing functions",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.conjugate_roots_factoring",
            "name": "Conjugate roots & factoring",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.conjugate_roots_writing_f",
            "name": "Conjugate roots & writing functions",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.descartes_rule_of_signs",
            "name": "Descartes' Rule of Signs",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.rational_zero_root_theore",
            "name": "Rational Zero/Root Theorem",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.fundamental_theorem_of_al",
            "name": "Fundamental Theorem of Algebra",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.solving_polynomial_equati",
            "name": "Solving polynomial equations",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.end_behavior_and_general_",
            "name": "End behavior and general graph shape",
            "generator_id": "algebra_1.factoring",
            "available": true
          },
          {
            "id": "algebra_2.polynomial_func.graphing",
            "name": "Graphing",
            "generator_id": "algebra_1.factoring",
            "available": true
          }
        ]
      },
      {
        "name": "General Functions",
        "topics": [
          {
            "id": "algebra_2.general_functio.evaluating",
            "name": "Evaluating",
            "generator_id": "algebra_2.general_functions",
            "available": true
          },
          {
            "id": "algebra_2.general_functio.operations",
            "name": "Operations",
            "generator_id": "algebra_2.general_functions",
            "available": true
          },
          {
            "id": "algebra_2.general_functio.inverses",
            "name": "Inverses",
            "generator_id": "algebra_2.general_functions",
            "available": true
          }
        ]
      },
      {
        "name": "Radical Functions and Rational Exponents",
        "topics": [
          {
            "id": "algebra_2.radical_functio.simplifying_radicals",
            "name": "Simplifying radicals",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.adding_and_subtracting_ra",
            "name": "Adding and subtracting radical expressions",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.multiplying_radical_expre",
            "name": "Multiplying radical expressions",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.dividing_radical_expressi",
            "name": "Dividing radical expressions",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.connecting_radical_expres",
            "name": "Connecting radical expressions and rational exponents",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.evaluating_rational_expon",
            "name": "Evaluating rational exponent expressions",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.the_properties_of_exponen",
            "name": "The properties of exponents",
            "generator_id": "algebra_1.exponent_rules",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.radical_equations",
            "name": "Radical equations",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.rational_exponent_equatio",
            "name": "Rational exponent equations",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.graphing_radical_equation",
            "name": "Graphing radical equations",
            "generator_id": "algebra_2.radicals",
            "available": true
          },
          {
            "id": "algebra_2.radical_functio.domain_and_range_of_radic",
            "name": "Domain and range of radical functions",
            "generator_id": "algebra_2.radicals",
            "available": true
          }
        ]
      },
      {
        "name": "Conic Sections",
        "topics": [
          {
            "id": "algebra_2.conic_sections.parabolas_graphing_proper",
            "name": "Parabolas, graphing & properties",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.parabolas_writing_equatio",
            "name": "Parabolas, writing equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.circles_graphing_properti",
            "name": "Circles, graphing & properties",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.circles_writing_equations",
            "name": "Circles, writing equations",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.ellipses_graphing_propert",
            "name": "Ellipses, graphing & properties",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.ellipses_writing_equation",
            "name": "Ellipses, writing equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.hyperbolas_graphing_prope",
            "name": "Hyperbolas, graphing & properties",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.hyperbolas_writing_equati",
            "name": "Hyperbolas, writing equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.classifying",
            "name": "Classifying",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "algebra_2.conic_sections.systems_of_quadratic_equa",
            "name": "Systems of quadratic equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          }
        ]
      },
      {
        "name": "Rational Expressions",
        "topics": [
          {
            "id": "algebra_2.rational_expres.graphing",
            "name": "Graphing",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_2.rational_expres.simplifying",
            "name": "Simplifying",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_2.rational_expres.multiplying_and_dividing",
            "name": "Multiplying and dividing",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_2.rational_expres.adding_and_subtracting",
            "name": "Adding and subtracting",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_2.rational_expres.complex_fractions",
            "name": "Complex fractions",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "algebra_2.rational_expres.equations",
            "name": "Equations",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          }
        ]
      },
      {
        "name": "Exponential and Logarithmic Expressions",
        "topics": [
          {
            "id": "algebra_2.exponential_and.graphing_exponential_func",
            "name": "Graphing exponential functions",
            "generator_id": "algebra_1.exponential_functions",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.exponential_equations_not",
            "name": "Exponential equations not requiring logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.exponents_and_logarithms",
            "name": "Exponents and logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.evaluating_logarithms",
            "name": "Evaluating logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.logarithms_and_exponents_",
            "name": "Logarithms and exponents as inverses",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.properties_of_logarithms",
            "name": "Properties of logarithms",
            "generator_id": "algebra_2.log_properties",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.writing_logs_in_terms_of_",
            "name": "Writing logs in terms of others",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.exponential_equations_req",
            "name": "Exponential equations requiring logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.inverses_of",
            "name": "Inverses of",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.logarithmic_equations_sim",
            "name": "Logarithmic equations, simple",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.logarithmic_equations_har",
            "name": "Logarithmic equations, hard",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.graphing_logarithmic_func",
            "name": "Graphing logarithmic functions",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.discrete_exponential_grow",
            "name": "Discrete exponential growth and decay word problems",
            "generator_id": "algebra_1.exponential_functions",
            "available": true
          },
          {
            "id": "algebra_2.exponential_and.continuous_exponential_gr",
            "name": "Continuous exponential growth and decay word problems",
            "generator_id": "algebra_1.exponential_functions",
            "available": true
          }
        ]
      },
      {
        "name": "Sequences and Series",
        "topics": [
          {
            "id": "algebra_2.sequences_and_s.general_sequences",
            "name": "General sequences",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "algebra_2.sequences_and_s.arithmetic_sequences",
            "name": "Arithmetic sequences",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "algebra_2.sequences_and_s.geometric_sequences",
            "name": "Geometric sequences",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "algebra_2.sequences_and_s.arithmetic_and_geometric_",
            "name": "Arithmetic and geometric mean",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "algebra_2.sequences_and_s.general_series",
            "name": "General series",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "algebra_2.sequences_and_s.arithmetic_series",
            "name": "Arithmetic series",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "algebra_2.sequences_and_s.geometric_series",
            "name": "Geometric series",
            "generator_id": "precalculus.sequences",
            "available": true
          }
        ]
      },
      {
        "name": "Trigonometry",
        "topics": [
          {
            "id": "algebra_2.trigonometry.angles_and_angle_measure",
            "name": "Angles and angle measure",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.radians_and_degrees",
            "name": "Radians and degrees",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.degrees_and_degrees_minut",
            "name": "Degrees and degrees-minutes-seconds",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.coterminal_angles",
            "name": "Coterminal angles",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.arc_length_and_sector_are",
            "name": "Arc length and sector area",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.right_triangle_trig_findi",
            "name": "Right triangle trig: Finding ratios",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.right_triangle_trig_findi",
            "name": "Right triangle trig: Finding angle measures",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.right_triangle_trig_findi",
            "name": "Right triangle trig: Finding angles and sides",
            "generator_id": "geometry.trigonometry",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.trig_functions_of_any_ang",
            "name": "Trig functions of any angle",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.the_law_of_sines",
            "name": "The Law of Sines",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.the_law_of_cosines",
            "name": "The Law of Cosines",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.area_and_laws_of_sines_an",
            "name": "Area and Laws of Sines and Cosines",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.graphing_trig_functions",
            "name": "Graphing trig functions",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.angle_sum_difference_iden",
            "name": "Angle sum/difference identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.double_angle_half_angle_i",
            "name": "Double-angle/half-angle identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "algebra_2.trigonometry.equations",
            "name": "Equations",
            "generator_id": "precalculus.trig",
            "available": true
          }
        ]
      },
      {
        "name": "Probability and Statistics",
        "topics": [
          {
            "id": "algebra_2.probability_and.sample_spaces_and_the_fun",
            "name": "Sample spaces and the Fundamental Counting Principle",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.probability_of_independen",
            "name": "Probability of independent and dependent events, word problems",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.probability_of_independen",
            "name": "Probability of independent and dependent events",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.probability_of_mutually_e",
            "name": "Probability of mutually exclusive events, word problems",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.probability_of_mutually_e",
            "name": "Probability of mutually exclusive events",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.permutations",
            "name": "Permutations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.combinations",
            "name": "Combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.permutations_vs_combinati",
            "name": "Permutations vs combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "algebra_2.probability_and.probability_with_permutat",
            "name": "Probability with permutations and combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          }
        ]
      }
    ]
  },
  "precalculus": {
    "title": "Precalculus",
    "description": "Covers all typical Precalculus material and more: trigonometric functions, equations, and identities; parametric equations; polar coordinates; vectors; limits; and more. Over 100 topics.",
    "categories": [
      {
        "name": "Functions",
        "topics": [
          {
            "id": "precalculus.functions.continuity",
            "name": "Continuity",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "precalculus.functions.extrema_intervals_of_incr",
            "name": "Extrema, intervals of increase and decrease",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "precalculus.functions.power_functions",
            "name": "Power functions",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.functions.average_rates_of_change",
            "name": "Average rates of change",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "precalculus.functions.transformations_of_graphs",
            "name": "Transformations of graphs",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.functions.piecewise_functions",
            "name": "Piecewise functions",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.functions.operations",
            "name": "Operations",
            "generator_id": "algebra_2.general_functions",
            "available": true
          },
          {
            "id": "precalculus.functions.inverses",
            "name": "Inverses",
            "generator_id": "algebra_2.general_functions",
            "available": true
          }
        ]
      },
      {
        "name": "Power, Polynomial, and Rational Functions",
        "topics": [
          {
            "id": "precalculus.power_polynomia.graphs_real_zeros_and_end",
            "name": "Graphs, real zeros, and end behavior of polynomial functions",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.dividing_polynomial_funct",
            "name": "Dividing polynomial functions",
            "generator_id": "algebra_2.polynomial_division",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.the_remainder_theorem_and",
            "name": "The Remainder Theorem and bounds of real zeros",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.writing_polynomial_functi",
            "name": "Writing polynomial functions and conjugate roots",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.complex_zeros_and_the_fun",
            "name": "Complex zeros and The Fundamental Theorem of Algebra",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.graphs_of_rational_functi",
            "name": "Graphs of rational functions",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.rational_equations",
            "name": "Rational equations",
            "generator_id": "algebra_2.rational_expressions",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.polynomial_inequalities",
            "name": "Polynomial inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "precalculus.power_polynomia.rational_inequalities",
            "name": "Rational inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          }
        ]
      },
      {
        "name": "Exponential and Logarithmic Expressions",
        "topics": [
          {
            "id": "precalculus.exponential_and.graphing_exponential_func",
            "name": "Graphing exponential functions",
            "generator_id": "algebra_1.exponential_functions",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.exponential_equations_not",
            "name": "Exponential equations not requiring logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.exponents_and_logarithms",
            "name": "Exponents and logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.evaluating_logarithms",
            "name": "Evaluating logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.logarithms_and_exponents_",
            "name": "Logarithms and exponents as inverses",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.properties_of_logarithms",
            "name": "Properties of logarithms",
            "generator_id": "algebra_2.log_properties",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.writing_logs_in_terms_of_",
            "name": "Writing logs in terms of others",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.exponential_equations_req",
            "name": "Exponential equations requiring logarithms",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.logarithmic_equations_sim",
            "name": "Logarithmic equations, simple",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.logarithmic_equations_har",
            "name": "Logarithmic equations, hard",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.graphing_logarithmic_func",
            "name": "Graphing logarithmic functions",
            "generator_id": "algebra_2.logarithms",
            "available": true
          },
          {
            "id": "precalculus.exponential_and.compound_interest",
            "name": "Compound interest",
            "generator_id": "algebra_2.logarithms",
            "available": true
          }
        ]
      },
      {
        "name": "Trigonometry",
        "topics": [
          {
            "id": "precalculus.trigonometry.angles_and_angle_measure",
            "name": "Angles and angle measure",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.radians_and_degrees",
            "name": "Radians and degrees",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.right_triangle_trig_findi",
            "name": "Right triangle trig: Finding ratios",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.right_triangle_trig_findi",
            "name": "Right triangle trig: Finding angles and sides",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.trig_functions_of_any_ang",
            "name": "Trig functions of any angle",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.graphing_trig_functions",
            "name": "Graphing trig functions",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.simple_trig_equations",
            "name": "Simple trig equations",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.inverse_trig_functions",
            "name": "Inverse trig functions",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.fundamental_identities",
            "name": "Fundamental identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.equations_with_factoring_",
            "name": "Equations with factoring and fundamental identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.sum_and_difference_identi",
            "name": "Sum and Difference Identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.multiple_angle_identities",
            "name": "Multiple-Angle Identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.product_to_sum_identities",
            "name": "Product-to-Sum Identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.equations_and_multiple_an",
            "name": "Equations and Multiple-Angle Identities",
            "generator_id": "precalculus.trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.the_law_of_sines",
            "name": "The Law of Sines",
            "generator_id": "precalculus.triangle_trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.the_law_of_cosines",
            "name": "The Law of Cosines",
            "generator_id": "precalculus.triangle_trig",
            "available": true
          },
          {
            "id": "precalculus.trigonometry.area_and_laws_of_sines_an",
            "name": "Area and Laws of Sines and Cosines",
            "generator_id": "precalculus.trig",
            "available": true
          }
        ]
      },
      {
        "name": "Parametric Equations",
        "topics": [
          {
            "id": "precalculus.parametric_equa.parametric_equations",
            "name": "Parametric equations",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.parametric_equa.projectile_motion",
            "name": "Projectile motion",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          }
        ]
      },
      {
        "name": "Polar Coordinates",
        "topics": [
          {
            "id": "precalculus.polar_coordinat.polar_coordinates",
            "name": "Polar coordinates",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.polar_coordinat.graphs_of_polar_equations",
            "name": "Graphs of polar equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.polar_coordinat.polar_and_rectangular_for",
            "name": "Polar and rectangular forms of equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.polar_coordinat.polar_forms_of_conic_sect",
            "name": "Polar forms of conic section",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.polar_coordinat.complex_numbers_in_polar_",
            "name": "Complex numbers in polar form",
            "generator_id": "precalculus.polar_conics",
            "available": true
          }
        ]
      },
      {
        "name": "Vectors",
        "topics": [
          {
            "id": "precalculus.vectors.basics",
            "name": "Basics",
            "generator_id": "precalculus.vectors",
            "available": true
          },
          {
            "id": "precalculus.vectors.diagrams",
            "name": "Diagrams",
            "generator_id": "precalculus.vectors",
            "available": true
          },
          {
            "id": "precalculus.vectors.operations",
            "name": "Operations",
            "generator_id": "precalculus.vectors",
            "available": true
          },
          {
            "id": "precalculus.vectors.dot_products",
            "name": "Dot products",
            "generator_id": "precalculus.vectors",
            "available": true
          }
        ]
      },
      {
        "name": "Three-Dimensional Vectors",
        "topics": [
          {
            "id": "precalculus.three_dimension.points_in_three_dimension",
            "name": "Points in three dimensions",
            "generator_id": "precalculus.vectors",
            "available": true
          },
          {
            "id": "precalculus.three_dimension.basics",
            "name": "Basics",
            "generator_id": "precalculus.vectors",
            "available": true
          },
          {
            "id": "precalculus.three_dimension.operations",
            "name": "Operations",
            "generator_id": "precalculus.vectors",
            "available": true
          },
          {
            "id": "precalculus.three_dimension.cross_products",
            "name": "Cross products",
            "generator_id": "precalculus.vectors",
            "available": true
          }
        ]
      },
      {
        "name": "Matrices and Systems",
        "topics": [
          {
            "id": "precalculus.matrices_and_sy.operations",
            "name": "Operations",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "precalculus.matrices_and_sy.determinants",
            "name": "Determinants",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "precalculus.matrices_and_sy.inverses",
            "name": "Inverses",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "precalculus.matrices_and_sy.cramer_s_rule",
            "name": "Cramer's Rule",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "precalculus.matrices_and_sy.equations",
            "name": "Equations",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "precalculus.matrices_and_sy.multivariable_linear_syst",
            "name": "Multivariable linear systems and row operations",
            "generator_id": "precalculus.matrices",
            "available": true
          },
          {
            "id": "precalculus.matrices_and_sy.partial_fraction_decompos",
            "name": "Partial fraction decomposition",
            "generator_id": "precalculus.matrices",
            "available": true
          }
        ]
      },
      {
        "name": "Conic Sections",
        "topics": [
          {
            "id": "precalculus.conic_sections.parabolas_graphing_proper",
            "name": "Parabolas, graphing & properties",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.parabolas_writing_equatio",
            "name": "Parabolas, writing equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.circles_graphing_properti",
            "name": "Circles, graphing & properties",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.circles_writing_equations",
            "name": "Circles, writing equations",
            "generator_id": "geometry.circles",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.ellipses_graphing_propert",
            "name": "Ellipses, graphing & properties",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.ellipses_writing_equation",
            "name": "Ellipses, writing equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.hyperbolas_graphing_prope",
            "name": "Hyperbolas, graphing & properties",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.hyperbolas_writing_equati",
            "name": "Hyperbolas, writing equations",
            "generator_id": "precalculus.polar_conics",
            "available": true
          },
          {
            "id": "precalculus.conic_sections.rotations_of_conic_sectio",
            "name": "Rotations of conic sections",
            "generator_id": "precalculus.polar_conics",
            "available": true
          }
        ]
      },
      {
        "name": "Discrete Mathematics",
        "topics": [
          {
            "id": "precalculus.discrete_mathem.sample_spaces_and_the_fun",
            "name": "Sample spaces and The Fundamental Counting Principle",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.discrete_mathem.permutations",
            "name": "Permutations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.discrete_mathem.combinations",
            "name": "Combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.discrete_mathem.permutations_vs_combinati",
            "name": "Permutations vs combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.discrete_mathem.the_binomial_theorem",
            "name": "The Binomial Theorem",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "precalculus.discrete_mathem.mathematical_induction",
            "name": "Mathematical induction",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          }
        ]
      },
      {
        "name": "Probability",
        "topics": [
          {
            "id": "precalculus.probability.independent_and_dependent",
            "name": "Independent and dependent events, word problems",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.probability.independent_and_dependent",
            "name": "Independent and dependent events",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.probability.mutually_exclusive_events",
            "name": "Mutually exclusive events, word problems",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.probability.mutually_exclusive_events",
            "name": "Mutually exclusive events",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          },
          {
            "id": "precalculus.probability.with_permutations_and_com",
            "name": "With permutations and combinations",
            "generator_id": "algebra_2.probability_statistics",
            "available": true
          }
        ]
      },
      {
        "name": "Sequences and Series",
        "topics": [
          {
            "id": "precalculus.sequences_and_s.general_sequences",
            "name": "General sequences",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "precalculus.sequences_and_s.arithmetic_sequences",
            "name": "Arithmetic sequences",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "precalculus.sequences_and_s.geometric_sequences",
            "name": "Geometric sequences",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "precalculus.sequences_and_s.arithmetic_and_geometric_",
            "name": "Arithmetic and geometric mean",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "precalculus.sequences_and_s.general_series",
            "name": "General series",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "precalculus.sequences_and_s.arithmetic_series",
            "name": "Arithmetic series",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "precalculus.sequences_and_s.geometric_series",
            "name": "Geometric series",
            "generator_id": "precalculus.sequences",
            "available": true
          },
          {
            "id": "precalculus.sequences_and_s.power_series",
            "name": "Power series",
            "generator_id": "precalculus.sequences",
            "available": true
          }
        ]
      },
      {
        "name": "Introduction to Calculus",
        "topics": [
          {
            "id": "precalculus.introduction_to.limits_by_direct_evaluati",
            "name": "Limits by direct evaluation",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.limits_at_kinks_and_jumps",
            "name": "Limits at kinks and jumps",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.limits_at_removable_disco",
            "name": "Limits at removable discontinuities",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.limits_at_essential_disco",
            "name": "Limits at essential discontinuities",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.limits_at_infinity",
            "name": "Limits at infinity",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.definition_of_the_derivat",
            "name": "Definition of the derivative",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.instantaneous_rates_of_ch",
            "name": "Instantaneous rates of change",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.power_rule_for_differenti",
            "name": "Power rule for differentiation",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.motion_along_a_line",
            "name": "Motion along a line",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.approximating_area_under_",
            "name": "Approximating area under a curve",
            "generator_id": "calculus.riemann_sums",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.area_under_a_curve_by_lim",
            "name": "Area under a curve by limit of sums",
            "generator_id": "calculus.riemann_sums",
            "available": true
          },
          {
            "id": "precalculus.introduction_to.indefinite_integrals",
            "name": "Indefinite integrals",
            "generator_id": "calculus.integrals",
            "available": true
          }
        ]
      }
    ]
  },
  "calculus": {
    "title": "Calculus",
    "description": "Covers all of the fundamentals of Calculus: limits, continuity, differentiation, and integration as well as applications such as related rates and volume using cylindrical shells.",
    "categories": [
      {
        "name": "Limits",
        "topics": [
          {
            "id": "calculus.limits.by_direct_evaluation",
            "name": "By direct evaluation",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "calculus.limits.at_jump_discontinuities_a",
            "name": "At jump discontinuities and kinks",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "calculus.limits.at_removable_discontinuit",
            "name": "At removable discontinuities",
            "generator_id": "calculus.lhopital",
            "available": true
          },
          {
            "id": "calculus.limits.at_essential_discontinuit",
            "name": "At essential discontinuities",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "calculus.limits.at_infinity",
            "name": "At infinity",
            "generator_id": "calculus.lhopital",
            "available": true
          }
        ]
      },
      {
        "name": "Continuity",
        "topics": [
          {
            "id": "calculus.continuity.determining_and_classifyi",
            "name": "Determining and classifying",
            "generator_id": "calculus.limits",
            "available": true
          }
        ]
      },
      {
        "name": "Differentiation",
        "topics": [
          {
            "id": "calculus.differentiation.average_rates_of_change",
            "name": "Average rates of change",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.definition_of_the_derivat",
            "name": "Definition of the derivative",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.instantaneous_rates_of_ch",
            "name": "Instantaneous rates of change",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.power_rule",
            "name": "Power Rule",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.higher_order_derivatives",
            "name": "Higher order derivatives",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.product_rule",
            "name": "Product Rule",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.quotient_rule",
            "name": "Quotient Rule",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.chain_rule",
            "name": "Chain Rule",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.rules_using_tables",
            "name": "Rules, using tables",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.trigonometric",
            "name": "Trigonometric",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.inverse_trigonometric",
            "name": "Inverse trigonometric",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.natural_logarithms_and_ex",
            "name": "Natural logarithms and exponentials",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.other_base_logarithms_and",
            "name": "Other base logarithms and exponentials",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.logarithmic",
            "name": "Logarithmic",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.differentiation.implicit",
            "name": "Implicit",
            "generator_id": "calculus.implicit_diff",
            "available": true
          },
          {
            "id": "calculus.differentiation.inverse_functions",
            "name": "Inverse functions",
            "generator_id": "calculus.derivatives",
            "available": true
          }
        ]
      },
      {
        "name": "Applications of Differentiation",
        "topics": [
          {
            "id": "calculus.applications_of.slope_tangent_and_normal_",
            "name": "Slope, tangent, and normal lines",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.rolle_s_theorem",
            "name": "Rolle's Theorem",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.mean_value_theorem",
            "name": "Mean Value Theorem",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.intervals_of_increase_and",
            "name": "Intervals of increase and decrease",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.intervals_of_concavity",
            "name": "Intervals of concavity",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.relative_extrema",
            "name": "Relative extrema",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.absolute_extrema",
            "name": "Absolute extrema",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.optimization",
            "name": "Optimization",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.curve_sketching",
            "name": "Curve sketching",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.graphical_comparison_of_f",
            "name": "Graphical comparison of f, f', and f''",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.motion_along_a_line",
            "name": "Motion along a line",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.related_rates",
            "name": "Related rates",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.differentials",
            "name": "Differentials",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.newton_s_method",
            "name": "Newton's Method",
            "generator_id": "calculus.derivatives",
            "available": true
          },
          {
            "id": "calculus.applications_of.limits_in_form_of_definit",
            "name": "Limits in form of definition of derivative",
            "generator_id": "calculus.limits",
            "available": true
          },
          {
            "id": "calculus.applications_of.l_h_pital_s_rule",
            "name": "L'H\u00f4pital's Rule",
            "generator_id": "calculus.lhopital",
            "available": true
          }
        ]
      },
      {
        "name": "Indefinite Integration",
        "topics": [
          {
            "id": "calculus.indefinite_inte.power_rule",
            "name": "Power Rule",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.logarithmic_rule_and_expo",
            "name": "Logarithmic Rule and Exponentials",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.trigonometric",
            "name": "Trigonometric",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.inverse_trigonometric",
            "name": "Inverse trigonometric",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.power_rule_with_substitut",
            "name": "Power rule with substitution",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.logarithmic_rule_and_expo",
            "name": "Logarithmic rule and exponentials with subs.",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.trigonometric_with_substi",
            "name": "Trigonometric with substitution",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.inverse_trigonometric_wit",
            "name": "Inverse trigonometric with substitution",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.indefinite_inte.integration_by_parts",
            "name": "Integration by parts",
            "generator_id": "calculus.integrals",
            "available": true
          }
        ]
      },
      {
        "name": "Definite Integration",
        "topics": [
          {
            "id": "calculus.definite_integr.approximating_area_under_",
            "name": "Approximating area under a curve",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.definite_integr.area_under_a_curve_by_lim",
            "name": "Area under a curve by limit of sums",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.definite_integr.riemann_sum_tables",
            "name": "Riemann sum tables",
            "generator_id": "calculus.riemann_sums",
            "available": true
          },
          {
            "id": "calculus.definite_integr.first_fundamental_theorem",
            "name": "First Fundamental Theorem of Calculus",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.definite_integr.substitution_with_change_",
            "name": "Substitution with change of variables",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.definite_integr.mean_value_theorem",
            "name": "Mean Value Theorem",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.definite_integr.second_fundamental_theore",
            "name": "Second Fundamental Theorem of Calculus",
            "generator_id": "calculus.integrals",
            "available": true
          }
        ]
      },
      {
        "name": "Applications of Integration",
        "topics": [
          {
            "id": "calculus.applications_of.area_under_a_curve",
            "name": "Area under a curve",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.applications_of.area_between_curves",
            "name": "Area between curves",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.applications_of.volume_by_slicing_disks_a",
            "name": "Volume by slicing, disks and washers",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.applications_of.volume_by_cylinders",
            "name": "Volume by cylinders",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.applications_of.volume_of_solids_with_kno",
            "name": "Volume of solids with known cross sections",
            "generator_id": "calculus.integrals",
            "available": true
          },
          {
            "id": "calculus.applications_of.motion_along_a_line_revis",
            "name": "Motion along a line revisited",
            "generator_id": "calculus.integrals",
            "available": true
          }
        ]
      },
      {
        "name": "Differential Equations",
        "topics": [
          {
            "id": "calculus.differential_eq.slope_fields",
            "name": "Slope fields",
            "generator_id": "calculus.diff_eq",
            "available": true
          },
          {
            "id": "calculus.differential_eq.introduction",
            "name": "Introduction",
            "generator_id": "calculus.diff_eq",
            "available": true
          },
          {
            "id": "calculus.differential_eq.separable",
            "name": "Separable",
            "generator_id": "calculus.diff_eq",
            "available": true
          },
          {
            "id": "calculus.differential_eq.exponential_growth_and_de",
            "name": "Exponential growth and decay",
            "generator_id": "calculus.diff_eq",
            "available": true
          }
        ]
      }
    ]
  },
  "grade_6": {
    "title": "Grade 6 Math",
    "description": "Covers all typical material found in sixth grade, over 90 topics focusing on real-world problems and visual diagrams.",
    "categories": [
      {
        "name": "Ratios",
        "topics": [
          {
            "id": "grade_6.ratios.introduction_to_ratios",
            "name": "Introduction to ratios",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.ratios.equivalent_ratios",
            "name": "Equivalent ratios",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.ratios.part_part_whole_ratios",
            "name": "Part-part-whole ratios",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.ratios.comparing_ratios",
            "name": "Comparing ratios",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          }
        ]
      },
      {
        "name": "Rates",
        "topics": [
          {
            "id": "grade_6.rates.unit_rates_and_equivalent",
            "name": "Unit rates and equivalent rates",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.rates.comparing_rates",
            "name": "Comparing rates",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.rates.converting_units",
            "name": "Converting units",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          }
        ]
      },
      {
        "name": "Percents",
        "topics": [
          {
            "id": "grade_6.percents.introduction_to_percents",
            "name": "Introduction to percents",
            "generator_id": "grade_6.percents",
            "available": true
          },
          {
            "id": "grade_6.percents.relating_percents_fractio",
            "name": "Relating percents, fractions, and decimals",
            "generator_id": "grade_6.percents",
            "available": true
          },
          {
            "id": "grade_6.percents.finding_percents_with_equ",
            "name": "Finding percents with equivalent fractions",
            "generator_id": "grade_6.percents",
            "available": true
          },
          {
            "id": "grade_6.percents.solving_percent_problems_",
            "name": "Solving percent problems with diagrams",
            "generator_id": "grade_6.percents",
            "available": true
          },
          {
            "id": "grade_6.percents.solving_percent_problems_",
            "name": "Solving percent problems with formulas",
            "generator_id": "grade_6.percents",
            "available": true
          }
        ]
      },
      {
        "name": "Dividing Fractions",
        "topics": [
          {
            "id": "grade_6.dividing_fracti.how_many_groups_times",
            "name": "How many groups/times?",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.dividing_fracti.what_fraction_of_a_whole",
            "name": "What fraction of a whole?",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.dividing_fracti.how_much_in_each_group_ti",
            "name": "How much in each group/time?",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.dividing_fracti.dividing_fractions",
            "name": "Dividing fractions",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          }
        ]
      },
      {
        "name": "Decimal Arithmetic",
        "topics": [
          {
            "id": "grade_6.decimal_arithme.decimal_addition_with_dia",
            "name": "Decimal addition with diagrams",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.decimal_addition",
            "name": "Decimal addition",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.decimal_subtraction_with_",
            "name": "Decimal subtraction with diagrams",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.decimal_subtraction",
            "name": "Decimal subtraction",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.decimal_multiplication_wi",
            "name": "Decimal multiplication with equivalent fractions",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.decimal_multiplication_wi",
            "name": "Decimal multiplication with area diagrams",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.decimal_multiplication",
            "name": "Decimal multiplication",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.long_division_with_remain",
            "name": "Long division with remainders",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.dividing_whole_numbers_th",
            "name": "Dividing whole numbers that result in decimals",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.dividing_decimals_by_whol",
            "name": "Dividing decimals by whole numbers",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.dividing_whole_numbers_by",
            "name": "Dividing whole numbers by decimals",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.decimal_arithme.dividing_decimals_by_deci",
            "name": "Dividing decimals by decimals",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          }
        ]
      },
      {
        "name": "Common Factors and Common Multiples",
        "topics": [
          {
            "id": "grade_6.common_factors_.factoring",
            "name": "Factoring",
            "generator_id": "grade_6.factors_multiples",
            "available": true
          },
          {
            "id": "grade_6.common_factors_.greatest_common_factor",
            "name": "Greatest common factor",
            "generator_id": "grade_6.factors_multiples",
            "available": true
          },
          {
            "id": "grade_6.common_factors_.least_common_multiple",
            "name": "Least common multiple",
            "generator_id": "grade_6.factors_multiples",
            "available": true
          },
          {
            "id": "grade_6.common_factors_.gcf_and_lcm_word_problems",
            "name": "GCF and LCM word problems",
            "generator_id": "grade_6.factors_multiples",
            "available": true
          }
        ]
      },
      {
        "name": "Negative Numbers and Absolute Value",
        "topics": [
          {
            "id": "grade_6.negative_number.numbers_on_a_number_line",
            "name": "Numbers on a number line",
            "generator_id": "grade_6.integers",
            "available": true
          },
          {
            "id": "grade_6.negative_number.number_line_word_problems",
            "name": "Number line word problems",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.negative_number.opposites_of_numbers",
            "name": "Opposites of numbers",
            "generator_id": "grade_6.integers",
            "available": true
          },
          {
            "id": "grade_6.negative_number.comparing_numbers",
            "name": "Comparing numbers",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.negative_number.ordering_numbers",
            "name": "Ordering numbers",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.negative_number.absolute_values",
            "name": "Absolute values",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.negative_number.comparing_with_absolute_v",
            "name": "Comparing with absolute values",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.negative_number.ordering_with_absolute_va",
            "name": "Ordering with absolute values",
            "generator_id": "grade_6.one_step",
            "available": true
          }
        ]
      },
      {
        "name": "Coordinate Plane",
        "topics": [
          {
            "id": "grade_6.coordinate_plan.points_on_the_coordinate_",
            "name": "Points on the coordinate plane",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.coordinate_plan.distances_on_the_coordina",
            "name": "Distances on the coordinate plane",
            "generator_id": "geometry.coordinate_geometry",
            "available": true
          },
          {
            "id": "grade_6.coordinate_plan.shapes_and_perimeter_on_t",
            "name": "Shapes and perimeter on the coordinate plane",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.coordinate_plan.distances_word_problems",
            "name": "Distances, word problems",
            "generator_id": "grade_6.one_step",
            "available": true
          }
        ]
      },
      {
        "name": "Numeric Expressions, Exponents, and the Order of Operations",
        "topics": [
          {
            "id": "grade_6.numeric_express.writing_numeric_expressio",
            "name": "Writing numeric expressions",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.numeric_express.numeric_expressions_with_",
            "name": "Numeric expressions with exponents",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.numeric_express.properties_of_addition_an",
            "name": "Properties of addition and multiplication",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.numeric_express.numeric_expressions_and_t",
            "name": "Numeric expressions and the order of operations",
            "generator_id": "grade_6.order_of_operations",
            "available": true
          },
          {
            "id": "grade_6.numeric_express.distributive_property_wit",
            "name": "Distributive property with area diagrams, numeric",
            "generator_id": "algebra_1.distributive_property",
            "available": true
          },
          {
            "id": "grade_6.numeric_express.distributive_property_num",
            "name": "Distributive property, numeric",
            "generator_id": "algebra_1.distributive_property",
            "available": true
          }
        ]
      },
      {
        "name": "Variables and Algebraic Expressions",
        "topics": [
          {
            "id": "grade_6.variables_and_a.writing_algebraic_express",
            "name": "Writing algebraic expressions",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.variables_and_a.evaluating_algebraic_expr",
            "name": "Evaluating algebraic expressions",
            "generator_id": "grade_6.one_step",
            "available": true
          }
        ]
      },
      {
        "name": "Equivalent Expressions",
        "topics": [
          {
            "id": "grade_6.equivalent_expr.combining_like_terms",
            "name": "Combining like terms",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.equivalent_expr.distributive_property_wit",
            "name": "Distributive property with area diagrams, algebraic",
            "generator_id": "algebra_1.distributive_property",
            "available": true
          },
          {
            "id": "grade_6.equivalent_expr.distributive_property_alg",
            "name": "Distributive property, algebraic",
            "generator_id": "algebra_1.distributive_property",
            "available": true
          }
        ]
      },
      {
        "name": "Equations",
        "topics": [
          {
            "id": "grade_6.equations.solutions_to_equations",
            "name": "Solutions to equations",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.equations.tape_diagrams",
            "name": "Tape diagrams",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.equations.hanger_diagrams",
            "name": "Hanger diagrams",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.equations.equations_word_problems",
            "name": "Equations word problems",
            "generator_id": "grade_6.one_step",
            "available": true
          }
        ]
      },
      {
        "name": "Inequalities",
        "topics": [
          {
            "id": "grade_6.inequalities.solutions_to_inequalities",
            "name": "Solutions to inequalities",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.inequalities.writing_and_graphing_ineq",
            "name": "Writing and graphing inequalities",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.inequalities.inequalities_word_problem",
            "name": "Inequalities word problems",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "grade_6.inequalities.solving_and_graphing_one_",
            "name": "Solving and graphing one-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "grade_6.inequalities.hanger_diagrams",
            "name": "Hanger diagrams",
            "generator_id": "grade_6.one_step",
            "available": true
          }
        ]
      },
      {
        "name": "Equations as Relationships between Two Variables",
        "topics": [
          {
            "id": "grade_6.equations_as_re.equivalent_ratio_equation",
            "name": "Equivalent ratio equations",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.equations_as_re.constant_rate_equations",
            "name": "Constant rate equations",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          },
          {
            "id": "grade_6.equations_as_re.equations_for_other_relat",
            "name": "Equations for other relationships",
            "generator_id": "grade_6.one_step",
            "available": true
          }
        ]
      },
      {
        "name": "Polygons",
        "topics": [
          {
            "id": "grade_6.polygons.parallelograms_understand",
            "name": "Parallelograms, understanding area formula",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polygons.parallelograms",
            "name": "Parallelograms",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polygons.triangles_understanding_a",
            "name": "Triangles, understanding area formula",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polygons.triangles",
            "name": "Triangles",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polygons.trapezoids",
            "name": "Trapezoids",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polygons.kites",
            "name": "Kites",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polygons.polygons_on_a_grid_or_coo",
            "name": "Polygons on a grid or coordinate plane",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polygons.polygons_and_shaded_regio",
            "name": "Polygons and shaded regions",
            "generator_id": "geometry.area_volume",
            "available": true
          }
        ]
      },
      {
        "name": "Polyhedra",
        "topics": [
          {
            "id": "grade_6.polyhedra.classifying_and_naming",
            "name": "Classifying and naming",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polyhedra.nets",
            "name": "Nets",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polyhedra.nets_and_surface_area",
            "name": "Nets and surface area",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polyhedra.nets_and_surface_area_on_",
            "name": "Nets and surface area on a grid",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polyhedra.identifying_invalid_nets",
            "name": "Identifying invalid nets",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polyhedra.volume_and_surface_area_u",
            "name": "Volume and surface area using isometric drawings",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polyhedra.formulas_for_volume_and_s",
            "name": "Formulas for volume and surface area of a cube",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "grade_6.polyhedra.isometric_sketching",
            "name": "Isometric sketching",
            "generator_id": "geometry.area_volume",
            "available": true
          }
        ]
      },
      {
        "name": "Area and Volume with Fractions",
        "topics": [
          {
            "id": "grade_6.area_and_volume.rectangles_with_fraction_",
            "name": "Rectangles with fraction side lengths",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.area_and_volume.triangles_with_fraction_s",
            "name": "Triangles with fraction side lengths",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          },
          {
            "id": "grade_6.area_and_volume.right_rectangular_prisms_",
            "name": "Right rectangular prisms with fraction side lengths",
            "generator_id": "grade_6.fractions_decimals",
            "available": true
          }
        ]
      },
      {
        "name": "Data Sets and Distributions",
        "topics": [
          {
            "id": "grade_6.data_sets_and_d.interpreting_dot_plots",
            "name": "Interpreting dot plots",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "grade_6.data_sets_and_d.drawing_dot_plots",
            "name": "Drawing dot plots",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "grade_6.data_sets_and_d.interpreting_histograms",
            "name": "Interpreting histograms",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "grade_6.data_sets_and_d.drawing_histograms",
            "name": "Drawing histograms",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "grade_6.data_sets_and_d.center_and_spread",
            "name": "Center and spread",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "grade_6.data_sets_and_d.interpreting_box_plots",
            "name": "Interpreting box plots",
            "generator_id": "grade_6.statistics",
            "available": true
          },
          {
            "id": "grade_6.data_sets_and_d.drawing_box_plots",
            "name": "Drawing box plots",
            "generator_id": "grade_6.statistics",
            "available": true
          }
        ]
      }
    ]
  },
  "pre_algebra": {
    "title": "Pre-Algebra",
    "description": "Fractions, integers, decimals, simple one/two step equations, inequalities, graphs, and proportions.",
    "categories": [
      {
        "name": "Arithmetic & Number Properties",
        "topics": [
          {
            "id": "pre_algebra.arithmetic_numb.adding_and_subtracting_in",
            "name": "Adding and subtracting integers",
            "generator_id": "grade_6.integers",
            "available": true
          },
          {
            "id": "pre_algebra.arithmetic_numb.multiplying_and_dividing_",
            "name": "Multiplying and dividing integers",
            "generator_id": "grade_6.integers",
            "available": true
          },
          {
            "id": "pre_algebra.arithmetic_numb.order_of_operations_with_",
            "name": "Order of operations with integers",
            "generator_id": "grade_6.order_of_operations",
            "available": true
          },
          {
            "id": "pre_algebra.arithmetic_numb.evaluating_variable_expre",
            "name": "Evaluating variable expressions",
            "generator_id": "grade_6.order_of_operations",
            "available": true
          },
          {
            "id": "pre_algebra.arithmetic_numb.the_distributive_property",
            "name": "The Distributive Property",
            "generator_id": "algebra_1.distributive_property",
            "available": true
          }
        ]
      },
      {
        "name": "Equations",
        "topics": [
          {
            "id": "pre_algebra.equations.one_step_equations",
            "name": "One-step equations",
            "generator_id": "grade_6.one_step",
            "available": true
          },
          {
            "id": "pre_algebra.equations.two_step_equations",
            "name": "Two-step equations",
            "generator_id": "algebra_1.two_step",
            "available": true
          },
          {
            "id": "pre_algebra.equations.multi_step_equations",
            "name": "Multi-step equations",
            "generator_id": "algebra_1.multi_step",
            "available": true
          },
          {
            "id": "pre_algebra.equations.equations_with_variables_",
            "name": "Equations with variables on both sides",
            "generator_id": "algebra_1.multi_step",
            "available": true
          },
          {
            "id": "pre_algebra.equations.solving_proportions",
            "name": "Solving proportions",
            "generator_id": "grade_6.ratios_rates",
            "available": true
          }
        ]
      },
      {
        "name": "Inequalities",
        "topics": [
          {
            "id": "pre_algebra.inequalities.one_step_inequalities",
            "name": "One-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "pre_algebra.inequalities.two_step_inequalities",
            "name": "Two-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "pre_algebra.inequalities.multi_step_inequalities",
            "name": "Multi-step inequalities",
            "generator_id": "algebra_1.inequalities",
            "available": true
          },
          {
            "id": "pre_algebra.inequalities.graphing_inequalities_on_",
            "name": "Graphing inequalities on a number line",
            "generator_id": "algebra_1.inequalities",
            "available": true
          }
        ]
      },
      {
        "name": "Linear Relations & Graphing",
        "topics": [
          {
            "id": "pre_algebra.linear_relation.points_on_the_coordinate_",
            "name": "Points on the coordinate plane",
            "generator_id": "algebra_1.linear_equations",
            "available": true
          },
          {
            "id": "pre_algebra.linear_relation.finding_slope_from_a_grap",
            "name": "Finding slope from a graph",
            "generator_id": "algebra_1.slope",
            "available": true
          },
          {
            "id": "pre_algebra.linear_relation.finding_slope_from_two_po",
            "name": "Finding slope from two points",
            "generator_id": "algebra_1.slope",
            "available": true
          },
          {
            "id": "pre_algebra.linear_relation.graphing_linear_equations",
            "name": "Graphing linear equations",
            "generator_id": "algebra_1.graphing_lines",
            "available": true
          },
          {
            "id": "pre_algebra.linear_relation.writing_slope_intercept_f",
            "name": "Writing slope-intercept form",
            "generator_id": "algebra_1.writing_linear_equations",
            "available": true
          }
        ]
      },
      {
        "name": "Geometry Foundations",
        "topics": [
          {
            "id": "pre_algebra.geometry_founda.the_pythagorean_theorem",
            "name": "The Pythagorean Theorem",
            "generator_id": "geometry.pythagorean",
            "available": true
          },
          {
            "id": "pre_algebra.geometry_founda.area_and_perimeter_of_rec",
            "name": "Area and perimeter of rectangles and triangles",
            "generator_id": "geometry.angles_lines",
            "available": true
          },
          {
            "id": "pre_algebra.geometry_founda.volume_of_rectangular_pri",
            "name": "Volume of rectangular prisms",
            "generator_id": "geometry.area_volume",
            "available": true
          },
          {
            "id": "pre_algebra.geometry_founda.angles_and_triangles",
            "name": "Angles and triangles",
            "generator_id": "geometry.angles_lines",
            "available": true
          }
        ]
      }
    ]
  }
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
