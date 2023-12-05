import requests
from dotenv import load_dotenv
import json

if __name__ == '__main__':
    print('This class is not meant to be ran directly')
else:

    with open('OnboardingConfigFileTest.json' ,'r') as file:
        config_data = json.load(file)

    read_access_token_url = config_data['read_access_token_url']
    read_access_token_params = config_data['read_access_token_params']
    update_access_token_url = config_data['update_access_token_url']
    update_access_token_params = config_data['update_access_token_params']

    class TokenManagerTest:

        def __init__(self, scope):
            """Assigning the variables for my API calls"""
            self.read_access_token_url = read_access_token_url
            self.read_access_token_params = read_access_token_params
            self.update_access_token_url = update_access_token_url
            self.update_access_token_params = update_access_token_params
            self.scope = scope
            
        
        def call_new_access_token(self):
            """Call to autostore token if OK is received"""
            """Need to implement switch statement to go through the codes"""
            match self.scope:
                case {'scope': 'Desk.tickets.READ'}:
                    self.read_access_token_params.update(self.scope)
                    response = requests.post(self.read_access_token_url, self.read_access_token_params)
                    statuscode = response.status_code
                    jsondata = response.json()
                    match statuscode:
                        case 200:
                            
                            print('Status Code: OK')
                            access_token_read = jsondata['access_token']
                            """Storing token in a text file so it can be retrieved from other class for an hour"""
                            with open("Access_Token_Text_Read", "w") as access_token_text_read:
                                access_token_text_read.write(access_token_read)
                        case 201:
                            print('Status Code: Created')
                        case 204:
                            print('Status Code: No content')
                        case 400:
                            print('Status Code: Bad request')
                        case 401:
                            print('Status Code: Unauthorized')
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
                case {'scope': 'Desk.tickets.UPDATE'}:
                    self.update_access_token_params.update(self.scope)
                    response = requests.post(self.update_access_token_url, self.update_access_token_params)
                    statuscode = response.status_code
                    jsondata = response.json()
                    match statuscode:
                        case 200:
                            print('Status Code: OK')
                            access_token_update = jsondata['access_token']
                            """Storing token in a text file so it can be retrieved from other class for an hour"""
                            with open("Access_Token_Text_Update", "w") as access_token_text_update:
                                access_token_text_update.write(access_token_update)
                        case 201:
                            print('Status Code: Created')
                        case 204:
                            print('Status Code: No content')
                        case 400:
                            print('Status Code: Bad request')
                        case 401:
                            print('Status Code: Unauthorized')
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
                case {'scope' : 'Desk.tickets.ALL'}:
                    self.read_access_token_params.update(self.scope)
                    response = requests.post(self.read_access_token_url, self.read_access_token_params)
                    statuscode = response.status_code
                    jsondata = response.json()
                    match statuscode:
                        case 200:
                            print('Status Code: OK')
                            access_token_all = jsondata['access_token']
                            """Storing token in a text file so it can be retrieved from other class for an hour"""
                            with open("Access_Token_Text_All", "w") as access_token_text_all:
                                access_token_text_all.write(access_token_all)
                        case 201:
                            print('Status Code: Created')
                        case 204:
                            print('Status Code: No content')
                        case 400:
                            print('Status Code: Bad request')
                        case 401:
                            print('Status Code: Unauthorized')
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
                    print("Logic for this scope hasnt been set up")


        def call_refresh_token(self):
            print("Refresh token method is a work in progress")


        def revoke_token(self):
            print("Revoke token method is a work in progress")

