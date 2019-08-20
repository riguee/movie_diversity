import tmdbsimple as tmdb
import sys
import urllib.request
import urllib
import re
import pandas as pd
from bs4 import BeautifulSoup
#imports the necessary libraries

country = sys.argv[1]
year = int(sys.argv[2])
rangepup = int(sys.argv[3])
#reads elements from the cmd line

a = 0

#loops through all the years selected in the cmd line
for a in range(rangepup) :
    input_file = open('./' + country + '/'+ str(year) + '.txt', 'r')
    #opens the input file of the country selected and the year of the loops
    #the input file is a .txt file with one movie per line
    output_file = open('./' + country + '/' + str(year) + 'attempt_input.csv', 'w')
    #defines the path and name of the output file
    tmdb.API_KEY = '044b74de638995f58e819e4736f5b29c'
    #API that is used
    search_url = 'http://search.nndb.com/search/nndb.cgi?nndb=1&omenu=unspecified&query=%s'
    people_url_prefix = 'http://www.nndb.com/people/'
    #urls necessary for the webscraping



    #definition of the function that looks for the ethnicity on the NNDb website
    def nndb_ethnicity_lookup(actor_name):
        print('-- Searching ethnicity on NNDB for %s' % actor_name)
        tmp = urllib.request.urlopen(search_url % urllib.parse.quote_plus(actor_name))
        result = tmp.read()
        print(result)
        soup = BeautifulSoup(result,features="html.parser")
        all_results = soup.find_all('a')
        potential_results = []
        for link in all_results:
            if (link.get('href').startswith(people_url_prefix) and link.contents[0] == actor_name):
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

    #code that loops through the lines of the input file
    #looks for the movie in the API and for the actors in the info provided by the API
    output_file.write('Actor;Character;Ethnicity\r')
    for line in input_file:
        search = tmdb.Search()
        response = search.movie(query=line)
        if (len(search.results) <= 0):
            continue
        s = search.results[0]
        print(s['title'] + " :")
        movie = tmdb.Movies(s['id'])
        response = movie.info()
        for actor in movie.credits()['cast']:
            try :
                if (actor['order'] > 5):
                    continue
                ethnicity = nndb_ethnicity_lookup(actor['name'])
                output_file.write('%s;%s;%s\r' % (actor['name'], actor['character'], ethnicity))
            except Exception:
                pass




    print("\n           Year " + str(year) + " finished!! :D")

    a += 1
    year -= 1
