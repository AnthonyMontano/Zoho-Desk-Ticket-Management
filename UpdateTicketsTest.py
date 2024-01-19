 from TokenManagerTest import TokenManagerTest
import requests
import re
import json
from bs4 import BeautifulSoup



"""The purpose of this class it to make changes to tickets in Zoho currently will be focused on changing status of tickets from new to in progess"""
class UpdateTickets:
        
        def __init__(self):
            self.ticket_ids = []
            self.url = "https://desk.zoho.com/api/v1/tickets"
            self.headers = {"orgId":"669421986"}
            self.access_token_params_Update = {'refresh_token': '1000.7047d081dfd4c30a41034db67f89c06a.1ed70f96f0197980c40e5bcdca52e872', 'grant_type': 'authorization_code', 'client_id': '1000.NJ04COKSQRRZDDBS1KBB4058OT8VLQ',
                           'client_secret':'595a91832356b66773fbb41b364f67b9c3d1c4eb09'}
            self.ticketsIds = []
            self.data = {'language' : 'English'}

        def getticketIds(self):
            """response = requests.post(url = self.url, params = self.params)
            statuscode = response.status_code
            jsondata = response.json()
            print(statuscode)
            print(jsondata)"""
            with open('OnboardingData1.json', "r") as f:
                 data_list = json.load(f)
            ticket_ids = []
            x =[]
            for data_dict in data_list:
                ticket_id = data_dict.get('Ticket ID')
                if ticket_id:
                    ticket_ids.append(ticket_id)
                    self.ticketsIds.append(ticket_id)
            

        def setticketIdsinprogress(self):
            startofcontenturl = "https://desk.zoho.com/api/v1/tickets/"
            endofcontenturl = ""
            index_to_modify = 0
            try:
                with open('Access_Token_Text_Update', 'r') as file:
                    access_token_str = file.read()
                self.headers['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
                for ticketid in self.ticketsIds:
                    contenturl = f"{startofcontenturl}{ticketid}"
                    response = requests.patch(url = contenturl, data= json.dumps(self.data), headers = self.headers)
                    new_key = "status"
                    new_value = "In Progress"
                    with open('OnboardingData1.json', 'r') as f:
                        existing_data = json.load(f)
                    existing_data[index_to_modify][new_key]=new_value
                    status_code = response.status_code
                    match status_code:
                        case 200:
                            print('Status Code: Ok... Updating Ticket IDs....')
                            data = response.json()
                            ticket_status = data["statusType"]
                            print(ticket_status)
                            with open('OnboardingData1.json', 'w') as f:
                                json.dump(existing_data, f, indent=4)
                            index_to_modify +=1
                        case 201:
                            print('Status Code: Created')
                        case 204:
                            print('Status Code: No content')
                        case 400:
                            print('Status Code: Bad request')
                        case 401:
                            print('Status Code: Unauthorized... Grabbing a new token... ')
                            instance_d = TokenManagerTest({'scope':'Desk.tickets.UPDATE'})
                            instance_d.call_new_access_token()
                            print("Renewed token, Now grabbing Ticket numbers and IDs....")
                            self.setticketIdsinprogress()
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
        
instance_a = UpdateTickets()
instance_a.getticketIds()
instance_a.setticketIdsinprogress()
