---
chapter: indefinite-integrals
topic: standard-integral
jee_frequency: 10
years_appeared: [2004, 2007, 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025]
question_count: 18
difficulty: medium
question_types: ['mcq']
exams: ['mains']
---

# Indefinite Integrals: Standard Integral

**JEE Frequency**: Appeared in **10 years** (2004 - 2025)

**Question Count**: 18 questions

## Question Types

- **MCQ**: 18 questions

## Difficulty Distribution

- **Medium**: 15 questions
- **Easy**: 1 questions
- **Hard**: 2 questions

## Worked Examples

### Example 1 (Year: 2004)

**Question:**

$$\int {{{dx} \over {\cos x - \sin x}}} $$ is equal to 

**Solution:**

$$\int {{{dx} \over {\cos x - \sin x}}} $$
<br><br>$$ = \int {{{dx} \over {\sqrt 2 \cos \left( {x + {\pi  \over 4}} \right)}}} $$
<br><br>$$ = {1 \over {\sqrt 2 }}\int {\sec \left( {x + {\pi  \over 4}} \right)dx} $$
<br><br>$$ = {1 \over {\sqrt 2 }}\log \left| {\tan \left( {{\pi  \over 4} + {x \over 2} + {\pi  \over 8}} \right)} \right| + C$$
<br><br>$$\left[ \, \right.$$ As $$\int {\sec x\,dx}  = \log \left| {\tan \left( {{\pi  \over 4} + {x \over 2}} \right)} \right|$$ $$\left. \, \right]$$
<br><br>$$ = {1 \over {\sqrt 2 }}\log \left| {\tan \left( {{x \over 2} + {{3\pi } \over 8}} \right)} \right| + C$$

### Example 2 (Year: 2004)

**Question:**

If $$\int {{{\sin x} \over {\sin \left( {x - \alpha } \right)}}dx = Ax + B\log \sin \left( {x - \alpha } \right), + C,} $$ then value of 
<br>$$(A, B)$$ is 

**Solution:**

$$\int {{{\sin x} \over {\sin \left( {x - \alpha } \right)}}} dx$$
<br><br>$$ = \int {{{\sin \left( {x - \alpha  + \alpha } \right)} \over {\sin \left( {x - \alpha } \right)}}} dx$$
<br><br>$$ = \int {{{\sin \left( {x - \alpha } \right)\cos \alpha  + \cos \left( {x - \alpha } \right)\sin \alpha } \over {\sin \left( {x - \alpha } \right)}}} $$
<br><br>$$ = \int {\left\{ {\cos \alpha  + \sin \alpha \,\cot \left. {\left( {x - \alpha } \right)} \right\}} \right.} dx$$
<br><br>$$ = \left( {\cos \alpha } \right)x + \left( {\sin \alpha } \right)\log \,\sin \left( {x - \alpha } \right) + C$$
<br><br>$$\therefore$$ $$A = \cos \alpha ,$$ $$B = \sin \alpha $$

### Example 3 (Year: 2007)

**Question:**

$$\int {{{dx} \over {\cos x + \sqrt 3 \sin x}}} $$ equals

**Solution:**

$$I = \int {{{dx} \over {\cos x + \sqrt 3 \sin x}}} $$
<br><br>$$ \Rightarrow I = \int {{{dx} \over {2\left[ {{1 \over 2}\cos x + {{\sqrt 3 } \over 2}\sin x} \right]}}} $$
<br><br>$$ = {1 \over 2}\int {{{dx} \over {\left[ {\sin {\pi  \over 6}\cos x + \cos {\pi  \over 6}\sin x} \right]}}} $$
<br><br>$$ = {1 \over 2}.\int {{{dx} \over {\sin \left( {x + {\pi  \over 6}} \right)}}} $$
<br><br>$$ \Rightarrow I = {1 \over 2}.\int {\cos ec\left( {x + {\pi  \over 6}} \right)dx} $$
<br><br>But we know that 
<br><br>$$\int {\cos ec\,x\,dx}  = \log \left| {\left( {\tan x/2} \right)} \right| + C$$
<br><br>$$\therefore$$ $$I = {1 \over 2}.\log \,\tan \left( {{x \over 2} + {\pi  \over {12}}} \right) + C$$

### Example 4 (Year: 2017)

**Question:**

If $$\,\,\,$$  f$$\left( {{{3x - 4} \over {3x + 4}}} \right)$$ = x + 2, x $$ \ne $$ $$-$$ $${4 \over 3}$$, and  
<br><br>$$\int {} $$f(x) dx = A log$$\left| {} \right.$$1 $$-$$ x $$\left| {} \right.$$ + Bx + C,  
<br><br>then the  ordered pair (A, B) is equal to :
<br><br>(where C is a constant of integration)

**Solution:**

Given, 
<br><br>f$$\left( {{{3x - 4} \over {3x + 4}}} \right)$$ = x + 2,  &nbsp;&nbsp;&nbsp;x &nbsp;$$ \ne $$&nbsp;$$-$$ $${4 \over 3}$$
<br><br>Let, $${{3x - 4} \over {3x + 4}}$$ = t
<br><br>$$ \Rightarrow $$$$\,\,\,$$ 3x $$-$$ 4 = 3tx + 4t
<br><br>$$ \Rightarrow $$$$\,\,\,$$ 3x $$-$$ 3tx = 4t + 4
<br><br>$$ \Rightarrow $$$$\,\,\,$$ x = $${{4t + 4} \over {3 - 3t}}$$
<br><br>So, f(t) = $${{4t + 4} \over {3 - 3t}}$$ + 2 = $${{10 - 2t} \over {3 - 3t}}$$
<br><br>$$\therefore\,\,\,$$ f (x) = $${{10 - 2x} \over {3 - 3x}}$$
<br><br>$$\therefore\,\,\,$$ $$\int {f(x)\,dx} $$
<br><br>= $$\int {{{2x - 10} \over {3x - 3}}} \,dx$$
<br><br>= $$\int {{{2x} \over {3x - 3}} - 10\int {{{dx} \over {3x - 3}}} } $$
<br><br>= $${2 \over 3}\int {{{x - 1} \over {x + 1}}} dx + {2 \over 3}\int {{{dx} \over {x - 1}} - {{10} \over 3}} \int {{{dx} \over {x - 1}}} $$
<br><br>= $${2 \over 3}$$ x + $${2 \over 3}$$ log $$\left| {x - 1} \right|$$ $$-$$ $${{10} \over 3}$$ log $$\left| {x - 1} \right|$$ + C
<br><br>= $$...

### Example 5 (Year: 2017)

**Question:**

The integral 
<br><br>$$\int {\sqrt {1 + 2\cot x(\cos ecx + \cot x)\,} \,\,dx} $$
<br><br>$$\left( {0 &lt; x &lt; {\pi  \over 2}} \right)$$ is equal to : 
<br><br>(where C is a constant of integration)

**Solution:**

Let, I = $$\int {\sqrt {1 + 2\cot x\cos ec + 2{{\cot }^2}x} .dx} $$<br><br>
$$ \Rightarrow $$  I = $$\int {\sqrt {{{{{\sin }^2}x + 2\cos x + 2{{\cos }^2}x} \over {{{\sin }^2}x}}} .dx} $$<br><br>
$$ \Rightarrow $$ I = $$\int {\sqrt {{{1 + 2\cos x + {{\cos }^2}x} \over {\sin x}}} .dx} $$<br><br>
$$ \Rightarrow $$ I = $$\int {\left| {{{1 + \cos x} \over {\sin x}}} \right|dx} $$<br><br>
$$ \Rightarrow $$ I = $$\int {\left| {\cos ec\,x + \cot x} \right|.dx} $$<br><br>
$$ \Rightarrow $$ I = $$\log \left| {\cos ec\,x - \cot x} \right| + \log \left| {\sin x} \right| + C$$<br><br>
$$ \Rightarrow $$ I = $$\log \left| {1 - \cos x} \right| + C$$<br><br>
$$ \Rightarrow $$ I = $$\log \left| {2{{\sin }^2}{x \over 2}} \right| + C$$<br><br>
$$ \Rightarrow $$ I = $$\log \left| {{{\sin }^2}{x \over 2}} \right| + \log 2+ C$$<br><br>
$$ \Rightarrow $$ I = 2$$\log \left| {{{\sin }}{x \over 2}} \right| + C_1$$<br>
