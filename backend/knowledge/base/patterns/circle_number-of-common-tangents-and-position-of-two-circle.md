---
chapter: circle
topic: number-of-common-tangents-and-position-of-two-circle
jee_frequency: 11
years_appeared: [2003, 2011, 2014, 2015, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 20
difficulty: medium
---

# Circle: Number Of Common Tangents And Position Of Two Circle

**JEE Frequency**: 11 years | **Questions**: 20

## Circle: Number of Common Tangents & Position of Two Circles - JEE Knowledge Base

**JEE Frequency:** 11 years
**Question Count:** ~20 questions

**1. Pattern Recognition:**

*   Questions involve finding the number of common tangents between two circles.
*   Problems often ask about the relative position of two circles (intersecting, touching, external, internal).
*   Conditions for intersection/touching are commonly explored using distance between centers and radii.

**2. Core Formulas:**

*   Circle Equation: ${(x-h)^2} + {(y-k)^2} = r^2$ (center (h, k), radius r)
*   Distance between centers: $d = \sqrt{{(h_2 - h_1)^2} + {(k_2 - k_1)^2}}$
*   Condition for touching:
    *   Externally: $d = r_1 + r_2$
    *   Internally: $d = |r_1 - r_2|$
*   Number of Common Tangents:
    *   External Circles: $d > r_1 + r_2$ (4 tangents)
    *   Circles touch Externally: $d = r_1 + r_2$ (3 tangents)
    *   Intersecting Circles: $|r_1 - r_2| < d < r_1 + r_2$ (2 tangents)
    *   Circles touch Internally: $d = |r_1 - r_2|$ (1 tangent)
    *   One circle inside another: $d < |r_1 - r_2|$ (0 tangents)
*   Equation of Common Chord:  $S_1 - S_2 = 0$  (where $S_1 = 0$ and $S_2 = 0$ are the equations of the two circles).

**3. Standard Approach:**

1.  **Identify Centers and Radii:** Determine the centers $(h_1, k_1), (h_2, k_2)$ and radii $r_1, r_2$ of both circles.
2.  **Calculate Distance:** Find the distance 'd' between the centers using the distance formula.
3.  **Apply Condition:** Compare 'd' with $r_1 + r_2$ and $|r_1 - r_2|$ to determine the relative position and the number of common tangents.
4.  **Use Common Chord concept (if applicable):** If the problem involves intersection and finding points or equations, use $S_1 - S_2 = 0$ to find the equation of common chord.
5. **Solve for unknowns:** Use given conditions (e.g., touching, intersection) to form equations and solve for unknown parameters (like radius, center coordinates).

**4. Quick Tips:**

*   **Visualize:** Sketching the circles helps understand the geometric configuration.
*   **Common Chord Trick:** The common chord is perpendicular to the line joining the centers. This can be used to find the equation of the common chord or points of intersection.
*   **Check for Simplifications:** Sometimes, completing the square or simplifying the circle equations makes calculations easier.

**5. Common Mistakes:**

*   **Incorrectly calculating 'd':** Ensure correct use of the distance formula.
*   **Forgetting absolute value:** When checking internal touching, remember to use $|r_1 - r_2|$.
*   **Confusing internal and external touching:**  Sketch the circles to avoid this.
*   **Assuming intersecting circles always have 2 common tangents:** Be mindful that if one circle is contained in the other, there will be zero common tangents even if they technically intersect in the abstract sense (touch internally).
