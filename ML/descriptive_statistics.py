import numpy as np 

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