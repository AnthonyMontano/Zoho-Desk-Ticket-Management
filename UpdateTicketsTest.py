from TokenManagerTest import TokenManagerTest
import requests
import re
import json
from bs4 import BeautifulSoup




with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/ZohoConfigFileTest.json' ,'r') as file:
    config_data = json.load(file)
update_access_token_params = config_data['update_access_token_params']

"""The purpose of this class it to make changes to tickets in Zoho currently will be focused on changing status of tickets from new to in progess"""
class UpdateTickets:
        
        def __init__(self):
            self.ticket_ids = []
            self.url = "https://desk.zoho.com/api/v1/tickets"
            self.headers = {"orgId":"669421986"}
            self.access_token_params_Update = update_access_token_params
            self.ticketsIds = []
            self.data = {'language' : 'Spanish'}

        def getticketIds(self):
            
            with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json', "r") as f:
                 data_list = json.load(f)
            ticket_ids = []
            x =[]
            for data_dict in data_list:
                ticket_id = data_dict.get('Ticket ID')
                if ticket_id:
                    ticket_ids.append(ticket_id)
                    self.ticketsIds.append(ticket_id)
            

        def change_ticket_id_status(self):
            startofcontenturl = "https://desk.zoho.com/api/v1/tickets/"
            endofcontenturl = ""
            index_to_modify = 0
            try:
                with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Update', 'r') as file:
                    access_token_str = file.read()
                self.headers['Authorization'] = f"Zoho-oauthtoken {access_token_str}"
                for ticketid in self.ticketsIds:
                    new_key, new_value = next(iter(self.data.items()))  
                    contenturl = f"{startofcontenturl}{ticketid}"
                    response = requests.patch(url = contenturl, data= json.dumps(self.data), headers = self.headers)
                    with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json', 'r') as f:
                        existing_data = json.load(f)
                    existing_data[index_to_modify][new_key]=new_value
                    status_code = response.status_code
                    match status_code:
                        case 200:
                            print(f'Status Code: Ok... Changing ticket status {new_key} to {new_value}....')
                            self.timestamp_and_create_comment(ticketid)
                            data = response.json()
                            print(data)
                            ticket_status = data["statusType"]
                            print(ticket_status)
                            with open('C:/Users/Anthony/Zoho/Scripts/Cloned-Repo/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json', 'w') as f:
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
                            self.change_ticket_id_status()
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
        
        def timestamp_and_create_comment(self,ticketid):
            comment_url_start = "https://desk.zoho.com/api/v1/tickets/"
            create_comment_url_middle = ticketid
            print(ticketid)
            endofcontenturl = "/comments"
            create_comment_url = f'{comment_url_start}{create_comment_url_middle}{endofcontenturl}'
            print(create_comment_url)
            create_comment_timestamp_data = {"isPublic" : 'true', "contentType": 'html', 'content' : 'Please ignore this message this is for testing purposes:\nScript 1 has pulled this tickets data and the ticket has been set to In Progress'}
            try:
                response = requests.post(url = create_comment_url, data= json.dumps(create_comment_timestamp_data), headers = self.headers)
                status_code = response.status_code
                match status_code:
                    case 200:
                        print('Status Code: OK')        
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
                        print("Renewed token, Updating tickets with comments....")
                        
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
instance_a.change_ticket_id_status()
