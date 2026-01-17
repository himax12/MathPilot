---
chapter: permutations-and-combinations
topic: conditional-permutations
jee_frequency: 10
years_appeared: [2002, 2004, 2008, 2016, 2019, 2020, 2021, 2022, 2023, 2025]
question_count: 53
difficulty: medium
---

# Permutations And Combinations: Conditional Permutations

**JEE Frequency**: 10 years | **Questions**: 53

## Permutations and Combinations: Conditional Permutations (JEE Focus)

**JEE Frequency (10 Years):** High (53 Questions)

**1. Pattern Recognition:**

*   Problem explicitly states a condition or constraint that limits the choices available at each step (e.g., digits must be odd, vowels must be in order, certain letters cannot be adjacent).
*   Problem asks for number of arrangements/selections under specific restrictions, often involving digits, letters, or objects with particular properties.

**2. Core Formulas:**

*   **Fundamental Principle of Counting (Multiplication):** If one event can occur in *m* ways and another event can occur in *n* ways, then both events can occur in *m* × *n* ways.
*   **Permutation:**  $^nP_r = \frac{n!}{(n-r)!}$  (Arrangement of *r* items from *n* distinct items)
*   **Combination:** $^nC_r = \frac{n!}{r!(n-r)!}$ (Selection of *r* items from *n* distinct items)
*   **Permutation with Repetition (of *p*, *q*, *r* items):** $\frac{n!}{p!q!r!}$

**3. Standard Approach:**

1.  **Identify the Condition:** Clearly state the restrictive condition(s) in the problem.
2.  **Break into Cases (if needed):** If the condition is complex, divide the problem into mutually exclusive and exhaustive cases.
3.  **Fulfill the Condition First:** Handle the restricted positions/elements first, filling them according to the given condition.
4.  **Fill Remaining Positions:**  Fill the remaining positions using the remaining elements, considering any further restrictions.
5.  **Apply FPC and Sum Cases:** Multiply the number of possibilities at each step using the Fundamental Principle of Counting. Sum the results from all the cases if they exist.

**4. Quick Tips:**

*   **Gap Method (for Non-Adjacent Elements):** Arrange the non-restricted elements first, then place the restricted elements in the gaps created.
*   **Divisibility Rules:** Remember divisibility rules for 3, 4, 5, 9, 11 etc. to quickly reduce options for digit-based problems.

**5. Common Mistakes:**

*   **Double Counting:** Be careful not to overcount when dealing with multiple cases or repetitive elements. Use the principle of inclusion-exclusion if necessary.
*   **Zero at Leading Position:** In digit-based problems, remember that a zero cannot be the leading digit of a number. Account for this when calculating possibilities.
*   **Not considering "Without Repetition" :** Read the question carefully. Often, the biggest mistake is assuming something when it isn't given.
