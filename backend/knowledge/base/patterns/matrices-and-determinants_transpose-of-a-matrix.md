---
chapter: matrices-and-determinants
topic: transpose-of-a-matrix
jee_frequency: 9
years_appeared: [2015, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024]
question_count: 12
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Matrices And Determinants: Transpose Of A Matrix

**JEE Frequency**: Appeared in **9 years** (2015 - 2024)

**Question Count**: 12 questions

## Question Types

- **MCQ**: 10 questions
- **INTEGER**: 2 questions

## Difficulty Distribution

- **Medium**: 10 questions
- **Easy**: 2 questions

## Worked Examples

### Example 1 (Year: 2015)

**Question:**

If $$A = \left[ {\matrix{
   1 &amp; 2 &amp; 2  \cr 
   2 &amp; 1 &amp; { - 2}  \cr 
   a &amp; 2 &amp; b  \cr 

 } } \right]$$ is a matrix satisfying the equation 
<br/><br>$$A{A^T} = 9\text{I},$$ where $$I$$ is $$3 \times 3$$ identity matrix, then the ordered 
<br/><br>pair $$(a, b)$$ is equal to :

**Solution:**

$$\left[ {\matrix{
   1 &amp; 2 &amp; 2  \cr 
   2 &amp; 1 &amp; { - 2}  \cr 
   a &amp; 2 &amp; b  \cr 

 } } \right]\left[ {\matrix{
   1 &amp; 2 &amp; a  \cr 
   2 &amp; 1 &amp; 2  \cr 
   2 &amp; { - 2} &amp; b  \cr 

 } } \right] = \left[ {\matrix{
   9 &amp; 0 &amp; 0  \cr 
   0 &amp; 9 &amp; 0  \cr 
   0 &amp; 0 &amp; 9  \cr 

 } } \right]$$
<br><br>$$ \Rightarrow \left[ {\matrix{
   {1 + 4 + 4} &amp; {2 + 2 - 4} &amp; {a + 4 + 2b}  \cr 
   {2 + 2 - 4} &amp; {4 + 1 + 4} &amp; {2a + 2 - 2b}  \cr 
   {a + 4 + 2b} &amp; {2a + 2 - 2b} &amp; {{a^2} + 4 + {b^2}}  \cr 

 } } \right]$$
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,$$ $$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, = \left[ {\matrix{
   9 &amp; 0 &amp; 0  \cr 
   0 &amp; 9 &amp; 0  \cr 
   0 &amp; 0 &amp; 9  \cr 

 } } \right]$$
<br><br>$$ \Rightarrow a + 4 + 2b = 0$$  $$ \Rightarrow a + 2b =  - 4\,\,\,\,\,\,\,\,\,\,\,\,\,\,...\left( i \right)$$
<br><br>$$2a + 2 - 2b = 0 \Rightarrow 2a - 2b =  - 2$$
<br><br>$$\,\,\,\,\,\,\,\,\,\,...

### Example 2 (Year: 2016)

**Question:**

If P = $$\left[ {\matrix{
   {{{\sqrt 3 } \over 2}} &amp; {{1 \over 2}}  \cr 
   { - {1 \over 2}} &amp; {{{\sqrt 3 } \over 2}}  \cr 

 } } \right],A = \left[ {\matrix{
   1 &amp; 1  \cr 
   0 &amp; 1  \cr 

 } } \right]\,\,\,$$ 
<br><br>Q = PAP<sup>T</sup>,  then P<sup>T</sup> Q<sup>2015</sup> P is : 

**Solution:**

P = $$\left[ {\matrix{
   {{{\sqrt 3 } \over 2}} &amp; {{1 \over 2}}  \cr 
   { - {1 \over 2}} &amp; {{{\sqrt 3 } \over 2}}  \cr 

 } } \right]$$
<br><br>$$ \therefore $$&nbsp;&nbsp;&nbsp;P<sup>T</sup> = $$\left[ {\matrix{
   {{{\sqrt 3 } \over 2}} &amp; { - {1 \over 2}}  \cr 
   {{1 \over 2}} &amp; {{{\sqrt 3 } \over 2}}  \cr 

 &nbsp;} } \right]$$
<br><br>As&nbsp;&nbsp;&nbsp; PP<sup>T</sup> = P<sup>T</sup>P = I
<br><br>given, Q = PAP<sup>T</sup>
<br><br>$$ \therefore $$&nbsp;&nbsp;&nbsp;P<sup>T</sup>Q = P<sup>T</sup>P AP<sup>T</sup>
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;&nbsp;P<sup>T</sup>Q = IAP<sup>T</sup> = AP<sup>T</sup> [ as &nbsp;&nbsp;&nbsp;P<sup>T</sup>P = I]
<br><br>Now, 
<br><br>P<sup>T</sup>&nbsp;&nbsp;Q<sup>2015</sup>&nbsp;&nbsp;P
<br><br>=&nbsp;&nbsp;P<sup>T</sup>Q &nbsp;&nbsp;. &nbsp;&nbsp;Q<sup>2014</sup>&nbsp;&nbsp;.&nbsp;&nbsp;P
<br><br>=&nbsp;&nbsp;AP<sup>T</sup>&nbsp;&nbsp;Q<sup>2014</sup>&nbsp;&nbsp;P
<br><br>=&nbsp;&nbsp;AP<sup>T</sup>&nbsp;&nbsp;.&nbsp;&nbsp;Q&nb...

### Example 3 (Year: 2017)

**Question:**

For two 3 × 3 matrices A and B, let A + B = 2B<sup>T</sup> and 3A + 2B = I<sub>3</sub>, where B<sup>T</sup> is
the transpose of B and I<sub>3</sub>  is 3 × 3 identity matrix. Then :

**Solution:**

Given, A + B = 2B<sup>T</sup> .......(1)
<br><br>$$ \Rightarrow $$ (A + B)<sup>T</sup> = (2B<sup>T</sup>)<sup>T</sup>
<br><br>$$ \Rightarrow $$ A<sup>T</sup> + B<sup>T</sup> = 2B
<br><br>$$ \Rightarrow $$ B = $${{{A^T} + {B^T}} \over 2}$$
<br><br>Now put this in equation (1)
<br><br>So, A + $${{{A^T} + {B^T}} \over 2}$$ = 2B<sup>T</sup>
<br><br>$$ \Rightarrow $$2A + A<sup>T</sup> = 3B<sup>T</sup>
<br><br>$$ \Rightarrow $$ A = $${{3{B^T} - {A^T}} \over 2}$$
<br><br>Also, 3A + 2B = I<sub>3</sub> .......(2)
<br><br>$$ \Rightarrow $$ $$3\left( {{{3{B^T} - {A^T}} \over 2}} \right) + 2\left( {{{{A^T} + {B^T}} \over 2}} \right)$$ = I<sub>3</sub>
<br><br>$$ \Rightarrow $$ 11B<sup>T</sup> - A<sup>T</sup> = 2I<sub>3</sub>
<br><br>$$ \Rightarrow $$ (11B<sup>T</sup> - A<sup>T</sup>)<sup>T</sup> = (2I<sub>3</sub>)<sup>T</sup>
<br><br>$$ \Rightarrow $$ 11B - A = 2I<sub>3</sub> ........(3)
<br><br>Multiply (3) by 3 and then adding  (2) and (3) we get,
<br><br>35B = 7I<sub>3</sub>
<br><br>$$ \Rightarr...

### Example 4 (Year: 2019)

**Question:**

The total number of matrices<br>
$$A = \left( {\matrix{
   0 &amp; {2y} &amp; 1  \cr 
   {2x} &amp; y &amp; { - 1}  \cr 
   {2x} &amp; { - y} &amp; 1  \cr 

 } } \right)$$<br>
(x, y $$ \in $$ R,x $$ \ne $$ y) for which A<sup>T</sup>A = 3I<sub>3</sub> is :-

**Solution:**

Given A<sup>T</sup>A = 3I<sub>3</sub>
<br><br>$$ \Rightarrow $$ $$\left[ {\matrix{
   0 &amp; {2x} &amp; {2x}  \cr 
   {2y} &amp; y &amp; { - y}  \cr 
   1 &amp; { - 1} &amp; 1  \cr 

 } } \right]\left[ {\matrix{
   0 &amp; {2y} &amp; 1  \cr 
   {2x} &amp; y &amp; { - 1}  \cr 
   {2x} &amp; { - y} &amp; 1  \cr 

 } } \right]$$
<br><br> = $$3\left[ {\matrix{
   1 &amp; 0 &amp; 0  \cr 
   0 &amp; 1 &amp; 0  \cr 
   0 &amp; 0 &amp; 1  \cr 

 } } \right]$$
<br><br>$$ \Rightarrow $$ $$\left[ {\matrix{
   {8{x^2}} &amp; 0 &amp; 0  \cr 
   0 &amp; {6{y^2}} &amp; 0  \cr 
   0 &amp; 0 &amp; 3  \cr 

 } } \right]$$ = $$\left[ {\matrix{
   3 &amp; 0 &amp; 0  \cr 
   0 &amp; 3 &amp; 0  \cr 
   0 &amp; 0 &amp; 3  \cr 

 } } \right]$$
<br><br>$$ \therefore $$ 8x<sup>2</sup> = 3, 6y<sup>2</sup> = 3
<br><br>$$ \Rightarrow $$ x = $$ \pm \sqrt {{3 \over 8}} $$, y = $$ \pm \sqrt {{1 \over 2}} $$
<br><br>Total possible combination of x and y = 2 $$ \times $$ 2 = 4

### Example 5 (Year: 2019)

**Question:**

Let A = $$\left( {\matrix{
   0 &amp; {2q} &amp; r  \cr 
   p &amp; q &amp; { - r}  \cr 
   p &amp; { - q} &amp; r  \cr 

 } } \right).$$ &nbsp;&nbsp;If&nbsp;&nbsp;AA<sup>T</sup> = I<sub>3</sub>, &nbsp;&nbsp;then &nbsp;&nbsp;$$\left| p \right|$$ is : 

**Solution:**

A is orthogonal matrix
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;0<sup>2</sup> + p<sup>2</sup> + p<sup>2</sup> = 1 
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;$$\left| p \right| = {1 \over {\sqrt 2 }}$$
