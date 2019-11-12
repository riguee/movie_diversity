from requests_html import HTMLSession
import requests as req
import json
from bs4 import BeautifulSoup
import html
import os
import sys
import tmdbsimple as tmdb
session = HTMLSession()


tmdb.API_KEY = '044b74de638995f58e819e4736f5b29c'

# Need to use another API for better results or a combination of two APIs
def tmdbSearch(year, movie):
    url = "https://api.themoviedb.org/3/search/movie?api_key=c4d48123a2a6f5d1d47be09f93ecc8db&language=en-US&query={}&page=1&year={}".format(movie, str(year))
    # search = tmdb.Search()
    # response = search.movie(query=movie)
    response = req.get(url)
    if response.status_code == 200:
        resp = response.json()
        if resp["total_results"]>>0:
            return(True)
        else:
            return(False)
    else:
        return(False)
    # s = search.results[0]
    # print(s['title'] + " :")
    # movie = tmdb.Movies(s['id'])
    # response = movie.info()
    # for actor in movie.credits()['cast']:
    #     try :
    #         if (actor['order'] > 5):
    #             continue
    #         ethnicity = nndb_ethnicity_lookup(actor['name'])
    #         output_file.write('%s;%s;%s\r' % (actor['name'], actor['character'], ethnicity))
    #     except Exception:
    #         pass

def webscrapeMovies(country, year):
    movies = []
    print('\t\tChecking the movies for the year '+str(year))
    data = session.get('https://www.the-numbers.com/'+country+'/movies/year/'+str(year))
    soup = BeautifulSoup(data.content, 'html.parser', from_encoding="utf-8")
    test = soup.find_all('tr')
    minimum = min(len(test), 41)
    print('\t\tExtracting '+str(minimum)+' movie titles')
    i=1
    while i<minimum:
        arr = str(test[i]).split('#tab=summary')[1][2:].split('</a>')[0]
        movies.append(html.unescape(arr))
        print(html.unescape(arr))
        i +=1
    return(movies)


def get_movies(year, country):

    dirName = country
    os.mkdir(dirName)
    try:
        print("Directory " , dirName ,  " Created ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")

    movies = {}
    while year >1999 :
        if os.path.isfile('./'+country+'/'+str(year)+'.txt')==False:
            movies = webscrapeMovies(country, year)
            filename = country+'/'+str(year)+'.txt'
            with open(filename, "w", encoding='utf-8') as txt_file:
                for line in movies:
                    txt_file.write(str(line) + "\n")
        else:
            movies = open('./'+country+'/'+str(year)+'.txt')
            nb_lines = 0
            for line in movies:
                nb_lines += 1
            if nb_lines<40:
                answer = input("The number of movies saved for {} is less than 40.\nDo you want to proceed anyways? (y/n)".format(str(year)))
                if answer.lower() == 'n':
                    print("well that's sad")
                elif answer.lower() == 'y':
                    print("you're super cool")
                else:
                    print("can you read???")
            year-=1

    #
    #
    #     for year in movies:
    #         with open(filename, "w", encoding='utf-8') as txt_file:
    #             for line in movies[year]:
    #                 txt_file.write(str(line) + "\n")
    #     year-=1
    # print(movies)
    # return(movies)

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
            req_url = "http://www.omdbapi.com/?t="+movie+"&y="+str(year)+"&plot=full&apikey=50f2d223"
            response = req.get(req_url)
            if response.status_code == 200:
                resp = response.json()
                try :
                    actors = resp['Actors'].split(',')
                    all_actors_by_year[year] += actors
                except :
                    print("movie "+ movie+" wasn't found")
    print(str(movies_not_found)+" movies weren't found")
    return(all_actors_by_year)

def getmoviesfromthefuckingfiles(year, country):
    movies_not_found_tmdb = []
    movies_not_found_omdb = []
    while year > 1999:
        input_file = open('./' + country + '/'+ str(year) + '.txt', 'r', encoding='utf_8')
        for line in input_file:
            if 'Star Wars' in line:
                line = "Star Wars"
            print('\tSearching movie {}'.format(line.strip()))
            tmdb_result = tmdbSearch(year, line)
            omdb_result = searchMovie(year, line)
            if omdb_result == 'error':
                print('Not found in omdb')
                movies_not_found_omdb.append(line)
            if tmdb_result == False:
                print('Not found in tmdb')
                movies_not_found_tmdb.append(line)
        year-=1
    print(str(len(movies_not_found_tmdb))+" weren't found in tmdb")
    print(str(len(movies_not_found_omdb))+" weren't found in omdb")
    diff = list(set(movies_not_found_omdb) - set(movies_not_found_tmdb))
    print('they have '+str(len(diff))+' different films not found.')
