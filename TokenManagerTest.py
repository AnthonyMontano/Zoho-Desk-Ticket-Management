import json
from dotenv import load_dotenv
import requests

if __name__ == "__main__":
    print("This class is not meant to be ran directly")
else:
    with open(
        "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/ZohoConfigFileTest.json",
        "r",
    ) as file:
        config_data = json.load(file)

    read_access_token_url = config_data["read_access_token_url"]
    read_access_token_params = config_data["read_access_token_params"]
    update_access_token_url = config_data["update_access_token_url"]
    update_access_token_params = config_data["update_access_token_params"]

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
                case {"scope": "Desk.tickets.READ"}:
                    self.read_access_token_params.update(self.scope)
                    response = requests.post(
                        self.read_access_token_url, self.read_access_token_params
                    )
                    statuscode = response.status_code
                    jsondata = response.json()
                    match statuscode:
                        case 200:
                            print("Status Code: OK")
                            access_token_read = jsondata["access_token"]
                            """Storing token in a text file so it can be retrieved from other class for an hour"""
                            with open(
                                "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Read",
                                "w"
                            ) as access_token_text_read:
                                access_token_text_read.write(access_token_read)
                        case 201:
                            print("Status Code: Created")
                        case 400:
                            print("Status Code: Bad request")
                        case 401:
                            print("Status Code: Unauthorized")
                        case 403:
                            print("Status Code: Forbidden (Unauthorised access)")
                        case _:
                            print("Refer to API codes in zoho docs")
                case {"scope": "Desk.tickets.UPDATE"}:
                    self.update_access_token_params.update(self.scope)
                    response = requests.post(
                        self.update_access_token_url, self.update_access_token_params
                    )
                    statuscode = response.status_code
                    print(statuscode)
                    jsondata = response.json()
                    match statuscode:
                        case 200:
                            print("Status Code: OK")
                            access_token_update = jsondata["access_token"]
                            print(access_token_update)
                            """Storing token in a text file so it can be retrieved from other class for an hour"""
                            with open(
                                "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Update",
                                "w",
                            ) as access_token_text_update:
                                access_token_text_update.write(access_token_update)
                        case 201:
                            print("Status Code: Created")
                        case 400:
                            print("Status Code: Bad request")
                        case 401:
                            print("Status Code: Unauthorized")
                        case 403:
                            print("Status Code: Forbidden (Unauthorised access)")
                        case _:
                            print("Status Code: Internal error")
                case {"scope": "Desk.tickets.ALL"}:
                    self.read_access_token_params.update(self.scope)
                    response = requests.post(
                        self.read_access_token_url, self.read_access_token_params
                    )
                    statuscode = response.status_code
                    jsondata = response.json()
                    match statuscode:
                        case 200:
                            print("Status Code: OK")
                            access_token_all = jsondata["access_token"]
                            """Storing token in a text file so it can be retrieved from other class for an hour"""
                            with open(
                                "Access_Token_Text_All", "w"
                            ) as access_token_text_all:
                                access_token_text_all.write(access_token_all)
                        case 201:
                            print("Status Code: Created")
                        case 400:
                            print("Status Code: Bad request")
                        case 401:
                            print("Status Code: Unauthorized")
                        case 403:
                            print("Status Code: Forbidden (Unauthorised access)")
                        case _:
                            print("Refer to API codes in zoho docs")
                case _:
                    print("Logic for this scope hasnt been set up")

        def call_refresh_token(self):
            print("Refresh token method is a work in progress")

        def revoke_token(self):
            print("Revoke token method is a work in progress")
