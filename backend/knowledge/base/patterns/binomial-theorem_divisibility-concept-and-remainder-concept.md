---
chapter: binomial-theorem
topic: divisibility-concept-and-remainder-concept
jee_frequency: 8
years_appeared: [2009, 2017, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 30
difficulty: medium
---

# Binomial Theorem: Divisibility Concept And Remainder Concept

**JEE Frequency**: 8 years | **Questions**: 30

## Binomial Theorem: Divisibility & Remainder Concepts (JEE)

**JEE Frequency:** High (8 years, 30 questions)

**1. Pattern Recognition:**

*   Problems involve finding remainders when expressions involving exponents are divided by a specific number.  Often, the exponents are large.
*   The expression to be divided often involves sums of powers or differences of powers.
*   Questions might ask for the *greatest* integer `k` such that an expression is divisible by another.

**2. Core Formulas:**

*   **Binomial Theorem:**  $(x+y)^n = \sum_{r=0}^{n} {n \choose r} x^{n-r} y^r$
*   **Remainder Theorem:** If P(x) is divided by (x-a), the remainder is P(a).
*   **Form:  Number = Quotient × Divisor + Remainder. i.e.,  N = QD + R**
*   **Important observation:** $(1 + x)^n = 1 + nx + $ terms involving $x^2$ and higher powers.
*   $a^n - b^n$ is divisible by $a-b$ for all $n \in \mathbb{N}$.
*   $a^n + b^n$ is divisible by $a+b$ for odd $n \in \mathbb{N}$.
*   $a^n - b^n$ is divisible by $a+b$ for even $n \in \mathbb{N}$.

**3. Standard Approach:**

1.  **Reduce to a Binomial Expansion:**  Express the base of the exponent as a sum or difference of a multiple of the divisor and a small number (usually 1 or -1).  Example: $8^{2n} = (9-1)^{2n}$.
2.  **Apply Binomial Theorem:** Expand the expression using the binomial theorem.
3.  **Identify Divisible Terms:**  All terms containing powers of the divisor will be divisible by it.
4.  **Isolate the Remainder:** The remainder will be the constant term (or the sum of constant terms and terms less than the divisor after simplification) after expanding and identifying the divisible terms. Simplify where necessary.
5.  **Consider Cyclicity/Patterns:** If the powers are very large, look for repeating patterns in the remainders.

**4. Quick Tips:**

*   **Modular Arithmetic:** Use modular arithmetic notation to simplify calculations. $a \equiv b \pmod{m}$ means a and b have the same remainder when divided by m. Example: $8 \equiv -1 \pmod{9}$.
*   **Focus on the Last Few Digits:**  For divisibility by powers of 2 or 5, focus on the last few digits of the number.
*   **Special Cases:** Recognize patterns like $a^2 - b^2 = (a+b)(a-b)$ to simplify expressions.  Look for opportunities to factorize.

**5. Common Mistakes:**

*   **Incorrect Application of Binomial Theorem:**  Double-check the coefficients and powers in the binomial expansion.
*   **Ignoring Negative Remainders:**  If you get a negative remainder, add the divisor to it to get the positive remainder.  For example, a remainder of -1 when dividing by 9 is equivalent to a remainder of 8.
*   **Overlooking Patterns:** Don't jump to brute-force calculation. Look for patterns in remainders as powers increase.
*   **Incorrect simplification**: Simplify the expression fully. Sometimes the expression still contains powers that can further be reduced.
