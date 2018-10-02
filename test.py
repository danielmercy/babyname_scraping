import re
from os import listdir, walk
import glob
from os.path import isfile, join
from database_talk_test import write_to_table

def parse_html_file(src):

  # create an empty list variables to hold reference to some data.
  yearList, rankList, maleList, femaleList, result, final_result = [], [], [], [], [], [None]*1001

  # open and extract ranks, male names and the female names
  with open(src, 'r') as file:

    # loop through each line in the file
    for line in file:

      year_pattern = re.compile('name="year"')
      pattern = re.compile('\<td>[A-Za-z0-9]') # compile the pattern to make the search run faster

      match = re.search(pattern, line) # match the pattern for each line

      if re.search(year_pattern, line):
        year = line.split('value=')[1].strip('>\n').split('"')[1]
        list.append(yearList, year)
        final_result[0] = year

      if match: # check if each lines match and if it matches, remove the unnecessary strings
        raw = line.split('<td>') # split each line into a list and remove '<td>'

        rank = raw[1].split('</td>')[0] # select the 2nd item in the list pointing to the rank and remove the closing '</td>' tag
        list.append(rankList, rank)

        male = raw[2].split('</td>')[0] # select the 3nd item in the list pointing to the rank and remove the closing '</td>' tag
        list.append(maleList, male)

        female = raw[3].split('</td>\n')[0] # select the last item in the list pointing to the rank adn remove the closing '</td>' tag
        list.append(femaleList, female)

        # print(raw)

    # Parse the data into a list of dicts
    for i in range(1000):
      final_result[i+1] = {
        'rank': rankList[i],
        'maleName': maleList[i],
        'femaleName': femaleList[i]
      }


  return final_result


def write_file():
    # Create a start and end year reference.
    start_year = 1990
    end_year = 2008

    # Create a while loop to iterate over the year and parse the year to the file name i.e baby(+ year).html
    with open('baby_names.txt', 'w') as file:
        while start_year <= end_year:

            # Reference the file in a variable "file_name"
            file_name = f'baby{start_year}.html'
            name_results = parse_html_file(file_name)


            file.write(f'\n{"-"*100}\n' f'YEAR: {name_results[0]}\n' f'From: baby{start_year}.html\n' f'{"-"*100}\n')
            file.write(f'\nRank{" "*(20 - len("rank") - 1)}'
                       f'Male Names{" "*(25 - len("Male Names") - 1)}'
                       f'Female Names{" "*(25 - len("Female Names") - 1)}\n')

            for i in range(1,1001):
                file.write(f'\n{name_results[i]["rank"]}{" "*(20 - len(name_results[i]["rank"]))}'
                           f'{name_results[i]["maleName"]}{" "*(25 - len(name_results[i]["maleName"]))}'
                           f'{name_results[i]["femaleName"]}{" "*(25 - len(name_results[i]["femaleName"]))}\n')

            start_year += 2
        print('Finished writing to file')

files = glob.glob('*.html')
for file in files:
    raw_data = parse_html_file(file)
    write_to_table(raw_data)

# print(parse_html_file('baby1990.html'))

# start_year = 1990
# end_year = 2008
#
# baby_names = {}
# while start_year <= end_year:
#   name_list = parse_html_file(f'baby{start_year}.html')
#   # print(f'{"-"*50}', f'\n YEAR: {name_list[0]}', f'\n From baby{start_year}.html\n{"-"*50}\n')
#   # print(f'Rank{" "*7}', f'Male Names{" "*5}', f'Female Names\n')
#   #
#   # for i in range(1,1001):
#   #   print(f'{name_list[i]["rank"]}{" "*10}', f'{name_list[i]["maleName"]}{" "*10}', f'{name_list[i]["femaleName"]}')
#   write_to_table(name_list)
#   start_year += 2
#




