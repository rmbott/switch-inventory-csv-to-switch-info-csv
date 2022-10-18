from nornir import InitNornir
from nornir_csv.plugins.inventory import CsvInventory
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import csv
from typing import List, Any, Iterable


# Flattens any sub-lists within a list
# (useful for Netmiko->textfsm results from Cisco switches)
def flatten(lst: List[Any]) -> Iterable[Any]:
    for sublist in lst:
         if isinstance(sublist, list):
             for item in sublist:
                 yield item
         else:
             yield sublist

# Load inventory
InventoryPluginRegister.register("CsvInventoryPlugin", CsvInventory)
nr = InitNornir(config_file='config.yaml')

#Create a list of switches
switches = []
for host in nr.inventory.hosts:
    switches.append(host)

# Run a "sh ver" command and save the results
print("Running \"sh ver\" on switches: ", list(nr.inventory.hosts.values()))
res = nr.run(
    task=netmiko_send_command,
    command_string="show version", use_textfsm=True
)

# If there are any switches to work with, use the results from the command run on the
# first switch to make a list of column headers for our output CSV.
if len(switches) > 0:
    resultsSwitch1 = res[list(nr.inventory.hosts.keys())[0]][0].result[0]
    resultkeys = list(resultsSwitch1.keys())
    
    # Add a new key for the inventory-name of the switch iself.
    key = ['switch']
    field_names = key + resultkeys
else:
    print("Inventory appears empty. There is nothing to be done.")

# Populate results
rows = []
for switch in switches:
    # Check for non-results
    if type(res[switch][0].result[0]) is not dict:
        print("Skipping ", switch, "because there were no results. (probably timed-out while trying to connect)")
    else:
        result = res[switch][0].result[0]
        result["switch"] = switch
        values = list(result.values())
        keys = list(result.keys())
        flattened_values = list(flatten(values))
        fixed_result = {keys[i]: flattened_values[i] for i in range(len(keys))}
        rows.append(fixed_result)

with open('info.csv', 'w') as csvfile:
   writer = csv.DictWriter(csvfile, fieldnames=field_names)
   writer.writeheader()
   writer.writerows(rows)
