# import working functions
import get_movies_and_cast as g_m
import get_gender as gender
import stats_and_viz as stats
import get_actor_ethnicity as ethn

#import sqlite for database handling
import sqlite3

year=2019
country='United-States'

g_m.getmoviesfromthefuckingfiles(year, country)
# movies = g_m.get_movies(year, country)
# casts = g_m.get_cast(movies)
# gender.getInfoOnActors(casts)
# if sys.argv[1] == "fetch":
#     movies = get_movies(year, country)
#     casts = get_cast(movies)
#     add_ethnicities(casts)
#
# else:
#     movies = get_movies(year, country)
#     casts = get_cast(movies)
#     stats = getstats(casts)
#     printpiechart(stats, country)

# key = os.getenv('OMDB_API_KEY', 'that doesnt work')
