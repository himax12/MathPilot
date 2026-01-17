---
chapter: limits-continuity-and-differentiability
topic: continuity
jee_frequency: 15
years_appeared: [2002, 2004, 2007, 2011, 2012, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 60
difficulty: medium
---

# Limits Continuity And Differentiability: Continuity

**JEE Frequency**: 15 years | **Questions**: 60

## Continuity: JEE Knowledge Base

**JEE Frequency:** High (60 questions in 15 years)

**1. Pattern Recognition:**

*   Functions defined piecewise, especially with different expressions for different intervals or at specific points.
*   Questions asking about the value of a function at a point to ensure continuity, or to find parameters that make the function continuous.
*   Involvement of standard functions like trigonometric functions, exponential functions, and greatest integer functions, often combined to create discontinuity.

**2. Core Formulas:**

*   Definition of Continuity at a point `x = a`:  $$\lim_{x \to a^-} f(x) = \lim_{x \to a^+} f(x) = f(a)$$
*   Left-Hand Limit (LHL):  $$\lim_{x \to a^-} f(x) = \lim_{h \to 0} f(a - h)$$
*   Right-Hand Limit (RHL): $$\lim_{x \to a^+} f(x) = \lim_{h \to 0} f(a + h)$$
*   Continuity of Standard Functions: Polynomials, exponential functions, sine, and cosine functions are continuous on their domains.  Be cautious of tan(x), cot(x), sec(x), and csc(x) due to potential discontinuities.

**3. Standard Approach:**

1.  **Identify the point(s) of potential discontinuity:** This is usually where the function definition changes (piecewise functions) or where a denominator could be zero.
2.  **Calculate LHL and RHL at the potential point(s) of discontinuity:** Use the appropriate function definition for each limit.
3.  **Check if LHL = RHL:** If they are not equal, the function is discontinuous.
4.  **Check if LHL = RHL = f(a):** If all three are equal, the function is continuous at x = a.
5.  **Determine the parameter values (if any) that make the function continuous:** Set LHL = RHL = f(a) and solve for the unknown parameter(s).

**4. Quick Tips:**

*   **Standard Limits:** Remember important limits like $\lim_{x \to 0} \frac{\sin x}{x} = 1$,  $\lim_{x \to 0} \frac{e^x - 1}{x} = 1$, and $\lim_{x \to 0} \frac{\ln(1+x)}{x} = 1$. These can significantly simplify limit calculations.
*   **Rationalization/Factorization:** When dealing with indeterminate forms like 0/0, try rationalizing the numerator or denominator or factoring out common terms.
*   **Greatest Integer Function:** For functions involving the greatest integer function `[x]`, always evaluate LHL and RHL separately, as `[a-h]` and `[a+h]` may differ. `[a-h] = a-1` when a is an integer. `[a+h] = a` when a is an integer.

**5. Common Mistakes:**

*   **Ignoring points of potential discontinuity:** Failing to identify points where the function might be discontinuous is a major error.
*   **Incorrectly calculating LHL and RHL:** Using the wrong function definition for LHL or RHL, or making algebraic errors in the limit calculation.
*   **Assuming continuity without proof:**  Don't assume a function is continuous just because it "looks" continuous. Always verify using the definition. Remember, composition of continuous function is continuous.
