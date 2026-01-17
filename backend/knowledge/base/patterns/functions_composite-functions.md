---
chapter: functions
topic: composite-functions
jee_frequency: 9
years_appeared: [2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 31
difficulty: medium
---

# Functions: Composite Functions

**JEE Frequency**: 9 years | **Questions**: 31

## Composite Functions: JEE Knowledge Base

**JEE Frequency:** 9 years
**Question Count:** 31 questions

**1. Pattern Recognition:**

*   Questions involve finding the composite of two or more functions: `f(g(x))`, `g(f(x))`, or nested compositions like `f(g(h(x)))`.
*   Cyclic or repeating patterns in function composition (e.g., f(f(x)), f(f(f(x))), etc.) are a common theme. Especially compositions involving rational functions.
*   Problems often require determining the domain/range of composite functions or finding x such that `(f o g)(x) = x` or some other specified value.

**2. Core Formulas:**

*   **(Definition):**  `(f o g)(x) = f(g(x))`
*   **(Associativity):** `(f o (g o h))(x) = ((f o g) o h)(x)`
*   **(Identity Function):** If `I(x) = x`, then `(f o I)(x) = (I o f)(x) = f(x)`
*   **(Domain):** The domain of `(f o g)(x)` is the set of all x in the domain of `g` such that `g(x)` is in the domain of `f`.
*   **(Inverse):** If `(f o g)(x) = x` and `(g o f)(x) = x`, then f and g are inverses of each other, denoted as `f(x) = g^{-1}(x)` and `g(x) = f^{-1}(x)`.

**3. Standard Approach:**

1.  **Evaluate from Inside Out:** Start by finding the inner function's value, `g(x)`, then substitute this value into the outer function, `f(g(x))`.
2.  **Determine Domain Carefully:**  Consider the domain restrictions of both the inner and outer functions. The overall domain is restricted by both.
3.  **Look for Patterns:** If repeatedly composing a function with itself, try calculating the first few iterations (`f(x)`, `f(f(x))`, `f(f(f(x)))`) to identify a repeating pattern or cycle.
4.  **Solve for x:**  If `(f o g)(x) = h(x)`, then `f(g(x)) = h(x)`. Solve this equation for `x`.  Be mindful of domain restrictions during the solving process.
5.  **Differentiation for Increasing/Decreasing:**  If the problem asks for the intervals where `(f o g)(x)` is increasing/decreasing, find the derivative `d/dx (f(g(x))) = f'(g(x)) * g'(x)` and analyze its sign.

**4. Quick Tips:**

*   **Test Simple Values:** If you're struggling to find a general pattern, try plugging in simple values for *x* (e.g., 0, 1, -1) to see if you can deduce a pattern empirically.
*   **Function Transformations:** Recognizing function transformations (shifts, stretches, reflections) can help simplify composite function problems. Understand how transformations impact the graph and equation.

**5. Common Mistakes:**

*   **Forgetting Domain Restrictions:** A very common error is not considering the domain of the inner function *and* the resulting domain requirement after applying the outer function.
*   **Incorrect Order of Composition:**  `f(g(x))` is generally *not* the same as `g(f(x))`.  Pay close attention to the order.
*   **Assuming Composability:**  Just because functions *f* and *g* are defined doesn't mean *f o g* or *g o f* are defined.  The range of the inner function must be a subset of the domain of the outer function.
