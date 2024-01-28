from TokenManagerTest import TokenManagerTest
from ZohoReporter import ZohoReporter
import requests
import re
import json
from bs4 import BeautifulSoup



with open(r'C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/ZohoConfigFileTest.json' ,'r') as file:
    config_data = json.load(file)
offboardingheaders = config_data['apiheaders']
offboardingparams = config_data['offboardingparams']
offboardingurl = config_data['apiurl']

"""Show this as new version in Github"""
"""The purpose of this class is to access offboarding ticket data and store it for furture scripting"""
class ManageOffboardingTickets:

    def __init__(self):
        self.offboardingurl = offboardingurl
        self.offboardingheaders = offboardingheaders
        self.offboardingparams = offboardingparams
        self.ticketdata = ""
        self.ticketIds = []
        self.jsoncontent = ""
        self.jsonstring = ""
        self.content = ""
        self.ticketnumbers = []
        self.ticketidsiter = []


    def getopenoffboardtickets(self):
            try:
                with open('C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Read', 'r') as file:
                    access_token_str = file.read()
                self.offboardingheaders['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
                response = requests.get(url = self.offboardingurl, headers = self.offboardingheaders, params = self.offboardingparams)
                status_code = response.status_code
                match status_code:
                    case 200:
                        print('Status Code: Ok... Grabbing Ticket Numbers and IDs....')
                        jsondata = response.json()
                        for ticket in jsondata.get('data',[]):
                            ticket_id = ticket.get('id')
                            ticket__number = ticket.get('ticketNumber')
                            self.ticketIds.append(ticket_id)
                            self.ticketnumbers.append(ticket__number)
                            self.ticketidsiter.append(ticket_id)
                    case 204:
                        print('Status Code: No content')
                    case 400:
                        print('Status Code: Bad request')
                    case 401:
                        print('Status Code: Unauthorized... Grabbing a new token... ')
                        instance_a = TokenManagerTest({'scope':'Desk.tickets.READ'})
                        instance_a.call_new_access_token()
                        print("Renewed token, Now grabbing Ticket numbers and IDs....")
                        self.getopenoffboardtickets()
                    case 403:
                        print('Status Code: Forbidden (Unauthorised access)')
                    case _:
                        print('Please refer to zoho api documentation')
            except requests.exceptions.ConnectionError:
                print("No internet available at the moment please try again later.")


    def getopenoffboardticketcontent(self):
        startofcontenturl = "https://desk.zoho.com/api/v1/tickets/"
        endofcontenturl = "/latestThread"
        with open('C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Read', 'r') as file:
                access_token_str = file.read()
        self.offboardingheaders['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
        for ticketid in self.ticketIds:
            contenturl = f"{startofcontenturl}{ticketid}{endofcontenturl}"
            response = requests.get(contenturl, headers=self.offboardingheaders)
            content_status_code = response.status_code
            match content_status_code:
                case 200:
                    print('Status Code: Ok... Grabbing Ticket Content....')
                    self.jsoncontent = json.loads(response.text)
                    ticket.prepoffboarddata()
                case 204:
                    print('Status Code: No content')
                case 400:
                    print('Status Code: Bad request')
                case 401:
                    print('Status Code: Unauthorized... Grabbing a new token...')
                    instance_z = TokenManagerTest({'scope':'Desk.tickets.READ'})
                    instance_z.call_new_access_token()
                    ticket.getopenoffboardticketcontent()
                case 403:
                    print('Status Code: Forbidden (Unauthorised access)')
                case _:
                    print("Refer to Zoho API documentation")


    def prepoffboarddata(self):
        """"""
        z = self.ticketnumbers.pop(0)
        y = self.ticketidsiter.pop(0)

        all_data = []

        a = self.jsoncontent['content']
        text=json.dumps(a, sort_keys=True, indent=4)
        soup = BeautifulSoup(text, 'html.parser')
        text_content = re.sub(r'<.*?>', '', soup.get_text(separator='\n'))
        all_text_pattern = re.compile(r'Employee Name:(.*?)Completed By:', re.DOTALL)
        all_text_match = re.search(all_text_pattern, text_content)
        if all_text_match:
            str = (f"{all_text_match.group(0).strip()}")
            lines = str.split('\n')
            data_dict = {'Ticket Number': z, 'Ticket ID': y}
            for line in lines:
                parts = line.split(':')
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else '' 
                data_dict[key] = value
            data_dict['1st Script'] = 1
            data_dict['2nd Script'] = 0
            data_dict['3rd Script'] = 0
            data_dict['4th Script'] = 0
            data_dict['5th Script'] = 0
            all_data.append(data_dict)

            try:
                with open("C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json", 'r') as existing_file:
                    existing_data = json.load(existing_file)
            except FileNotFoundError:
                existing_data = []

        # Append new data to the existing content
            existing_data.extend(all_data)

        # Write the combined data back to the file
            with open("C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json", 'w') as f:
                json.dump(existing_data, f, indent=4)

ticket = ManageOffboardingTickets()
ticket.getopenoffboardtickets()
ticket.getopenoffboardticketcontent()
z = ZohoReporter()
z.getticketIds()
z.update_no_email_ticket_data()

        