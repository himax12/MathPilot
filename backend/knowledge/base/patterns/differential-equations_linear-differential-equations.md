---
chapter: differential-equations
topic: linear-differential-equations
jee_frequency: 14
years_appeared: [2003, 2008, 2011, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 95
difficulty: medium
---

# Differential Equations: Linear Differential Equations

**JEE Frequency**: 14 years | **Questions**: 95

## Linear Differential Equations: JEE Knowledge Base

**JEE Frequency:** High (14 years, 95 questions)

**1. Pattern Recognition:**

*   Differential equation can be expressed in the form $\frac{dy}{dx} + P(x)y = Q(x)$ or $\frac{dx}{dy} + P(y)x = Q(y)$.
*   Often requires rearrangement or simplification to reach the standard linear form.
*   Presence of terms like $y, dy/dx$ (or $x, dx/dy$) and functions of *x* (or *y*) only are clues.

**2. Core Formulas:**

*   **Standard Form 1:** $\frac{dy}{dx} + P(x)y = Q(x)$
*   **Standard Form 2:** $\frac{dx}{dy} + P(y)x = Q(y)$
*   **Integrating Factor (IF) for Form 1:** $IF = e^{\int P(x) dx}$
*   **Integrating Factor (IF) for Form 2:** $IF = e^{\int P(y) dy}$
*   **Solution for Form 1:** $y(IF) = \int Q(x) (IF) dx + C$
*   **Solution for Form 2:** $x(IF) = \int Q(y) (IF) dy + C$

**3. Standard Approach:**

1.  Rewrite the given differential equation in either standard form:  $\frac{dy}{dx} + P(x)y = Q(x)$ or $\frac{dx}{dy} + P(y)x = Q(y)$.
2.  Identify $P(x)$ (or $P(y)$) and calculate the Integrating Factor (IF).
3.  Multiply the standard form equation by the IF.
4.  Integrate both sides using the solution formulas, remembering the constant of integration *C*.
5.  Use the given initial condition (e.g., y(1) = 1) to find the value of *C*.

**4. Quick Tips:**

*   **Bernoulli's Equation:** Equations of the form $\frac{dy}{dx} + P(x)y = Q(x)y^n$ can be reduced to linear form by substituting $z = y^{1-n}$.
*   **Spotting Perfect Derivatives:**  Sometimes, after multiplying by an IF, the LHS becomes a perfect derivative (e.g., $\frac{d}{dx}(xy)$). Directly integrate if possible.

**5. Common Mistakes:**

*   **Incorrectly Identifying P(x) and Q(x):** Double-check the standard form before calculating the IF. Sign errors are frequent.
*   **Forgetting the Constant of Integration (C):**  *C* is crucial for finding the particular solution using the initial condition.
*   **Incorrect Integration:** Carefully perform the integration, especially when dealing with trigonometric or logarithmic functions.
