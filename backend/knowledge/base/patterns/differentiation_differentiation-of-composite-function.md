---
chapter: differentiation
topic: differentiation-of-composite-function
jee_frequency: 6
years_appeared: [2010, 2014, 2019, 2022, 2023, 2024]
question_count: 8
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Differentiation: Differentiation Of Composite Function

**JEE Frequency**: Appeared in **6 years** (2010 - 2024)

**Question Count**: 8 questions

## Question Types

- **MCQ**: 7 questions
- **INTEGER**: 1 questions

## Difficulty Distribution

- **Medium**: 4 questions
- **Easy**: 3 questions
- **Hard**: 1 questions

## Worked Examples

### Example 1 (Year: 2010)

**Question:**

Let  $$f:\left( { - 1,1} \right) \to R$$ be a differentiable function with $$f\left( 0 \right) =  - 1$$ and $$f'\left( 0 \right) = 1$$. Let $$g\left( x \right) = {\left[ {f\left( {2f\left( x \right) + 2} \right)} \right]^2}$$. Then $$g'\left( 0 \right) = $$

**Solution:**

$$g'\left( x \right) = 2\left( {f\left( {2f\left( x \right) + 2} \right)} \right)$$
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\left( {{d \over {dx}}\left( {f\left( {2f\left( x \right) + 2} \right)} \right)} \right)$$
<br><br>$$ = 2f\left( {2f\left( x \right) + 2} \right)f'\left( {2f\left( x \right)} \right)$$ 
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, + \left. 2 \right).\left( {2f'\left( x \right)} \right)$$
<br><br>$$ \Rightarrow g'\left( 0 \right) = 2f\left( {2f\left( 0 \right) + 2} \right).$$ 
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,f'\left( {2f\left( 0 \right) + 2} \right).2f'\left( 0 \right)$$
<br><br>$$ = 4f\left( 0 \right){\left( {f'\left( 0 \right)} \right)^2}$$
<br><br>$$ = 4\left( { - 1} \right){\left( 1 \right)^2} =  - 4$$

### Example 2 (Year: 2014)

**Question:**

If $$g$$ is the inverse of a function $$f$$ and $$f'\left( x \right) = {1 \over {1 + {x^5}}},$$ then $$g'\left( x \right)$$ is equal to:

**Solution:**

Since $$f(x)$$ and $$g(x)$$ are inverse of each other
<br><br>$$\therefore$$ $$g'\left( {f\left( x \right)} \right) = {1 \over {f'\left( x \right)}}$$
<br><br>$$ \Rightarrow g'\left( {f\left( x \right)} \right) = 1 + {x^5}$$
<br><br>$$\left( \, \right.$$ As $$\,f'\left( x \right) = {1 \over {1 + {x^5}}}$$ $$\left. \, \right)$$
<br><br>Here $$x=g(y)$$
<br><br>$$\therefore$$ $$g'\left( y \right) = 1 + \left\{ {g\left( y \right)} \right\}$$
<br><br>$$ \Rightarrow g'\left( x \right) = 1 + \left\{ {g\left( x \right)} \right\}$$

### Example 3 (Year: 2019)

**Question:**

Let f(x) = log<sub>e</sub>(sin x), (0 &lt; x &lt; $$\pi $$) and g(x) = sin<sup>–1</sup>
(e<sup>–x</sup>
), (x $$ \ge $$ 0). If $$\alpha $$ is a positive real number such that
a = (fog)'($$\alpha $$) and b = (fog)($$\alpha $$), then :

**Solution:**

f(x) = ln(sin x), g(x) = sin<sup>–1</sup> (e<sup>–x</sup>)<br><br>
f(g(x)) = ln(sin(sin<sup>–1</sup> e<sup>–x</sup>)) = -x<br><br>
f(g($$\alpha $$)) = – $$\alpha $$ = b<br><br>
As f(g(x)) = – x <br><br>
$$ \therefore $$ (f(g(x)))' = – 1<br><br>
 $$ \Rightarrow $$ (f(g($$\alpha $$)))' = – 1 = a<br><br>
$$ \therefore $$ b = – $$\alpha $$,
a = – 1<br><br>
$$ \therefore $$ a$$\alpha $$<sup>2</sup> - b$$\alpha $$ - a = - $$\alpha $$<sup>2</sup> + $$\alpha $$<sup>2</sup> + 1 = 1

### Example 4 (Year: 2019)

**Question:**

If ƒ(1) = 1, ƒ'(1) = 3, then the derivative of
ƒ(ƒ(ƒ(x))) + (ƒ(x))<sup>2
</sup> at x = 1 is :

**Solution:**

Given ƒ(1) = 1, ƒ'(1) = 3
<br><br>Let y = ƒ(ƒ(ƒ(x))) + (ƒ(x))<sup>2
</sup>
<br><br>On differentiating both sides with respect to x we get,
<br><br>$${{dy} \over {dx}}$$ = ƒ'(ƒ(ƒ(x))).ƒ'(ƒ(x)).ƒ'(x) + 2ƒ(x).ƒ'(x)
<br><br>Now at x = 1,
<br><br>$${{dy} \over {dx}}$$ = ƒ'(ƒ(ƒ(1))).ƒ'(ƒ(1)).ƒ'(1) + 2ƒ(1).ƒ'(1)
<br><br>= ƒ'(ƒ(1)).ƒ'(1).ƒ'(1) + 2.1.ƒ'(1)
<br><br>= ƒ'(1).ƒ'(1).ƒ'(1) + 2.1.ƒ'(1)
<br><br>= 3$$ \times $$3$$ \times $$3 + 2$$ \times $$3
<br><br>= 33

### Example 5 (Year: 2022)

**Question:**

<p>Let f : R $$\to$$ R be defined as $$f(x) = {x^3} + x - 5$$. If g(x) is a function such that $$f(g(x)) = x,\forall 'x' \in R$$, then g'(63) is equal to ________________.</p>

**Solution:**

<p>$$f(x) = 3{x^2} + 1$$</p>
<p>f'(x) is bijective function</p>
<p>and $$f(g(x)) = x \Rightarrow g(x)$$ is inverse of f(x)</p>
<p>$$g(f(x)) = x$$</p>
<p>$$g'(f(x))\,.\,f'(x) = 1$$</p>
<p>$$g'(f(x)) = {1 \over {3{x^2} + 1}}$$</p>
<p>Put x = 4 we get</p>
<p>$$g'(63) = {1 \over {49}}$$</p>
