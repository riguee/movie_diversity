import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
#imports the necessary libraries

list_of_countries = ['Germany', 'United States', 'United Kingdom', 'China', 'India']
#list of the countries we are studying, will be used later
data = pd.read_csv('final_file.csv', sep = ';')
data = data.drop('Unnamed: 0', axis = 1)
#creates and cleans dataframe

for thing in list_of_countries:
#loops through the countries
    temp_study_df = data[data['country'] == thing]
    study_df = temp_study_df.drop('country', axis = 1)
    study_df= study_df.set_index('year')
    #creates dataframe that we study for the country selected, with years as index

    dicty = {'black' : [], 'white' : [], 'multiracial' : [], 'asian' : [], 'indian' : [], 'middle eastern' : [], 'hispanic' : [], 'other' : []}
    #dictionary that will keep the percentages of each ethnicities for each year

    for column in study_df:
        for year in study_df.index:
            #loops through the dataframe
            dicty[column].append(study_df[column].loc[year] / study_df.loc[year].sum())
            #calcultes percentage of the slice concerned and adds it to the dictionary

    percentages = pd.DataFrame.from_dict(dicty)
    percentages = percentages.join(data['year'])
    percentages = percentages.set_index(percentages['year'])
    #creates the final dataframe of the percentages of the country

    y = (percentages[['black','white','multiracial','asian', 'middle eastern', 'indian', 'hispanic', 'other']].transpose())
    #creates nwe dataframe from the previous one and turns it
    y.to_csv(thing + '.csv')
    #saves the dataframe as a csv under the name of the country


    #the next lines plot the data on a stackplot graph and set the axis, labels and legend
    x = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000]
    labels = ['black','white','multiracial','asian', 'middle eastern', 'indian', 'hispanic', 'other']
    fig, ax = plt.subplots()
    ax.stackplot(x, y, labels=labels)
    ax.legend(loc='upper left')
    plt.show()
    plt.savefig('./' + thing + '_stackplot.jpg')
    plt.close()
