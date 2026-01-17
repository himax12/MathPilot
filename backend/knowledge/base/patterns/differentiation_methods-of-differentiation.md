---
chapter: differentiation
topic: methods-of-differentiation
jee_frequency: 6
years_appeared: [2011, 2020, 2022, 2023, 2024, 2025]
question_count: 11
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Differentiation: Methods Of Differentiation

**JEE Frequency**: Appeared in **6 years** (2011 - 2025)

**Question Count**: 11 questions

## Question Types

- **MCQ**: 8 questions
- **INTEGER**: 3 questions

## Difficulty Distribution

- **Medium**: 10 questions
- **Easy**: 1 questions

## Worked Examples

### Example 1 (Year: 2011)

**Question:**

$${{{d^2}x} \over {d{y^2}}}$$ equals:

**Solution:**

$${{{d^2}x} \over {d{y^2}}} = {d \over {dy}}\left( {{{dx} \over {dy}}} \right)$$
<br><br>$$ = {d \over {dx}}\left( {{{dx} \over {dy}}} \right){{dx} \over {dy}}$$
<br><br>$$ = {d \over {dx}}\left( {{1 \over {dy/dx}}} \right){{dx} \over {dy}}$$
<br><br>$$ =  - {1 \over {{{\left( {{{dy} \over {dx}}} \right)}^2}}}.{{{d^2}y} \over {d{x^2}}}.{1 \over {{{dy} \over {dx}}}}$$
<br><br>$$ =  - {1 \over {{{\left( {{{dy} \over {dx}}} \right)}^3}}}{{{d^2}y} \over {d{x^2}}}$$

### Example 2 (Year: 2020)

**Question:**

Let ƒ and g be differentiable functions on R
such that fog is the identity function. If for some
a, b $$ \in $$ R, g'(a) = 5 and g(a) = b, then ƒ'(b) is
equal to :

**Solution:**

Given the function composition f(g(x)) is the identity function, it means f(g(x)) = x for all x.

<br><br>$$ \Rightarrow $$ ƒ'(g(x)) g'(x) = 1
<br><br>put x = a
<br><br>$$ \Rightarrow $$ ƒ'(b) g'(a) = 1
<br><br>$$ \Rightarrow $$ ƒ'(b) = $${1 \over 5}$$

### Example 3 (Year: 2022)

**Question:**

<p>Let f and g be twice differentiable even functions on ($$-$$2, 2) such that $$f\left( {{1 \over 4}} \right) = 0$$, $$f\left( {{1 \over 2}} \right) = 0$$, $$f(1) = 1$$ and $$g\left( {{3 \over 4}} \right) = 0$$, $$g(1) = 2$$. Then, the minimum number of solutions of $$f(x)g''(x) + f'(x)g'(x) = 0$$ in $$( - 2,2)$$ is equal to ________.</p>

**Solution:**

Let $h(x)=f(x) \cdot g^{\prime}(x)$
<br/><br/>
As $f(x)$ is even $f\left(\frac{1}{2}\right)=\left(\frac{1}{4}\right)=0$
<br/><br/>
$\Rightarrow f\left(-\frac{1}{2}\right)=f\left(-\frac{1}{4}\right)=0$
<br/><br/>
and $g(x)$ is even $\Rightarrow g^{\prime}(x)$ is odd <br/><br/>
and $g(1)=2$ ensures one root of $g^{\prime}(x)$ is 0 .
<br/><br/>
So, $h(x)=f(x) \cdot g^{\prime}(x)$ has minimum five zeroes
<br/><br/>
$\therefore h^{\prime}(x)=f^{\prime}(x) \cdot g^{\prime}(x)+f(x) \cdot g^{\prime \prime}(x)=0$,
<br/><br/>
has minimum 4 zeroes


### Example 4 (Year: 2023)

**Question:**

<p>Let $$f:\mathbb{R}\to\mathbb{R}$$ be a differentiable function that satisfies the relation $$f(x+y)=f(x)+f(y)-1,\forall x,y\in\mathbb{R}$$. If $$f'(0)=2$$, then $$|f(-2)|$$ is equal to ___________.</p>

**Solution:**

$f(x+y)=f(x)+f(y)-1$
<br/><br/>
$$
\begin{aligned}
& f^{\prime}(x)=\lim _{h \rightarrow 0} \frac{f(x+h)-f(x)}{h} \\\\
& f^{\prime}(x)=\lim _{h \rightarrow 0} \frac{f(h)-f(0)}{h}=f^{\prime}(0)=2 \\\\
& f^{\prime}(x)=2 \Rightarrow d y=2 d x \\\\
& y=2 x+C \\\\
& \mathrm{x}=0, \mathrm{y}=1, \mathrm{c}=1 \\\\
& \mathrm{y}=2 \mathrm{x}+1 \\\\
& |f(-2)|=|-4+1|=|-3|=3
\end{aligned}
$$

### Example 5 (Year: 2023)

**Question:**

<p>For the differentiable function $$f: \mathbb{R}-\{0\} \rightarrow \mathbb{R}$$, let $$3 f(x)+2 f\left(\frac{1}{x}\right)=\frac{1}{x}-10$$, then $$\left|f(3)+f^{\prime}\left(\frac{1}{4}\right)\right|$$ is equal to</p>

**Solution:**

<ol>
<li><p>Given the equation: $$3f(x) + 2f\left(\frac{1}{x}\right) = \frac{1}{x} - 10$$</p>
</li>
<li><p>Replace $$x$$ with $$\frac{1}{x}$$ in the original equation: 
<br/>$$3f\left(\frac{1}{x}\right) + 2f(x) = x - 10$$</p>
</li>
<li><p>Now, we have two equations:</p>
</li>
</ol>
<p>$$3f(x) + 2f\left(\frac{1}{x}\right) = \frac{1}{x} - 10$$
<br/><br/>$$3f\left(\frac{1}{x}\right) + 2f(x) = x - 10$$</p>
<ol>
<li>By adding the two equations, we can find $$f(x)$$:</li>
</ol>
<p>$$5f(x) = \frac{3}{x} - 2x - 10$$</p>
<ol>
<li>Now, let&#39;s differentiate both sides with respect to $$x$$:</li>
</ol>
<p>$$5f&#39;(x) = -\frac{3}{x^2} - 2$$</p>
<ol>
<li>Now, we can find the values for $$f(3)$$ and $$f&#39;\left(\frac{1}{4}\right)$$:</li>
</ol>
<p>$$f(3) = \frac{1}{5}(1 - 6 - 10) = -3$$
<br/><br/>$$f&#39;\left(\frac{1}{4}\right) = \frac{1}{5}(-48 - 2) = -10$$</p>
<ol>
<li>Finally, calculate the expression we are interested in :</li>
</ol>
<p>$$\left|f(3) + f&#39;\left(\frac{1}{4}\right)\right| =...
