from requests_html import HTMLSession
import requests as req
import json
from bs4 import BeautifulSoup
import html
import os
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
    while year >2018 :
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
