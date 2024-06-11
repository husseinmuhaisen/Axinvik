import re
import utmp
from prettytable import PrettyTable

def print_name():
    print(
        """
  ,  /\  .  
 //`-||-'\\ 
(| -=||=- |)
 \\,-||-.// 
  `  ||  '  
     ||     
     ||     
     ||     
     ||     
     || 

Axinvik v 1.0
"""
    )

print_name()

def extractIPs(file_path):
    ipPattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    with open(file_path, 'r') as file:
        logContent = file.read()
    ipAddresses = re.findall(ipPattern, logContent)
    return ipAddresses

def table():
    table = PrettyTable()
    table.field_names = ['IP address(s)']
    file_path = input("[+] Enter the file path:\n")
    ipAddresses = extractIPs(file_path)
    for ip in ipAddresses:
        table.add_row([ip])
    print(table)

def wtmpParse():

    file_path = input("[+] Enter the file path:\n")
    with open(file_path, 'rb') as fd:
        binContent = fd.read()

    # creating the pretty table object
    table = PrettyTable()
    table.field_names = ["Time", "Type", "User", "Host", "Entry details"]
    userPattern = re.compile(r"user='([^']*)'")
    hostPattern = re.compile(r"host'([^']*)'")

    for entry in utmp.read(binContent):
        entryStr = str(entry)
        userMatch = userPattern.search(entryStr)
        userMatch = userMatch.group(1) if userMatch else "No user"

        hostMatch = hostPattern.search(entryStr)
        hostMatch = hostPattern.group(1) if hostMatch else "No host"
        table.add_row([entry.time, entry.type, entry.user, entry.host, entry])
    
    print(table)


def mainMenu():
    try:
        while True:
            print("\n1) Extract IP addresses")
            print("2) Parse WTMP file content")
            print("3) Exit")
            option = input("\n[+] Select your option: ")

            if option == '1':
                table()
            elif option == '2':
                wtmpParse()
            elif option == '3':
                print("[-] Exiting... ")
                break
            else:
                print("[-] Invalid choice detected")
    except KeyboardInterrupt:
        print("\n[-] Exiting due to user interruption ((CTRL + C) or other interruptions)")

if __name__ == "__main__":
    mainMenu()

