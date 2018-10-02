#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import timeit
import os
from glob import glob

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def parse_html_file(src):

  # create an empty list variables to hold reference to some data.
  yearList, rankList, maleList, femaleList = [], [], [], []

  # fill the list with 1001 None items as a placeholder.
  final_result = [None]*1001

  try:
    # open and extract ranks, male names and the female names
    with open(src, 'r') as file:

      # loop through each line in the file
      for line in file:

        # Compile RegEx pattern for getting the year from the html file
        year_pattern = re.compile('name="year"')

        # Compile the pattern to make the search run faster
        pattern = re.compile('<td>[A-Za-z0-9]')

        # match the pattern for each line
        match = re.search(pattern, line)

        # Check if there is a year string in the line and then extract it.
        if re.search(year_pattern, line):
          year = line.split('value=')[1].strip('>\n').split('"')[1]
          # --- list.append(yearList, year) this line is not necessary.

          # Append the year string into the first position of the list
          final_result[0] = year

        # check if each lines match and if it matches, strip off the unnecessary strings
        if match:

          # split each line into a list and remove '<td>'
          raw = line.split('<td>')

          # select the 2nd item in the list pointing to the rank and remove the closing '</td>' tag
          # and append the data to the list respectively.
          rank = raw[1].split('</td>')[0]
          list.append(rankList, rank)

          # select the 3nd item in the list pointing to the male names and remove the closing '</td>' tag
          # and append the data to the list respectively.
          male = raw[2].split('</td>')[0]
          list.append(maleList, male)

          # select the last item in the list pointing to the female names and remove the closing '</td>\n' string
          # and append the data to the list respectively.
          female = raw[3].split('</td>\n')[0]
          list.append(femaleList, female)

      # Parse the data into a list of dicts
      for i in range(1000):
        # Insert dicts data starting from index position 1
        final_result[i+1] = {
          'rank': rankList[i],
          'maleName': maleList[i],
          'femaleName': femaleList[i]
        }
  except FileNotFoundError:
    print(f'File with name {src} doesn\'t exist in the working directory')
    sys.exit(0)


  return final_result

def write_data_to_file(data):

  if data:
    start_time = timeit.default_timer()
    finished = False
    sourceFile = ''
    with open('baby_names.txt', 'a') as file:
      sourceFile = file

      # This line writes the year and file data source name to the file.
      label = file.write(f'\n{"-"*100}\n' f'YEAR: {data[0]}\n' f'From: baby{data[0]}.html\n' f'{"-"*100}\n')

      if label:
        print(f"Start writing parsed data from baby{data[0]}.html to file....")
      # This line writes the labels of the data to the file.
      file.write(f'\nRank{" "*(20 - len("rank") - 1)}'
               f'Male Names{" "*(25 - len("Male Names") - 1)}'
               f'Female Names{" "*(25 - len("Female Names") - 1)}\n')

      # This line creates a loop from 1 - 1001 since the dicts data start index at 1
      label_3 = ''
      for i in range(1,1001):
        # This line individaually access the dict data key value pairs from the data list
        # and then parse each data into the file.
        file.write(f'\n{data[i]["rank"]}{" "*(20 - len(data[i]["rank"]))}'
                            f'{data[i]["maleName"]}{" "*(25 - len(data[i]["maleName"]))}'
                            f'{data[i]["femaleName"]}{" "*(25 - len(data[i]["femaleName"]))}\n')

    stop_time = timeit.default_timer()

    if sourceFile.closed:
      finished = True
      finish_time = stop_time - start_time
      print(f'Finished writing to file in {finish_time}s\n')

    return finished
  return False



def extract_file(files):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  if os.path.exists('baby_names.txt'):
    print("Removing old file...")
    os.remove('baby_names.txt')
    print("done.\n")

  if files:
    # This line will parse the html data with the custom parse_html_file method and reference it inside a data variable
    for file in files:
      data = parse_html_file(file)
      # This line passes the data to the write_data_to_file  method to parse the data into the new text file
      write_data_to_file(data)


  # if data:

  # else:
  return True


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print( '''
      usage: [--summaryfile] option or file
      
      --all, -a             Parse all html file in the directory.
      
      Files in working directory
      
      - baby1990.html
      - baby1992.html
      - baby1994.html
      - baby1996.html
      - baby1998.html
      - baby2000.html
      - baby2002.html
      - baby2004.html
      - baby2006.html
      - baby2008.html
      
      example
      
      1. python babynames.py --summaryfile baby1990.html baby2006.html
      2. python babynames.py --summaryfile --all or -a
      
      ''' )
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  print(args)
  if '--all' in args:
    # This line with get all files with .html extension into a list
    filenamess = glob('*.html')
    extract_file(filenamess)
  elif '-a' in args:
    # This line with get all files with .html extension into a list
    filenamess = glob('*.html')
    extract_file(filenamess)
  else:
    extract_file(args)

if __name__ == '__main__':
  main()
