import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt


student_score = [96,45,82,90,98,30,36,65,68,75]


#mean, median and mode
mean = np.mean(student_score)
median = np.median(student_score)
print(f"Mean and Median : {mean} , {median}")
##find the range = max-min
find_range = np.max(student_score) - np.min(student_score)
print(f"Range : {find_range}")


#find the variance 
#method : numpy formula 
variance = np.var(student_score,ddof=1)
print(f"Variance by numpy : {variance}")

#method 2 : Variance manual
mean = np.sum(student_score)/ len(student_score) # np.mean(student_score)
variance2 = np.sum([(x-mean)**2 for x in student_score])/(len(student_score)-1)
print(f"Manual calculated variance : {variance2}")


##standard deviation 
std = variance ** 0.5
std1 = np.std(student_score)
print(f"Standard deviation : {std}")
print(f"standard deviation by numpy : {std1}")

##coefficient of variation
cv = (std / mean) * 100 
print(f"coefficient of variation : {cv}")

#IQR
q1 = np.percentile(student_score,q=25)
q3 = np.percentile(student_score,q=75)
IQR = q3-q1
print(f"IQR : {IQR}")

lower_bound_outliers = q1 - 1.5 * IQR 
upper_bound_outliers = q3 + 1.5 * IQR 
print(f"lower bound outliers : {lower_bound_outliers}")
print(f"upper bound outliers : {upper_bound_outliers}")


#data visualization 
#Frequency distribution 

scores = [40,60,34,60,55,67,90,98,78,99]

bins = [40,50,60,70,80,90,100]
labels = ['D','C','B','B+','A','A+']

category = pd.cut(scores, bins=bins, labels=labels,right=False)
print(category)
freq_table = category.value_counts()
print(freq_table)
relative_freq = freq_table / len(scores)
print(relative_freq)




# Generate sample data
data = np.random.normal(100, 15, 1000)  # mean=100, sd=15, n=1000

# Create histogram
plt.figure(figsize=(10, 6))
plt.subplot(1,1,1)
plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Histogram of Data Distribution')
plt.axvline(np.mean(data), color='red', linestyle='--', label=f'Mean: {np.mean(data):.2f}')
plt.axvline(np.median(data), color='green', linestyle='--', label=f'Median: {np.median(data):.2f}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()



# Sample data
data = [12, 15, 18, 20, 22, 25, 28, 30, 35, 40, 45, 100]  # 100 is outlier

# # Create box plot
plt.figure(figsize=(8, 6))
box = plt.boxplot(data, vert=True, patch_artist=True)
box['boxes'][0].set_facecolor('lightblue')
plt.ylabel('Values')
plt.title('Box Plot Example')
plt.grid(True, alpha=0.3)

# Add annotations
q1 = np.percentile(data, 25)
median = np.percentile(data, 50)
q3 = np.percentile(data, 75)

plt.text(1.1, q1, f'Q1: {q1}', fontsize=10)
plt.text(1.1, median, f'Median: {median}', fontsize=10)
plt.text(1.1, q3, f'Q3: {q3}', fontsize=10)

plt.show()


# Categorical data
categories = ['Product A', 'Product B', 'Product C', 'Product D']
sales = [150, 230, 180, 200]

plt.figure(figsize=(10, 6))
plt.bar(categories, sales, color='steelblue', edgecolor='black')
plt.xlabel('Products')
plt.ylabel('Sales (units)')
plt.title('Product Sales Comparison')
plt.grid(True, alpha=0.3, axis='y')
plt.show()




# Generate correlated data
x = np.random.rand(100) * 100
y = 2 * x + 10 + np.random.randn(100) * 10  # y ≈ 2x + 10

plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.6, edgecolors='black')
plt.xlabel('X Variable')
plt.ylabel('Y Variable')
plt.title('Scatter Plot: X vs Y')
plt.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--", label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
plt.legend()
plt.show()