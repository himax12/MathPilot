---
chapter: application-of-derivatives
topic: maxima-and-minima
jee_frequency: 22
years_appeared: [2002, 2003, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 99
difficulty: medium
---

# Application Of Derivatives: Maxima And Minima

**JEE Frequency**: 22 years | **Questions**: 99

## Application of Derivatives: Maxima and Minima - JEE Knowledge Base

**JEE Frequency:** High (22 years, 99 questions)

**1. Pattern Recognition:**

*   Problems involve finding the maximum or minimum value of a function (e.g., distance, area, sum, expression) subject to given constraints.
*   Keywords like "maximum," "minimum," "greatest," "least," "largest," etc., directly indicate this topic.
*   Geometric problems involving optimization of shapes (rectangles, triangles) inscribed within other shapes (ellipses, circles).

**2. Core Formulas:**

*   First Derivative Test: If $f'(c) = 0$ and $f'(x)$ changes sign from + to - at x=c, then x=c is a point of local maxima. If  $f'(x)$ changes sign from - to + at x=c, then x=c is a point of local minima.
*   Second Derivative Test: If $f'(c) = 0$ and $f''(c) > 0$, then x=c is a point of local minima. If $f'(c) = 0$ and $f''(c) < 0$, then x=c is a point of local maxima.
*   Absolute Maxima/Minima: Check the function's values at critical points (where $f'(x) = 0$ or is undefined) and endpoints of the interval.
*   Constraint Handling (Lagrange Multipliers conceptually, often solvable by elimination):  If maximizing $f(x,y)$ subject to $g(x,y) = c$, solve the problem with constraints.
*   AM-GM Inequality:  For non-negative numbers $a_1, a_2, ..., a_n$:  $\frac{a_1 + a_2 + ... + a_n}{n} \ge \sqrt[n]{a_1 a_2 ... a_n}$

**3. Standard Approach:**

1.  **Define the Function:** Clearly identify the function $f(x)$ (or $f(x, y)$) you need to maximize or minimize.  Express it in terms of a single variable if necessary, using given constraints.
2.  **Find Critical Points:** Calculate the first derivative, $f'(x)$, and set it to zero to find critical points. Also, consider points where $f'(x)$ is undefined.
3.  **Test Critical Points:** Use the first or second derivative test to determine whether each critical point corresponds to a local maximum, local minimum, or neither.
4.  **Absolute Maxima/Minima:**  If the problem involves a closed interval, evaluate the function at the critical points *within* the interval and at the endpoints of the interval. The largest value is the absolute maximum, and the smallest is the absolute minimum.
5.  **Answer the Question:** Make sure you answer exactly what the question is asking (e.g., find the *value* of x where the maximum occurs, or find the *maximum value* itself).

**4. Quick Tips:**

*   **AM-GM Inequality:**  Useful for problems where the function involves a sum and a product (like `x + 1/x`). Look for ways to rewrite the function in a form suitable for AM-GM.
*   **Symmetry:** Exploit symmetry in the problem. For example, in ellipse problems, maximize in the first quadrant and use symmetry to find the total area/perimeter.
*   **Parameterization:** Parameterize curves to simplify the function (e.g., $x = a\cos\theta$, $y = b\sin\theta$ for an ellipse).

**5. Common Mistakes:**

*   **Forgetting Endpoints:**  When finding absolute maxima/minima on a closed interval, always check the endpoints.
*   **Incorrect Differentiation:**  Ensure accurate differentiation, especially when dealing with implicit functions or trigonometric functions.
*   **Not Verifying the Solution:** After finding a critical point, verify that it actually corresponds to a maximum or minimum using a derivative test. Simply setting the derivative to zero is not sufficient. Failing to check the second derivative or sign change of first derivative.
