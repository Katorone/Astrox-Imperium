#!/usr/bin/python3

# More information, as well as the (non)licence can be found at: https://github.com/Katorone/Astrox-Imperium
# If you run into any issues, feel free to open an issue on Github, or write me (katorone#2957) on the Astrox discord.

### Please see shipdata_settings.py for configuration options.

# This script imports ship data from a csv-file to the Astrox MOD/ships directory.
# It will rewrite the <STATS> section as follows:
#  - First pass: Insert the keys and values from the csv in the order defined by "keys'.
#  - Second pass: Delete all duplicate keys below the inserted ones
# Any key that isn't in the csv will be safe and end up at the bottom of the <STATS>-section
# All other sections will be kept as they were.

############################
###   Code starts here   ###
############################
def exitScript(force=False):
  if force or mod.pauseOnExit:
    print("")
    input("Press enter to exit.")
  quit()

import os, glob, sys, importlib
config = 'shipdata_settings.py'
if len(sys.argv) > 1:
  if sys.argv[1][:8] == '--config' and len(sys.argv) == 3:
    config = sys.argv[2]
  else:
    print('USAGE: shipdata_2_csv.py --config /path/to/config.py')
    exitScript(True)
if os.path.isfile(config):
  print('✔️ Loading settings from: '+config)
else:
  print('🛑 The config file doesn\'t exist: '+config)
  exitScript(True)
mod = importlib.import_module(config[:-3])

# rewrites the data in ship files
def processShipFiles(shipdata, validKeys):
  target = mod.shipdata['target']
  for filename in shipdata.keys():
    targetFile = os.path.join(target, filename+".txt")
    data = mod.readFile(targetFile)
    newdata = list()
    modify = False
    if not os.path.isfile(targetFile):
      print("❌ WARNING: no such file '"+filename+"' in '"+target+"', ignoring record.")
      continue
    # Go over each line of the original ship text file
    for line in data:
      line = line.strip()
      if line == "": continue             #  Ignore empty lines
      elif line[:7] == '<STATS>':         #  <STATS> marks the start of the editing block
        newdata.append(line)
        modify = True
        for key in validKeys:             #   Loop through the configured keys and add them after <STATS> in order.
          if key[:2] == "//":
            newdata.append(key)
          else:
            newdata.append(key+";"+shipdata[filename][key])
        continue
      elif line[:6] == '<ITEM>':          #  <ITEM> marks the end of the editing block, every following line is copied over.
        newdata.append('//; --------------------------------- SHIP PARTS -----------------------------------')
        newdata.append('//; --------------- ITEM,type,catID,pfID,xp,yp,zp,xr,yr,zr--------------------------')
        modify = False
      # EDIT BLOCK
      if modify:                          #  If we're currently in the editing block:
        if line[:2] == '//':               #   Don't copy over comments in the edited block
          continue
        fileKey = line.split(';')[0]
        if fileKey in shipdata[filename]: #   check if the key of this line is in validkeys
          continue
        elif fileKey in deleteKeys:       #   If the key needs to be deleted, don't copy it over.
          continue
        else:
          newdata.append(line)            #    Copy the line if it doesn't have a configured key in 'keys'
      else:
        newdata.append(line)              #   Copy all lines when we're not in the editing block
    mod.writeFile(targetFile, newdata) # Write!
  print("✔️ Finished writing the csv to the Astrox Imperium shipfiles")


# Checks if all keys in 'keys' are in the csv
def validateKeys(csvKeys):
  failure = False
  # Check if configured keys are also present in the csv
  for key in mod.keys['to_shipfile']:
    if key[:2] != '//' and key not in csvKeys:
      failure=True
      print("❌ The key '"+key+"' was configured for export but wasn't found in the .csv.")
  if failure:
    print("❌ WARNING: One or more configured keys wasn't found in the .csv. The script will continue and keep the original value(s) in the ship file.")
    print("------------------------------")
  # Check if keys from the csv are configured keys
  failure = False
  for key in csvKeys:
    if key not in mod.keys['to_shipfile']:
      failure=True
      print("❌ The key '"+key+"' was found in the .csv but wasn't configured for export.")
  if failure:
    print("WARNING: One or more keys from the .csv weren't configured for export. The script will continue but keep the original value(s) in the ship file.")
    print("------------------------------")
  # Check if deleted keys are in the csv or keys['delete_from_shipfiles']
  failure = False
  for key in mod.keys['delete_from_shipfiles']:
    if key in csvKeys and key in mod.keys['to_shipfile']:
      failure=True
      print("❌ The key '"+key+"' was set to be deleted but was found in the .csv AND set to be exported.")
    else:
      deleteKeys.append(key)
  if failure:
    print("WARNING: One or more keys -set to be deleted- were found in the .csv and keys['to_shipfile'].")
    print("         This is ambiguous, no action will be taken for these keys.")
    print("------------------------------")



# Create the data structure based on shipdata.csv
deleteKeys = []
def createDatastructure():
  data = mod.readFile(mod.shipdata['read_csv_location']) # Read the csv file to memory
  csvKeys = mod.cleanLine(data[0], '"\t ', ';')          # Fetch the headers
  # Only export the keys that are defined in keys['to_shipfile'] AND appear in the .csv
  exportKeys = mod.commonListItems(csvKeys, mod.keys['to_shipfile'])
  # Check the index of 'SHIP_filename'
  filenameIndex = -1
  if 'SHIP_filename' in csvKeys:
    filenameIndex = csvKeys.index('SHIP_filename')
  else:
    print("🛑 Couldn't find the field 'SHIP_filename' in "+shipdata['read_csv_location'])
    print("   It is mandatory to have this field, this script can't find the original txt file otherwise.")
    print("   Exiting")
    exitScript()
  # Map the data to the header keys to create 'key: value' pairs.
  shipdata = {}
  for line in data[1:]:
    line = mod.cleanLine(line, '"\t ', ';')
    filename = line[filenameIndex]
    shipdata[filename] = {}
    # Loop through the header
    for idx, key in enumerate(exportKeys):
      # Fix 'SHIP_specials_raw'
      if key == 'SHIP_specials_raw':
        line[idx] = ",".join(line[idx].split('\r'))
        line[idx] = "#".join(line[idx].split(': '))
      if key in mod.keys['delete_from_shipfiles']:    # Don't take action if this key is also set to be deleted
        continue
      # Excel doesn't export an empty field when it's the last on a row.
      # By checking the length of the line against the position of the header, we can avoid an error.
      if idx <= len(line):
        shipdata[filename][key] = line[idx]
  validateKeys(csvKeys)
  processShipFiles(shipdata, exportKeys)

createDatastructure()
exitScript()
