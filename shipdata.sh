#!/bin/bash

# Requires: bash, find

# This script can be used to export an ordered set of keys from the ship txt files to a csv file.

# Run 'shipdata.sh -keys' to get a list of all config keys between <STATS> and <ITEM>
# Adjust the array to add, remove or reorder colums in the exported .csv
# Using the arguments 'shipdata.sh -keys -format' will format the output to an array like below.
KEYS=( \
  "SHIP_name" \
  "SHIP_manufacturer" \
  "SHIP_class" \
  "SHIP_skill_level" \
  "SHIP_type" \
  "SHIP_active_slots" \
  "SHIP_passive_slots" \
  "SHIP_base_price" \
  "SHIP_base_thrust" \
  "SHIP_base_engine_burn" \
  "SHIP_base_turn" \
  "SHIP_base_speed" \
  "SHIP_base_energy" \
  "SHIP_base_recharge" \
  "SHIP_base_armor" \
  "SHIP_base_shield" \
  "SHIP_base_shield_recharge" \
  "SHIP_base_mass" \
  "SHIP_base_cargo" \
  "SHIP_base_drones" \
  "SHIP_base_lifesupport" \
  "SHIP_base_scan_pulsespeed" \
  "SHIP_base_scan_pulserange" \
  "SHIP_base_scan_speed" \
  "SHIP_base_scan_max_targets" \
  "SHIP_explosive_resistance" \
  "SHIP_impact_resistance" \
  "SHIP_energy_resistance" \
  "SHIP_faction_id" \
  "SHIP_specials_raw" \
)

# Path to the Ship Data directory
SOURCE="/home/user/.local/share/Steam/steamapps/common/Astrox Imperium/Astrox Imperium_Data/MOD/ships/"

SHIPS=()
declare -A SHIPDATA
ACTION=$1
DOFORMAT=$2

function parseOutput {
  echo "Preparing output..."
  # Done parsing, cook the output
  if [[ $ACTION == "-keys" ]]; then
    # Keys were asked
    declare -A uniqueKeys
    for i in "${FOUNDKEYS[@]}"; do
      uniqueKeys["$i"]=1;
    done
    if [[ $DOFORMAT = "-format" ]]; then
      echo ""
      echo "Here's the list of unique config keys from ship .txt files, in array format"
      echo "---------------------------------------------------------------------------"
      echo "KEYS=( \\"
      printf '  "%s" \\\n' "${!uniqueKeys[@]}"
      echo ")"
      echo ""
    else
      echo ""
      echo "Here's the list of unique config keys from ship .txt files"
      echo "----------------------------------------------------------"
      printf '%s\n' "${!uniqueKeys[@]}"
      echo ""
      echo "Tip: use './shipdata.sh -keys -format' to output an array."
    fi
  # Create a .csv export
  else
    # create the header
    IFS=';'; echo "${KEYS[*]}" > shipdata.tmp; IFS=$' \t\n'
    # Loop through the ships, then KEYS to output the requested data
    for i in "${SHIPS[@]}"; do
      line=""
      for j in "${KEYS[@]}"; do
        # Special handling for "SHIP_specials_raw"
        if [[ $j == "SHIP_specials_raw" ]]; then
          eol=$'\r'
          specials="${SHIPDATA[${i},${j}]}"
          specials="${specials//,/$eol}"
          specials="${specials//#/: }"
          line="${line};\"${specials}\""
        else
          line="${line};\"${SHIPDATA[${i},${j}]}\""
        fi
      done
      line=${line:1}
      echo ${line} >> shipdata.tmp
    done
    mv ./shipdata.tmp ./shipdata.csv
    echo ""
    echo "Created 'shipdata.csv' in your current directory."
  fi
}

parseTxt () {
  local FILE="$1"
  local collect=false
  local NAME=$(basename "${FILE}" ".txt"); NAME=${NAME:11:-1}
  # Add ship to list of found ships
  SHIPS+=( "$NAME" )
  while IFS=$' \t\r\n' read -r line; do
    # If we're between <STATS> and <ITEM>, collect the keys & values
    if [[ "${line:0:7}" == '<STATS>' ]]; then collect=true; continue; fi
    # Stop parsing when <ITEM> is encountered
    if [[ "${line:0:6}" == "<ITEM>" ]]; then break; fi
    # Ignore lines starting with //
    if [[ "${line:0:2}" == "//" ]]; then continue; fi
    if [[ $collect == true ]]; then
      key=$(echo "${line}" | cut -d ";" -f 1)
      FOUNDKEYS=(${FOUNDKEYS[@]} "${key}")
      info=$(echo "${line}" | cut -d ";" -f 2- --output-delimiter " ")
      info=${info%$'\r'}
      SHIPDATA[${NAME},${key}]=${info}
    fi
  done < "${FILE}"

}

loopTxt () {
  echo "Parsing ship txt files..."
  FOUNDKEYS=()
  count=$(find "${SOURCE}" -type f -name "*.txt" -printf '.' | wc -c)
  counter=0
  echo -n "Parsing file ${counter} of ${count}"
  while IFS= read fn; do
    $counter
    echo -n -e "\r\033[1A\033[0KParsing file $((++counter)) of ${count}"
    parseTxt "${fn}"
  done < <(find "${SOURCE}" -type f -name "*.txt")
  echo " ... Finished!"
  parseOutput
}
loopTxt


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
#  SHIP_collider_z              Length of the collission box
#  SHIP_collider_y              Height of the collission box
#  SHIP_collider_x              Width of the collission box
##
## Life Support (Self explanatory, always 0 in the ship files)
#  SHIP_ls_points
#  SHIP_ls_food
#  SHIP_ls_thermal
#  SHIP_ls_water
#  SHIP_ls_waste
