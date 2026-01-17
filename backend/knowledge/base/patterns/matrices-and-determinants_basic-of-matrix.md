---
chapter: matrices-and-determinants
topic: basic-of-matrix
jee_frequency: 2
years_appeared: [2010, 2022]
question_count: 2
difficulty: hard
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Matrices And Determinants: Basic Of Matrix

**JEE Frequency**: Appeared in **2 years** (2010 - 2022)

**Question Count**: 2 questions

## Question Types

- **MCQ**: 1 questions
- **INTEGER**: 1 questions

## Difficulty Distribution

- **Hard**: 1 questions
- **Medium**: 1 questions

## Worked Examples

### Example 1 (Year: 2010)

**Question:**

The number of $$3 \times 3$$ non-singular matrices, with four entries as $$1$$ and all other entries as $$0$$, is :

**Solution:**

$$\left[ {\matrix{
   1 &amp; {...} &amp; {...}  \cr 
   {...} &amp; 1 &amp; {...}  \cr 
   {...} &amp; {...} &amp; 1  \cr 

 } } \right]\,\,$$ are $$6$$ non-singular matrices because $$6$$
<br><br>blanks will be filled by $$5$$ zeros and $$1$$ one.
<br><br>Similarly, $$\left[ {\matrix{
   {...} &amp; {...} &amp; 1  \cr 
   {...} &amp; 1 &amp; {...}  \cr 
   1 &amp; {...} &amp; {...}  \cr 

 } } \right]\,\,$$ are $$6$$ non-singular matrices.
<br><br>So, required cases are more than $$7,$$ non-singular $$3 \times 3$$ matrices.

### Example 2 (Year: 2022)

**Question:**

<p>Let $$A=\left[\begin{array}{lll}
1 & a & a \\
0 & 1 & b \\
0 & 0 & 1
\end{array}\right], a, b \in \mathbb{R}$$. If for some <br/><br/>$$n \in \mathbb{N}, A^{n}=\left[\begin{array}{ccc}
1 & 48 & 2160 \\
0 & 1 & 96 \\
0 & 0 & 1
\end{array}\right]
$$ then $$n+a+b$$ is equal to ____________.</p>

**Solution:**

<p>$$A = \left[ {\matrix{
   1 & 0 & 0  \cr 
   0 & 1 & 0  \cr 
   0 & 0 & 1  \cr 

 } } \right] + \left[ {\matrix{
   0 & a & a  \cr 
   0 & 0 & b  \cr 
   0 & 0 & 0  \cr 

 } } \right] = I + B$$</p>
<p>$${B^2} = \left[ {\matrix{
   0 & a & a  \cr 
   0 & 0 & b  \cr 
   0 & 0 & 0  \cr 

 } } \right] + \left[ {\matrix{
   0 & a & a  \cr 
   0 & 0 & b  \cr 
   0 & 0 & 0  \cr 

 } } \right] = \left[ {\matrix{
   0 & 0 & {ab}  \cr 
   0 & 0 & 0  \cr 
   0 & 0 & 0  \cr 

 } } \right]$$</p>
<p>$${B^3} = 0$$</p>
<p>$$\therefore$$ $${A^n} = {(1 + B)^n} = {}^n{C_0}I + {}^n{C_1}B + {}^n{C_2}{B^2} + {}^n{C_3}{B^3} + \,\,....$$</p>
<p>$$ = \left[ {\matrix{
   1 & 0 & 0  \cr 
   0 & 1 & 0  \cr 
   0 & 0 & 1  \cr 

 } } \right] + \left[ {\matrix{
   0 & {na} & {na}  \cr 
   0 & 0 & {nb}  \cr 
   0 & 0 & 0  \cr 

 } } \right] + \left[ {\matrix{
   0 & 0 & {{{n(n - 1)ab} \over 2}}  \cr 
   0 & 0 & 0  \cr 
   0 & 0 & 0  \cr 

 } } \right]$$</p>
<p>$$ = \left[ {\matrix{
   1 & {na} & {na + {{n(n - 1)} ...
