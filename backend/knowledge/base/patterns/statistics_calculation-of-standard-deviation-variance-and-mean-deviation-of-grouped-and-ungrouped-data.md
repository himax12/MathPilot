---
chapter: statistics
topic: calculation-of-standard-deviation-variance-and-mean-deviation-of-grouped-and-ungrouped-data
jee_frequency: 21
years_appeared: [2003, 2004, 2005, 2006, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
question_count: 117
difficulty: medium
---

# Statistics: Calculation Of Standard Deviation Variance And Mean Deviation Of Grouped And Ungrouped Data

**JEE Frequency**: 21 years | **Questions**: 117

## Statistics: Standard Deviation, Variance & Mean Deviation

**JEE Frequency:** High (21 Years, 117 Questions)

This document summarizes key concepts and strategies for solving JEE problems related to standard deviation, variance, and mean deviation of grouped and ungrouped data.

**1. Pattern Recognition:**

*   Questions frequently involve calculating variance/standard deviation given sums of observations and their squares ($$\sum x_i$$ and $$\sum x_i^2$$).
*   Look for problems involving correction of errors in data sets and their impact on variance.
*   Questions might test the properties of variance and standard deviation concerning change of origin and scale.

**2. Core Formulas:**

*   **Mean (Ungrouped):**  $$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$
*   **Variance (Ungrouped):** $$\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2 = \frac{1}{n}\sum_{i=1}^{n} x_i^2 - (\bar{x})^2$$
*   **Standard Deviation (Ungrouped):** $$\sigma = \sqrt{\sigma^2}$$
*   **Mean Deviation about Mean (Ungrouped):** $$MD = \frac{1}{n}\sum_{i=1}^{n} |x_i - \bar{x}|$$
*   **Variance (Grouped):** $$\sigma^2 = \frac{1}{N} \sum_{i=1}^{n} f_i (x_i - \bar{x})^2 = \frac{1}{N}\sum_{i=1}^{n} f_i x_i^2 - (\bar{x})^2$$, where $$N = \sum f_i$$

**3. Standard Approach:**

1.  **Identify the type of data:** Grouped or Ungrouped.
2.  **Calculate the mean:**  Use the appropriate formula for grouped or ungrouped data.
3.  **Calculate the variance:**  Use the formula that utilizes $$\sum x_i^2$$ and $$\sum x_i$$ as it is often easier for JEE problems. For grouped data, consider using assumed mean method if the values are large.
4.  **Calculate the standard deviation:** Take the square root of the variance.
5.  **For error correction problems:** Calculate the initial variance, adjust the $$\sum x_i$$ and $$\sum x_i^2$$ values with the corrected data, and then recalculate the variance.

**4. Quick Tips:**

*   **Change of Origin & Scale:** If $$y_i = a x_i + b$$, then
    *   $$\bar{y} = a\bar{x} + b$$
    *   $$\sigma_y = |a|\sigma_x$$ (Standard deviation is affected by change of scale only, not origin).
    *   $$\sigma_y^2 = a^2 \sigma_x^2$$ (Variance is affected by the square of the change of scale).
*   **Consecutive Integers:** The variance of the first *n* natural numbers is $$\frac{n^2 - 1}{12}$$. This can save time if applicable.

**5. Common Mistakes:**

*   **Incorrect Formula Selection:** Using the ungrouped formula for grouped data, or vice versa.
*   **Sign Errors:**  Carelessness while calculating the deviations (x<sub>i</sub> - x̄).
*   **Error Correction Miscalculation:** Forgetting to subtract the incorrect value and add the correct value when updating $$\sum x_i$$ and $$\sum x_i^2$$. Remember to square the values for $$\sum x_i^2$$ calculations.
