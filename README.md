# printer_life_sheet_count

What is it?
-----------
Unloads the number of sheets printed on the selected printer from the first day of work using the SNMP v1 protocol.

How it work?
-----------
To work you will need:
- IP adresses of the printers;
- pysnmp.hlapi package
- time module
- win32ui module
- configparser module

First you must make settings in the KyoMon.ini file.
After using the script, you can see the received data in the life_count.txt file.
