---
chapter: differentiation
topic: successive-differentiation
jee_frequency: 8
years_appeared: [2003, 2017, 2019, 2020, 2022, 2023, 2024, 2025]
question_count: 19
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Differentiation: Successive Differentiation

**JEE Frequency**: Appeared in **8 years** (2003 - 2025)

**Question Count**: 19 questions

## Question Types

- **MCQ**: 13 questions
- **INTEGER**: 6 questions

## Difficulty Distribution

- **Medium**: 13 questions
- **Hard**: 5 questions
- **Easy**: 1 questions

## Worked Examples

### Example 1 (Year: 2003)

**Question:**

If $$f\left( x \right) = {x^n},$$ then the value of 
<p>$$f\left( 1 \right) - {{f'\left( 1 \right)} \over {1!}} + {{f''\left( 1 \right)} \over {2!}} - {{f'''\left( 1 \right)} \over {3!}} + ..........{{{{\left( { - 1} \right)}^n}{f^n}\left( 1 \right)} \over {n!}}$$  is</p>

**Solution:**

$$f\left( x \right) = {x^n} \Rightarrow f\left( 1 \right) = 1$$ 
<br><br>$$f'\left( x \right) = n{x^{n - 1}} \Rightarrow f'\left( 1 \right) = n$$
<br><br>$$f''\left( x \right) = n\left( {n - 1} \right){x^{n - 2}}$$
<br><br>$$ \Rightarrow f''\left( 1 \right) = n\left( {n - 1} \right)$$
<br><br>$$\therefore$$ $${f^n}\left( x \right) = n!$$
<br><br>$$ \Rightarrow {f^n}\left( 1 \right) = n!$$
<br><br>$$ = 1 - {n \over {1!}} + {{n\left( {n - 1} \right)} \over {2!}}{{n\left( {n - 1} \right)\left( {n - 2} \right)} \over {3!}}$$ 
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, + .... + {\left( { - 1} \right)^n}{{n!} \over {n!}}$$
<br><br>$$ = {}^n\,{C_0} - {}^n\,{C_1} + {}^n\,{C_2} - {}^n\,{C_3}$$
<br><br>$$\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, + ...... + {\left( { - 1} \right)^n}\,{}^n{C_n} = 0$$

### Example 2 (Year: 2017)

**Question:**

Let f be a polynomial function such that
<br><br>f (3x) = f ' (x) . f '' (x),  for all x $$ \in $$ <b>R</b>. Then : 

**Solution:**

<p>Let $$f(x) = {a_0}{x^n} + {a_1}{x^{n - 1}} + {a_2}{x^{n - 1}} + \,\,....\,\, + {a_{n - 1}}x + {a_n}$$</p>
<p>$$f'(x) = {a_0}n{x^{n - 1}} + {a_1}(n - 1){x^{n - 2}} + \,\,.....\,\, + {a_{n - 1}}$$</p>
<p>$$f''(x) = {a_0}n(n - 1){x^{n - 2}} + {a_1}(n - 1)(n - 2){x^{n - 3}} + \,\,....\,\, + {a_{n - 2}}$$</p>
<p>Now,</p>
<p>$$f(3x) = {3^n}{a_0}{x^n} + {3^{n - 1}}{a_1}{x^{n - 1}} + {3^{n - 2}}{a_2}{x^{n - 2}} + \,\,....\,\, + 3{a_{n - 1}} + {a_n}$$</p>
<p>$$f'(x)\,.\,f''(x) = [{a_0}n{x^{n - 1}} + {a_1}(n - 1){x^{n - 2}} + \,\,....\,\, + {a_{n - 1}}]$$</p>
<p>$$[{a_0}n(n - 1){x^{n - 2}} + {a_1}(n - 1)(n - 2){x^{n - 3}} + \,\,....\,\, + {a_{n - 2}}]$$</p>
<p>Comparing highest powers of x, we get</p>
<p>$${3^n}{a_0}{x_n} = a_0^2(n - 1){x^{n - 1 + n - 2}} = a_0^2{n^2}(n - 1){x^{2n - 3}}$$</p>
<p>Therefore, $$2n - 3 = n$$</p>
<p>$$\Rightarrow$$ n = 3 and $${3^n}{a_0} = a_0^2{n^2}(n - 1)$$</p>
<p>$$ \Rightarrow {a_0} = 27 = {3 \over 2}$$</p>
<p>Therefore, $$f(x) = {3 \over 2}{x^3} + {a_1}{x^2} ...

### Example 3 (Year: 2019)

**Question:**

Let f : R $$ \to $$ R be a function such that  f(x) = x<sup>3</sup> + x<sup>2</sup>f'(1) + xf''(2) + f'''(3), x $$ \in $$ R.  Then f(2) equals -

**Solution:**

f(x) = x<sup>3</sup> + x<sup>2</sup>f '(1) + xf ''(2) + f '''(3)
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;f '(x) = 3x<sup>2</sup> + 2xf '(1) + f ''(x)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. . . . . (1)
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;f ''(x) = 6x + 2f '(1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. . . . . . (2)
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;f '''(x) = 6 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. . . . . .(3)
<br><br>put x = 1 in equation (1) : 
<br><br>f '(1) = 3 + 2f '(1) + f ''(2)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. . . . .(4)
<br><br>put x = 2 in equation (2) : 
<br><br>f ''(2) = 12 + 2f '(1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. . . . .(5)
<br><br>from equation (4) &amp; (5) : 
<br><br>$$-$$3 $$-$$ f '(1) = 12 + 2f'(1)
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;3f '(1) = $$-$$ 15
<br><br>$$ \Rightarrow $$&nbsp;&nbsp;f '(1) = $$-$$ 5 $$ \Rightarrow $$&nbsp;&nbsp;f ''(2) = 2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. . . . .(2)
<br><br>put x = 3 in equation (3) :
<br><br>f ''' (3) = 6
<br><br>$$ \therefore $$&nbsp;&nbsp;f(x) = x<sup>...

### Example 4 (Year: 2020)

**Question:**

If y<sup>2</sup> + log<sub>e</sub> (cos<sup>2</sup>x) = y, <br>$$x \in \left( { - {\pi  \over 2},{\pi  \over 2}} \right)$$, then : 

**Solution:**

Given y<sup>2</sup> + log<sub>e</sub> (cos<sup>2</sup>x) = y .....(1)
<br><br>Put x  = 0, we get
<br><br>y<sup>2</sup> + log<sub>e</sub> (1) = y
<br><br>$$ \Rightarrow $$ y<sup>2</sup> = y
<br><br>$$ \Rightarrow $$ y = 0, 1
<br><br>Differentiating (1) we get
<br><br>2yy' + $${1 \over {\cos x}}\left( { - \sin x} \right)$$ = y'
<br><br>$$ \Rightarrow $$ 2yy' - 2tanx = y'  ....(2)
<br><br>From (2) when x = 0, y = 0 then y'(0) = 0
<br><br>From (2) when x = 0, y = 1 then 
<br><br>2y' = y'
<br><br>$$ \Rightarrow $$ y'(0) = 0
<br><br>Again differentiating (2) we get
<br><br>2(y')<sup>2</sup>
 + 2yy'' – 2sec<sup>2</sup>x = y''
<br><br>from (2) when x = 0, y = 0, y’(0) = 0 then
<br><br>y”(0) = -2
<br><br>Also from (2) when x = 0, y = 1, y’(0) = 0 then
<br><br>y”(0) = 2
<br><br>$$ \therefore $$ |y''(0)| = 2

### Example 5 (Year: 2022)

**Question:**

<p>If $$y(x) = {\left( {{x^x}} \right)^x},\,x > 0$$, then $${{{d^2}x} \over {d{y^2}}} + 20$$ at x = 1 is equal to ____________.</p>

**Solution:**

<p>$$\because$$ $$y(x) = {\left( {{x^x}} \right)^x}$$</p>
<p>$$\therefore$$ $$y = {x^{{x^2}}}$$</p>
<p>$$\therefore$$ $${{dy} \over {dx}} = {x^2}\,.\,{x^{{x^2} - 1}} + {x^{{x^2}}}\ln x\,.\,2x$$</p>
<p>$$\therefore$$ $${{dx} \over {dy}} = {1 \over {{x^{{x^2} + 1}}(1 + 2\ln x)}}$$ ..... (i)</p>
<p>Now, $${{{d^2}x} \over {dx^2}} = {d \over {dx}}\left( {{{\left( {{x^{{x^2} + 1}}(1 + 2\ln x)} \right)}^{ - 1}}} \right)\,.\,{{dx} \over {dy}}$$</p>
<p>$$ = {{ - x{{\left( {{x^{{x^2} + 1}}(1 + 2\ln x)} \right)}^{ - 2}}\,.\,{x^{{x^2}}}(1 + 2\ln x)({x^2} + 2{x^2}\ln x + 3)} \over {{x^{{x^2}}}(1 + 2\ln x)}}$$</p>
<p>$$ = {{ - {x^{{x^2}}}(1 + 2\ln x)({x^3} + 3 + 2{x^2}\ln x)} \over {{{\left( {{x^{{x^2}}}(1 + 2\ln x)} \right)}^3}}}$$</p>
<p>$${{{d^2}x} \over {d{y^2}(at\,x = 1)}} =  - 4$$</p>
<p>$$\therefore$$ $${{{d^2}x} \over {d{y^2}(at\,x = 1)}} + 20 = 16$$</p>
