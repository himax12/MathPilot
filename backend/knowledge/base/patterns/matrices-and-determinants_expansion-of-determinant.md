---
chapter: matrices-and-determinants
topic: expansion-of-determinant
jee_frequency: 17
years_appeared: [2002, 2003, 2004, 2005, 2007, 2009, 2014, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 52
difficulty: medium
---

# Matrices And Determinants: Expansion Of Determinant

**JEE Frequency**: 17 years | **Questions**: 52

## Matrices and Determinants: Expansion of Determinant - JEE Knowledge Base

**JEE Frequency:** 17 years
**Question Count:** 52 questions

**1. Pattern Recognition:**

*   The question explicitly asks for the value of a determinant.
*   Elements often involve algebraic expressions, trigonometric functions, logarithmic functions, or progressions (AP, GP, HP).
*   Look for opportunities to simplify using properties of determinants *before* expanding.

**2. Core Formulas:**

*   **Determinant of a 3x3 matrix:**
    $$
    \begin{vmatrix}
    a & b & c \\
    d & e & f \\
    g & h & i
    \end{vmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg)
    $$
*   **Properties of Determinants:** (Crucial for simplification before expansion)
    *   Row/Column operations (e.g., $R_i \rightarrow R_i + kR_j$) do *not* change the value if $k$ is a constant.
    *   Interchanging rows/columns changes the sign.
    *   If two rows/columns are identical, the determinant is 0.
    *   If a row/column is entirely zero, the determinant is 0.
    *   $\det(AB) = \det(A) \det(B)$
*   **Factorization Method:**  If the determinant vanishes at x=a, (x-a) is a factor

**3. Standard Approach:**

1.  **Simplify:** Use properties of determinants (row/column operations) to create zeros or identical rows/columns.  Aim to get at least two zeros in a row or column.
2.  **Expand:** Choose the row or column with the most zeros. This minimizes computation. Use cofactor expansion.
3.  **Factorize:** Look for common factors after expansion.
4.  **Substitute:** If the question involves variables (like *x* or *n*), substitute simple values to check your answer (optional, for verification).
5. **Verify:** If time permits, substitute your answer into the original question and double-check

**4. Quick Tips:**

*   **GP Simplification:** If elements involve logarithms of terms in GP, use the property $\log a_n = \log ar^{n-1} = \log a + (n-1)\log r$ to create arithmetic progressions within the determinant entries.
*   **Cube Roots of Unity:** Remember $1 + \omega + \omega^2 = 0$ and $\omega^3 = 1$ when dealing with complex cube roots of unity. Use these relationships to simplify expressions within the determinant.
*   **Look for Symmetry:** If the matrix exhibits symmetry, it might suggest a particular simplifying operation.

**5. Common Mistakes:**

*   **Sign Errors:** Be very careful with signs during cofactor expansion. Remember the checkerboard pattern of signs (+ - +; - + -; + - +).
*   **Incorrect Operations:** Ensure row/column operations are performed correctly. A single arithmetic error can propagate through the entire solution. Don't multiply a row/column by a variable, because then you have to divide by the same variable outside the determinant.
*   **Premature Expansion:** Avoid expanding the determinant before simplification. It leads to unnecessary computation and increases the chance of errors.
*   **Ignoring Given Conditions:** Pay close attention to given conditions (e.g., *a* > 0, discriminant is negative). These conditions often dictate the final answer or help eliminate incorrect options.
