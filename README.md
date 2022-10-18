# switch-inventory-csv-to-switch-info-csv
Creates a CSV of switch info ( model, serial, MAC, firmware version, etc...) from a switch inventory CSV using nornir and netmiko

## Initial Setup:
1) You'll need to modify hosts.csv giving each switch a name and an IP address -- this is your inventory
2) You'll need to modify config.yaml (specifically the "inventory_dir_path:" parameter) to point to your project directory
3) If you move config.yaml to different folder as infoToCSV.py you'll need to modify the "nr = InitNornir(config_file='config.yaml')" line of infoToCSV.py reflect that.
4) You'll may need to run the following: "pip install nornir nornir-csv nornir-netmiko nornir-utils textfsm"
5) Since infoToCSV.py writes a file "info.csv" to the project folder, you'll need write permissions to that folder.

## Notes:
I've only tested this on Cisco devices.
