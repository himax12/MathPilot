---
chapter: area-under-the-curves
topic: area-bounded-between-the-curves
jee_frequency: 23
years_appeared: [2002, 2003, 2004, 2005, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 141
difficulty: medium
---

# Area Under The Curves: Area Bounded Between The Curves

**JEE Frequency**: 23 years | **Questions**: 141

## Area Under the Curves: Area Bounded Between Curves - JEE Knowledge Base

**JEE Frequency:** High (23 years, 141 questions)

**1. Pattern Recognition:**

*   Look for questions involving multiple curves (polynomials, trigonometric functions, absolute value functions, logarithmic functions, exponential functions, etc.).
*   The question explicitly asks for the "area bounded/enclosed by the curves."
*   Often includes absolute value functions or piecewise defined functions requiring careful consideration of intervals.

**2. Core Formulas:**

*   Area between curves *f(x)* and *g(x)* from *x = a* to *x = b*, where *f(x) ≥ g(x)*:  $$A = \int_a^b [f(x) - g(x)] \, dx$$
*   Area when integrating with respect to *y*:  $$A = \int_c^d [h(y) - k(y)] \, dy$$, where *h(y) ≥ k(y)* from *y = c* to *y = d*.
*   Total area accounting for sign changes: $$A = \int_a^b |f(x) - g(x)| \, dx$$. Requires identifying points of intersection to determine intervals where *f(x) > g(x)* or vice-versa.

**3. Standard Approach:**

1.  **Sketch the Curves:** Accurately plot the given curves to visualize the bounded region.  Pay close attention to intersections and behavior of functions, especially around discontinuities or absolute value changes.
2.  **Find Points of Intersection:** Solve the equations of the curves simultaneously to find the x-coordinates (or y-coordinates) of the points of intersection. These points define the limits of integration.
3.  **Determine Dominating Function:** Identify which function is greater than the other within each interval defined by the intersection points.  This determines which function to subtract.
4.  **Set Up and Evaluate the Integral(s):** Set up the definite integral(s) using the appropriate limits and the difference of the functions. Evaluate the integral(s) to find the area.
5.  **Consider Symmetry:** Exploit symmetry (if present) to simplify calculations. Calculate the area of one symmetric part and multiply by the appropriate factor.

**4. Quick Tips:**

*   **Absolute Value/Mod Functions:** Break down the area integral into separate intervals based on where the absolute value expression changes sign.
*   **Inverse Functions:** If integrating with respect to *x* is difficult, consider integrating with respect to *y*.  Express *x* as a function of *y*.

**5. Common Mistakes:**

*   **Forgetting Absolute Value:** Not using the absolute value sign when the dominating function changes, leading to negative area.
*   **Incorrect Limits of Integration:** Using the wrong intersection points as the limits of integration. Make sure the limits correspond to the interval being integrated.
*   **Algebra Errors:** Making mistakes in finding points of intersection or in evaluating the definite integral. Be meticulous with your algebra.
