#!/usr/bin/python3

# This script imports ship data from a csv-file to the Astrox MOD/ships directory.
# It will rewrite the <STATS> section as follows:
#  - First pass: Insert the keys and values from the csv in the order defined by "keys'.
#  - Second pass: Delete all duplicate keys below the inserted ones
# Any key that isn't in the csv will be safe and end up at the bottom of the <STATS>-section
# All other sections will be kept as they were.
#
# Any directory can be used as a target for the import, but this directory needs to have a copy of the original files.

# Path to the csv
# For windows, use: C:\\\path\\\to\\\shipdata.csv
source = "/home/user/path/to/Astrox/shipdata.csv"
# Path to the Astrox Imperium ship-files
target = "/home/user/.local/share/Steam/steamapps/common/Astrox Imperium/Astrox Imperium_Data/MOD/ships/"

# Delimiter used in the csv
delimiter = '";"'

# Import settings from exportShipdata.py?
# If False, you need to manually edit the 'keys' variable
#   I suggest to keep this to True, so both exportShipdata and importShipdata have consistent behavior.
#   However, the manual setting is useful for testing only a few changes from a bigger rework. Since
#   this script will only overwrite key;value pairs of keys that are in the 'keys'-list
copyKeys = True
keys = []


### End of configuration ###
###   Code starts here   ###
import glob
import os
shipdata = {}
exportdata = {}
validKeys = []
if copyKeys:
  from exportShipdata import keys

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
def cleanLine(line):
  line = line.strip()
  if line[-1] == delimiter: line = line[0:-1]
  return [x.strip('"') for x in line.split(delimiter)]

# rewrites the data in ship files
def processShipFiles():
  for filename in shipdata.keys():
    targetFile = os.path.join(target, filename)
    tempFile = targetFile+".tmp"
    data = readFile(targetFile)
    newdata = list()
    modify = False
    if not os.path.isfile(targetFile):
      print("WARNING: no such file '"+filename+"' in '"+target+"', ignoring record.")
      continue
    # Go over each line of the original ship text file
    for line in data:
      line = line.strip()
      if line == "": continue           #  Ignore empty lines
      elif line[:7] == '<STATS>':       #  <STATS> marks the start of the editing block
        newdata.append(line)
        modify = True
        for key in validKeys:           #   Loop through the configured keys and add them after <STATS> in order.
          if key[:2] == "//":
            newdata.append(key)
          else:
            newdata.append(key+";"+shipdata[filename][key])
        continue
      elif line[:6] == '<ITEM>':        #  <ITEM> marks the end of the editing block, every following line is copied over.
        modify = False
      if line[:2] == '//' and modify:   #  Don't copy over comments in the edited block
        continue
      if modify:                        #  If we're currently in the editing block:
        fileKey = line.split(';')[0]
        if fileKey in validKeys:        #   check if the key of this line is in validkeys
          continue
        else:
          newdata.append(line)          #    Copy the line if it doesn't have a configured key in 'keys'
      else:
        newdata.append(line)            #   Copy all lines when we're not in the editing block
    writeFile(tempFile, newdata)        # Write a temp file
    os.replace(tempFile, targetFile)    # move the temp file over the original txt
  print("Finished importing the csv to Astrox Imperium shipdata")


# Checks if all keys in 'keys' are in the csv
def validateKeys(csvKeys):
  failure = False
  # Check if configured keys are also present in the csv
  for key in keys:
    if key[:2] != '//' and key not in csvKeys:
      failure=True
      print("The key '"+key+"' was configured but wasn't found in the csv.")
    else:
      validKeys.append(key)
  if failure:
    print("WARNING: One or more configured keys didn't match the csv. The script will continue but keep the original value(s) in the ship file.")
  # Check if keys from the csv are configured keys
  failure = False
  for key in csvKeys:
    if key not in keys:
      failure=True
      print("The key '"+key+"' was found in the .csv but wasn't configured for export.")
  if failure:
    print("WARNING: One or more keys from the csv weren't configured for export. The script will continue but keep the original value(s) in the ship file.")

# Create the data structure based on shipdata.csv
def createDatastructure():
  data = readFile(source)       # Read the csv file to memory
  csvKeys = cleanLine(data[0])  # Fetch the headers
  # Check the index of 'SHIP_filename'
  filenameIndex = -1
  if 'SHIP_filename' in csvKeys:
    filenameIndex = csvKeys.index('SHIP_filename')
  else:
    print("Error: Couldn't find the field 'SHIP_filename' in "+source)
    print("It is mandatory to have this field, this script can't find the original txt file otherwise.")
    print("Exiting")
    quit()
  # Map the data to the header keys to create 'key: value' pairs.
  for line in data[1:]:
    line = cleanLine(line)
    filename = line[filenameIndex]+".txt"
    shipdata[filename] = {}
    # Loop through the header
    for idx, key in enumerate(csvKeys):
      # Fix 'SHIP_specials_raw'
      if key == 'SHIP_specials_raw':
        line[idx] = ",".join(line[idx].split('\r'))
        line[idx] = "#".join(line[idx].split(': '))
      shipdata[filename][key] = line[idx]
  validateKeys(csvKeys)
  processShipFiles()

createDatastructure()

