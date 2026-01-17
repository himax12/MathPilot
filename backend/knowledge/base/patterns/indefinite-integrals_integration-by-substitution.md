---
chapter: indefinite-integrals
topic: integration-by-substitution
jee_frequency: 15
years_appeared: [2005, 2008, 2012, 2013, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 55
difficulty: medium
---

# Indefinite Integrals: Integration By Substitution

**JEE Frequency**: 15 years | **Questions**: 55

## Indefinite Integrals: Integration by Substitution (JEE Knowledge Base)

**JEE Frequency:** High (55 questions in 15 years)

**1. Pattern Recognition:**

*   **Composite Functions:** Look for functions within functions, especially within trigonometric, logarithmic, or exponential functions.
*   **Derivative Relationship:** Check if the derivative of an inner function is present (or can be easily created) in the integrand.
*   **Hidden Substitution:**  Sometimes a clever algebraic manipulation is needed to reveal a suitable substitution. Think completing the square, adding/subtracting terms, or factoring.

**2. Core Formulas:**

*   $$\int f(g(x)) \cdot g'(x) \, dx = F(g(x)) + C$$, where $$F'(u) = f(u)$$
*   $$\int \frac{f'(x)}{f(x)} dx = \ln|f(x)| + C$$
*   $$\int [f(x)]^n f'(x) dx = \frac{[f(x)]^{n+1}}{n+1} + C, \text{ where } n \neq -1$$

**3. Standard Approach:**

1.  **Identify Potential Substitution:**  Analyze the integrand for a suitable function, $$g(x)$$, whose derivative might be present.
2.  **Define the Substitution:** Let $$u = g(x)$$.  Calculate $$du = g'(x) \, dx$$.
3.  **Substitute and Simplify:**  Rewrite the integral entirely in terms of $$u$$ and $$du$$. Simplify the resulting integral.
4.  **Integrate:** Evaluate the integral with respect to $$u$$.
5.  **Back-Substitute:** Replace $$u$$ with $$g(x)$$ in the result to express the answer in terms of $$x$$.  Don't forget the constant of integration, $$+C$$.

**4. Quick Tips:**

*   **Trigonometric Transformations:**  Use trigonometric identities (sum-to-product, product-to-sum, double/half angle formulas) to simplify the integrand before substituting.
*   **Reverse Engineering:** If the integral looks complicated, try differentiating the answer choices to see if they match the integrand. This is especially useful in multiple-choice questions.

**5. Common Mistakes:**

*   **Forgetting Back-Substitution:**  Leaving the answer in terms of the new variable *u* is a very common error.  Always substitute back to the original variable.
*   **Incorrect Derivative:**  Double-check the calculation of $$du = g'(x) \, dx$$. A wrong derivative ruins the entire process.
*   **Ignoring the Constant of Integration:** Always add the constant of integration, *C*, to the final answer of an indefinite integral.  It's penalized in JEE.
