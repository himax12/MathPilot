---
chapter: indefinite-integrals
topic: integration-by-partial-fraction
jee_frequency: 1
years_appeared: [2021]
question_count: 2
difficulty: medium
question_types: ['integer']
exams: ['mains']
---

# Indefinite Integrals: Integration By Partial Fraction

**JEE Frequency**: Appeared in **1 years** (2021 - 2021)

**Question Count**: 2 questions

## Question Types

- **INTEGER**: 2 questions

## Difficulty Distribution

- **Medium**: 1 questions
- **Hard**: 1 questions

## Worked Examples

### Example 1 (Year: 2021)

**Question:**

If $$\int {{{2{e^x} + 3{e^{ - x}}} \over {4{e^x} + 7{e^{ - x}}}}dx = {1 \over {14}}(ux + v{{\log }_e}(4{e^x} + 7{e^{ - x}})) + C} $$, where C is a constant of integration, then u + v is equal to _____________.

**Solution:**

$$2{e^x} + 3{e^{ - x}} = A(4{e^x} + 7{e^{ - x}}) + B(4{e^x} - 7{e^{ - x}}) + \lambda $$<br><br>2 = 4A + 4B ; 3 = 7A $$-$$ 7B ; $$\lambda$$ = 0<br><br>$$A + B = {1 \over 2}$$<br><br>$$A - B = {3 \over 7}$$<br><br>$$A = {1 \over 2}\left( {{1 \over 2} + {3 \over 7}} \right) = {{7 + 6} \over {28}} = {{13} \over {28}}$$<br><br>$$B = A - {3 \over 7} = {{13} \over {28}} - {3 \over 7} = {{13 - 12} \over {28}} = {1 \over {28}}$$<br><br>$$\int {{{13} \over {28}}dx + {1 \over {28}}\int {{{4{e^x} - 7{e^{ - x}}} \over {4{e^x} + 7{e^{ - x}}}}} dx} $$<br><br>= $${{13} \over {28}}x + {1 \over {28}}\ln |4{e^x} + 7{e^{ - x}}| + C$$<br><br>$$u = {{13} \over 2};v = {1 \over 2}$$<br><br>$$\Rightarrow$$ u + v = 7

### Example 2 (Year: 2021)

**Question:**

If $$\int {{{\sin x} \over {{{\sin }^3}x + {{\cos }^3}x}}dx = } $$ 
<br><br>$$\alpha {\log _e}|1 + \tan x| + \beta {\log _e}|1 - \tan x + {\tan ^2}x| + \gamma {\tan ^{ - 1}}\left( {{{2\tan x - 1} \over {\sqrt 3 }}} \right) + C$$, when C is constant of integration, then the value of $$18(\alpha  + \beta  + {\gamma ^2})$$ is ______________.

**Solution:**

$$ = \int {{{{{\sin x} \over {{{\cos }^3}x}}} \over {1 + {{\tan }^3}x}}dx = \int {{{\tan x.{{\sec }^2}x} \over {(\tan x + 1)(1 + {{\tan }^2}x - \tan x)}}dx} } $$<br><br>Let $$\tan x = t \Rightarrow {\sec ^2}x.\,dx = dt$$<br><br>$$ = \int {{t \over {(t + 1)({t^2} - t + 1)}}dt} $$<br><br>$$ = \int {\left( {{A \over {t + 1}} + {{B(2t - 1)} \over {{t^2} - t + 1}} + {C \over {{t^2} - t + 1}}} \right)dx} $$<br><br>$$ \Rightarrow A({t^2} - t + 1) + B(2t - 1)({t^2} - t + 1) + C(t + 1) = t$$<br><br>$$ \Rightarrow {t^2}(A + 2B) + t( - A + B + C) + A - B + C = 1$$<br><br>$$\therefore$$ $$A + 2B = 0$$ ..... (1)<br><br>$$ - A + B + C = 1$$ ... (2)<br><br>$$A - B + C = 0$$ ... (3)<br><br>$$ \Rightarrow C = {1 \over 2} \Rightarrow A - B =  - {1 \over 2}$$ ... (4)<br><br>$$A + 2B = 0$$<br><br>$$A - B =  - {1 \over 2}$$<br><br>$$\Rightarrow$$ $$3B = {1 \over 2} \Rightarrow B = {1 \over 6}$$<br><br>$$A =  - {1 \over 3}$$<br><br>$$I =  - {1 \over 3}\int {{{dt} \over {1 + t}} + {1 \over 6}\int {{{2t - 1} ...
