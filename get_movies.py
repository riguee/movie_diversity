from requests_html import HTMLSession
import requests as req
import json
from bs4 import BeautifulSoup
import html
import os
import re
import pandas as pd
import urllib.request
import urllib
import matplotlib.pyplot as plt
import sys
session = HTMLSession()


def get_movies(year, country):

    dirName = country
    try:
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")

    movies = {}
    while year >1999 :
        print('\t\tChecking the movies for the year '+str(year))
        movies[year]=[]
        data = session.get('https://www.the-numbers.com/'+country+'/movies/year/'+str(year))
        soup = BeautifulSoup(data.content, 'html.parser', from_encoding="utf-8")
        test = soup.find_all('tr')
        minimum = min(len(test), 41)
        print('\t\tExtracting '+str(minimum)+' movie titles')
        i=1
        while i<minimum:
            arr = str(test[i]).split('#tab=summary')[1][2:].split('</a>')[0]
            movies[year].append(html.unescape(arr))
            print(html.unescape(arr))
            i +=1
        filename = country+'/'+str(year)+'.txt'

        for year in movies:
            with open(filename, "w", encoding='utf-8') as txt_file:
                for line in movies[year]:
                    txt_file.write(str(line) + "\n")
        year-=1
    print(movies)
    return(movies)

def searchMovie(year, movie):
    req_url = "http://www.omdbapi.com/?t="+movie+"&y="+str(year)+"&plot=full&apikey=50f2d223"
    response = req.get(req_url)
    if response.status_code == 200:
        resp = response.json()
        try :
            actors = resp['Actors'].split(',')
            return(actors)
        except :
            return('error')

def get_cast(movies):
    movies_not_found=0

    all_actors_by_year={}
    for year in movies.keys():
        all_actors_by_year[year] = []
        for movie in movies[year]:
            print(movie)
            info = searchMovie(year, movie)
            if info!='error':
                all_actors_by_year[year] += info
            else:
                info=searchMovie(year-1, movie)
                if info!='error':
                    all_actors_by_year[year] += info
                else:
                    print('movie '+movie+" wasnt found")
                    movies_not_found+=1
            # req_url = "http://www.omdbapi.com/?t="+movie+"&y="+str(year)+"&plot=full&apikey=50f2d223"
            # response = req.get(req_url)
            # if response.status_code == 200:
            #     resp = response.json()
            #     try :
            #         actors = resp['Actors'].split(',')
            #         all_actors_by_year[year] += actors
            #     except :
            #         print("movie "+ movie+" wasn't found")
    print(str(movies_not_found)+" weren't found")
    return(all_actors_by_year)

def test_ethnicity_lookup():
    all_ethnicities_and_actors = []
    for year in all_actors_by_year.keys():
        for actor in all_actors_by_year[year]:
            print(actor)
            try:
                data = session.get('https://ethnicelebs.com/'+actor.replace(' ', '-'))
                soup = BeautifulSoup(data.content, 'html.parser', from_encoding="utf-8")
                test_value = (soup.findAll(text=re.compile("Ethnicity:")))
                ethnicity = test_value[0].split(':')[1].strip()
            except:
                ethnicity = ''
            print('ethnicity is '+ethnicity)
            all_ethnicities_and_actors.append({'year':year, 'actor':actor,'ethnicity': ethnicity})
    print(all_ethnicities_and_actors)

def nndb_ethnicity_lookup(actor_name):
    search_url = 'http://search.nndb.com/search/nndb.cgi?nndb=1&omenu=unspecified&query=%s'
    people_url_prefix = 'http://www.nndb.com/people/'
    print('-- Searching ethnicity on NNDB for %s' % actor_name)
    tmp = urllib.request.urlopen(search_url % urllib.parse.quote_plus(actor_name))
    result = tmp.read()
    soup = BeautifulSoup(result,features="html.parser")
    all_results = soup.find_all('a')
    potential_results = []
    for link in all_results:
        if (link.get('href').startswith(people_url_prefix) and link.contents[0] == actor_name.strip()):
            potential_results.append(link.get('href'))
    if len(potential_results) > 1:
        print("-- -- Multiple results for %s. Aborting." % actor_name)
        return
    if len(potential_results) <= 0:
        print("-- -- No result for %s. Aborting." % actor_name)
        return
    tmp = urllib.request.urlopen(potential_results[0])
    result = tmp.read()
    soup = BeautifulSoup(result,features="html.parser")
    ethnicity_occ = soup.findAll(text=re.compile("Ethnicity"))
    if (len(ethnicity_occ) > 0):
        return ethnicity_occ[0].next_element.strip()
    return 'Unknown'

def add_ethnicities(actors_by_year):
    actors_to_search = []
    all_actor_ethnicities = []
    existing_actors =  pd.read_csv('all_actors_2.csv', encoding='utf_8')
    actors_to_find = 0
    actors_found = 0
    # actors_to_search = pd.DataFrame(columns=['actor'])
    # all_actor_ethnicities = pd.DataFrame(columns=['actor', 'ethnicity'])
    all_actors = []
    for year in actors_by_year.keys():
        all_actors+=actors_by_year[year]
    all_actors = list(dict.fromkeys(all_actors))
    for actor in all_actors:
        try:
            actor = actor.strip()
            ethn = existing_actors['ethnicity'].loc[existing_actors['actor'] == actor].iloc[0]
            print('actor '+ actor.strip() +' in the database already')
        except:
        # if actor.strip() in existing_actors['actor']:
        #     print(actor +' exists in the database already')
            all_actor_ethnicities.append([actor.strip(), ""])
            # try:
            #     ethnicity = nndb_ethnicity_lookup(actor)
            #     if ethnicity == 'Unknown' or ethnicity == '' or ethnicity == None:
            #         print(actor+" wasn't found in the nndb database")
            #         actors_to_search.append(actor.strip())
            #         actors_to_find+=1
            #     else:
            #         all_actor_ethnicities.append([actor.strip(), ethnicity])
            #         actors_found+=1
            # except:
            #     print('An error happened while looking up the ethnicity of '+actor)
    print(all_actor_ethnicities)
    print(actors_to_search)
    all_actor_ethnicities = pd.DataFrame(all_actor_ethnicities)
    print(all_actor_ethnicities)
    # all_actor_ethnicities.to_csv("test_actors.csv")
    actors_to_search =  pd.DataFrame(actors_to_search)
    with open('all_actors.csv', 'a', encoding="utf-8") as f:
        all_actor_ethnicities.to_csv(f, header=False)
    with open('unknown_actors.csv', 'a', encoding="utf-8") as f:
        actors_to_search.to_csv(f, header=False)
#len_df['category_sub_1'].loc[len_df['sku'] == prod_ref].iloc[0]

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
                print(existing_actors['ethnicity'].loc[existing_actors['actor'] == actor].iloc[0])
                ethn = existing_actors['ethnicity'].loc[existing_actors['actor'] == actor].iloc[0]
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
        #plt.show('./' + country + '/' + fig_name)
        plt.savefig('./' + country + '/' + str(year) + '.png')
        plt.close()

year=2019
country='United-Kingdom'


if sys.argv[1] == "fetch":
    movies = get_movies(year, country)
    casts = get_cast(movies)
    add_ethnicities(casts)

else:
    movies = get_movies(year, country)
    casts = get_cast(movies)
    stats = getstats(casts)
    printpiechart(stats, country)

# key = os.getenv('OMDB_API_KEY', 'that doesnt work')
