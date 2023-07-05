from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_dataset(folder_id):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        results = service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return []

        dataset = []

        for item in items:
            name = item['name']
            file_id = item['id']
            mime_type = item['mimeType']

            if mime_type == 'application/vnd.google-apps.folder':
                dataset.append({'type': 'folder', 'name': name, 'id': file_id})
                subfolder_dataset = get_dataset(file_id)
                dataset.extend(subfolder_dataset)
            else:
                dataset.append({'type': 'file', 'name': name, 'id': file_id, 'content': None})
                # Retrieve the content of the file
                request = service.files().get_media(fileId=file_id)
                content = request.execute()
                dataset[-1]['content'] = content  # Update the 'content' field of the latest file

        return dataset

    except HttpError as error:
        print(f'An error occurred: {error}')
        return []


