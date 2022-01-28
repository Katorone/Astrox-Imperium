# More information, as well as the (non)licence can be found at: https://github.com/Katorone/Astrox-Imperium
# If you run into any issues, feel free to open an issue on Github, or write me (katorone#2957) on the Astrox discord.

# This file contains configuration settings for:
# - shipfiles_2_csv.py
# - csv_2_shipfiles.py

# For complex setups it's now possible to include these scripts in a toolchain.
# Both py scripts will accept the argument --config /path/to/custom_config.py
#   Example: python3 ~/Projects/Astrox/shipfiles_2_csv.py --config ~/Projects/AstroxModPack/modpacksettings.py
# The benefit here is that only a copy of this file needs to be adjusted while
# the actual scripts can be easily updated.

# Please read through this file and adjust the values where needed.

# Initializing variables containing settings, please don't change the following lines:
shipdata = {}
keys = {}
delimiter = {}

### PATHS
## Note: Example for windows users:
##       C:\Program Files (x86)\Steam\Steamapps\Common\Astrox Imperium\Astrox Imperium_Data\MOD\ships
## These paths are completely configurable to help with toolchaining and automation.
## See the note on top about calling shipdata_2_csv.py and csv_2_shipdata.py with the config argument.
##
# Path to the Astrox Imperium ship files you want to create a csv FROM
shipdata['source'] = "~/.local/share/Steam/steamapps/common/Astrox Imperium/Astrox Imperium_Data/MOD/ships"
# Path to the Astrox Imperium ship files you want to export a csv TO
# IMPORTANT: Any directory can be used as a destination, but this directory needs to have a copy
#            of Astrox ship files!
shipdata['target'] = "~/Projects/Astrox/ships"
# Path and name of the csv where to store shipdata TO
shipdata['write_csv_location'] = "~/Projects/Astrox/shipdata.csv"
# Path and name of the csv where to read shipdata FROM
shipdata['read_csv_location'] = "~/Projects/Astrox/shipdata.csv"

# Pause after running the script?
# When True, this settings adds: 'All done. Press enter to exit.' after the scripts run
# Enable this if you want to see the scripts' output when running them from the file browser
pauseOnExit = True

# A list of keys to read from the shipfiles and export to csv.
# This list and the one below are functionally the same, merely formatted differently!
keys['from_shipfiles'] = [
  "SHIP_name", "SHIP_filename", "SHIP_class", "SHIP_type", "SHIP_skill_level",
  "SHIP_base_price", "SHIP_manufacturer", "SHIP_active_slots", "SHIP_passive_slots",
  "SHIP_base_drones", "SHIP_base_shield", "SHIP_base_armor", "SHIP_base_energy",
  "SHIP_base_cargo", "SHIP_base_lifesupport", "SHIP_base_mass", "SHIP_base_thrust",
  "SHIP_base_turn", "SHIP_base_engine_burn", "SHIP_base_speed", "SHIP_impact_resistance",
  "SHIP_energy_resistance", "SHIP_explosive_resistance", "SHIP_specials_raw",
  "SHIP_description",
]
# A list of keys to write TO the shipfiles from a csv.
# If empty, the order from keys['from_shipfiles'] will be used.
#  -> keys['to_shipfile'] = []
# Comments (added with '//') will be exported to the shipfiles as well!
keys['to_shipfile'] = [
  "//General Info",
  "SHIP_name",
  "SHIP_filename",
  "SHIP_class",
  "SHIP_type",
  "SHIP_skill_level",
  "SHIP_base_price",
  "SHIP_manufacturer",
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
  "//Resistance",
  "SHIP_impact_resistance",
  "SHIP_energy_resistance",
  "SHIP_explosive_resistance",
  "//Bonuses",
  "SHIP_specials_raw",
  "//Description",
  "SHIP_description",
]
# Are there any keys that have to be deleted from all files?  List them here:
# IMPORTANT: Regardless of this setting, if the key is listed in keys['to_shipfile'], and
#            also exists in the csv, it will not be deleted!
#            This setting will ONLY delete keys that are NOT in keys['to_shipfile'] or NOT
#            in the csv and ONLY when exporting a csv back to the ship files.
keys['delete_from_shipfiles'] = [
  "SHIP_id"
]

#### A COMPLETE LIST (as of writing) OF KEYS CAN BE FOUND BELOW ####

# When writing 'SHIP_specials_raw' to the csv, expand them to be human readable?
# This setting makes it easier to edit SHIP_specials_raw
# Examples
#   False : Thrust#0.20,Miner Range#0.60,Miner Energy#0.50
#   True : Thrust: 0.20
#          Miner Range: 0.60
#          Miner Energy: 0.50
# NOTE: csv_2_shipdata.py will always try to rebuild the original string for Astrox,
#       regardless of this setting.
expandSpecials = True


### CSV OPTIONS
## When creating the csv from shipdata, the script will always encapsulate the fields with quotation marks
## Both Excel and LibreOffice Calc should have no issues reading these files.
## Because of a wide range of system and language settings, it is possible to config
## the delimiter here, for both reading a csv and writing to a csv.
##
## NOTE: Excel users might want to set these to "|", per https://github.com/Katorone/Astrox-Imperium/blob/main/README.md
# For best compatibility, do not set this to any of these characters: #.,:
# Delimiter to use when creating a csv FROM shipfiles
delimiter['write_csv'] = ";"
# Delimiter to use when writing shipfiles FROM a csv
delimiter['read_csv'] = ";"


### List of all found keys and their meaning:
##
## Descriptive information:
#  SHIP_name                    Short descriptive name of the ship
#  SHIP_description             Long text, description of the ship's type and usage
#  SHIP_class                   The class of the ship: Shuttle, Frigate, ...
#  SHIP_skill_level             The level needed in SHIP_class university courses to be able to fly the ship
#  SHIP_type                    Faction of the ship: Fabricator, Excavation, ...
#  SHIP_filename                Filename for the ship's data and image
#  SHIP_manufacturer            Fluff, name of the factory that built the ship
#  SHIP_manufacturer_icon       Icon of the manufacturer
##
## Base statistics (All of these values are BEFORE any (potential) modifiers)
#  SHIP_active_slots            Amount of active slots
#  SHIP_passive_slots           Amount of passive slots
#  SHIP_base_armor              Armor hitpoints
#  SHIP_base_shield             Total shield capacity
#  SHIP_base_shield_recharge    Recharge speed of the shields
#  SHIP_base_energy             Total energy capacity
#  SHIP_base_recharge           Energy recharge rate
#  SHIP_base_mass               How 'heavy' the ship is.  Higher mass means lower speed and turn-rate
#  SHIP_base_thrust             Accelleration of the ship
#  SHIP_base_speed              Top speed without afterburner
#  SHIP_base_turn               Turning speed of the ship
#  SHIP_base_engine_burn        Rate at which engines use energy (lower is better)
#  SHIP_base_scan_pulsespeed    How fast the passive scanner scans
#  SHIP_base_scan_pulserange    How far the passive scanner can target
#  SHIP_base_scan_max_targets   Amount of objects the ship's passive scanner can target at once
#  SHIP_base_scan_speed         Base speed of the active scanner
#  SHIP_base_cargo              Cargo space in m²
#  SHIP_base_price              Cost of the ship
#  SHIP_base_drones             Amount of drones the ship can command
#  SHIP_base_lifesupport        Lifesupport points of the ship's internal systems
#  SHIP_specials_raw            Text describing the bonusses for a specific ship (Drone Range#0.30,Miner Strength#0.50)
##
## Resistances (All of these values are BEFORE any (potential) modifiers)
#  SHIP_explosive_resistance    Resistance against missles
#  SHIP_impact_resistance       Resistance against projectiles
#  SHIP_energy_resistance       Resistance against beams & lasers
##
## Mercenary & NPC related
#  SHIP_level                   Mercenary: current level
#  SHIP_xp                      Mercenary: XP earned on their current level
#  SHIP_next_level_xp           Mercenary: XP needed to earn their next level
#  SHIP_base_level              Mercenary/Shipyard: impacts the hire level of a mercenary, and changes the odds of
#                                 the ship being picked by the ADJUST_HANGAR-event (MOD/events/events_background.txt)
#  SHIP_payroll                 Mercenary: recurring wages
#  SHIP_armor                   Mercenary/NPC: Current armor points
#  SHIP_energy                  Mercenary/NPC: Current energy points
#  SHIP_shield                  Mercenary/NPC: Current shield points
#  SHIP_owner                   Mercenary/NPC: Name of the pilot
#  SHIP_loyalty                 Mercenary: current loyalty percentage
#  SHIP_talent                  Mercenary: Determines the ship's loadout: Combat, Exploration, ...
#  SHIP_faction_id              Mercenary/NPC: Used by the game to show the ship's faction
##
## Model related
#  SHIP_material_texture_a      Main (base) texture
#  SHIP_material_texture_b      Textures with details added on top
#  SHIP_material_texture_c      Texture for parts that glow
#  SHIP_material_color_a        Voodoo
#  SHIP_material_color_b        Voodoo
#  SHIP_engine_color            Burn and trailing color of the engine(s)
#  SHIP_collider_z              Unused
#  SHIP_collider_y              Unused
#  SHIP_collider_x              Unused
##
## Life Support (Self explanatory, always 0 in the ship files)
#  SHIP_ls_points
#  SHIP_ls_food
#  SHIP_ls_thermal
#  SHIP_ls_water
#  SHIP_ls_waste


##########################################################
###           Some functions I regularly use           ###
### It makes little sense to duplicate them everywhere ###
##########################################################
import os

## Validation and parsing of user settings:
# If csv -> shipfiles-keys is empty, use the ones for shipfiles -> csv
if len(keys['to_shipfile']) == 0:
  keys['to_shipfile'] = keys['from_shipfiles']
# Expands paths when ~ is used
for i in shipdata: shipdata[i] = os.path.expanduser(shipdata[i])
# Check if all paths exist (don't check individual files)
for i in ['source', 'target']:
  shipdata[i] = os.path.join(shipdata[i], '.')
e = False
for i in shipdata:
  if not os.path.isdir(os.path.dirname(shipdata[i])):
    e = True
    print("🛑 The configured directory for shipdata['"+i+"'] does not exist: "+os.path.dirname(shipdata[i]))
if e: input("Press enter to exit."); quit()

# reads data from path
def readFile(path):
  fh = open(path, 'r', encoding='utf8', newline='\n')
  data = fh.readlines()
  fh.close()
  return data

# Writes a list of data to path
def writeFile(path, dataList):
  fh = open(path+".tmp", 'w', encoding='utf8', newline='')
  for line in dataList:
    fh.write(line+'\r\n')
  fh.close()
  os.replace(path+".tmp", path)
  print("✔️ Finished writing: "+path)

# Takes a string and returns a list
def cleanLine(line, strip, delim):
  line = line.strip()
  if line == "": return line
  if line[-1] == delim: line = line[0:-1]
  return [x.strip(strip) for x in line.split(delim)]

# Compares two lists and returns the common items
def commonListItems(l1, l2):
  l2Set = set(l2)
  return [x for x in l1 if x in l2Set]
