---
chapter: 3d-geometry
topic: lines-and-plane
jee_frequency: 16
years_appeared: [2002, 2005, 2006, 2009, 2011, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
question_count: 123
difficulty: medium
---

# 3D Geometry: Lines And Plane

**JEE Frequency**: 16 years | **Questions**: 123

## 3D Geometry: Lines and Planes - JEE Knowledge Base

**JEE Frequency:** High (16 years, 123 questions)

**1. Pattern Recognition:**

*   **Mixed Equations:** Questions often involve finding relationships between lines and planes using their vector or Cartesian equations. Look for equations like  $$\overrightarrow{r} = \overrightarrow{a} + \lambda \overrightarrow{b}$$ (line) and $$\overrightarrow{r}.\overrightarrow{n} = d$$ (plane) or their Cartesian equivalents.
*   **Distance/Angle Calculation:** Finding the distance between a point and a plane, a line and a plane, or the angle between lines and planes are common themes.
*   **Image/Foot of Perpendicular:** Finding the image of a point in a plane or the foot of the perpendicular from a point to a line or plane is frequently tested.
*   **Coplanarity/Intersection**: Questions based on coplanarity of lines or finding the point of intersection of a line and a plane.

**2. Core Formulas:**

*   **Distance from a point $$(x_1, y_1, z_1)$$ to a plane $$ax + by + cz + d = 0$$:**

    $$Distance = \frac{|ax_1 + by_1 + cz_1 + d|}{\sqrt{a^2 + b^2 + c^2}}$$

*   **Angle $$\theta$$ between a line with direction ratios $$(a_1, b_1, c_1)$$ and a plane with normal vector $$(a_2, b_2, c_2)$$:**

    $$\sin \theta = \frac{|a_1a_2 + b_1b_2 + c_1c_2|}{\sqrt{a_1^2 + b_1^2 + c_1^2}\sqrt{a_2^2 + b_2^2 + c_2^2}}$$

*   **Equation of a plane passing through a point $$(x_1, y_1, z_1)$$ and perpendicular to a vector $$(a, b, c)$$:**

    $$a(x - x_1) + b(y - y_1) + c(z - z_1) = 0$$

*   **Shortest distance between two skew lines: $$\overrightarrow{r} = \overrightarrow{a_1} + \lambda \overrightarrow{b_1}$$ and $$\overrightarrow{r} = \overrightarrow{a_2} + \mu \overrightarrow{b_2}$$**

    $$d = \left| \frac{(\overrightarrow{a_2} - \overrightarrow{a_1}) \cdot (\overrightarrow{b_1} \times \overrightarrow{b_2})}{|\overrightarrow{b_1} \times \overrightarrow{b_2}|} \right|$$

**3. Standard Approach:**

1.  **Convert to Vector Form (if needed):** If given Cartesian equations, convert them to vector form to easily identify direction vectors and points.
2.  **Identify Key Vectors:** Determine the direction vector of the line(s) and the normal vector of the plane(s).
3.  **Apply Relevant Formula:** Select the appropriate formula based on what's being asked (distance, angle, equation of plane).
4.  **Solve for Unknowns:** Substitute known values and solve for any unknown variables (e.g., $$\lambda$$, $$a$$, distance).
5.  **Check your answer**: Check the final answer by plugging back into the equations, or verifying your solution geometrically.

**4. Quick Tips:**

*   **Unit Vectors:**  Work with unit vectors whenever possible (especially for direction cosines) to simplify calculations.
*   **Coplanarity Condition:** Three points $$\overrightarrow{a}, \overrightarrow{b}, \overrightarrow{c}$$ are collinear if  $$\overrightarrow{b} - \overrightarrow{a} = \lambda (\overrightarrow{c} - \overrightarrow{a})$$ for some scalar $$\lambda$$.  Four points $$\overrightarrow{a}, \overrightarrow{b}, \overrightarrow{c}, \overrightarrow{d}$$ are coplanar if $$[\overrightarrow{b} - \overrightarrow{a} \quad \overrightarrow{c} - \overrightarrow{a} \quad \overrightarrow{d} - \overrightarrow{a}] = 0$$ (scalar triple product).
*   **Visualize:** Try to visualize the geometric setup (lines, planes, points) to aid in understanding the problem. A quick sketch can sometimes help.

**5. Common Mistakes:**

*   **Confusing Direction Ratios/Direction Cosines:** Use direction cosines (normalized direction ratios) when calculating angles, or explicitly specify when you're using just direction ratios.
*   **Incorrect Formula Application:**  Ensure you are using the correct formula for the specific scenario (e.g., distance from a point *to* a plane vs. distance between two lines).  Pay close attention to the difference between sine and cosine formulas for angles.
*   **Sign Errors:** Be careful with signs when substituting values into formulas, especially when dealing with vector components. Always double-check your arithmetic.
