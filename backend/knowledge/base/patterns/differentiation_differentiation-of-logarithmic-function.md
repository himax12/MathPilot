---
chapter: differentiation
topic: differentiation-of-logarithmic-function
jee_frequency: 7
years_appeared: [2004, 2006, 2019, 2021, 2022, 2023, 2024]
question_count: 11
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Differentiation: Differentiation Of Logarithmic Function

**JEE Frequency**: Appeared in **7 years** (2004 - 2024)

**Question Count**: 11 questions

## Question Types

- **MCQ**: 9 questions
- **INTEGER**: 2 questions

## Difficulty Distribution

- **Medium**: 11 questions

## Worked Examples

### Example 1 (Year: 2004)

**Question:**

If $$x = {e^{y + {e^y} + {e^{y + .....\infty }}}}$$ , $$x &gt; 0,$$ then $${{{dy} \over {dx}}}$$ is 

**Solution:**

$$x = {e^{y + {e^{y + .....\infty }}}}\,\, \Rightarrow x = {e^{y + x}}.$$ 
<br><br>Taking log.
<br><br>$$\log \,\,x = y + x$$
<br><br>$$ \Rightarrow {1 \over x} = {{dy} \over {dx}} + 1$$
<br><br>$$ \Rightarrow {{dy} \over {dx}} = {1 \over x} - 1 = {{1 - x} \over x}$$


### Example 2 (Year: 2006)

**Question:**

If  $${x^m}.{y^n} = {\left( {x + y} \right)^{m + n}},$$ then $${{{dy} \over {dx}}}$$ is 

**Solution:**

$${x^m}.{y^n} = {\left( {x + y} \right)^{m + n}}$$
<br><br>$$ \Rightarrow m\ln x + n\ln y = \left( {m + n} \right)\ln \left( {x + y} \right)$$
<br><br>Differentiating both sides.
<br><br>$$\therefore$$ $${m \over x} + {n \over y}{{dy} \over {dx}} = {{m + n} \over {x + y}}\left( {1 + {{dy} \over {dx}}} \right)$$
<br><br>$$ \Rightarrow \left( {{m \over x} - {{m + n} \over {x + y}}} \right) = \left( {{{m + n} \over {x + y}} - {n \over y}} \right){{dy} \over {dx}}$$
<br><br>$$ \Rightarrow {{my - nx} \over {x\left( {x + y} \right)}} = \left( {{{my - nx} \over {y\left( {x + y} \right)}}} \right){{dy} \over {dx}}$$
<br><br>$$ \Rightarrow {{dy} \over {dx}} = {y \over x}$$ 

### Example 3 (Year: 2019)

**Question:**

If &nbsp;xlog<sub>e</sub>(log<sub>e</sub>x) $$-$$ x<sup>2</sup> + y<sup>2</sup> = 4(y &gt; 0),  then $${{dy} \over {dx}}$$ at x = e is equal to : 

**Solution:**

Differentiating with respect to x,
<br><br>$$x.{1 \over {\ell nx}}.{1 \over x} + \ell n(\ell nx) - 2x + 2y.{{dy} \over {dx}} = 0$$
<br><br>at&nbsp;&nbsp;&nbsp;$$x = e$$&nbsp;&nbsp;we get
<br><br>$$1 - 2e + 2y{{dy} \over {dx}} = 0 \Rightarrow {{dy} \over {dx}} = {{2e - 1} \over {2y}}$$
<br><br>$$ \Rightarrow {{dy} \over {dx}} = {{2e - 1} \over {2\sqrt {4 + {e^2}} }}\,\,$$
<br><br>as&nbsp;&nbsp;&nbsp;$$y(e) = \sqrt {4 + {e^2}} $$

### Example 4 (Year: 2019)

**Question:**

For x &gt; 1,  if  (2x)<sup>2y</sup> = 4e<sup>2x$$-$$2y</sup>,  
<br><br>then  (1 + log<sub>e</sub> 2x)<sup>2</sup> $${{dy} \over {dx}}$$ is equal to : 

**Solution:**

(2x)<sup>2y</sup> = 4e<sup>2x-2y</sup>
<br><br>2y$$\ell $$n2x = $$\ell $$n4 + 2x $$-$$ 2y
<br><br>y = $${{x + \ell n2} \over {1 + \ell n2x}}$$
<br><br>y ' = $${{\left( {1 + \ell n2x} \right) - \left( {x + \ell n2} \right){1 \over x}} \over {{{\left( {1 + \ell n2x} \right)}^2}}}$$
<br><br>y '$${\left( {1 + \ell n2x} \right)^2} = \left[ {{{x\ell n2x - \ell n2} \over x}} \right]$$

### Example 5 (Year: 2021)

**Question:**

If y = y(x) is an implicit function of x such that log<sub>e</sub>(x + y) = 4xy, then $${{{d^2}y} \over {d{x^2}}}$$ at x = 0 is equal to ___________.

**Solution:**

ln(x + y) = 4xy (At x = 0, y = 1)<br><br>x + y = e<sup>4xy</sup><br><br>$$ \Rightarrow 1 + {{dy} \over {dx}} = {e^{4xy}}\left( {4x{{dy} \over {dx}} + 4y} \right)$$<br><br>At x = 0 <br><br>$${{dy} \over {dx}} = 3$$<br><br>$${{{d^2}y} \over {d{x^2}}} = {e^{4xy}}{\left( {4x{{dy} \over {dx}} + 4y} \right)^2} + {e^{4xy}}\left( {4x{{{d^2}y} \over {d{x^2}}} + 4y} \right)$$<br><br>At x = 0, $${{{d^2}y} \over {d{x^2}}} = {e^0}{(4)^2} + {e^0}(24)$$<br><br>$$ \Rightarrow {{{d^2}y} \over {d{x^2}}} = 40$$
