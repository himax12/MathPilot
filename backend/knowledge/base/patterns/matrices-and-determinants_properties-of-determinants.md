---
chapter: matrices-and-determinants
topic: properties-of-determinants
jee_frequency: 11
years_appeared: [2007, 2008, 2009, 2012, 2013, 2019, 2020, 2021, 2022, 2023, 2024]
question_count: 45
difficulty: medium
---

# Matrices And Determinants: Properties Of Determinants

**JEE Frequency**: 11 years | **Questions**: 45

## Matrices and Determinants: Properties of Determinants (JEE Focus)

**JEE Frequency:** High (11 years of questions)
**Question Count:** 45

**1. Pattern Recognition:**

*   The question explicitly asks for the determinant of a matrix derived from A, or compares determinants based on properties. Look for keywords like "det," "adjoint," "transpose," "inverse," or "singular/non-singular."
*   Matrices often involve unknown variables (like α), and the determinant is used in an equation to solve for them.
*   Questions frequently combine properties of determinants with properties of adjoint, inverse, and transpose.

**2. Core Formulas:**

*   Determinant of Transpose:  $|A^T| = |A|$
*   Determinant of Product: $|AB| = |A| |B|$
*   Determinant of Adjoint: $|adj(A)| = |A|^{n-1}$ where 'n' is the order of the matrix. Further, $|adj(adj(A))| = |A|^{(n-1)^2}$
*   Determinant of Inverse: $|A^{-1}| = \frac{1}{|A|}$ (A must be non-singular, i.e. $|A| \ne 0$)
*   Determinant of kA: $|kA| = k^n |A|$, where 'n' is the order of the matrix.

**3. Standard Approach:**

1.  **Identify Key Properties:**  Carefully read the question and identify the relevant properties that link the given matrices/determinants.
2.  **Apply Formulas:** Apply the core formulas to simplify the given expression.  Often involves manipulation using the determinant of product, adjoint, or inverse properties.
3.  **Simplify and Solve:**  Simplify the resulting equation and solve for the unknown variable (if any) or the determinant.
4.  **Check for Singular/Non-Singular Conditions:** If inverse is involved, make sure the original matrix is non-singular by checking $|A| \ne 0$.
5.  **Consider Row/Column Operations:**  If direct calculation is difficult, consider applying row or column operations *while tracking the change in determinant*.

**4. Quick Tips:**

*   **Triangular Matrices:** The determinant of a triangular matrix (upper or lower) is the product of its diagonal elements.
*   **Adjoint-Inverse Relationship:** $A^{-1} = \frac{1}{|A|} adj(A)$. Sometimes applying this alongside other rules can simplify problems. This implies $A\cdot adj(A) = |A|I$, where I is the Identity Matrix.

**5. Common Mistakes:**

*   **Order of Matrix:** Forgetting to consider the order (n) of the matrix when applying formulas involving adjoint or scalar multiplication.
*   **Singular Matrix Assumption:** Applying inverse properties without checking if the matrix is non-singular ($|A| = 0$ leads to undefined inverse).
*   **Sign Errors in Row/Column Operations:**  Carelessly applying row/column operations and making errors in the determinant changes (e.g., swapping rows changes the sign). Always clearly mark which operation you are doing so that you do not make careless errors.
