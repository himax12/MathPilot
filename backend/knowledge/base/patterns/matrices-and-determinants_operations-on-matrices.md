---
chapter: matrices-and-determinants
topic: operations-on-matrices
jee_frequency: 8
years_appeared: [2006, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 32
difficulty: medium
---

# Matrices And Determinants: Operations On Matrices

**JEE Frequency**: 8 years | **Questions**: 32

## Matrices and Determinants: Operations on Matrices - JEE Knowledge Base

**JEE Frequency:** 8 years
**Question Count:** 32 questions

This document focuses on techniques crucial for quickly and accurately solving JEE problems related to matrix operations.

**1. Pattern Recognition:**

*   **Matrix Equations:** Problems involving matrix equations like  `AX = B`, `A² + A + I = 0`, or expressions containing powers of matrices. The goal is often to find relationships between matrices, their inverses, or specific elements.
*   **Special Matrices:** Identify if matrices are orthogonal, symmetric, skew-symmetric, idempotent (A² = A), involutory (A² = I), or nilpotent (Aⁿ = 0 for some n). These properties lead to faster solutions.
*   **Matrix Powers:**  Look for patterns in matrix powers (A², A³, etc.).  Express Aⁿ in terms of I and A. Check for cyclic behavior or diagonalization possibilities.

**2. Core Formulas:**

*   **Matrix Multiplication:**  (AB)<sub>ij</sub> = ∑<sub>k=1</sub><sup>n</sup> A<sub>ik</sub>B<sub>kj</sub>
*   **Matrix Inverse:**  A<sup>-1</sup> = (1/|A|) adj(A), where |A| is the determinant and adj(A) is the adjugate of A.  AA⁻¹ = A⁻¹A = I
*   **Transpose Properties:** (A<sup>T</sup>)<sup>T</sup> = A, (AB)<sup>T</sup> = B<sup>T</sup>A<sup>T</sup>, (A + B)<sup>T</sup> = A<sup>T</sup> + B<sup>T</sup>
*   **Adjoint Properties:** adj(AB) = adj(B)adj(A), adj(adj(A)) = |A|<sup>n-2</sup> A (for n x n matrix A).  A(adj A) = (adj A)A = |A|I

**3. Standard Approach:**

1.  **Identify Matrix Type:** Check for special properties (symmetric, orthogonal, etc.) before starting complex calculations.
2.  **Simplify the Expression:** Use matrix algebra properties (associativity, distributivity) to simplify given equations.  Carefully observe order of operations - Matrix multiplication is NOT commutative.
3.  **Calculate Low Powers:**  If the problem involves A<sup>n</sup>, calculate A², A³, etc., to identify a pattern or relation.
4.  **Use Inverse (if applicable):** If the determinant is non-zero, find the inverse and use it to solve matrix equations.
5.  **Consider Cayley-Hamilton Theorem:** For 2x2 and 3x3 matrices, the Cayley-Hamilton theorem (A<sup>2</sup> - tr(A)A + det(A)I = 0 for 2x2) can simplify power calculations significantly.

**4. Quick Tips:**

*   **Check Options:**  If options are provided, try substituting simple matrices (e.g., identity matrix, zero matrix) or values to eliminate incorrect answers.
*   **Use Determinants:**  In equations involving matrix products, taking the determinant of both sides can simplify the problem. Remember |AB| = |A||B|.
*   **Orthogonal Matrices:** If A is orthogonal (A<sup>T</sup>A = I), then A⁻¹ = A<sup>T</sup> and |A| = ±1. This drastically simplifies many calculations.

**5. Common Mistakes:**

*   **Non-Commutativity:** Forgetting that matrix multiplication is not commutative (AB ≠ BA in general).  Always pay attention to the order of multiplication.
*   **Incorrect Use of Inverse:** Trying to find the inverse of a singular matrix (|A| = 0).  Check the determinant before attempting to calculate A⁻¹.
*   **Assuming (A+B)² = A² + 2AB + B²:** This is only true if A and B commute (AB = BA). In general, (A+B)² = A² + AB + BA + B².
