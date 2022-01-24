# Astrox-Imperium
A collection of scripts aimed at datacollection and modding of Astrox Imperium

- shipdata-2-csv.py - Exports data from the Astrox Imperium ship-files and creates a csv.
- csv-2-shipdata.py - Imports data from a csv and exports it to Astrox Imperium ship-files (designed to be used with exportShipdata.py).
- shipdata.sh - A bash script that exports a configurable list of keys from the Atrox Imperium ship-files and creates a csv.

Get Python 3 here: https://www.python.org/downloads/

Working with CSV files:
- With LibreOffice Calc you won't have any issues. Just tell Calc to encapsulate the fields with '"' and split them on ';' when exporting your spreadsheet back to csv for csv-2-shipdata.
- With Excel, things are trickier and some configuration is needed:
  - In Windows' Control Panel -> Regional Settings -> Additional Settings -> Change 'List separator' to '|'.
  - In csv-2-shipdata.py, change line 19 to `delimiter = '|'`.
  - If you want to be able to doubleclick the csv and immediately open it with excel, change shipdata-2-csv.py:line 13 to `delimiter='|'`.


