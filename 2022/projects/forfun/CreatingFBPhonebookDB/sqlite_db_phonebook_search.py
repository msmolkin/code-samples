#! /usr/bin/python3
# Do the same search, but using an sqlite database this time
import sqlite3
import pathlib

db = pathlib.Path("data/all_countries.db")
try:
    conn = sqlite3.connect(db)
except Exception as e:
    print(e)
cur = conn.cursor()
# cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
# <sqlite3.Cursor object at 0x7faf20cb9810>
# >>> print(cur.fetchall())
# [('Israel.txt',), ('Russia.txt',), ('Spain.txt',)]
# >>> data = cur.execute("SELECT * FROM 'Israel.txt'")
# for column in data.description: print(column[0])
# phone
# fb_id
# fname
# lname
# gender
# current_city
# hometown
# relationship_status
# work
# graduation_year
# email
# dob
fname, lname = input("What's the name? ").title().split(' ')

def get_desired_country():
    data = pathlib.Path() / 'data'
    if not data.exists() and data.is_dir(): print("Please run this from the project's main directory.")
    data_files = [src for src in data.iterdir() if src.is_file() and not ("France" in src.name or "Germany" in src.name)]

    menu = {}
    i = 1

    for country_file in data_files:
        country_name = country_file.name[:country_file.name.index('.')] 
        menu[i] = country_name, country_file
        i += 1

    for key in sorted(menu.keys()):
        print(str(key) + ': ' + menu[key][0])
    # print(menu)
    country = input("What country is the person in? ") # France is experimental, as it has too many delimiters (and uses a different delimiter)

    if not country: country = 1 # USA by default
    else: country = int(country)
    # TODO: now that I have the country, I take the corresponding database as a CSV
    if country not in menu: raise(IndexError("Invalid country key"))
    print(menu[country][1])

    country_name = menu[country][0]
    country_file = menu[country][1]
    return menu[country]

country = get_desired_country()
country_file = country[0] + '.txt'
# data = cur.execute("SELECT * FROM 'Israel.txt' WHERE fname='Zozo' AND lname='Mozo'")
# data.arraysize      data.description    data.executescript( data.fetchone(      data.rowcount      
# data.close(         data.execute(       data.fetchall(      data.lastrowid      data.setinputsizes(
# data.connection(    data.executemany(   data.fetchmany(     data.row_factory    data.setoutputsize(
# >>> print(data.fetchall())
# [(972501231234, 1505054940, 'Zozo', 'Mozo', 'male', 'Saint Petersburg, Russia', 'Sëdnyrd, Komi, Russia', None, None, None, None, None)]
# >>> data = cur.execute("SELECT phone FROM 'Israel.txt' WHERE fname='Zozo' AND lname='Mozo'")
people = cur.execute("SELECT fname, lname, phone FROM '" + country_file + "' WHERE fname='" + fname + "' AND lname='" + lname + "'")
people = people.fetchall()
print(str(len(people)) + " result" + ('' if len(people) == 1 else 's') + " found")
for row in people:
    print(row)
# [(972501231234,)]
# >>> data = cur.execute("SELECT fname, lname,gender FROM 'Israel.txt' WHERE phone=972502001041")
# >>> print(data.fetchall())
# [('Asaf', 'Alaluf', 'male')]
