# -*- coding: utf-8 -*-
"""
@author: MinhTok1oPC

Task: As a data analyst, you are task to predict whether or not the loaners (borrowers) can and will payback their
loan in full. This prediction based on the purpose of the loan, interest rate, Fico scores, debt-to-income ratio
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('D:\Py-Material\Loan+Analysis+Project\Loan Analysis Project')
print(os.getcwd())

loan_data = pd.read_excel('loandataset.xlsx')
customer_data = pd.read_csv('customer_data.csv', sep = ';')

# Merge data
complete_data = pd.merge(loan_data, customer_data, left_on = 'customerid', right_on = 'id')

# Check for missing data
complete_data.isnull().sum()
complete_data[['city', 'country']] = complete_data[['city', 'country']].fillna('N/A')
complete_data.isnull().sum()

# Check for duplicated data
complete_data.duplicated().sum()
#complete_data = complete_data.drop_duplicates()

# Currently, in purpose columns, there are lots of purpose has similar concept
def categorize_purpose(purpose):
    if purpose in ['creditcard', 'debt_consolidation']:
        return 'Financial'
    elif purpose in ['small_business', 'education']:
        return 'Educational/Business'
    else:
        return 'Other'

complete_data['purpose_category'] = complete_data['purpose'].apply(categorize_purpose)

# Based on dataset, any customers that likely can't pay off the loan, will have the combination of
# dpi ratio is > 20, delinq.2years is > 2 and revol.util > 60
# This kind of customers is consider high risk (can't pay off debt)

def asset_risk(row):
    if row['dti'] > 20 and row['delinq.2yrs'] > 2 and row['revol.util'] > 60:
        return 'High risk'
    else:
        return 'Low risk'
    
complete_data['Risk'] = complete_data.apply(asset_risk, axis = 1)

# Categorize FICO scores
def categorize_fico(fico_score):
    if fico_score >= 800 and fico_score <= 850:
        return 'Excellent'
    elif fico_score >= 740 and fico_score < 800:
        return 'Very Good'
    elif fico_score >= 670 and fico_score < 740:
        return 'Good'
    elif fico_score >= 580 and fico_score < 670:
        return 'Fair'
    else:
        return 'Bad'

complete_data['fico_category'] = complete_data['fico'].apply(categorize_fico)

# Identify customers have more than average inquiries and derogatory records
def identify_high_inq_derog(row):
    avg_inq = complete_data['inq.last.6mths'].mean()
    avg_derog = complete_data['pub.rec'].mean()
    
    if row['inq.last.6mths'] > avg_inq and row['pub.rec'] > avg_derog:
        return True
    else:
        return False
    
complete_data['High_Inquiries_and_Pub_Rec'] = complete_data.apply(identify_high_inq_derog, axis = 1)

complete_data.to_excel('Loans_final_analysis.xlsx', index = False)

# Data visualization
# Distribution of loans by purpose
sns.set_style('darkgrid')
plt.figure(figsize = (10, 6))
sns.countplot(x = 'purpose', data = complete_data, palette = 'dark')
plt.title('Loan purpose distribution')
plt.xlabel('Purpose of loans')
plt.ylabel('Numbers of loans')
plt.xticks(rotation = 45)

# DTI and incomes
plt.figure(figsize = (10, 6))
sns.scatterplot(x = 'log.annual.inc', y = 'dti', data = complete_data)
plt.title('Debt-To-Income and Annual Income ratio')

# Distribution of FICO scores
plt.figure(figsize = (10, 6))
sns.histplot(complete_data['fico'], bins = 30, kde = True)
plt.title('Distribution of Fico scores')

# Determine risk and interest rates
plt.figure(figsize = (10, 6))
sns.boxplot(x = 'Risk', y = 'int.rate', data = complete_data)
plt.title('Interest Rate and Risk')

