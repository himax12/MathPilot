---
chapter: probability
topic: conditional-probability-and-multiplication-theorem
jee_frequency: 16
years_appeared: [2007, 2008, 2009, 2011, 2012, 2014, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 40
difficulty: medium
---

# Probability: Conditional Probability And Multiplication Theorem

**JEE Frequency**: 16 years | **Questions**: 40

## Probability: Conditional Probability & Multiplication Theorem - JEE Knowledge Base

**JEE Frequency:** 16 years
**Question Count:** 40 questions

**1. Pattern Recognition:**

*   Look for problems involving events dependent on the outcome of previous events (e.g., "if the first event occurs, then...").
*   Keywords such as "given that," "provided that," or explicit conditional probability notation,  P(A|B).
*   Problems involving sequential events and finding the probability of their joint occurrence.

**2. Core Formulas:**

*   **Conditional Probability:** \( P(A|B) = \frac{P(A \cap B)}{P(B)} \),  provided \( P(B) > 0 \)
*   **Multiplication Theorem:** \( P(A \cap B) = P(A) \cdot P(B|A) = P(B) \cdot P(A|B) \)
*   **Total Probability Theorem:** \( P(A) = P(A \cap B_1) + P(A \cap B_2) + ... + P(A \cap B_n) = \sum_{i=1}^{n} P(B_i)P(A|B_i) \) where \( B_1, B_2, ..., B_n \) are mutually exclusive and exhaustive events.
*   **Bayes' Theorem:** \( P(B_i|A) = \frac{P(B_i)P(A|B_i)}{\sum_{j=1}^{n} P(B_j)P(A|B_j)} \)

**3. Standard Approach:**

1.  **Define Events:** Clearly define each event using appropriate notation (A, B, etc.).
2.  **Identify Conditional Probability:** Recognize which probabilities are conditional and which are unconditional.
3.  **Apply the Formula:** Use the conditional probability or multiplication theorem based on the problem's requirements.  If appropriate, break the problem down using total probability theorem or Bayes' theorem.
4.  **Calculate Probabilities:**  Determine the probabilities of individual events and their intersections.  This often involves combinatorics.
5.  **Solve and Verify:**  Plug in the values and solve for the unknown probability. Double-check your answer for reasonableness (probability should be between 0 and 1).

**4. Quick Tips:**

*   **Venn Diagrams:** Use Venn diagrams to visualize events and their intersections, especially for simpler problems.
*   **Tree Diagrams:** Construct tree diagrams to track sequential events and their associated probabilities for easier calculation of \(P(A \cap B)\).

**5. Common Mistakes:**

*   **Confusing P(A|B) and P(B|A):** These are NOT the same unless P(A) = P(B).
*   **Incorrectly applying Total Probability Theorem:** Ensure that events are mutually exclusive and exhaustive.
*   **Not considering the "given" condition:** In conditional probability, the sample space is reduced to the event that is given.  This changes probabilities of subsequent events.
