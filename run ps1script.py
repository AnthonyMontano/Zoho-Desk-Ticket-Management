import subprocess, sys
p = subprocess.Popen(["powershell.exe", 
              "C:\\Users\\anthonym\\Zoho\\env\\Scripts\\Zoho-Desk-Ticket-Management\\UserDataHandling.ps1"], 
              stdout=sys.stdout)
p.communicate()