---
chapter: probability
topic: bayes-theorem
jee_frequency: 7
years_appeared: [2018, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 15
difficulty: medium
question_types: ['mcq', 'integer']
exams: ['mains']
---

# Probability: Bayes Theorem

**JEE Frequency**: Appeared in **7 years** (2018 - 2025)

**Question Count**: 15 questions

## Question Types

- **MCQ**: 13 questions
- **INTEGER**: 2 questions

## Difficulty Distribution

- **Medium**: 14 questions
- **Easy**: 1 questions

## Worked Examples

### Example 1 (Year: 2018)

**Question:**

A box 'A' contains $$2$$ white, $$3$$ red and $$2$$ black balls. Another box 'B' contains $$4$$ white, $$2$$ red and $$3$$ black balls. If two balls are drawn at random, without eplacement, from a randomly selected box and one ball turns out to be white while the other ball turns out to be red,  then the probability that both balls are drawn from box 'B' is : 

**Solution:**

Probability of drawing a white ball and then a red ball 
<br><br>from bag  B is given by 
$${{{}^4{C_1} \times {}^2{C_1}} \over {{}^9{C_2}}}$$ = $${2 \over 9}$$
<br><br>Probability of drawing a white ball and then a red ball 
<br><br>from bag A is given by $${{{}^2{C_1} \times {}^3{C_1}} \over {{}^7{C_2}}}$$ = $${2 \over 7}$$
<br><br>Hence, the probability of drawing a white ball and then 
<br><br>a red ball from bag B = $${{{2 \over 9}} \over {{2 \over 7} + {2 \over 9}}}$$ = $${{2 \times 7} \over {18 + 14}}$$ = $${7 \over {16}}$$

### Example 2 (Year: 2020)

**Question:**

Box I contains 30 cards numbered 1 to 30 and
Box II contains 20 cards numbered 31 to 50. A
box is selected at random and a card is drawn
from it. The number on the card is found to be
a non-prime number. The probability that the
card was drawn from Box I is :

**Solution:**

Let B<sub>1</sub> be the event where Box-I is selected.
<br><br>And B<sub>2</sub> be the event where Box-II is selected.
<br><br>P(B<sub>1</sub>) = P(B<sub>2</sub>) = $${1 \over 2}$$
<br><br>Let E be the event where selected card is non prime.
<br><br>For B<sub>1</sub> : Prime numbers: {2, 3, 5, 7, 11, 13, 17, 19, 23, 29}
<br><br>For B<sub>2</sub> : Prime numbers: {31, 37, 41, 43, 47}
<br><br>P(E) = P(B<sub>1</sub>) $$ \times $$ $$P\left( {{E \over {{B_1}}}} \right)$$ +  P(B<sub>2</sub>) $$ \times $$ $$P\left( {{E \over {{B_2}}}} \right)$$
<br><br>= $${1 \over 2} \times {{20} \over {30}}$$ + $${1 \over 2} \times {{15} \over {20}}$$
<br><br>Required probability :
<br><br>$$P\left( {{{{B_1}} \over E}} \right)$$ = $${{P\left( {{B_2}} \right).P\left( {{E \over {{B_1}}}} \right)} \over {P\left( E \right)}}$$
<br><br>= $${{{1 \over 2} \times {{20} \over {30}}} \over {{1 \over 2} \times {{20} \over {30}} + {1 \over 2}{{15} \over {20}}}}$$
<br><br>= $${{{2 \over 3}} \over {{2 \over 3} + {3 \ov...

### Example 3 (Year: 2021)

**Question:**

In a group of 400 people, 160 are smokers and non-vegetarian; 100 are smokers and vegetarian and the remaining 140 are non-smokers and vegetarian. Their chances of getting a particular chest disorder are 35%, 20% and 10% respectively. A person is chosen from the group at random and is found to be suffering from the chest disorder. The probability that the selected person is a smoker and non-vegetarian is :

**Solution:**

Consider following events<br><br>A : Person chosen is a smoker and non vegetarian.<br><br>B : Person chosen in a smoker and vegetarian.<br><br>C : Person chosen is a non-smoker and vegetarian.<br><br>E : Person chosen has a chest disorder<br><br>Given <br><br>$$P(A) = {{160} \over {400}}$$
<br><br>$$P(B) = {{100} \over {400}}$$
<br><br>$$P(C) = {{140} \over {400}}$$<br><br>$$P\left( {{E \over A}} \right) = {{35} \over {100}}$$
<br><br>$$P\left( {{E \over B}} \right) = {{20} \over {100}}$$
<br><br>$$P\left( {{E \over C}} \right) = {{10} \over {100}}$$<br><br>To find<br><br>$$P\left( {{A \over E}} \right) = {{P(A)P\left( {{E \over A}} \right)} \over {P(A).P\left( {{E \over A}} \right) + P(B).P\left( {{E \over B}} \right) + P(C).P\left( {{E \over C}} \right)}}$$<br><br>$$ = {{{{160} \over {400}} \times {{35} \over {100}}} \over {{{160} \over {400}} \times {{35} \over {100}} \times {{100} \over {400}} \times {{20} \over {200}} + {{140} \over {400}} \times {{10} \over {100}}}}$$<br><br>$$ =...

### Example 4 (Year: 2022)

**Question:**

<p>Bag A contains 2 white, 1 black and 3 red balls and bag B contains 3 black, 2 red and n white balls. One bag is chosen at random and 2 balls drawn from it at random, are found to be 1 red and 1 black. If the probability that both balls come from Bag A is $${6 \over {11}}$$, then n is equal to __________.</p>

**Solution:**

<img src="https://app-content.cdn.examgoal.net/fly/@width/image/1l8la6rik/8b350f4d-948a-4095-a004-5c8116776062/a60740c0-3efb-11ed-8e30-11b9f1cb84fb/file-1l8la6ril.png?format=png" data-orsrc="https://app-content.cdn.examgoal.net/image/1l8la6rik/8b350f4d-948a-4095-a004-5c8116776062/a60740c0-3efb-11ed-8e30-11b9f1cb84fb/file-1l8la6ril.png" loading="lazy" style="max-width: 100%; height: auto; display: block; margin: 0px auto; max-height: 40vh;" alt="JEE Main 2022 (Online) 24th June Morning Shift Mathematics - Probability Question 92 English Explanation"><br>$$
\begin{aligned}
&amp;P(1 R \text { and } 1 B)=P(A) \cdot P\left(\frac{1 R 1 B}{A}\right)+P(B) \cdot P\left(\frac{1 R 1 B}{B}\right) \\\\
&amp;=\frac{1}{2} \cdot \frac{{ }^{3} C_{1} \cdot{ }^{1} C_{1}}{{ }^{6} C_{2}}+\frac{1}{2} \cdot \frac{{ }^{2} C_{1} \cdot{ }^{3} C_{1}}{{ }^{n+5} C_{2}} \\\\
&amp;P\left(\frac{1 R 1 B}{A}\right)=\frac{\frac{1}{2} \cdot \frac{3}{15}}{\frac{1}{2} \cdot \frac{3}{15}+\frac{1}{2} \cdot \frac{6 \cdot 2}{(...

### Example 5 (Year: 2022)

**Question:**

<p>Bag I contains 3 red, 4 black and 3 white balls and Bag II contains 2 red, 5 black and 2 white balls. One ball is transferred from Bag I to Bag II and then a ball is drawn from Bag II. The ball so drawn is found to be black in colour. Then the probability, that the transferred ball is red, is :</p>

**Solution:**

Let $E \rightarrow$ Ball drawn from Bag II is black.
<br/><br/>
$E_{R} \rightarrow$ Bag I to Bag II red ball transferred.
<br/><br/>
$E_{B} \rightarrow$ Bag I to Bag II black ball transferred.
<br/><br/>
$E_{w} \rightarrow$ Bag I to Bag II white ball transferred.
<br/><br/>
$P\left(E_{R} / E\right)=\frac{P\left(E / E_{R}\right) \cdot P\left(E_{R}\right)}{P\left(E / E_{R}\right) P\left(E_{R}\right)+P\left(E / E_{B}\right) P\left(E_{B}\right)+P\left(E / E_{W}\right) P\left(E_{W}\right)}$
<br/><br/>
Here,
<br/><br/>
$P\left(E_{R}\right)=3 / 10, \quad P\left(E_{B}\right)=4 / 10, \quad P\left(E_{W}\right)=3 / 10$
<br/><br/>
and
<br/><br/>
$$
\begin{aligned}
& P\left(E / E_{R}\right)=5 / 10, \quad P\left(E / E_{B}\right)=6 / 10, \quad P\left(E / E_{W}\right)=5 / 10 \\\\
& \therefore \quad P\left(E_{R} / E\right)=\frac{15 / 100}{15 / 100+24 / 100+15 / 100} \\\\
& =\frac{15}{54}=\frac{5}{18}
\end{aligned}
$$
