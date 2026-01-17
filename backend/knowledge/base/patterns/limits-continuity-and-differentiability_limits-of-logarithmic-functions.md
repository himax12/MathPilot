---
chapter: limits-continuity-and-differentiability
topic: limits-of-logarithmic-functions
jee_frequency: 3
years_appeared: [2002, 2003, 2022]
question_count: 3
difficulty: medium
question_types: ['mcq']
exams: ['mains']
---

# Limits Continuity And Differentiability: Limits Of Logarithmic Functions

**JEE Frequency**: Appeared in **3 years** (2002 - 2022)

**Question Count**: 3 questions

## Question Types

- **MCQ**: 3 questions

## Difficulty Distribution

- **Medium**: 2 questions
- **Easy**: 1 questions

## Worked Examples

### Example 1 (Year: 2002)

**Question:**

$$\mathop {\lim }\limits_{x \to 0} {{\log {x^n} - \left[ x \right]} \over {\left[ x \right]}}$$, $$n \in N$$, ( [x] denotes the greatest integer less than or equal to x )

**Solution:**

Since $$\mathop {\lim }\limits_{x \to 0} \left[ x \right]$$ does not exist, hence the required limit does not exist. 

### Example 2 (Year: 2003)

**Question:**

If $$\mathop {\lim }\limits_{x \to 0} {{\log \left( {3 + x} \right) - \log \left( {3 - x} \right)} \over x}$$ = k, the value of k is

**Solution:**

$$\mathop {\lim }\limits_{x \to 0} {{\log \left( {3 + x} \right) - \log \left( {3 - x} \right)} \over x} = K$$ 
<br><br>(by $$L'$$  Hospital rule)
<br><br>$$\mathop {\lim }\limits_{x \to 0} {{{1 \over {3 + x}} - {{ - 1} \over {3 - x}}} \over 1} = K$$
<br><br>$$\therefore$$ $${2 \over 3} = K$$

### Example 3 (Year: 2022)

**Question:**

<p>If the function $$f(x) = \left\{ {\matrix{
   {{{{{\log }_e}(1 - x + {x^2}) + {{\log }_e}(1 + x + {x^2})} \over {\sec x - \cos x}}} & , & {x \in \left( {{{ - \pi } \over 2},{\pi  \over 2}} \right) - \{ 0\} }  \cr 
   k & , & {x = 0}  \cr 

 } } \right.$$ is continuous at x = 0, then k is equal to:</p>

**Solution:**

<p>$$f(x) = \left\{ {\matrix{
   {{{{{\log }_e}(1 - x + {x^2}) + {{\log }_e}(1 + x + {x^2})} \over {\sec x - \cos x}}} & , & {x \in \left( {{{ - \pi } \over 2},{\pi  \over 2}} \right) - \{ 0\} }  \cr 
   k & , & {x = 0}  \cr 

 } } \right.$$</p>
<p>for continuity at $$x = 0$$</p>
<p>$$\mathop {\lim }\limits_{x \to 0} f(x) = k$$</p>
<p>$$\therefore$$ $$k = \mathop {\lim }\limits_{x \to 0} {{{{\log }_e}({x^4} + {x^2} + 1)} \over {\sec x - \cos x}}\left( {{0 \over 0}\,\mathrm{form}} \right)$$</p>
<p>$$ = \mathop {\lim }\limits_{x \to 0} {{\cos x{{\log }_e}({x^4} + {x^2} + 1)} \over {{{\sin }^2}x}}$$</p>
<p>$$ = \mathop {\lim }\limits_{x \to 0} {{{{\log }_e}({x^4} + {x^2} + 1)} \over {{x^2}}}$$</p>
<p>$$ = \mathop {\lim }\limits_{x \to 0} {{\ln (1 + {x^2} + {x^4})} \over {{x^2} + {x^4}}}\,.\,{{{x^2} + {x^4}} \over {{x^2}}}$$</p>
<p>$$ = 1$$</p>
