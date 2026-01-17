---
chapter: permutations-and-combinations
topic: conditional-combinations
jee_frequency: 8
years_appeared: [2003, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 36
difficulty: medium
---

# Permutations And Combinations: Conditional Combinations

**JEE Frequency**: 8 years | **Questions**: 36

## Knowledge Base: Conditional Combinations (JEE Math)

**Chapter:** Permutations and Combinations
**Topic:** Conditional Combinations
**JEE Frequency:** 8 years
**Question Count:** 36 questions

**1. Pattern Recognition:**

*   The problem specifies conditions that *restrict* the selection of elements from different groups (e.g., at least 'x' from group A, specific individuals must/must not be together).
*   Keywords like "at least," "at most," "must include," "cannot include," and explicit restrictions on group composition are indicators.

**2. Core Formulas:**

*   Combination Formula:  $^nC_r = \frac{n!}{r!(n-r)!}$
*   Principle of Inclusion-Exclusion (for two sets):  $n(A \cup B) = n(A) + n(B) - n(A \cap B)$
*   Complementary Counting: Total number of ways - Number of ways violating the condition.
*   Summation of disjoint cases: If events are mutually exclusive, total ways = sum of ways of individual events.
*   Multiplication Principle: If one thing can be done in 'm' ways and a subsequent thing in 'n' ways, total ways to do both = m*n

**3. Standard Approach:**

1.  **Identify Groups & Constraints:** Clearly define the groups from which elements are selected and note down all conditional statements.
2.  **Case Formation:** Break the problem into mutually exclusive and exhaustive cases that satisfy the given conditions (e.g., "at least 2 boys" could be 2 boys & 1 girl, or 3 boys & 0 girls).
3.  **Calculate Individual Cases:** Use the combination formula  $^nC_r$ to calculate the number of ways to choose elements for each case. Remember the multiplication principle if selections from different groups are combined.
4.  **Sum the Cases:** Add up the results from all valid cases to get the final answer.
5.  **Consider Complementary Counting:** If direct calculation is complex, calculate the total possible outcomes and subtract the outcomes that *violate* the given conditions.

**4. Quick Tips:**

*   When dealing with "at least," consider using complementary counting (total - "none" - "one," etc.).
*   If specific elements must be together or excluded, treat them as a single unit or remove them from the possible selection, respectively.

**5. Common Mistakes:**

*   **Overlapping Cases:** Ensure that the cases you've defined are mutually exclusive.  Double-counting will lead to an incorrect answer.
*   **Ignoring the 'at least' or 'at most' conditions:** Carefully consider all the boundary conditions imposed.
*   **Incorrectly Applying Combination vs. Permutation:**  Remember that combination is used when order doesn't matter.  This is almost always the case in these Conditional Combination problems.
