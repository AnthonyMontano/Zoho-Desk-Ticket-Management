from TokenManager import TokenManager
import requests
import re
import json
from bs4 import BeautifulSoup

"""The Purpose of this class it to access Onboarding ticket data and store it in a understandable way for comprehension and future scripting """
"""Need to implement a method or class that makes changes to the tickets such as changing the status to in progress"""
class ManageOnboardingTickets:

    def __init__(self):
        self.url = "https://desk.zoho.com/api/v1/tickets"
        self.headers = {"orgId":"EnterOrgID"}
        self.params = {'departmentIds': 'EnterDepartmentId', 'status':'enterticketstatushere'}
        self.ticketdata = ""
        self.ticketIds = []
        self.jsoncontent = ""
        self.jsonstring = ""
        self.content = ""
    

    def getopentickets(self):
        try:
            with open('Access_Token_Text', 'r') as file:
                access_token_str = file.read()
            self.headers['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
            response = requests.get(url = self.url, headers = self.headers, params = self.params)
            status_code = response.status_code
            match status_code:
                case 200:
                    print('Status Code: Ok... Grabbing Ticket Numbers and IDs....')
                    jsondata = response.json()
                    for ticket in jsondata.get('data',[]):
                        ticket_id = ticket.get('id')
                        ticket__number = ticket.get('ticketNumber')
                        self.ticketIds.append(ticket_id)
                        self.ticketdata += f"Ticket Number: {ticket__number}\nTicket ID: {ticket_id}\n\n"
                case 201:
                    print('Status Code: Created')
                case 204:
                    print('Status Code: No content')
                case 400:
                    print('Status Code: Bad request')
                case 401:
                    print('Status Code: Unauthorized... Grabbing a new token... ')
                    instance_a = TokenManager()
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
            print("The internet is not accessible at the moment please try again later.")


    def GetOnboardticketContent(self):
        startofcontenturl = "https://desk.zoho.com/api/v1/tickets/"
        endofcontenturl = "/latestThread"
        with open('Enter File Here', 'r') as file:
                access_token_str = file.read()
        #
        # access_token_str = open('Access_Token_Text', 'r').read()
        self.headers['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
        for ticketid in self.ticketIds:
            contenturl = f"{startofcontenturl}{ticketid}{endofcontenturl}"
            response = requests.get(contenturl, headers=self.headers)
            content_status_code = response.status_code
            match content_status_code:
                case 200:
                    print('Status Code: Ok... Grabbing Ticket Content....')
                    self.jsoncontent = json.loads(response.text)
                    ticket.PrepData()
                case 201:
                    print('Status Code: Created')
                case 204:
                    print('Status Code: No content')
                case 400:
                    print('Status Code: Bad request')
                case 401:
                    print('Status Code: Unauthorized... Grabbing a new token...')
                    instance_d = TokenManager()
                    instance_d.call_new_access_token()
                    ticket.GetOnboardticketContent()
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


    def PrepData(self):
        """Need to go back and really learn REGEX as this is a pivotal part to the process. This part took the longest to research for me"""
        a = self.jsoncontent['content']
        text=json.dumps(a, sort_keys=True, indent=4)
        soup = BeautifulSoup(text, 'html.parser')
        text_content = re.sub(r'<.*?>', '', soup.get_text(separator='\n'))       
        contact_info_pattern = re.compile(r'Contact Info:(.*?)IT Equipment:', re.DOTALL)
        supervisor_info_pattern = re.compile(r'Supervisor:(.*?)Location Info:', re.DOTALL)
        location_info_pattern = re.compile(r'Location Info:(.*?)Recorded Date:', re.DOTALL)
        recorded_date_pattern = re.compile(r'Recorded Date:(.*?)Notes:', re.DOTALL)
        contact_info_match = re.search(contact_info_pattern, text_content)
        supervisor_info_match = re.search(supervisor_info_pattern, text_content)
        location_info_match = re.search(location_info_pattern, text_content)
        recorded_date_match = re.search(recorded_date_pattern, text_content)    
        str = (f"{contact_info_match.group(1).strip()}\n{supervisor_info_match.group(1).strip()}\n{location_info_match.group(1).strip()}\nEntry Date:{recorded_date_match.group(1).strip()}")
        lines = str.split('\n')
        data_dict = {}
        for line in lines:
            parts = line.split(':')
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else '' 
            data_dict[key] = value
        with open("Enter File Here", 'a') as f:  
            for key, value in data_dict.items():  
                f.write('%s:%s\n' % (key, value))
            f.write('\n')
        
ticket = ManageOnboardingTickets()
ticket.getopentickets()
ticket.GetOnboardticketContent()