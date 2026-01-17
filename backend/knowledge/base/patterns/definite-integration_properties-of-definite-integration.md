---
chapter: definite-integration
topic: properties-of-definite-integration
jee_frequency: 23
years_appeared: [2002, 2003, 2004, 2005, 2006, 2007, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 238
difficulty: medium
---

# Definite Integration: Properties Of Definite Integration

**JEE Frequency**: 23 years | **Questions**: 238

## Definite Integration: Properties - JEE Knowledge Base

**JEE Frequency:** High (23 years, 238 questions)

**1. Pattern Recognition:**

*   Presence of definite integrals with specific limits (e.g., 0 to a, -a to a, periodic functions).
*   Functional equations or relationships within the integrand hinting at specific properties.
*   Integrals involving greatest integer function, modulus function, or trigonometric functions over symmetric intervals.

**2. Core Formulas:**

*   **(P0: Basic Property):**  $$\int_a^b f(x) dx = - \int_b^a f(x) dx$$
*   **(P1: Split Integral):** $$\int_a^b f(x) dx = \int_a^c f(x) dx + \int_c^b f(x) dx$$
*   **(P2: Property 4):** $$\int_0^a f(x) dx = \int_0^a f(a-x) dx$$
*   **(P3: Even/Odd Function):**
    *   If f(x) is even: $$\int_{-a}^a f(x) dx = 2 \int_0^a f(x) dx$$
    *   If f(x) is odd: $$\int_{-a}^a f(x) dx = 0$$
*   **(P4: Periodicity):** If f(x) is periodic with period T: $$\int_0^{nT} f(x) dx = n \int_0^T f(x) dx$$  and  $$\int_a^{a+T} f(x) dx = \int_0^{T} f(x) dx$$

**3. Standard Approach:**

1.  **Check for Odd/Even Functions:** Simplify the integral using the odd/even function property (P3) if applicable.
2.  **Apply Property 4 (P2):** Substitute  `x`  with  `(a-x)` if the limits are from `0` to `a`. Add the original and transformed integral.
3.  **Split the Integral:** Use P1 to break the integral based on critical points of modulus, greatest integer function, or piecewise functions.
4.  **Periodicity:** Check if the function is periodic. If yes, simplify using the periodicity property (P4).
5.  **Simplify and Integrate:** After applying the properties, the integral should be easier to solve.

**4. Quick Tips:**

*   **King's Rule (P2):**  Always consider applying $$\int_a^b f(x) dx = \int_a^b f(a+b-x) dx$$ and adding to the original integral.  This often leads to significant simplification.
*   **Visualize:** For integrals with modulus or greatest integer functions, sketching the function can help determine the points where the integral needs to be split.

**5. Common Mistakes:**

*   **Incorrectly identifying Even/Odd Functions:** Ensure the function satisfies the actual definition of even/odd before applying the property.
*   **Ignoring Critical Points:** For modulus or greatest integer functions, forgetting to split the integral at critical points (where the expression inside changes sign or value) will lead to incorrect results.
*   **Forgetting the Limits:** When applying substitutions or properties, always remember to adjust the limits of integration accordingly.
