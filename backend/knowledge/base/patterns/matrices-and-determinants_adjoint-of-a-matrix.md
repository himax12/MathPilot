---
chapter: matrices-and-determinants
topic: adjoint-of-a-matrix
jee_frequency: 5
years_appeared: [2016, 2017, 2023, 2024, 2025]
question_count: 17
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Matrices And Determinants: Adjoint Of A Matrix

**JEE Frequency**: Appeared in **5 years** (2016 - 2025)

**Question Count**: 17 questions

## Question Types

- **MCQ**: 13 questions
- **INTEGER**: 4 questions

## Difficulty Distribution

- **Medium**: 13 questions
- **Hard**: 4 questions

## Worked Examples

### Example 1 (Year: 2016)

**Question:**

If $$A = \left[ {\matrix{
   {5a} &amp; { - b}  \cr 
   3 &amp; 2  \cr 

 } } \right]$$  and $$A$$ adj $$A=A$$ $${A^T},$$ then $$5a+b$$ is equal to :

**Solution:**

$$A\left( {Adj\,\,A} \right) = A\,{A^T}$$
<br><br>$$ \Rightarrow {A^{ - 1}}A\left( {adj\,\,A} \right) = {A^{ - 1}}A\,{A^T}$$
<br><br>$$Adj\,\,A = {A^T}$$
<br><br>$$ \Rightarrow \left[ {\matrix{
   2 &amp; b  \cr 
   { - 3} &amp; {5a}  \cr 

 } } \right] = \left[ {\matrix{
   {5a} &amp; 3  \cr 
   { - b} &amp; 2  \cr 

 } } \right]$$
<br><br>$$ \Rightarrow a = {2 \over 5}\,\,$$ and $$\,\,b = 3$$
<br><br>$$ \Rightarrow 5a + b = 5$$ 

### Example 2 (Year: 2017)

**Question:**

Let A be any 3 $$ \times $$ 3 invertible matrix. Then which one of the following is <b>not</b> always true ? 

**Solution:**

We know, the formula
<br><br>A<sup>-1</sup> = $${{adj\left( A \right)} \over {\left| A \right|}}$$
<br><br>$$ \therefore $$ adj (A) = $$\left|  \right.$$A$$\left| \right.$$.A<sup>$$-$$1</sup>
<br><br><b>So, Option (A) is true.</b>
<br><br>We know, the formula
<br><br>adj (adj (A)) = $${\left| A \right|^{n - 2}}.A$$
<br><br>Now if we put n = 3 as given that A is a 3 $$ \times $$ 3 matrix, we get
<br><br>adj (adj (A)) = $${\left| A \right|^{3 - 2}}.A$$ = $$\left| A \right|.A$$
<br><br><b>So, Option (B) is also true.</b>
<br><br>We know, the formula
<br><br>adj (adj (A)) = $${\left| A \right|^{n - 1}}{\left( {adj\left( A \right)} \right)^{ - 1}}$$
<br><br>Now if we put n = 3 as given that A is a 3 $$ \times $$ 3 matrix, we get
<br><br>adj (adj (A)) = $${\left| A \right|^{3 - 1}}{\left( {adj\left( A \right)} \right)^{ - 1}}$$ = $${\left| A \right|^{2}}{\left( {adj\left( A \right)} \right)^{ - 1}}$$
<br><br><b>So, Option (C) is also true.</b>
<br><br>Now in this formula
<br><br>adj (adj (A)...

### Example 3 (Year: 2017)

**Question:**

If $$A = \left[ {\matrix{
   2 &amp; { - 3}  \cr 
   { - 4} &amp; 1  \cr 

 } } \right]$$,
<br><br>then adj(3A<sup>2</sup> + 12A) is equal to

**Solution:**

We have, $$A = \left[ {\matrix{
   2 &amp; { - 3}  \cr 
   { - 4} &amp; 1  \cr 

 } } \right]$$
<br><br>$$ \therefore $$ A<sup>2</sup> = A.A = $$\left[ {\matrix{
   2 &amp; { - 3}  \cr 
   { - 4} &amp; 1  \cr 

 } } \right]\left[ {\matrix{
   2 &amp; { - 3}  \cr 
   { - 4} &amp; 1  \cr 

 } } \right]$$
<br><br>= $$\left[ {\matrix{
   {4 + 12} &amp; { - 6 - 3}  \cr 
   { - 8 - 4} &amp; {12 + 1}  \cr 

 } } \right]$$
<br><br>= $$\left[ {\matrix{
   {16} &amp; { - 9}  \cr 
   { - 12} &amp; {13}  \cr 

 } } \right]$$
<br><br>Now, 3A<sup>2</sup> + 12A 
<br><br>= $$3\left[ {\matrix{
   {16} &amp; { - 9}  \cr 
   { - 12} &amp; {13}  \cr 

 } } \right] + 12\left[ {\matrix{
   2 &amp; { - 3}  \cr 
   { - 4} &amp; 1  \cr 

 } } \right]$$
<br><br>= $$\left[ {\matrix{
   {48} &amp; { - 27}  \cr 
   { - 36} &amp; {39}  \cr 

 } } \right] + \left[ {\matrix{
   {24} &amp; { - 36}  \cr 
   { - 48} &amp; {12}  \cr 

 } } \right]$$
<br><br>= $$\left[ {\matrix{
   {72} &amp; { - 63}  \cr 
   { - 84} &amp...

### Example 4 (Year: 2023)

**Question:**

<p>Let $$B=\left[\begin{array}{lll}1 & 3 & \alpha \\ 1 & 2 & 3 \\ \alpha & \alpha & 4\end{array}\right], \alpha > 2$$ be the adjoint of a matrix $$A$$ and $$|A|=2$$. Then 
$$\left[\begin{array}{ccc}\alpha & -2 \alpha & \alpha\end{array}\right] B\left[\begin{array}{c}\alpha \\ -2 \alpha \\ \alpha\end{array}\right]$$ is equal to :</p>

**Solution:**

$$
B=\left[\begin{array}{lll}
1 & 3 & \alpha \\
1 & 2 & 3 \\
\alpha & \alpha & 4
\end{array}\right], \alpha>2
$$
<br/><br/>And $\operatorname{adj}(A)=B,|A|=2$
<br/><br/>$$
\begin{aligned}
& \Rightarrow|\operatorname{adj}(A)|=|B| \\\\
& \Rightarrow 2^2=(8-3 \alpha)-3(4-3 \alpha)+\alpha(-\alpha) \\\\
& \Rightarrow \alpha^2-6 \alpha+8=0
\end{aligned}
$$
<br/><br/>$$
\begin{aligned}
\Rightarrow & (\alpha-4)(\alpha-2)=0 \\\\
& \alpha=4,2 \text { but } \alpha>2 \text { so } \alpha=4
\end{aligned}
$$
<br/><br/>Now
<br/><br/>$$
\begin{aligned}
& {\left[\begin{array}{ccc}\alpha & -2 \alpha & \alpha\end{array}\right] B\left[\begin{array}{c}
\alpha \\
-2 \alpha \\
\alpha
\end{array}\right]=\left[\begin{array}{lll}
4-8 & 4
\end{array}\right]\left[\begin{array}{lll}
1 & 3 & 4 \\
1 & 2 & 3 \\
4 & 4 & 4
\end{array}\right]\left[\begin{array}{c}
4 \\
-8 \\
4
\end{array}\right]} \\\\
& =\left[\begin{array}{lll}
12 & 12 & 8
\end{array}\right]\left[\begin{array}{c}
4 \\
-8 \\
4
\end{array}\right] \\\\
& =...

### Example 5 (Year: 2023)

**Question:**

<p>Let $$A=\left[\begin{array}{ccc}2 & 1 & 0 \\ 1 & 2 & -1 \\ 0 & -1 & 2\end{array}\right]$$. If $$|\operatorname{adj}(\operatorname{adj}(\operatorname{adj} 2 A))|=(16)^{n}$$, then $$n$$ is equal to :</p>

**Solution:**

We have,
<br/><br/>$$
\begin{aligned}
& |\mathrm{A}|=\left|\begin{array}{ccc}
2 & 1 & 0 \\
1 & 2 & -1 \\
0 & -1 & 2
\end{array}\right|=2(4-1)-1(2-0)+0 \\\\
& =6-2=4 \\\\
& \text { So, }|2 \mathrm{~A}|=2^3|\mathrm{~A}|=8 \times 4=32 \\\\
& \text { Now, }|\operatorname{adj}(\operatorname{adj}(\operatorname{adj} 2 \mathrm{~A}))|=|2 \mathrm{~A}|^{(n-1)^3} \\\\
& =(32)^{2^3}=32^8 \\\\
& \Rightarrow 16^n=(32)^8=2^8 \times 16^8 \\\\
& \Rightarrow 16^n=16^{2+8} \Rightarrow n=10
\end{aligned}
$$
<br/><br/><b>Concepts :</b>
<br/><br/>(a) $|k \mathrm{~A}|=k^n|\mathrm{~A}|$
<br/><br/>(b) $|\operatorname{adj} \mathrm{A}|=|\mathrm{A}|^{n-1}$
