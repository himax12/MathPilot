---
chapter: definite-integration
topic: definite-integral-as-a-limit-of-sum
jee_frequency: 11
years_appeared: [2002, 2003, 2004, 2005, 2016, 2017, 2019, 2021, 2022, 2023, 2024]
question_count: 24
difficulty: medium
---

# Definite Integration: Definite Integral As A Limit Of Sum

**JEE Frequency**: 11 years | **Questions**: 24

## Definite Integral As A Limit Of Sum - JEE Knowledge Base

**JEE Frequency:** 11 years
**Question Count:** 24

This topic involves converting a limit of a summation into a definite integral, allowing for easier evaluation.

**1. Pattern Recognition:**

*   **Summation:** Look for expressions involving sums with a large number of terms (n tending to infinity). The sum usually involves `r/n` within the terms.
*   **n in denominator:** Identify expressions where the sum is divided by a power of `n`. The power is crucial for defining the upper limit of integration.

**2. Core Formulas:**

*   **Limit Definition:**
    $$ \lim_{n \to \infty} \sum_{r=1}^{n} \frac{1}{n} f\left(\frac{r}{n}\right) = \int_{0}^{1} f(x) \, dx $$
*   **Generalized Limit Definition:**
    $$ \lim_{n \to \infty} \sum_{r=1}^{n} \frac{b-a}{n} f\left(a + \frac{r}{n}(b-a)\right) = \int_{a}^{b} f(x) \, dx $$
*   **Useful Series:** While not directly a formula, remember standard series like:
    *   $\sum_{r=1}^{n} r = \frac{n(n+1)}{2}$
    *   $\sum_{r=1}^{n} r^2 = \frac{n(n+1)(2n+1)}{6}$
    *   $\sum_{r=1}^{n} r^3 = \left(\frac{n(n+1)}{2}\right)^2$
    These can sometimes simplify expressions *before* applying the limit.

**3. Standard Approach:**

1.  **Express as a Summation:** Rewrite the given expression in the form $\lim_{n \to \infty} \sum_{r=1}^{n} (\text{term involving }r, n)$.
2.  **Identify `f(r/n)`:**  Manipulate the summand (the term inside the summation) to isolate the term `r/n`. The remaining portion (excluding `1/n` or a constant multiple thereof) is often `f(r/n)`.
3.  **Identify the Limits:** The lower limit is usually 0. The upper limit is typically 1.  If `r` goes from `a` to `b`, the integration range becomes $[a/n, b/n]$, as n approaches infinity.
4.  **Convert to Integral:**  Replace the summation with the corresponding definite integral, using the formulas above.
5.  **Evaluate the Integral:** Solve the definite integral using standard integration techniques.

**4. Quick Tips:**

*   **Logarithmic Sums:** If the problem involves a product within the limit, take the natural logarithm first. This converts the product into a sum, making it amenable to the integral definition. (See Q5 as an example).  Remember to exponentiate the result after integration!
*   **Recognize Standard Functions:** Be familiar with the integrals of common functions: `sin x`, `cos x`, `e^x`, `ln x`, `1/(1+x^2)`, etc.

**5. Common Mistakes:**

*   **Incorrectly Identifying `f(r/n)`:**  Pay close attention to isolating the correct function of `r/n`.  Double-check your algebra.
*   **Forgetting the `1/n` factor:**  The `1/n` factor is crucial for converting the sum to an integral. Don't miss it.
*   **Wrong Limits of Integration:**  If the sum doesn't start from `r=1` or end at `r=n`, carefully determine the correct limits of integration. This often involves `lim (r_start / n)` as the lower limit and `lim (r_end / n)` as the upper limit.
