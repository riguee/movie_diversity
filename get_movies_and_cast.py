from requests_html import HTMLSession
import requests as req
import json
from bs4 import BeautifulSoup
import html
import os
import sys
import sqlite3
import tmdbsimple as tmdb
session = HTMLSession()


tmdb.API_KEY = '044b74de638995f58e819e4736f5b29c'
conn = sqlite3.connect('movie.db')
c = conn.cursor()

def doer():
    genres = pd.read_sql_query("SELECT * from genre", conn, index_col="id")
    actors = pd.read_sql_query("SELECT * from actors", conn, index_col="id")
    countries = pd.read_sql_query("SELECT * FROM countries", conn, index_col="id")
    movies = pd.read_sql_query("SELECT * FROM movies;", conn, index_col='id')


# Need to use another API for better results or a combination of two APIs
def tmdbSearch(year, movie, movies, genres, actors, countries):
    url = "https://api.themoviedb.org/3/search/movie?api_key=c4d48123a2a6f5d1d47be09f93ecc8db&language=en-US&query={}&page=1&year={}".format(movie, str(year))
    response = req.get(url)
    if response.status_code == 200:
        resp = response.json()
        if resp["total_results"]>>0:
            id = resp["results"][0]["id"]
            url = f"https://api.themoviedb.org/3/movie/{id}?api_key=c4d48123a2a6f5d1d47be09f93ecc8db&language=en-US"
            response = req.get(url)
            response = response.json()
            movie_data = {'name':movie,
                    'release_date': response["release_date"],
                    'imdb_rating': ,
                    'rotten_tomatoes_rating': ,
                    'google_rating': ,
                    'tmdb_id': response['id'],
                    'imdb_id': respons['imdb_id'],
                    'omdb_id': None,
                    'budget': response['budget'],
                    'language': response['original_language'],
                    'revenue': response['revenue'],
                    'runtime': response['runtime'],
                    'collection': response['belongs_to_collection']['name']

            }
            url_cast = f"https://api.themoviedb.org/3/movie/{id}/credits?api_key=c4d48123a2a6f5d1d47be09f93ecc8db"
            response_cast = req.get(url_cast)
            if response_cast.status_code == 200:
                cast = {"actor": [], "movie": [], "character": []}
                resp = response_cast.json()
                num = min(10; len(resp["cast"]))
                for i in range(num):
                    cast["actor"].append(resp["cast"][i]["name"])
                    cast["movie"].append()

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
    #try:
    #    os.mkdir(dirName)
    #    print("Directory " , dirName ,  " Created ")
    #except FileExistsError:
    #    print("Directory " , dirName ,  " already exists")

    movies = {}
    while year >1999 :
        if os.path.isfile('./'+country+'/'+str(year)+'.txt')==False:
            movies[year] = webscrapeMovies(country, year)
            #filename = country+'/'+str(year)+'.txt'
            #with open(filename, "w", encoding='utf-8') as txt_file:
            #    for line in movies:
            #        txt_file.write(str(line) + "\n")
        else:
            movies = open('./'+country+'/'+str(year)+'.txt')
            nb_lines = 0
            movies[year]=[]
            for line in movies:
                movies[year.append(line)]
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
    return(movies)
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

def search_movies(movies):
    movies_not_found_tmdb = []
    movies_not_found_omdb = []
    for year in movies.keys():
        for line in movies[year]:
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
