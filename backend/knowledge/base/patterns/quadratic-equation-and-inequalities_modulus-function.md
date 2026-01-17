---
chapter: quadratic-equation-and-inequalities
topic: modulus-function
jee_frequency: 10
years_appeared: [2002, 2003, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 22
difficulty: medium
---

# Quadratic Equation And Inequalities: Modulus Function

**JEE Frequency**: 10 years | **Questions**: 22

## Quadratic Equation & Inequalities: Modulus Function - JEE Knowledge Base

**JEE Frequency (10 Years): High (22 Questions)**

**1. Pattern Recognition:**

*   Presence of `|x|`, `|f(x)|`, or `|g(x)|` within a quadratic or related equation.
*   The expression inside the modulus (e.g., `x`, `sqrt(x) - 2`, `2^x - 1`) often appears elsewhere in the equation, facilitating substitution.
*   Look for symmetry around the origin, especially when dealing with `|x|`.

**2. Core Formulas:**

*   Definition of Modulus:  $|x| = \begin{cases} x, & \text{if } x \ge 0 \\ -x, & \text{if } x < 0 \end{cases}$
*   $|x|^2 = x^2$
*   $|f(x)| = a \Rightarrow f(x) = a \text{ or } f(x) = -a$ (where $a \ge 0$)
*   $\sqrt{x^2} = |x|$
*   $|a \cdot b| = |a| \cdot |b|$

**3. Standard Approach:**

1.  **Identify the Modulus:** Pinpoint the expression within the modulus function.
2.  **Case-wise Analysis:**  Create cases based on the sign of the expression inside the modulus.
    *   Case 1:  `f(x) >= 0`: Replace `|f(x)|` with `f(x)`.
    *   Case 2:  `f(x) < 0`: Replace `|f(x)|` with `-f(x)`.
3.  **Solve the Equations:** Solve the resulting equation in each case.
4.  **Check Validity:** Crucially, check if the solutions obtained in each case satisfy the initial assumption for that case (e.g., if you solved with `x >= 0`, discard any negative solutions).
5.  **Combine Solutions:** The complete solution set is the union of the valid solutions from all cases.

**4. Quick Tips:**

*   **Substitution:** If `|f(x)|` and `f(x)` both appear, substitute `y = |f(x)|` to simplify the equation into a form solvable through substitution.
*   **Graphical Approach:** Sketching the graph of `y = f(x)` and reflecting the part below the x-axis above it helps visualize the solutions of `y = |f(x)|`. This is particularly useful for equations like  `|f(x)| = g(x)`.
*   **Symmetry:** If the equation only involves even powers of `x` and `|x|`, explore symmetry.  Usually, if `x = a` is a solution, then `x = -a` is also a solution.

**5. Common Mistakes:**

*   **Forgetting to Check Validity:**  The most common error. Always verify that your solutions satisfy the assumptions made for each case.
*   **Ignoring the Modulus Sign:**  Treating `|x|` as just `x` without considering the negative case.
*   **Incorrectly Squaring:** When squaring both sides of an equation involving modulus, remember that squaring removes the sign information. Be careful about introducing extraneous roots.  For instance, if you have  `|x| = a`,  squaring leads to `x^2 = a^2`, which means `x = ±a`. Don't only consider one solution.
