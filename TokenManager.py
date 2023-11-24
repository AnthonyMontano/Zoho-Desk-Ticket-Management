import requests
import token

class TokenManager:

    def __init__(self):
        """Assigning the variables for my API calls"""
        self.url = "Enter Site Here"
        self.access_token_params = {'refresh_token':'Enter Token Here',
                        'grant_type':'refresh_token','client_id': 'Enter ID here',
                         'client_secret':'Enter Secret here'}
        

    def call_new_access_token(self):
        """Call to autostore token if OK is received"""
        """Need to implement switch statement to go through the codes"""
        response = requests.post(self.url, self.access_token_params)
        statuscode = response.status_code
        jsondata = response.json()
        match statuscode:
            case 200:
                print('Status Code: OK')          
                print(jsondata['access_token'])
                access_token = jsondata['access_token']
                """Storing token in a text file so it can be retrieved from other class for an hour"""
                with open("Access_Token_Text", "w") as access_token_text:
                    access_token_text.write(access_token)
                #access_token_text = open("Access_Token_Text", "w")
                #access_token_text.write(access_token)  
                #access_token_text.close()                      
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
        
    """Has no use if the goal is to automate the entire process"""
    def retrieve_scope(self):
        x = input("Please enter number correlating to the scope you wish for the token to have:\n1. All\n2. Read\n3. Write\n4. Create\n5. Update\n")
        match x:
            case '1':
                self.scope = 'Desk.tickets.ALL'
            case '2':
                self.scope = 'Desk.tickets.READ'
            case '3':
                self.scope = 'Desk.tickets.WRITE'
            case '4':
                self.scope = 'Desk.tickets.CREATE'
            case '5':
                self.scope = 'Desk.tickets.UPDATE'
            case _:
                print('Invalid input.')
        self.access_token_params['scope'] = self.scope


    def call_refresh_token(self):
        print("Called Refresh_token")


    def revoke_token(self):
        print("Token revoked")
