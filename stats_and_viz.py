import pandas as pd
import matplotlib.pyplot as plt

def getstats(actors_by_year):
    all_ethnicities_by_year = {}
    existing_actors =  pd.read_csv('all_actors_2.csv', encoding='utf_8')
    existing_actors = existing_actors[['actor','ethnicity']]
    print(existing_actors.head())
    actors_to_search = []
    for year in actors_by_year.keys():
        print('\t\tLooking up actors for the year '+str(year))
        all_ethnicities_by_year[year]={}
        for actor in actors_by_year[year]:
            actor = actor.strip()
            print('\tLooking for '+actor)
            try:
                ethn = existing_actors['ethnicity'].loc[existing_actors['actor'] == actor].iloc[0]
                print(ethn)
                if ethn in all_ethnicities_by_year[year].keys():
                    all_ethnicities_by_year[year][ethn]+=1
                else:
                    all_ethnicities_by_year[year][ethn]=1
            except:
                print("it didn't work for "+actor)
                actors_to_search.append(actor)
                if 'other' in all_ethnicities_by_year[year].keys():
                    all_ethnicities_by_year[year]['other']+=1
                else :
                    all_ethnicities_by_year[year]['other']=1
    actors_to_search =  pd.DataFrame(actors_to_search)
    with open('unknown_actors.csv', 'a', encoding="utf-8") as f:
        actors_to_search.to_csv(f, header=False, index=False)
    print(all_ethnicities_by_year)
    return(all_ethnicities_by_year)

def printpiechart(dict, country):
    for year in dict.keys():
        year_dict = dict[year]
        fig = plt.pie(x = [year_dict[i] for i in year_dict.keys()], labels= year_dict.keys(), shadow=False)
        plt.axis('equal')
        plt.legend(loc='lower left')
        plt.title(country + str(year))
        plt.savefig('./' + country + '/' + str(year) + '.png')
        plt.close()
