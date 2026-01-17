---
chapter: probability
topic: permutation-and-combination-based-problem
jee_frequency: 11
years_appeared: [2010, 2015, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 30
difficulty: medium
---

# Probability: Permutation And Combination Based Problem

**JEE Frequency**: 11 years | **Questions**: 30

## Probability: Permutation & Combination Based Problems (JEE Knowledge Base)

**JEE Frequency:** 11 years
**Question Count:** 30 questions

**1. Pattern Recognition:**

*   The problem involves selecting items (people, balls, numbers) and forming groups/arrangements/committees.
*   Keywords like "at random", "without replacement", "committee", "arrangements", "probability of specific configuration" are indicative.
*   Often involves calculating the ratio of favorable outcomes to the total possible outcomes using combinatorial principles.

**2. Core Formulas:**

*   Number of combinations:  ${n \choose r} = \frac{n!}{r!(n-r)!}$
*   Number of permutations: $P(n, r) = \frac{n!}{(n-r)!}$
*   Addition Rule of Probability (Mutually Exclusive Events): $P(A \cup B) = P(A) + P(B)$
*   Conditional Probability:  $P(A|B) = \frac{P(A \cap B)}{P(B)}$
*   Total Probability Theorem: $P(A) = \sum_{i=1}^{n} P(A|B_i)P(B_i)$ where $B_i$ are mutually exclusive and exhaustive.

**3. Standard Approach:**

1.  **Define Events:** Clearly define the event whose probability you need to find.
2.  **Calculate Total Possible Outcomes (Sample Space):** Determine the total number of ways to select or arrange items without any restrictions. Use ${n \choose r}$ or $P(n,r)$ depending on whether order matters.
3.  **Calculate Favorable Outcomes:**  Determine the number of ways the desired event can occur. This often involves breaking down the event into smaller, manageable cases. Use casework and combine the results using the addition rule.
4.  **Calculate Probability:** Divide the number of favorable outcomes by the total number of possible outcomes:  $P(Event) = \frac{\text{Favorable Outcomes}}{\text{Total Outcomes}}$
5.  **Simplify:** Simplify the probability expression and check for any logical errors.

**4. Quick Tips:**

*   **Identical Objects/Boxes:**  If placing *n* distinct objects into *k* identical boxes, consider using the Stirling Numbers of the Second Kind if applicable.  For placing *n* identical objects into *k* distinct boxes, use stars and bars method: ${n+k-1 \choose k-1}$.
*   **Casework Strategy:** Complex problems are often solved by breaking down the desired event into mutually exclusive cases. Calculate the probability of each case separately, then sum them up.
*   **Complementary Probability:** Sometimes it's easier to calculate the probability of the event *not* happening and subtract it from 1: $P(A) = 1 - P(A')$.

**5. Common Mistakes:**

*   **Order vs. Combination Confusion:** Incorrectly using permutations when combinations are required (and vice-versa). Carefully analyze whether the order of selection matters.
*   **Double Counting:** Ensure that you are not counting the same outcome multiple times, especially when using casework.
*   **Ignoring Restrictions:** Forgetting to account for constraints given in the problem (e.g., "at least one woman", "without replacement").
