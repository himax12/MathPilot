---
chapter: binomial-theorem
topic: multinomial-theorem
jee_frequency: 6
years_appeared: [2020, 2021, 2022, 2023, 2024, 2025]
question_count: 8
difficulty: medium
question_types: ['integer', 'mcq']
exams: ['mains']
---

# Binomial Theorem: Multinomial Theorem

**JEE Frequency**: Appeared in **6 years** (2020 - 2025)

**Question Count**: 8 questions

## Question Types

- **INTEGER**: 5 questions
- **MCQ**: 3 questions

## Difficulty Distribution

- **Medium**: 7 questions
- **Hard**: 1 questions

## Worked Examples

### Example 1 (Year: 2020)

**Question:**

Let $${\left( {2{x^2} + 3x + 4} \right)^{10}} = \sum\limits_{r = 0}^{20} {{a_r}{x^r}} $$<br><br>
Then $${{{a_7}} \over {{a_{13}}}}$$ is equal to ______.

**Solution:**

<b>Note : </b> <b>Multinomial Theorem : </b>
<br><br>The general term of $${\left( {{x_1} + {x_2} + ... + {x_n}} \right)^n}$$ the expansion is 
<br><br>$${{n!} \over {{n_1}!{n_2}!...{n_n}!}}x_1^{{n_1}}x_2^{{n_2}}...x_n^{{n_n}}$$
<br><br>where n<sub>1</sub> + n<sub>2</sub> + ..... + n<sub>n</sub> = n
<br><br>Here, in $${(2{x^2} + 3x + 4)^{10}}$$ general term is <br><br>$$ = {{10!} \over {{n_1}!{n_2}!{n_3}!}}{(2{x^2})^{{n_1}}}{(3x)^{{n_2}}}{(4)^{{n_3}}}$$<br><br>$$ = {{10!} \over {{n_1}!{n_2}!{n_3}!}}{.2^{{n_1}}}{.3^{{n_2}}}{.4^{{n_3}}}.{x^{2{n_1} + {n_2}}}$$<br><br>$$ \therefore $$ Coefficient of $$ {x^{2{n_1} + {n_2}}}$$  is <br><br>$${{10!} \over {{n_1}!{n_2}!{n_3}!}}{.2^{{n_1}}}{.3^{{n_2}}}{.4^{{n_3}}}$$<br><br>where $${n_1} + {n_2} + {n_3} = 10$$<br><br> For, Coefficient of x<sup>7</sup> : <br>2n<sub>1</sub> + n<sub>2</sub> = 7<br><br>Possible values of n<sub>1</sub>, n<sub>2</sub> and n<sub>3</sub> are <br><br><table>
<thead>
  <tr>
    <th>$${n_1}$$</th>
    <th>$${n_2}$$</th>
   ...

### Example 2 (Year: 2021)

**Question:**

If the coefficient of a<sup>7</sup>b<sup>8</sup> in the expansion of (a + 2b + 4ab)<sup>10</sup> is K.2<sup>16</sup>, then K is equal to _____________.

**Solution:**

$${{10!} \over {\alpha !\beta !\gamma !}}{a^\alpha }{(2b)^\beta }.{(4ab)^\gamma }$$<br><br>$${{10!} \over {\alpha !\beta !\gamma !}}{a^{\alpha  + \gamma }}.\,{b^{\beta  + \gamma }}\,.\,{2^\beta }\,.\,{4^\gamma }$$<br><br>$$\alpha  + \beta  + \gamma  = 10$$ ..... (1)<br><br>$$\alpha  + \gamma  = 7$$ .... (2)<br><br>$$\beta  + \gamma  = 8$$ ..... (3)<br><br>$$(2) + (3) - (1) \Rightarrow \gamma  = 5$$<br><br>$$\alpha  = 2$$<br><br>$$\beta  = 3$$<br><br>so coefficients = $${{10!} \over {2!3!5!}}{2^3}{.2^{10}}$$<br><br>$$ = {{10 \times 9 \times 8 \times 7 \times 6 \times 5} \over {2 \times 3 \times 2 \times 5!}} \times {2^{13}}$$<br><br>$$ = 315 \times {2^{16}} \Rightarrow k = 315$$

### Example 3 (Year: 2022)

**Question:**

<p>If the constant term in the expansion of 
<br/><br/>$${\left( {3{x^3} - 2{x^2} + {5 \over {{x^5}}}} \right)^{10}}$$ is 2<sup>k</sup>.l, where l is an odd integer, then the value of k is equal to:</p>

**Solution:**

<b>Note : </b> <b>Multinomial Theorem : </b>
<br><br>The general term of $${\left( {{x_1} + {x_2} + ... + {x_n}} \right)^n}$$ the expansion is 
<br><br>$${{n!} \over {{n_1}!{n_2}!...{n_n}!}}x_1^{{n_1}}x_2^{{n_2}}...x_n^{{n_n}}$$
<br><br>where n<sub>1</sub> + n<sub>2</sub> + ..... + n<sub>n</sub> = n
<br/><br/><p>Given,</p>
<p>$${\left( {3{x^2} - 2{x^2} + {5 \over {{x^5}}}} \right)^{10}}$$</p>
<p>$$ = {{{{(3{x^8} - 2{x^7} + 5)}^{10}}} \over {{x^{50}}}}$$</p>
<p>Now constant term in $${\left( {3{x^3} - 2{x^2} + {5 \over {{x^5}}}} \right)^{10}} = {x^{50}}$$ term in $${(3{x^8} - 2{x^7} + 5)^{10}}$$</p>
<p>General term in $${(3{x^8} - 2{x^7} + 5)^{10}}$$ is</p>
<p>$$ = {{10!} \over {{n_1}!\,{n_2}!\,{n_3}!}}{(3{x^8})^{{n_1}}}{( - 2{x^7})^{{n_2}}}{(5)^{{n_3}}}$$</p>
<p>$$ = {{10!} \over {{n_1}!\,{n_2}!\,{n_3}!}}{(3)^{{n^1}}}{( - 2)^{{n_2}}}{(5)^{{n^3}}}\,.\,{x^{8{n_1} + 7{n_2}}}$$</p>
<p>$$\therefore$$ Coefficient of $${x^{8{n_1} + 7{n_2}}}$$ is</p>
<p>$$ = {{10!} \over {{n_1}!\,{n_2}!\,{n_3}...

### Example 4 (Year: 2023)

**Question:**

Let $\left(a+b x+c x^{2}\right)^{10}=\sum\limits_{i=0}^{20} p_{i} x^{i}, a, b, c \in \mathbb{N}$.<br/><br/> If $p_{1}=20$ and $p_{2}=210$, then

$2(a+b+c)$ is equal to :

**Solution:**

<p>We are given that $\left(a+bx+cx^2\right)^{10} = \sum_{i=0}^{20} p_i x^i$, and we are given that $p_1 = 20$ and $p_2 = 210$.<br/><br/> We need to find the value of $2(a+b+c)$.</p>
Using the multinomial theorem, we can express the expansion of $(a + bx + cx^2)^{10}$ as follows:

<br/><br/>$$
\sum\limits_{k_1+k_2+k_3=10} {{10!} \over {{k_1}!{k_2}!{k_3}!}} a^{k_1} (bx)^{k_2} (cx^2)^{k_3}
$$

<br/><br/>Now we need to find the coefficients of $x^1$ and $x^2$ in the expansion:

<br/><br/>For $x^1$ term, we have:
<br/><br/>$$
k_2 = 1, k_1 = 9, k_3 = 0
$$

<br/><br/>So,
<br/><br/>$$
p_1 = {{10!} \over {9!1!0!}} a^9 b^1 = 10a^9 b
$$

<br/><br/>For $x^2$ term, there are two possibilities:
<br/><br/>$$
k_2 = 2, k_1 = 8, k_3 = 0 \quad \text{and} \quad k_2 = 0, k_1 = 9, k_3 = 1
$$

<br/><br/>So,
<br/><br/>$$
p_2 = {{10!} \over {8!2!0!}} a^8 b^2 + {{10!} \over {9!0!1!}} a^9 c = 45a^8 b^2 + 10a^9 c
$$

<p>Now we are given $p_1 = 20$ and $p_2 = 210$. So,
$$
10a^9 b = 20 \implies a^9 b = 2
$$</p>
<p...

### Example 5 (Year: 2023)

**Question:**

<p>The coefficient of $$x^7$$ in $${(1 - x + 2{x^3})^{10}}$$ is ___________.</p>

**Solution:**

Given expression is $\left(1-x+2 x^3\right)^{10}$
<br/><br/>So, general term is $\frac{10 !}{r_{1} ! r_{2} ! r_{3} !}(1)^{r_1}(-1)^{r_2} \cdot(2)^{r_3} \cdot(x)^{r_2+r_3}$
<br/><br/>Where, $r_1+r_2+r_3=10$ and $r_2+3 r_3=7$
<br/><br/>Now, for possibility,
<br/><br/>$\begin{array}{ccc}r_1 & r_2 & r_3 \\ 3 & 7 & 0 \\ 7 & 1 & 2 \\ 5 & 4 & 1\end{array}$
<br/><br/>Thus, required co-efficient
<br/><br/>$$
\begin{aligned}
& =\frac{10 !}{3 ! 7 !}(-1)^7+\frac{10 !}{5 ! 4 !}(-1)^4(2)+\frac{10 !}{7 ! 2 !}(-1)^1(2)^2 \\\\
& =-120+2520-1440 \\\\
& =2520-1560=960
\end{aligned}
$$
