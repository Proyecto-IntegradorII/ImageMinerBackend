from flask import Flask, jsonify
import threading
import time
from flask_cors import CORS
from flask import Flask, jsonify, request
import requests
from googleapiclient.discovery import build
from auxiliars import convert_to_valid_folder_name
from oauth import authenticate_gdrive, create_new_folder_and_get_id, upload_drive_folder
from scrapping import download_images_from_google

import os

app = Flask(__name__)
CORS(app)

def process_data():
    # Simulate data processing
    for i in range(5):
        time.sleep(5)
        print("Data processing iteration", i+1)

@app.route('/api', methods=['GET'])
def multi_thread_api():
    # Send an immediate response
    response_message = "Response sent. Continuing to process data..."
    response = jsonify({"message": response_message})
    response.status_code = 200
    
    # Start a new thread to process data asynchronously
    processing_thread = threading.Thread(target=process_data)
    processing_thread.start()
    
    return response

@app.route('/', methods=['GET'])
def welcome():
    # Send an immediate response
    response_message = "This is the welcome endpoint to image miner. Creating n-sized images datasets is now possible!"
    response = jsonify({"message": response_message})
    response.status_code = 200
   
    return response

@app.route('/web_scrapping', methods=['POST'])
def get_length():
    data = request.json
    query_string = data.get('query')
    number_of_images_int= data.get('number_of_images')
    search_query = query_string
    destination_folder = convert_to_valid_folder_name(search_query)
    number_of_images = int(number_of_images_int)
    download_images_from_google(search_query, destination_folder, number_of_images)#getting images
    local_images_folder_path = destination_folder
    creds = authenticate_gdrive()
    id_folder_drive_to_upload = create_new_folder_and_get_id(local_images_folder_path,creds)
    processing_thread = threading.Thread(target=upload_drive_folder,args=(local_images_folder_path,id_folder_drive_to_upload,creds))#uploading (preparing) images
    processing_thread.start()
    return jsonify({"folder_id": id_folder_drive_to_upload}), 200

@app.route('/count_files', methods=['POST'])
def count_files():
    data = request.json
    
    folder_id = data.get('folder_id')  # Replace with the ID of your Google Drive folder
    
    # Fetch the list of files in the folder
    response = build('drive', 'v3', credentials=authenticate_gdrive()).files().list(q=f"'{folder_id}' in parents", fields="files(id)").execute()
    
    # Count the number of files
    file_count = len(response.get('files', []))
    
    return jsonify({'file_count': file_count})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)