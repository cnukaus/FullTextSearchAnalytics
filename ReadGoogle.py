from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import httplib2

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def ReadGoogle(ID,sheetname='Sheet1'):
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Google Sheets API Python Quickstart'
	rangepass=sheetname+"!A1:B"#for row in rows:
	#	search("https://explorer.xdag.io/block/"+row)
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
	                'version=v4')
	service = discovery.build('sheets', 'v4', http=http,
	                          discoveryServiceUrl=discoveryUrl)

	spreadsheetId = ID
	rangeName = rangepass#'Class Data!A2:E'
	result = service.spreadsheets().values().get(
	    spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])

	if not values:
	 	print('No data found.')
	else:
		for row in values:
			pass#print(row)
	#print (values[0][0:3]) 
	return ([values[i][0] for i in range(len(values)) if i!=0])