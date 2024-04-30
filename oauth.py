from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from googleapiclient.http import MediaFileUpload
from auxiliars import convert_to_valid_folder_name

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

def upload_file_to_drive(filename, filepath, folder_destination_id,creds):
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': filename,
        'parents': [folder_destination_id]
    }
    media = MediaFileUpload(filepath, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID: %s' % file.get('id'))

def create_new_folder_and_get_id(drive_new_folder_name,creds):
    service = build('drive', 'v3', credentials=creds)
    # Crea la metadata para la nueva carpeta
    folder_metadata = {
        'name': drive_new_folder_name,#NEW FOLDER NAME
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ["126bk1h19PGTUVov2qz17ywff1Ld1OPH_"]#PARETN FOLDER ID
    }

    # Crea la carpeta
    folder = service.files().create(body=folder_metadata, fields='id').execute()

    # Obtiene el ID de la carpeta creada
    new_folder_id = folder.get('id')
    return new_folder_id


def upload_drive_folder(local_images_folder_path,id_folder_drive_to_upload,creds):
    
    
    for filename in os.listdir(local_images_folder_path):
        if filename.endswith('.jpg'):
            upload_file_to_drive(filename, os.path.join(local_images_folder_path, filename), id_folder_drive_to_upload,creds)
    return id_folder_drive_to_upload

# Example usage
#search_query = "nubes"
#local_images_folder_path = convert_to_valid_folder_name(search_query)
#creds = authenticate_gdrive()
#id_folder_drive_to_upload = create_new_folder_and_get_id(local_images_folder_path,creds)
#upload_drive_folder(local_images_folder_path,id_folder_drive_to_upload,creds)