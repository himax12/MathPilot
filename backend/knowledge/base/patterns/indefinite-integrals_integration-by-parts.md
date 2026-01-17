---
chapter: indefinite-integrals
topic: integration-by-parts
jee_frequency: 6
years_appeared: [2014, 2019, 2022, 2023, 2024, 2025]
question_count: 8
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Indefinite Integrals: Integration By Parts

**JEE Frequency**: Appeared in **6 years** (2014 - 2025)

**Question Count**: 8 questions

## Question Types

- **MCQ**: 7 questions
- **INTEGER**: 1 questions

## Difficulty Distribution

- **Medium**: 7 questions
- **Hard**: 1 questions

## Worked Examples

### Example 1 (Year: 2014)

**Question:**

The integral $$\int {\left( {1 + x - {1 \over x}} \right){e^{x + {1 \over x}}}dx} $$ is equal to 

**Solution:**

Let $$I = \int {\left( {1 + x - {1 \over x}} \right)} {e^{x + {\raise0.5ex\hbox{$\scriptstyle 1$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle x$}}}}dx$$
<br><br>$$ = \int {{e^{x + {\raise0.5ex\hbox{$\scriptstyle 1$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle x$}}}}} dx + \int {\left( {x - {1 \over x}} \right)} {e^{x + {\raise0.5ex\hbox{$\scriptstyle 1$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle x$}}}}dx$$
<br><br>$$ = x.{e^{x + {\raise0.5ex\hbox{$\scriptstyle 1$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle x$}}}} - \int {x\left( {1 - {1 \over {{x^2}}}} \right)} {e^{x+{\raise0.5ex\hbox{$\scriptstyle 1$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle x$}}}}dx$$
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, + \int {\left( {x - {1 \over x}} \right)} {e^{x + {\raise0.5ex\hbox{$\scriptstyle 1$}
\kern-0.1em/\kern-0.15em
\lower0.25ex\hbox{$\scriptstyle x$}}}}dx$$
<br><br>$$ = x.{e^{x + {1 \over x}}} - \int {\left( {x...

### Example 2 (Year: 2019)

**Question:**

The integral $$\int \, $$cos(log<sub>e</sub> x) dx  is equal to : (where C is a constant of integration) 

**Solution:**

$${\rm I} = \int {\cos \left( {\ell nx} \right)} dx$$
<br><br>$${\rm I} = \cos (\ln x).x + \int {\sin \left( {\ell nx} \right)dx} $$
<br><br>$${\rm I} = \cos \left( {\ell nx} \right)x + \left[ {\sin \left( {\ell nx} \right).x - \int {\cos \left( {\ell nx} \right)dx} } \right]$$
<br><br>$${\rm I} = {x \over 2}\left[ {\sin \left( {\ell nx} \right) + \cos \left( {\ell nx} \right)} \right] + C$$

### Example 3 (Year: 2022)

**Question:**

<p>For $$I(x)=\int \frac{\sec ^{2} x-2022}{\sin ^{2022} x} d x$$, if $$I\left(\frac{\pi}{4}\right)=2^{1011}$$, then</p>

**Solution:**

<p>Given,</p>
<p>$$I(x) = \int {{{{{\sec }^2}x - 2022} \over {{{\sin }^{2022}}x}}dx} $$</p>
<p>$$ = \int {{{{{\sec }^2}x} \over {{{\sin }^{2022}}x}}dx - \int {{{2022} \over {{{\sin }^{2022}}x}}dx} } $$</p>
<p>$$ = \int {{1 \over {{{\sin }^{2022}}x}}\,.\,{{\sec }^2}x\,dx - \int {{{2022} \over {{{\sin }^{2022}}x}}dx} } $$</p>
<p>$$ = {1 \over {{{\sin }^{2022}}x}}\,.\,\tan x - \int {\left( {{{ - 2022} \over {{{\sin }^{2023}}x}}\,.\,\cos x\,.\,\tan x} \right)dx - \int {{{2022} \over {{{\sin }^{2022}}x}}dx + C} } $$</p>
<p>$$ = {{\tan x} \over {{{\sin }^{2022}}x}} + \int {\left( {{{2022} \over {{{\sin }^{2023}}x}}\,.\,\cos x\,.\,{{\sin x} \over {\cos x}}} \right)dx - \int {{{2022} \over {{{\sin }^{2022}}x}}dx + C} } $$</p>
<p>$$ = {{\tan x} \over {{{\sin }^{2022}}x}} + \int {{{2022} \over {{{\sin }^{2022}}x}}dx - \int {{{2022} \over {{{\sin }^{2022}}x}}dx} } $$</p>
<p>$$ = {{\tan x} \over {{{\sin }^{2022}}x}} + C$$</p>
<p>Given, $$I\left( {{\pi  \over 4}} \right) = {2^{1011}}$$</p>
<p>$$\th...

### Example 4 (Year: 2023)

**Question:**

<p>If $$I(x) = \int {{e^{{{\sin }^2}x}}(\cos x\sin 2x - \sin x)dx} $$ and $$I(0) = 1$$, then $$I\left( {{\pi  \over 3}} \right)$$ is equal to :</p>

**Solution:**

$$
\begin{aligned}
& \text { Given, } I(x)=\int e^{\sin ^2 x}(\cos x \sin 2 x-\sin x) d x \\\\
& =\int e^{\sin ^2 x} \cdot \cos x \cdot \sin 2 x d x-\int \sin x e^{\sin ^2 x} d x \\\\
& =\int \frac{\cos x}{\mathrm{I}} \cdot \frac{e^{\sin ^2 x} \cdot \sin 2 x}{\mathrm{II}} d x-\int \sin x \cdot e^{\sin ^2 x} d x \\\\
& =\cos x \cdot e^{\sin ^2 x}-\int(-\sin x) e^{\sin ^2 x} d x-\int \sin x e^{\sin ^2 x} d x \\\\
& =\cos x \cdot e^{\sin ^2 x}+\int \sin x e^{\sin ^2 x} \cdot d x-\int \sin x \cdot e^{\sin ^2 x} d x+C
\end{aligned}
$$
<br/><br/>$I(x)=e^{\sin ^2 x} \cdot \cos x+C$
<br/><br/>Given, $I(0)=1 \Rightarrow C=0$
<br/><br/>So, $ I(x)=e^{\sin ^2 x} \cdot \cos x$
<br/><br/>$$
\Rightarrow I(\pi / 3)=e^{3 / 4} \cdot \frac{1}{2}=\frac{e^{3 / 4}}{2}
$$

### Example 5 (Year: 2023)

**Question:**

<p>Let $$I(x)=\int \frac{x^{2}\left(x \sec ^{2} x+\tan x\right)}{(x \tan x+1)^{2}} d x$$. If $$I(0)=0$$, then $$I\left(\frac{\pi}{4}\right)$$ is equal to :</p>

**Solution:**

We have,
<br/><br/>$$
\begin{aligned}
I(x)= & \int \frac{x^2\left(x \sec ^2 x+\tan x\right)}{(x \tan x+1)^2} d x \\\\
= & x^2 \int \frac{x \sec ^2 x+\tan x}{(x \tan x+1)^2} d x \\\\
& \quad-\int\left\{\frac{d}{d x}\left(x^2\right) \int \frac{x \sec ^2 x+\tan x}{(x \tan x+1)^2} d x\right\} d x \text { (integration by parts) }
\end{aligned}
$$
<br/><br/>$$
=x^2\left(\frac{-1}{x \tan x+1}\right)+\int \frac{2 x}{x \tan x+1} d x
$$
<br/><br/>Now, let 
<br/><br/>$$
\begin{aligned}
I_1 & =2 \int \frac{x}{x \tan x+1} d x \\\\
& =2 \int \frac{x \cos x}{x \sin x+\cos x} d x
\end{aligned}
$$
<br/><br/>$$
\begin{aligned}
& \text { On putting } x \sin x+\cos x=t \\\\
& \Rightarrow  (x \cos x+\sin x-\sin x) d x=d t \\\\
& \Rightarrow  x \cos x d x=d t
\end{aligned}
$$
<br/><br/>$$
\begin{aligned}
&\therefore I_1 =2 \int \frac{d t}{t}=2 \log t+c \\\\
& =2 \log (x \sin x+\cos x)+c
\end{aligned}
$$
<br/><br/>$$
\begin{gathered}
\therefore I(x)=\frac{-x^2}{x \tan x+1}+2 \log(x \sin x+\cos x)+c
\end{gath...
