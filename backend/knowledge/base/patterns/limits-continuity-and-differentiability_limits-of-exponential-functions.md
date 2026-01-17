---
chapter: limits-continuity-and-differentiability
topic: limits-of-exponential-functions
jee_frequency: 9
years_appeared: [2002, 2004, 2016, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 22
difficulty: medium
---

# Limits Continuity And Differentiability: Limits Of Exponential Functions

**JEE Frequency**: 9 years | **Questions**: 22

## Limits of Exponential Functions: JEE Knowledge Base

**JEE Frequency:** 9 years
**Question Count:** 22 questions

This document focuses on evaluating limits involving exponential functions, a frequent topic in JEE.

**1. Pattern Recognition:**

*   Functions of the form  $$[f(x)]^{g(x)}$$ where  $$f(x) \to 1$$ and $$g(x) \to \infty$$ as  $$x \to a$$ (or  $$x \to \infty$$). This is the $$1^\infty$$ indeterminate form.
*   Presence of exponential terms like  $$e^{f(x)}$$  and the need to simplify exponents before directly applying limit theorems.

**2. Core Formulas:**

*   $$\lim_{x \to 0} \frac{e^x - 1}{x} = 1$$
*   $$\lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x = e$$
*   $$\lim_{x \to 0} (1+x)^{1/x} = e$$
*   $$\lim_{x \to a} [f(x)]^{g(x)} = e^{\lim_{x \to a} [f(x)-1]g(x)}$$ when  $$\lim_{x \to a} f(x) = 1$$  and  $$\lim_{x \to a} g(x) = \infty$$
*   $$\lim_{x \to \infty} \left(1 + \frac{a}{x} + \frac{b}{x^2} + ... \right)^{cx} = e^{\lim_{x\to \infty} c \cdot (a + b/x + ...)} = e^{ac}$$

**3. Standard Approach:**

1.  **Identify the Form:** Check if the limit is of the form $$1^\infty$$.
2.  **Rewrite:** Express the limit as  $$L = \lim_{x \to a} [f(x)]^{g(x)}$$.
3.  **Apply the Formula:** Use the formula  $$L = e^{\lim_{x \to a} [f(x)-1]g(x)}$$.
4.  **Simplify and Evaluate:** Simplify the exponent using algebraic manipulation, series expansions (if required), and standard limit results.
5.  **Solve for Unknowns:** If the limit is given and contains unknowns, equate the evaluated limit with the given value and solve for the unknowns.

**4. Quick Tips:**

*   For limits at infinity of rational functions raised to some power, focus on the leading coefficients and powers of *x*.
*   Recognize and use standard series expansions when limits involve trigonometric or exponential functions near zero (e.g., $$e^x \approx 1+x$$ for small *x*).

**5. Common Mistakes:**

*   **Incorrectly identifying the indeterminate form:** Make sure that $$f(x) \to 1$$ and $$g(x) \to \infty$$ simultaneously.
*   **Forgetting to apply the exponential:** Remember to take *e* to the power of the calculated limit of the exponent.
*   **Algebraic errors:** Careful simplification of the expression inside the limit is crucial. Miscalculations can lead to a completely wrong answer.
