---
chapter: permutations-and-combinations
topic: number-of-combinations
jee_frequency: 18
years_appeared: [2003, 2004, 2006, 2007, 2008, 2010, 2011, 2012, 2013, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 45
difficulty: medium
---

# Permutations And Combinations: Number Of Combinations

**JEE Frequency**: 18 years | **Questions**: 45

## Permutations and Combinations: Number of Combinations - JEE Knowledge Base

**JEE Frequency:** High (18 years, 45 questions)

**1. Pattern Recognition:**

*   Problems involve selecting groups of objects *without* considering order.
*   Keywords: "choose," "select," "form a group," "distribute identical objects," "combination," "committee," "team".
*   Often involve restrictions like minimum/maximum selections, identical objects, or distribution into distinct groups.

**2. Core Formulas:**

*   Combination Formula: $${}^n{C_r} = \frac{n!}{r!(n-r)!}$$
*   Properties: $${}^n{C_r} = {}^n{C_{n-r}}$$ , $${}^n{C_0} = {}^n{C_n} = 1$$ , $${}^n{C_1} = n$$
*   Pascal's Identity: $${}^n{C_r} + {}^n{C_{r-1}} = {}^{n+1}{C_r}$$
*   Sum of Combinations: $${}^n{C_0} + {}^n{C_1} + {}^n{C_2} + ... + {}^n{C_n} = 2^n$$
*   Stars and Bars (for identical objects into distinct boxes): Number of ways to distribute *n* identical objects into *r* distinct boxes: $${}^{n+r-1}{C_{r-1}}$$ (when each box can have 0 or more objects). If each box must have at least one object: $${}^{n-1}{C_{r-1}}$$

**3. Standard Approach:**

1.  **Identify 'n' and 'r':** Determine the total number of objects (n) and the number of objects to be chosen (r).
2.  **Check for Restrictions:** Note any constraints like minimum/maximum selections, or identical objects. Adapt formulas accordingly. Use stars and bars when distributing identical objects.
3.  **Apply the appropriate formula:** Choose the correct combination formula based on the problem and the presence of identical objects.
4.  **Simplify and Solve:** Simplify the factorial expressions to find the numerical answer.
5.  **Consider Multiple Cases (if necessary):** Break the problem into mutually exclusive cases and add the results if there are multiple ways to satisfy the condition.

**4. Quick Tips:**

*   **Complementary Counting:** If directly calculating the required combinations is difficult, find the total number of combinations and subtract the undesired ones. Total combinations = Desired combinations + Undesired Combinations.
*   **Pascal's Triangle:** Use Pascal's Triangle to quickly evaluate combinations for small values of *n* and *r*. Remember the rule: $${}^{n}{C_{r}} + {}^{n}{C_{r+1}} = {}^{n+1}{C_{r+1}}$$

**5. Common Mistakes:**

*   **Confusing Permutations and Combinations:** Ensure order *doesn't* matter before using combinations.
*   **Incorrectly Applying Stars and Bars:** Be careful to adjust the formula if there are minimum requirements for each box (i.e., each box must have at least one item).
*   **Forgetting to consider all cases:** Ensure that all possible valid arrangements are accounted for, especially in problems involving multiple constraints. Double check your solution.
