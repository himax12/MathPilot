---
chapter: permutations-and-combinations
topic: divisibility-of-numbers
jee_frequency: 6
years_appeared: [2002, 2018, 2021, 2022, 2023, 2025]
question_count: 8
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Permutations And Combinations: Divisibility Of Numbers

**JEE Frequency**: Appeared in **6 years** (2002 - 2025)

**Question Count**: 8 questions

## Question Types

- **MCQ**: 3 questions
- **INTEGER**: 5 questions

## Difficulty Distribution

- **Medium**: 7 questions
- **Hard**: 1 questions

## Worked Examples

### Example 1 (Year: 2002)

**Question:**

The sum of integers from 1 to 100 that are divisible by 2 or 5 is :

**Solution:**

According to this question, any number between 1 to 100 should be divisible by 2 or 5 but not by 2$$ \times $$5 = 10.
<br><br>Possible numbers between 1 to 100 divisible by 2 are 2, 4, 6, .... , 100
<br><br>This is an A.P where first term = 2, last term = 100 and total terms = 50.
<br><br>$$ \therefore $$ Sum of the numbers divisible by 2
<br><br> = $${{50} \over 2}\left[ {2 + 100} \right]$$
<br><br>= 25$$ \times $$102
<br><br>= 2550
<br><br>Possible numbers between 1 to 100 divisible by 5 are 5, 10, 15, .... , 100
<br><br>$$ \therefore $$ Sum of the numbers divisible by 5
<br><br> = $${{20} \over 2}\left[ {5 + 100} \right]$$
<br><br>= 10$$ \times $$105
<br><br>= 1050
<br><br> And possible numbers between 1 to 100 divisible by 10 are 10, 20, 30, .... , 100
<br><br>$$ \therefore $$ Sum of the numbers divisible by 10
<br><br> = $${{10} \over 2}\left[ {10 + 100} \right]$$
<br><br>= 5$$ \times $$110
<br><br>= 550
<br><br>$$ \therefore $$ Required sum = 2550 + 1050 - 550 = 3050

### Example 2 (Year: 2018)

**Question:**

The number of numbers between 2,000 and 5,000 that can be formed with the digits 0, 1, 2, 3, 4 (repetition of digits is not allowed) and are multiple of 3 is : 

**Solution:**

Here number should be divisible by 3, that means sum of numbers should be divisible by 3.
<br><br>Possible 4 digits among 0, 1, 2, 3, 4 which are divisible by 3 are 
<br><br>(1)$$\,\,\,\,$$ (0, 2, 3, 4) Sum of digits = 0 + 2 + 3 +4 = 9 (divisible by 3)
<br><br>(2) $$\,\,\,\,$$ (0, 1, 2, 3) Sum of digits = 0 + 1 + 2 + 3 = 6 (divisible by 3)
<br><br><b><u>Case 1</u> :</b> 
<br><br>When 4 digits are (0, 2, 3, 4) then
<br><br><img src="https://imagex.cdn.examgoal.net/3R4b82BWeqZkJMFfg/OxOYkm43wKbY12PT0KKtsriR1dki0/JRv8CIoiECylgeiXoiRy0b/image.png" style="max-width: 100%;  height: auto;display: block;margin: 0 auto;" loading="lazy" alt="JEE Main 2018 (Online) 16th April Morning Slot Mathematics - Permutations and Combinations Question 172 English Explanation 1"><br><br>$$\therefore\,\,\,\,$$ Total possible numbers = $$^3{C_1}$$ $$ \times $$ $$^3{C_1}$$ $$ \times $$ $$^2{C_1}$$ $$ \times $$ $$^1{C_1}$$ 
<br><br>= &nbsp;&nbsp; 3 $$ \times $$ 3 $$ \times $$ 2 $$ \times $$ 1 = 18
<br><br><b><u>...

### Example 3 (Year: 2021)

**Question:**

A natural number has prime factorization given by n = 2<sup>x</sup>3<sup>y</sup>5<sup>z</sup>, where y and z are such <br>that y + z = 5 and y<sup>$$-$$1</sup> + z<sup>$$-$$1</sup> = $${5 \over 6}$$, y &gt; z. Then the number of odd divisions of n, including 1, is :

**Solution:**

y + z = 5 ....... (1)<br><br>$${1 \over y} + {1 \over z} = {5 \over 6}$$<br><br>$$ \Rightarrow {{y + z} \over {yz}} = {5 \over 6}$$<br><br>$$ \Rightarrow {5 \over {yz}} = {5 \over 6}$$<br><br>$$ \Rightarrow $$ yz = 6<br><br>Also, (y $$-$$ z)<sup>2</sup> = (y + z)<sup>2</sup> $$-$$ 4yz<br><br>$$ \Rightarrow $$ (y $$-$$ z)<sup>2</sup> = (y + z)<sup>2</sup> $$-$$ 4yz<br><br>$$ \Rightarrow $$ (y $$-$$ z)<sup>2</sup> = 25 $$-$$ 4(6) = 1<br><br>$$ \Rightarrow $$ y $$-$$ z = 1 ..... (2)<br><br>from (1) and (2), y = 3 and z = 2<br><br>for calculating odd divisor of p = 2<sup>x</sup> . 3<sup>y</sup> . 5<sup>z</sup><br><br>x must be zero<br><br>P = 2<sup>0</sup> . 3<sup>3</sup> . 5<sup>2</sup> <br><br>$$ \Rightarrow $$ Total possible cases = (3<sup>0</sup>5<sup>0</sup> + 3<sup>1</sup>5<sup>0</sup> + 3<sup>2</sup>5<sup>0</sup> + 3<sup>3</sup>5<sup>0</sup> + .... + 3<sup>3</sup>5<sup>2</sup>)<br><br>$$ \therefore $$ Total odd divisors must be (3 + 1) ( 2 + 1) = 12

### Example 4 (Year: 2021)

**Question:**

Let n be a non-negative integer. Then the number of divisors of the form "4n + 1" of the number (10)<sup>10</sup> . (11)<sup>11</sup> . (13)<sup>13</sup> is equal to __________.

**Solution:**

N = 2<sup>10</sup> $$\times$$ 5<sup>10</sup> $$\times$$ 11<sup>11</sup> $$\times$$ 13<sup>13</sup><br><br>Now, power of 2 must be zero,<br><br>power of 5 can be anything,<br><br>power of 13 can be anything<br><br>But, power of 11 should be even.<br><br>So, required number of divisors is <br><br>1 $$\times$$ 11 $$\times$$ 14 $$\times$$ 6 = 924

### Example 5 (Year: 2022)

**Question:**

<p>The total number of 3-digit numbers, whose greatest common divisor with 36 is 2, is ___________.</p>

**Solution:**

<p>$$\because$$ x $$\in$$ [100, 999], x $$\in$$ N</p>
<p>Then $${x \over 2}$$ $$\in$$ [50, 499], $${x \over 2}$$ $$\in$$ N</p>
<p>Number whose G.C.D. with 18 is 1 in this range have the required condition. There are 6 such number from 18 $$\times$$ 3 to 18 $$\times$$ 4. Similarly from 18 $$\times$$ 4 to 18 $$\times$$ 5 ......., 26 $$\times$$ 18 to 27 $$\times$$ 18</p>
<p>$$\therefore$$ Total numbers = 24 $$\times$$ 6 + 6 = 150</p>
<p>The extra numbers are 53, 487, 491, 493, 497 and 499.</p>
