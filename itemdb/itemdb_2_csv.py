#!/usr/bin/python3

# More information, as well as the (non)licence can be found at: https://github.com/Katorone/Astrox-Imperium

# This script exports 2 files to a csv:
#  - MOD/items/items_database.txt -> itemdb.csv
#  - MOD/items/specs_database.txt -> docdb.csv
# It will also do some sanity checking, which should be useful for mod & modpack creators:
#  - Each file can only contain unique IDs (the exported csv will only contain the first match)
#  - Every ID between items and documents needs to be unique (the script will warn)
#  - Warns when an item doesn't have a doc for crafting
#  - Check if the .png for an item/doc exists
#  - Orphaned documents

# Example for windows: c:\path\to\Astrox\MOD\items\
source = '/home/user/.steam/steam/steamapps/common/Astrox Imperium/Astrox Imperium_Data/MOD/items/'
itemfile = 'items_database.txt'
docfile = 'specs_database.txt'

# Delimiter to use in the exported csv
delimiter = ';'

# List of item IDs that don't have a crafting document
ignoreUncraftable = [
  "1",    "2",    "3",    "4",    "5",    "6",    "7",    "8",    "9",    "10",   # Resources - Raw
  "11",   "20",   "21",   "22",   "23",   "24",   "25",   "26",   "27",   "28",   # Resources - Loot
  "29",   "100",  "101",  "103",  "114",  "102",  "104",  "109",  "118",  "113",  # Materials
  "105",  "106",  "107",  "108",  "110" , "2000", "111",  "115",  "112",          # Materials
  "121",  "117",  "116",  "124",  "119",  "123",  "120",  "122",                  # Materials
  "150",  "151",  "152",  "153",  "164",  "155",  "156",  "157",  "158",  "168",  # Components - Class A
  "160",  "161",  "162",  "163",  "154",  "159",  "165",  "166",  "167",  "169",  # Components - Class B
  "170",  "200",  "201",  "202",  "203",  "204",  "205",  "206",  "207",  "208",  # Components - Class C
  "209",  "210",  "211",  "212",  "213",  "214",  "215",  "216",  "217",  "218",  # Components - Class D
  "219",  "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", # Components - Class E
  "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", # Components - Class F
  "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", # Components - Class G
  "2030", "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038", "2039", # Components - Class H
  "2040", "2041", "2042", "2043", "2044", "2045", "2046", "2047", "2048", "2049", # Components - Class I
  "2050", "2051", "2052", "2053", "2054", "2055", "2056", "2057", "2058", "2059", # Components - Class J
  "2080", "2081", "2082", "400",  "401",  "402",                                  # Components - Class M
  "302",  "300",  "301",  "351",  "353",  "350",  "352",  "330",  "332",  "331",  # Trade Goods
  "333",  "341",  "342",  "340",  "343",  "303",  "304",  "305",  "322",  "324",  # Trade Goods
  "320",  "321",  "323",  "325",  "311",  "310",  "312",  "313",  "403",  "404",  # Trade Goods
  "405",  "406",  "407",  "408",                                                  # Trade Goods
  "600",  "601",  "602",  "603",  "604",  "605",  "606",  "607",  "608",  "609",  # Life Support - Food
  "620",  "621",  "622",  "623",  "624",  "625",  "626",  "627",  "628",  "629",  # Life Support - Water
  "640",  "641",  "642",  "643",  "644",  "645",  "646",  "647",  "648",  "649",  # Life Support - Thermal
  "660",  "661",  "662",  "663",  "664",  "665",  "666",  "667",  "668",  "669",  # Life Support - Waste
  "690",  "670",  "671",  "691",  "672",  "673",  "692",  "674",  "675",  "693",  # Consumables
  "676",  "677",  "700",  "678",  "679",  "701",  "680",  "681",  "710",  "711",  # Consumables
  "712",  "702",  "703",  "735",  "736",  "737",  "738",                          # Consumables
]

## These settings tell the script which title it needs to look for when examining data.
header = {}
# You probably won't need to change this, unless Momo changes this in an update.
# Unique sorting key of items (items_database.txt)
header['itemId'] = '1 ITEM ID'
# Unique sorting key of documents (specs_database.txt)
header['docId'] = '1 DOC ID'
# Name of the item's image
header['itemImage'] = '6 icon image'
# Name of the document's image
header['docImage'] = '6 doc image'
# The item ID that a doc would craft:
header['docItemId'] = '9 CRAFTS ID'



### End of configuration ###
###   Code starts here   ###
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
  print("✔️ Finished writing: "+path)

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
    print("🛑 couldn't locate '"+identifier+"' in '"+source+"'")
    quit()
  # Parse the items, stored as item[id]
  data = {}
  data[delimiter+'header'+delimiter] = header  # store the header for future use
  doubles = {}                                 # stores the ID that are duplicates
  for line in lines:
    if line[:2] == '//': continue              # Ignore comments
    line = cleanLine(line, '\t ', ';')
    if line == "": continue                    # Ignore empty lines
    id = line[identifierIndex]
    if id in data:                             # Duplicate checking
      doubles[id] = 2 if id not in doubles else doubles[id] + 1
    else:                                      # No duplicate, add the line.
      data[id] = line
  if len(doubles) > 0:
    for id in doubles:
      print("❌ The unique identifier '"+id+"' matched "+str(doubles[id])+" different lines.")
    print("❌ Duplicates were found.  The script will only use the first match per duplicate.")
    print("------------------------------")
  else:
    print("✔️ There were no duplicate keys in: "+file)
  return data

def composeCsv(data, target):
  lines = []
  for item in data:         # data is a dictionary-type, which is guarantueed to be ordered by insertion.
    joiner = '"'+delimiter+'"'
    lines.append('"'+joiner.join(data[item])+'"')
  writeFile(target, lines)

# Check itemData and docData for duplicate IDs
def findDuplicateEntries(fn1, data1, fn2, data2):
  duplicates = {}
  for id in data1.keys() & data2.keys():
    if id == delimiter+'header'+delimiter: continue
    duplicates[id] = 2 if id not in duplicates else duplicates[id] + 1
  if len(duplicates) > 0:
    for id in duplicates:
      print("❌ The unique identifier '"+id+"' matched "+str(duplicates[id])+" times in "+fn1+" and "+fn2+".")
    print("❌ Duplicate IDs were found across "+fn1+" and "+fn2+".")
    print("------------------------------")
  else:
    print("✔️ There were no duplicate keys across: "+fn1+" and "+fn2+".")

# Checks that the column header[itemId] has en entry in the column header[docItemId]
def sanityCheck(items, itemHeader, docs, docsHeader):
  itemHeaderIdentifier = getIdentifierIndex(items[delimiter+'header'+delimiter], itemHeader)
  if itemHeaderIdentifier == -1:
    print("🛑 couldn't locate '"+itemHeader+"' in findMissing(), unable to continue sanity check.")
    return
  docsHeaderIdentifier = getIdentifierIndex(docs[delimiter+'header'+delimiter], docsHeader)
  if docsHeaderIdentifier == -1:
    print("🛑 couldn't locate '"+docsHeader+"' in findMissing(), unable to continue sanity check.")
    return
  itemIDs = []
  for i in items:
    if i == delimiter+'header'+delimiter: continue
    itemIDs.append(items[i][itemHeaderIdentifier])
  docIDs = []
  for i in docs:
    if i == delimiter+'header'+delimiter: continue
    docIDs.append(docs[i][docsHeaderIdentifier])
  # Let's go over all items in docIDs and make sure they're unique
  seen = set()
  duplicates = [x for x in docIDs if x in seen or seen.add(x)]
  if len(duplicates) > 0:
    print("❌ The following item ID(s) have more than one crafting document: "+', '.join(duplicates))
    print("------------------------------")
  else:
    print("✔️ All documents point to a unique item.")
  # We have 2 lists of IDs, find the IDs from itemIDS that are missing in docIDs
  docSet = set(docIDs)
  ignoreSet = set(ignoreUncraftable)
  missingDocs = [x for x in itemIDs if x not in docSet and x not in ignoreSet]
  if len(missingDocs) > 0:
    print("❌ The following item ID(s) do not have a crafting document: "+', '.join(missingDocs))
    print("   Items that are uncraftable by design can be added to the 'ignoreUncraftable'-list in itemdb_2_csv.py")
    print("------------------------------")
  else:
    print("✔️ All items have a crafting document attached (with "+str(len(ignoreUncraftable))+" ignored uncraftables).")
  # For the orphaned check, we find docIDs that are missing in itemIDs
  itemSet = set(itemIDs)
  missingItems = [x for x in docIDs if x not in itemSet]
  if len(missingItems) > 0:
    print("❌ The following item ID(s) have a crafting document, but the item does not exist: "+', '.join(missingItems))
    print("------------------------------")
  else:
    print("✔️ All documents have an existing item attached.")

def checkFileLinks(data, header):
  headerIdentifier = getIdentifierIndex(data[delimiter+'header'+delimiter], header)
  if headerIdentifier == -1:
    print("🛑 couldn't locate '"+header+"' in checkFileLinks(), unable to continue sanity check.")
    return
  haserror = False
  for i in data:
    if i == delimiter+'header'+delimiter: continue
    file = data[i][headerIdentifier]
    if not os.path.isfile(os.path.join(source, file)):
      haserror = True
      print("❌ Item id '"+i+"' links to '"+file+"', which doesn't exists.")
  if not haserror:
    print("✔️ All files in column '"+header+"' exist.")

if __name__ == "__main__":
  itemData = parseFile(itemfile, header["itemId"])
  composeCsv(itemData, 'items_database.csv')
  docData = parseFile(docfile, header["docId"])
  composeCsv(docData, 'specs_database.csv')
  # Check itemData and docData for duplicate IDs
  findDuplicateEntries(itemfile, itemData, docfile, docData)
  # Sanity checks:
  # - Check if all items have a document
  # - Check if all documents point to an existing item
  # - Check if all documents point to a unique item
  sanityCheck(itemData, header["itemId"], docData, header["docItemId"])
  # Check if the .png for an item/doc exists
  checkFileLinks(itemData, header["itemImage"])
  checkFileLinks(docData, header["docImage"])
  print("")
  input("All done. Press enter to exit.")
