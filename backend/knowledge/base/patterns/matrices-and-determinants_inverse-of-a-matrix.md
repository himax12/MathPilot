---
chapter: matrices-and-determinants
topic: inverse-of-a-matrix
jee_frequency: 11
years_appeared: [2004, 2005, 2014, 2016, 2018, 2019, 2021, 2022, 2023, 2024, 2025]
question_count: 22
difficulty: medium
---

# Matrices And Determinants: Inverse Of A Matrix

**JEE Frequency**: 11 years | **Questions**: 22

## Inverse of a Matrix: JEE Knowledge Base

**JEE Frequency:** 11 years
**Question Count:** 22 questions

**1. Pattern Recognition:**

*   Questions often involve finding the inverse directly, or using given matrix equations (like polynomials in A) to deduce the inverse.
*   Check for relationships like orthogonal matrices ($AA^T = I$), adjoint matrices, or special matrix forms that simplify finding the inverse.

**2. Core Formulas:**

*   **Inverse Formula:**  $A^{-1} = \frac{1}{|A|} adj(A)$, where $|A|$ is the determinant of A and $adj(A)$ is the adjugate (transpose of the cofactor matrix) of A.
*   **Adjoint Calculation (2x2 Matrix):** If $A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$, then $adj(A) = \begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$.
*   **Property of Inverse:** $A A^{-1} = A^{-1} A = I$, where I is the identity matrix.
*   **Inverse of Product:** $(AB)^{-1} = B^{-1} A^{-1}$.
*   **Inverse of Transpose:** $(A^T)^{-1} = (A^{-1})^T$.

**3. Standard Approach:**

1.  **Check Determinant:** Calculate $|A|$. If $|A| = 0$, the matrix is singular and the inverse does not exist.
2.  **Find Adjugate:** Calculate the cofactor matrix and then take its transpose to get the adjugate.  For 3x3 matrices, be careful with sign conventions (+/-).
3.  **Apply Inverse Formula:** Use $A^{-1} = \frac{1}{|A|} adj(A)$.
4.  **Verify (Optional):** Multiply $A$ by $A^{-1}$ to ensure the result is the identity matrix ($I$).

**4. Quick Tips:**

*   **Matrix Polynomials:** If an equation like $A^2 - 5A + 7I = 0$ is given, pre-multiply by $A^{-1}$ to directly find $A^{-1}$ in terms of $A$ and $I$:  $A - 5I + 7A^{-1} = 0 \implies A^{-1} = \frac{1}{7}(5I - A)$.
*   **Orthogonal Matrices:** If $A$ is orthogonal, then $A^{-1} = A^T$.

**5. Common Mistakes:**

*   **Incorrect Adjugate:** Errors in calculating cofactors (especially the signs) are a frequent mistake. Double-check your calculations.
*   **Determinant Zero:** Forgetting to check if the determinant is zero *before* attempting to find the inverse.
*   **Applying Properties Incorrectly:**  Misusing the order of matrices in properties like $(AB)^{-1} = B^{-1}A^{-1}$. Be mindful of the order of multiplication.
