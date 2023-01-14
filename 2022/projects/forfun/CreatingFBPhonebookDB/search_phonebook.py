#!/usr/bin/env python3

import pathlib
import csv
from pprint import pprint
from typing import Iterable

def input_query():
    inp = valid_inp = False
    while not inp:
        inp = input("Do you have a [name] or a [number] to search with? ")
        query = ['type', 'value']
        while inp and valid_inp == False:
            if inp == 'name':
                name = input("What's the name? ")
                query[0] = 'name'
                #try:
                if ' ' in name:
                    fname, lname = name.title().split(' ')
                    query[1] = (fname, lname)
                    valid_inp = True
                # elif ':' in name:
                    # Just so I can deal with test cases that I pull directly from the data
                    # fname, lname = name.title().split(':')
                    # query[1] = (fname, lname)
                else:
                # except ValueError as e:
                    # inp = False
                    print("Please enter a first and last name.")
                    # raise ValueError("Please enter a first and last name.")
            elif inp == 'number':
                phone = input("What's the number? ")
                query[0] = 'phone_number'
                try:
                    int(phone)
                    # if len(phone) == 10:
                    #     phone = '1' + phone
                except ValueError as e:
                    print('Please format your phone number query as a number.')
                query[1] = phone
                valid_inp = True
            else:
                inp = False
                print('Try again. Please enter either "name" or "number".')
                # fname, lname = query
                # search for the fname, lname in the database
                # print("Searching for " + name + " in " + country_name + ". Please wait.")
                # don't forget to account for multiple cases (i.e. if there are multiple people with this name)
    return query

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

def search_db(country: Iterable, query: Iterable) -> None:
    country_name = country[0]
    country_file = country[1]

    fieldnames = ('phone', 'fb_id', 'fname', 'lname', 'gender', 'current_city', 'hometown', 'relationship_status', 'work', 'graduation_year', 'email', 'dob')

    # still need to test if this works
    with open(country_file) as f:
        reader = csv.DictReader(f, fieldnames, delimiter=':', quoting=csv.QUOTE_NONE)
        count = 0
        for row in reader:
            if query[0] == 'phone_number' and query[1] in row['phone']: yield row
            elif query[0] == 'name':
                fname, lname = query[1]
                try:
                    if fname in row['fname'] and lname in row['lname'] or fname == '*' and lname in row['lname']: yield row
                except TypeError as e:
                    print(e)

def main():
    #query = input_query()
    #print(query)
    #test1 = ['name', ('Dedy', 'Tetro')]
    #test2 = ['phone_number', '972502000008']
    
    country = get_desired_country()
    # pdb.set_trace()
    detailed_output = input("[B]asic output, or \n[D]etailed output?\n ").lower() == 'd'
    for row in search_db(country, input_query()):
        print(row['fname'] + ' ' + row['lname'])
        print(row['phone'])
        if detailed_output: pprint(row)

if __name__ == '__main__':
    main()