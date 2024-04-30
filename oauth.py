from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from googleapiclient.http import MediaFileUpload


# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_gdrive():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_file_to_drive(filename, filepath, folder_id):
    creds = authenticate_gdrive()
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(filepath, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID: %s' % file.get('id'))



def oauth_and_upload(folder_id,image_folder_path):
    for filename in os.listdir(image_folder_path):
        if filename.endswith('.jpg'):
            upload_file_to_drive(filename, os.path.join(image_folder_path, filename), folder_id)

#folder_id = '126bk1h19PGTUVov2qz17ywff1Ld1OPH_'  # Make sure to replace this with your actual folder ID
#image_folder_path = 'cat_images'
#oauth_and_upload(folder_id,image_folder_path)