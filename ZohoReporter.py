import json
import requests
from TokenManagerTest import TokenManagerTest

if __name__ == "__main__":
    print("This class is not meant to be run directly")
else:
    with open(
        "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/ZohoConfigFileTest.json",'r'
    ) as file:
        config_data = json.load(file)
    update_access_token_params = config_data["update_access_token_params"]
    apiheaders = config_data["apiheaders"]

    """The purpose of this class it to make changes to tickets in Zoho currently will be focused on changing status of tickets from new to in progess"""

    class ZohoReporter:
        def __init__(self):
            self.ticket_ids = []
            self.url = "https://desk.zoho.com/api/v1/tickets"
            self.headers = apiheaders
            self.access_token_params_Update = update_access_token_params
            self.ticketsIds = []
            self.data = None
            self.count = 0
            

        def getticketIds(self):
            try:
                with open("C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json","r"
                ) as f:
                    data_list = json.load(f)
            except FileNotFoundError:
                print("STOP")
            ticket_ids = []
            x = []
            for data_dict in data_list:
                ticket_id = data_dict.get("Ticket ID")
                if ticket_id:
                    ticket_ids.append(ticket_id)
                    self.ticketsIds.append(ticket_id)
            print("done grabbing ticket ids")

        def set_status(self):
            try:
                startofcontenturl = "https://desk.zoho.com/api/v1/tickets/"
                with open("C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json", "r") as f:
                    existing_data = json.load(f)

                for entry in existing_data:
                    if entry.get("Employee Email") == "":
                        self.data = {"status": "Closed"}
                    elif entry.get("5th Script") == 11111:
                        self.data = {"status": "Closed"}
                    else:
                        self.data = {"status" : "In Progress"}
                    ticketid = entry.get("Ticket ID")
                    with open(
                        "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Update",
                        "r"
                    ) as file:
                        access_token_str = file.read()
                    self.headers["Authorization"] = f"Zoho-oauthtoken {access_token_str}"
                    new_key, new_value = next(iter(self.data.items()))
                    contenturl = f"{startofcontenturl}{ticketid}"
                    response = requests.patch(
                        url=contenturl, data=json.dumps(self.data), headers=self.headers
                    )
                    status_code = response.status_code
                    match status_code:
                        case 200:
                            print(f"Status Code: Ok... Changing ticket status {new_key} to {new_value}....")
                        case 201:
                            print("Status Code: Created")
                        case 400:
                            print("Status Code: Bad request")
                        case 401:
                            print(
                                "Status Code: Unauthorized... Grabbing a new token... "
                            )
                            instance_d = TokenManagerTest(
                                {"scope": "Desk.tickets.UPDATE"}
                            )
                            instance_d.call_new_access_token()
                            print(
                                "Renewed token, Now grabbing Ticket numbers and IDs...."
                            )
                            self.set_status()
                        case 403:
                            print("Status Code: Forbidden (Unauthorised access)")
                        case _:
                            print("Please refer to Zoho Desk API docomentation")
            except requests.exceptions.ConnectionError:
                print("No internet available at the moment please try again later.")
                
        def update_no_email_ticket_data(self):
            try:
                with open("C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json", "r") as f:
                    existing_data = json.load(f)

                for entry in existing_data:
                    if entry.get("Employee Email") == "":
                        # Update the desired values for entries with empty "Employee email"
                        entry["1st Script"] = 100
                        entry["2nd Script"] = 100
                        entry["3rd Script"] = 100
                        entry["4th Script"] = 100
                        entry["5th Script"] = 100
                        
                        # Add more fields to update as needed

                with open("C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json", "w") as f:
                    json.dump(existing_data, f, indent=4)
                
                print("Updated values for entries with empty Employee email.")

            except FileNotFoundError:
                print("JSON file not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON file.")
            except Exception as e:
                print(f"An error occurred: {e}")
                
        def report_and_timestamp(self):
            
            script1_timestamp = {
                "isPublic": "true",
                "contentType": "html",
                "content": "Please ignore this message this is for testing purposes:%0AScript 1 has pulled this tickets data and the ticket has been set to In Progress",
            }
            script2_timestamp = {
                "isPublic": "true",
                "contentType": "html",
                "content": "Please ignore this message this is for testing purposes:\nScript 2 has scheduled the offboarding tickets to run at the requested times",
            }
            script3_timestamp = {
                "isPublic": "true",
                "contentType": "html",
                "content": "Please ignore this message this is for testing purposes:Script 3 has ran portions of the offboard",
            }
            script4_timestamp = {
                "isPublic": "true",
                "contentType": "html",
                "content": "Please ignore this message this is for testing purposes:Script 4 is notifying you to please back up the user in Datto and remove the license ones the data is backed up. Thank you for your assistance.",
            }
            script5_timestamp = {
                "isPublic": "true",
                "contentType": "html",
                "content": "Please ignore this message this is for testing purposes:Script 5 ",
            }
            script_no_email_timestamp = {
                "isPublic": "true",
                "contentType": "html",
                "content": "Please ignore this message this is for testing purposes:User had no email"
                
            }
            
            with open(
                "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json",
                "r"
            ) as existing_file1:
                existing_data1 = json.load(existing_file1)
                for ticketid in self.ticketsIds:
                    count =  ( existing_data1[self.count]["1st Script"]
                            + existing_data1[self.count]["2nd Script"]
                            + existing_data1[self.count]["3rd Script"]
                            + existing_data1[self.count]["4th Script"]
                            + existing_data1[self.count]["5th Script"])
                    
                
                
                    comment_url_start = "https://desk.zoho.com/api/v1/tickets/"
                    create_comment_url_middle = ticketid
                    endofcontenturl = "/comments"
                    create_comment_url = (
                        f"{comment_url_start}{create_comment_url_middle}{endofcontenturl}"
                    )
                    
                    try:
                        match count:
                            case 1:
                                data1 = json.dumps(script1_timestamp)
                            case 11:
                                data1 = json.dumps(script2_timestamp)
                            case 111:
                                data1 = json.dumps(script3_timestamp)    
                            case 1111:
                                data1 = json.dumps(script4_timestamp)
                            case 11111:
                                data1 = json.dumps(script5_timestamp)
                            case 500:
                                data1 = json.dumps(script_no_email_timestamp)
                        with open(
                            "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/Access_Token_Text_Update",
                            "r"
                        ) as file:
                            access_token_str = file.read()
                        self.headers["Authorization"] = f"Zoho-oauthtoken {access_token_str}"
                        
                        response = requests.post(
                            url=create_comment_url, data=data1, headers=self.headers
                        )
                        status_code = response.status_code
                        
                        match status_code:
                            case 200:
                                with open(
                                    "C:/Users/anthonym/Zoho/env/Scripts/Zoho-Desk-Ticket-Management/Config Files/OpenOffboardsData.json",
                                    "r"
                                ) as existing_file2:
                                    existing_data2 = json.load(existing_file2)
                                match count:
                                    case 1:
                                        existing_data2[self.count]["2nd Script"] = 10
                                        
                                    case 11:
                                        existing_data2[self.count]["3rd Script"] = 100
                                    
                                    case 111:
                                        existing_data2[self.count]["4th Script"] = 1000
                                        
                                    case 1111:
                                        existing_data2[self.count]["5th Script"] = 10000
                                        
                                    case 11111:
                                        print("nice")
                            case 201:
                                print("Status Code: Created")
                            case 400:
                                print("Status Code: Bad request")
                            case 401:
                                print("Status Code: Unauthorized... Grabbing a new token... ")
                                instance_z = TokenManagerTest({"scope": "Desk.tickets.UPDATE"})
                                instance_z.call_new_access_token()
                                self.report_and_timestamp
                                print("Renewed token, Updating tickets with comments....")
                            case 403:
                                print("Status Code: Forbidden (Unauthorised access)")
                            case _:
                                print("Refer to Zoho API codes")
                    except requests.exceptions.ConnectionError:
                        print("No internet available at the moment please try again later.")
                        
                        