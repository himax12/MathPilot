---
chapter: matrices-and-determinants
topic: trace-of-a-matrix
jee_frequency: 7
years_appeared: [2008, 2010, 2020, 2021, 2023, 2024, 2025]
question_count: 12
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Matrices And Determinants: Trace Of A Matrix

**JEE Frequency**: Appeared in **7 years** (2008 - 2025)

**Question Count**: 12 questions

## Question Types

- **MCQ**: 7 questions
- **INTEGER**: 5 questions

## Difficulty Distribution

- **Medium**: 9 questions
- **Hard**: 3 questions

## Worked Examples

### Example 1 (Year: 2008)

**Question:**

Let $$A$$ be $$a\,2 \times 2$$ matrix with real entries. Let $$I$$ be the $$2 \times 2$$ identity matrix. Denote by tr$$(A)$$, the sum of diagonal entries of $$a$$. Assume that $${a^2} = I.$$ 
<br><b>Statement-1 :</b> If $$A \ne I$$ and $$A \ne  - I$$, then det$$(A)=-1$$
<br><b>Statement- 2 :</b> If $$A \ne I$$ and $$A \ne  - I$$, then tr $$(A)$$ $$ \ne 0$$.

**Solution:**

Let $$A = \left[ {\matrix{
   a &amp; b  \cr 
   c &amp; d  \cr 

 } } \right]$$ $$\,\,\,$$ then $${A^2} = 1$$
<br><br>$$ \Rightarrow {a^2} + bc = 1\,\,\,\,ab + bd = 0$$
<br><br>$$ac + cd = 0\,\,\,\,bc + {d^2} = 1$$
<br><br>From these four relations, 
<br><br>$${a^2} + bc = bc + {d^2} \Rightarrow {a^2} = {d^2}$$
<br><br>and $$\,\,b\left( {a + d} \right) = 0 = c\left( {a + d} \right)$$
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\, \Rightarrow a =  - d$$
<br><br>We can take $$a = 1,b = 0,c = 0,d =  - 1$$ 
<br><br>as one possible set of values, then 
<br><br>$$A = \left[ {\matrix{
   1 &amp; 0  \cr 
   0 &amp; { - 1}  \cr 

 } } \right]$$ 
<br><br>Clearly $$A \ne I\,\,\,$$ and $$\,\,\,\,A \ne  - I\,\,$$ and $$\,\,\,A =  - 1$$
<br><br>$$\therefore$$ $$\,\,\,\,\,$$ Statement $$1$$ is true. 
<br><br>Also if $$A \ne I\,\,\,\,\,tr\left( A \right) = 0$$ 
<br><br>$$\therefore$$ $$\,\,\,\,\,$$ Statement $$2$$ is false.

### Example 2 (Year: 2010)

**Question:**

Let $$A$$ be a $$\,2 \times 2$$ matrix with non-zero entries and let $${A^2} = I,$$ 
<br>where $$I$$ is $$2 \times 2$$ identity matrix. Define 
<br>$$Tr$$$$(A)=$$ sum of diagonal elements of $$A$$ and $$\left| A \right| = $$ determinant of matrix $$A$$.
<br><b>Statement- 1:</b> $$Tr$$$$(A)=0$$.
<br><b>Statement- 2:</b> $$\left| A \right| = 1$$ .

**Solution:**

Let $$A = \left( {\matrix{
   a &amp; b  \cr 
   c &amp; d  \cr 

 } } \right)$$ where $$a,b,c,d$$ $$ \ne 0$$ 
<br><br>$${A^2} = \left( {\matrix{
   a &amp; b  \cr 
   c &amp; d  \cr 

 } } \right)\left( {\matrix{
   a &amp; b  \cr 
   c &amp; d  \cr 

 } } \right)$$
<br><br>$$ \Rightarrow {A^2} = \left( {\matrix{
   {{a^2} + bc} &amp; {ab + bd}  \cr 
   {ac + cd} &amp; {bc + {d^2}}  \cr 

 } } \right)$$
<br><br>$$ \Rightarrow {a^2} + bc = 1,\,bc + {d^2} = 1$$
<br><br>$$ab + bd = ac + cd = 0$$
<br><br>$$c \ne 0\,\,\,\,\,b \ne 0$$
<br><br>$$ \Rightarrow a + d = 0 \Rightarrow Tr\left( A \right) = 0$$
<br><br>$$\left| A \right| = ad - bc =  - {a^2} - bc =  - 1$$ 

### Example 3 (Year: 2020)

**Question:**

The number of all 3 × 3 matrices A, with
enteries from the set {–1, 0, 1} such that the sum
of the diagonal elements of AA<sup>T</sup> is 3, is

**Solution:**

Let A = $$\left[ {\matrix{
   {{a_{11}}} &amp; {{a_{12}}} &amp; {{a_{13}}}  \cr 
   {{a_{21}}} &amp; {{a_{22}}} &amp; {{a_{23}}}  \cr 
   {{a_{31}}} &amp; {{a_{32}}} &amp; {{a_{33}}}  \cr 

 } } \right]$$
<br><br>$$ \therefore $$ A<sup>T</sup> = $$\left[ {\matrix{
   {{a_{11}}} &amp; {{a_{21}}} &amp; {{a_{31}}}  \cr 
   {{a_{12}}} &amp; {{a_{22}}} &amp; {{a_{32}}}  \cr 
   {{a_{13}}} &amp; {{a_{23}}} &amp; {{a_{33}}}  \cr 

 } } \right]$$
<br><br>diagonal elements of AA<sup>T</sup>
 are $$a_{11}^2 + a_{12}^2 + a_{13}^2$$
, <br>$$a_{21}^2 + a_{22}^2 + a_{23}^2$$
, $$a_{31}^2 + a_{32}^2 + a_{33}^2$$
<br><br>Given Sum = ($$a_{11}^2 + a_{12}^2 + a_{13}^2$$) + <br>($$a_{21}^2 + a_{22}^2 + a_{23}^2$$) + ($$a_{31}^2 + a_{32}^2 + a_{33}^2$$) = 3
<br><br>This is only possible when  three enteries must be either 1 or – 1 and all other six enteries are 0.
<br><br>$$ \therefore $$ Number of matrices = <sup>9</sup>C<sub>3</sub> $$ \times $$ 2 $$ \times $$ 2 $$ \times $$ 2
<br><br>= 672

### Example 4 (Year: 2020)

**Question:**

Let A be a 2 $$ \times $$ 2 real matrix with entries from
{0, 1} and |A|
$$ \ne $$ 0. Consider the following two
statements :
<br><br>(P) If A $$ \ne $$ I<sub>2</sub>
, then |A| = –1
<br>(Q) If |A| = 1, then tr(A) = 2,
<br><br>where I<sub>2</sub>
 denotes 2 $$ \times $$ 2 identity matrix and tr(A)
denotes the sum of the diagonal entries of A. Then :


**Solution:**

Let A = $$\left[ {\matrix{
   a &amp; b  \cr 
   c &amp; d  \cr 

 } } \right]$$, where a, b, c, d $$ \in $$ {0, 1}
<br><br>$$ \Rightarrow $$ |A| =  ad – bc
<br><br>$$ \therefore $$ ad = 0 or 1 and bc = 0 or 1
<br><br>So possible values of |A| are 1, 0 or –1
<br><br>(P) If A $$ \ne $$ I<sub>2</sub>
 then |A| is either 0 or –1
<br><br>(Q) If |A| = 1 then ad = 1 and bc = 0
<br><br>$$ \Rightarrow $$ a = d = 1 $$ \Rightarrow $$ Tr(A) = 2

### Example 5 (Year: 2021)

**Question:**

The total number of 3 $$\times$$ 3 matrices A having entries from the set {0, 1, 2, 3} such that the sum of all the diagonal entries of AA<sup>T</sup> is 9, is equal to _____________.

**Solution:**

$$A{A^T} = \left[ {\matrix{
   x &amp; y &amp; z  \cr 
   a &amp; b &amp; c  \cr 
   d &amp; e &amp; f  \cr 

 } } \right]\left[ {\matrix{
   x &amp; a &amp; d  \cr 
   y &amp; b &amp; e  \cr 
   z &amp; c &amp; f  \cr 

 } } \right]$$<br><br>$$ = \left[ {\matrix{
   {{x^2} + {y^2} + {z^2}} &amp; {ax + by + cz} &amp; {dx + ey + fz}  \cr 
   {ax + by + cz} &amp; {{a^2} + {b^2} + {c^2}} &amp; {ad + be + cf}  \cr 
   {dx + ey + fz} &amp; {ad + be + cf} &amp; {{d^2} + {e^2} + {f^2}}  \cr 

 } } \right]$$<br><br>$$Tr(A{A^T}) = {x^2} + {y^2} + {z^2} + {a^2} + {b^2} + {c^2} + {d^2} + {e^2} + {f^2} = 9$$<br><br>Case-I : Nine ones = 1 case<br><br>Case-II : 8 zeroes and one entry is 3 =  $${{{9!} \over {8!}} = 9}$$ cases<br><br>Case-III : Two 2’s, one 1’s and 6 zeroes = $${{9!} \over {2!6!}} = 63 \times 4 = 252$$<br><br>Case IV : one 2, five 1, rest 0 $${{9!} \over {5!3!}} = 63 \times 8 = 504$$<br><br>$$ \therefore $$ Total cases = 9 + 252 + 504 + 1 = 766
