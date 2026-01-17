---
chapter: definite-integration
topic: newton-lebnitz-rule-of-differentiation
jee_frequency: 10
years_appeared: [2003, 2005, 2016, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 37
difficulty: medium
---

# Definite Integration: Newton Lebnitz Rule Of Differentiation

**JEE Frequency**: 10 years | **Questions**: 37

## Newton-Leibniz Rule of Differentiation: JEE Knowledge Base

**JEE Frequency:** High (37 questions in 10 years indicates a frequently tested concept)

**1. Pattern Recognition:**

*   Presence of a definite integral where the limits are functions of the variable with respect to which differentiation is required.  Look for phrases like "differentiating with respect to x" after an integral sign.
*   The question often asks for a derivative, a limit involving the derivative, or the value of a function obtained after differentiating the integral.
*  Problems may involve finding a function defined in terms of integral with variable limits.

**2. Core Formulas:**

*   **Newton-Leibniz Rule:**
    \[\frac{d}{dx} \int_{g(x)}^{h(x)} f(t) \, dt = f(h(x)) \cdot h'(x) - f(g(x)) \cdot g'(x)\]
*   **Leibniz Rule with Constant Lower Limit:**
    \[\frac{d}{dx} \int_{a}^{h(x)} f(t) \, dt = f(h(x)) \cdot h'(x)\]  (where 'a' is a constant)
*   **L'Hopital's Rule (often used in conjunction):**
    \[\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}\] (if the limit is in indeterminate form, such as 0/0 or ∞/∞)

**3. Standard Approach:**

1.  **Identify the Integral:** Isolate the integral with variable limits.
2.  **Apply Newton-Leibniz:**  Differentiate both sides of the equation with respect to the relevant variable using the appropriate form of the Newton-Leibniz rule.
3.  **Simplify:** Simplify the resulting equation after differentiation.
4.  **Solve/Evaluate:** Solve for the desired derivative or use the differentiated form to evaluate the limit using L'Hopital's rule if necessary.
5. **Apply Initial value(s) if any**: Plug in given point and derivative values in equation to eliminate integration constant.

**4. Quick Tips:**

*   **Chain Rule Awareness:** Remember to multiply by the derivative of the upper and lower limits (h'(x) and g'(x)).
*   **L'Hopital's Rule Trigger:** If you get an indeterminate form (0/0 or ∞/∞) when directly substituting into the limit, immediately think about using L'Hopital's rule *after* applying the Newton-Leibniz rule.

**5. Common Mistakes:**

*   **Forgetting to Multiply by Derivative of Limits:** The most common mistake is omitting the `h'(x)` and `g'(x)` terms.
*   **Incorrect Application of L'Hopital's Rule:** Applying L'Hopital's rule *before* differentiating the integral using Newton-Leibniz. Differentiation is key.
*   **Treating x as Constant Inside Integral:** When differentiating, remember 'x' inside the limits of integral are variables. Do not treat them as a constant.
