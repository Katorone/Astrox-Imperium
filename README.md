# Astrox-Imperium
A collection of scripts aimed at datacollection and modding of Astrox Imperium

- shipdata/
  - shipdata_2_csv.py - Exports data from the Astrox Imperium ship-files and creates a csv.
  - csv_2_shipdata.py - Imports data from a csv and exports it to Astrox Imperium ship-files (designed to be used with shipdata_2_csv.py).
- itemdb/
  - itemdb_2_csv.py - Exports items_database.txt and specs_database.txt to csv and performs sanity checks.

Requires Python 3 (get it here: https://www.python.org/downloads/)
When installing Python on windows, I strongly suggest to enable the option to add python to the PATH.  This will make it easier to create bat files.

Working with CSV files:
- With LibreOffice Calc you won't have any issues. Just tell Calc to encapsulate the fields with '"' and split them on ';' when exporting your spreadsheet back to csv for csv_2_shipdata.
- With Excel, things are trickier and some configuration is needed:
  - In Windows' Control Panel -> Regional Settings -> Additional Settings -> Change 'List separator' to '|'.
  - In shipdata_settings.py, change the delimiter to `delimiter['write_csv'] = "|"` and `delimiter['read_csv'] = "|"`.

Example of a .bat script to use on windows:
```batch
C:\Users\UserName\AppData\Local\Programs\Python\Python310\python.exe C:\AstroxFiles\shipdata_2_csv.py
pause
```
Running this batch file (with paths adjusted for your system) will create shipdata.csv in the same directory.


Libreoffice Calc import settings for csv:

![image](https://user-images.githubusercontent.com/918422/151455249-13715516-f0aa-41f6-9eda-ad9e3a8818f0.png)
