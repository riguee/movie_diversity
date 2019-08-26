from requests_html import HTMLSession
from bs4 import BeautifulSoup
import html
session = HTMLSession()

data = session.get('https://www.the-numbers.com/United-States/movies/year/2019')
soup = BeautifulSoup(data.content, 'html.parser', from_encoding="utf-8")
test = soup.find_all('tr')
min = min(len(test), 21)
movies = []
i=1
while i<min:
    arr = str(test[i]).split('#tab=summary')[1][2:].split('</a>')[0]
    movies.append(html.unescape(arr))
    i +=1
print(movies)
with open("output.txt", "w", encoding='utf-8') as txt_file:
    for line in movies:
        txt_file.write(line + "\n") # works with any number of elements in a line

api_key = "c4d48123a2a6f5d1d47be09f93ecc8db"
api_read_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNGQ0ODEyM2EyYTZmNWQxZDQ3YmUwOWY5M2VjYzhkYiIsInN1YiI6IjVkNDk3MGFmMDI4ZjE0MDAxMTAxZmM1NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sodqYMB0rEAic55k5u6HnmCGG2S55rf12RfGC6ntAaI"
url = "http://www.omdbapi.com/?t=" + '' + "&y=2019&plot=full&apikey=PlzBanMe"
