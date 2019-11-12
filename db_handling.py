import sqlite3
import pandas as pd

conn = sqlite3.connect('movie.db')
c = conn.cursor()

def ask_what_to_do(details = 'start'):
    if details == 'error':
        further = input('Sorry something went wrong. What table do you want to see more of? (Enter none to exit)')
    elif details == 'more':
        further = input('Do you want to see more from another table? (Enter none to exit)')
    else:
        further = input('What table do you want to see more of? (Enter none to exit)')
    if further.lower() == 'none':
        print("Goodbye :)")
        return None
    else:
        try:
            df = pd.read_sql_query("SELECT * from {}".format(further.lower()), conn)
            print("{} are:".format(further.lower()))
            print(df.head())
            ask_what_to_do('more')
        except:
            ask_what_to_do('error')

def do_stuff():
    question = input("Do you want to see the tables? (y/n)")
    if question.lower() == 'y':
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(c.fetchall())
        value = ask_what_to_do()
        return None
    else :
        action = input("What do you want to do then?")
        print("Sorry {} machine broken :/".format(action))

if __name__ == "__main__":
    do_stuff()
    conn.close()



# c.execute("CREATE TABLE actors (id int AUTO_INCREMENT, name VARCHAR(100) NOT NULL, date_of_birth DATE NOT NULL, date_of_death DATE DEFAULT NULL, gender VARCHAR(10), ethnicity VARCHAR(30) DEFAULT 'unknown', nationality VARCHAR(60), PRIMARY KEY (id))")
# c.execute("CREATE TABLE movies (id int AUTO_INCREMENT, name VARCHAR(100) NOT NULL, release_date DATE NOT NULL, imdb_rating FLOAT, rotten_tomatoes_rating FLOAT, google_rating FLOAT, PRIMARY KEY (id))")
# c.execute("CREATE TABLE countries (id int AUTO_INCREMENT, name VARCHAR(100) NOT NULL, population_in_mill INT, continent VARCHAR(20), PRIMARY KEY (id))")

# # Create table
# c.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')
#
# # Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
#*
# # Save (commit) the changes
# conn.commit()
#
# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# conn.close()
