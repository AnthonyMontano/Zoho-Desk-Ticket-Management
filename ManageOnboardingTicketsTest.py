from TokenManagerTest import TokenManagerTest
import requests
import re
import json
from bs4 import BeautifulSoup


with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/ZohoConfigFileTest.json' ,'r') as file:
    config_data = json.load(file)
onboardingheaders = config_data['apiheaders']
onboardingparams = config_data['onboardingparams']
onboardingurl = config_data['apiurl']


"""The Purpose of this class it to access Onboarding ticket data and store it in a understandable way for comprehension and future scripting """
"""Need to implement a method or class that makes changes to the tickets such as changing the status to in progress"""
class ManageOnboardingTicketsTest:

    def __init__(self):
        self.onboardingheaders = onboardingheaders
        self.onboardingparams = onboardingparams
        self.onboardingurl = onboardingurl
        self.ticketdata = ""
        self.ticketIds = []
        self.jsoncontent = ""
        self.jsonstring = ""
        self.content = ""
        self.ticketnumbers = []
        self.ticketidsiter = []
    

    def getopentickets(self):
        try:
            #ticketids = []
            with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Read', 'r') as file:
                access_token_str = file.read()
            self.onboardingheaders['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
            response = requests.get(url = self.onboardingurl, headers = self.onboardingheaders, params = self.onboardingparams)
            status_code = response.status_code
            match status_code:
                case 200:
                    print('Status Code: Ok... Grabbing Ticket Numbers and IDs....')
                    jsondata = response.json()
                    for ticket in jsondata.get('data',[]):
                        ticket_id = ticket.get('id')
                        ticket_number = ticket.get('ticketNumber')
                        self.ticketIds.append(ticket_id)
                        self.ticketnumbers.append(ticket_number)
                        self.ticketidsiter.append(ticket_id)
                case 201:
                    print('Status Code: Created')
                case 204:
                    print('Status Code: No content')
                case 400:
                    print('Status Code: Bad request')
                case 401:
                    print('Status Code: Unauthorized... Grabbing a new token... ')
                    scope = {'scope':'Desk.tickets.READ'}
                    instance_a = TokenManagerTest(scope)
                    instance_a.call_new_access_token()
                    print("Renewed token, Now grabbing Ticket numbers and IDs....")
                    self.getopentickets()
                case 403:
                    print('Status Code: Forbidden (Unauthorised access)')
                case 404:
                    print('Status Code: URL not found')
                case 405:
                    print('Status Code: Method not allowed (Method called is not supported for the API invoked)')
                case 413:
                    print('Status Code: Payload Too Large')
                case 415:
                    print('Status Code: Unsupported Media Type')
                case 422:
                    print('Status Code: Unprocessable Entity')
                case 429:
                    print('Status Code: Too Many Requests')
                case 500:
                    print('Status Code: Internal error')
        except requests.exceptions.ConnectionError:
            print("No internet available at the moment please try again later.")


    def GetOnboardticketContent(self):
        startofcontenturl = "https://desk.zoho.com/api/v1/tickets/"
        endofcontenturl = "/latestThread"
        with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Read', 'r') as file:
                access_token_str = file.read()
        self.onboardingheaders['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
        for ticketid in self.ticketIds:
            
            contenturl = f"{startofcontenturl}{ticketid}{endofcontenturl}"
            response = requests.get(contenturl, headers=self.onboardingheaders)
            content_status_code = response.status_code
            match content_status_code:
                case 200:
                    print('Status Code: Ok... Grabbing Ticket Content....')
                    self.jsoncontent = json.loads(response.text)
                    self.preponboarddata()
                case 201:
                    print('Status Code: Created')
                case 204:
                    print('Status Code: No content')
                case 400:
                    print('Status Code: Bad request')
                case 401:
                    print('Status Code: Unauthorized... Grabbing a new token...')
                    instance_d = TokenManagerTest({'scope':'Desk.tickets.READ'})
                    instance_d.call_new_access_token()
                    self.GetOnboardticketContent()
                case 403:
                    print('Status Code: Forbidden (Unauthorised access)')
                case 404:
                    print('Status Code: URL not found')
                case 405:
                    print('Status Code: Method not allowed (Method called is not supported for the API invoked)')
                case 413:
                    print('Status Code: Payload Too Large')
                case 415:
                    print('Status Code: Unsupported Media Type')
                case 422:
                    print('Status Code: Unprocessable Entity')
                case 429:
                    print('Status Code: Too Many Requests')
                case 500:
                    print('Status Code: Internal error')
                case _:
                    print('Something Went wrong')


    def preponboarddata(self):
        """"""
        z = self.ticketnumbers.pop(0)
        y = self.ticketidsiter.pop(0)
        
        all_data = []

        a = self.jsoncontent['content']
        text=json.dumps(a, sort_keys=True, indent=4)
        soup = BeautifulSoup(text, 'html.parser')
        text_content = re.sub(r'<.*?>', '', soup.get_text(separator='\n'))       
        all_text_pattern = re.compile(r'Contact Info:(.*?)Notes:', re.DOTALL)
        all_text_match = re.search(all_text_pattern, text_content)
        if all_text_match:
            str = (f"{all_text_match.group(1).strip()}")
            lines = str.split('\n')          
            data_dict = {'Ticket Number': z, 'Ticket ID': y}  # Create a new data_dict for each ticket number           
            for line in lines:
                parts = line.split(':')
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ''                         
                data_dict[key] = value
            all_data.append(data_dict)

            try:
                with open("C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/OpenOnboardsData.json", 'r') as existing_file:
                    existing_data = json.load(existing_file)
            except FileNotFoundError:
                existing_data = []

        # Append new data to the existing content
            existing_data.extend(all_data)

        # Write the combined data back to the file
            with open("C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/OpenOnboardsData.json", 'w') as f:
                json.dump(existing_data, f, indent=4)
            
                

        
ticket = ManageOnboardingTicketsTest()
ticket.getopentickets()
ticket.GetOnboardticketContent()





