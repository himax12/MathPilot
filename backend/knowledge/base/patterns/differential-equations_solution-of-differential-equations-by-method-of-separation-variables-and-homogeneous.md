---
chapter: differential-equations
topic: solution-of-differential-equations-by-method-of-separation-variables-and-homogeneous
jee_frequency: 17
years_appeared: [2002, 2004, 2005, 2010, 2011, 2012, 2013, 2014, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 106
difficulty: medium
---

# Differential Equations: Solution Of Differential Equations By Method Of Separation Variables And Homogeneous

**JEE Frequency**: 17 years | **Questions**: 106

## Differential Equations: Separation of Variables & Homogeneous - JEE Knowledge Base

**JEE Frequency:** High (17 years, 106 questions)

**1. Pattern Recognition:**

*   **Separation of Variables:** Equation can be written in the form  `f(y) dy = g(x) dx`. The key is isolating y terms with dy and x terms with dx.
*   **Homogeneous DE:** Equation can be expressed as  `dy/dx = f(y/x)`. This implies `f(tx, ty) = f(x, y)` for all t. Look for y/x terms directly or expressions that can be manipulated to form them.

**2. Core Formulas:**

*   **Separation of Variables:** Integrate both sides after separating: `∫f(y) dy = ∫g(x) dx + C`.
*   **Homogeneous Substitution:** `y = vx` , `dy/dx = v + x(dv/dx)`
*   **Integrating Factor for Linear DE (related, often combined):** For `dy/dx + P(x)y = Q(x)`, the integrating factor (IF) is: `IF = e^{∫P(x) dx}`. Solution is: `y * IF = ∫(Q(x) * IF) dx + C`

**3. Standard Approach:**

1.  **Identify:** Determine if the equation is separable or homogeneous.
2.  **Separate (Separable):**  Rewrite the equation in the form `f(y) dy = g(x) dx`.
3.  **Substitute (Homogeneous):** Let `y = vx` and `dy/dx = v + x(dv/dx)`. Simplify and separate variables.
4.  **Integrate:** Integrate both sides of the separated equation.
5.  **Solve for y:** Express the solution explicitly as `y = f(x)` or implicitly as `F(x, y) = C`. Use initial conditions to find C.

**4. Quick Tips:**

*   **Check options:**  Differentiate answer choices and see if it matches the given differential equation.  Very efficient if the question doesn't ask for a general solution.
*   **Homogenization Trick:** If the powers of x and y in each term are the same, consider it a clue towards homogeneity.

**5. Common Mistakes:**

*   **Forgetting the Constant of Integration (+C):** Essential for general solutions.
*   **Incorrect Integration:** Review standard integration formulas, especially trigonometric and logarithmic integrals.
*   **Algebraic Errors:** Pay close attention to signs and simplification during variable separation and substitution. In homogenous DEs always make sure to go back to the original variable after integrating.
