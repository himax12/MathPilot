---
chapter: limits-continuity-and-differentiability
topic: differentiability
jee_frequency: 18
years_appeared: [2002, 2003, 2005, 2006, 2007, 2008, 2009, 2012, 2015, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 75
difficulty: medium
---

# Limits Continuity And Differentiability: Differentiability

**JEE Frequency**: 18 years | **Questions**: 75

## Differentiability: JEE Knowledge Base

**JEE Frequency:** High (18 years, 75 questions)

**1. Pattern Recognition:**

*   Problems often involve piecewise defined functions, limits involving derivatives, or functions defined by functional equations.
*   Look for questions asking if a function is differentiable at a specific point or across an interval. Keywords: `differentiable`, `f'(x) exists`, `left-hand derivative`, `right-hand derivative`.

**2. Core Formulas:**

*   **Definition of Derivative:**
    $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$
*   **Left-Hand Derivative (LHD):**
    $LHD = \lim_{h \to 0^-} \frac{f(x+h) - f(x)}{h}$
*   **Right-Hand Derivative (RHD):**
    $RHD = \lim_{h \to 0^+} \frac{f(x+h) - f(x)}{h}$
*   **Differentiability Condition:** A function is differentiable at x=c if and only if:
    *   f(x) is continuous at x=c.
    *   $LHD|_{x=c} = RHD|_{x=c}$
*   **Derivative of Implicit functions:** If $f(x,y) = 0$ then $\frac{dy}{dx} = -\frac{\partial f / \partial x}{\partial f / \partial y}$

**3. Standard Approach:**

1.  **Check Continuity:** Before checking differentiability at a point, ensure the function is continuous at that point. Use the definition of continuity: $\lim_{x \to c^-} f(x) = \lim_{x \to c^+} f(x) = f(c)$.
2.  **Calculate LHD and RHD:**  Use the definitions provided above.  Be careful with piecewise functions; use the appropriate definition for each side.
3.  **Equate LHD and RHD:**  If the function is continuous, equate the LHD and RHD. If they are equal, the function is differentiable at that point.
4.  **Functional Equations:**  For functions defined by functional equations (like f(x+y) = f(x)f(y)), differentiate the equation with respect to x, treat y as a constant, and then set x=0 to find f'(0). Then relate it back to f'(x).
5.  **Higher Order Differentiability:** Differentiate f'(x) and follow steps 1-3 to check if the function is twice differentiable.

**4. Quick Tips:**

*   **Shortcut for Piecewise Functions:** If $f(x)$ is defined as $g(x)$ for $x<c$ and $h(x)$ for $x>c$, and both $g(x)$ and $h(x)$ are differentiable, then differentiability of $f(x)$ at $x=c$ is sufficient if $g'(c) = h'(c)$.
*   **Use L'Hopital's Rule:**  Limits involving derivatives (like in some sample questions) can often be solved using L'Hopital's Rule.

**5. Common Mistakes:**

*   **Forgetting to check continuity first:** A function *must* be continuous to be differentiable.
*   **Incorrectly calculating LHD or RHD:** Pay close attention to the intervals in piecewise functions and the sign of 'h' in the limit.
*   **Assuming differentiability implies existence of higher-order derivatives:** Differentiability only guarantees the existence of the first derivative; higher-order derivatives must be checked separately.
