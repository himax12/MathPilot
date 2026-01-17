---
chapter: sets-and-relations
topic: symmetric-transitive-and-reflexive-properties
jee_frequency: 13
years_appeared: [2004, 2005, 2006, 2008, 2010, 2011, 2018, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 47
difficulty: medium
---

# Sets And Relations: Symmetric Transitive And Reflexive Properties

**JEE Frequency**: 13 years | **Questions**: 47

## Sets and Relations: Symmetric, Transitive, and Reflexive Properties - JEE Knowledge Base

**JEE Frequency:** High (13 years, 47 questions)

**1. Pattern Recognition:**

*   Questions involve determining whether a given relation `R` on a set `A` satisfies reflexive, symmetric, or transitive properties (or combinations thereof).
*   The relation `R` is often explicitly defined as a set of ordered pairs. Sometimes `R` is defined verbally.

**2. Core Formulas:**

*   **Reflexive:**  $\forall a \in A, (a, a) \in R$
*   **Symmetric:** $\forall a, b \in A, \text{if } (a, b) \in R \text{ then } (b, a) \in R$
*   **Transitive:** $\forall a, b, c \in A, \text{if } (a, b) \in R \text{ and } (b, c) \in R \text{ then } (a, c) \in R$

**3. Standard Approach:**

1.  **Reflexivity:** Check if `(a, a)` is in `R` for *every* element `a` in set `A`. If even one element fails, `R` is *not* reflexive.
2.  **Symmetry:**  For *every* `(a, b)` in `R`, check if `(b, a)` is also in `R`. If even one pair fails, `R` is *not* symmetric.
3.  **Transitivity:** For *every* pair of ordered pairs `(a, b)` and `(b, c)` in `R`, check if `(a, c)` is also in `R`.  If even one triple fails, `R` is *not* transitive.
4.  **Careful with empty conditions:** If symmetry or transitivity have no element in the set to fulfill their condition, it is considered true.

**4. Quick Tips:**

*   **Counterexamples are Powerful:** To prove a property *doesn't* hold, a single counterexample is sufficient.
*   **Simplify Verbal Relations:** If `R` is defined verbally, try to write out a few example pairs to understand its behavior.

**5. Common Mistakes:**

*   **Forgetting to check ALL elements for reflexivity:** Don't stop after checking a few; verify for every element in `A`.
*   **Confusing necessary and sufficient conditions:** Symmetry requires *if* `(a, b)` is in `R`, *then* `(b, a)` must *also* be in `R`. If `(a, b)` is *not* in `R`, you *don't* need to check for `(b, a)`.
*   **Incorrectly applying transitivity:** Make sure to consider *all* pairs `(a, b)` and `(b, c)` in `R` and check if `(a, c)` is also present.
