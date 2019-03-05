import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#imports necessary libraries

intervals = pd.read_csv('limits.csv', sep = ';')
percent = pd.read_csv('stats.csv', sep = ';')
#creates dataframes for the intervals (calculated separately) and the official statistics
#sep by ; because French excel :-(

percent = percent.replace(',', '.', regex = True)
for x in percent.index:
    for y in [ 'Germany', 'United Kingdom', 'United States', 'China', 'India']:
        percent[y].loc[x] = float(percent[y].loc[x])
#because of French setup of excel, the data needs to be cleaned
#and transformed into numerical values


intervals = intervals.set_index('value')
intervals = intervals.transpose()
intervals = intervals.replace(',', '.', regex=True)
for x in intervals.index:
    for y in columns:
        intervals[y].loc[x] = float(intervals[y].loc[x])
#cleans the second dataframe in the same way as the previous one

min_values = ['asian lower limit', 'black lower limit', 'hispanic lower limit', 'indian lower limit',
             'middle eastern lower limit', 'multiracial lower limit', 'other lower limit', 'white lower limit']
max_values = ['asian upper limit', 'black upper limit', 'hispanic upper limit', 'indian upper limit',
             'middle eastern upper limit', 'multiracial upper limit', 'other upper limit', 'white upper limit']
countries = ['Germany', 'United Kingdom', 'United States', 'China', 'India']
keys = ['white', 'black', 'hispanic', 'multiracial', 'asian', 'indian', 'middle eastern', 'other']
keys = keys.sort()
#creates lists that will be used later

min = intervals.loc[min_values]
max = intervals.loc[max_values]
#creates new dataframes from the previous lists



my_range = range(1, len(percent.index)+1)
#creates a range for the visualisations

for country in countries:
    min_list = list(min[country])
    max_list = list(max[country])
    #creates lists for the upper and lower limits of the confidence intervals of the country

    #plots the graph for eah country
    plt.plot(percent[country], my_range, 'ro')
    #plots a circle for the offical statistic for each ethnicity
    plt.hlines(y = my_range, xmin=min[country], xmax=max[country], color='skyblue')
    #drawws horizontal lines representing the interval
    plt.yticks(my_range, percent['ethnicities'])
    #defines the y axis as non-numerical
    plt.title(country)
    plt.savefig( country + 'intervals3.png')
    plt.ylabel('ethnicities')
    #defines the labels
    plt.ylim(0.5,8.5)
    #selects the size of the y axis
    plt.show()
    plt.close()
