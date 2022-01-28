#!/usr/bin/python3

# More information, as well as the (non)licence can be found at: https://github.com/Katorone/Astrox-Imperium
# If you run into any issues, feel free to open an issue on Github, or write me (katorone#2957) on the Astrox discord.

### Please see shipdata_settings.py for configuration options.

# This script exports Astrox ship data to a csv-file.

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

# Function that exports the collected data to .csv
def writeExport(shipdata):
  joiner = '"'+mod.delimiter['write_csv']+'"'
  data = []
  line = []
  # Write header
  for i in mod.keys['from_shipfiles']:
    if i[:2] == '//': continue
    line.append(i)
  data.append('"'+joiner.join(line)+'"')
  # Write data
  for i in shipdata.keys():  # Loop over the ships
    line = []
    for j in mod.keys['from_shipfiles']:    # Loop over the ordered keys
      if j[:2] == '//': continue
      line.append(shipdata[i].get(j, ""))   # List all keys per ship
    data.append('"'+joiner.join(line)+'"')
  mod.writeFile(mod.shipdata['write_csv_location'], data)

# Function which opens each txt file in turn and parses it
unlistedKeys = []
def parseFile(data, shipname):
  collect = False
  result = {}
  for line in data:
    line = mod.cleanLine(line, '\t ', ';')
    key = line[0]
    if key == "": continue                             # Ignore empty lines
    if key[:7] == '<STATS>': collect = True; continue  # Start collecting at <STATS>
    if key[:6] == '<ITEM>': break                      # Stop collecting at <ITEM>
    if key[:2] == '//': continue                       # Ignore comments
    if collect:
      val = ";".join(line[1:])
      # Sanity checking
      if key == "SHIP_filename" and val != shipname:    # Make sure SHIP_filename matches the filename
        print('❌ Error for: '+shipname+', SHIP_filename doesn\'t match source file')
      if key not in mod.keys['from_shipfiles']:         # Check if the file contains an unlisted key in mod.keys['from_shipfiles']
        if key not in unlistedKeys:
          print('❌ Unlisted key for '+shipname+': '+key+'. This key won\'t be exported and future warnings for this key will be surpressed.')
          unlistedKeys.append(key)
        continue
      # data manipulation
      if key == 'SHIP_specials_raw' and mod.expandSpecials:
        val = ': '.join(val.split('#'))
        val = '\r'.join(val.split(','))
      # Store the information
      result[key] = val
  return result

# Function that collects all txt files in 'source'
def getFiles(source):
  # Get a list of txt files in source
  shipdata = {}
  files = glob.glob(os.path.join(source, '*.txt'))
  for fn in files:
    filename = os.path.basename(fn)
    shipname = filename[0:-4]
    shipdata[shipname] = parseFile(mod.readFile(fn), shipname)
  writeExport(shipdata)

getFiles(mod.shipdata['source']);
exitScript()
