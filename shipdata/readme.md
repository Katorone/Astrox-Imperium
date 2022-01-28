Astrox Imperium: shipdata to csv to shipdata

To use these tools, download:
- shipdata_2_csv.py
- csv_2_shipdata.py
- shipdata_settings.py

Please read through shipdata_settings.py.  This file contains all configurable options and explanation of what each option does.

As their names imply, these scripts can be used to read Astrox Imperium shipfiles to a .csv file for easy editing.  Afterwards this .csv can be exported back to Astrox ship files.

When upgrading from previous versions without shipdata_settings.py, I suggest to first download shipdata_settings.py and edit it with the settings you have in your current .py files.  Afterwards, download shipdata_2_csv.py and csv_2_shipdata.py as well, overwriting the older versions.

For complex setups it's now possible to include these scripts in a toolchain.
Both py scripts will accept the argument `--config /path/to/custom_config.py`

Example: `python3 ~/Projects/Astrox/shipfiles_2_csv.py --config ~/Projects/AstroxModPack/modpacksettings.py`

The benefit here is that only a copy of this file needs to be adjusted while the actual scripts can be easily updated.
