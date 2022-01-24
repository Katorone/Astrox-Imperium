# Astrox-Imperium
A collection of scripts aimed at datacollection and modding of Astrox Imperium

- exportShipdata.py - Exports data from the Astrox Imperium ship-files and creates a csv.
- importShipdata.py - Imports data from a csv and exports it to Astrox Imperium ship-files (designed to be used with exportShipdata.py).
- shipdata.sh - A bash script that exports a configurable list of keys from the Atrox Imperium ship-files and creates a csv.

Get Python 3 here: https://www.python.org/downloads/

Working with CSV files:
- With LibreOffice Calc you won't have any issues. Just tell Calc to encapsulate the fields with '"' and split them on ';'
- With Excel, things are trickier and some configuration is needed:
  - In Windows' Control Panel -> Regional Settings -> Additional Settings -> Change 'List separator' to '|'.
  - In importShipData.py, change line 19 to `delimiter = '|'
