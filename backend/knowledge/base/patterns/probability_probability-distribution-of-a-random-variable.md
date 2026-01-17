---
chapter: probability
topic: probability-distribution-of-a-random-variable
jee_frequency: 9
years_appeared: [2005, 2006, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 29
difficulty: medium
---

# Probability: Probability Distribution Of A Random Variable

**JEE Frequency**: 9 years | **Questions**: 29

## Probability Distribution of a Random Variable: JEE Knowledge Base

**JEE Frequency:** 9 years
**Question Count:** 29

**1. Pattern Recognition:**

*   Problems involve associating numerical values with random experiment outcomes.
*   Frequently asks for Expected Value (Mean), Variance, or probabilities based on given distributions (Poisson, Binomial, etc.)
*   Distribution may be explicitly given in table form, or implicitly described through a word problem.

**2. Core Formulas:**

*   **Expected Value (Mean):**  \(E[X] = \sum x_i P(X=x_i)\) (Discrete), \(E[X] = \int x f(x) dx\) (Continuous)
*   **Variance:** \(Var(X) = E[X^2] - (E[X])^2\)
*   **Standard Deviation:** \(\sigma = \sqrt{Var(X)}\)
*   **Binomial Distribution:** \(P(X=k) = {n \choose k} p^k (1-p)^{n-k}\), E[X] = np, Var(X) = np(1-p)
*   **Poisson Distribution:** \(P(X=k) = \frac{e^{-\lambda} \lambda^k}{k!}\), E[X] = \(\lambda\), Var(X) = \(\lambda\)

**3. Standard Approach:**

1.  **Identify the Random Variable:** Clearly define what X represents numerically.
2.  **Determine the Distribution:** Is it Binomial, Poisson, or something else? If not explicitly stated, deduce from the problem description. Check if distribution is valid by checking sum of probabilities equal to 1.
3.  **Calculate Probabilities:** Find the probabilities associated with each value the random variable can take. This might involve using the distribution formula or analyzing the sample space.
4.  **Apply the Formula:** Use the appropriate formula to calculate the expected value, variance, or requested probability.
5.  **Simplify:** Ensure your final answer is simplified.

**4. Quick Tips:**

*   **Poisson Approximation:** If n is large and p is small in a Binomial distribution, approximate with Poisson: \(\lambda = np\).
*   **Linearity of Expectation:** \(E[aX + b] = aE[X] + b\)

**5. Common Mistakes:**

*   **Incorrectly Identifying the Distribution:** Misinterpreting the problem statement leading to the wrong distribution being used.
*   **Forgetting the Condition \( \sum P(X=x_i) = 1\):** Always check if the probabilities in a given distribution sum up to 1. If not, there's an error or a missing piece.
*   **Calculation Errors:** Careless mistakes in applying formulas, especially with binomial coefficients or factorial calculations.
