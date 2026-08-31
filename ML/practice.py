import numpy as np 

#Q1
student_heights = [160, 165, 170, 175, 180, 185, 190]

mean = np.mean(student_heights)
median = np.median(student_heights)
std = np.std(student_heights, ddof=1) #ddof=1 sample population, ddof=0 entire population
ce = (std / mean) * 100 
print(f"Q1 \n mean:{mean}\n median:{median}\n std:{std}\n ce:{ce}\n")

#Q2
# a) Average house price in a city with some luxury mansions : median
# b) Most popular shoe size in a store : mode 
# c) Average temperature in a city (no extreme values) : mean 
# d) Typical commute time (with some outliers due to traffic) : median

#Q3
"""
Company A: Mean salary = ₹10L, SD = ₹2L Company B: Mean salary = ₹8L, SD = ₹1.5L

a) Which company has higher absolute variability? b) Which company has higher relative variability (CV)? c) If you value consistency, which company is better?

a ) : Company A has higher absolute variability due to the high standard deviation 
b ) : Company A has higher relative variability which is 18.75 
c ) : company B is better
"""

#Q4
"""
Question 4 (15 points): Dataset: [5, 7, 8, 10, 12, 15, 18, 20, 25, 100]

a) Calculate Q1, Q2, Q3, and IQR b) Identify any outliers c) Should you use mean or median? Why?
"""
Dataset =  [5, 7, 8, 10, 12, 15, 18, 20, 25, 100]
Q1 = np.percentile(Dataset, 25)
Q2 = np.percentile(Dataset,50)
Q3 = np.percentile(Dataset, 75)

IQR = Q3 - Q1 
lower_bound = Q1 - 1.5 * IQR 
upper_bound = Q3 + 1.5 * IQR 
print(lower_bound, upper_bound)

outliers = [x  for x in Dataset if not  lower_bound <= x <= upper_bound]
print(outliers)

"""
Question 5 (20 points): You're analyzing e-commerce conversion rates:

Conversion rates (%): [2.1, 2.3, 2.5, 2.4, 2.2, 2.6, 2.3, 2.4, 2.5, 8.9]
The last value (8.9%) was during a special promotion.

a) Calculate mean and median b) Calculate standard deviation c) Identify if 8.9% is an outlier (using IQR method) d) What conversion rate would you report as "typical"? e) Create a frequency distribution with bins: 2.0-2.9%, 3.0-8.9%, 9.0+%
"""

conversation_rate = [2.1, 2.3, 2.5, 2.4, 2.2, 2.6, 2.3, 2.4, 2.5, 8.9]
mean = np.mean(conversation_rate)
median = np.median(conversation_rate)
std = np.std(conversation_rate, ddof=1)

Q1 = np.percentile(conversation_rate, 25)
Q3 = np.percentile(conversation_rate, 75)
IQR = Q3 - Q1 

lower_bound = Q1 - 1.5 * IQR 
upper_bound = Q3 + 1.5 * IQR 
print(lower_bound, upper_bound)
outliers = [x for x in conversation_rate if x < lower_bound or x > upper_bound]
print(outliers ) # yes 8.9 is outliers 

bins = [2.0,3.0,9.0,10.0]
labels = ['2.0-2.9%','3.0-8.9%','9.0+%']

import pandas as pd 
category = pd.cut(conversation_rate,bins=bins, labels=labels, right = False )
print(category )
freq_table = category.value_counts()
print(freq_table)
relative_freq = freq_table / len(conversation_rate)
print(relative_freq)


#Q6
"""
Question 6 (15 points): Create a small Python program that: a) Takes a list of numbers as input b) Calculates and prints: mean, median, mode, variance, SD, IQR c) Identifies any outliers d) Recommends which measure of central tendency to use
"""

num = [10,34,12,65,89,33,34,90,175]
print(f'mean : {np.mean(num)}')
print(f'Median : {np.median(num)}')
print(f'Mode : : 34')
print(f'Variance : {np.var(num,ddof=1)}')
print(f'std : {np.std(num,ddof=1)}')

Q1 = np.percentile(num,25)
Q3 = np.percentile(num,75)
IQR = Q3 - Q1 
print(f'IQR : {IQR}')

lower = Q1 - 1.5 * IQR 
upper = Q3 + 1.5 * IQR
#chedk outliers 
print(lower, upper )
outliers = [x for x in num if not  lower <= x <= upper]
print(f"Outliers : {outliers}")
# we can use median for central tendancy for measurement 


#Q7 
"""
Question 7 (15 points): Explain in your own words (no code): a) Why do we use (n-1) instead of n for sample variance? b) When is SD more useful than variance? c) Why is median better than mean for skewed distributions?

b) std is more useful than variance when we is calculating the heights in cm
c ) median is better than mean when there is some outliers 
"""



"""
Finally I got 74 marks out of 100
"""