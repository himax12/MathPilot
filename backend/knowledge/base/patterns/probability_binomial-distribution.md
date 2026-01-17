---
chapter: probability
topic: binomial-distribution
jee_frequency: 15
years_appeared: [2002, 2003, 2004, 2007, 2009, 2011, 2013, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024]
question_count: 36
difficulty: medium
---

# Probability: Binomial Distribution

**JEE Frequency**: 15 years | **Questions**: 36

## Binomial Distribution: JEE Knowledge Base

**JEE Frequency:** High (15 years, 36 questions)

**1. Pattern Recognition:**

*   Problem states a fixed number of independent trials (e.g., coin tosses, dice rolls).
*   Each trial has only two possible outcomes: success or failure.
*   Probability of success (`p`) remains constant across all trials. Look for keywords like "fair coin", "unbiased dice", "independent events".

**2. Core Formulas:**

*   Probability Mass Function (PMF):  $P(X = k) = {n \choose k} p^k (1-p)^{n-k}$
*   Mean: $\mu = np$
*   Variance: $\sigma^2 = np(1-p)$
*   Standard Deviation: $\sigma = \sqrt{np(1-p)}$
*   Probability of at least one success: $P(X \ge 1) = 1 - P(X=0) = 1 - (1-p)^n$

**3. Standard Approach:**

1.  Identify the number of trials, `n`.
2.  Determine the probability of success, `p`, in a single trial.
3.  Calculate the probability of failure, `q = 1 - p`.
4.  Apply the relevant formula (PMF, mean, variance, etc.) based on what the problem asks.
5.  Simplify the expression and choose the correct answer.

**4. Quick Tips:**

*   **Mean and Variance Relationship:** If mean and variance are given, use $\mu = np$ and $\sigma^2 = np(1-p)$ to quickly find `n` and `p`.  Divide variance by mean: $\frac{\sigma^2}{\mu} = 1-p$.
*   **At Least One Success:** Use the complement rule:  $P(X \ge 1) = 1 - P(X=0)$ – it's often simpler.

**5. Common Mistakes:**

*   **Incorrectly identifying 'p':**  Carefully define what constitutes a "success" in the problem. For example, "getting a prime number on a dice roll" has p=1/2, not 1/6.
*   **Confusing Variance and Standard Deviation:** Remember to square the standard deviation to get the variance, and vice-versa.
*   **Misinterpreting "at least" or "at most":**  Understand the wording precisely.  "At least 2" means 2 or more. "At most 2" means 2 or less.
