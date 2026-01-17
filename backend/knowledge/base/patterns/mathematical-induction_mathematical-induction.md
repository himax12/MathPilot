---
chapter: mathematical-induction
topic: mathematical-induction
jee_frequency: 3
years_appeared: [2002, 2004, 2005]
question_count: 3
difficulty: medium
question_types: ['mcq']
exams: ['mains']
---

# Mathematical Induction: Mathematical Induction

**JEE Frequency**: Appeared in **3 years** (2002 - 2005)

**Question Count**: 3 questions

## Question Types

- **MCQ**: 3 questions

## Difficulty Distribution

- **Medium**: 2 questions
- **Easy**: 1 questions

## Worked Examples

### Example 1 (Year: 2002)

**Question:**

If $${a_n} = \sqrt {7 + \sqrt {7 + \sqrt {7 + .......} } } $$  having $$n$$ radical signs then by methods of mathematical induction which is true 

**Solution:**

Given $${a_n} = \sqrt {7 + \sqrt {7 + \sqrt {7 + .......} } } $$
<br><br>$$\therefore$$ $${a_n} = \sqrt {7 + {a_n}} $$
<br><br>$$ \Rightarrow $$ $$a_n^2 = 7 + {a_n}$$
<br><br>$$ \Rightarrow $$ $$a_n^2 - {a_n} - 7 = 0$$
<br><br>$$ \Rightarrow {a_n} = {{1 \pm \sqrt {1 - 4 \times 1 \times  - 7} } \over 2}$$
<br><br>$$ \Rightarrow {a_n} = {{1 \pm \sqrt {29} } \over 2}$$
<br><br>As $${a_n}$$ &gt; 0, 
<br><br>$$\therefore$$ $${a_n} = {{1 + \sqrt {29} } \over 2}$$ = 3.19
<br><br>So $${a_n} &gt; 3\,\,\forall \,\,n \ge 1$$ 

### Example 2 (Year: 2004)

**Question:**

Let $$S(K)$$ $$ = 1 + 3 + 5... + \left( {2K - 1} \right) = 3 + {K^2}.$$  Then which of the following is true 

**Solution:**

Given $$S(K)$$ $$ = 1 + 3 + 5... + \left( {2K - 1} \right) = 3 + {K^2}$$
<br><br>When k = 1, S(1): 1 = 3 + 1, 
<br><br>L.H.S of S(k) $$ \ne $$ R.H.S of S(k)
<br><br>So S(1) is not true.
<br><br>As S(1) is not true so principle of mathematical induction can not be used.
<br><br>S(K+1) = 1 + 3 + 5... + (2K - 1) + (2K + 1) = 3 + (k + 1)<sup>2</sup>
<br><br>Now let S(k) is true
<br><br>$$\therefore$$ 1 + 3 + 5 +........(2k - 1) = 3 + k<sup>2</sup>
<br><br>$$ \Rightarrow $$ 1 + 3 + 5 +........(2k - 1) + (2k + 1) = 3 + k<sup>2</sup> + 2k +1
<br><br>= 3 + (k + 1)<sup>2</sup>
<br><br>$$ \Rightarrow $$ S(k + 1) is true.
<br><br>$$\therefore$$ S(k) $$ \Rightarrow $$ S(k + 1)

### Example 3 (Year: 2005)

**Question:**

If $$A = \left[ {\matrix{
   1 &amp; 0  \cr 
   1 &amp; 1  \cr 

 } } \right]$$ and $$I = \left[ {\matrix{
   1 &amp; 0  \cr 
   0 &amp; 1  \cr 

 } } \right],$$ then which one of the following holds for all $$n \ge 1,$$ by the principle of mathematical induction? 

**Solution:**

Given $$A = \left[ {\matrix{
   1 &amp; 0  \cr 
   1 &amp; 1  \cr 

 } } \right]$$
<br><br>$$\therefore$$ $$A \times A$$ = $${A^2}$$ = $$\left[ {\matrix{
   1 &amp; 0  \cr 
   2 &amp; 1  \cr 

 } } \right]$$
<br><br>and $${A^3}$$ = $${A^2} \times A$$ = $$\left[ {\matrix{
   1 &amp; 0  \cr 
   3 &amp; 1  \cr 

 } } \right]$$
<br><br>So we can say $${A^n}$$ = $$\left[ {\matrix{
   1 &amp; 0  \cr 
   n &amp; 1  \cr 

 } } \right]$$
<br><br>Now $$nA - \left( {n - 1} \right){\rm I}$$
<br><br>= $$\left[ {\matrix{
   n &amp; 0  \cr 
   n &amp; n  \cr 

 } } \right]$$ - $$\left[ {\matrix{
   {n - 1} &amp; 0  \cr 
   0 &amp; {n - 1}  \cr 

 } } \right]$$
<br><br>= $$\left[ {\matrix{
   1 &amp; 0  \cr 
   n &amp; 1  \cr 

 } } \right]$$ = $${A^n}$$
<br><br>$$\therefore$$ $${A^n} = nA - \left( {n - 1} \right){\rm I}$$ 
