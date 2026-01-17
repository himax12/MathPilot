---
chapter: matrices-and-determinants
topic: symmetric-and-skew-symmetric-matrices
jee_frequency: 6
years_appeared: [2011, 2019, 2021, 2022, 2023, 2025]
question_count: 12
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Matrices And Determinants: Symmetric And Skew Symmetric Matrices

**JEE Frequency**: Appeared in **6 years** (2011 - 2025)

**Question Count**: 12 questions

## Question Types

- **MCQ**: 9 questions
- **INTEGER**: 3 questions

## Difficulty Distribution

- **Medium**: 11 questions
- **Easy**: 1 questions

## Worked Examples

### Example 1 (Year: 2011)

**Question:**

Let  $$A$$ and $$B$$ be two symmetric matrices of order $$3$$. 
<br><br/><b>Statement - 1 :</b> $$A(BA)$$ and $$(AB)$$$$A$$ are symmetric matrices. 
<br><br/><b>Statement - 2 :</b> $$AB$$ is symmetric matrix if matrix multiplication of $$A$$ with $$B$$ is commutative.

**Solution:**

$$\therefore$$ $$A' = A,B' = B$$ 
<br><br>Now $$\,\,\,\left( {A\left( {BA} \right)} \right)' = \left( {BA} \right)'A'$$ 
<br><br>$$ = \left( {A'B'} \right)A' = \left( {AB} \right)A = A\left( {BA} \right)$$ 
<br><br>Similarly $$\left( {\left( {AB} \right)A} \right)' = \left( {AB} \right)A$$
<br><br>So, $$A\left( {BA} \right)\,\,\,\,$$ and $$A\left( {BA} \right)\,\,\,\,$$ are symmetric matrices.
<br><br>Again $$\left( {AB} \right)' = B'A' = BA$$
<br><br>Now if $$BA=AB$$, then $$AB$$ is symmetric matrix.

### Example 2 (Year: 2019)

**Question:**

If A is a symmetric matrix and B is a skew-symmetric matrix such that A + B = $$\left[ {\matrix{
   2 &amp; 3  \cr 
   5 &amp; { - 1}  \cr 

 } } \right]$$, then AB is equal
to : 

**Solution:**

$$A + B = \left[ {\matrix{
   2 &amp; 3  \cr 
   5 &amp; { - 1}  \cr 

 } } \right] = P(say)$$<br><br>
Now $$A = {{P + {P^T}} \over 2}\&amp; B = {{P - {P^T}} \over 2}$$<br><br>
So $$A = {1 \over 2}\left( {\left[ {\matrix{
   2 &amp; 3  \cr 
   5 &amp; { - 1}  \cr 

 } } \right] + \left[ {\matrix{
   2 &amp; 5  \cr 
   3 &amp; { - 1}  \cr 

 } } \right]} \right) = \left[ {\matrix{
   2 &amp; 4  \cr 
   4 &amp; { - 1}  \cr 

 } } \right]$$<br><br>
$$B = {1 \over 2}\left( {\left[ {\matrix{
   2 &amp; 3  \cr 
   5 &amp; { - 1}  \cr 

 } } \right] - \left[ {\matrix{
   2 &amp; 5  \cr 
   3 &amp; { - 1}  \cr 

 } } \right]} \right) = \left[ {\matrix{
   0 &amp; { - 1}  \cr 
   1 &amp; 0  \cr 

 } } \right]$$<br><br>
So $$AB = \left( {\left[ {\matrix{
   2 &amp; 4  \cr 
   4 &amp; { - 1}  \cr 

 } } \right]\left[ {\matrix{
   0 &amp; { - 1}  \cr 
   1 &amp; 0  \cr 

 } } \right]} \right) = \left[ {\matrix{
   4 &amp; { - 2}  \cr 
   { - 1} &amp; { - 4}  \cr 

 } } \right]$$

### Example 3 (Year: 2021)

**Question:**

Let A and B be 3 $$\times$$ 3 real matrices such that A is symmetric matrix and B is skew-symmetric matrix. Then the system of linear equations (A<sup>2</sup>B<sup>2</sup> $$-$$ B<sup>2</sup>A<sup>2</sup>) X = O, where X is a 3 $$\times$$ 1 column matrix of unknown variables and O is a 3 $$\times$$ 1 null matrix, has :

**Solution:**

A<sup>T</sup> = A, B<sup>T</sup> = $$-$$B<br><br>Let A<sup>2</sup>B<sup>2</sup> $$-$$ B<sup>2</sup>A<sup>2</sup> = P<br><br>P<sup>T</sup> = (A<sup>2</sup>B<sup>2</sup> $$-$$ B<sup>2</sup>A<sup>2</sup>)<sup>T</sup> = (A<sup>2</sup>B<sup>2</sup>)<sup>T</sup> $$-$$ (B<sup>2</sup>A<sup>2</sup>)<sup>T</sup><br><br>= (B<sup>2</sup>)<sup>T</sup> (A<sup>2</sup>)<sup>T</sup> $$-$$ (A<sup>2</sup>)<sup>T</sup> (B<sup>2</sup>)<sup>T</sup><br><br>= B<sup>2</sup>A<sup>2</sup> $$-$$ A<sup>2</sup>B<sup>2</sup><br><br>$$ \Rightarrow $$ P is skew-symmetric matrix<br><br>$$\left[ {\matrix{
   0 &amp; a &amp; b  \cr 
   { - a} &amp; 0 &amp; c  \cr 
   { - b} &amp; { - c} &amp; 0  \cr 

 } } \right]\left[ {\matrix{
   x  \cr 
   y  \cr 
   z  \cr 

 } } \right] = \left[ {\matrix{
   0  \cr 
   0  \cr 
   0  \cr 

 } } \right]$$<br><br>$$ \therefore $$ ay + bz = 0 ..... (1)<br><br>$$-$$ax + cz = 0 .... (2)<br><br>$$-$$bx $$-$$cy = 0 ..... (3)<br><br>From equation 1, 2, 3<br><br>$$\Delta$$ = 0 &amp; $$\Delta...

### Example 4 (Year: 2021)

**Question:**

Let A be a symmetric matrix of order 2 with integer entries. If the sum of the diagonal elements of A<sup>2</sup> is 1, then the possible number of such matrices is :

**Solution:**

Let $$A = \left[ {\matrix{
   a &amp; b  \cr 
   b &amp; c  \cr 

 } } \right]$$<br><br>$${A^2} = \left[ {\matrix{
   a &amp; b  \cr 
   b &amp; c  \cr 

 } } \right]\left[ {\matrix{
   a &amp; b  \cr 
   b &amp; c  \cr 

 } } \right] = \left[ {\matrix{
   {{a^2} + {b^2}} &amp; {ab + bc}  \cr 
   {ab + bc} &amp; {{c^2} + {b^2}}  \cr 

 } } \right]$$<br><br>$$ = {a^2} + 2{b^2} + {c^2} = 1$$<br><br>$$a = 1,b = 0,c = 0$$<br><br>$$a = 0,b = 0,c = 1$$<br><br>$$a =  - 1,b = 0,c = 0$$<br><br>$$c =  - 1,b = 0,a = 0$$

### Example 5 (Year: 2021)

**Question:**

Let $$A = \left[ {\matrix{
   2 &amp; 3  \cr 
   a &amp; 0  \cr 

 } } \right]$$, a$$\in$$R be written as P + Q where P is a symmetric matrix and Q is skew symmetric matrix. If det(Q) = 9, then the modulus of the sum of all possible values of determinant of P is equal to :

**Solution:**

$$A = \left[ {\matrix{
   2 & 3  \cr 
   a & 0  \cr 

 } } \right]$$, $${A^T} = \left[ {\matrix{
   2 & a  \cr 
   3 & 0  \cr 

 } } \right]$$<br/><br/>$$A = {{A + {A^T}} \over 2} + {{A - {A^T}} \over 2}$$<br/><br/>Let $$P = {{A + {A^T}} \over 2}$$ and $$Q = {{A - {A^T}} \over 2}$$<br/><br/>$$Q = \left( {\matrix{
   0 & {{{3 - a} \over 2}}  \cr 
   {{{a - 3} \over 2}} & 0  \cr 

 } } \right)$$<br/><br/>Det (Q) = 9<br/><br/>$$0 - \left( {{{3 - a} \over 2}} \right)\left( {{{a - 3} \over 2}} \right) = 9$$<br/><br/>$$ \Rightarrow {\left( {{{a - 3} \over 2}} \right)^2} = 9 \Rightarrow {(a - 3)^2} = 36$$<br/><br/>$$a - 3 =  \pm \,6 \Rightarrow a = 9, - 3$$<br/><br/>$$P = \left[ {\matrix{
   2 & {{{a + 3} \over 2}}  \cr 
   {{{a + 3} \over 2}} & 0  \cr 

 } } \right]$$<br/><br/>$$P = \left[ {\matrix{
   2 & 6  \cr 
   6 & 0  \cr 

 } } \right]$$ or $$\left[ {\matrix{
   2 & 0  \cr 
   0 & 0  \cr 

 } } \right]$$
<br/><br/> | P | = - 36 or 0
<br/><br/>$$\therefore$$ | $$-$$36 + 0 | = 36
