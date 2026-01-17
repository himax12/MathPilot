---
chapter: 3d-geometry
topic: lines-in-space
jee_frequency: 18
years_appeared: [2003, 2004, 2005, 2006, 2007, 2008, 2011, 2012, 2013, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 131
difficulty: medium
---

# 3D Geometry: Lines In Space

**JEE Frequency**: 18 years | **Questions**: 131

## 3D Geometry: Lines in Space - JEE Knowledge Base

**JEE Frequency:** 18 years
**Question Count:** 131 questions

**1. Pattern Recognition:**

*   Identifying equations of lines in Cartesian form (symmetric form) or vector form. Look for parameters or direction ratios.
*   Problems usually involve finding the angle between lines, the distance between lines (skew or parallel), coplanarity of lines, or intersection points.

**2. Core Formulas:**

*   **Equation of a line (Vector form):** $\vec{r} = \vec{a} + \lambda \vec{b}$, where $\vec{a}$ is a point on the line and $\vec{b}$ is the direction vector.
*   **Equation of a line (Cartesian form):** $\frac{x-x_1}{a} = \frac{y-y_1}{b} = \frac{z-z_1}{c}$, where $(x_1, y_1, z_1)$ is a point on the line and $(a, b, c)$ are the direction ratios.
*   **Angle between two lines:** $cos\theta = \frac{|\vec{b_1} \cdot \vec{b_2}|}{|\vec{b_1}| |\vec{b_2}|}$
*   **Condition for coplanarity (Cartesian form):**  $\begin{vmatrix} x_2 - x_1 & y_2 - y_1 & z_2 - z_1 \\ a_1 & b_1 & c_1 \\ a_2 & b_2 & c_2 \end{vmatrix} = 0$, where line 1 passes through $(x_1, y_1, z_1)$ with direction ratios $(a_1, b_1, c_1)$ and line 2 passes through $(x_2, y_2, z_2)$ with direction ratios $(a_2, b_2, c_2)$.
*   **Shortest distance between two skew lines:** $d = \frac{| (\vec{a_2} - \vec{a_1}) \cdot (\vec{b_1} \times \vec{b_2}) |}{|\vec{b_1} \times \vec{b_2}|}$

**3. Standard Approach:**

1.  Convert all line equations to either Cartesian or vector form (choose the one that's most convenient based on the problem).
2.  Identify the direction ratios/direction vectors and a point on each line.
3.  Apply the relevant formula based on the question (angle, coplanarity, distance, etc.).
4.  Solve for the unknown variables or parameters.
5.  Verify your solution (if possible) by substituting back into the original equations.

**4. Quick Tips:**

*   **Direction Cosines vs. Direction Ratios:** Remember that direction cosines are normalized direction ratios (sum of squares = 1). Direction ratios are proportional to direction cosines.
*   **Perpendicular Lines:** If lines are perpendicular, the dot product of their direction vectors is zero: $\vec{b_1} \cdot \vec{b_2} = 0$.
*   **Skew Lines:** Lines that are neither parallel nor intersecting are skew lines.

**5. Common Mistakes:**

*   **Incorrectly Identifying Direction Ratios/Vectors:** Pay close attention to the form of the equation.  Ensure coefficients are correctly used.
*   **Forgetting Modulus:** When calculating the angle or shortest distance, remember to take the absolute value.
*   **Not Checking for Parallel Lines Before Applying Skew Distance Formula:**  If lines are parallel, a different formula applies. Check if $\vec{b_1} = k\vec{b_2}$
