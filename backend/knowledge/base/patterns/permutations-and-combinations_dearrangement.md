---
chapter: permutations-and-combinations
topic: dearrangement
jee_frequency: 1
years_appeared: [2023]
question_count: 1
difficulty: medium
question_types: ['integer']
exams: ['mains']
---

# Permutations And Combinations: Dearrangement

**JEE Frequency**: Appeared in **1 years** (2023 - 2023)

**Question Count**: 1 questions

## Question Types

- **INTEGER**: 1 questions

## Difficulty Distribution

- **Medium**: 1 questions

## Worked Examples

### Example 1 (Year: 2023)

**Question:**

<p>In an examination, 5 students have been allotted their seats as per their roll numbers. The number of ways, in which none of the students sits on the allotted seat, is _________.</p>

**Solution:**

This problem can be solved using the concept of derangements, which is a permutation of objects where no object appears in its original position. In this case, we have 5 students who should not sit in their allotted seats. 

<br/><br/>The formula for calculating the number of derangements (also known as subfactorials) is :

<br/><br/>D(n) $$
=n !\left[\frac{1}{0!}-\frac{1}{1 !}+\frac{1}{2 !}-\frac{1}{3 !}+\frac{1}{4 !}-\ldots \ldots . .+(-1)^n \frac{1}{n !}\right]
$$

<br/><br/>Where n is the number of students, in this case, 5.

<br/><br/>Using the formula, let's calculate the derangements for 5 students :

<br/><br/>D(5) = $5! \left(\frac{1}{0!} - \frac{1}{1!} + \frac{1}{2!} - \frac{1}{3!} + \frac{1}{4!} - \frac{1}{5!}\right)$

<br/><br/>D(5) = $120 \left(1 - 1 + \frac{1}{2} - \frac{1}{6} + \frac{1}{24} - \frac{1}{120}\right)$

<br/><br/>D(5) = $120 \left(0 + \frac{1}{2} - \frac{1}{6} + \frac{1}{24} - \frac{1}{120}\right)$

<br/><br/>D(5) = $120 \left(\frac{1}{2} - \frac{1}{6} + \fra...
