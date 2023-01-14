#!/usr/bin/python3

# To correct the database file:

import time


def fix_colons(s: str, correct_num: int):
    """ fix number of colons in line

    Args:
        s (str): the string to correct
        correct_num (int): the number of colons it should have

    Raises:
        ValueError: it shold never receive a string with the correct number of colons

    Returns:
        str: the corrected line with the proper num of colons
    """
    ... but what about cases where we have too few colons in this line bc it's an overflow from last line?
    can't just add them in
    if correct_num < s.count(':'): return add_colons(s, correct_num)
    if correct_num > s.count(':'): return remove_extra_colons(s, correct_num)
    else: raise ValueError("given line has the correct number of colons, nothing to fix.")  # correct number of colons

def add_colons(s, num):
    """ add all the extra colons necessary to match the record to the usual number of fields

    Args:
        s (str): see fix_colons(s, correct_num)
        num (int): see fix_colons(s, correct_num)

    Raises:
        ValueError: should never be raised. Raised if function is called on string without colons to add

    Returns:
        str: see fix_colons(s, correct_num)
    """
    col = num - s.count(':')
    if col <= 0: raise ValueError("ERR: too MANY colons. Cannot add colons.")
    else: return s + col * ':'

# TODO@me: create a script to remove colons when there are too many. this seems like something I need to do manually for now until I figure out how to code it
def remove_extra_colons(s, num):
    """ remove all the extra colons necessary to match the record to the usual number of fields

    Args:
        s (str): see fix_colons(s, correct_num)
        num (int): see fix_colons(s, correct_num)

    Raises:
        ValueError: should never be raised. Raised if function is called on string without colons to add

    Returns:
        str: see fix_colons(s, correct_num)
    """
    col = num - s.count(':')
    if col >= 0: raise ValueError("ERR: too MANY colons. Cannot add colons.")
    else: raise BaseException("I'm too dumb to figure out how to remove these automatically")

# The countries and the numbers of colons in most records for each country (courtesy of find_db_errors.py)
countries_colons = {'Israel': 11, 'Russia': 13, 'Spain': 11, 'USA': 13, 'Italy': 13, 'South Africa': 13, 'UK': 11}
# Open errors file
for country in countries_colons:
    with open('errors/'+country+'_errors.txt', 'r') as errors_file:
        with open('data/'+country+'.txt.csv') as out:
# For each line in the country_errors file, split it into two usable parts, using format `line '+line_number+': '+line_text`
            errors_file_lines = errors_file.readlines()
            main_file_lines   = out.readlines()
            for line in errors_file_lines:
                colon_index = line.index(':')
                line_number, line_text = int(line[5:colon_index]), line[colon_index+2:]
                if line_number == 0: continue   # skip csv headers line
                print(str(line_number), main_file_lines[line_number] + line_text)
                time.sleep(.5)
                
# Then go to line_number in the main file, and update line_text to include the proper number of colons
                
            #out.writelines(errors)

# Israel: 11
# Russia: 13
# Spain: 11
# USA: 13
# Italy: 13
# South Africa: 13
# UK: 11
# [('Israel', 11), ('Russia', 13), ('Spain', 11), ('USA', 13) ('Italy', 13), ('South Africa', 13), ('UK', 11)]
# note: opening and closing these big files takes a LONG time