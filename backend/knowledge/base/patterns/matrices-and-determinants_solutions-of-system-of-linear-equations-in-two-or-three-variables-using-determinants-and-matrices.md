---
chapter: matrices-and-determinants
topic: solutions-of-system-of-linear-equations-in-two-or-three-variables-using-determinants-and-matrices
jee_frequency: 17
years_appeared: [2003, 2005, 2008, 2010, 2011, 2013, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 117
difficulty: medium
---

# Matrices And Determinants: Solutions Of System Of Linear Equations In Two Or Three Variables Using Determinants And Matrices

**JEE Frequency**: 17 years | **Questions**: 117

## Matrices and Determinants: Solutions of System of Linear Equations

**JEE Frequency:** High (17 years, 117 questions)

This knowledge base focuses on solving systems of linear equations using matrices and determinants, a frequent topic in JEE.

**1. Pattern Recognition:**

*   **Homogeneous vs. Non-Homogeneous Systems:** Distinguish between systems with constants equal to zero (homogeneous) and those with non-zero constants (non-homogeneous). Homogeneous systems *always* have a trivial (all-zero) solution. The key question is existence of *non-trivial* solutions.
*   **Number of Variables & Equations:** Compare the number of variables (usually x, y, z) to the number of equations.  Underdetermined systems (more variables than equations) often have infinitely many solutions.
*   **Parameter Dependence:** Look for a parameter (like 'k', 'a', or 'λ') in the coefficients. The question likely involves finding values of the parameter that result in specific solution scenarios (unique solution, infinite solutions, no solution).

**2. Core Formulas:**

*   **Determinant of Coefficient Matrix (Δ):**  For a system AX = B, where A is the coefficient matrix, calculate its determinant: $$\Delta = |A|$$
*   **Cramer's Rule:** For a system AX = B, if Δ ≠ 0, then:
    $$x = \frac{\Delta_x}{\Delta}, y = \frac{\Delta_y}{\Delta}, z = \frac{\Delta_z}{\Delta}$$, where  Δ<sub>x</sub>, Δ<sub>y</sub>, and Δ<sub>z</sub> are obtained by replacing the corresponding column of A with the column vector B.
*   **Adjoint and Inverse:** For a system AX = B, if Δ ≠ 0 then $$X = A^{-1}B$$ where $$A^{-1} = \frac{adj(A)}{|A|}$$
*   **Homogeneous System Condition for Non-Trivial Solution:** For a homogeneous system AX = 0, non-trivial solutions exist if and only if:  $$|A| = 0$$
*   **Rank of a Matrix:** If system of m equations and n variables has coefficient matrix A, then rank of A must be equal to rank of Augmented matrix [A|B] for system to be consistent i.e. have at least one solution. Number of independent solutions = n - rank(A).

**3. Standard Approach:**

1.  **Form the Coefficient Matrix (A) and the Constant Vector (B).** Represent the system in the matrix form AX = B.
2.  **Calculate the Determinant of A (|A| or Δ).** This is crucial for determining the nature of the solutions.
3.  **Analyze the Determinant:**
    *   If |A| ≠ 0: The system has a unique solution (consistent and independent). Use Cramer's Rule or matrix inversion to find the solution.
    *   If |A| = 0:  The system either has no solution (inconsistent) or infinitely many solutions (consistent and dependent).
4.  **For |A| = 0, calculate the adjoint of A (adj(A)).**  Examine adj(A)B.
    *   If adj(A)B ≠ 0: The system is inconsistent (no solution).
    *   If adj(A)B = 0: The system has infinitely many solutions.  Express some variables in terms of others by solving fewer equations.
5.  **Solve for variables.**

**4. Quick Tips:**

*   **Homogeneous Systems (AX = 0):** If you *know* a non-trivial solution exists, immediately set the determinant of the coefficient matrix to zero and solve for the unknown parameters.
*   **Special Cases:** Look for patterns where equations are multiples of each other or where variables can be easily eliminated.
*   **Check Answers:** If possible, substitute the obtained solutions back into the original equations to verify their correctness.

**5. Common Mistakes:**

*   **Incorrect Determinant Calculation:**  Pay meticulous attention to signs and cofactor expansions. Double-check your determinant calculations, as errors here invalidate the entire solution.
*   **Assuming Unique Solution When |A| = 0:** Don't prematurely assume a unique solution. Further analysis is required.
*   **Forgetting to Check Consistency when |A| = 0:** Always check if the system is consistent (has at least one solution) before assuming infinitely many solutions when |A|=0. Calculate adj(A)B for non-homogeneous systems. Check ranks of A and [A|B].
