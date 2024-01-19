from TokenManagerTest import TokenManagerTest
import requests
import re
import json
from bs4 import BeautifulSoup
"""Show this as new version in Github"""
"""The purpose of this class is to access offboarding ticket data and store it for furture scripting"""
class ManageOffboardingTickets:

    def __init__(self):
        self.url = "https://desk.zoho.com/api/v1/tickets"
        self.headers = {"orgId":"669421986"}
        self.params = {'departmentIds': '279921000042815136', 'status':'open'}
        self.ticketdata = ""
        self.ticketIds = []
        self.jsoncontent = ""
        self.jsonstring = ""
        self.content = ""


    def getopenoffboardtickets(self):
            try:
                with open('Access_Token_Text_Read', 'r') as file:
                    access_token_str = file.read()
                #access_token_str = open('Access_Token_Text', 'r').read()
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
                        instance_a = TokenManagerTest({'scope':'Desk.tickets.READ'})
                        instance_a.call_new_access_token()
                        print("Renewed token, Now grabbing Ticket numbers and IDs....")
                        self.getopenoffboardtickets()
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


    def getopenoffboardticketcontent(self):
        startofcontenturl = "https://desk.zoho.com/api/v1/tickets/"
        endofcontenturl = "/latestThread"
        with open('Access_Token_Text_Read', 'r') as file:
                access_token_str = file.read()
        self.headers['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
        for ticketid in self.ticketIds:
            contenturl = f"{startofcontenturl}{ticketid}{endofcontenturl}"
            response = requests.get(contenturl, headers=self.headers)
            content_status_code = response.status_code
            match content_status_code:
                case 200:
                    print('Status Code: Ok... Grabbing Ticket Content....')
                    self.jsoncontent = json.loads(response.text)
                    ticket.prepoffboarddata()
                case 201:
                    print('Status Code: Created')
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


    def prepoffboarddata(self):
        """"""
        a = self.jsoncontent['content']
        text=json.dumps(a, sort_keys=True, indent=4)
        soup = BeautifulSoup(text, 'html.parser')
        text_content = re.sub(r'<.*?>', '', soup.get_text(separator='\n'))
        
        all_text_pattern = re.compile(r'Employee Name:(.*?)Completed By:', re.DOTALL)
        print(all_text_pattern)
        all_text_match = re.search(all_text_pattern, text_content)
        if all_text_match:
            str = (f"{all_text_match.group(1).strip()}")
            lines = str.split('\n')
            data_dict = {}
            for line in lines:
                parts = line.split(':')
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else '' 
                data_dict[key] = value
            with open("offboarding.json", 'a') as f: 
                for key, value in data_dict.items(): 
                    f.write('%s:%s\n' % (key, value))
                f.write('\n')
        else:
            "Ticket doesnt seem to be in the smartsheet format needed."


ticket = ManageOffboardingTickets()
ticket.getopenoffboardtickets()
ticket.getopenoffboardticketcontent()
        