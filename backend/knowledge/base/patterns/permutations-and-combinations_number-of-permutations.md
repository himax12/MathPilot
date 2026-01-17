---
chapter: permutations-and-combinations
topic: number-of-permutations
jee_frequency: 12
years_appeared: [2005, 2009, 2015, 2016, 2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 38
difficulty: medium
---

# Permutations And Combinations: Number Of Permutations

**JEE Frequency**: 12 years | **Questions**: 38

## Permutations and Combinations: Number of Permutations (JEE Focus)

**JEE Frequency:** High (12 years, 38 questions)

**1. Pattern Recognition:**

*   Arranging objects (letters, digits, people, etc.) in a specific order.
*   Finding the rank/position of a word in a dictionary order.
*   Forming numbers with specific digit constraints and non-repetition.

**2. Core Formulas:**

*   Permutation of *n* distinct objects taken *r* at a time:  $^nP_r = \frac{n!}{(n-r)!}$
*   Permutation of *n* objects where *p* are alike of one kind, *q* are alike of another kind, and so on: $\frac{n!}{p!q!...}$
*   Permutation with repetition allowed (r selections from n): $n^r$
*   Circular permutation of *n* distinct objects: $(n-1)!$
*   Circular permutation of *n* distinct objects, where clockwise and anticlockwise arrangements are indistinguishable (e.g., necklace): $\frac{(n-1)!}{2}$

**3. Standard Approach:**

1.  **Identify Distinct/Identical Objects:** Determine if objects are unique or have repetitions.
2.  **Apply Correct Formula:** Choose the appropriate permutation formula based on object types and constraints (repetition allowed/not allowed, circular/linear arrangement).
3.  **Handle Constraints:** Address restrictions such as specific objects being together, not together, or occupying certain positions.  Often, solve the unrestricted case and subtract unwanted arrangements.
4.  **Dictionary Order Problems:** Calculate the number of words lexicographically *smaller* than the target word.  This involves summing permutations with fixed prefixes.
5.  **Calculate and Simplify:** Carefully calculate the final answer, simplifying factorial expressions where possible.

**4. Quick Tips:**

*   **Gap Method:** For problems where objects *must* be separated, arrange the other objects first, then place the separating objects in the gaps.
*   **Tie Objects Together:** For problems where objects *must* be together, treat them as a single unit. Remember to permute the tied objects internally.
*   **Use Principle of Inclusion Exclusion (PIE):** If you have overlapping cases, use PIE to avoid overcounting: $|A \cup B| = |A| + |B| - |A \cap B|$

**5. Common Mistakes:**

*   **Forgetting to permute internally:** When objects are tied together, remember to permute them within the tie.
*   **Incorrectly identifying distinct/identical objects:** Careless misidentification leads to wrong formula usage.
*   **Not considering all cases in dictionary order problems:** Ensure that all permutations lexicographically smaller than the target word are accounted for. Remember leading zeros can be a problem in number formation problems.
