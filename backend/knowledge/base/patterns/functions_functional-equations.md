---
chapter: functions
topic: functional-equations
jee_frequency: 11
years_appeared: [2003, 2005, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 39
difficulty: medium
---

# Functions: Functional Equations

**JEE Frequency**: 11 years | **Questions**: 39

## Functional Equations: JEE Knowledge Base

**JEE Frequency:** 11 years
**Question Count:** 39

**1. Pattern Recognition:**

*   Presence of an equation relating the function's value at one or more points to its values at other points. Common forms include: `f(x+y)`, `f(x-y)`, `f(xy)`, `f(1/x)`.
*   Equation must hold for *all* or a *specified domain* of the variables (e.g., all real numbers, integers, positive reals).

**2. Core Formulas:**

*   **Cauchy's Functional Equation:** If `f(x+y) = f(x) + f(y)` for all x, y in R, then:
    *   `f(x) = cx` if `f` is continuous, where `c = f(1)`.
    *   `f(nx) = nf(x)` for all `n` in integers.
*   **Exponential Functional Equation:** If `f(x+y) = f(x)f(y)` for all x, y in R, then:
    *   `f(x) = a^x` if `f` is continuous, where `a = f(1)`.
*   **General Strategy Formula:**
    * if `f(x) + af(1/x) = g(x)`, find values for `f(x)` and `f(1/x)` by swapping `x` and `1/x` in the equation, creating a system of equations to solve.

**3. Standard Approach:**

1.  **Substitution:** Substitute specific values for variables (e.g., x=0, y=0, x=1, y=1, x=y, x=-y) to simplify the equation and find initial values or relationships.
2.  **Iteration:**  Apply the functional equation repeatedly. Look for patterns that emerge after multiple iterations.
3.  **Guess and Verify:** Based on the form of the equation, guess a solution (e.g., linear, quadratic, exponential) and verify if it satisfies the equation.
4.  **Differentiability (Advanced):** If the function is assumed or known to be differentiable, differentiate both sides of the equation with respect to one variable and solve the resulting differential equation (less frequent in JEE).
5. **Constructing new functions:** If given `f(x+y)`, try constructing new function `g(x) = e^{f(x)}`, or `g(x) = sin(f(x))` etc.

**4. Quick Tips:**

*   Look for symmetry. If the equation is symmetric in `x` and `y`, consider substitutions like `x = y`.
*   If the domain is restricted (e.g., only natural numbers), try using mathematical induction.

**5. Common Mistakes:**

*   **Assuming continuity without proof:** Cauchy's functional equation has non-continuous solutions if continuity is not given.
*   **Not verifying the solution:** Always check if the found function satisfies the original functional equation, especially if you guessed a solution.
*   **Incorrectly applying substitutions:** Carefully substitute the values into the equation, paying attention to the order of operations.
