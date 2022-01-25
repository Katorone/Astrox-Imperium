#!/usr/bin/python3

# More information, as well as the (non)licence can be found at: https://github.com/Katorone/Astrox-Imperium

# This script exports 2 files to a csv:
#  - MOD/items/items_database.txt -> itemdb.csv
#  - MOD/items/specs_database.txt -> docdb.csv

# TODO:
# It will also do some sanity checking, which should be useful for mod & modpack creators:
#  - Every ID across items and documents needs to be unique
#  - Warns when an item doesn't have a doc for crafting
#  - Check if the .png for an item/doc exists
#  - Orphaned documents

# Example for windows: c:\path\to\Astrox\MOD\items\
source = '/home/kato/.steam/steam/steamapps/common/Astrox Imperium/Astrox Imperium_Data/MOD/items/'
itemfile = 'items_database.txt'
docfile = 'specs_database.txt'

# Delimiter to use in the exported csv
delimiter = ';'

# Unique sorting key of items (items_database.txt)
# You probably won't need to change this, unless Momo changes this in an update.
itemIdentifier = '1 ITEM ID'

# Unique sorting key of documents (specs_database.txt)
# You probably won't need to change this, unless Momo changes this in an update.
docIdentifier = '1 DOC ID'


### End of configuration ###
###   Code starts here   ###
import glob
import os

# reads data from path
def readFile(path):
  fh = open(path, 'r', encoding='utf8', newline='\n')
  data = fh.readlines()
  fh.close()
  return data

# Writes a list of data to path
def writeFile(path, dataList):
  fh = open(path, 'w', encoding='utf8', newline='')
  for line in dataList:
    fh.write(line+'\r\n')
  fh.close()

# Takes a string and returns a list
def cleanLine(line, strip, delim):
  line = line.strip()
  if line == "": return line
  if line[-1] == delim: line = line[0:-1]
  return [x.strip(strip) for x in line.split(delim)]

# Finds the header, which is the last commented line at the start of a file
def getHeader(data):
  for idx, line in enumerate(data):
    if line[:2] != '//':
      return data[idx-1][2:]

# Gets the index of the identifier from the header[list]
def getIdentifierIndex(header, identifier):
  if identifier not in header: return -1
  return header.index(identifier)

def parseFile(file, identifier, ):
  lines = readFile(os.path.join(source, file))
  header = cleanLine(getHeader(lines), '\t ', ';')
  identifierIndex = getIdentifierIndex(header, identifier)
  if identifierIndex == -1:
    print("ERROR: couldn't locate '"+identifier+"' in '"+source+"'")
    quit()
  # Parse the items, stored as item[id]
  data = {}
  data[delimiter+'header'+delimiter] = header  # store the header for future use
  for line in lines:
    if line[:2] == '//': continue              # Ignore comments
    line = cleanLine(line, '\t ', ';')
    if line == "": continue                    # Ignore empty lines
    data[line[identifierIndex]] = line    # TODO: check if the ID is unique for this dictionary before setting it
  return data

def composeCsv(data, target):
  lines = []
  for item in data:         # data is a dictionary-type, which is guarantueed to be ordered by insertion.
    joiner = '"'+delimiter+'"'
    lines.append('"'+joiner.join(data[item])+'"')
  writeFile(target, lines)

itemData = parseFile(itemfile, itemIdentifier)
composeCsv(itemData, 'items_database.csv')
docData = parseFile(docfile, docIdentifier)
composeCsv(docData, 'specs_database.csv')

