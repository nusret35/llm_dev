import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to the credentials JSON file
credentials_path = '/Users/nusretkizilaslan/Desktop/AIProject/llm_dev/starry-iris-391817-5556af7501b1.json'

# Initialize the Drive service
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=credentials)

# Function to upload image
def upload_image(image_path, folder_id=None):
    file_metadata = {
        'name': os.path.basename(image_path)
    }
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(image_path, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, supportsAllDrives=True, fields='id').execute()
    file_id = file.get('id')

    # Define the permission body
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    # Add the permission to the file
    drive_service.permissions().create(fileId=file_id, body=permission).execute()
    return f"https://drive.google.com/uc?id={file_id}"

# Function to list all files in Google Drive
def list_files():
    results = drive_service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

