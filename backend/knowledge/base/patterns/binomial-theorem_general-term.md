---
chapter: binomial-theorem
topic: general-term
jee_frequency: 15
years_appeared: [2002, 2003, 2004, 2005, 2007, 2013, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 81
difficulty: medium
---

# Binomial Theorem: General Term

**JEE Frequency**: 15 years | **Questions**: 81

## Binomial Theorem: General Term (JEE Knowledge Base)

**JEE Frequency:** High (15 years, 81 questions)

**1. Pattern Recognition:**

*   The question asks for a specific term's coefficient ($x^n$), independent term, or relates coefficients of different terms in a binomial expansion.
*   Involves finding the number of integral terms within an expansion of the form $$(a + b)^{n}$$.
*   May involve relating 'r' (term number) and 'm' (power) given a specific condition on the coefficients.

**2. Core Formulas:**

*   **General Term:**  $$T_{r+1} = {^nC_r} \, a^{n-r} \, b^r$$
*   **Finding Independent Term:** Identify 'r' such that the power of x in $$T_{r+1}$$ is zero.
*   **Coefficient Ratio:** $$\frac{T_{r+1}}{T_r} = \frac{n-r+1}{r} \cdot \frac{b}{a}$$  (useful for A.P./G.P. problems)
*   **Integral Terms:** If  $$(a^{1/p} + b^{1/q})^n$$, find the number of 'r' values such that both $$(n-r)/p$$ and $$r/q$$ are integers.

**3. Standard Approach:**

1.  **Identify:** Recognize the binomial expression and the term you're interested in.
2.  **Apply General Term:** Write the general term, $$T_{r+1}$$, using the formula.
3.  **Solve for 'r':**  Equate the power of x in $$T_{r+1}$$ to the desired power or use the given condition to find the value of 'r'.
4.  **Substitute & Simplify:** Substitute the 'r' value back into $$T_{r+1}$$ to find the coefficient or the required term.
5.  **Use Coefficient Relationships:**  If coefficients are in A.P. or G.P., set up equations using the coefficients of (r-1)th, rth, and (r+1)th terms and solve.

**4. Quick Tips:**

*   **Symmetry of Coefficients:** $${^nC_r} = {^nC_{n-r}}$$.  Use this to simplify expressions.
*   **Divisibility:** In finding integral terms, focus on finding 'r' values that make the powers integers *directly*. Don't get bogged down in complex number theory.
*   **Coefficient of x<sup>0</sup> (Constant Term):**  Quickly determine the 'r' for which the exponent of 'x' in the general term is zero and directly substitute into the general term formula.

**5. Common Mistakes:**

*   **Forgetting the ' + 1' :** Remember that $$T_{r+1}$$ represents the (r+1)th term, *not* the rth term.
*   **Incorrect Simplification of Exponents:**  Be careful when simplifying fractional exponents, especially with nested radicals. Check for prime factorization.
*   **Not Considering All Cases for Integral Terms:** Make sure you've found *all* values of 'r' that result in integral terms, within the permissible range $$0 \le r \le n$$.
