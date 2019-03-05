import pandas as pd
import matplotlib.pyplot as plt
import pylab
import sys

country = sys.argv[1]  #look into a country's folder
input_file = int(sys.argv[2])  #most recent your to start from
rangepup = int(sys.argv[3])  #looks through the number of files that's input


list = ("white", "black", "hispanic", "multiracial",
        "asian", "other", "middle eastern", "indian", "year")


column_names = ['Actor', 'Ethnicity'] #columns we're interested in, Actor and Ethnicity (initial df also includes character name)
final_unknown = pd.DataFrame(columns = column_names) #final df that gives the unknown actors in all the files the program runs through
counter = 0
veryvery_final_data = pd.DataFrame(columns = list)

for counter in range(rangepup) :

    dataset = pd.read_csv('actors_database.csv', sep=';', encoding='latin-1') #df of the manually inpit actors to be improved/filled in
    datapath = "./" + country + "/" + str(input_file) + "attempt_input.csv" #datapath for the concerned file
    df = pd.read_csv(datapath, sep=';', encoding='latin-1', header='infer') #reads the csv as a df (seperatoin as ; because French computer ftw)
    data = df[['Actor', 'Ethnicity']] #columns considered



            #this loops aims to match the previously unmatched actors
            #with actors' ethnicities manually added to the database
            #separates the df into two dadtaframes:
            #one that contains only unmatched actors and ethnicities
            #the other that contains all the others

    datatemp = data.loc[df['Ethnicity']!='None']
    loopdata = data.loc[data['Ethnicity']=='None']
    a = 0 #counter that loops through the unmatched actors in the input df
    b = 0 #counter that loops through the actors in the manually produced database
    for a in loopdata.index :
        for b in dataset.index :
            if loopdata['Actor'].loc[a] == dataset['Actor'].loc[b] :
                    #if the actor in the input df is also found in the database
                loopdata['Ethnicity'].loc[a] =  dataset['Ethnicity'].loc[b]
                    #replace the 'None' ethnicity with the ethnicity in the database
            b += 1
        a += 1



    data = pd.concat([datatemp, loopdata], ignore_index=True)
        #joins the two new dataframes together
    still_unknown = data.loc[data['Ethnicity'] == 'None']
        #creates a new df for actors still unmatched to be looked up and added into the database
    still_unknown.drop_duplicates(subset='Actor', keep='first', inplace=True)
        #removes names taht appear twice
    still_unknown.to_csv(country + '/' + str(input_file) + 'still_unknown.csv', header=True)
        #exports this df to a csv file


    final_unknown = final_unknown.append(still_unknown)
        #also creates a general file that will output all unknown actors
        #of all the files ran through the loop in one single df


    x = 0  #counter that runs through all actors of the newly created df
            #dictionnary that will count the number of appearance of
            #actors of each ethnicity

    dict = {
            "white" : 0,
            "black" : 0,
            "hispanic" : 0,
            "multiracial" : 0,
            "asian" : 0,
            "other" : 0,
            "middle eastern" : 0,
            "indian" : 0,
            "year" : input_file
        }

    data = data.replace(' ', '', regex=True).astype('str')
            #deletes spaces as the database df is manually input
            #and might have so added spaces by mistake
    #import pdb; pdb.set_trace()
    for x in data.index :
        if data['Ethnicity'].loc[x] == 'White' :
            dict["white"] += 1
        elif data['Ethnicity'].loc[x] == 'Black' :
            dict["black"] += 1
        elif data['Ethnicity'].loc[x] == 'Hispanic' :
            dict["hispanic"] += 1
        elif data['Ethnicity'].loc[x] == 'Multiracial' :
            dict["multiracial"] += 1
        elif data['Ethnicity'].loc[x] == 'Asian' :
            dict["asian"] += 1
        elif data['Ethnicity'].loc[x] == 'MiddleEastern' :
            dict["middle eastern"] += 1
        elif data['Ethnicity'].loc[x] == 'Asian/Indian' :
            dict['indian'] += 1
        else :
            dict["other"] += 1
        x += 1
                #loops through th actors and increments one to the ethnicity
                #that correspond
                #increments category 'other' if the ethnicity is not part of the categories

    keys = ['white', 'black', 'hispanic', 'multiracial', 'asian', 'indian', 'middle eastern', 'other']
    dict2 = {x:dict[x] for x in keys}
    final_data = pd.DataFrame.from_dict(dict2, orient = 'index') #creates df from final dict
    final_data.columns = ['Number of Characters'] #names the column; the category is the index
    final_data.to_csv ("./" + country + "/" + str(input_file) + "output.csv", index = True, header=True, sep =';')
    print(final_data) 
    very_final_data = pd.DataFrame(dict, index=[0])
    veryvery_final_data = veryvery_final_data.append(very_final_data)


            #this is just a pie chart for easier understanding of the data,
            #but not final visualisation
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red', 'blue', 'green', 'purple']
    fig = plt.pie(x = final_data, labels=final_data.index, colors=colors,
            autopct='%1.1f%%', shadow=False)
    plt.axis('equal')
    plt.legend(loc='lower left')
    plt.title(country + str(input_file))
    #plt.show('./' + country + '/' + fig_name)
    plt.savefig('./' + country + '/' + str(input_file) + '.png')
    plt.close()



    input_file -= 1
    counter +=1

final_unknown.drop_duplicates(subset='Actor', keep='first', inplace=True)
final_unknown.to_csv(country + '/final_unknown.csv', header=True, encoding = 'charmap')
very_final_data.to_csv(country + './very_final_data' + country + '.csv', header=True)
veryvery_final_data.to_csv(country + './very_very_final_data' + country + '.csv', header=True)
        #creates the final csv from all the unmatched actors,
        #removing names that appear twice
