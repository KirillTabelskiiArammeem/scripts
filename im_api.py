import requests
'http://192.168.98.11/appsrvtest01/#/swagger-ui'
class ApiClient:

    base_url = 'http://192.168.98.11/appsrvtest01/'

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session_id = None

    def call(self, http_method: str, api_method: str, json: dict=None, cookies=None):
        response = requests.request(http_method, f'{self.base_url}{api_method}', json=json, cookies=cookies)
        return response

    def get_auth_modules(self):
        return self.call('GET', 'authmodules').json()

    def get_auth_module(self, module_id: str):
        return self.call('GET', f'authmodules/{module_id}').json()

    def get_auth_modules_full(self):
        for module in self.get_auth_modules():
            yield self.get_auth_module(module['id'])

    def login(self, auth_module_id):
        print(f"Module={auth_module_id};User={self.username};Password={self.password}")
        response = requests.request('POST', 'http://192.168.98.11/appsrvtest01/auth/apphost/',
                                    json={"authString":f"Module={auth_module_id};User={self.username};Password={self.password}"}).json()
        self.session_id = response['sessionId']


    def get_person(self):
        response = self.call('GET', 'api/entities/UNSAccountB', cookies={'ss-id': self.session_id})
        print(response.url)
        print(response.status_code)
        print(response.text)

#[{'id': 'RoleBasedPerson', 'caption': 'Employee (role based)', 'authTemplate': 'Module=RoleBasedPerson;User[VI.DB_USER];(Password)Password[VI.DB_Password];(NewPassword)NewPassword[VI.DB_NewPassword]', 'passwordBased': True, 'isDefault': False}]

api = ApiClient(username='oi', password='')
# for module in api.get_auth_modules_full():
#     print(module)
api.login('RoleBasedPerson')


tables = ['ADSAccount', 'ADSContact', 'EX0MailUser', 'EX0MailContact', 'EX0Mailbox', 'SPSUser', 'O3SUser', 'NotesUser',

          'SAPUser', 'SAPBWUser', 'SAPUserMandant', 'LDAPAccount', 'UNSAccountB', 'UNXAccount', 'AADUser',
          'O3EMailbox', 'O3EMailContact', 'O3EMailUser', 'GAPUser', 'CSMUser', 'EBSUser', 'PAGUser'
          ]

print(tables)
resp = api.call('GET', f'api/entities/person', cookies={'ss-id': api.session_id})
print(resp.url)
print(resp.json())
# for table in tables:
#     resp = api.call('GET', f'api/entities/{table}', cookies={'ss-id': api.session_id})
#     print(resp.url)
#     print(resp.json())
#
