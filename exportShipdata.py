#!/usr/bin/python3

# This script exports ship data from the Astrox MOD/ships directory to a .csv file.

# Path to the Astrox Imperium/Astrox Imperium_Data/MOD/ships/ -directory:
# For windows, use: C:/path/to/ships
source = "/home/user/.local/share/Steam/steamapps/common/Astrox Imperium/Astrox Imperium_Data/MOD/ships/"

# Make 'SHIP_specials_raw' human readable? (True/False)
expandSpecials = True

# This array should contain all possible SHIP-keys, but can be ordered in any way.
# The order of the keys also determines the order of the columns in the exported csv
# Only use the key name, don't add the separator ";", the script needs to add this itself.
keys = [
  "//General Info",
  "SHIP_name",
  "SHIP_filename",
  "SHIP_class",
  "SHIP_type",
  "SHIP_skill_level",
  "SHIP_base_level",
  "SHIP_base_price",
  "SHIP_manufacturer",
  "SHIP_manufacturer_icon",
  "SHIP_faction_id",
  "//Main Stats",
  "SHIP_active_slots",
  "SHIP_passive_slots",
  "SHIP_base_drones",
  "SHIP_base_shield",
  "SHIP_base_armor",
  "SHIP_base_energy",
  "SHIP_base_cargo",
  "SHIP_base_lifesupport",
  "//Propulsion",
  "SHIP_base_mass",
  "SHIP_base_thrust",
  "SHIP_base_turn",
  "SHIP_base_engine_burn",
  "SHIP_base_speed",
  "//Sensors",
  "SHIP_base_scan_max_targets",
  "SHIP_base_scan_speed",
  "SHIP_base_scan_pulserange",
  "SHIP_base_scan_pulsespeed",
  "//Resistance",
  "SHIP_impact_resistance",
  "SHIP_energy_resistance",
  "SHIP_explosive_resistance",
  "//Regeneration",
  "SHIP_base_recharge",
  "SHIP_base_shield_recharge",
  "//Bonuses",
  "SHIP_specials_raw",
  "//Description",
  "SHIP_description",
  "//Editor",
  "SHIP_material_texture_a",
  "SHIP_material_texture_b",
  "SHIP_material_texture_c",
  "SHIP_material_color_a",
  "SHIP_material_color_b",
  "SHIP_engine_color",
  "//Misc",
  "SHIP_shield",
  "SHIP_armor",
  "SHIP_energy",
  "SHIP_ls_food",
  "SHIP_ls_water",
  "SHIP_ls_thermal",
  "SHIP_ls_waste",
  "SHIP_ls_points",
  "SHIP_collider_x",
  "SHIP_collider_y",
  "SHIP_collider_z",
  "//Merc stuff",
  "SHIP_owner",
  "SHIP_xp",
  "SHIP_next_level_xp",
  "SHIP_level",
  "SHIP_talent",
  "SHIP_loyalty",
  "SHIP_payroll",
  "//; --------------------------------- SHIP PARTS -----------------------------------",
  "//; --------------- ITEM,type,catID,pfID,xp,yp,zp,xr,yr,zr--------------------------",
]

### End of configuration ###
###   Code starts here   ###
import glob
import os
shipdata = {}

# Function that exports the collected data to .csv
def writeExport():
  outfile = open('shipdata.tmp', 'w')
  # Write headers
  line = ""
  for i in keys:
    if i[:2] == '//': continue
    line=line+'"'+i+'";'
  outfile.write(line+'\n')
  # Write data
  for i in shipdata.keys():  # Loop over the ships
    line = ""
    for j in keys:           # Loop over the ordered keys
      if j[:2] == '//': continue
      val = shipdata[i].get(j, "")
      line=line+'"'+val+'";'
    outfile.write(line+'\n')
  outfile.close()
  # Move the tempfile to shipdata.csv
  os.replace("shipdata.tmp", "shipdata.csv")
  print("Finished exporting Astrox Imperium shipdata to shipdata.csv")


# Function which opens each txt file in turn and parses it
def parseFile(source):
  filename = os.path.basename(source)
  shipname = filename[0:-4]
  #name = name[0:-4]
  collect = False
  shipdata[shipname] = {}
  # We're opening with utf-8 compatibility because of non-western languages
  with open(source, encoding='utf8') as f:
    for line in f:
      line = line.strip()
      # If we're between <STATS> and <ITEM>, collect the keys & values
      if line == "": continue
      if line[:7] == '<STATS>':
        collect = True
        continue
      if line[:6] == '<ITEM>': break
      if line[:2] == '//': continue
      if collect:
        keyVal = line.split(';')
        key = keyVal[0]
        val = ";".join(keyVal[1:])
        # Sanity checking
        if key == "SHIP_filename" and val != shipname:       # Make sure SHIP_filename matches the filename
          print('Error in file: '+filename+', SHIP_filename doesn\'t match source file')
        if key not in keys:                                  # Make sure the 'key' is in 'keys'
          print('Error in file: '+filename+', Unknown key: '+key)
          # Add the missing key to the end of 'keys'
          keys.append(key)
        # data manipulation
        if expandSpecials == True and key == 'SHIP_specials_raw':
          val = ': '.join(val.split('#'))
          val = '\r'.join(val.split(','))
        # Store the information
        shipdata[shipname][key] = val

# Function that collects all txt files in 'source'
def getFiles(source):
  # Get a list of txt files in source
  files = glob.glob(os.path.join(source, '*.txt'))
  for fn in files:
    parseFile(fn)
  writeExport()

if __name__ == "__main__":
  getFiles(source);
