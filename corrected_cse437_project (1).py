# -*- coding: utf-8 -*-
"""Corrected_CSE437_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/185ezAQDseqNS-oW3gj1V3p1BH3pwqTdo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/CSE437 Project/Living close to an university on academic performance.csv')

df.head()

columns_to_drop = ['Timestamp','Email Address','Provide Your Name']
main = df.copy()
main.drop(columns_to_drop, axis=1, inplace=True)

main.head()

df.describe()

main .info()

main.shape

main.isnull().sum()

total_duplicates = main.duplicated().sum()
print(f"Total number of duplicate rows: {total_duplicates}")

unique_counts = main.nunique()

categorical_features = unique_counts[unique_counts <= 10].index
quantitative_features = unique_counts[unique_counts > 10].index

nc = len(categorical_features)
qc = len(quantitative_features)

print(f"Categorical Features: {nc}")
print(categorical_features)

print(f"\nQuantitative Features: {qc}")
print(quantitative_features)

for x in range(len(categorical_features)):
    unique1 = main[categorical_features[x]].nunique()
    print(f"Number of unique values in {categorical_features[x]} column: {unique1}")
    unique2= main[categorical_features[x]].unique()
    print(f"Unique values in {categorical_features[x]} : {unique2}")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")

print(main.columns.tolist())

main1 = main.copy()

main1['2. How far do you live from the university?'] = main['2. How far do you live from the university?'].map({
    'More than 10 km': 1,
    '1–5 km': 2,
    '6–10 km': 3,
    'Less than 1 km': 4
})

main1['3. How do you commute to the university?'] = main['3. How do you commute to the university?'].map({
    'Public Transport': 1,
    'Walking': 2,
    'Personal Vehicle': 3,
    'Others': 4
})

main1['4. What is your academic CGPA range?'] = main['4. What is your academic CGPA range?'].map({
    '3.7>': 1,
    '3.3 - 3.7': 2,
    '<3.0': 3,
    '3.0 - 3.3': 4
})

main1['5. How many hours per week do you dedicate to studying (outside class hours)?'] = main['5. How many hours per week do you dedicate to studying (outside class hours)?'].map({
    'Less than 5': 1,
    'More than 15': 2,
    '11 -15': 3,
    '5 - 10': 4
})

main1['6. How often do you study on campus (e.g., in the library, study rooms)? '] = main['6. How often do you study on campus (e.g., in the library, study rooms)? '].map({
    'Never': 1,
    'Few times a Week': 2,
    'Once a Week': 3,
    'Daily': 4
})

main1['7. What type of accommodation do you live in?'] = main['7. What type of accommodation do you live in?'].map({
    'Family home': 1,
    'Off-campus shared apartment': 2,
    'Off-campus private residence': 3
})

main1['8. How does your living distance affect your punctuality for classes?'] = main['8. How does your living distance affect your punctuality for classes?'].map({
    'Frequently late': 1,
    'Always on time': 2,
    'Occasionally late': 3,
    'Often on time': 4,
})

main1['9. Is the long distance disturbing your sleeping routine?'] = main['9. Is the long distance disturbing your sleeping routine?'].map({
    'Yes': 1,
    'Sometimes': 2,
    'No': 3
})

main1['10. State your academic performance'] = main['10. State your academic performance'].map({
    'Good': 1,
    'Moderate': 2,
    'Bad': 3
})

main1.head()

plt.figure(figsize=(20, 8))
sns.heatmap(main1.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

main1 = main.copy()

# One-hot encode each column with categorical data
main1 = pd.get_dummies(main1, columns=[
    '2. How far do you live from the university?',
    '3. How do you commute to the university?',
    '4. What is your academic CGPA range?',
    '5. How many hours per week do you dedicate to studying (outside class hours)?',
    '6. How often do you study on campus (e.g., in the library, study rooms)? ',
    '7. What type of accommodation do you live in?',
    '8. How does your living distance affect your punctuality for classes?',
    '9. Is the long distance disturbing your sleeping routine?',
    '10. State your academic performance'
], drop_first=True).astype(int)

main1.head()

nan_counts = main1.isna().sum()
print(nan_counts)

main1.info()

# Skewness and Kurtosis
skewness = main1.skew()
kurtosis = main1.kurtosis()

print("Skewness of the dataset:")
print(skewness)

print("\nKurtosis of the dataset:")
print(kurtosis)

"""# **# Null Hypothesis:** Living close to the university has no impact on academic performance.

# **# Alternative Hypothesis:** Living close to the university has a significant impact on academic performance.

# T- Test
"""

import numpy as np
import scipy.stats as stats



academic_performance_column = "10. State your academic performance_Good"
assert academic_performance_column in main1.columns, "Academic performance column not found!"

#  "close" and "far" distance columns are being identified
close_columns = [col for col in main1.columns if "2. How far do you live from the university?_" in col and
                 ("Less than 1 km" in col or "1–5 km" in col)]
far_columns = [col for col in main1.columns if "2. How far do you live from the university?_" in col and
               ("6–10 km" in col or "More than 10 km" in col)]

# Combining one-hot values for "close" and "far" distances
close_distance = main1[close_columns].sum(axis=1)  # Students living close
far_distance = main1[far_columns].sum(axis=1)  # Students living far

# Ensuring no Nan values
academic_performance = main1[academic_performance_column].dropna()

# Filtering the academic performance data for close and far distances
close_performance = academic_performance[close_distance > 0]
far_performance = academic_performance[far_distance > 0]


# Performing an independent t-test
t_stat, p_value = stats.ttest_ind(close_performance, far_performance)


print(f"t-statistic: {t_stat}")
print(f"p-value: {p_value}")

# Determining significance
alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant relationship between living distance and academic performance.")
else:
    print("Fail to reject the null hypothesis: There is no significant relationship between living distance and academic performance.")

"""# Chi- Square Test"""

import pandas as pd
import scipy.stats as stats


# Defining the columns
living_distance_columns = [col for col in main1.columns if "2. How far do you live from the university?_" in col]
academic_performance_columns = [col for col in main1.columns if "10. State your academic performance_" in col]


# Ensuring the columns are found
assert len(living_distance_columns) > 0, "Living distance columns not found!"
assert len(academic_performance_columns) > 0, "Academic performance columns not found!"

# Combining one-hot encoded columns to create categorical data
living_distance = main1[living_distance_columns].idxmax(axis=1)  # Gettitng the column with the max value
academic_performance = main1[academic_performance_columns].idxmax(axis=1)  # Getting the column with the max value


# Cross-tabulation to prepare a contingency table
contingency_table = pd.crosstab(living_distance, academic_performance)

# Perform the Chi-Square Test
chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)


print("Chi-Square Test Results:")
print(f"Chi-Square Statistic: {chi2_stat}")
print(f"Degrees of Freedom: {dof}")
print(f"P-Value: {p_value}")

# Interpretation
alpha = 0.05  # Significance level
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant relationship between living distance and academic performance.")
else:
    print("Fail to reject the null hypothesis: There is no significant relationship between living distance and academic performance.")

"""# Anova Test"""

import pandas as pd
import scipy.stats as stats


# Defining the columns
living_distance_columns = [col for col in main1.columns if "2. How far do you live from the university?_" in col]
academic_performance_column = "10. State your academic performance_Good"
# Ensuring columns exist
assert len(living_distance_columns) > 0, "Living distance columns not found!"
assert academic_performance_column in main1.columns, "Academic performance column not found!"

# Creating the groups for ANOVA based on living distance
anova_groups = []
for col in living_distance_columns:
    group = main1.loc[main1[col] == 1, academic_performance_column]
    anova_groups.append(group)


# Performing the ANOVA test
f_stat, p_value = stats.f_oneway(*anova_groups)

# Printing the results
print("ANOVA Test Results:")
print(f"F-Statistic: {f_stat}")
print(f"P-Value: {p_value}")

# Interpretation
alpha = 0.05  # Significance level
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant difference in academic performance between living distance groups.")
else:
    print("Fail to reject the null hypothesis: There is no significant difference in academic performance between living distance groups.")