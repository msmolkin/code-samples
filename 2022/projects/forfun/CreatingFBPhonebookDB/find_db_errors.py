#!/usr/bin/python3

# To automate the preparation for correcting the database file:

# Figure out the most common number of colons per line
# from collections import defaultdict


# def calc_mode_of_colons(arr):
#     hashmap = defaultdict(int)
#     for line in arr:
#         num_colons = line.count(':')
#         hashmap[num_colons] += 1
#     return max(hashmap, key=hashmap.get)

# Create errors file
countries_colons = {'Israel': 11, 'Russia': 13, 'Spain': 11, 'USA': 13, 'Italy': 13, 'South Africa': 13, 'UK': 11}
for country in countries_colons:
    with open('data/'+country+'.txt.csv') as f:
        with open('errors/'+country+'_errors.txt', 'w') as out: # Potential issue if code is reused: doesn't raise FileExistsError, overwrites file instead
            errors = []
            # all_lines = f.readlines()
            # usual_number_of_colons = calc_mode_of_colons(all_lines)
            #for line in enumerate(all_lines):
            for line in enumerate(f.readlines()):
                if line[1].count(':') != countries_colons[country]: errors.append('line '+str(line[0])+': '+line[1])
            out.writelines(errors)

# Israel: 11
# Russia: 13
# Spain: 11
# USA: 13
# Italy: 13
# South Africa: 13
# UK: 11
# [('Israel', 11), ('Russia', 13), ('Spain', 11), ('USA', 13) ('Italy', 13), ('South Africa', 13), ('UK', 11)]
# note: opening and closing these big files takes a LONG time