---
chapter: probability
topic: total-probability-theorem
jee_frequency: 4
years_appeared: [2018, 2023, 2024, 2025]
question_count: 4
difficulty: medium
question_types: ['mcq']
exams: ['mains']
---

# Probability: Total Probability Theorem

**JEE Frequency**: Appeared in **4 years** (2018 - 2025)

**Question Count**: 4 questions

## Question Types

- **MCQ**: 4 questions

## Difficulty Distribution

- **Medium**: 3 questions
- **Hard**: 1 questions

## Worked Examples

### Example 1 (Year: 2018)

**Question:**

A bag contains 4 red and 6 black balls. A ball is drawn at random from the bag, its colour is observed and
this ball along with two additional balls of the same colour are returned to the bag. If now a ball is drawn at
random from the bag, then the probability that this drawn ball is red, is :

**Solution:**

<img class="question-image" src="https://imagex.cdn.examgoal.net/FRHuFr5edm6Tja4Gu/yJLnWIShoB9ykwqjLQu8SsxaY6a5c/8HbYlkf1aBJy58JNefAXaD/image.png" loading="lazy" alt="JEE Main 2018 (Offline) Mathematics - Probability Question 190 English Explanation"> 
<br><br>If we follow path 1, then probability of getting 1st ball black $$ = {6 \over {10}}$$ and probability of getting 2nd ball red when there is 4 R and 8 B balls = $${4 \over {12}}$$.
<br><br>So, the probability of getting 1st ball black and 2nd ball red = $${6 \over {10}} \times {4 \over {12}}$$.
<br><br>If we follow path 2, then the probability of getting 1st ball red $$ = {4 \over {10}}$$ and probability of getting 2nd ball red when in the bag there is 6 red and 6 black balls = $${6 \over {12}}$$
<br><br>$$\therefore\,\,\,$$  Probability of getting 2nd ball as red 
<br><br>$$ = {6 \over {10}} \times {4 \over {12}} + {4 \over {10}} \times {6 \over {12}}$$
<br><br>$$ = {1 \over 5} + {1 \over 5}$$
<br><br>$$ = {2 \over 5}$$ 

### Example 2 (Year: 2023)

**Question:**

A bag contains 6 white and 4 black balls. A die is rolled once and the number of balls equal to the number obtained on the die are drawn from the bag at random. The probability that all the balls drawn are white is :

**Solution:**

Let $X$ be the number rolled on the die, and let $W$ be the event that all balls drawn are white. We want to find the probability $P(W)$, which can be calculated using the law of total probability as follows :

<br/><br/>$$P(W) = \sum\limits_{x=1}^{6} P(W|X=x)P(X=x)$$

<br/><br/>The probability of rolling any number from 1 to 6 on the die is equal, so $P(X=x) = \frac{1}{6}$ for all $x \in \{1, 2, 3, 4, 5, 6\}$. 

<br/><br/>Now let's calculate the conditional probabilities $P(W|X=x)$ for each possible value of $x$ :

<br/><br/>1. $P(W|X=1) = {{{}^6{C_1}} \over {{}^{10}{C_1}}}= \frac{6}{10} = \frac{3}{5}$, since there are 6 white balls out of a total of 10 balls.
<br/><br/>2. $P(W|X=2) = {{{}^6{C_2}} \over {{}^{10}{C_2}}} = \frac{15}{45} = \frac{1}{3}$, since there are 15 ways to choose 2 white balls out of 6, and 45 ways to choose 2 balls out of 10.
<br/><br/>3. $P(W|X=3) = {{{}^6{C_3}} \over {{}^{10}{C_3}}} = \frac{20}{120} = \frac{1}{6}$, since there are 20 ways to choose 3 white ball...

### Example 3 (Year: 2024)

**Question:**

A bag contains 8 balls, whose colours are either white or black. 4 balls are drawn at random without replacement and it was found that 2 balls are white and other 2 balls are black. The probability that the bag contains equal number of white and black balls is :

**Solution:**

$\begin{aligned} & \mathrm{P}(4 \mathrm{~W} 4 \mathrm{~B} / 2 \mathrm{~W} 2 \mathrm{~B})= \\\\ & \frac{P(4 W 4 B) \times P(2 W 2 B / 4 W 4 B)}{P(2 W 6 B) \times P(2 W 2 B / 2 W 6 B)+P(3 W 5 B) \times P(2 W 2 B / 3 W 5 B)} \\ & +\ldots \ldots \ldots \ldots+P(6 W 2 B) \times P(2 W 2 B / 6 W 2 B)\end{aligned}$
<br/><br/>$\begin{aligned} & =\frac{\frac{1}{5} \times \frac{{ }^4 \mathrm{C}_2 \times{ }^4 \mathrm{C}_2}{{ }^8 \mathrm{C}_4}}{\frac{1}{5} \times \frac{{ }^2 \mathrm{C}_2 \times{ }^6 \mathrm{C}_2}{{ }^8 \mathrm{C}_4}+\frac{1}{5} \times \frac{{ }^3 \mathrm{C}_2 \times{ }^5 \mathrm{C}_2}{{ }^8 \mathrm{C}_4}+\ldots+\frac{1}{5} \times \frac{{ }^6 \mathrm{C}_2 \times{ }^2 \mathrm{C}_2}{{ }^8 \mathrm{C}_4}} \\\\ & =\frac{2}{7}\end{aligned}$

### Example 4 (Year: 2025)

**Question:**

<p>Bag 1 contains 4 white balls and 5 black balls, and Bag 2 contains <i>n</i> white balls and 3 black balls. One ball is drawn randomly from Bag 1 and transferred to Bag 2. A ball is then drawn randomly from Bag 2. If the probability, that the ball drawn is white, is $ \frac{29}{45} $, then <i>n</i> is equal to:</p>

**Solution:**

<p>$$\begin{aligned}
& \text { Bag } 1=\{4 \mathrm{~W}, 5 \mathrm{~B}\} \\
& \text { Bag } \mathbf{2}=\{\mathbf{n W}, \mathbf{3 B}\} \\
& \mathrm{P}\left(\frac{\mathrm{~W}}{\mathrm{Bag} 2}\right)=\frac{29}{45} \\
& \Rightarrow \mathrm{P}\left(\frac{\mathrm{~W}}{\mathrm{~B}_1}\right) \times \mathrm{P}\left(\frac{\mathrm{~W}}{\mathrm{~B}_2}\right)+\mathrm{P}\left(\frac{\mathrm{~B}}{\mathrm{~B}_1}\right) \times \mathrm{P}\left(\frac{\mathrm{~W}}{\mathrm{~B}_2}\right)=\frac{29}{45} \\
& \frac{4}{9} \times \frac{\mathrm{n}+1}{\mathrm{n}+4}+\frac{5}{9} \times \frac{\mathrm{n}}{\mathrm{n}+4}=\frac{29}{45}
\end{aligned}$$</p>
<p>$\mathrm{n = 6}$</p>
